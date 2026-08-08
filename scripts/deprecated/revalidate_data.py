#!/usr/bin/env python3
"""
Data Revalidation — Re-ingest existing datasets through the canonical provenance chain.

Walks all dataset directories on ZFS and creates genuine:
  - rhizoCrypt DAG sessions with per-file events
  - DAG dehydration (Merkle roots)
  - loamSpine session commits (one per dataset, carries Merkle root)
  - bearDog Ed25519 signatures
  - sweetGrass attribution braids with source_session linking

No per-file spine entries — the DAG Merkle root binds all files.
See PROVENANCE_TRIO_ARCHITECTURE.md for architectural rationale.

Usage:
  python3 revalidate_data.py                    # all datasets
  python3 revalidate_data.py --dataset chembl37  # single dataset
  python3 revalidate_data.py --dry-run           # list what would be processed
  python3 revalidate_data.py --max-files 50      # limit files per dataset (for testing)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from prov_inline import InlineBraid

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")
REPORT_DIR = Path("/tmp/revalidation_reports")
CHECKPOINT_INTERVAL = 500


def scan_dataset(dataset_path):
    """Find all data files in a dataset directory."""
    files = []
    for f in sorted(dataset_path.rglob("*")):
        if f.is_file() and not f.name.startswith("."):
            files.append(f)
    return files


def revalidate_dataset(dataset_name, dataset_path, max_files=None):
    """Re-ingest a single dataset through the full provenance chain via InlineBraid."""
    files = scan_dataset(dataset_path)
    if not files:
        return None

    if max_files:
        files = files[:max_files]

    total = len(files)
    total_bytes = sum(f.stat().st_size for f in files)

    print(f"\n  {'=' * 60}")
    print(f"  REVALIDATE: {dataset_name}")
    print(f"  Files: {total}  |  Size: {total_bytes / 1024 / 1024:.1f} MB")
    print(f"  {'=' * 60}")

    try:
        braid = InlineBraid(dataset_name, checkpoint_interval=CHECKPOINT_INTERVAL)
    except RuntimeError as e:
        print(f"  FAIL: {e}")
        return {"dataset": dataset_name, "status": "fail", "reason": str(e)}

    t_start = time.time()

    for i, filepath in enumerate(files):
        try:
            braid.ingest_file(filepath)
        except Exception as e:
            print(f"  [{i+1}/{total}] {filepath.name}  FAIL: {e}")
            continue

        if (i + 1) % 50 == 0 or i == total - 1:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            stats = braid.stats()
            print(f"  [{i+1}/{total}] events={stats['event_count']} "
                  f"({rate:.1f} files/s)")

    print(f"  [FINALIZE] Dehydrating {braid.event_count} events...", flush=True)
    result = braid.finalize()

    merkle_hex = result.get("merkle_root")
    wall = time.time() - t_start

    summary = {
        "dataset": dataset_name,
        "status": "ok" if merkle_hex else "partial",
        "files": total,
        "total_bytes": total_bytes,
        "dag_events": result["event_count"],
        "session_id": result["session_id"],
        "spine_id": result["spine_id"],
        "merkle_root": merkle_hex,
        "signed": bool(result.get("signature")),
        "braided": bool(result.get("braid")),
        "errors": result["errors"],
        "wall_seconds": round(wall, 1),
    }

    print(f"  RESULT: {summary['status'].upper()} | "
          f"merkle={str(merkle_hex)[:16]}... | "
          f"events={summary['dag_events']}/{total} | "
          f"{wall:.1f}s")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Revalidate existing data through real provenance chain")
    parser.add_argument("--dataset", type=str, help="Single dataset to revalidate")
    parser.add_argument("--dry-run", action="store_true", help="List datasets without processing")
    parser.add_argument("--max-files", type=int, default=None, help="Max files per dataset")
    parser.add_argument("--skip-large", action="store_true", help="Skip datasets > 10 GB")
    args = parser.parse_args()

    if not DATA_ROOT.exists():
        print(f"Data root not found: {DATA_ROOT}")
        sys.exit(1)

    # Discover datasets
    if args.dataset:
        datasets = [(args.dataset, DATA_ROOT / args.dataset)]
        if not datasets[0][1].exists():
            print(f"Dataset not found: {datasets[0][1]}")
            sys.exit(1)
    else:
        datasets = sorted(
            [(d.name, d) for d in DATA_ROOT.iterdir() if d.is_dir()],
            key=lambda x: sum(f.stat().st_size for f in x[1].rglob("*") if f.is_file()) if not args.dry_run else 0,
        )

    if args.dry_run:
        print(f"\n{'Dataset':40s} {'Files':>8s} {'Size':>12s}")
        print("-" * 64)
        for name, path in datasets:
            files = list(path.rglob("*"))
            file_count = sum(1 for f in files if f.is_file())
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            size_str = f"{total_size / 1024 / 1024:.1f} MB" if total_size < 1024**3 else f"{total_size / 1024**3:.1f} GB"
            print(f"{name:40s} {file_count:>8d} {size_str:>12s}")
        print(f"\nTotal: {len(datasets)} datasets")
        return

    # Run revalidation
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    t_global = time.time()

    print(f"\n{'#' * 70}")
    print(f"  DATA REVALIDATION — Real Provenance Chain")
    print(f"  Datasets: {len(datasets)}")
    print(f"  Pipeline: BLAKE3 → CAS → DAG event (per file)")
    print(f"            → dehydrate → session.commit → sign → braid (per dataset)")
    print(f"{'#' * 70}")

    for idx, (name, path) in enumerate(datasets):
        if args.skip_large:
            total_size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            if total_size > 10 * 1024**3:
                print(f"\n  SKIP {name} ({total_size / 1024**3:.1f} GB > 10 GB limit)")
                continue

        result = revalidate_dataset(name, path, max_files=args.max_files)
        if result:
            results.append(result)

    # Summary
    wall_global = time.time() - t_global
    ok_count = sum(1 for r in results if r["status"] == "ok")
    partial_count = sum(1 for r in results if r["status"] == "partial")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    total_events = sum(r.get("dag_events", 0) for r in results)
    total_braids = sum(1 for r in results if r.get("braided"))

    print(f"\n{'#' * 70}")
    print(f"  REVALIDATION COMPLETE")
    print(f"{'#' * 70}")
    print(f"  Datasets processed: {len(results)}")
    print(f"  OK:                 {ok_count}")
    print(f"  Partial:            {partial_count}")
    print(f"  Failed:             {fail_count}")
    print(f"  Total DAG events:   {total_events}")
    print(f"  Total braids:       {total_braids}")
    print(f"  Wall time:          {wall_global:.1f}s ({wall_global/60:.1f} min)")
    print(f"{'#' * 70}")

    report_path = REPORT_DIR / f"revalidation_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "datasets": len(results),
            "ok": ok_count,
            "partial": partial_count,
            "failed": fail_count,
            "total_dag_events": total_events,
            "total_braids": total_braids,
            "wall_seconds": round(wall_global, 1),
            "results": results,
        }, f, indent=2)
    print(f"\n  Report: {report_path}")


if __name__ == "__main__":
    main()
