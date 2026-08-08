#!/usr/bin/env python3
"""
convergence_drain.py — Phase 1 Convergence Tiering: warm→cold CAS drain

Drains CAS objects from the NVMe warm tier to cold ZFS storage.
Objects already on cold are evicted directly; warm-only objects are
replicated first. The drain is recorded in the provenance chain via
rhizoCrypt (DAG event) + loamSpine (DataAnchor) + sweetGrass (braid seal).

Usage:
    python3 convergence_drain.py                 # drain with default thresholds
    python3 convergence_drain.py --dry-run       # report what would be drained
    python3 convergence_drain.py --high-water 80 # trigger only if warm > 80%
    python3 convergence_drain.py --low-water 20  # drain until warm < 20%

The script is idempotent and crash-safe: if interrupted, re-running picks
up where it left off (objects already evicted won't be re-processed).
"""

import argparse
import hashlib
import json
import os
import shutil
import socket
import struct
import sys
import time

WARM_CAS = "/mnt/cas-hot/datasets/standalone/_content"
COLD_CAS = "/mnt/nestgate/cold/zfs/cas/datasets/standalone/_content"
RECEIPT_PATH = "/mnt/cas-hot/_drain_receipt.json"

RIBOCIPHER_PREFIX = struct.pack("BB", 0xEC, 0x01)
MEMBRANE = f"/run/user/{os.getuid()}/membrane"
RHIZO = f"{MEMBRANE}/rhizocrypt-westgate-tower-155f.sock"
LOAM = f"{MEMBRANE}/loamspine-westgate-tower-155f.sock"
SWEETGRASS = f"{MEMBRANE}/sweetgrass-westgate-tower-155f.sock"

SPINE_NAME = "tier-drain-westgate"


def rpc_ribo(sock_path, method, params=None):
    req = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1})
    data = RIBOCIPHER_PREFIX + req.encode() + b"\n"
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(sock_path)
    s.sendall(data)
    resp = b""
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        resp += chunk
        if b"\n" in resp:
            break
    s.close()
    if resp[:2] == RIBOCIPHER_PREFIX:
        resp = resp[2:]
    return json.loads(resp.strip())


def rpc_plain(sock_path, method, params=None):
    req = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1})
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(sock_path)
    s.sendall(req.encode() + b"\n")
    resp = b""
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        resp += chunk
        if b"\n" in resp:
            break
    s.close()
    return json.loads(resp.strip())


def get_warm_usage_pct():
    stat = os.statvfs("/mnt/cas-hot")
    total = stat.f_blocks * stat.f_frsize
    used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
    return (used / total) * 100 if total else 0


def drain_prefix(prefix, dry_run=False):
    warm_dir = os.path.join(WARM_CAS, prefix)
    cold_dir = os.path.join(COLD_CAS, prefix)

    if not os.path.isdir(warm_dir):
        return 0, 0, 0, 0

    warm_objs = os.listdir(warm_dir)
    if not warm_objs:
        return 0, 0, 0, 0

    evicted = replicated = errors = bytes_freed = 0

    if not dry_run:
        os.makedirs(cold_dir, exist_ok=True)

    for obj in warm_objs:
        warm_path = os.path.join(warm_dir, obj)
        cold_path = os.path.join(cold_dir, obj)

        try:
            obj_size = os.path.getsize(warm_path)

            if dry_run:
                if os.path.exists(cold_path):
                    evicted += 1
                else:
                    replicated += 1
                bytes_freed += obj_size
                continue

            if os.path.exists(cold_path):
                os.unlink(warm_path)
                evicted += 1
                bytes_freed += obj_size
            else:
                shutil.copy2(warm_path, cold_path)
                os.unlink(warm_path)
                replicated += 1
                bytes_freed += obj_size
        except Exception:
            errors += 1

    return evicted, replicated, errors, bytes_freed


def record_provenance(receipt):
    drain_summary = json.dumps({
        "operation": "warm-to-cold-drain",
        "evicted": receipt["evicted"],
        "replicated": receipt["replicated"],
        "bytes_freed": receipt["bytes_freed"],
        "buckets": receipt["buckets"],
        "gate": "westgate",
        "timestamp": receipt["timestamp"],
    })
    drain_hash = hashlib.blake2b(drain_summary.encode(), digest_size=32).hexdigest()

    try:
        session = rpc_ribo(RHIZO, "dag.session.create", {
            "namespace": "tier-drain",
            "metadata": {"type": "warm-to-cold", "gate": "westgate"},
        })
        sid = session.get("result", "")
        rpc_ribo(RHIZO, "dag.event.append", {
            "session_id": sid,
            "event_type": {"DataCreate": {"data": drain_summary}},
        })
        print(f"  DAG: event recorded (session {str(sid)[:20]}...)")
    except Exception as e:
        print(f"  DAG: {e}")

    try:
        spines = rpc_plain(LOAM, "spine.list", {})
        spine_ids = spines.get("result", {}).get("spine_ids", [])
        spine_id = None
        for sid in spine_ids:
            status = rpc_plain(LOAM, "spine.status", {"spine_id": sid})
            if status.get("result", {}).get("name") == SPINE_NAME:
                spine_id = sid
                break
        if not spine_id:
            resp = rpc_plain(LOAM, "spine.create", {
                "name": SPINE_NAME,
                "owner": "westgate-overwatch",
                "metadata": {"type": "convergence-tiering"},
            })
            spine_id = resp.get("result", {}).get("spine_id", "")

        rpc_plain(LOAM, "entry.append", {
            "spine_id": spine_id,
            "entry_type": {"DataAnchor": {
                "data_hash": drain_hash,
                "size": len(drain_summary),
                "metadata": json.dumps({
                    "type": "drain.complete",
                    "evicted": receipt["evicted"],
                    "replicated": receipt["replicated"],
                    "freed_gb": round(receipt["bytes_freed"] / (1024**3), 1),
                }),
            }},
        })
        print(f"  Spine: DataAnchor committed ({spine_id[:20]}...)")
    except Exception as e:
        print(f"  Spine: {e}")

    try:
        resp = rpc_ribo(SWEETGRASS, "braid.create", {
            "data_hash": drain_hash,
            "mime_type": "application/json",
            "size": len(drain_summary),
            "strand_id": f"tier-drain-westgate-{int(time.time())}",
            "metadata": {
                "type": "tier.drain.complete",
                "evicted": receipt["evicted"],
                "replicated": receipt["replicated"],
                "freed_gb": round(receipt["bytes_freed"] / (1024**3), 1),
            },
        })
        braid_id = resp.get("result", {}).get("@id", "?")
        print(f"  Braid: {braid_id[:40]}...")
    except Exception as e:
        print(f"  Braid: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convergence drain: warm→cold CAS")
    parser.add_argument("--dry-run", action="store_true", help="Report only, don't evict")
    parser.add_argument("--high-water", type=float, default=50,
                        help="Only drain if warm tier exceeds this %% (default: 50)")
    parser.add_argument("--low-water", type=float, default=15,
                        help="Drain until warm tier drops below this %% (default: 15)")
    args = parser.parse_args()

    usage = get_warm_usage_pct()
    print(f"=== Convergence Drain — {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"Warm tier: {usage:.1f}%  (high-water: {args.high_water}%, low-water: {args.low_water}%)")

    if usage < args.high_water and not args.dry_run:
        print(f"Below high-water mark — no drain needed.")
        return

    if not os.path.isdir(WARM_CAS):
        print(f"Warm CAS not found: {WARM_CAS}")
        return

    prefixes = sorted(p for p in os.listdir(WARM_CAS) if os.path.isdir(os.path.join(WARM_CAS, p)))
    total_evicted = total_replicated = total_errors = total_bytes_freed = 0
    bucket_summaries = []
    start = time.time()
    mode = "DRY RUN" if args.dry_run else "DRAIN"

    print(f"Mode: {mode}  |  Prefixes: {len(prefixes)}\n")

    for i, prefix in enumerate(prefixes):
        evicted, replicated, errors, freed = drain_prefix(prefix, dry_run=args.dry_run)
        total_evicted += evicted
        total_replicated += replicated
        total_errors += errors
        total_bytes_freed += freed

        bucket_summaries.append({
            "prefix": prefix,
            "evicted": evicted,
            "replicated": replicated,
            "errors": errors,
            "bytes_freed": freed,
        })

        if (i + 1) % 16 == 0 or i == len(prefixes) - 1:
            elapsed = time.time() - start
            pct = (i + 1) / len(prefixes) * 100
            freed_gb = total_bytes_freed / (1024**3)
            print(f"  [{i+1:3d}/{len(prefixes)}] {pct:5.1f}% | "
                  f"evicted: {total_evicted:,} | replicated: {total_replicated:,} | "
                  f"freed: {freed_gb:.1f} GB | {elapsed:.0f}s")

        if not args.dry_run and (i + 1) % 32 == 0:
            current = get_warm_usage_pct()
            if current < args.low_water:
                print(f"\n  Warm tier at {current:.1f}% — below low-water, stopping early.")
                break

    elapsed = time.time() - start
    freed_gb = total_bytes_freed / (1024**3)

    print(f"\n=== {mode} COMPLETE — {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"  Evicted (on cold):      {total_evicted:,}")
    print(f"  Replicated (warm→cold): {total_replicated:,}")
    print(f"  Errors:                 {total_errors:,}")
    print(f"  Space freed:            {freed_gb:.1f} GB")
    print(f"  Time:                   {elapsed:.0f}s ({elapsed/60:.1f} min)")
    if elapsed > 0:
        print(f"  Rate:                   {(total_evicted + total_replicated) / elapsed:.0f} objects/s")

    if args.dry_run:
        return

    receipt = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "evicted": total_evicted,
        "replicated": total_replicated,
        "errors": total_errors,
        "bytes_freed": total_bytes_freed,
        "elapsed_s": round(elapsed, 1),
        "buckets": len(bucket_summaries),
        "bucket_details": bucket_summaries,
    }
    with open(RECEIPT_PATH, "w") as f:
        json.dump(receipt, f, indent=2)
    print(f"\n  Receipt: {RECEIPT_PATH}")

    if total_evicted + total_replicated > 0:
        print("\n=== Recording in provenance chain ===")
        record_provenance(receipt)

    print(f"\n  Final warm tier: {get_warm_usage_pct():.1f}%")


if __name__ == "__main__":
    main()
