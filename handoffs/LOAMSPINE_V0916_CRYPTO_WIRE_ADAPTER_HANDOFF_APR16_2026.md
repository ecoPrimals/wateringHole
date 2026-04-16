<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Crypto Wire Adapter (Provenance Trio Pass)

**Date**: April 16, 2026
**Primal**: loamSpine
**Version**: 0.9.16
**Previous handoff**: `LOAMSPINE_V0916_BOND_PERSISTENCE_SELF_KNOWLEDGE_HANDOFF_APR15_2026.md` (archived)

---

## Summary

Implements the production signing path for the Provenance Trio: a JSON-RPC
`crypto.sign_ed25519` / `crypto.verify_ed25519` adapter that speaks the
canonical wire contract from `CRYPTO_WIRE_CONTRACT.md`. This replaces
`CliSigner` as the production signing mechanism; `CliSigner` remains as a
development fallback.

---

## What Changed

### New: `JsonRpcCryptoSigner` / `JsonRpcCryptoVerifier`

- **File**: `crates/loam-spine-core/src/traits/crypto_provider.rs`
- **Exports**: `loam_spine_core::traits::{JsonRpcCryptoSigner, JsonRpcCryptoVerifier}`
- Implements `Signer` / `Verifier` traits via UDS JSON-RPC (NDJSON framing)
- Wire format: `{ message: base64, key_id?: string }` → `{ signature: base64, algorithm: "ed25519" }`
- Verify wire: `{ message: base64, signature: base64, public_key: base64 }` → `{ valid: bool }`
- Crypto provider discovered at runtime via capability system (no hardcoded names)
- 8 unit tests with mock UDS JSON-RPC server
- `const fn` constructors for both types

### Updated: Niche / Consumed Capabilities

- `SIGNING` dependency description now references `crypto.sign_ed25519` / `crypto.verify_ed25519` wire methods
- Graceful degradation chain: `JsonRpcCryptoSigner` → `CliSigner` → error

---

## Provenance Trio Audit Response

| Audit Item | Status |
|-----------|--------|
| "loamSpine async-trait at zero" | CONFIRMED — native `-> impl Future` throughout; zero `async_trait` crate usage |
| "Bond ledger persistent" | DONE (previous pass) — `bonding.ledger.*` wire contract |
| "rhizoCrypt SigningClient field alignment" | ADDRESSED on loamSpine side — `JsonRpcCryptoSigner` speaks canonical wire format; rhizoCrypt needs its own adapter |
| "sweetGrass Postgres full-path" | N/A — sweetGrass scope |
| "sweetGrass async-trait" | N/A — sweetGrass scope (documented as conscious trade-off) |

---

## Quality Metrics

| Metric | Value |
|--------|-------|
| Tests | **1,442** (all passing) |
| Source files | 187 `.rs` files |
| JSON-RPC methods | 37 |
| Clippy | 0 warnings (pedantic + nursery) |
| `cargo doc` | 0 warnings |
| Unsafe | 0 (`#![forbid(unsafe_code)]`) |
| SPDX headers | All 187 source files |
| Capability Wire Standard | **Full L3** |

---

## Gates (All Green)

```
cargo fmt --all -- --check     ✓
cargo clippy --all-targets     ✓ (0 warnings)
cargo doc --no-deps            ✓ (0 warnings)
cargo test --workspace         ✓ (1,442 passed, 0 failed)
```

---

## Remaining Known Debt

| Area | Status |
|------|--------|
| `BTSP_NULL` cipher only | Phase 3 — awaiting BTSP provider session key propagation |
| PostgreSQL / RocksDB backends | v1.0.0 target |
| `rusqlite` C dep | Feature-gated, not default (`redb` default is pure Rust) |
| `bincode` v1 RUSTSEC | Migration to v2 is storage format breaking change |
| `provider_client` / `crypto_provider` DRY | Same NDJSON-over-UDS pattern — future refactor into shared transport module |

---

*Previous handoffs archived in `handoffs/archive/LOAMSPINE_V0916_*`*
