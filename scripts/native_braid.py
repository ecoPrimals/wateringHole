#!/usr/bin/env python3
"""
Native bulk braider — Python is ONLY the RPC orchestrator.

Python walks directories and hashes; Rust primals do CAS storage + dedup + DAG:
  - content.put      → Rust CAS store with BLAKE3 dedup
  - content.exists   → Rust dedup check (skip re-upload)
  - dag.event.append_batch → Rust DAG event recording
  - dag.dehydration.trigger → Rust merkle tree computation
  - session.commit   → Rust spine commit
  - braid.create     → Rust provenance braid

Middle-out parallel architecture:
  - Multiple workers each claim different chunks (prefix dirs)
  - All workers share one spine (loamSpine) via .native_braid_state
  - Workers coordinate via .claim files (atomic file locking)
  - Oversized chunks get batch-staged to NVMe in sub-ranges
  - Workers "meet" when all chunks are committed to the spine

Per-chunk flow:
  1. claim_chunk(name)                                       [file lock]
  2. stage_batch(cold_dir → NVMe)                            [rsync, if oversized]
  3. walk + BLAKE3 + content.put(NVMe files) → manifest      [Python + nestGate]
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
import base64
import fcntl
import hashlib
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


CAS_PUT_INLINE_MAX = 64 * 1024 * 1024  # base64 inline ceiling for content.put


def nvme_free_gb():
    st = os.statvfs("/mnt/cas-hot")
    return (st.f_bavail * st.f_frsize) / (1024 ** 3)


def streaming_blake3(filepath, chunk_size=4 * 1024 * 1024):
    """Stream BLAKE3 hash for arbitrarily large files (avoids OOM)."""
    try:
        import blake3 as _blake3
        h = _blake3.blake3()
    except ImportError:
        h = hashlib.blake2b(digest_size=32)
    sz = 0
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(chunk_size)
            if not buf:
                break
            h.update(buf)
            sz += len(buf)
    return h.hexdigest(), sz


def cas_put_file(filepath, tag=""):
    """Hash a file with streaming BLAKE3 and store in CAS via content.put.

    Small files (<=CAS_PUT_INLINE_MAX) are sent inline as base64.
    Large files are streamed in chunks to avoid OOM.
    nestGate deduplicates by BLAKE3 — if the hash already exists, it's a no-op.
    """
    blake3_hex, file_size = streaming_blake3(filepath)

    # Check dedup first to avoid reading data again
    exists_resp = _rpc("nestgate", "content.exists", {"hash": blake3_hex}, timeout=30)
    if isinstance(exists_resp, dict) and "result" in exists_resp:
        r = exists_resp["result"]
        if isinstance(r, dict) and r.get("exists"):
            if tag:
                mb = file_size / 1048576
                print(f"{tag} CAS dedup: {filepath.name} ({mb:.0f} MB)", flush=True)
            return blake3_hex, file_size, True

    if file_size <= CAS_PUT_INLINE_MAX:
        with open(filepath, "rb") as f:
            data_b64 = base64.b64encode(f.read()).decode()
        result = _rpc("nestgate", "content.put", {
            "content_base64": data_b64,
            "hash": blake3_hex,
        }, timeout=120)
    else:
        # Large file — read in chunks and send as base64
        # nestGate content.put requires the full payload; stream BLAKE3
        # already verified the hash. Read and encode in one pass.
        with open(filepath, "rb") as f:
            data_b64 = base64.b64encode(f.read()).decode()
        result = _rpc("nestgate", "content.put", {
            "content_base64": data_b64,
            "hash": blake3_hex,
        }, timeout=3600)

    dedup = False
    if isinstance(result, dict) and "result" in result:
        r = result["result"]
        dedup = r.get("deduplicated", False) if isinstance(r, dict) else False
    if tag:
        mb = file_size / 1048576
        dup_str = " (dedup)" if dedup else ""
        print(f"{tag} CAS: {filepath.name} ({mb:.0f} MB){dup_str}", flush=True)
    return blake3_hex, file_size, dedup


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


def is_chunk_claimed_or_done(ds_path, chunk_name, state, incremental=False):
    """Check if chunk is done (in state) or claimed by another worker.

    In incremental mode, a "done" chunk is reopened if the directory now
    has more files than when it was last braided — new ingress needs a braid.
    """
    chunk_state = state.get("chunks", {}).get(chunk_name)
    if chunk_state:
        if not incremental:
            return True
        chunk_dir = ds_path if chunk_name in ("_flat", "_root") else ds_path / chunk_name
        if chunk_dir.is_dir():
            try:
                current_count = sum(1 for e in os.scandir(str(chunk_dir))
                                    if e.is_file() and not e.name.startswith("."))
            except OSError:
                return True
            braided_count = chunk_state.get("files", 0)
            if current_count > braided_count:
                release_claim(ds_path, chunk_name)
                return False
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
# Core: content.put → DAG → spine pipeline
# ---------------------------------------------------------------------------

def ingest_directory(directory, tag=""):
    """Walk directory, BLAKE3-hash each file, store in CAS via content.put.

    Returns manifest dict {relative_path: blake3_hex} and stats.
    Python walks the directory; Rust does the CAS storage + dedup.
    """
    t0 = time.time()
    directory = Path(directory)
    manifest = {}
    count = 0
    dedup = 0
    total_bytes = 0

    entries = []
    for entry in os.scandir(str(directory)):
        if entry.is_file() and not entry.name.startswith("."):
            ext = entry.name.rsplit(".", 1)[-1] if "." in entry.name else ""
            if f".{ext}" not in SKIP_EXTENSIONS:
                entries.append(entry)

    for i, entry in enumerate(entries):
        if shutdown:
            break
        rel = entry.name
        filepath = directory / rel
        try:
            blake3_hex, fsize, is_dedup = cas_put_file(filepath)
            manifest[rel] = blake3_hex
            count += 1
            total_bytes += fsize
            if is_dedup:
                dedup += 1
        except Exception as e:
            print(f"{tag} CAS error: {rel}: {e}", flush=True)

        if tag and (i + 1) % 500 == 0:
            elapsed = time.time() - t0
            rate = count / elapsed if elapsed > 0 else 0
            print(f"{tag} CAS: {count}/{len(entries)} files "
                  f"({dedup} dedup), {elapsed:.0f}s ({rate:.0f}/s)",
                  flush=True)

    elapsed = time.time() - t0
    if tag:
        rate = count / elapsed if elapsed > 0 else 0
        print(f"{tag} CAS: {count} files ({dedup} dedup), "
              f"{total_bytes / 1048576:.0f} MB, {elapsed:.0f}s ({rate:.0f}/s)",
              flush=True)

    return {
        "manifest": manifest,
        "count": count,
        "deduplicated": dedup,
        "bytes_total": total_bytes,
    }


def build_dag_events(manifest, dataset_name, session_id):
    """Convert CAS manifest to DAG event batch requests."""
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

    try:
        merkle_root = rpc_result("rhizocrypt", "dag.dehydration.trigger", {
            "session_id": session_id,
        })
        if isinstance(merkle_root, dict):
            merkle_root = merkle_root.get("merkle_root", merkle_root)
    except RuntimeError as e:
        merkle_root = hashlib.blake2b(
            json.dumps(list(manifest.keys()), sort_keys=True).encode(),
            digest_size=32,
        ).hexdigest()
        print(f"{tag} dehydration fallback: {e}", flush=True)

    if spine_id and spine_id != "pending" and merkle_root:
        try:
            rpc_result("loamspine", "session.commit", {
                "spine_id": spine_id,
                "session_id": session_id,
                "session_hash": str(merkle_root),
                "merkle_root": str(merkle_root),
                "vertex_count": appended,
                "committer": COMMITTER_DID,
            })
        except RuntimeError as e:
            print(f"{tag} spine commit deferred (beardog sign unavailable): {e}", flush=True)

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
# Root-level file braiding (for datasets with both subdirs and root files)
# ---------------------------------------------------------------------------

def braid_root_files(ds_path, dataset_name, session_id, spine_id, tag=""):
    """Braid only the top-level files of a dataset (not subdirectories).

    ALL files are staged to NVMe before processing — cold is for durability,
    not for work.
    """
    root_files = []
    for entry in os.scandir(str(ds_path)):
        if entry.is_file() and not entry.name.startswith("."):
            ext = entry.name.rsplit(".", 1)[-1] if "." in entry.name else ""
            if ext not in {"lock", "tmp", "part"}:
                root_files.append(entry)

    if not root_files:
        print(f"{tag} No root-level files", flush=True)
        return None

    total_size_gb = sum(f.stat().st_size for f in root_files) / (1024 ** 3)
    free = nvme_free_gb()

    if total_size_gb > free - STAGE_MIN_FREE_GB:
        print(f"{tag} Root files too large ({total_size_gb:.0f} GB) for NVMe "
              f"({free:.0f} GB free) — batch staging", flush=True)
        return _braid_root_files_batched(
            ds_path, root_files, dataset_name, session_id, spine_id, tag)

    dst = STAGE_ROOT / dataset_name / "_root"
    dst.mkdir(parents=True, exist_ok=True)

    print(f"{tag} Staging {len(root_files)} root files "
          f"({total_size_gb:.1f} GB) → NVMe...", flush=True)
    t0 = time.time()
    for f in root_files:
        shutil.copy2(f.path, str(dst / f.name))
    stage_elapsed = time.time() - t0
    print(f"{tag} Staged in {stage_elapsed:.0f}s "
          f"({total_size_gb * 1024 / max(stage_elapsed, 1):.0f} MB/s)", flush=True)

    cas_result = ingest_directory(dst, tag=tag)
    manifest = cas_result.get("manifest", {})
    total_bytes = cas_result.get("bytes_total", 0)
    total_dedup = cas_result.get("deduplicated", 0)

    shutil.rmtree(dst, ignore_errors=True)

    if not manifest or shutdown:
        return None

    dag_events = build_dag_events(manifest, dataset_name, session_id)
    appended, dag_errors = append_dag_batch(dag_events, tag=tag)

    try:
        merkle_root = rpc_result("rhizocrypt", "dag.dehydration.trigger", {
            "session_id": session_id,
        })
        if isinstance(merkle_root, dict):
            merkle_root = merkle_root.get("merkle_root", merkle_root)
    except RuntimeError as e:
        merkle_root = hashlib.blake2b(
            json.dumps(list(manifest.keys()), sort_keys=True).encode(),
            digest_size=32,
        ).hexdigest()
        print(f"{tag} dehydration fallback: {e}", flush=True)

    if spine_id and spine_id != "pending" and merkle_root:
        try:
            rpc_result("loamspine", "session.commit", {
                "spine_id": spine_id,
                "session_id": session_id,
                "session_hash": str(merkle_root),
                "merkle_root": str(merkle_root),
                "vertex_count": appended,
                "committer": COMMITTER_DID,
            })
        except RuntimeError as e:
            print(f"{tag} spine commit deferred (beardog sign unavailable): {e}", flush=True)

    large_count = sum(1 for f in root_files
                      if f.stat().st_size > CAS_PUT_INLINE_MAX)
    small_count = len(root_files) - large_count
    print(f"{tag} Root committed: {appended} events "
          f"({small_count} small + {large_count} large files), "
          f"root={str(merkle_root)[:16]}...", flush=True)

    return {
        "chunk": "_root",
        "files": len(manifest),
        "dedup": total_dedup,
        "bytes": total_bytes,
        "merkle_root": merkle_root,
        "dag_appended": appended,
        "dag_errors": dag_errors,
    }


def _braid_root_files_batched(ds_path, root_files, dataset_name,
                               session_id, spine_id, tag=""):
    """Batch-stage root files when they exceed NVMe capacity."""
    manifest = {}
    total_bytes = 0
    total_dedup = 0
    batch_num = 0
    batch = []
    batch_size = 0
    max_batch_gb = STAGE_BATCH_MAX_GB

    sorted_files = sorted(root_files, key=lambda f: f.stat().st_size)

    for f in sorted_files:
        fsize = f.stat().st_size
        if batch and (batch_size + fsize) / (1024 ** 3) > max_batch_gb:
            _process_root_batch(batch, batch_num, dataset_name, tag,
                                manifest, locals())
            batch = []
            batch_size = 0
        batch.append(f)
        batch_size += fsize

    if batch:
        batch_num += 1
        dst = STAGE_ROOT / dataset_name / f"_root_b{batch_num}"
        dst.mkdir(parents=True, exist_ok=True)
        print(f"{tag}[batch {batch_num}] Staging {len(batch)} files "
              f"({batch_size / (1024 ** 3):.1f} GB) → NVMe...", flush=True)
        for f in batch:
            shutil.copy2(f.path, str(dst / f.name))
        cas_result = ingest_directory(dst, tag=f"{tag}[batch {batch_num}]")
        manifest.update(cas_result.get("manifest", {}))
        total_bytes += cas_result.get("bytes_total", 0)
        total_dedup += cas_result.get("deduplicated", 0)
        shutil.rmtree(dst, ignore_errors=True)

    if not manifest or shutdown:
        return None

    dag_events = build_dag_events(manifest, dataset_name, session_id)
    appended, dag_errors = append_dag_batch(dag_events, tag=tag)

    try:
        merkle_root = rpc_result("rhizocrypt", "dag.dehydration.trigger", {
            "session_id": session_id,
        })
        if isinstance(merkle_root, dict):
            merkle_root = merkle_root.get("merkle_root", merkle_root)
    except RuntimeError as e:
        merkle_root = hashlib.blake2b(
            json.dumps(list(manifest.keys()), sort_keys=True).encode(),
            digest_size=32,
        ).hexdigest()
        print(f"{tag} dehydration fallback: {e}", flush=True)

    if spine_id and spine_id != "pending" and merkle_root:
        try:
            rpc_result("loamspine", "session.commit", {
                "spine_id": spine_id,
                "session_id": session_id,
                "session_hash": str(merkle_root),
                "merkle_root": str(merkle_root),
                "vertex_count": appended,
                "committer": COMMITTER_DID,
            })
        except RuntimeError as e:
            print(f"{tag} spine commit deferred (beardog sign unavailable): {e}", flush=True)

    print(f"{tag} Root batched committed: {appended} events, "
          f"root={str(merkle_root)[:16]}...", flush=True)

    return {
        "chunk": "_root",
        "files": len(manifest),
        "dedup": total_dedup,
        "bytes": total_bytes,
        "merkle_root": merkle_root,
        "dag_appended": appended,
        "dag_errors": dag_errors,
    }


# ---------------------------------------------------------------------------
# Dataset orchestration
# ---------------------------------------------------------------------------

def braid_dataset(dataset_name, worker_id="w0", worker_index=0, worker_count=1,
                   incremental=False):
    """Braid a dataset using content.put per subdirectory.

    Middle-out parallel: multiple workers each claim different chunks via
    file-based locking. All commit to the same spine. Workers can start
    from different points in the chunk list and "meet" when all are done.

    --incremental: re-scan even already-braided datasets for new chunks
    (subdirs or files added since the .braided marker was written).
    """
    ds_path = DATA_ROOT / dataset_name
    marker = ds_path / ".braided"

    if marker.exists() and not incremental:
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
    else:
        root_files = [e.name for e in os.scandir(str(ds_path))
                      if e.is_file() and not e.name.startswith(".")
                      and e.name.split(".")[-1] not in {"lock", "tmp", "part"}]
        if root_files:
            subdirs = ["_root"] + subdirs

    if incremental and marker.exists():
        done_chunks = state.get("chunks", {})
        new_chunks = [s for s in subdirs if s not in done_chunks]
        grown_chunks = []
        for s in subdirs:
            if s in done_chunks:
                chunk_dir = ds_path if s in ("_flat", "_root") else ds_path / s
                if chunk_dir.is_dir():
                    try:
                        current = sum(1 for e in os.scandir(str(chunk_dir))
                                      if e.is_file() and not e.name.startswith("."))
                    except OSError:
                        continue
                    if current > done_chunks[s].get("files", 0):
                        grown_chunks.append((s, done_chunks[s]["files"], current))
        if not new_chunks and not grown_chunks:
            return {"dataset": dataset_name, "status": "skipped",
                    "reason": "incremental: no new data"}
        if new_chunks:
            print(f"{tag} Incremental: {len(new_chunks)} new chunks",
                  flush=True)
        if grown_chunks:
            for name, old, cur in grown_chunks:
                print(f"{tag} Incremental: {name} grew {old}→{cur} files",
                      flush=True)

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

        if is_chunk_claimed_or_done(ds_path, chunk_name, _load_state_locked(state_path, lock_path, dataset_name), incremental=incremental):
            continue

        if not claim_chunk(ds_path, chunk_name, worker_id):
            continue

        chunk_dir = ds_path if chunk_name in ("_flat", "_root") else ds_path / chunk_name
        global_idx = subdirs.index(chunk_name) + 1
        chunk_tag = f"{tag}[{chunk_name} {global_idx}/{len(subdirs)}]"

        session_id = rpc_result("rhizocrypt", "dag.session.create", {
            "session_type": "General",
            "dataset": f"{dataset_name}/{chunk_name}",
            "committer": COMMITTER_DID,
        })

        if chunk_name == "_root":
            result = braid_root_files(
                ds_path, dataset_name, session_id, spine_id, tag=chunk_tag)
        else:
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

    if all_done >= len(subdirs) and (not marker.exists() or incremental):
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
        "data_hash": composite_hash,
        "mime_type": "application/x-chunked-braid",
        "size": total_bytes,
        "strand_id": f"{dataset_name}-{int(time.time())}",
        "metadata": {
            "dataset": dataset_name,
            "license": "CC-BY-4.0",
            "committer": COMMITTER_DID,
            "spine_id": spine_id,
            "merkle_root": composite_hash,
            "signature": signature,
            "chunk_count": len(chunk_roots),
        },
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
    parser.add_argument("--incremental", action="store_true",
                        help="Re-scan already-braided datasets for new files/chunks")
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

    if args.incremental:
        datasets = sorted(
            d.name for d in DATA_ROOT.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
    else:
        datasets = sorted(
            d.name for d in DATA_ROOT.iterdir()
            if d.is_dir() and not d.name.startswith(".")
            and not (d / ".braided").exists()
        )

    if only:
        datasets = [d for d in datasets if d in only]
    datasets = [d for d in datasets if d not in skip]

    mode_str = "incremental" if args.incremental else "fresh"
    print(f"=== Native Braid [{worker_id}] ({mode_str}) ===", flush=True)
    print(f"Worker: {worker_index+1}/{worker_count}", flush=True)
    print(f"Datasets to process: {len(datasets)}", flush=True)
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
            braided = " [BRAIDED]" if (ds_path / ".braided").exists() else ""
            print(f"  {d}{braided}: {len(my_chunks)}/{len(subdirs)} chunks assigned",
                  flush=True)
        return

    results = []
    for ds in datasets:
        if shutdown:
            break
        result = braid_dataset(ds, worker_id, worker_index, worker_count,
                               incremental=args.incremental)
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
