#!/usr/bin/env python3
"""
Manifest-Driven Data Acquisition — replaces metered_download.sh

Reads DataManifest TOML files and executes the full acquisition pipeline:
  1. InlineBraid init (native socket DAG session + spine creation)
  2. For each entry: fetch → braid.ingest_file (BLAKE3 + CAS + DAG batch)
  3. Automatic batch flush + partial dehydration checkpoints
  4. braid.finalize() (dehydrate → session.commit → sign → braid)

Inline provenance: native Python socket RPC (16K RPCs/s), in-process BLAKE3
hashing, single file read for hash + CAS. No socat subprocess spawning.
Measured at 265 files/s warm, 3.6x headroom over download rate.

Bandwidth governance: respects rate_limit_mbps from manifest and queries
topology.bandwidth.budget before starting (when available).

Usage:
  python3 manifest_download.py /path/to/manifest.toml
  python3 manifest_download.py --manifest-dir /path/to/manifests/
  python3 manifest_download.py --list  # show all manifests and status
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

sys.path.insert(0, str(Path(__file__).parent))
from prov_inline import InlineBraid, convergence_gate, convergence_wait

DEFAULT_MANIFEST_DIR = Path(__file__).parent.parent / "manifests"
LOG_FILE = Path("/tmp/manifest_download.log")


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} — {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_manifest(path):
    """Load and validate a DataManifest TOML."""
    with open(path, "rb") as f:
        data = tomllib.load(f)
    m = data.get("manifest", {})
    if not m.get("dataset"):
        raise ValueError(f"Manifest {path} missing [manifest].dataset")
    return data


def resolve_entries(manifest):
    """Resolve the entries to download from the manifest's entries_source."""
    m = manifest["manifest"]
    src = m.get("entries_source", {})
    src_type = src.get("type", "inline")

    if src_type in ("csv", "tsv"):
        return resolve_csv_entries(m, src)
    elif src_type == "inline":
        return manifest.get("manifest", {}).get("entries", [])
    elif src_type == "single":
        return [{"url": src.get("url", ""), "dest": src.get("dest", "")}]
    elif src_type == "glob":
        pattern = src.get("path", "")
        files = sorted(Path("/").glob(pattern.lstrip("/")))
        return [{"path": str(f), "id": f.name} for f in files if f.is_file()]
    else:
        log(f"  Unknown entries_source type: {src_type}")
        return []


def resolve_csv_entries(manifest, src):
    """Resolve entries from a CSV/TSV file with URL template."""
    csv_path = Path(src.get("path", ""))
    if not csv_path.exists():
        log(f"  Entries CSV not found: {csv_path}")
        return []

    url_template = src.get("url_template", "")
    columns = src.get("columns", {})
    delimiter = src.get("delimiter", ",")
    has_header = src.get("header", True)

    entries = []
    with open(csv_path, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader)
            col_map = {name: int(idx) if isinstance(idx, (int, float)) else header.index(str(idx))
                       for name, idx in columns.items()}
        else:
            col_map = {name: int(idx) for name, idx in columns.items()}

        for row in reader:
            if not row:
                continue
            entry = {}
            for name, idx in col_map.items():
                if idx < len(row):
                    entry[name] = row[idx]
            if url_template:
                try:
                    entry["url"] = url_template.format(**entry)
                except KeyError:
                    continue
            entry["id"] = entry.get("id", entry.get("af_id", entry.get("uniprot_id", "")))
            entries.append(entry)

    return entries


def check_bandwidth_budget(rate_limit_mbps):
    """Query topology.bandwidth.budget if available. Returns effective rate."""
    # Phase 3 (Option A): when cellMembrane implements topology.bandwidth.*,
    # this function will query it. For now, use the manifest's rate_limit_mbps.
    return rate_limit_mbps


def download_file(url, dest_path, rate_limit_mbps=None):
    """Download a file with curl, respecting rate limits and resume."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        try:
            head = subprocess.run(
                ["curl", "-sI", url],
                capture_output=True, text=True, timeout=30,
            )
            for line in head.stdout.split("\n"):
                if "content-length" in line.lower():
                    expected = int(line.split(":")[1].strip())
                    actual = dest_path.stat().st_size
                    if actual >= expected:
                        return True, "already_complete"
        except Exception:
            pass

    cmd = ["curl", "-L", "-C", "-", "-o", str(dest_path)]
    if rate_limit_mbps:
        rate_bytes = int(rate_limit_mbps * 125_000)
        cmd.extend(["--limit-rate", f"{rate_bytes}"])
    cmd.append(url)

    try:
        subprocess.run(cmd, timeout=86400, check=True)
        return True, "downloaded"
    except subprocess.CalledProcessError as e:
        return False, f"curl_error_{e.returncode}"
    except subprocess.TimeoutExpired:
        return False, "timeout"


def run_manifest(manifest_path):
    """Execute a single DataManifest: declare → acquire → complete."""
    manifest = load_manifest(manifest_path)
    m = manifest["manifest"]
    dataset = m["dataset"]
    display = m.get("display_name", dataset)
    acq = m.get("acquisition", {})
    storage = m.get("storage", {})
    prov = m.get("provenance", {})

    method = acq.get("method", "http_bulk")
    rate_limit = acq.get("rate_limit_mbps", 400)
    checkpoint_interval = acq.get("checkpoint_interval", 5000)
    license_id = m.get("license", "CC0-1.0")

    base_path = Path(storage.get("base_path", "/mnt/nestgate/cold/zfs/data"))
    subdir = storage.get("subdirectory", dataset)
    dest_dir = base_path / subdir

    effective_rate = check_bandwidth_budget(rate_limit)

    log(f"{'=' * 70}")
    log(f"  MANIFEST ACQUISITION — {display}")
    log(f"  Dataset:    {dataset}")
    log(f"  Method:     {method}")
    log(f"  Rate limit: {effective_rate} Mbps")
    log(f"  Dest:       {dest_dir}")
    log(f"{'=' * 70}")

    # 1. Resolve entries
    entries = resolve_entries(manifest)
    if not entries:
        log(f"  No entries resolved — check entries_source in manifest")
        return

    total = len(entries)
    log(f"  Entries:    {total}")

    # 2. Init InlineBraid (native socket DAG session + spine)
    log(f"  [DECLARE] Initializing inline braid (native sockets)...")
    try:
        braid = InlineBraid(dataset, checkpoint_interval=checkpoint_interval or 2000)
    except RuntimeError as e:
        log(f"  FAIL — {e}")
        return
    log(f"  Session:    {braid.session_id}")
    log(f"  Spine:      {braid.spine_id}")

    # 3. Acquire each entry — braid inline while file is still in page cache
    acquired = 0
    skipped = 0
    failed = 0
    backpressure_check_interval = prov.get("backpressure_batch", 100)
    convergence_lag_max_val = prov.get("convergence_lag_max", 10000)
    warm_min_free = prov.get("warm_min_free_gb", 20.0)

    for i, entry in enumerate(entries):
        if i % backpressure_check_interval == 0:
            gate = convergence_wait(
                dataset,
                warm_min_free_gb=warm_min_free,
                convergence_lag_max=convergence_lag_max_val,
            )
            if gate["verdict"] == "STOP":
                log(f"  STOPPED by backpressure: {gate['reason']}")
                break
            if gate.get("waited_seconds"):
                log(f"  Backpressure cleared after {gate['waited_seconds']}s")
        url = entry.get("url", "")
        entry_id = entry.get("id", f"entry_{i}")

        if method == "local":
            file_path = Path(entry.get("path", ""))
        elif method in ("http_bulk", "api"):
            if not url:
                continue
            filename = url.split("/")[-1] or f"{entry_id}.dat"
            file_path = dest_dir / filename

            ok, status = download_file(url, file_path, effective_rate)
            if not ok:
                log(f"  [{i+1}/{total}] {entry_id:40s} FAIL ({status})")
                failed += 1
                continue
            if status == "already_complete":
                skipped += 1
        else:
            file_path = Path(entry.get("path", ""))

        if not file_path.exists():
            log(f"  [{i+1}/{total}] {entry_id:40s} SKIP (not on disk)")
            skipped += 1
            continue

        braid.ingest_file(file_path)
        acquired += 1

        if (i + 1) % 100 == 0 or i == total - 1:
            stats = braid.stats()
            log(f"  [{i+1}/{total}] acquired={acquired} skipped={skipped} "
                f"failed={failed} events={stats['event_count']}")

    # 4. Finalize (dehydrate → spine commit → sign → braid)
    log(f"  [COMPLETE] Finalizing ({braid.event_count} events)...")
    result = braid.finalize(license_id=license_id)

    log(f"")
    log(f"  RESULTS — {display}")
    log(f"    Acquired:     {acquired}")
    log(f"    Skipped:      {skipped}")
    log(f"    Failed:       {failed}")
    log(f"    DAG events:   {result['event_count']}")
    log(f"    Merkle root:  {result['merkle_root'] or 'NONE'}")
    log(f"    Signature:    {'YES' if result['signature'] else 'NO'}")
    log(f"    Session:      {result['session_id']}")
    log(f"    Spine:        {result['spine_id']}")
    log(f"    Errors:       {result['errors']}")
    log(f"{'=' * 70}")


def list_manifests(manifest_dir):
    """List all manifests and their status."""
    print(f"\n{'Dataset':40s} {'Method':12s} {'Expected':>12s} {'License':12s}")
    print("-" * 80)
    for f in sorted(manifest_dir.glob("*.toml")):
        try:
            m = load_manifest(f)["manifest"]
            dataset = m.get("dataset", "?")
            method = m.get("acquisition", {}).get("method", "?")
            expected = m.get("expected_total", 0)
            license_id = m.get("license", "?")
            print(f"{dataset:40s} {method:12s} {expected:>12,} {license_id:12s}")
        except Exception as e:
            print(f"{f.name:40s} ERROR: {e}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Manifest-driven data acquisition with full provenance"
    )
    parser.add_argument("manifest", nargs="?", help="Path to a DataManifest TOML")
    parser.add_argument("--manifest-dir", type=str, help="Directory of manifests to process")
    parser.add_argument("--list", action="store_true", help="List all manifests")
    args = parser.parse_args()

    if args.list:
        manifest_dir = Path(args.manifest_dir) if args.manifest_dir else DEFAULT_MANIFEST_DIR
        list_manifests(manifest_dir)
        return

    if args.manifest:
        run_manifest(Path(args.manifest))
    elif args.manifest_dir:
        manifest_dir = Path(args.manifest_dir)
        for f in sorted(manifest_dir.glob("*.toml")):
            log(f"\nProcessing manifest: {f.name}")
            try:
                run_manifest(f)
            except Exception as e:
                log(f"  ERROR processing {f.name}: {e}")
    else:
        run_manifest_dir = DEFAULT_MANIFEST_DIR
        if run_manifest_dir.exists():
            for f in sorted(run_manifest_dir.glob("*.toml")):
                log(f"\nProcessing manifest: {f.name}")
                try:
                    run_manifest(f)
                except Exception as e:
                    log(f"  ERROR processing {f.name}: {e}")
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
