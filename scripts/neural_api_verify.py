#!/usr/bin/env python3
"""
Neural API Routing Verification — N2-N4 validation across all atomics.

Tests that biomeOS Neural API correctly routes capability.call to each
primal in the Tower, Provenance Trio, and Nest atomics. Reports pass/fail
per domain with response details.

This script replaces ad-hoc verification by systematically probing every
domain that should be routable through the Neural API.

Usage:
    python3 neural_api_verify.py                  # full verification
    python3 neural_api_verify.py --domain braid   # single domain
    python3 neural_api_verify.py --json            # machine-readable
    python3 neural_api_verify.py --socket /path    # custom neural-api socket
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

RIBOCIPHER_PREFIX = struct.pack("BB", 0xEC, 0x01)


def neural_rpc(method, params=None, timeout=10, socket_path=None):
    """Send a JSON-RPC 2.0 request to the Neural API socket."""
    sock_path = socket_path or NEURAL_API_SOCKET
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1,
    })
    data = RIBOCIPHER_PREFIX + req.encode() + b"\n"

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
    except socket.timeout:
        s.close()
        return {"error": "timeout"}
    except (ConnectionError, OSError) as e:
        s.close()
        return {"error": str(e)}
    s.close()

    raw = bytes(buf)
    if raw[:2] == RIBOCIPHER_PREFIX:
        raw = raw[2:]
    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"error": f"invalid response: {raw[:200]}"}


def capability_call(capability, operation, args=None, timeout=10, socket_path=None):
    """Route a capability.call through Neural API."""
    params = {
        "capability": capability,
        "operation": operation,
    }
    if args:
        params["args"] = args
    return neural_rpc("capability.call", params, timeout, socket_path)


def semantic_call(method, params=None, timeout=10, socket_path=None):
    """Use semantic fallback — call domain.operation directly as method name."""
    return neural_rpc(method, params, timeout, socket_path)


# Verification probes: (name, domain, operation, args, expected_primal, validate_fn)
PROBES = [
    # Tower Atomic
    {
        "name": "Tower: health.check → bearDog",
        "atomic": "tower",
        "domain": "health",
        "operation": "check",
        "args": {},
        "primal": "bearDog",
        "validate": lambda r: "result" in r,
    },
    {
        "name": "Tower: discovery.peers → songBird",
        "atomic": "tower",
        "domain": "discovery",
        "operation": "peers",
        "args": {},
        "primal": "songBird",
        "validate": lambda r: "result" in r,
    },
    # Provenance Trio
    {
        "name": "Provenance: braid.list → sweetGrass",
        "atomic": "provenance",
        "domain": "braid",
        "operation": "list",
        "args": {"filter": {}, "limit": 5},
        "primal": "sweetGrass",
        "validate": lambda r: "result" in r,
    },
    {
        "name": "Provenance: braid.query → sweetGrass",
        "atomic": "provenance",
        "domain": "braid",
        "operation": "query",
        "args": {"filter": {}, "limit": 1},
        "primal": "sweetGrass",
        "validate": lambda r: "result" in r,
    },
    {
        "name": "Provenance: spine.status → loamSpine",
        "atomic": "provenance",
        "domain": "spine",
        "operation": "status",
        "args": {},
        "primal": "loamSpine",
        "validate": lambda r: "result" in r,
    },
    # Nest Atomic
    {
        "name": "Nest: content.list → nestGate",
        "atomic": "nest",
        "domain": "content",
        "operation": "list",
        "args": {"limit": 5},
        "primal": "nestGate",
        "validate": lambda r: "result" in r,
    },
    {
        "name": "Nest: content.exists → nestGate",
        "atomic": "nest",
        "domain": "content",
        "operation": "exists",
        "args": {"hash": "blake3:0000000000000000000000000000000000000000000000000000000000000000"},
        "primal": "nestGate",
        "validate": lambda r: "result" in r,
    },
]

SEMANTIC_PROBES = [
    {
        "name": "Semantic: braid.list (direct method)",
        "method": "braid.list",
        "params": {"filter": {}, "limit": 5},
        "primal": "sweetGrass",
        "validate": lambda r: "result" in r,
    },
    {
        "name": "Semantic: health.check (direct method)",
        "method": "health.check",
        "params": {},
        "primal": "bearDog",
        "validate": lambda r: "result" in r,
    },
]


def run_probe(probe, socket_path=None):
    """Run a single capability.call probe and return result dict."""
    t0 = time.time()
    try:
        resp = capability_call(
            probe["domain"],
            probe["operation"],
            probe.get("args"),
            timeout=10,
            socket_path=socket_path,
        )
        elapsed = time.time() - t0
        passed = probe["validate"](resp)
        error_msg = None
        if not passed:
            if "error" in resp:
                err = resp["error"]
                error_msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            else:
                error_msg = "unexpected response shape"
    except Exception as e:
        elapsed = time.time() - t0
        passed = False
        error_msg = str(e)
        resp = {}

    return {
        "name": probe["name"],
        "atomic": probe.get("atomic", "semantic"),
        "domain": probe.get("domain", probe.get("method", "?")),
        "primal": probe["primal"],
        "passed": passed,
        "elapsed_ms": round(elapsed * 1000),
        "error": error_msg,
        "response_keys": list(resp.keys()) if isinstance(resp, dict) else None,
    }


def run_semantic_probe(probe, socket_path=None):
    """Run a semantic fallback probe."""
    t0 = time.time()
    try:
        resp = semantic_call(
            probe["method"],
            probe.get("params"),
            timeout=10,
            socket_path=socket_path,
        )
        elapsed = time.time() - t0
        passed = probe["validate"](resp)
        error_msg = None
        if not passed:
            if "error" in resp:
                err = resp["error"]
                error_msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            else:
                error_msg = "unexpected response shape"
    except Exception as e:
        elapsed = time.time() - t0
        passed = False
        error_msg = str(e)
        resp = {}

    return {
        "name": probe["name"],
        "atomic": "semantic",
        "domain": probe["method"],
        "primal": probe["primal"],
        "passed": passed,
        "elapsed_ms": round(elapsed * 1000),
        "error": error_msg,
        "response_keys": list(resp.keys()) if isinstance(resp, dict) else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Neural API Routing Verification")
    parser.add_argument("--domain", type=str, help="Test a single domain only")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--socket", type=str, help="Custom neural-api socket path")
    parser.add_argument("--semantic-only", action="store_true", help="Only test semantic fallback")
    args = parser.parse_args()

    socket_path = args.socket

    if not os.path.exists(socket_path or NEURAL_API_SOCKET):
        print(f"Neural API socket not found: {socket_path or NEURAL_API_SOCKET}")
        print("Is biomeOS running in Coordinated state?")
        sys.exit(1)

    results = []

    if not args.semantic_only:
        probes = PROBES
        if args.domain:
            probes = [p for p in probes if p["domain"] == args.domain]
        for probe in probes:
            r = run_probe(probe, socket_path)
            results.append(r)

    for probe in SEMANTIC_PROBES:
        if args.domain and probe["method"].split(".")[0] != args.domain:
            continue
        r = run_semantic_probe(probe, socket_path)
        results.append(r)

    if args.json:
        passed = sum(1 for r in results if r["passed"])
        json.dump({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "socket": socket_path or NEURAL_API_SOCKET,
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "results": results,
        }, sys.stdout, indent=2)
        print()
    else:
        print(f"\nNeural API Routing Verification")
        print(f"Socket: {socket_path or NEURAL_API_SOCKET}")
        print(f"{'=' * 80}")
        print(f"{'Probe':50s} {'Result':8s} {'Time':>8s} {'Notes'}")
        print(f"{'-' * 80}")

        for r in results:
            status = "\033[32mPASS\033[0m" if r["passed"] else "\033[31mFAIL\033[0m"
            time_str = f"{r['elapsed_ms']}ms"
            notes = r["error"] or ""
            print(f"{r['name']:50s} {status:17s} {time_str:>8s} {notes}")

        print(f"{'=' * 80}")
        passed = sum(1 for r in results if r["passed"])
        failed = len(results) - passed
        color = "\033[32m" if failed == 0 else "\033[31m"
        print(f"  {color}{passed}/{len(results)} passed\033[0m")

        if failed > 0:
            print(f"\n  Known issues:")
            print(f"  - sweetGrass may not have announced to the capability registry")
            print(f"  - capability.call may timeout on provenance routing (AAR gap #1)")
            print(f"  - Verify biomeOS is in Coordinated state, not Bootstrap")
        print()


if __name__ == "__main__":
    main()
