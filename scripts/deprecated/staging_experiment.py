#!/usr/bin/env python3
"""
Staging Experiment — measures rsync vs tar-pipe vs direct-ingest
across different data type profiles.

Usage:
    python3 staging_experiment.py --test 1 --method rsync
    python3 staging_experiment.py --test 1 --method tar
    python3 staging_experiment.py --test 1 --method direct
    python3 staging_experiment.py --test all              # run all 15 combos
    python3 staging_experiment.py --summary               # print results table
"""

import argparse
import json
import os
import resource
import shutil
import socket
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path

MEMBRANE = "/run/user/1000/membrane"
RIBOCIPHER_PREFIX = struct.pack("BB", 0xEC, 0x01)
SOCKETS = {
    "nestgate":   f"{MEMBRANE}/nestgate-westgate-tower-155f.sock",
    "rhizocrypt": f"{MEMBRANE}/rhizocrypt-westgate-tower-155f.sock",
    "loamspine":  f"{MEMBRANE}/loamspine-westgate-tower-155f.sock",
    "sweetgrass": f"{MEMBRANE}/sweetgrass-westgate-tower-155f.sock",
    "beardog":    f"{MEMBRANE}/beardog-westgate-tower-155f.sock",
}

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")
STAGE_ROOT = Path("/mnt/cas-hot/_stage/_experiment")
CAS_FAMILY = "standalone"
RESULTS_FILE = Path(__file__).parent / "staging_experiment_results.json"

TESTS = {
    1: {
        "name": "Type A: Many Small Files",
        "dataset": "alphafold_structures",
        "subdir": "A3",
        "description": "6477 CIF files, 100-300 KB each",
    },
    2: {
        "name": "Type A-large: Oversized Dir Subset",
        "dataset": "alphafold_structures",
        "subdir": "A0",
        "a0_prefix_limit": 2,
        "description": "A0 subset — first 2 filename prefixes (~500K files)",
    },
    3: {
        "name": "Type B: Single Large File",
        "dataset": "rnacentral",
        "subdir": None,
        "description": "1x 9 GB .gz file — bandwidth-bound",
    },
    4: {
        "name": "Type C: Medium Archives",
        "dataset": "sra_fastq",
        "subdir": "PRJNA1224988_cyano_bloom",
        "description": "351 .fastq.gz files, 2.9 GB total",
    },
    5: {
        "name": "Type D: Moderate Structured",
        "dataset": "open_targets",
        "subdir": None,
        "description": "18 parquet files, 30-85 MB each, 1.2 GB total",
    },
}

METHODS = ["rsync", "tar", "direct"]


# ---------------------------------------------------------------------------
# RPC (reused from native_braid.py)
# ---------------------------------------------------------------------------

def _rpc(primal, method, params=None, timeout=600, recv_size=4 * 1024 * 1024):
    sock_path = SOCKETS[primal]
    req = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1})
    use_prefix = primal != "beardog"
    data = (RIBOCIPHER_PREFIX if use_prefix else b"") + req.encode() + b"\n"

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(sock_path)
        s.sendall(data)
        buf = bytearray()
        while True:
            chunk = s.recv(recv_size)
            if not chunk:
                break
            buf.extend(chunk)
            if b"\n" in buf:
                break
    except (socket.timeout, ConnectionError, OSError) as e:
        s.close()
        return {"error": str(e)}
    s.close()

    raw = bytes(buf)
    if raw[:2] == RIBOCIPHER_PREFIX:
        raw = raw[2:]
    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"error": "JSON parse failed", "raw_len": len(raw)}


def rpc_result(primal, method, params=None, timeout=600):
    resp = _rpc(primal, method, params, timeout)
    if isinstance(resp, dict) and "result" in resp:
        return resp["result"]
    if isinstance(resp, dict) and "error" in resp:
        err = resp["error"]
        msg = err.get("message", err) if isinstance(err, dict) else err
        raise RuntimeError(f"RPC {primal}.{method} failed: {msg}")
    raise RuntimeError(f"RPC {primal}.{method}: unexpected response")


# ---------------------------------------------------------------------------
# Instrumentation: ARC stats, zpool iostat sampler, memory
# ---------------------------------------------------------------------------

def read_arc_stats():
    stats = {}
    try:
        with open("/proc/spl/kstat/zfs/arcstats") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3 and parts[0] not in ("name", "---"):
                    try:
                        stats[parts[0]] = int(parts[2])
                    except ValueError:
                        pass
    except OSError:
        pass
    return stats


def arc_snapshot():
    s = read_arc_stats()
    return {
        "arc_hits": s.get("hits", 0),
        "arc_misses": s.get("misses", 0),
        "l2_hits": s.get("l2_hits", 0),
        "l2_misses": s.get("l2_misses", 0),
        "arc_size_gb": s.get("size", 0) / 1073741824,
    }


def arc_delta(before, after):
    d_hits = after["arc_hits"] - before["arc_hits"]
    d_misses = after["arc_misses"] - before["arc_misses"]
    d_l2_hits = after["l2_hits"] - before["l2_hits"]
    d_l2_misses = after["l2_misses"] - before["l2_misses"]
    d_total = d_hits + d_misses
    d_l2_total = d_l2_hits + d_l2_misses
    return {
        "arc_hit_rate": d_hits / d_total * 100 if d_total > 0 else 0,
        "arc_ops": d_total,
        "l2_hit_rate": d_l2_hits / d_l2_total * 100 if d_l2_total > 0 else 0,
        "l2_ops": d_l2_total,
    }


class ZpoolSampler(threading.Thread):
    """Background thread sampling zpool iostat at 1s intervals."""

    def __init__(self, pool="nestgate"):
        super().__init__(daemon=True)
        self.pool = pool
        self.samples = []
        self._halt = threading.Event()

    def run(self):
        while not self._halt.is_set():
            try:
                r = subprocess.run(
                    ["zpool", "iostat", self.pool, "-p", "1", "1"],
                    capture_output=True, text=True, timeout=5,
                )
                for line in r.stdout.strip().split("\n"):
                    parts = line.split()
                    if len(parts) >= 7 and parts[0] == self.pool:
                        self.samples.append({
                            "t": time.time(),
                            "read_ops": int(parts[3]),
                            "write_ops": int(parts[4]),
                            "read_bw": int(parts[5]),
                            "write_bw": int(parts[6]),
                        })
            except Exception:
                pass

    def stop(self):
        self._halt.set()
        self.join(timeout=3)

    def summary(self):
        if not self.samples:
            return {"avg_read_mbps": 0, "avg_read_iops": 0, "avg_write_mbps": 0, "samples": 0}
        n = len(self.samples)
        return {
            "avg_read_mbps": sum(s["read_bw"] for s in self.samples) / n / 1048576,
            "avg_read_iops": sum(s["read_ops"] for s in self.samples) / n,
            "avg_write_mbps": sum(s["write_bw"] for s in self.samples) / n / 1048576,
            "avg_write_iops": sum(s["write_ops"] for s in self.samples) / n,
            "peak_read_mbps": max(s["read_bw"] for s in self.samples) / 1048576,
            "samples": n,
        }


def peak_rss_mb():
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    return ru.ru_maxrss / 1024


# ---------------------------------------------------------------------------
# Staging methods
# ---------------------------------------------------------------------------

def stage_rsync(src, dst, tag=""):
    """rsync -a src/ dst/ — current production method."""
    dst.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    result = subprocess.run(
        ["rsync", "-a", "--exclude=.*", f"{src}/", f"{dst}/"],
        capture_output=True, text=True, timeout=7200,
    )
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"  {tag} rsync FAILED: {result.stderr[:200]}", flush=True)
        return None, elapsed
    return dst, elapsed


def stage_tar(src, dst, tag=""):
    """tar cf - | tar xf - — sequential directory traversal."""
    dst.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    tar_create = subprocess.Popen(
        ["tar", "cf", "-", "--exclude=./.*", "-C", str(src), "."],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    tar_extract = subprocess.Popen(
        ["tar", "xf", "-", "-C", str(dst)],
        stdin=tar_create.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    tar_create.stdout.close()
    _, err_extract = tar_extract.communicate(timeout=7200)
    tar_create.wait()
    elapsed = time.time() - t0
    if tar_extract.returncode != 0:
        print(f"  {tag} tar FAILED: {err_extract[:200]}", flush=True)
        return None, elapsed
    return dst, elapsed


def stage_rsync_a0_subset(src, dst, prefix_limit=2, tag=""):
    """rsync with --include filters for A0 prefix-subset test."""
    prefixes = set()
    try:
        for entry in os.scandir(str(src)):
            if entry.is_file() and not entry.name.startswith("."):
                prefixes.add(entry.name[:6])
                if len(prefixes) >= prefix_limit * 50:
                    break
    except OSError:
        pass
    selected = sorted(prefixes)[:prefix_limit]
    if not selected:
        return None, 0

    dst.mkdir(parents=True, exist_ok=True)
    include_args = []
    for pfx in selected:
        include_args.extend(["--include", f"{pfx}*"])
    include_args.extend(["--exclude", "*"])

    t0 = time.time()
    result = subprocess.run(
        ["rsync", "-a"] + include_args + [f"{src}/", f"{dst}/"],
        capture_output=True, text=True, timeout=7200,
    )
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"  {tag} rsync A0 subset FAILED: {result.stderr[:200]}", flush=True)
        return None, elapsed
    return dst, elapsed


def stage_tar_a0_subset(src, dst, prefix_limit=2, tag=""):
    """tar with find-based file list for A0 prefix-subset test."""
    prefixes = set()
    try:
        for entry in os.scandir(str(src)):
            if entry.is_file() and not entry.name.startswith("."):
                prefixes.add(entry.name[:6])
                if len(prefixes) >= prefix_limit * 50:
                    break
    except OSError:
        pass
    selected = sorted(prefixes)[:prefix_limit]
    if not selected:
        return None, 0

    dst.mkdir(parents=True, exist_ok=True)

    find_patterns = " -o ".join(f'-name "{pfx}*"' for pfx in selected)
    find_cmd = f'find {src} -maxdepth 1 -type f \\( {find_patterns} \\) -print0'

    t0 = time.time()
    find_proc = subprocess.Popen(
        ["bash", "-c", find_cmd],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    tar_create = subprocess.Popen(
        ["tar", "cf", "-", "--null", "-T", "-"],
        stdin=find_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    find_proc.stdout.close()
    tar_extract = subprocess.Popen(
        ["tar", "xf", "-", "-C", str(dst), "--strip-components",
         str(len(src.parts))],
        stdin=tar_create.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    tar_create.stdout.close()
    tar_extract.communicate(timeout=7200)
    tar_create.wait()
    find_proc.wait()
    elapsed = time.time() - t0
    return dst, elapsed


# ---------------------------------------------------------------------------
# Ingest via nestGate content.ingest
# ---------------------------------------------------------------------------

def ingest_directory(directory, tag=""):
    t0 = time.time()
    result = rpc_result("nestgate", "content.ingest", {
        "directory": str(directory),
        "family_id": CAS_FAMILY,
        "source": "staging_experiment",
        "pipeline": "experiment",
    }, timeout=3600)
    elapsed = time.time() - t0
    count = result.get("count", 0)
    dedup = result.get("deduplicated", 0)
    mb = result.get("bytes_total", 0) / 1048576
    rate = count / elapsed if elapsed > 0 else 0
    print(f"  {tag} CAS: {count} files ({dedup} dedup), "
          f"{mb:.0f} MB, {elapsed:.1f}s ({rate:.0f}/s)", flush=True)
    return result, elapsed


# ---------------------------------------------------------------------------
# Run a single experiment
# ---------------------------------------------------------------------------

def resolve_source(test_num):
    """Return the cold-tier source path for a given test."""
    cfg = TESTS[test_num]
    base = DATA_ROOT / cfg["dataset"]
    if cfg.get("subdir"):
        return base / cfg["subdir"]
    return base


def run_experiment(test_num, method):
    cfg = TESTS[test_num]
    src = resolve_source(test_num)
    is_a0 = cfg.get("a0_prefix_limit") is not None
    tag = f"[T{test_num}:{method}]"

    print(f"\n{'='*60}", flush=True)
    print(f"{tag} {cfg['name']}", flush=True)
    print(f"{tag} Source: {src}", flush=True)
    print(f"{tag} Method: {method}", flush=True)
    print(f"{tag} {cfg['description']}", flush=True)
    print(f"{'='*60}", flush=True)

    dst = STAGE_ROOT / f"t{test_num}_{method}"
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)

    arc_before = arc_snapshot()
    sampler = ZpoolSampler()
    sampler.start()
    rss_before = peak_rss_mb()

    t_total_start = time.time()
    stage_elapsed = 0
    ingest_elapsed = 0
    staged_path = None
    ingest_result = {}

    if method == "direct":
        print(f"  {tag} Direct ingest from cold path...", flush=True)
        ingest_result, ingest_elapsed = ingest_directory(src, tag=tag)
    else:
        # Stage phase
        if is_a0:
            pfx_limit = cfg["a0_prefix_limit"]
            if method == "rsync":
                staged_path, stage_elapsed = stage_rsync_a0_subset(
                    src, dst, prefix_limit=pfx_limit, tag=tag)
            else:
                staged_path, stage_elapsed = stage_tar_a0_subset(
                    src, dst, prefix_limit=pfx_limit, tag=tag)
        else:
            if method == "rsync":
                staged_path, stage_elapsed = stage_rsync(src, dst, tag=tag)
            else:
                staged_path, stage_elapsed = stage_tar(src, dst, tag=tag)

        print(f"  {tag} Staged in {stage_elapsed:.1f}s", flush=True)

        # Count staged files/size
        if staged_path and staged_path.exists():
            staged_files = sum(1 for _ in staged_path.rglob("*") if _.is_file())
            staged_bytes = sum(f.stat().st_size for f in staged_path.rglob("*") if f.is_file())
            print(f"  {tag} Staged: {staged_files} files, "
                  f"{staged_bytes / 1048576:.0f} MB", flush=True)
        else:
            staged_files = 0
            staged_bytes = 0

        # Ingest phase
        if staged_path:
            ingest_result, ingest_elapsed = ingest_directory(staged_path, tag=tag)
        else:
            print(f"  {tag} Staging failed — skipping ingest", flush=True)

    t_total = time.time() - t_total_start

    sampler.stop()
    arc_after = arc_snapshot()
    rss_after = peak_rss_mb()

    # Cleanup staged data
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)

    pool_stats = sampler.summary()
    cache_delta = arc_delta(arc_before, arc_after)

    result = {
        "test": test_num,
        "test_name": cfg["name"],
        "method": method,
        "description": cfg["description"],
        "source": str(src),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "wall_clock_s": round(t_total, 2),
        "stage_s": round(stage_elapsed, 2),
        "ingest_s": round(ingest_elapsed, 2),
        "files_ingested": ingest_result.get("count", 0),
        "files_dedup": ingest_result.get("deduplicated", 0),
        "bytes_total": ingest_result.get("bytes_total", 0),
        "throughput_mbps": round(
            ingest_result.get("bytes_total", 0) / 1048576 / t_total, 1
        ) if t_total > 0 else 0,
        "files_per_sec": round(
            ingest_result.get("count", 0) / t_total, 1
        ) if t_total > 0 else 0,
        "pool": pool_stats,
        "cache": cache_delta,
        "peak_rss_mb": round(max(rss_before, rss_after), 1),
    }

    print(f"\n{tag} RESULT:", flush=True)
    print(f"  Wall clock:  {t_total:.1f}s "
          f"(stage {stage_elapsed:.1f}s + ingest {ingest_elapsed:.1f}s)", flush=True)
    print(f"  Files:       {result['files_ingested']} "
          f"({result['files_dedup']} dedup)", flush=True)
    print(f"  Throughput:  {result['throughput_mbps']} MB/s, "
          f"{result['files_per_sec']} files/s", flush=True)
    print(f"  Pool avg:    {pool_stats['avg_read_mbps']:.1f} MB/s read, "
          f"{pool_stats['avg_read_iops']:.0f} IOPS", flush=True)
    print(f"  ARC hit:     {cache_delta['arc_hit_rate']:.1f}% "
          f"({cache_delta['arc_ops']} ops)", flush=True)
    print(f"  L2ARC hit:   {cache_delta['l2_hit_rate']:.1f}% "
          f"({cache_delta['l2_ops']} ops)", flush=True)

    return result


# ---------------------------------------------------------------------------
# Results persistence and summary
# ---------------------------------------------------------------------------

def load_results():
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return []


def save_result(result):
    results = load_results()
    results.append(result)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


def print_summary():
    results = load_results()
    if not results:
        print("No results yet.")
        return

    by_test = {}
    for r in results:
        key = r["test"]
        by_test.setdefault(key, []).append(r)

    print(f"\n{'='*90}")
    print(f"{'TEST':<35} {'METHOD':<8} {'WALL(s)':<9} {'STAGE(s)':<9} "
          f"{'INGEST(s)':<10} {'MB/s':<8} {'f/s':<8} {'HDD MB/s':<9}")
    print(f"{'-'*90}")

    for test_num in sorted(by_test.keys()):
        runs = sorted(by_test[test_num], key=lambda x: x["wall_clock_s"])
        for r in runs:
            name = r["test_name"][:33]
            print(f"{name:<35} {r['method']:<8} {r['wall_clock_s']:<9.1f} "
                  f"{r['stage_s']:<9.1f} {r['ingest_s']:<10.1f} "
                  f"{r['throughput_mbps']:<8.1f} {r['files_per_sec']:<8.1f} "
                  f"{r['pool']['avg_read_mbps']:<9.1f}")
        print()

    print(f"{'='*90}")

    print("\n=== Winner by Test ===")
    for test_num in sorted(by_test.keys()):
        runs = sorted(by_test[test_num], key=lambda x: x["wall_clock_s"])
        best = runs[0]
        worst = runs[-1]
        speedup = worst["wall_clock_s"] / best["wall_clock_s"] if best["wall_clock_s"] > 0 else 0
        print(f"  T{test_num} {best['test_name'][:40]:<42} "
              f"Winner: {best['method']:<6} ({best['wall_clock_s']:.1f}s) "
              f"— {speedup:.1f}x faster than {worst['method']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Staging experiment matrix")
    parser.add_argument("--test", type=str, help="Test number 1-5 or 'all'")
    parser.add_argument("--method", choices=METHODS, help="Staging method")
    parser.add_argument("--subdir", type=str, help="Override subdir for the test")
    parser.add_argument("--summary", action="store_true", help="Print results summary")
    args = parser.parse_args()

    if args.summary:
        print_summary()
        return

    if not args.test:
        parser.print_help()
        return

    if args.test == "all":
        test_nums = list(TESTS.keys())
        methods = METHODS
    else:
        test_nums = [int(args.test)]
        methods = [args.method] if args.method else METHODS

    if args.subdir:
        for tn in test_nums:
            TESTS[tn]["subdir"] = args.subdir

    STAGE_ROOT.mkdir(parents=True, exist_ok=True)

    for tn in test_nums:
        if tn not in TESTS:
            print(f"Unknown test {tn}, valid: {list(TESTS.keys())}")
            continue
        for m in methods:
            try:
                result = run_experiment(tn, m)
                save_result(result)
            except Exception as e:
                print(f"ERROR in T{tn}:{m}: {e}", flush=True)
                import traceback
                traceback.print_exc()

    print_summary()


if __name__ == "__main__":
    main()
