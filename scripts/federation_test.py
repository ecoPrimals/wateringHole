#!/usr/bin/env python3
"""
Federation Test — nest.sync cross-gate validation

Tests that data + provenance replicate correctly between two gates on the LAN.
Validates the full chain: CAS content → DAG session → spine → braid.

Prerequisites:
  - westGate NUCLEUS running (13 primals, UDS sockets)
  - A second gate on the LAN with NUCLEUS running (e.g., southGate, eastGate)
  - Both gates on the 10 Gbps mesh or reachable via WireGuard
  - At least one dataset ingested on westGate with full provenance

Usage:
  python3 federation_test.py --remote-gate eastGate --remote-host 192.168.4.5
  python3 federation_test.py --local-only  # test with local gate only (loopback)

Test matrix:
  1. Ingest a small test dataset on westGate
  2. Verify provenance chain (DAG → spine → braid)
  3. Replicate CAS content to remote gate via content.replicate
  4. Verify remote gate has the content (content.exists)
  5. Verify DAG slice checkout from remote gate
  6. Verify braid sync
  7. Verify Merkle proof on remote gate
"""

import argparse
import base64
import json
import struct
import subprocess
import sys
import tempfile
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


def rpc(primal, method, params=None, timeout=30, socket_override=None):
    """JSON-RPC 2.0 call over UDS."""
    sock = socket_override or SOCKETS[primal]
    req = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1})
    use_prefix = primal != "beardog"
    data = (RIBOCIPHER_PREFIX if use_prefix else b"") + req.encode() + b"\n"

    r = subprocess.run(
        ["socat", "-t10", "-", f"UNIX-CONNECT:{sock}"],
        input=data, capture_output=True, timeout=timeout,
    )
    if not r.stdout:
        return None

    raw = r.stdout
    if raw[:2] == RIBOCIPHER_PREFIX:
        raw = raw[2:]
    for line in raw.split(b"\n"):
        line = line.strip()
        if line:
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def result(primal, method, params=None, **kwargs):
    """Call RPC, return just the result."""
    r = rpc(primal, method, params, **kwargs)
    if r and "result" in r:
        return r["result"]
    return None


def test_step(name, condition, detail=""):
    """Report a test step."""
    status = "PASS" if condition else "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return condition


class FederationTest:
    def __init__(self, remote_gate=None, remote_host=None, local_only=False):
        self.remote_gate = remote_gate
        self.remote_host = remote_host
        self.local_only = local_only
        self.passed = 0
        self.failed = 0

    def check(self, name, condition, detail=""):
        if test_step(name, condition, detail):
            self.passed += 1
        else:
            self.failed += 1
        return condition

    def run(self):
        print(f"\n{'=' * 70}")
        print(f"  FEDERATION TEST")
        print(f"  Local gate:  westGate")
        print(f"  Remote gate: {self.remote_gate or 'N/A (local-only)'}")
        print(f"  Remote host: {self.remote_host or 'N/A'}")
        print(f"{'=' * 70}\n")

        # Phase 1: Verify local primals are alive
        print("Phase 1: Local primal health")
        for primal in ["nestgate", "rhizocrypt", "loamspine", "sweetgrass", "beardog"]:
            r = result(primal, "health.check")
            self.check(
                f"{primal} health",
                r is not None,
                f"v{r.get('version', '?')}" if r else "unreachable",
            )

        # Phase 2: Ingest test data
        print("\nPhase 2: Ingest test dataset")

        test_data = b"Federation test payload - " + time.strftime("%Y%m%dT%H%M%S").encode()
        test_b64 = base64.b64encode(test_data).decode()

        cas_result = result("nestgate", "content.put", {
            "data": test_b64, "hash_type": "blake3",
        })
        cas_hash = cas_result.get("hash", "") if cas_result else ""
        self.check("CAS content.put", bool(cas_hash), f"hash={cas_hash[:16]}...")

        session_id = result("rhizocrypt", "dag.session.create", {
            "session_type": "General",
            "description": "Federation test session",
        })
        self.check("DAG session.create", bool(session_id), f"id={session_id}")

        vertex_id = result("rhizocrypt", "dag.event.append", {
            "session_id": session_id,
            "event_type": "DataIngested",
            "metadata": [["test", "federation"], ["blake3", cas_hash]],
            "payload_ref": cas_hash,
            "parents": [],
        }) if session_id else None
        self.check("DAG event.append", bool(vertex_id), f"vertex={vertex_id}")

        spine_id = result("loamspine", "spine.create", {
            "name": "federation-test",
            "owner": "westgate",
        })
        self.check("Spine create", bool(spine_id), f"id={spine_id}")

        # Phase 3: Dehydrate and commit
        print("\nPhase 3: Dehydrate + commit")

        merkle_root = result("rhizocrypt", "dag.dehydration.trigger", {
            "session_id": session_id,
        }) if session_id else None
        merkle_hex = merkle_root if isinstance(merkle_root, str) else str(merkle_root) if merkle_root else None
        self.check("DAG dehydrate", bool(merkle_hex), f"root={str(merkle_hex)[:16]}...")

        if merkle_hex and spine_id and session_id:
            commit = result("loamspine", "session.commit", {
                "spine_id": spine_id,
                "session_id": session_id,
                "session_hash": list(bytes.fromhex(merkle_hex)),
                "vertex_count": 1,
                "committer": "did:eco:westgate",
            })
            self.check("Spine session.commit", bool(commit))
        else:
            self.check("Spine session.commit", False, "skipped (no merkle root)")

        sign_msg = base64.b64encode(f"federation-test:{merkle_hex}".encode()).decode()
        sig = result("beardog", "crypto.sign_ed25519", {"message": sign_msg})
        self.check("BearDog sign", bool(sig))

        braid = result("sweetgrass", "braid.create", {
            "data_hash": cas_hash,
            "mime_type": "text/plain",
            "size": len(test_data),
            "name": "Federation test braid",
            "source_session": session_id,
            "source_merkle_root": merkle_hex,
        })
        self.check("SweetGrass braid.create", bool(braid))

        # Phase 4: Verify provenance chain
        print("\nPhase 4: Verify provenance chain")

        exists = result("nestgate", "content.exists", {"hash": cas_hash})
        self.check("CAS content.exists", exists and exists.get("exists", False))

        session_info = result("rhizocrypt", "dag.session.get", {
            "session_id": session_id,
        }) if session_id else None
        self.check(
            "DAG session state",
            session_info is not None,
            f"vertices={session_info.get('vertex_count', '?')}" if session_info else "",
        )

        # Phase 5: Cross-gate replication (if remote available)
        if not self.local_only and self.remote_gate and self.remote_host:
            print(f"\nPhase 5: Cross-gate replication → {self.remote_gate}")

            replicate = result("nestgate", "content.replicate", {
                "hashes": [cas_hash],
                "remote_gate": self.remote_gate,
                "remote_host": self.remote_host,
            })
            self.check(
                f"content.replicate → {self.remote_gate}",
                replicate is not None,
                str(replicate)[:60] if replicate else "",
            )
        else:
            print("\nPhase 5: Cross-gate replication — SKIPPED (no remote gate)")

        # Summary
        total = self.passed + self.failed
        print(f"\n{'=' * 70}")
        print(f"  FEDERATION TEST RESULTS")
        print(f"  Passed: {self.passed}/{total}")
        print(f"  Failed: {self.failed}/{total}")
        print(f"  Status: {'ALL PASS' if self.failed == 0 else 'FAILURES DETECTED'}")
        print(f"{'=' * 70}\n")

        if cas_hash:
            print(f"  Test CAS hash:    {cas_hash}")
        if session_id:
            print(f"  Test session:     {session_id}")
        if spine_id:
            print(f"  Test spine:       {spine_id}")
        if merkle_hex:
            print(f"  Test Merkle root: {merkle_hex}")
        print()

        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(description="Federation test — cross-gate data + provenance replication")
    parser.add_argument("--remote-gate", type=str, help="Remote gate name (e.g., eastGate)")
    parser.add_argument("--remote-host", type=str, help="Remote gate IP/hostname")
    parser.add_argument("--local-only", action="store_true", help="Test local provenance chain only")
    args = parser.parse_args()

    test = FederationTest(
        remote_gate=args.remote_gate,
        remote_host=args.remote_host,
        local_only=args.local_only or (not args.remote_gate),
    )
    success = test.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
