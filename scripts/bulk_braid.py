#!/usr/bin/env python3
"""
Bulk retrospective braider — clear the provenance backlog.

Stages each dataset from cold HDD → NVMe warm tier, braids at NVMe
speed, then cleans up the staging copy. CAS writes already go to NVMe
via multi-tier content.put (cross-tier dedup prevents re-writes).

Lifecycle per dataset:
  1. rsync cold → /mnt/cas-hot/_stage/{dataset}/  (HDD→NVMe, sequential)
  2. InlineBraid.ingest_file() from staging   (NVMe reads, fast)
  3. finalize (DAG dehydrate → spine commit → bearDog sign → braid)
  4. rm -rf staging copy                       (NVMe freed)
  5. .braided marker written on cold dataset   (idempotent re-runs)

Skips datasets that already have a .braided marker.

Usage:
    python3 bulk_braid.py                     # all datasets
    python3 bulk_braid.py --only kegg,chebi   # specific datasets
    python3 bulk_braid.py --skip alphafold_structures  # skip specific
    python3 bulk_braid.py --dry-run           # list what would run
    python3 bulk_braid.py --no-stage          # braid directly from HDD
"""

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from prov_inline import InlineBraid, convergence_gate

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")
STAGE_ROOT = Path("/mnt/cas-hot/_stage")
SKIP_EXTENSIONS = {".part", ".tmp", ".lock", ".swp"}
SKIP_PREFIXES = (".", "_")
REPORT_INTERVAL = 15
STAGE_MIN_FREE_GB = 20

ALWAYS_SKIP = {"alphafold_structures"}

shutdown = False


def handle_signal(signum, frame):
    global shutdown
    shutdown = True
    print("\n[bulk_braid] Shutdown signal received, finishing current dataset...",
          flush=True)


def should_skip_file(path):
    name = path.name
    if name.startswith(SKIP_PREFIXES):
        return True
    if path.suffix in SKIP_EXTENSIONS:
        return True
    if name.endswith(".meta.json"):
        return True
    return False


def nvme_free_gb():
    st = os.statvfs("/mnt/cas-hot")
    return (st.f_bavail * st.f_frsize) / (1024 ** 3)


def dataset_size_bytes(ds_path):
    total = 0
    for f in ds_path.rglob("*"):
        if f.is_file() and not should_skip_file(f):
            try:
                total += f.stat().st_size
            except OSError:
                pass
    return total


def stage_dataset(dataset_name):
    """rsync dataset from cold HDD to NVMe staging. Returns staging path."""
    src = DATA_ROOT / dataset_name
    dst = STAGE_ROOT / dataset_name

    dst.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["rsync", "-a", "--exclude=.*", f"{src}/", f"{dst}/"],
        capture_output=True, text=True, timeout=7200,
    )

    if result.returncode != 0:
        raise RuntimeError(f"rsync failed: {result.stderr[:200]}")

    return dst


def unstage_dataset(dataset_name):
    """Remove NVMe staging copy."""
    dst = STAGE_ROOT / dataset_name
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)


def braid_dataset(dataset_name, dry_run=False, use_staging=True):
    """Braid a single dataset. Returns result dict."""
    ds_path = DATA_ROOT / dataset_name
    marker = ds_path / ".braided"

    if marker.exists():
        return {"dataset": dataset_name, "status": "skipped", "reason": "already braided"}

    files_src = sorted(
        f for f in ds_path.rglob("*")
        if f.is_file() and not should_skip_file(f)
    )

    if not files_src:
        return {"dataset": dataset_name, "status": "skipped", "reason": "no files"}

    if dry_run:
        total_bytes = sum(f.stat().st_size for f in files_src)
        return {
            "dataset": dataset_name, "status": "dry_run",
            "file_count": len(files_src),
            "size_gb": round(total_bytes / (1024**3), 1),
        }

    tag = f"[{dataset_name}]"
    staged_path = None

    gate = convergence_gate(dataset_name, warm_min_free_gb=STAGE_MIN_FREE_GB)
    if gate["verdict"] == "STOP":
        print(f"{tag} STOPPED by backpressure: {gate['reason']}", flush=True)
        return {"dataset": dataset_name, "status": "backpressure_stop", "reason": gate["reason"]}

    if use_staging:
        free = nvme_free_gb()
        if free < STAGE_MIN_FREE_GB:
            print(f"{tag} NVMe only {free:.0f} GB free, braiding from HDD", flush=True)
            use_staging = False

    if use_staging:
        print(f"{tag} Staging {len(files_src)} files → NVMe...", flush=True)
        t_stage = time.time()
        try:
            staged_path = stage_dataset(dataset_name)
            stage_elapsed = time.time() - t_stage
            print(f"{tag} Staged in {stage_elapsed:.0f}s", flush=True)
        except Exception as e:
            print(f"{tag} Stage failed ({e}), falling back to HDD", flush=True,
                  file=sys.stderr)
            staged_path = None

    braid_root = staged_path if staged_path else ds_path
    files = sorted(
        f for f in braid_root.rglob("*")
        if f.is_file() and not should_skip_file(f)
    )

    if not files:
        if staged_path:
            unstage_dataset(dataset_name)
        return {"dataset": dataset_name, "status": "skipped", "reason": "no files after staging"}

    print(f"{tag} Braiding: {len(files)} files from "
          f"{'NVMe' if staged_path else 'HDD'}", flush=True)

    t_start = time.time()
    last_report = t_start

    try:
        braid = InlineBraid(dataset_name)
    except RuntimeError as e:
        print(f"{tag} FATAL: {e}", file=sys.stderr, flush=True)
        if staged_path:
            unstage_dataset(dataset_name)
        return {"dataset": dataset_name, "status": "error", "error": str(e)}

    for i, fp in enumerate(files):
        if shutdown:
            print(f"{tag} Interrupted at {i}/{len(files)}", flush=True)
            break

        try:
            braid.ingest_file(fp)
        except Exception as e:
            braid.errors += 1
            if braid.errors <= 5:
                print(f"{tag} Error on {fp.name}: {e}", file=sys.stderr, flush=True)

        now = time.time()
        if now - last_report > REPORT_INTERVAL:
            elapsed = now - t_start
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            pct = (i + 1) / len(files) * 100
            print(f"{tag} {i+1}/{len(files)} ({pct:.0f}%) rate={rate:.1f}/s "
                  f"errors={braid.errors}", flush=True)
            last_report = now

    if staged_path:
        unstage_dataset(dataset_name)

    if shutdown:
        return {
            "dataset": dataset_name,
            "status": "interrupted",
            "processed": i + 1,
            "total": len(files),
        }

    result = braid.finalize()
    elapsed = time.time() - t_start
    rate = len(files) / elapsed if elapsed > 0 else 0

    marker.write_text(json.dumps({
        "dataset": dataset_name,
        "file_count": len(files),
        "event_count": result.get("event_count", 0),
        "merkle_root": str(result.get("merkle_root", "")),
        "session_id": result.get("session_id", ""),
        "spine_id": result.get("spine_id", ""),
        "braided_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "elapsed_s": round(elapsed, 1),
        "rate": round(rate, 1),
        "errors": result.get("errors", 0),
        "staged": bool(staged_path),
    }, indent=2) + "\n")

    print(f"{tag} DONE: {result.get('event_count', 0)} events, "
          f"{rate:.1f}/s, {result.get('errors', 0)} errors, "
          f"{elapsed:.0f}s {'(NVMe)' if staged_path else '(HDD)'}", flush=True)

    return {
        "dataset": dataset_name,
        "status": "braided",
        "file_count": len(files),
        "event_count": result.get("event_count", 0),
        "rate": round(rate, 1),
        "elapsed": round(elapsed, 1),
        "errors": result.get("errors", 0),
        "merkle_root": str(result.get("merkle_root", "")),
        "staged": bool(staged_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Bulk retrospective braider")
    parser.add_argument("--only", help="Comma-separated list of datasets to braid")
    parser.add_argument("--skip", help="Comma-separated list of datasets to skip")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-stage", action="store_true",
                        help="Skip NVMe staging, braid directly from HDD")
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    all_datasets = sorted(
        d.name for d in DATA_ROOT.iterdir()
        if d.is_dir() and d.name not in ALWAYS_SKIP
    )

    if args.only:
        selected = set(args.only.split(","))
        all_datasets = [d for d in all_datasets if d in selected]

    if args.skip:
        skip = set(args.skip.split(","))
        all_datasets = [d for d in all_datasets if d not in skip]

    already = sum(1 for d in all_datasets if (DATA_ROOT / d / ".braided").exists())
    remaining = [d for d in all_datasets if not (DATA_ROOT / d / ".braided").exists()]

    print(f"=== Bulk Braid {'(NVMe staged)' if not args.no_stage else '(HDD direct)'} ===",
          flush=True)
    print(f"Total datasets: {len(all_datasets)}", flush=True)
    print(f"Already braided: {already}", flush=True)
    print(f"To process: {len(remaining)}", flush=True)
    if not args.no_stage:
        print(f"NVMe free: {nvme_free_gb():.0f} GB", flush=True)
    print(flush=True)

    if args.dry_run:
        total_files = 0
        total_gb = 0
        for ds in remaining:
            r = braid_dataset(ds, dry_run=True)
            fc = r.get("file_count", 0)
            gb = r.get("size_gb", 0)
            total_files += fc
            total_gb += gb
            if fc > 0:
                print(f"  {r['dataset']}: {fc} files ({gb} GB)")
        print(f"\nTotal: {total_files:,} files, {total_gb:.1f} GB")
        return

    t_start = time.time()
    results = []

    for ds in remaining:
        if shutdown:
            break
        results.append(braid_dataset(ds, use_staging=not args.no_stage))

    wall = time.time() - t_start
    braided = [r for r in results if r["status"] == "braided"]
    errors = [r for r in results if r["status"] == "error"]
    skipped = [r for r in results if r["status"] == "skipped"]

    print(f"\n=== BULK BRAID COMPLETE ===", flush=True)
    print(f"Braided:  {len(braided)}", flush=True)
    print(f"Skipped:  {len(skipped)}", flush=True)
    print(f"Errors:   {len(errors)}", flush=True)
    print(f"Wall:     {wall:.0f}s ({wall/3600:.1f}h)", flush=True)

    total_events = sum(r.get("event_count", 0) for r in braided)
    total_errors = sum(r.get("errors", 0) for r in braided)
    print(f"Total events: {total_events:,}", flush=True)
    print(f"Total file errors: {total_errors}", flush=True)

    if errors:
        print(f"\nFailed datasets:", flush=True)
        for r in errors:
            print(f"  {r['dataset']}: {r.get('error', 'unknown')}", flush=True)


if __name__ == "__main__":
    main()
