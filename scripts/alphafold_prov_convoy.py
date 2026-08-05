#!/usr/bin/env python3
"""
AlphaFold provenance convoy — parallel queue partitions with native sockets.

Replaces socat subprocess spawning with direct Python UDS connections.
Single-worker socat: ~38/s. Native socket: should be 10-50x faster per worker.

Usage:
  python3 alphafold_prov_convoy.py --workers 4 --start-after 3183600
  python3 alphafold_prov_convoy.py --workers 4 --resume
  python3 alphafold_prov_convoy.py --partition 0 --of 4  # single worker
"""

import argparse
import base64
import json
import multiprocessing
import os
import signal
import socket
import struct
import subprocess
import sys
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

DEST = Path("/mnt/nestgate/cold/zfs/data/alphafold_structures")
PROV_QUEUE = DEST / ".prov_queue"
DATASET_NAME = "alphafold_structures_v6"

BATCH_SIZE = 200
CHECKPOINT_INTERVAL = 2000
REPORT_INTERVAL = 30

shutdown = False


def handle_signal(signum, frame):
    global shutdown
    shutdown = True


def rpc(primal, method, params=None, timeout=30):
    """JSON-RPC over UDS with native Python socket — no socat subprocess."""
    sock_path = SOCKETS[primal]
    req = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1})
    use_prefix = primal != "beardog"
    data = (RIBOCIPHER_PREFIX if use_prefix else b"") + req.encode() + b"\n"

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(sock_path)
        s.sendall(data)

        buf = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            if b"\n" in buf:
                break
    except (socket.timeout, ConnectionError, OSError):
        s.close()
        return None
    s.close()

    try:
        raw = buf
        if raw[:2] == RIBOCIPHER_PREFIX:
            raw = raw[2:]
        return json.loads(raw.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def rpc_result(primal, method, params=None):
    resp = rpc(primal, method, params)
    if resp and "result" in resp:
        return resp["result"]
    return None


def hex_to_content_hash(hex_str):
    raw = bytes.fromhex(hex_str)
    return {"Blake3": list(raw)}


import blake3 as _blake3

MAX_CAS_SIZE = 100 * 1024 * 1024


def hash_and_cas_put(filepath):
    """Read file once, BLAKE3 hash + CAS put from same buffer. Returns hash hex."""
    try:
        data = filepath.read_bytes()
    except (OSError, IOError):
        return None

    h = _blake3.blake3(data).hexdigest()

    if len(data) <= MAX_CAS_SIZE:
        file_b64 = base64.b64encode(data).decode()
        rpc_result("nestgate", "content.put", {
            "data": file_b64, "hash_type": "blake3",
        })
    else:
        ref = json.dumps({
            "type": "large_file_reference",
            "blake3": h, "size": len(data),
            "path": str(filepath), "gate": "westgate",
        }).encode()
        rpc_result("nestgate", "content.put", {
            "data": base64.b64encode(ref).decode(), "hash_type": "blake3",
        })

    return h


def dag_session_create(dataset_name):
    result = rpc_result("rhizocrypt", "dag.session.create", {
        "session_type": "General",
        "dataset": dataset_name,
        "committer": "did:eco:westgate",
    })
    if isinstance(result, dict):
        return result.get("session_id")
    return result


def dag_event_append_batch(session_id, batch):
    """Append batch of DAG events. batch = [(hash, name, size, dataset), ...]"""
    requests = [
        {
            "session_id": session_id,
            "event_type": {"DataCreate": {}},
            "metadata": [
                ["dataset", ds_name],
                ["filename", name],
                ["blake3", b3hash],
                ["size", str(size)],
            ],
            "payload_ref": b3hash,
            "parents": [],
        }
        for b3hash, name, size, ds_name in batch
    ]
    return rpc_result("rhizocrypt", "dag.event.append_batch", {
        "requests": requests,
    })


def dag_event_append(session_id, b3hash, name, size, dataset_name):
    return rpc_result("rhizocrypt", "dag.event.append", {
        "session_id": session_id,
        "event_type": {"DataCreate": {}},
        "metadata": [
            ["dataset", dataset_name],
            ["filename", name],
            ["blake3", b3hash],
            ["size", str(size)],
        ],
        "payload_ref": b3hash,
        "parents": [],
    })


def dag_partial_dehydrate(session_id):
    return rpc_result("rhizocrypt", "dag.partial_dehydrate", {
        "session_id": session_id,
    })


def spine_create(dataset_name):
    return rpc_result("loamspine", "spine.create", {
        "name": f"federation:{dataset_name}",
    })


def convoy_state_file(partition_id):
    return DEST / f".prov_state_convoy_{partition_id}"


def load_convoy_state(partition_id):
    sf = convoy_state_file(partition_id)
    if sf.exists():
        try:
            return json.loads(sf.read_text())
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def save_convoy_state(partition_id, session_id, spine_id, event_count,
                      lines_processed, byte_offset):
    convoy_state_file(partition_id).write_text(json.dumps({
        "session_id": session_id,
        "spine_id": spine_id,
        "event_count": event_count,
        "lines_processed": lines_processed,
        "byte_offset": byte_offset,
    }))


def get_partition_bounds(queue_path, partition_id, num_partitions, start_after_line=0):
    """Calculate byte offsets for this partition's chunk of the queue file."""
    total_size = queue_path.stat().st_size

    if start_after_line > 0:
        with open(queue_path, "rb") as f:
            for _ in range(start_after_line):
                if not f.readline():
                    break
            remaining_start = f.tell()
    else:
        remaining_start = 0

    remaining_size = total_size - remaining_start
    chunk_size = remaining_size // num_partitions

    part_start = remaining_start + (partition_id * chunk_size)
    if partition_id == num_partitions - 1:
        part_end = total_size
    else:
        part_end = remaining_start + ((partition_id + 1) * chunk_size)

    with open(queue_path, "rb") as f:
        if partition_id > 0:
            f.seek(part_start)
            f.readline()
            part_start = f.tell()
        if partition_id < num_partitions - 1:
            f.seek(part_end)
            f.readline()
            part_end = f.tell()

    return part_start, part_end


def run_convoy_worker(partition_id, num_partitions, start_after_line, resume):
    """Process one partition of the queue with native sockets."""
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    tag = f"[convoy-{partition_id}/{num_partitions}]"
    part_start, part_end = get_partition_bounds(
        PROV_QUEUE, partition_id, num_partitions, start_after_line
    )

    state = load_convoy_state(partition_id) if resume else None
    if state and state.get("session_id") and state.get("byte_offset", 0) >= part_start:
        session_id = state["session_id"]
        spine_id = state["spine_id"]
        event_count = state.get("event_count", 0)
        lines_processed = state.get("lines_processed", 0)
        byte_offset = state.get("byte_offset", part_start)
        print(f"{tag} Resuming: events={event_count:,} offset={byte_offset:,}", flush=True)
    else:
        session_id = dag_session_create(f"{DATASET_NAME}_convoy_{partition_id}")
        spine_result = spine_create(f"{DATASET_NAME}_convoy_{partition_id}")
        spine_id = spine_result.get("spine_id") if isinstance(spine_result, dict) else (
            spine_result if spine_result else "unknown"
        )
        if not session_id:
            print(f"{tag} FATAL: DAG session creation failed", file=sys.stderr, flush=True)
            return {"partition": partition_id, "braided": 0, "errors": -1}
        event_count = 0
        lines_processed = 0
        byte_offset = part_start
        chunk_mb = (part_end - part_start) / 1048576
        print(f"{tag} Started: session={session_id[:12]}... "
              f"range={part_start:,}..{part_end:,} ({chunk_mb:.0f} MB)", flush=True)

    total_braided = 0
    errors = 0
    t_start = time.time()
    last_report = t_start

    while byte_offset < part_end and not shutdown:
        file_entries = []
        with open(PROV_QUEUE, "rb") as f:
            f.seek(byte_offset)
            while f.tell() < part_end:
                raw_line = f.readline()
                if not raw_line:
                    break
                line = raw_line.decode("utf-8", errors="replace").strip()
                lines_processed += 1
                parts = line.split("\t")
                if len(parts) != 2:
                    continue
                filepath, size_str = parts
                file_entries.append((Path(filepath), int(size_str), lines_processed))
                if len(file_entries) >= BATCH_SIZE:
                    byte_offset = f.tell()
                    break
            else:
                byte_offset = f.tell()

        if not file_entries:
            break

        dag_batch = []
        for fp, sz, ln in file_entries:
            h = hash_and_cas_put(fp)
            if not h:
                errors += 1
                continue
            dag_batch.append((h, fp.name, sz, DATASET_NAME))

        if dag_batch:
            result = dag_event_append_batch(session_id, dag_batch)
            if result:
                count = len(result) if isinstance(result, list) else len(dag_batch)
                event_count += count
                total_braided += count
            else:
                for h, fname, sz, ds in dag_batch:
                    vertex = dag_event_append(session_id, h, fname, sz, ds)
                    if vertex:
                        event_count += 1
                        total_braided += 1
                    else:
                        errors += 1

            if event_count > 0 and event_count % CHECKPOINT_INTERVAL < len(dag_batch):
                dag_partial_dehydrate(session_id)
                save_convoy_state(partition_id, session_id, spine_id,
                                  event_count, lines_processed, byte_offset)

        save_convoy_state(partition_id, session_id, spine_id,
                          event_count, lines_processed, byte_offset)

        now = time.time()
        if now - last_report > REPORT_INTERVAL:
            elapsed = now - t_start
            rate = total_braided / elapsed if elapsed > 0 else 0
            pct = (byte_offset - part_start) / max(1, part_end - part_start) * 100
            print(f"{tag} braided={total_braided:,} rate={rate:.1f}/s "
                  f"progress={pct:.1f}% err={errors}", flush=True)
            last_report = now

    elapsed = time.time() - t_start
    rate = total_braided / elapsed if elapsed > 0 else 0
    status = "INTERRUPTED" if shutdown else "DONE"
    print(f"{tag} {status}: braided={total_braided:,} rate={rate:.1f}/s "
          f"errors={errors} elapsed={elapsed:.0f}s", flush=True)

    return {"partition": partition_id, "braided": total_braided,
            "errors": errors, "rate": rate, "elapsed": elapsed}


def main():
    parser = argparse.ArgumentParser(description="AlphaFold provenance convoy — native sockets")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--partition", type=int, default=None)
    parser.add_argument("--of", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--start-after", type=int, default=0,
                        help="Skip lines already processed by original trailer")
    args = parser.parse_args()

    if not PROV_QUEUE.exists():
        print("No .prov_queue file found", file=sys.stderr)
        sys.exit(1)

    total_lines = sum(1 for _ in open(PROV_QUEUE, "rb"))
    remaining = total_lines - args.start_after
    print(f"Queue: {total_lines:,} total, skip {args.start_after:,}, "
          f"process {remaining:,}", flush=True)

    if args.partition is not None:
        num_parts = args.of or args.workers
        result = run_convoy_worker(args.partition, num_parts,
                                   args.start_after, args.resume)
        print(json.dumps(result))
        return

    num_workers = args.workers
    print(f"Launching {num_workers} convoy workers (native sockets)...", flush=True)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    with multiprocessing.Pool(num_workers) as pool:
        jobs = []
        for i in range(num_workers):
            job = pool.apply_async(
                run_convoy_worker,
                (i, num_workers, args.start_after, args.resume)
            )
            jobs.append(job)

        results = []
        for job in jobs:
            try:
                results.append(job.get())
            except Exception as e:
                results.append({"error": str(e)})

    total_braided = sum(r.get("braided", 0) for r in results)
    total_errors = sum(r.get("errors", 0) for r in results)
    max_elapsed = max((r.get("elapsed", 0) for r in results), default=0)
    combined_rate = total_braided / max_elapsed if max_elapsed > 0 else 0

    print(f"\n=== CONVOY COMPLETE ===", flush=True)
    print(f"Workers:       {num_workers}", flush=True)
    print(f"Total braided: {total_braided:,}", flush=True)
    print(f"Total errors:  {total_errors:,}", flush=True)
    print(f"Combined rate: {combined_rate:.1f}/s", flush=True)
    print(f"Wall time:     {max_elapsed:.0f}s ({max_elapsed/3600:.1f}h)", flush=True)

    for r in results:
        p = r.get("partition", "?")
        print(f"  convoy-{p}: {r.get('braided',0):,} braided, "
              f"{r.get('rate',0):.1f}/s, {r.get('errors',0)} errors", flush=True)


if __name__ == "__main__":
    main()
