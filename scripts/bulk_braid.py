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
from prov_inline import InlineBraid, ChunkedBraid, convergence_gate

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")
STAGE_ROOT = Path("/mnt/cas-hot/_stage")
SKIP_EXTENSIONS = {".part", ".tmp", ".lock", ".swp"}
SKIP_PREFIXES = (".", "_")
REPORT_INTERVAL = 15
STAGE_MIN_FREE_GB = 20

ALWAYS_SKIP = set()
CHUNK_STAGE_THRESHOLD = 50000

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


def probe_dir_size(path, file_cap=500_000, time_cap=30):
    """Quick probe: count files and bytes, abort if over caps.

    Returns (file_count, byte_count, capped) — capped=True means the
    directory exceeds the cap and actual totals are higher.
    """
    count = 0
    total = 0
    t0 = time.time()
    try:
        for f in path.rglob("*"):
            if not f.is_file() or should_skip_file(f):
                continue
            count += 1
            try:
                total += f.stat().st_size
            except OSError:
                pass
            if count >= file_cap or (time.time() - t0) > time_cap:
                return count, total, True
    except Exception:
        pass
    return count, total, False


MAX_STAGE_BYTES = 500 * 1024**3  # 500 GB — leave headroom on NVMe


def stage_path(src, dst_name):
    """rsync a path from cold HDD to NVMe staging. Returns staging path."""
    dst = STAGE_ROOT / dst_name
    dst.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["rsync", "-a", "--exclude=.*", f"{src}/", f"{dst}/"],
        capture_output=True, text=True, timeout=86400,
    )

    if result.returncode != 0:
        raise RuntimeError(f"rsync failed: {result.stderr[:200]}")

    return dst


def stage_dataset(dataset_name):
    """rsync entire dataset from cold HDD to NVMe staging."""
    return stage_path(DATA_ROOT / dataset_name, dataset_name)


def unstage_dataset(dataset_name):
    """Remove NVMe staging copy."""
    dst = STAGE_ROOT / dataset_name
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)


def has_subdirs(ds_path):
    """Check if dataset has subdirectory structure (prefix dirs)."""
    for entry in ds_path.iterdir():
        if entry.is_dir() and not entry.name.startswith("."):
            return True
    return False


def braid_chunked(dataset_name, use_staging=True):
    """Braid a large dataset using ChunkedBraid — one spine, N sessions.

    Each subdirectory becomes a chunk with its own rhizoCrypt session,
    dehydrated and committed to a shared loamSpine. Crash-resumable via
    .braid_state persisted after each chunk commit.
    """
    ds_path = DATA_ROOT / dataset_name
    marker = ds_path / ".braided"
    if marker.exists():
        return {"dataset": dataset_name, "status": "skipped", "reason": "already braided"}

    tag = f"[{dataset_name}]"
    subdirs = sorted(
        d.name for d in ds_path.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    cb = ChunkedBraid(dataset_name, state_dir=ds_path)
    already_done = sum(1 for s in subdirs if cb.is_chunk_done(s))

    print(f"{tag} Chunked braid: {len(subdirs)} subdirectories, "
          f"{already_done} already committed (resume)", flush=True)

    t_start = time.time()

    for si, subdir_name in enumerate(subdirs):
        if shutdown:
            break
        if cb.is_chunk_done(subdir_name):
            continue

        subdir_src = ds_path / subdir_name
        chunk_tag = f"{tag}[{subdir_name} {si+1}/{len(subdirs)}]"

        braid_root = subdir_src
        staged = False
        if use_staging:
            free = nvme_free_gb()
            if free < STAGE_MIN_FREE_GB:
                print(f"{chunk_tag} NVMe {free:.0f} GB free — reading from HDD", flush=True)
            else:
                fcount, fbytes, capped = probe_dir_size(subdir_src)
                est_gb = fbytes / (1024**3)
                if capped or fbytes > MAX_STAGE_BYTES or fbytes > free * 0.8 * (1024**3):
                    print(f"{chunk_tag} Oversized chunk (~{fcount:,} files, "
                          f"~{est_gb:.0f} GB{'+' if capped else ''}), "
                          f"braiding from HDD", flush=True)
                else:
                    print(f"{chunk_tag} Staging → NVMe "
                          f"({fcount:,} files, {est_gb:.1f} GB)...", flush=True)
                    t_stg = time.time()
                    try:
                        braid_root = stage_path(subdir_src, f"{dataset_name}/{subdir_name}")
                        staged = True
                        print(f"{chunk_tag} Staged in {time.time() - t_stg:.0f}s", flush=True)
                    except Exception as e:
                        print(f"{chunk_tag} Stage failed ({e}), HDD fallback", flush=True)
                        braid_root = subdir_src

        files = sorted(
            f for f in braid_root.rglob("*")
            if f.is_file() and not should_skip_file(f)
        )

        cb.begin_chunk(subdir_name)
        chunk_files = 0
        for fi, fp in enumerate(files):
            if shutdown:
                break
            try:
                cb.ingest_file(fp)
                chunk_files += 1
            except Exception as e:
                cb.total_errors += 1
                if cb.total_errors <= 10:
                    print(f"{chunk_tag} Error: {fp.name}: {e}", flush=True)
            if (fi + 1) % 500 == 0:
                elapsed = time.time() - t_start
                total_so_far = cb.total_files + chunk_files
                rate = total_so_far / elapsed if elapsed > 0 else 0
                print(f"{chunk_tag} [{fi+1}/{len(files)}] "
                      f"total={total_so_far} ({rate:.1f}/s)", flush=True)

        result = cb.commit_chunk()
        elapsed = time.time() - t_start
        rate = cb.total_files / elapsed if elapsed > 0 else 0
        print(f"{chunk_tag} Committed: {result['files']} files, "
              f"root={str(result.get('merkle_root', ''))[:16]}... "
              f"({rate:.1f}/s cumulative)", flush=True)

        if staged:
            staged_chunk = STAGE_ROOT / dataset_name / subdir_name
            if staged_chunk.exists():
                shutil.rmtree(staged_chunk, ignore_errors=True)

    if shutdown:
        print(f"{tag} Interrupted — {len(cb.completed_chunks)}/{len(subdirs)} "
              f"chunks committed to spine. Resume will continue.", flush=True)
        unstage_dataset(dataset_name)
        return {
            "dataset": dataset_name,
            "status": "interrupted",
            "chunks_done": len(cb.completed_chunks),
            "chunks_total": len(subdirs),
            "files": cb.total_files,
            "errors": cb.total_errors,
        }

    result = cb.finalize()

    marker_data = {
        "braided_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "files": result["total_files"],
        "errors": result["total_errors"],
        "elapsed_s": round(time.time() - t_start),
        "spine_id": result["spine_id"],
        "chunk_count": result["chunk_count"],
        "signature": result.get("signature"),
    }
    with open(marker, "w") as f:
        json.dump(marker_data, f, indent=2)

    elapsed = time.time() - t_start
    print(f"{tag} COMPLETE: {result['total_files']} files across "
          f"{result['chunk_count']} chunks, {result['total_errors']} errors, "
          f"{elapsed:.0f}s", flush=True)

    unstage_dataset(dataset_name)
    return {
        "dataset": dataset_name,
        "status": "complete",
        "files": result["total_files"],
        "errors": result["total_errors"],
        "chunk_count": result["chunk_count"],
        "elapsed_s": round(elapsed),
        "spine_id": result["spine_id"],
    }


def braid_dataset(dataset_name, dry_run=False, use_staging=True):
    """Braid a single dataset. Routes to chunked braiding for large datasets."""
    ds_path = DATA_ROOT / dataset_name
    marker = ds_path / ".braided"

    if marker.exists():
        return {"dataset": dataset_name, "status": "skipped", "reason": "already braided"}

    if has_subdirs(ds_path) and not dry_run:
        return braid_chunked(dataset_name, use_staging=use_staging)

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
        braid = ChunkedBraid(dataset_name, state_dir=ds_path)
        braid.begin_chunk("_flat")
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
            braid.total_errors += 1
            if braid.total_errors <= 5:
                print(f"{tag} Error on {fp.name}: {e}", file=sys.stderr, flush=True)

        now = time.time()
        if now - last_report > REPORT_INTERVAL:
            elapsed = now - t_start
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            pct = (i + 1) / len(files) * 100
            print(f"{tag} {i+1}/{len(files)} ({pct:.0f}%) rate={rate:.1f}/s "
                  f"errors={braid.total_errors}", flush=True)
            last_report = now

    if staged_path:
        unstage_dataset(dataset_name)

    if shutdown:
        braid.commit_chunk()
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
        "total_files": result.get("total_files", 0),
        "spine_id": result.get("spine_id", ""),
        "chunk_count": result.get("chunk_count", 1),
        "braided_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "elapsed_s": round(elapsed, 1),
        "rate": round(rate, 1),
        "errors": result.get("total_errors", 0),
        "staged": bool(staged_path),
    }, indent=2) + "\n")

    print(f"{tag} DONE: {result.get('total_files', 0)} events, "
          f"{rate:.1f}/s, {result.get('total_errors', 0)} errors, "
          f"{elapsed:.0f}s {'(NVMe)' if staged_path else '(HDD)'}", flush=True)

    return {
        "dataset": dataset_name,
        "status": "braided",
        "file_count": len(files),
        "total_files": result.get("total_files", 0),
        "rate": round(rate, 1),
        "elapsed": round(elapsed, 1),
        "errors": result.get("total_errors", 0),
        "spine_id": result.get("spine_id", ""),
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

    if args.only:
        selected = set(args.only.split(","))
        all_datasets = sorted(
            d.name for d in DATA_ROOT.iterdir()
            if d.is_dir() and d.name in selected
        )
    else:
        all_datasets = sorted(
            d.name for d in DATA_ROOT.iterdir()
            if d.is_dir() and d.name not in ALWAYS_SKIP
        )

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
    braided = [r for r in results if r["status"] in ("braided", "complete")]
    errors = [r for r in results if r["status"] == "error"]
    skipped = [r for r in results if r["status"] == "skipped"]

    print(f"\n=== BULK BRAID COMPLETE ===", flush=True)
    print(f"Braided:  {len(braided)}", flush=True)
    print(f"Skipped:  {len(skipped)}", flush=True)
    print(f"Errors:   {len(errors)}", flush=True)
    print(f"Wall:     {wall:.0f}s ({wall/3600:.1f}h)", flush=True)

    total_events = sum(r.get("total_files", r.get("event_count", 0)) for r in braided)
    total_errors = sum(r.get("errors", 0) for r in braided)
    print(f"Total events: {total_events:,}", flush=True)
    print(f"Total file errors: {total_errors}", flush=True)

    if errors:
        print(f"\nFailed datasets:", flush=True)
        for r in errors:
            print(f"  {r['dataset']}: {r.get('error', 'unknown')}", flush=True)


if __name__ == "__main__":
    main()
