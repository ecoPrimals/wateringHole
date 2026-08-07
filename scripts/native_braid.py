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

Middle-out parallel architecture:
  - Multiple workers each claim different chunks (prefix dirs)
  - All workers share one spine (loamSpine) via .native_braid_state
  - Workers coordinate via .claim files (atomic file locking)
  - Oversized chunks get batch-staged to NVMe in sub-ranges
  - Workers "meet" when all chunks are committed to the spine

Per-chunk flow:
  1. claim_chunk(name)                                       [file lock]
  2. stage_batch(cold_dir → NVMe)                            [rsync, if oversized]
  3. content.ingest(NVMe_or_cold_path) → manifest            [nestGate Rust]
  4. dag.session.create → dag.event.append_batch(manifest)   [rhizoCrypt Rust]
  5. dag.dehydration.trigger → session.commit                [loamSpine Rust]
  6. unstage_batch()                                         [cleanup]

Usage:
    python3 native_braid.py --only alphafold_structures --worker 0/3   # worker 0 of 3
    python3 native_braid.py --only alphafold_structures --worker 1/3   # worker 1 of 3
    python3 native_braid.py --only alphafold_structures --worker 2/3   # worker 2 of 3
    python3 native_braid.py --only alphafold_structures                # single worker (all chunks)
    python3 native_braid.py --dry-run                                  # list what would run
"""

import argparse
import fcntl
import json
import os
import shutil
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

DATA_ROOT = Path("/mnt/nestgate/cold/zfs/data")
STAGE_ROOT = Path("/mnt/cas-hot/_stage")
CAS_FAMILY = "standalone"
COMMITTER_DID = "did:eco:westgate"
DAG_BATCH_SIZE = 500
SKIP_EXTENSIONS = {".part", ".tmp", ".lock", ".swp"}

STAGE_BATCH_MAX_GB = 400
STAGE_MIN_FREE_GB = 200
OVERSIZED_FILE_THRESHOLD = 100_000

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
# Chunk claiming — multiple workers coordinate via .claim files
# ---------------------------------------------------------------------------

def claim_chunk(ds_path, chunk_name, worker_id):
    """Atomically claim a chunk for this worker. Returns True if claimed."""
    claim_dir = ds_path / ".claims"
    claim_dir.mkdir(exist_ok=True)
    claim_file = claim_dir / f"{chunk_name}.claim"
    try:
        fd = os.open(str(claim_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"{worker_id}:{os.getpid()}:{time.time()}\n".encode())
        os.close(fd)
        return True
    except FileExistsError:
        return False


def is_chunk_claimed_or_done(ds_path, chunk_name, state):
    """Check if chunk is done (in state) or claimed by another worker."""
    if chunk_name in state.get("chunks", {}):
        return True
    claim_file = ds_path / ".claims" / f"{chunk_name}.claim"
    if claim_file.exists():
        try:
            age = time.time() - claim_file.stat().st_mtime
            if age > 86400:
                claim_file.unlink(missing_ok=True)
                return False
        except OSError:
            pass
        return True
    return False


def release_claim(ds_path, chunk_name):
    """Release a chunk claim (on error — successful chunks stay claimed)."""
    claim_file = ds_path / ".claims" / f"{chunk_name}.claim"
    claim_file.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Batch staging — oversized chunks staged to NVMe in sub-ranges
# ---------------------------------------------------------------------------

def probe_chunk_size(chunk_dir, cap=OVERSIZED_FILE_THRESHOLD, time_cap=15):
    """Quick probe: count files, abort if over cap. Returns (count, capped)."""
    count = 0
    t0 = time.time()
    try:
        for entry in os.scandir(str(chunk_dir)):
            if entry.is_file() and not entry.name.startswith("."):
                count += 1
                if count >= cap or (time.time() - t0) > time_cap:
                    return count, True
    except OSError:
        pass
    return count, False


STAGE_FILE_THRESHOLD = 200


def choose_staging_method(file_count):
    """Auto-select staging method based on experiment results.

    Findings (staging_experiment.py, Aug 2026):
      Type A (>200 small files): tar 1.6x faster than rsync (sequential readdir)
      Type B (few large files):  rsync ~1.3x faster than tar (single file, no pipe overhead)
      Type C/D (moderate):       rsync and tar equivalent
    """
    if file_count > STAGE_FILE_THRESHOLD:
        return "tar"
    return "rsync"


def stage_chunk_to_nvme(cold_dir, dataset_name, chunk_name, tag="",
                        method=None):
    """Stage a chunk from cold HDD to NVMe. Returns staged path or None."""
    free = nvme_free_gb()
    if free < STAGE_MIN_FREE_GB:
        print(f"{tag} NVMe {free:.0f} GB free — below staging threshold", flush=True)
        return None

    dst = STAGE_ROOT / dataset_name / chunk_name
    dst.mkdir(parents=True, exist_ok=True)

    if method is None:
        try:
            fc = sum(1 for e in os.scandir(str(cold_dir))
                     if e.is_file() and not e.name.startswith("."))
        except OSError:
            fc = 0
        method = choose_staging_method(fc)

    print(f"{tag} Staging → NVMe ({method})...", flush=True)
    t0 = time.time()

    if method == "tar":
        ok = _stage_tar(cold_dir, dst, tag)
    else:
        ok = _stage_rsync(cold_dir, dst, tag)

    if not ok:
        shutil.rmtree(dst, ignore_errors=True)
        return None

    elapsed = time.time() - t0
    print(f"{tag} Staged in {elapsed:.0f}s ({method})", flush=True)
    return dst


def _stage_rsync(cold_dir, dst, tag=""):
    try:
        result = subprocess.run(
            ["rsync", "-a", "--exclude=.*", f"{cold_dir}/", f"{dst}/"],
            capture_output=True, text=True, timeout=7200,
        )
        if result.returncode != 0:
            print(f"{tag} rsync failed: {result.stderr[:200]}", flush=True)
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"{tag} rsync timed out (2h)", flush=True)
        return False
    except Exception as e:
        print(f"{tag} rsync error: {e}", flush=True)
        return False


def _stage_tar(cold_dir, dst, tag=""):
    try:
        tar_create = subprocess.Popen(
            ["tar", "cf", "-", "--exclude=./.*", "-C", str(cold_dir), "."],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        tar_extract = subprocess.Popen(
            ["tar", "xf", "-", "-C", str(dst)],
            stdin=tar_create.stdout, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        tar_create.stdout.close()
        _, err = tar_extract.communicate(timeout=7200)
        tar_create.wait()
        if tar_extract.returncode != 0:
            print(f"{tag} tar failed: {err[:200]}", flush=True)
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"{tag} tar timed out (2h)", flush=True)
        return False
    except Exception as e:
        print(f"{tag} tar error: {e}", flush=True)
        return False


def unstage_chunk(dataset_name, chunk_name):
    """Remove staged chunk from NVMe."""
    dst = STAGE_ROOT / dataset_name / chunk_name
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)


def batch_stage_and_ingest(cold_dir, dataset_name, chunk_name,
                           session_id, spine_id, tag=""):
    """For oversized chunks: stage in filename-prefix batches, ingest each.

    Splits the flat directory into batches by first 6 characters of filename.
    Each batch is staged to NVMe, ingested, and cleaned up.
    All batches share the same DAG session.
    """
    prefixes = set()
    try:
        for entry in os.scandir(str(cold_dir)):
            if entry.is_file() and not entry.name.startswith("."):
                prefixes.add(entry.name[:6])
    except OSError as e:
        print(f"{tag} Failed to scan directory: {e}", flush=True)
        return None

    prefix_groups = sorted(prefixes)
    print(f"{tag} Oversized chunk: {len(prefix_groups)} prefix groups", flush=True)

    total_files = 0
    total_dedup = 0
    total_bytes = 0
    total_dag_appended = 0
    total_dag_errors = 0
    batch_num = 0

    i = 0
    while i < len(prefix_groups) and not shutdown:
        free = nvme_free_gb()
        batch_prefixes = []
        while i < len(prefix_groups):
            batch_prefixes.append(prefix_groups[i])
            i += 1
            if len(batch_prefixes) >= 200:
                break

        batch_num += 1
        batch_tag = f"{tag}[batch {batch_num}]"
        dst = STAGE_ROOT / dataset_name / f"{chunk_name}_b{batch_num}"
        dst.mkdir(parents=True, exist_ok=True)

        print(f"{batch_tag} Staging {len(batch_prefixes)} prefix groups → NVMe "
              f"({free:.0f} GB free)...", flush=True)
        t0 = time.time()

        find_patterns = " -o ".join(
            f'-name "{pfx}*"' for pfx in batch_prefixes
        )
        find_cmd = (f'find {cold_dir} -maxdepth 1 -type f '
                    f'\\( {find_patterns} \\) -print0')
        try:
            find_proc = subprocess.Popen(
                ["bash", "-c", find_cmd],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            tar_c = subprocess.Popen(
                ["tar", "cf", "-", "--null", "-T", "-"],
                stdin=find_proc.stdout, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            find_proc.stdout.close()
            tar_x = subprocess.Popen(
                ["tar", "xf", "-", "-C", str(dst),
                 "--strip-components",
                 str(len(Path(str(cold_dir)).parts))],
                stdin=tar_c.stdout, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            tar_c.stdout.close()
            tar_x.communicate(timeout=7200)
            tar_c.wait()
            find_proc.wait()
            if tar_x.returncode != 0:
                print(f"{batch_tag} tar stage failed", flush=True)
                shutil.rmtree(dst, ignore_errors=True)
                continue
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"{batch_tag} Stage error: {e}", flush=True)
            shutil.rmtree(dst, ignore_errors=True)
            continue

        stage_elapsed = time.time() - t0
        print(f"{batch_tag} Staged in {stage_elapsed:.0f}s (tar)", flush=True)

        cas_result = ingest_directory(dst, tag=batch_tag)
        manifest = cas_result.get("manifest", {})

        if manifest and not shutdown:
            dag_events = build_dag_events(manifest, dataset_name, session_id)
            appended, dag_errors = append_dag_batch(dag_events, tag=batch_tag)
            total_dag_appended += appended
            total_dag_errors += dag_errors

        total_files += cas_result.get("count", 0)
        total_dedup += cas_result.get("deduplicated", 0)
        total_bytes += cas_result.get("bytes_total", 0)

        shutil.rmtree(dst, ignore_errors=True)

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
            "vertex_count": total_dag_appended,
            "committer": COMMITTER_DID,
        })

    print(f"{tag} Committed: {total_dag_appended} events ({total_files} files, "
          f"{total_dedup} dedup), root={str(merkle_root)[:16]}...", flush=True)

    return {
        "chunk": chunk_name,
        "files": total_files,
        "dedup": total_dedup,
        "bytes": total_bytes,
        "merkle_root": merkle_root,
        "dag_appended": total_dag_appended,
        "dag_errors": total_dag_errors,
    }


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

def braid_dataset(dataset_name, worker_id="w0", worker_index=0, worker_count=1):
    """Braid a dataset using native content.ingest per subdirectory.

    Middle-out parallel: multiple workers each claim different chunks via
    file-based locking. All commit to the same spine. Workers can start
    from different points in the chunk list and "meet" when all are done.
    """
    ds_path = DATA_ROOT / dataset_name
    marker = ds_path / ".braided"

    if marker.exists():
        return {"dataset": dataset_name, "status": "skipped", "reason": "already braided"}

    tag = f"[{dataset_name}][{worker_id}]"

    subdirs = sorted(
        d.name for d in ds_path.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    state_path = ds_path / ".native_braid_state"
    lock_path = ds_path / ".native_braid_state.lock"

    state = _load_state_locked(state_path, lock_path, dataset_name)

    if not state.get("spine_id"):
        spine_result = rpc_result("loamspine", "spine.create", {
            "name": f"federation:{dataset_name}",
            "owner": COMMITTER_DID,
        })
        state["spine_id"] = (
            spine_result.get("spine_id") if isinstance(spine_result, dict)
            else spine_result or "pending"
        )
        _save_state_locked(state_path, lock_path, state)

    spine_id = state["spine_id"]
    is_chunked = len(subdirs) > 0

    if not is_chunked:
        subdirs = ["_flat"]

    my_chunks = subdirs[worker_index::worker_count]
    already_done = sum(1 for s in subdirs if s in state.get("chunks", {}))
    print(f"{tag} Native braid: {len(subdirs)} total chunks, "
          f"{already_done} done, {len(my_chunks)} assigned to this worker, "
          f"spine={spine_id[:12]}...", flush=True)

    t_start = time.time()
    my_files = 0
    my_bytes = 0
    my_committed = 0

    for si, chunk_name in enumerate(my_chunks):
        if shutdown:
            break

        if is_chunk_claimed_or_done(ds_path, chunk_name, _load_state_locked(state_path, lock_path, dataset_name)):
            continue

        if not claim_chunk(ds_path, chunk_name, worker_id):
            continue

        chunk_dir = ds_path if chunk_name == "_flat" else ds_path / chunk_name
        global_idx = subdirs.index(chunk_name) + 1
        chunk_tag = f"{tag}[{chunk_name} {global_idx}/{len(subdirs)}]"

        session_id = rpc_result("rhizocrypt", "dag.session.create", {
            "session_type": "General",
            "dataset": f"{dataset_name}/{chunk_name}",
            "committer": COMMITTER_DID,
        })

        file_count, is_oversized = probe_chunk_size(chunk_dir)

        if is_oversized:
            result = batch_stage_and_ingest(
                chunk_dir, dataset_name, chunk_name,
                session_id, spine_id, tag=chunk_tag,
            )
        else:
            staged = stage_chunk_to_nvme(chunk_dir, dataset_name, chunk_name, tag=chunk_tag)
            ingest_dir = staged if staged else chunk_dir
            result = braid_chunk(
                ingest_dir, dataset_name, chunk_name,
                session_id, spine_id, tag=chunk_tag,
            )
            if staged:
                unstage_chunk(dataset_name, chunk_name)

        if result:
            state = _load_state_locked(state_path, lock_path, dataset_name)
            state.setdefault("chunks", {})[chunk_name] = {
                "files": result["files"],
                "dedup": result["dedup"],
                "merkle_root": str(result["merkle_root"])[:64] if result["merkle_root"] else None,
                "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "worker": worker_id,
            }
            state["total_files"] = state.get("total_files", 0) + result["files"]
            state["total_bytes"] = state.get("total_bytes", 0) + result["bytes"]
            _save_state_locked(state_path, lock_path, state)
            my_files += result["files"]
            my_bytes += result["bytes"]
            my_committed += 1
        else:
            release_claim(ds_path, chunk_name)

    state = _load_state_locked(state_path, lock_path, dataset_name)
    all_done = len(state.get("chunks", {}))

    elapsed = time.time() - t_start
    print(f"{tag} Worker done: {my_committed} chunks, {my_files} files in {elapsed:.0f}s. "
          f"Dataset: {all_done}/{len(subdirs)} chunks total.", flush=True)

    if all_done >= len(subdirs) and not marker.exists():
        _finalize_dataset(dataset_name, state, subdirs, marker, tag)

    return {
        "dataset": dataset_name,
        "status": "complete" if all_done >= len(subdirs) else "partial",
        "worker": worker_id,
        "chunks_done_by_worker": my_committed,
        "chunks_done_total": all_done,
        "chunks_total": len(subdirs),
        "files": my_files,
        "elapsed_s": round(elapsed),
    }


def _finalize_dataset(dataset_name, state, subdirs, marker, tag):
    """Final braid: sign composite root, create sweetGrass braid, write marker."""
    import base64
    import blake3

    spine_id = state["spine_id"]
    completed = state.get("chunks", {})
    total_files = state.get("total_files", 0)
    total_bytes = state.get("total_bytes", 0)

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

    _rpc("sweetgrass", "braid.create", {
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

    print(f"{tag} FINALIZED: {total_files} files, {len(chunk_roots)} chunks, "
          f"spine={spine_id[:12]}...", flush=True)


def _load_state_locked(path, lock_path, dataset_name):
    """Load state with file lock for multi-worker safety."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(lock_path, "a+") as lf:
            fcntl.flock(lf, fcntl.LOCK_SH)
            try:
                if path.exists():
                    with open(path) as f:
                        state = json.load(f)
                    if state.get("dataset") == dataset_name:
                        return state
            except (json.JSONDecodeError, KeyError):
                pass
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)
    except OSError:
        pass
    return {"dataset": dataset_name, "chunks": {}, "total_files": 0, "total_bytes": 0}


def _save_state_locked(path, lock_path, state):
    """Save state with exclusive file lock for multi-worker safety."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            if path.exists():
                try:
                    with open(path) as f:
                        existing = json.load(f)
                    existing_chunks = existing.get("chunks", {})
                    existing_chunks.update(state.get("chunks", {}))
                    state["chunks"] = existing_chunks
                    state["total_files"] = sum(c.get("files", 0) for c in existing_chunks.values())
                    state["total_bytes"] = sum(c.get("bytes", 0) for c in existing_chunks.values())
                except (json.JSONDecodeError, KeyError):
                    pass
            tmp = path.with_suffix(".tmp")
            with open(tmp, "w") as f:
                json.dump(state, f, indent=2)
            tmp.rename(path)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Native bulk braider (middle-out parallel)")
    parser.add_argument("--only", help="Comma-separated dataset names")
    parser.add_argument("--skip", help="Comma-separated datasets to skip")
    parser.add_argument("--worker", help="Worker assignment: INDEX/TOTAL (e.g. 0/3, 1/3, 2/3)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    worker_index = 0
    worker_count = 1
    if args.worker:
        parts = args.worker.split("/")
        worker_index = int(parts[0])
        worker_count = int(parts[1])
    worker_id = f"w{worker_index}"

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

    print(f"=== Native Braid [{worker_id}] ===", flush=True)
    print(f"Worker: {worker_index+1}/{worker_count}", flush=True)
    print(f"Total unbraided: {len(datasets)}", flush=True)
    print(f"NVMe free: {nvme_free_gb():.0f} GB", flush=True)
    print(f"CAS family: {CAS_FAMILY}", flush=True)
    print(flush=True)

    if args.dry_run:
        for d in datasets:
            ds_path = DATA_ROOT / d
            subdirs = sorted(
                sd.name for sd in ds_path.iterdir()
                if sd.is_dir() and not sd.name.startswith(".")
            ) or ["_flat"]
            my_chunks = subdirs[worker_index::worker_count]
            print(f"  {d}: {len(my_chunks)}/{len(subdirs)} chunks assigned", flush=True)
        return

    results = []
    for ds in datasets:
        if shutdown:
            break
        result = braid_dataset(ds, worker_id, worker_index, worker_count)
        results.append(result)

    print(f"\n=== Summary [{worker_id}] ===", flush=True)
    for r in results:
        status = r.get("status", "?")
        done = r.get("chunks_done_by_worker", 0)
        total_done = r.get("chunks_done_total", 0)
        total = r.get("chunks_total", 0)
        print(f"  {r['dataset']}: {status} (worker: {done} chunks, "
              f"total: {total_done}/{total})", flush=True)


if __name__ == "__main__":
    main()
