#!/usr/bin/env python3
"""
Manifest-Driven Data Acquisition — replaces metered_download.sh

Reads DataManifest TOML files and executes the full acquisition pipeline:
  1. nest.declare_dataset (DAG session + spine creation)
  2. For each entry: fetch → BLAKE3 → CAS → DAG event (no per-file spine)
  3. Partial dehydration checkpoints
  4. nest.complete_dataset (dehydrate → session.commit → sign → braid)

Canonical provenance: per-file CAS+DAG only, session-level spine commit.
See PROVENANCE_TRIO_ARCHITECTURE.md for the canonical pipeline.

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
from bulk_ingest import (
    rpc, rpc_result, blake3_hash, cas_put,
    dag_session_create, dag_event_append, dag_partial_dehydrate,
    dag_dehydrate, spine_create,
    spine_session_commit, sign_merkle_root, braid_create,
    hex_to_content_hash,
)

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

    # 2. Create DAG session (nest.declare_dataset)
    log(f"  [DECLARE] Creating DAG session...")
    session_id = dag_session_create(dataset)
    if not session_id:
        log(f"  FAIL — rhizoCrypt unreachable")
        return
    log(f"  Session:    {session_id}")

    log(f"  [DECLARE] Creating spine...")
    spine_id = spine_create(dataset)
    if not spine_id:
        log(f"  FAIL — loamSpine unreachable")
        return
    log(f"  Spine:      {spine_id}")

    # 3. Create intent braid
    manifest_bytes = manifest_path.read_bytes()
    import hashlib
    manifest_hash = hashlib.blake2b(manifest_bytes, digest_size=32).hexdigest()
    braid_create(
        b3hash=manifest_hash,
        mime_type="application/toml",
        size=len(manifest_bytes),
        dataset=f"{dataset} (intent)",
        license_id=license_id,
        session_id=session_id,
    )
    log(f"  [DECLARE] Intent braid created")

    # 4. Acquire each entry
    event_count = 0
    acquired = 0
    skipped = 0
    failed = 0

    for i, entry in enumerate(entries):
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

        # BLAKE3 hash
        b3 = blake3_hash(file_path)
        size = file_path.stat().st_size

        # CAS store
        cas_put(file_path, b3)

        # DAG event (per-file; spine commit is session-level at dehydration)
        vertex = dag_event_append(session_id, b3, file_path.name, size, dataset)
        if vertex:
            event_count += 1

        acquired += 1

        if (i + 1) % 100 == 0 or i == total - 1:
            log(f"  [{i+1}/{total}] acquired={acquired} skipped={skipped} failed={failed}")

        # Checkpoint
        if checkpoint_interval > 0 and event_count > 0 and event_count % checkpoint_interval == 0:
            log(f"  [CHECKPOINT] Partial dehydration at {event_count} events")
            partial = dag_partial_dehydrate(session_id)
            if partial:
                merkle = partial.get("merkle_root", partial) if isinstance(partial, dict) else partial
                log(f"    root={str(merkle)[:16]}...")

    # 5. Finalize (nest.complete_dataset)
    log(f"  [COMPLETE] Dehydrating DAG session ({event_count} events)...")
    merkle_root = dag_dehydrate(session_id)
    merkle_hex = merkle_root if isinstance(merkle_root, str) else str(merkle_root) if merkle_root else None

    if merkle_hex and spine_id:
        log(f"  [COMPLETE] Committing to spine...")
        spine_session_commit(spine_id, session_id, merkle_hex, event_count)

    if merkle_hex:
        log(f"  [COMPLETE] Signing Merkle root...")
        sign_merkle_root(merkle_hex, dataset)

    log(f"  [COMPLETE] Creating final braid...")
    braid_create(
        b3hash=merkle_hex or "0" * 64,
        mime_type="application/x-dataset",
        size=0,
        dataset=dataset,
        license_id=license_id,
        session_id=session_id,
        merkle_root=merkle_hex,
    )

    log(f"")
    log(f"  RESULTS — {display}")
    log(f"    Acquired:     {acquired}")
    log(f"    Skipped:      {skipped}")
    log(f"    Failed:       {failed}")
    log(f"    DAG events:   {event_count}")
    log(f"    Merkle root:  {merkle_hex or 'NONE'}")
    log(f"    Session:      {session_id}")
    log(f"    Spine:        {spine_id}")
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
