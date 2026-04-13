<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 42: primalSpring Audit Resolution — Ionic Bond Seal, BTSP Metadata, Accept Hardening

**Date**: April 13, 2026
**Primal**: BearDog (cryptographic service provider)
**Scope**: Ionic bond lifecycle completion, BTSP capability metadata, accept hardening

---

## 1. Upstream Audit Items Resolved

### Item 1: BTSP server endpoint (`btsp.server.*`)

**Audit claim**: "Only client-side `btsp.handshake` exists."

**Finding**: Already fully implemented. BearDog exposes 5 server-side methods:
- `btsp.server.create_session` — real (BtspSessionStore)
- `btsp.server.verify` — real (HMAC verify + X25519 + HKDF session keys)
- `btsp.server.export_keys` — real (wrapped key export)
- `btsp.server.negotiate` — real (cipher negotiation on active session)
- `btsp.server.status` — real (store stats)

Legacy aliases: `btsp.session.create`, `btsp.session.verify`, `btsp.session.negotiate`.

Transport-level full 4-step handshake (ClientHello → ServerHello → ChallengeResponse → HandshakeComplete) runs via `perform_server_handshake` before JSON-RPC in production mode.

**Fix applied**: Capability metadata in `capabilities.rs` was missing `server.export_keys`. Fixed:
- `btsp_server` capability bumped to v1.1
- `server.export_keys` added to methods array
- Cost estimate added for `btsp.server.export_keys`

primalSpring's `PRIMAL_GAPS.md` already marks this RESOLVED in the cross-spring blockers table.

### Item 2: Ionic bond runtime (`crypto.ionic_bond`) — propose → accept → seal

**Audit claim**: "Full lifecycle via IPC needs BearDog's wire method."

**Finding**: propose/accept/verify/revoke/list were all implemented with real Ed25519 crypto. Missing: explicit `seal` step.

**Fix applied**: Three changes:

1. **`crypto.ionic_bond.seal` method** — New JSON-RPC method completing the three-step lifecycle:
   - Takes `{bond_id, sealer}` where sealer must be proposer or acceptor
   - Re-verifies both proposer and acceptor Ed25519 signatures
   - Transitions `Active` → `Sealed` only if both sigs pass
   - Rejects: unauthorized sealers, non-Active bonds, expired bonds, tampered signatures
   - `BondState::Sealed` added to the state machine

2. **Accept hardened** — Two defense-in-depth improvements:
   - Proposer Ed25519 signature now verified at `accept` time (previously only at `verify`)
   - Proposal TTL enforced at `accept` — expired proposals rejected before bond creation

3. **Capability metadata updated** — `ionic_bond` capability bumped to v2.0 with `seal` in methods; `discover_capabilities` includes `ionic_bond.seal`; cost estimates and operation dependencies updated.

---

## 2. Bond Lifecycle (Updated)

```
Proposer                          BearDog                          Acceptor
   |                                 |                                |
   |-- crypto.ionic_bond.propose --> |                                |
   |<-- proposal_id + terms -------- |                                |
   |                                 |<-- crypto.ionic_bond.accept -- |
   |                                 |--- bond_id + active_bond ----> |
   |                                 |                                |
   |       (either party seals — re-verifies both signatures)        |
   |                                 |                                |
   |-- crypto.ionic_bond.seal ----> |                                |
   |<-- {sealed: true, bond} ------- |                                |
   |                                 |                                |
   |       (bond is now sealed — enforcement-ready)                   |
```

---

## 3. New Tests

| Test | Validates |
|------|-----------|
| `propose_accept_seal_lifecycle` | Full three-step lifecycle; sealed bond verifies as valid with state "sealed" |
| `seal_rejects_unauthorized_sealer` | Non-party sealer rejected |
| `seal_rejects_revoked_bond` | Only Active bonds can be sealed |
| `seal_detects_tampered_signature` | Tampered acceptor sig → seal fails |
| `sealed_bond_can_be_revoked` | Sealed bonds can still be revoked; verify returns "revoked" |

---

## 4. Method Surface

**100 JSON-RPC methods** (was 99).

New: `crypto.ionic_bond.seal`

---

## 5. Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | 0 warnings |
| `cargo test --workspace` | All passing, 0 failures |

---

## 6. Downstream Alignment Notes

- **primalSpring**: `PRIMAL_GAPS.md` has a stale "High" row for BTSP server endpoints that contradicts the "RESOLVED" status in the cross-spring blockers table. primalSpring should clean this up.
- **primalSpring bonding**: `bonding.propose` / `bonding.status` local methods return stubs ("ionic negotiation runtime pending BearDog crypto signatures"). These should now delegate to BearDog's `crypto.ionic_bond.{propose,accept,seal}` via `capability.call` or direct IPC.
- **healthSpring / hotSpring**: Can now call the full `btsp.server.*` surface (including `export_keys`) and `crypto.ionic_bond.{propose,accept,seal,verify,revoke,list}` for wire-level bond enforcement.
