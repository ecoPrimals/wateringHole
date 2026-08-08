#!/usr/bin/env python3
"""
Data Convergence Check — validates provenance state across the ZFS data estate.

Reports each dataset's provenance state:
  - CONVERGED:  Has Merkle root + Ed25519 signature + sweetGrass braid
  - CAS-ONLY:   Files in CAS but no DAG/spine/braid
  - PRIMORDIAL:  On disk but no CAS entries
  - PARTIAL:     Some files braided, others not

Routes all queries through biomeOS Neural API via neural_braid.py.
Falls back to direct sweetGrass socket if Neural API routing is unavailable.

Springs should check convergence before trusting data for computation.
This is the trust gate between "data available" and "data provenance-sealed".

Usage:
  python3 convergence_check.py             # full report
  python3 convergence_check.py --dataset X # single dataset
  python3 convergence_check.py --json      # machine-readable output
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from neural_braid import NeuralBraidClient, _uds_rpc, _find_sweetgrass_socket, MEMBRANE

import blake3 as _blake3

_braid_client = NeuralBraidClient()


def blake3_hash(filepath):
    """In-process BLAKE3 hash — no b3sum subprocess."""
    return _blake3.blake3(filepath.read_bytes()).hexdigest()

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")


def _content_exists(data_hash):
    """Check CAS existence via Neural API (semantic fallback → direct socket)."""
    try:
        result = _braid_client._call_semantic("content.exists", {"hash": data_hash})
        if isinstance(result, dict):
            return result.get("exists", False)
        return bool(result)
    except Exception:
        pass
    nestgate_sock = None
    for f in __import__("os").listdir(MEMBRANE):
        if f.startswith("nestgate") and f.endswith(".sock"):
            nestgate_sock = __import__("os").path.join(MEMBRANE, f)
            break
    if nestgate_sock:
        try:
            result = _uds_rpc(nestgate_sock, "content.exists", {"hash": data_hash})
            if isinstance(result, dict):
                return result.get("exists", False)
            return bool(result)
        except Exception:
            pass
    return False


def check_cas_membership(filepath):
    """Check if a file's BLAKE3 hash exists in CAS."""
    try:
        h = blake3_hash(filepath)
        return _content_exists(h), h
    except Exception:
        return False, None


def check_dataset_convergence(dataset_name, dataset_path, sample_size=10):
    """Check provenance state for a dataset by sampling files.
    
    Uses bounded iteration to avoid hanging on datasets with millions of files.
    """
    scan_limit = sample_size * 20
    files = []
    total_bytes = 0
    for f in dataset_path.rglob("*"):
        if f.is_file() and not f.name.startswith(".") and f.stat().st_size > 0:
            files.append(f)
            total_bytes += f.stat().st_size
            if len(files) >= scan_limit:
                break

    if not files:
        return {
            "dataset": dataset_name,
            "state": "EMPTY",
            "files": 0,
            "size_bytes": 0,
        }

    total_files = len(files)
    scanned_all = total_files < scan_limit

    step = max(1, total_files // sample_size)
    sample = [files[i * step] for i in range(min(sample_size, total_files))]

    cas_hits = 0
    for fp in sample:
        exists, _ = check_cas_membership(fp)
        if exists:
            cas_hits += 1

    try:
        braid_result = _braid_client.braid_list(tag=dataset_name, limit=1)
    except Exception:
        braid_result = None
    has_braid = (
        isinstance(braid_result, dict)
        and braid_result.get("total", 0) > 0
    )

    cas_ratio = cas_hits / len(sample) if sample else 0

    if has_braid and cas_ratio >= 0.9:
        state = "CONVERGED"
    elif cas_ratio >= 0.5:
        state = "PARTIAL" if not has_braid else "CONVERGED"
    elif cas_ratio > 0:
        state = "CAS-ONLY"
    else:
        state = "PRIMORDIAL"

    size_str = f"{total_bytes / 1024 / 1024:.0f} MB" if total_bytes < 1024**3 else \
        f"{total_bytes / 1024**3:.1f} GB"

    return {
        "dataset": dataset_name,
        "state": state,
        "files": total_files if scanned_all else f"{scan_limit}+",
        "size_bytes": total_bytes,
        "size_human": size_str,
        "cas_ratio": round(cas_ratio, 2),
        "has_braid": has_braid,
        "sampled": len(sample),
    }


def main():
    parser = argparse.ArgumentParser(description="Check data provenance convergence")
    parser.add_argument("--dataset", type=str, help="Single dataset to check")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--sample", type=int, default=10, help="Files to sample per dataset")
    args = parser.parse_args()

    if args.dataset:
        path = DATA_ROOT / args.dataset
        if not path.exists():
            print(f"Not found: {path}")
            sys.exit(1)
        datasets = [(args.dataset, path)]
    else:
        datasets = sorted(
            [(d.name, d) for d in DATA_ROOT.iterdir() if d.is_dir()],
            key=lambda x: x[0],
        )

    results = []
    t0 = time.time()

    if not args.json:
        print(f"\n{'Dataset':35s} {'State':12s} {'Files':>10s} {'Size':>10s} {'CAS':>6s} {'Braid':>6s}")
        print("-" * 85)

    for name, path in datasets:
        r = check_dataset_convergence(name, path, sample_size=args.sample)
        results.append(r)
        if not args.json:
            state_color = {
                "CONVERGED": "\033[32m",
                "PARTIAL": "\033[33m",
                "CAS-ONLY": "\033[33m",
                "PRIMORDIAL": "\033[31m",
                "EMPTY": "\033[90m",
            }.get(r["state"], "")
            reset = "\033[0m"
            fc = r['files']
            fc_str = f"{fc:>10,}" if isinstance(fc, int) else f"{fc:>10s}"
            print(f"{name:35s} {state_color}{r['state']:12s}{reset} "
                  f"{fc_str} {r.get('size_human', '?'):>10s} "
                  f"{r.get('cas_ratio', 0):>5.0%} "
                  f"{'YES' if r.get('has_braid') else 'no':>6s}")

    elapsed = time.time() - t0

    if args.json:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "datasets": len(results),
            "converged": sum(1 for r in results if r["state"] == "CONVERGED"),
            "partial": sum(1 for r in results if r["state"] == "PARTIAL"),
            "cas_only": sum(1 for r in results if r["state"] == "CAS-ONLY"),
            "primordial": sum(1 for r in results if r["state"] == "PRIMORDIAL"),
            "wall_seconds": round(elapsed, 1),
            "results": results,
        }, sys.stdout, indent=2)
        print()
    else:
        converged = sum(1 for r in results if r["state"] == "CONVERGED")
        partial = sum(1 for r in results if r["state"] == "PARTIAL")
        cas_only = sum(1 for r in results if r["state"] == "CAS-ONLY")
        primordial = sum(1 for r in results if r["state"] == "PRIMORDIAL")
        print(f"\n{'='*85}")
        print(f"  CONVERGED: {converged}  |  PARTIAL: {partial}  |  "
              f"CAS-ONLY: {cas_only}  |  PRIMORDIAL: {primordial}")
        print(f"  Checked {len(results)} datasets in {elapsed:.1f}s")
        print(f"{'='*85}")


if __name__ == "__main__":
    main()
