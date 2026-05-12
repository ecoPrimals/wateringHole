# loamSpine v0.9.16 — Tower Signing + Deep Debt Cleanup

**Date**: April 28, 2026  
**From**: loamSpine v0.9.16  
**Responding to**: primalSpring v0.9.20 Phase 55 — NUCLEUS Two-Tier Crypto Model

---

## What Changed

### Tower-Signed Ledger Entries (IMPLEMENTED)

`entry.append` and `session.commit` now sign entries via BearDog `crypto.sign_ed25519` when `BEARDOG_SOCKET` is set.

- **Signing flow**: Entry canonical bytes are signed before append. The base64 Ed25519 signature and algorithm are stored in entry metadata (`tower_signature`, `tower_signature_alg`). The chain hash computed by `Spine::append` commits to the signed entry.
- **Verification pattern**: Strip `tower_signature` + `tower_signature_alg` from metadata, recompute `to_canonical_bytes()`, verify against the stored signature via `crypto.verify_ed25519`.
- **Standalone mode**: When `BEARDOG_SOCKET` is not set, entries are unsigned — backward compatible.
- **Binary**: `loamspine-service` reads `BEARDOG_SOCKET` at startup and logs whether Tower signing is enabled.
- **Core API**: New `prepare_entry()` + `append_prepared_entry()` methods on `LoamSpineService` enable signing between entry creation and chain append.
- **Wire method**: `crypto.sign_ed25519` (per `CRYPTO_WIRE_CONTRACT.md`), not `crypto.sign`. Base64 standard encoding.

### BTSP Tunnel Consumption (DOCUMENTED)

Per NUCLEUS Two-Tier Crypto Model: "no primal actively establishes persistent BTSP tunnels — this is the next evolution frontier." loamSpine declares BTSP consumed and completes the 4-step handshake but does not use tunnels for encrypted ledger replication. No other primal does either.

### Deep Debt Audit (CLEAN)

10-dimension audit performed April 28, 2026:

| Dimension | Result |
|-----------|--------|
| TODOs/FIXMEs/HACKs | None in production |
| Unsafe code | `#![forbid(unsafe_code)]` on all crates |
| Mocks in production | None — all `#[cfg(test)]` gated |
| `println!`/`eprintln!` in production | None |
| `unwrap()`/`expect()` in production | None |
| Large files (>800L) | **Refactored** — max now 783L |
| `#[allow]` → `#[expect]` | All justified with documented reasons |
| Hardcoded primal names | Only `BEARDOG_SOCKET` + `biomeos` paths (NUCLEUS convention) |
| `cargo deny` | advisories ok, bans ok, licenses ok, sources ok |
| External dependencies | No native deps (ring is lockfile ghost, blake3 in pure mode) |

### Test File Refactoring

- `service_tests.rs` (872→663L): Tower signing tests extracted to `service_tests_tower_signing.rs` (224L) with shared mock helper
- `tests_protocol_transport.rs` (837→662L): PG-52 trio lifecycle tests extracted to `tests_protocol_trio.rs` (195L)
- New test: `test_unsigned_entry_when_no_tower_signer` (verifies backward compat)

---

## Correction to Phase 55 Handoff

The `PRIMALSPRING_V0920_PHASE55_CRYPTO_COMPOSITION_HANDOFF_APR28_2026.md` states under loamSpine:

> **Gap**: declares BTSP consumed but no active channels; entries not signed

**Correction**: Entries are now signed when `BEARDOG_SOCKET` is set. The "entries not signed" gap is **resolved**. BTSP tunnels remain a documented evolution target (no primal does this yet).

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,509 (all concurrent, zero flaky) |
| Max .rs file | 783L (chaos.rs, test file) |
| Max production file | 605L |
| Clippy | Clean (pedantic + nursery) |
| `cargo fmt` | Clean |
| `cargo deny` | Clean (0 ignored advisories) |
| Unsafe | Forbidden (`#![forbid(unsafe_code)]`) |

---

## Environment Variables

loamSpine consumes these NUCLEUS-standard env vars:

| Variable | Purpose | Status |
|----------|---------|--------|
| `BEARDOG_SOCKET` | Tower crypto delegation (sign entries) | **Consumed** (v0.9.16) |
| `BTSP_PROVIDER_SOCKET` | BTSP handshake provider | Consumed (v0.9.16) |
| `FAMILY_SEED` | BTSP key derivation | Consumed (v0.9.16) |
| `DISCOVERY_SOCKET` | Capability-based resolution | Available; infant discovery uses it |
| `BIOMEOS_SOCKET_DIR` | UDS directory | Consumed for socket paths |

---

## Previous Resolved Items

- **PG-52**: UDS trio lifecycle (create/append/seal) — VERIFIED LIVE (April 27)
- **Provenance receipts**: `CommitSessionResponse` enriched with `spine_id` + `committed_at` (April 27)
- **BTSP 4-step handshake**: Complete (April 24)
- **Bond ledger**: Fully implemented (`bonding.ledger.*`); upstream wire alignment pending with BearDog

---

## What's Next

1. **BTSP encrypted tunnels**: When any primal establishes persistent BTSP tunnels, loamSpine can adopt encrypted ledger replication
2. **Signing capability middleware**: RPC-layer signature verification (v0.10.0 target)
3. **Encrypt-at-rest**: When NestGate evolves native encryption, loamSpine can delegate storage encryption

---

*Ref: `wateringHole/NUCLEUS_TWO_TIER_CRYPTO_MODEL.md` — loamSpine purpose: `ledger`*
