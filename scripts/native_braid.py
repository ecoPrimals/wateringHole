#!/usr/bin/env python3
"""
Native bulk braider — Python is ONLY the RPC orchestrator.

All file I/O, hashing, and CAS storage happen in Rust via primal RPCs:
  - content.ingest  → Rust walks directory, BLAKE3 hashes, CAS stores with dedup
  - dag.event.append_batch → Rust DAG event recording
  - dag.dehydration.trigger → Rust merkle tree computation
  - session.commit → Rust spine commit
  - braid.create → Rust provenance braid

Python never reads file data, never hashes, never base64-encodes.

Per-chunk flow:
  1. content.ingest(directory) → manifest {file: hash}      [nestGate Rust]
  2. dag.session.create → dag.event.append_batch(manifest)   [rhizoCrypt Rust]
  3. dag.dehydration.trigger → session.commit                [loamSpine Rust]
  4. braid.create                                            [sweetGrass Rust]

Usage:
    python3 native_braid.py                                # all unbraided datasets
    python3 native_braid.py --only alphafold_structures    # specific dataset
    python3 native_braid.py --dry-run                      # list what would run
"""

import argparse
import json
import os
import signal
import socket
import struct
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

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")
CAS_FAMILY = "standalone"
COMMITTER_DID = "did:eco:westgate"
DAG_BATCH_SIZE = 500
SKIP_EXTENSIONS = {".part", ".tmp", ".lock", ".swp"}

shutdown = False


def handle_signal(signum, frame):
    global shutdown
    shutdown = True
    print("\n[native_braid] Shutdown signal received...", flush=True)


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


def _rpc(primal, method, params=None, timeout=600, recv_size=4 * 1024 * 1024):
    """JSON-RPC 2.0 over UDS. Large recv buffer for manifest responses."""
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
        if isinstance(err, dict):
            raise RuntimeError(f"RPC {primal}.{method} failed: {err.get('message', err)}")
        raise RuntimeError(f"RPC {primal}.{method} failed: {err}")
    raise RuntimeError(f"RPC {primal}.{method}: unexpected response")


def nvme_free_gb():
    st = os.statvfs("/mnt/cas-hot")
    return (st.f_bavail * st.f_frsize) / (1024 ** 3)


# ---------------------------------------------------------------------------
# Core: content.ingest → DAG → spine pipeline
# ---------------------------------------------------------------------------

def ingest_directory(directory, tag=""):
    """Call nestGate content.ingest — Rust walks, hashes, CAS stores.

    Returns manifest dict {relative_path: blake3_hex} and stats.
    """
    t0 = time.time()
    result = rpc_result("nestgate", "content.ingest", {
        "directory": str(directory),
        "family_id": CAS_FAMILY,
        "source": "native_braid",
        "pipeline": "retrospective_braid",
    }, timeout=3600)

    elapsed = time.time() - t0
    count = result.get("count", 0)
    dedup = result.get("deduplicated", 0)
    mb = result.get("bytes_total", 0) / 1048576

    if tag:
        rate = count / elapsed if elapsed > 0 else 0
        print(f"{tag} CAS: {count} files ({dedup} dedup), "
              f"{mb:.0f} MB, {elapsed:.0f}s ({rate:.0f}/s)", flush=True)

    return result


def build_dag_events(manifest, dataset_name, session_id):
    """Convert content.ingest manifest to DAG event batch requests."""
    requests = []
    for rel_path, blake3_hex in manifest.items():
        requests.append({
            "session_id": session_id,
            "event_type": {"DataCreate": {}},
            "metadata": [
                ["dataset", dataset_name],
                ["filename", rel_path],
                ["blake3", blake3_hex],
            ],
            "payload_ref": blake3_hex,
            "parents": [],
        })
    return requests


def append_dag_batch(requests, tag=""):
    """Send DAG events in batches to rhizoCrypt."""
    total = len(requests)
    appended = 0
    errors = 0

    for i in range(0, total, DAG_BATCH_SIZE):
        if shutdown:
            break
        batch = requests[i:i + DAG_BATCH_SIZE]
        result = _rpc("rhizocrypt", "dag.event.append_batch", {"requests": batch})
        if isinstance(result, dict) and "result" in result:
            r = result["result"]
            appended += len(r) if isinstance(r, list) else len(batch)
        else:
            for req in batch:
                r = _rpc("rhizocrypt", "dag.event.append", req)
                if isinstance(r, dict) and "result" in r:
                    appended += 1
                else:
                    errors += 1

        if tag and (i + len(batch)) % 5000 < DAG_BATCH_SIZE:
            print(f"{tag} DAG: {appended}/{total} events", flush=True)

    return appended, errors


def braid_chunk(directory, dataset_name, chunk_name, session_id, spine_id, tag=""):
    """Full per-chunk pipeline: CAS ingest → DAG → dehydrate → commit."""
    cas_result = ingest_directory(directory, tag=tag)
    manifest = cas_result.get("manifest", {})

    if not manifest:
        print(f"{tag} Empty manifest — skipping", flush=True)
        return None

    if shutdown:
        return None

    dag_events = build_dag_events(manifest, dataset_name, session_id)
    appended, dag_errors = append_dag_batch(dag_events, tag=tag)

    if shutdown:
        return None

    merkle_root = rpc_result("rhizocrypt", "dag.dehydration.trigger", {
        "session_id": session_id,
    })
    if isinstance(merkle_root, dict):
        merkle_root = merkle_root.get("merkle_root", merkle_root)

    if spine_id and spine_id != "pending" and merkle_root:
        rpc_result("loamspine", "session.commit", {
            "spine_id": spine_id,
            "session_id": session_id,
            "session_hash": str(merkle_root),
            "merkle_root": str(merkle_root),
            "vertex_count": appended,
            "committer": COMMITTER_DID,
        })

    print(f"{tag} Committed: {appended} events, "
          f"root={str(merkle_root)[:16]}..., {dag_errors} errors", flush=True)

    return {
        "chunk": chunk_name,
        "files": cas_result.get("count", 0),
        "dedup": cas_result.get("deduplicated", 0),
        "bytes": cas_result.get("bytes_total", 0),
        "merkle_root": merkle_root,
        "dag_appended": appended,
        "dag_errors": dag_errors,
    }


# ---------------------------------------------------------------------------
# Dataset orchestration
# ---------------------------------------------------------------------------

def braid_dataset(dataset_name):
    """Braid a dataset using native content.ingest per subdirectory."""
    ds_path = DATA_ROOT / dataset_name
    marker = ds_path / ".braided"

    if marker.exists():
        return {"dataset": dataset_name, "status": "skipped", "reason": "already braided"}

    tag = f"[{dataset_name}]"

    subdirs = sorted(
        d.name for d in ds_path.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    state_path = ds_path / ".native_braid_state"
    state = _load_state(state_path, dataset_name)

    if not state.get("spine_id"):
        spine_result = rpc_result("loamspine", "spine.create", {
            "name": f"federation:{dataset_name}",
            "owner": COMMITTER_DID,
        })
        state["spine_id"] = (
            spine_result.get("spine_id") if isinstance(spine_result, dict)
            else spine_result or "pending"
        )
        _save_state(state_path, state)

    spine_id = state["spine_id"]
    completed = state.get("chunks", {})
    is_chunked = len(subdirs) > 0

    if not is_chunked:
        subdirs = ["_flat"]

    already_done = sum(1 for s in subdirs if s in completed)
    print(f"{tag} Native braid: {len(subdirs)} chunks, "
          f"{already_done} done, spine={spine_id[:12]}...", flush=True)

    t_start = time.time()
    total_files = state.get("total_files", 0)
    total_bytes = state.get("total_bytes", 0)

    for si, chunk_name in enumerate(subdirs):
        if shutdown:
            break
        if chunk_name in completed:
            continue

        chunk_dir = ds_path if chunk_name == "_flat" else ds_path / chunk_name
        chunk_tag = f"{tag}[{chunk_name} {si+1}/{len(subdirs)}]"

        session_id = rpc_result("rhizocrypt", "dag.session.create", {
            "session_type": "General",
            "dataset": f"{dataset_name}/{chunk_name}",
            "committer": COMMITTER_DID,
        })

        result = braid_chunk(
            chunk_dir, dataset_name, chunk_name,
            session_id, spine_id, tag=chunk_tag,
        )

        if result:
            completed[chunk_name] = {
                "files": result["files"],
                "dedup": result["dedup"],
                "merkle_root": str(result["merkle_root"])[:64] if result["merkle_root"] else None,
                "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }
            total_files += result["files"]
            total_bytes += result["bytes"]
            state["chunks"] = completed
            state["total_files"] = total_files
            state["total_bytes"] = total_bytes
            _save_state(state_path, state)

    if shutdown:
        print(f"{tag} Interrupted — {len(completed)}/{len(subdirs)} chunks done. "
              f"Resume will continue.", flush=True)
        return {
            "dataset": dataset_name, "status": "interrupted",
            "chunks_done": len(completed), "chunks_total": len(subdirs),
        }

    import base64
    import blake3

    chunk_roots = [c["merkle_root"] for c in completed.values() if c.get("merkle_root")]
    roots_str = ",".join(str(r) for r in chunk_roots)
    composite_hash = blake3.blake3(roots_str.encode()).hexdigest()

    sign_payload = f"federation:{dataset_name}:{spine_id}:{len(chunk_roots)}"
    sig_result = _rpc("beardog", "sign", {
        "message": base64.b64encode(sign_payload.encode()).decode(),
        "key_id": "default",
    })
    signature = None
    if isinstance(sig_result, dict) and "result" in sig_result:
        sr = sig_result["result"]
        signature = sr.get("signature") if isinstance(sr, dict) else sr

    braid = _rpc("sweetgrass", "braid.create", {
        "content_hash": composite_hash,
        "mime_type": "application/x-chunked-braid",
        "size": total_bytes,
        "dataset": dataset_name,
        "license": "CC-BY-4.0",
        "committer": COMMITTER_DID,
        "session_id": spine_id,
        "merkle_root": composite_hash,
        "signature": signature,
        "chunk_count": len(chunk_roots),
    })

    marker_data = {
        "braided_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "braider": "native_braid",
        "files": total_files,
        "bytes": total_bytes,
        "spine_id": spine_id,
        "chunk_count": len(chunk_roots),
        "signature": signature,
    }
    with open(marker, "w") as f:
        json.dump(marker_data, f, indent=2)

    elapsed = time.time() - t_start
    print(f"{tag} COMPLETE: {total_files} files, {len(chunk_roots)} chunks, "
          f"{elapsed:.0f}s", flush=True)

    return {
        "dataset": dataset_name, "status": "complete",
        "files": total_files, "chunk_count": len(chunk_roots),
        "elapsed_s": round(elapsed),
    }


def _load_state(path, dataset_name):
    if path.exists():
        try:
            with open(path) as f:
                state = json.load(f)
            if state.get("dataset") == dataset_name:
                return state
        except (json.JSONDecodeError, KeyError):
            pass
    return {"dataset": dataset_name, "chunks": {}, "total_files": 0, "total_bytes": 0}


def _save_state(path, state):
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    tmp.rename(path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Native bulk braider")
    parser.add_argument("--only", help="Comma-separated dataset names")
    parser.add_argument("--skip", help="Comma-separated datasets to skip")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    only = set(args.only.split(",")) if args.only else None
    skip = set(args.skip.split(",")) if args.skip else set()

    datasets = sorted(
        d.name for d in DATA_ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".")
        and not (d / ".braided").exists()
    )

    if only:
        datasets = [d for d in datasets if d in only]
    datasets = [d for d in datasets if d not in skip]

    print(f"=== Native Braid ===", flush=True)
    print(f"Total unbraided: {len(datasets)}", flush=True)
    print(f"NVMe free: {nvme_free_gb():.0f} GB", flush=True)
    print(f"CAS family: {CAS_FAMILY}", flush=True)
    print(flush=True)

    if args.dry_run:
        for d in datasets:
            print(f"  {d}", flush=True)
        return

    results = []
    for ds in datasets:
        if shutdown:
            break
        result = braid_dataset(ds)
        results.append(result)

    print(f"\n=== Summary ===", flush=True)
    for r in results:
        status = r.get("status", "?")
        files = r.get("files", 0)
        print(f"  {r['dataset']}: {status} ({files} files)", flush=True)


if __name__ == "__main__":
    main()
