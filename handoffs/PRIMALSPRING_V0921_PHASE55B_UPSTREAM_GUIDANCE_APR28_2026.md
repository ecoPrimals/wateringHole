# primalSpring v0.9.21 Phase 55b — Upstream Guidance

**Date**: April 28, 2026
**From**: primalSpring (composition validation)
**To**: All primal teams
**Context**: Post-harvest review after absorbing NestGate S48, biomeOS v3.30, Songbird W178, Squirrel AN/AO

---

## What Just Happened

The two-tier crypto architecture (Phase 55) triggered a wave of upstream evolution:

- **NestGate** shipped native encrypt-at-rest and auth bypass — exactly what was asked
- **Squirrel** wired HTTP providers, discovery resolution, and the crypto RPC surface
- **biomeOS** cleaned deep debt (events refactor, JWT hardening, `#[expect(reason)]`)
- **Songbird** migrated 20+ error types to anyhow

Two gaps are now **RESOLVED**: NestGate encrypt-at-rest and Squirrel DISCOVERY_SOCKET.

This document provides focused guidance for the remaining evolution work.

---

## Priority 1: BearDog — Purpose-Key RPC (blocks Squirrel + NestGate end-to-end)

Both Squirrel and NestGate have client stubs ready for purpose-key crypto.
BearDog needs to ship server-side support for these three patterns:

### `secrets.retrieve` with purpose keys

Squirrel calls: `secrets.retrieve("nucleus:{family}:purpose:inference")`
NestGate calls: `secrets.retrieve("nucleus:{family}:purpose:storage")`

BearDog already has `secrets.store` and `secrets.retrieve` in its RPC surface.
The ask is that the key derivation from `nucleus_crypto_bootstrap.sh` can also
happen inside BearDog itself — so primals can request purpose keys without
depending on the bootstrap script having run first.

**Suggested**: when `secrets.retrieve` is called for a key matching
`nucleus:{family}:purpose:{name}` and the key doesn't exist yet, derive it
using HKDF from the family seed + purpose string and store it. Lazy derivation.

### `crypto.encrypt` / `crypto.decrypt` with purpose context

Squirrel has wired `encrypt_with_purpose(data, purpose)` and
`decrypt_with_purpose(envelope, purpose)`. These map to:

```json
{"method":"crypto.encrypt","params":{"data":"<b64>","purpose":"inference","algorithm":"chacha20-poly1305"}}
{"method":"crypto.decrypt","params":{"envelope":{"v":1,"ct":"...","n":"...","alg":"chacha20-poly1305"},"purpose":"inference"}}
```

BearDog already has `chacha20_poly1305_encrypt` / `chacha20_poly1305_decrypt`.
The delta is purpose-key resolution: look up the purpose key from secrets,
use it as the encryption key.

### What this unlocks

Once BearDog ships this:
- Squirrel inference payloads encrypt/decrypt automatically when `FAMILY_ID` is set
- NestGate storage encryption keys resolve via BearDog instead of env var override
- Any primal can encrypt domain data using purpose keys (e.g. rhizoCrypt DAG events)

---

## Priority 2: rhizoCrypt — Tower Crypto Delegation — ALREADY RESOLVED (S52)

> **rhizoCrypt response (S54)**: The signing delegation ask is **already implemented**.
> The hash delegation ask is **architecturally inappropriate** and is declined.

### What's Already Shipped (S52)

rhizoCrypt delegates **vertex signing** to the crypto provider since S52:

- `sign_vertex_if_available()` calls `crypto.sign_ed25519` via capability-discovered
  signing provider on every `dag.event.append` and `dag.event.append_batch`
- Lazy discovery via `tokio::sync::OnceCell` — zero cost in standalone mode
- Graceful degradation when no provider is present
- 5 tests covering signing, caching, and graceful degradation
- Documented in `specs/CRYPTO_MODEL.md` with architecture diagram

This is the **same pattern** loamSpine uses for `entry.append` signing and
sweetGrass uses for `braid.create` signing.

### Why Hash Delegation Is Declined

The ask to delegate BLAKE3 hashing to `crypto.blake3_hash` is declined because:

1. **BLAKE3 is deterministic** — same input → same hash, no key material. Delegation
   adds zero cryptographic value. Anyone can independently verify a BLAKE3 hash.

2. **1000x+ performance regression** — BLAKE3 is on rhizoCrypt's hottest path
   (~80ns local). IPC round-trip over UDS is ~100-500μs. This would destroy
   vertex creation throughput (1.4M/sec → ~2K/sec).

3. **The audit trail is already solved** — S52's vertex signing means the crypto
   provider signs every vertex's canonical bytes (which include the BLAKE3 hash).
   The Ed25519 signature IS the audit trail. Delegating the hash adds nothing.

4. **Neither sibling delegates hashing** — loamSpine delegates `crypto.sign_ed25519`
   (signing, not hashing). sweetGrass delegates `crypto.sign` (signing, not hashing).
   No Nest primal delegates deterministic hashing to the Tower.

5. **`CRYPTO_MODEL.md` explicitly documents this two-tier model**: local hashing for
   data integrity, delegated signing for attestation. This is by design.

### DAG Payload Encryption (Future — Not Urgent)

Encrypting DAG event payloads via `crypto.encrypt` with purpose `"dag"` is a valid
future item, but low priority: rhizoCrypt is ephemeral by design (data discarded by
default). Active sessions are protected by filesystem permissions (UDS) and BTSP
handshake. Dehydrated data goes to permanent storage (NestGate encrypt-at-rest).
Noted in roadmap, not blocking.

---

## Priority 3: sweetGrass — Tower Crypto Delegation

Same pattern as rhizoCrypt. sweetGrass currently hashes braid entries locally.

**Ask**: Delegate to `crypto.blake3_hash` or `crypto.sign` when Tower is available.
This ensures the provenance chain is Tower-auditable.

**Also**: The `anchoring.anchor` operation should delegate signing to
`crypto.sign` (Ed25519 via BearDog) when available, rather than using
local signing. This gives anchors ecosystem-wide trust via BearDog's key
hierarchy.

---

## Priority 4: loamSpine — BTSP Active Channels

**Current**: loamSpine declares BTSP support but doesn't establish active
encrypted channels.

**Ask**: On startup, if `BTSP_PROVIDER_SOCKET` is present, establish a BTSP
session via `btsp.session.create` / `btsp.session.negotiate`. Once established,
spine entries should flow through the encrypted channel.

This is the last Nest primal without active BTSP — rhizoCrypt and sweetGrass
both establish sessions.

---

## Priority 5: ToadStool + barraCuda — Self-Registration via DISCOVERY_SOCKET

Squirrel now resolves capabilities via `DISCOVERY_SOCKET` (Method 2 in
`discover_capability()`). For this to be fully useful, primals need to
self-register at startup.

**Ask for both ToadStool and barraCuda**: At startup:
1. Check for `DISCOVERY_SOCKET` env var
2. If present, send `ipc.register` with capabilities and endpoint
3. If absent, continue in standalone mode (no failure)

```json
{"jsonrpc":"2.0","method":"ipc.register","params":{
  "primal_id":"toadstool",
  "capabilities":["compute.dispatch","compute.capabilities"],
  "endpoint":"unix:///run/user/1000/biomeos/toadstool-{family}.sock"
},"id":1}
```

Currently the composition launcher handles registration on behalf of primals.
Self-registration means primals can join a NUCLEUS dynamically without a
central launcher.

---

## Status Scoreboard

| Primal | Last Handoff | Key Ask | Priority |
|--------|-------------|---------|----------|
| **BearDog** | W72 (signed registration) | Purpose-key RPC (`secrets.retrieve` + `crypto.encrypt`/`decrypt` with purpose) | P1 — blocks end-to-end encryption |
| **rhizoCrypt** | S54 | **RESOLVED** — vertex signing delegated (S52); hash delegation declined (deterministic, 1000x perf cost, no crypto value); DAG encryption roadmapped | P2 → Done |
| **sweetGrass** | v0.7.28 | Tower crypto delegation (hash + anchor signing) | P3 |
| **loamSpine** | v0.9.16 | BTSP active channels at startup | P4 |
| **ToadStool** | Display Phase 2 | `DISCOVERY_SOCKET` self-registration | P5 |
| **barraCuda** | Sprint 46 | `DISCOVERY_SOCKET` self-registration | P5 |
| **NestGate** | S48 | RESOLVED (encrypt-at-rest + auth bypass shipped) | Done |
| **Squirrel** | AN | RESOLVED (HTTP providers + discovery + crypto foundation) | Done |
| **Songbird** | W178 | RESOLVED (anyhow migration, error honesty) | Done |
| **biomeOS** | v3.30 | RESOLVED (deep debt cleanup, JWT hardening) | Done |
| **petalTongue** | Phase 55 | Current (awakening, signing, sensor) | Tracking |
| **coralReef** | Iter 86 | Current (deep debt, smart refactoring) | Tracking |

---

**Reference**: `NUCLEUS_TWO_TIER_CRYPTO_MODEL.md`, `primalSpring/docs/NUCLEUS_IPC_METHOD_MAP.md`
