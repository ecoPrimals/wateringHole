#!/usr/bin/env python3
"""
Neural API Braid Client — canonical interface for braid operations.

All braid operations route through biomeOS Neural API via capability.call.
If Neural API routing fails (sweetGrass not announced, capability.call
timeout), falls back to direct sweetGrass socket. This fallback will be
removed once the routing gaps are resolved.

This replaces direct-socket braid calls in convergence_check.py and
other scripts. Callers should use this module instead of managing
individual primal sockets.

Usage as module:
    from neural_braid import NeuralBraidClient

    client = NeuralBraidClient()
    braids = client.braid_list(tag="kegg")
    braid = client.braid_get("braid-uuid")
    results = client.convergence_check(["blake3:abc...", "blake3:def..."])

Usage as CLI:
    python3 neural_braid.py list                            # list recent braids
    python3 neural_braid.py list --tag kegg --limit 20      # filter by tag
    python3 neural_braid.py get <braid-id>                  # get braid by ID
    python3 neural_braid.py get-by-hash <blake3:hash>       # get braid by content hash
    python3 neural_braid.py query --tag alphafold           # query braids
    python3 neural_braid.py convergence <hash1> <hash2>     # check convergence
    python3 neural_braid.py verify                          # verify routing works
"""

import argparse
import json
import os
import socket
import struct
import sys
import time

NEURAL_API_SOCKET = os.environ.get(
    "BIOMEOS_NEURAL_API_SOCKET",
    "/run/user/1000/membrane/biomeos-neural-api.sock",
)

MEMBRANE = os.environ.get("MEMBRANE_DIR", "/run/user/1000/membrane")

RIBOCIPHER_PREFIX = struct.pack("BB", 0xEC, 0x01)


def _uds_rpc(sock_path, method, params=None, timeout=30, use_ribocipher=True):
    """Raw JSON-RPC 2.0 over UDS."""
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1,
    })
    data = (RIBOCIPHER_PREFIX if use_ribocipher else b"") + req.encode() + b"\n"

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(sock_path)
        s.sendall(data)
        buf = bytearray()
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            if b"\n" in buf:
                break
    except (socket.timeout, ConnectionError, OSError) as e:
        s.close()
        raise ConnectionError(f"UDS {sock_path}: {e}")
    s.close()

    raw = bytes(buf)
    if raw[:2] == RIBOCIPHER_PREFIX:
        raw = raw[2:]
    resp = json.loads(raw.decode("utf-8", errors="replace"))
    if "error" in resp:
        err = resp["error"]
        msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
        raise RuntimeError(f"RPC {method}: {msg}")
    return resp.get("result")


def _find_sweetgrass_socket():
    """Discover sweetGrass socket by scanning membrane directory."""
    for f in os.listdir(MEMBRANE):
        if f.startswith("sweetgrass") and f.endswith(".sock"):
            return os.path.join(MEMBRANE, f)
    return None


class NeuralBraidClient:
    """Braid operations via biomeOS Neural API with direct-socket fallback.

    Primary path: capability.call through Neural API socket.
    Fallback: direct sweetGrass socket (used when Neural API routing
    fails, e.g. sweetGrass not announced to capability registry).
    """

    def __init__(self, neural_api_socket=None, sweetgrass_socket=None):
        self.neural_api = neural_api_socket or NEURAL_API_SOCKET
        self._sweetgrass = sweetgrass_socket
        self._fallback_warned = False

    @property
    def sweetgrass_socket(self):
        if self._sweetgrass is None:
            self._sweetgrass = _find_sweetgrass_socket()
        return self._sweetgrass

    def _call_neural_api(self, capability, operation, args=None, timeout=10):
        """Route through biomeOS Neural API."""
        params = {"capability": capability, "operation": operation}
        if args:
            params["args"] = args
        return _uds_rpc(self.neural_api, "capability.call", params, timeout)

    def _call_semantic(self, method, params=None, timeout=10):
        """Semantic fallback — call domain.operation as method name on Neural API."""
        return _uds_rpc(self.neural_api, method, params, timeout)

    def _call_direct(self, method, params=None, timeout=30):
        """Direct sweetGrass socket fallback."""
        sg = self.sweetgrass_socket
        if not sg:
            raise ConnectionError("sweetGrass socket not found in membrane directory")
        if not self._fallback_warned:
            print("  [fallback] Neural API routing unavailable, using direct sweetGrass socket",
                  file=sys.stderr)
            self._fallback_warned = True
        return _uds_rpc(sg, method, params, timeout)

    def _braid_call(self, method, params=None, timeout=10):
        """Try Neural API first (semantic), fall back to direct socket."""
        try:
            return self._call_semantic(method, params, timeout)
        except Exception:
            pass
        try:
            domain, op = method.split(".", 1)
            return self._call_neural_api(domain, op, params, timeout)
        except Exception:
            pass
        return self._call_direct(method, params, timeout)

    def braid_list(self, tag=None, source_gate=None, limit=100, offset=0):
        """List braids with optional filtering.

        Returns: {"total": N, "items": [...]}
        """
        filter_obj = {}
        if tag:
            filter_obj["tag"] = tag
        if source_gate:
            filter_obj["source_gate"] = source_gate
        params = {"filter": filter_obj, "limit": limit, "offset": offset}
        return self._braid_call("braid.list", params)

    def braid_get(self, braid_id):
        """Get a braid by ID.

        Returns: {"braid": {...}}
        """
        return self._braid_call("braid.get", {"id": braid_id})

    def braid_get_by_hash(self, data_hash):
        """Get a braid by content hash.

        Returns: {"braid": {...}} or None
        """
        return self._braid_call("braid.get_by_hash", {"data_hash": data_hash})

    def braid_query(self, tag=None, data_hash=None, limit=50):
        """Query braids with filtering.

        Returns: {"total": N, "items": [...]}
        """
        filter_obj = {}
        if tag:
            filter_obj["tag"] = tag
        if data_hash:
            filter_obj["data_hash"] = data_hash
        return self._braid_call("braid.query", {"filter": filter_obj, "limit": limit})

    def braid_create(self, data_hash, name, tags=None, source_session=None,
                     source_merkle_root=None, mime_type=None):
        """Create a braid with canonical wire format.

        Returns: {"braid_id": "uuid"}
        """
        params = {"data_hash": data_hash, "name": name}
        if tags:
            params["tags"] = tags
        if source_session:
            params["source_session"] = source_session
        if source_merkle_root:
            params["source_merkle_root"] = source_merkle_root
        if mime_type:
            params["mime_type"] = mime_type
        return self._braid_call("braid.create", params)

    def braid_commit(self, braid_id):
        """Commit a braid to loamSpine permanent ledger.

        Returns: {"committed": true, "spine_entry": "entry-id"}
        """
        return self._braid_call("braid.commit", {"braid_id": braid_id})

    def convergence_check(self, data_hashes):
        """Check convergence for a batch of content hashes.

        Args:
            data_hashes: list of "blake3:..." strings (max 1000)

        Returns: {"results": [{"hash": "...", "converged": bool}, ...]}
        """
        return self._braid_call(
            "convergence.batch_check",
            {"data_hashes": data_hashes[:1000]},
            timeout=30,
        )

    def convergence_single(self, data_hash):
        """Check convergence for a single content hash."""
        return self._braid_call(
            "convergence.check",
            {"data_hash": data_hash},
            timeout=10,
        )

    def verify_routing(self):
        """Quick check that braid routing works. Returns (ok, method_used, detail)."""
        for method_name, label in [
            ("semantic", "braid.list via semantic fallback"),
            ("capability.call", "braid.list via capability.call"),
            ("direct", "braid.list via direct socket"),
        ]:
            try:
                if method_name == "semantic":
                    result = self._call_semantic("braid.list", {"filter": {}, "limit": 1})
                elif method_name == "capability.call":
                    result = self._call_neural_api("braid", "list", {"filter": {}, "limit": 1})
                else:
                    result = self._call_direct("braid.list", {"filter": {}, "limit": 1})
                return True, label, result
            except Exception:
                continue
        return False, "all methods failed", None


def main():
    parser = argparse.ArgumentParser(description="Neural API Braid Client")
    sub = parser.add_subparsers(dest="command")

    ls = sub.add_parser("list", help="List braids")
    ls.add_argument("--tag", type=str, help="Filter by tag")
    ls.add_argument("--gate", type=str, help="Filter by source gate")
    ls.add_argument("--limit", type=int, default=20, help="Max results")
    ls.add_argument("--json", action="store_true", help="JSON output")

    get = sub.add_parser("get", help="Get braid by ID")
    get.add_argument("id", type=str, help="Braid ID")
    get.add_argument("--json", action="store_true", help="JSON output")

    gbh = sub.add_parser("get-by-hash", help="Get braid by content hash")
    gbh.add_argument("hash", type=str, help="blake3:... hash")
    gbh.add_argument("--json", action="store_true", help="JSON output")

    qry = sub.add_parser("query", help="Query braids")
    qry.add_argument("--tag", type=str, help="Filter by tag")
    qry.add_argument("--hash", type=str, help="Filter by data hash")
    qry.add_argument("--limit", type=int, default=50, help="Max results")
    qry.add_argument("--json", action="store_true", help="JSON output")

    conv = sub.add_parser("convergence", help="Check convergence")
    conv.add_argument("hashes", nargs="+", help="blake3:... hashes to check")
    conv.add_argument("--json", action="store_true", help="JSON output")

    sub.add_parser("verify", help="Verify braid routing works")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = NeuralBraidClient()

    if args.command == "verify":
        ok, method, detail = client.verify_routing()
        if ok:
            print(f"\033[32mPASS\033[0m: {method}")
            if detail:
                total = detail.get("total", "?") if isinstance(detail, dict) else "?"
                print(f"  sweetGrass reports {total} braids")
        else:
            print(f"\033[31mFAIL\033[0m: {method}")
            sys.exit(1)
        return

    if args.command == "list":
        result = client.braid_list(tag=args.tag, source_gate=args.gate, limit=args.limit)
        if hasattr(args, "json") and args.json:
            json.dump(result, sys.stdout, indent=2)
            print()
        else:
            items = result.get("items", []) if isinstance(result, dict) else []
            total = result.get("total", len(items)) if isinstance(result, dict) else 0
            print(f"\nBraids: {total} total, showing {len(items)}")
            print(f"{'ID':40s} {'Name':20s} {'Hash':20s}")
            print("-" * 82)
            for b in items:
                if isinstance(b, dict):
                    bid = str(b.get("id", "?"))[:38]
                    name = str(b.get("name", ""))[:18]
                    h = str(b.get("data_hash", ""))[:18]
                    print(f"{bid:40s} {name:20s} {h:20s}")

    elif args.command == "get":
        result = client.braid_get(args.id)
        json.dump(result, sys.stdout, indent=2)
        print()

    elif args.command == "get-by-hash":
        result = client.braid_get_by_hash(args.hash)
        json.dump(result, sys.stdout, indent=2)
        print()

    elif args.command == "query":
        result = client.braid_query(tag=args.tag, data_hash=args.hash, limit=args.limit)
        if hasattr(args, "json") and args.json:
            json.dump(result, sys.stdout, indent=2)
            print()
        else:
            items = result.get("items", []) if isinstance(result, dict) else []
            total = result.get("total", len(items)) if isinstance(result, dict) else 0
            print(f"\nQuery results: {total} total, showing {len(items)}")
            for b in items:
                if isinstance(b, dict):
                    print(f"  {b.get('id', '?')} — {b.get('name', '')} ({b.get('data_hash', '')[:20]})")

    elif args.command == "convergence":
        result = client.convergence_check(args.hashes)
        if hasattr(args, "json") and args.json:
            json.dump(result, sys.stdout, indent=2)
            print()
        else:
            results = result.get("results", []) if isinstance(result, dict) else []
            for r in results:
                if isinstance(r, dict):
                    h = r.get("hash", "?")[:30]
                    c = r.get("converged", False)
                    status = "\033[32mCONVERGED\033[0m" if c else "\033[33mPENDING\033[0m"
                    print(f"  {h}  {status}")


if __name__ == "__main__":
    main()
