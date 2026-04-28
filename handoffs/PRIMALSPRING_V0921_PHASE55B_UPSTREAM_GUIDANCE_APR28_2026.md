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

## Priority 2: rhizoCrypt — Tower Crypto Delegation

**Current**: rhizoCrypt hashes DAG events locally (BLAKE3 in-process).

**Ask**: When operating within a NUCLEUS composition (detected by `BEARDOG_SOCKET`
or `BTSP_PROVIDER_SOCKET` presence), delegate hashing to the Tower via
`crypto.blake3_hash` or `crypto.sign`. This gives the Tower a complete audit
trail of all content-addressed operations.

**Pattern**:
```
if BEARDOG_SOCKET is set:
    hash = rpc_call(beardog, "crypto.blake3_hash", {data: ...})
else:
    hash = local_blake3(data)  // standalone fallback
```

This is the same capability-first pattern Squirrel uses for discovery resolution:
try Tower, fall through to local.

**Also**: Consider encrypting DAG event payloads using `crypto.encrypt` with
purpose `"dag"` when a FAMILY_ID is present.

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
| **rhizoCrypt** | S53 | Tower crypto delegation (hash + optional encrypt) | P2 |
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
