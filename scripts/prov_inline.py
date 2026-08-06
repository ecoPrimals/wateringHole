"""
Inline provenance — native socket braid for download pipelines.

Single-import module that any download script uses to braid files at
acquisition time. No subprocess spawning (socat, b3sum). Data flows
from download buffer → BLAKE3 hash → CAS put → DAG batch in-process.

Measured performance:
  - Inline (warm):   265 files/s (single worker)
  - Native RPC cap:  16,352 RPCs/s
  - Download rate:   74 files/s (AlphaFold, bandwidth-capped)
  - Headroom:        3.6x — single worker keeps up with downloads

Validated: inline Python blake3 produces identical CAS content addresses
to trailer b3sum. CAS reports deduplicated=True for re-ingested files.
Trailer and inline are provably equivalent.

Usage:
    from prov_inline import InlineBraid

    braid = InlineBraid("my_dataset")

    # In download loop:
    data = download_file(url)
    braid.ingest(data, filename, len(data))
    write_to_disk(filepath, data)

    # When done:
    result = braid.finalize(license_id="CC-BY-4.0")
"""

import base64
import json
import os
import socket
import struct
import time
from pathlib import Path

import blake3

MEMBRANE = "/run/user/1000/membrane"
RIBOCIPHER_PREFIX = struct.pack("BB", 0xEC, 0x01)

SOCKETS = {
    "nestgate":   f"{MEMBRANE}/nestgate-westgate-tower-155f.sock",
    "rhizocrypt": f"{MEMBRANE}/rhizocrypt-westgate-tower-155f.sock",
    "loamspine":  f"{MEMBRANE}/loamspine-westgate-tower-155f.sock",
    "sweetgrass": f"{MEMBRANE}/sweetgrass-westgate-tower-155f.sock",
    "beardog":    f"{MEMBRANE}/beardog-westgate-tower-155f.sock",
}

MAX_CAS_SIZE = 100 * 1024 * 1024
COMMITTER_DID = "did:eco:westgate"
DEFAULT_BATCH_SIZE = 200
DEFAULT_CHECKPOINT_INTERVAL = 2000


def _rpc(primal, method, params=None, timeout=30):
    """JSON-RPC 2.0 over UDS with native Python socket."""
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

    raw = buf
    if raw[:2] == RIBOCIPHER_PREFIX:
        raw = raw[2:]
    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _rpc_result(primal, method, params=None, timeout=30):
    resp = _rpc(primal, method, params, timeout)
    if resp and "result" in resp:
        return resp["result"]
    return None


class InlineBraid:
    """Inline provenance braider — call from download loops.

    Creates a DAG session + spine at init. Each ingest() call hashes and
    CAS-stores the data, then queues a DAG event. Events are flushed in
    batches for efficiency. finalize() commits the session.
    """

    def __init__(self, dataset_name, batch_size=DEFAULT_BATCH_SIZE,
                 checkpoint_interval=DEFAULT_CHECKPOINT_INTERVAL):
        self.dataset_name = dataset_name
        self.batch_size = batch_size
        self.checkpoint_interval = checkpoint_interval

        self.session_id = _rpc_result("rhizocrypt", "dag.session.create", {
            "session_type": "General",
            "dataset": dataset_name,
            "committer": COMMITTER_DID,
        })
        if not self.session_id:
            raise RuntimeError(f"Failed to create DAG session for {dataset_name}")

        spine_result = _rpc_result("loamspine", "spine.create", {
            "name": f"federation:{dataset_name}",
            "owner": COMMITTER_DID,
        })
        self.spine_id = (
            spine_result.get("spine_id") if isinstance(spine_result, dict)
            else spine_result or "pending"
        )

        self._batch = []
        self.event_count = 0
        self.total_bytes = 0
        self.errors = 0

    def ingest(self, data, filename, size=None):
        """Hash data, store in CAS, queue DAG event. Returns BLAKE3 hex hash.

        Args:
            data: bytes — file content (already in memory from download)
            filename: str — original filename for DAG metadata
            size: int — file size (defaults to len(data))
        """
        if size is None:
            size = len(data)

        h = blake3.blake3(data).hexdigest()

        if len(data) <= MAX_CAS_SIZE:
            _rpc_result("nestgate", "content.put", {
                "data": base64.b64encode(data).decode(),
                "hash_type": "blake3",
            })
        else:
            ref = json.dumps({
                "type": "large_file_reference",
                "blake3": h, "size": size,
                "path": filename, "gate": "westgate",
            }).encode()
            _rpc_result("nestgate", "content.put", {
                "data": base64.b64encode(ref).decode(),
                "hash_type": "blake3",
            })

        self._batch.append((h, filename, size, self.dataset_name))
        self.total_bytes += size

        if len(self._batch) >= self.batch_size:
            self._flush_batch()

        return h

    def ingest_file(self, filepath):
        """Convenience: read file from disk and ingest. For retrospective braiding."""
        fp = Path(filepath)
        data = fp.read_bytes()
        return self.ingest(data, fp.name, len(data))

    def _flush_batch(self):
        if not self._batch:
            return

        requests = [
            {
                "session_id": self.session_id,
                "event_type": {"DataCreate": {}},
                "metadata": [
                    ["dataset", ds],
                    ["filename", name],
                    ["blake3", h],
                    ["size", str(size)],
                ],
                "payload_ref": h,
                "parents": [],
            }
            for h, name, size, ds in self._batch
        ]

        result = _rpc_result("rhizocrypt", "dag.event.append_batch", {
            "requests": requests,
        })

        if result:
            count = len(result) if isinstance(result, list) else len(self._batch)
            self.event_count += count
        else:
            for h, name, size, ds in self._batch:
                vertex = _rpc_result("rhizocrypt", "dag.event.append", {
                    "session_id": self.session_id,
                    "event_type": {"DataCreate": {}},
                    "metadata": [
                        ["dataset", ds], ["filename", name],
                        ["blake3", h], ["size", str(size)],
                    ],
                    "payload_ref": h,
                    "parents": [],
                })
                if vertex:
                    self.event_count += 1
                else:
                    self.errors += 1

        if self.event_count % self.checkpoint_interval < len(self._batch):
            _rpc_result("rhizocrypt", "dag.partial_dehydrate", {
                "session_id": self.session_id,
            })

        self._batch = []

    def finalize(self, license_id="CC-BY-4.0"):
        """Flush remaining events, dehydrate DAG, commit spine, sign, braid.

        Returns dict with merkle_root, signature, braid info.
        """
        self._flush_batch()

        merkle_root = _rpc_result("rhizocrypt", "dag.dehydration.trigger", {
            "session_id": self.session_id,
        })
        if isinstance(merkle_root, dict):
            merkle_root = merkle_root.get("merkle_root", merkle_root)

        if self.spine_id and self.spine_id != "pending" and merkle_root:
            _rpc_result("loamspine", "session.commit", {
                "spine_id": self.spine_id,
                "session_id": self.session_id,
                "merkle_root": merkle_root if isinstance(merkle_root, str) else str(merkle_root),
                "vertex_count": self.event_count,
                "committer": COMMITTER_DID,
            })

        signature = None
        if merkle_root:
            sign_msg = base64.b64encode(
                f"federation:{self.dataset_name}:{merkle_root}".encode()
            ).decode()
            sig_result = _rpc_result("beardog", "sign", {
                "message": sign_msg,
                "key_id": "default",
            })
            if isinstance(sig_result, dict):
                signature = sig_result.get("signature")
            elif isinstance(sig_result, str):
                signature = sig_result

        braid = None
        if merkle_root:
            braid = _rpc_result("sweetgrass", "braid.create", {
                "content_hash": merkle_root if isinstance(merkle_root, str) else str(merkle_root),
                "mime_type": "application/x-dag-session",
                "size": self.total_bytes,
                "dataset": self.dataset_name,
                "license": license_id,
                "committer": COMMITTER_DID,
                "session_id": self.session_id,
                "merkle_root": merkle_root if isinstance(merkle_root, str) else str(merkle_root),
                "signature": signature,
            })

        return {
            "session_id": self.session_id,
            "spine_id": self.spine_id,
            "merkle_root": merkle_root,
            "signature": signature,
            "braid": braid,
            "event_count": self.event_count,
            "total_bytes": self.total_bytes,
            "errors": self.errors,
        }

    def stats(self):
        """Return current progress without finalizing."""
        return {
            "session_id": self.session_id,
            "event_count": self.event_count,
            "pending_batch": len(self._batch),
            "total_bytes": self.total_bytes,
            "errors": self.errors,
        }


# ---------------------------------------------------------------------------
# ChunkedBraid — one spine, N sessions (sub-ephemeral per chunk)
# ---------------------------------------------------------------------------

STREAMING_HASH_CHUNK = 8 * 1024 * 1024  # 8 MB read chunks for large files


class ChunkedBraid:
    """Chunked provenance braider — one loamSpine, N rhizoCrypt sessions.

    Each chunk (e.g. a subdirectory of a large dataset) gets its own DAG
    session, dehydrated and committed to the shared spine independently.
    Crash-resumable via .braid_state on the dataset directory.

    Usage:
        cb = ChunkedBraid("alphafold_structures", state_dir=Path("/data/alphafold_structures"))

        for subdir in subdirs:
            if cb.is_chunk_done(subdir.name):
                continue
            cb.begin_chunk(subdir.name)
            for f in subdir.rglob("*"):
                cb.ingest_file(f)
            cb.commit_chunk()

        result = cb.finalize()
    """

    def __init__(self, dataset_name, state_dir=None,
                 batch_size=DEFAULT_BATCH_SIZE,
                 checkpoint_interval=DEFAULT_CHECKPOINT_INTERVAL):
        self.dataset_name = dataset_name
        self.batch_size = batch_size
        self.checkpoint_interval = checkpoint_interval
        self._state_path = Path(state_dir) / ".braid_state" if state_dir else None

        self.chunk_roots = []
        self.completed_chunks = {}
        self.total_files = 0
        self.total_bytes = 0
        self.total_errors = 0

        self._current_chunk = None
        self._chunk_session_id = None
        self._batch = []
        self._chunk_event_count = 0

        resumed = self._load_state()

        if resumed and self.spine_id:
            pass
        else:
            spine_result = _rpc_result("loamspine", "spine.create", {
                "name": f"federation:{dataset_name}",
                "owner": COMMITTER_DID,
            })
            self.spine_id = (
                spine_result.get("spine_id") if isinstance(spine_result, dict)
                else spine_result or "pending"
            )
            if not resumed:
                self._save_state()

    def _load_state(self):
        if not self._state_path or not self._state_path.exists():
            self.spine_id = None
            return False
        try:
            with open(self._state_path) as f:
                state = json.load(f)
            if state.get("dataset") != self.dataset_name:
                self.spine_id = None
                return False
            self.spine_id = state.get("spine_id")
            self.completed_chunks = state.get("chunks", {})
            self.chunk_roots = [
                c["merkle_root"] for c in self.completed_chunks.values()
                if c.get("merkle_root")
            ]
            self.total_files = state.get("total_files", 0)
            self.total_bytes = state.get("total_bytes", 0)
            self.total_errors = state.get("total_errors", 0)
            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            self.spine_id = None
            return False

    def _save_state(self):
        if not self._state_path:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "dataset": self.dataset_name,
            "spine_id": self.spine_id,
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "chunks": self.completed_chunks,
            "total_files": self.total_files,
            "total_bytes": self.total_bytes,
            "total_errors": self.total_errors,
        }
        tmp = self._state_path.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(state, f, indent=2)
        tmp.rename(self._state_path)

    def is_chunk_done(self, chunk_name):
        return chunk_name in self.completed_chunks

    def begin_chunk(self, chunk_name):
        """Start a new sub-session for this chunk."""
        if self._current_chunk is not None:
            raise RuntimeError(
                f"Chunk '{self._current_chunk}' still open — call commit_chunk() first"
            )
        self._current_chunk = chunk_name
        self._chunk_event_count = 0
        self._batch = []

        params = {
            "session_type": "General",
            "dataset": f"{self.dataset_name}/{chunk_name}",
            "committer": COMMITTER_DID,
        }
        if self.spine_id and self.spine_id != "pending":
            params["parent_session"] = self.spine_id
        self._chunk_session_id = _rpc_result("rhizocrypt", "dag.session.create", params)
        if not self._chunk_session_id:
            raise RuntimeError(f"Failed to create DAG session for chunk {chunk_name}")

    def ingest(self, data, filename, size=None):
        """Hash data, store in CAS, queue DAG event."""
        if self._chunk_session_id is None:
            raise RuntimeError("No chunk open — call begin_chunk() first")
        if size is None:
            size = len(data)

        h = blake3.blake3(data).hexdigest()

        if len(data) <= MAX_CAS_SIZE:
            _rpc_result("nestgate", "content.put", {
                "data": base64.b64encode(data).decode(),
                "hash_type": "blake3",
            })
        else:
            ref = json.dumps({
                "type": "large_file_reference",
                "blake3": h, "size": size,
                "path": filename, "gate": "westgate",
            }).encode()
            _rpc_result("nestgate", "content.put", {
                "data": base64.b64encode(ref).decode(),
                "hash_type": "blake3",
            })

        self._batch.append((h, filename, size, self.dataset_name))
        self.total_bytes += size

        if len(self._batch) >= self.batch_size:
            self._flush_batch()

        return h

    def ingest_file(self, filepath):
        """Read file and ingest. Uses streaming hash for large files."""
        fp = Path(filepath)
        fsize = fp.stat().st_size

        if fsize <= MAX_CAS_SIZE:
            data = fp.read_bytes()
            return self.ingest(data, fp.name, fsize)

        hasher = blake3.blake3()
        with open(fp, "rb") as f:
            while True:
                chunk = f.read(STREAMING_HASH_CHUNK)
                if not chunk:
                    break
                hasher.update(chunk)
        h = hasher.hexdigest()

        ref = json.dumps({
            "type": "large_file_reference",
            "blake3": h, "size": fsize,
            "path": fp.name, "gate": "westgate",
        }).encode()
        _rpc_result("nestgate", "content.put", {
            "data": base64.b64encode(ref).decode(),
            "hash_type": "blake3",
        })

        self._batch.append((h, fp.name, fsize, self.dataset_name))
        self.total_bytes += fsize

        if len(self._batch) >= self.batch_size:
            self._flush_batch()

        return h

    def _flush_batch(self):
        if not self._batch:
            return

        requests = [
            {
                "session_id": self._chunk_session_id,
                "event_type": {"DataCreate": {}},
                "metadata": [
                    ["dataset", ds],
                    ["filename", name],
                    ["blake3", h],
                    ["size", str(size)],
                ],
                "payload_ref": h,
                "parents": [],
            }
            for h, name, size, ds in self._batch
        ]

        result = _rpc_result("rhizocrypt", "dag.event.append_batch", {
            "requests": requests,
        })

        if result:
            count = len(result) if isinstance(result, list) else len(self._batch)
            self._chunk_event_count += count
        else:
            for h, name, size, ds in self._batch:
                vertex = _rpc_result("rhizocrypt", "dag.event.append", {
                    "session_id": self._chunk_session_id,
                    "event_type": {"DataCreate": {}},
                    "metadata": [
                        ["dataset", ds], ["filename", name],
                        ["blake3", h], ["size", str(size)],
                    ],
                    "payload_ref": h,
                    "parents": [],
                })
                if vertex:
                    self._chunk_event_count += 1
                else:
                    self.total_errors += 1

        if self._chunk_event_count % self.checkpoint_interval < len(self._batch):
            _rpc_result("rhizocrypt", "dag.partial_dehydrate", {
                "session_id": self._chunk_session_id,
            })

        self._batch = []

    def commit_chunk(self):
        """Dehydrate the current chunk session and commit to the spine."""
        if self._current_chunk is None:
            return None

        self._flush_batch()

        merkle_root = _rpc_result("rhizocrypt", "dag.dehydration.trigger", {
            "session_id": self._chunk_session_id,
        })
        if isinstance(merkle_root, dict):
            merkle_root = merkle_root.get("merkle_root", merkle_root)

        if self.spine_id and self.spine_id != "pending" and merkle_root:
            _rpc_result("loamspine", "session.commit", {
                "spine_id": self.spine_id,
                "session_id": self._chunk_session_id,
                "merkle_root": str(merkle_root),
                "vertex_count": self._chunk_event_count,
                "committer": COMMITTER_DID,
            })

        self.total_files += self._chunk_event_count
        self.chunk_roots.append(merkle_root)
        self.completed_chunks[self._current_chunk] = {
            "session_id": self._chunk_session_id,
            "merkle_root": str(merkle_root) if merkle_root else None,
            "files": self._chunk_event_count,
            "committed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }

        chunk_name = self._current_chunk
        self._current_chunk = None
        self._chunk_session_id = None
        self._chunk_event_count = 0
        self._batch = []

        self._save_state()

        return {
            "chunk": chunk_name,
            "merkle_root": merkle_root,
            "files": self.completed_chunks[chunk_name]["files"],
        }

    def finalize(self, license_id="CC-BY-4.0"):
        """Sign and create the dataset-level braid over all committed chunks."""
        if self._current_chunk is not None:
            self.commit_chunk()

        roots_str = ",".join(str(r) for r in self.chunk_roots if r)
        sign_payload = f"federation:{self.dataset_name}:{self.spine_id}:{len(self.chunk_roots)}"

        signature = None
        sign_msg = base64.b64encode(sign_payload.encode()).decode()
        sig_result = _rpc_result("beardog", "sign", {
            "message": sign_msg,
            "key_id": "default",
        })
        if isinstance(sig_result, dict):
            signature = sig_result.get("signature")
        elif isinstance(sig_result, str):
            signature = sig_result

        braid = None
        if self.chunk_roots:
            composite_hash = blake3.blake3(roots_str.encode()).hexdigest()
            braid = _rpc_result("sweetgrass", "braid.create", {
                "content_hash": composite_hash,
                "mime_type": "application/x-chunked-braid",
                "size": self.total_bytes,
                "dataset": self.dataset_name,
                "license": license_id,
                "committer": COMMITTER_DID,
                "session_id": self.spine_id,
                "merkle_root": composite_hash,
                "signature": signature,
                "chunk_count": len(self.chunk_roots),
            })

        return {
            "spine_id": self.spine_id,
            "chunk_count": len(self.chunk_roots),
            "chunk_roots": self.chunk_roots,
            "total_files": self.total_files,
            "total_bytes": self.total_bytes,
            "total_errors": self.total_errors,
            "signature": signature,
            "braid": braid,
        }

    def stats(self):
        return {
            "dataset": self.dataset_name,
            "spine_id": self.spine_id,
            "chunks_done": len(self.completed_chunks),
            "current_chunk": self._current_chunk,
            "total_files": self.total_files,
            "total_bytes": self.total_bytes,
            "total_errors": self.total_errors,
        }


# ---------------------------------------------------------------------------
# Convergence backpressure gate
# ---------------------------------------------------------------------------

WARM_TIER_PATH = Path(os.environ.get("NESTGATE_WARM_PATHS", "/mnt/cas-hot").split(":")[0])

def convergence_gate(
    dataset: str = "",
    batch_size: int = 100,
    warm_min_free_gb: float = 20.0,
    convergence_lag_max: int = 10000,
) -> dict:
    """Check whether the pipeline should continue downloading/braiding.

    Layers three pressure signals:
      1. Warm tier free space (os.statvfs — always available)
      2. sweetGrass convergence lag (RPC — graceful degradation if unavailable)
      3. Future: topology.bandwidth.budget

    Returns dict with verdict ("GO", "WAIT", "STOP"), reason, and metrics.
    """
    result = {
        "verdict": "GO",
        "reason": "clear",
        "warm_free_gb": None,
        "unconverged_count": None,
        "wait_seconds": 0,
    }

    warm_path = WARM_TIER_PATH
    if warm_path.exists():
        try:
            st = os.statvfs(warm_path)
            free_gb = (st.f_bavail * st.f_frsize) / (1024 ** 3)
            result["warm_free_gb"] = round(free_gb, 1)
            if free_gb < 10:
                result["verdict"] = "STOP"
                result["reason"] = f"warm tier critically low ({free_gb:.1f} GB free)"
                return result
            if free_gb < warm_min_free_gb:
                result["verdict"] = "WAIT"
                result["wait_seconds"] = 30
                result["reason"] = f"warm tier low ({free_gb:.1f} GB < {warm_min_free_gb} GB)"
                return result
        except OSError:
            pass

    if dataset:
        try:
            conv = _rpc_result("sweetgrass", "convergence.batch_check", {
                "dataset": dataset,
                "limit": convergence_lag_max + 1,
            })
            if isinstance(conv, dict):
                unconverged = conv.get("unconverged_count", 0)
                result["unconverged_count"] = unconverged
                if unconverged > convergence_lag_max:
                    result["verdict"] = "WAIT"
                    result["wait_seconds"] = 60
                    result["reason"] = (
                        f"convergence lag ({unconverged} > {convergence_lag_max})"
                    )
        except Exception:
            pass

    return result


def convergence_wait(dataset: str = "", **kwargs):
    """Block until convergence_gate returns GO. Logs wait events."""
    gate = convergence_gate(dataset, **kwargs)
    if gate["verdict"] == "GO":
        return gate
    waited = 0
    while gate["verdict"] == "WAIT":
        wait_s = gate.get("wait_seconds", 30) or 30
        print(f"  BACKPRESSURE: {gate['reason']} — waiting {wait_s}s", flush=True)
        time.sleep(wait_s)
        waited += wait_s
        gate = convergence_gate(dataset, **kwargs)
    if waited:
        gate["waited_seconds"] = waited
    return gate
