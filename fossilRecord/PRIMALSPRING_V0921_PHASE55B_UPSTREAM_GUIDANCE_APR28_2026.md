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

## ~~Priority 2: rhizoCrypt — Tower Crypto Delegation~~ RESOLVED

rhizoCrypt S52 already ships vertex signing delegation to `crypto.sign_ed25519`
on every `dag.event.append` — the same pattern loamSpine and sweetGrass use.

The original ask to delegate BLAKE3 hash computation was **incorrect** and has
been withdrawn. BLAKE3 is deterministic and keyless — delegation adds zero
cryptographic value while imposing a 1000x+ latency penalty on the hot path
(~80ns local vs ~100-500us IPC). The Ed25519 vertex signature already covers
the canonical bytes including the hash.

**Correct model**: Local hashing for data integrity, delegated signing for
attestation. All three Nest primals now implement this identically.

DAG payload encryption (`crypto.encrypt` with purpose `"dag"`) is accepted as
a low-priority future item by the rhizoCrypt team.

---

## ~~Priority 3: sweetGrass — Tower Crypto Delegation~~ RESOLVED

sweetGrass v0.7.28 shipped braid signing delegation (`braid.create` → BearDog
`crypto.sign` Ed25519 via `CryptoDelegate` module) and anchor signing delegation
(`anchoring.anchor`). Tower-level `Witness::from_tower_ed25519` witnesses with
`tier: "tower"` and `did:key:z6Mk...` agent DID. Graceful degradation to unsigned.
Also eliminated `hostname` crate for pure Rust. 1,462 tests.

---

## ~~Priority 4: loamSpine — BTSP Active Channels + Signing Delegation~~ RESOLVED

loamSpine shipped Tower-signed ledger entries (Apr 28): `entry.append` and
`session.commit` sign via BearDog `crypto.sign_ed25519` with `tower_signature`
in entry metadata. `prepare_entry()` + `append_prepared_entry()` split for signing
between creation and chain append. BTSP tunnel consumption documented as next
frontier (no primal actively uses tunnels yet). 1,509 tests.

---

## ~~Priority 5: ToadStool + barraCuda — Self-Registration via DISCOVERY_SOCKET~~ RESOLVED

Both primals now self-register at startup:
- **barraCuda Sprint 47**: `register_with_discovery()` with 11 capability tags
- **ToadStool S207**: `register_with_discovery()` with `["compute.dispatch","compute.capabilities"]`

ToadStool also shipped encrypted compute dispatch (S205): purpose-key retrieval
via BearDog `secrets.retrieve`, payload encrypt/decrypt via `crypto.encrypt`/`crypto.decrypt`.
Deep debt clean across S206-S208 (lint evolution, dep unification, stale features removed,
`expect`→`Result`, 49 unsafe blocks SAFETY-documented). 7,842 tests.

---

## Status Scoreboard

| Primal | Last Handoff | Key Ask | Priority |
|--------|-------------|---------|----------|
| **BearDog** | W74 | **RESOLVED** — lazy purpose-key derivation + purpose encrypt/decrypt | Done |
| **rhizoCrypt** | S54 | **RESOLVED** — signing delegation shipped (S52), hash delegation withdrawn | Done |
| **sweetGrass** | v0.7.28 | **RESOLVED** — braid + anchor signing delegation shipped | Done |
| **loamSpine** | v0.9.16 (Apr 28) | **RESOLVED** — Tower-signed entries via `crypto.sign_ed25519` | Done |
| **ToadStool** | S205–S208 | **RESOLVED** — encrypted dispatch + self-registration + deep debt | Done |
| **barraCuda** | Sprint 47 | **RESOLVED** — Songbird self-registration shipped | Done |
| **NestGate** | S48 | **RESOLVED** (encrypt-at-rest + auth bypass shipped) | Done |
| **Squirrel** | AN | **RESOLVED** (HTTP providers + discovery + crypto foundation) | Done |
| **Songbird** | W178 | **RESOLVED** (anyhow migration, error honesty) | Done |
| **biomeOS** | v3.30 | **RESOLVED** (deep debt cleanup, JWT hardening) | Done |
| **petalTongue** | Phase 55 | Current (awakening, signing, sensor) | Tracking |
| **coralReef** | Iter 86 | Current (deep debt, smart refactoring) | Tracking |

---

**Reference**: `NUCLEUS_TWO_TIER_CRYPTO_MODEL.md`, `primalSpring/docs/NUCLEUS_IPC_METHOD_MAP.md`
