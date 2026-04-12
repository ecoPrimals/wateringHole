# BearDog v0.9.0 — Wave 36: Composition Elevation Sprint — Ionic Bond Lifecycle, BTSP Naming, Smart Refactoring

| Field | Value |
|-------|-------|
| Date | 2026-04-12 |
| From | BearDog v0.9.0 (composition elevation session) |
| To | primalSpring, all downstream primals |
| License | AGPL-3.0-or-later |
| Supersedes | BEARDOG_V090_WAVE35_DEEP_DEBT_CLEANUP_HANDOFF_APR11_2026 |

---

## 1. What Happened

Composition elevation sprint targeting primalSpring downstream audit findings:
ionic bond lifecycle hardening, BTSP naming alignment, production mock elimination,
wildcard import cleanup, smart refactoring of three 800+ LOC files, and PKCS#11
discovery evolution.

**All four quality gates pass clean.** 14,769+ tests, 0 failures.

---

## 2. Ionic Bond Lifecycle Hardened

| Change | Detail |
|--------|--------|
| `IonicBond` type gains `terms_hash` field | SHA-256 hex of canonical bond terms, stored at seal time |
| `crypto.ionic_bond.verify` now re-verifies Ed25519 | Both proposer and acceptor signatures validated against stored `terms_hash` |
| 4 new lifecycle tests | `sealed_bond_stores_terms_hash`, `verify_detects_tampered_proposer_signature`, `verify_detects_tampered_acceptor_signature`, `full_lifecycle_propose_accept_list_revoke` |
| `crypto.ionic_bond.list` added to cost_estimates | Was advertised but missing from capabilities cost block |

**For other primals**: If you consume `IonicBond` via JSON deserialization, the new
`terms_hash` field will appear in the bond payload. It is non-optional (`String`).
If you deserialize with `#[serde(deny_unknown_fields)]`, add the field to your types.

---

## 3. BTSP Naming Alignment

| Was | Now |
|-----|-----|
| Doc comments said `btsp.session.create` | Canonical `btsp.server.create_session` (handler aliases preserved) |
| Doc comments said `btsp.session.verify` | Canonical `btsp.server.verify` |
| Doc comments said `btsp.session.negotiate` | Canonical `btsp.server.negotiate` |

Legacy `btsp.session.*` method names still route correctly at runtime for backward
compatibility. No wire-level breaking change.

---

## 4. Production Mocks Eliminated (2 sites)

| File | Was | Now |
|------|-----|-----|
| `beardog-monitoring/service.rs` `collect_performance_metrics` | Hardcoded (25% CPU, 60% memory, 8GB total, 1 day uptime) | Real `/proc/stat` CPU, `/proc/meminfo` memory+total+used, `start_time.elapsed()` uptime; graceful zeros on non-Linux |
| `beardog-types/production/monitoring.rs` `PerformanceMonitor` | `Default::default()` regardless of state | Returns most recent recorded metric from history; `initialize()` clears stale history |

---

## 5. Wildcard Imports Eliminated (Production Code)

11+ files in `beardog-tunnel/universal_hsm_discovery/` switched from `use super::super::*`
to explicit imports. `simplified_seed_tunnel.rs` removed unused `use beardog_types::canonical::*`.
`beardog-types/providers/base/defaults.rs` replaced `configuration::*`, `performance::*`,
`schema::*` with ~30 explicit type imports.

---

## 6. Smart Refactoring (3 Large Files)

| File | Before | After | Strategy |
|------|--------|-------|----------|
| `port_discovery.rs` | 940 LOC | `config.rs` + `env.rs` + `discoverer.rs` + `hierarchical.rs` + `mod.rs` | Config/env/algorithm/chain separation |
| `btsp.rs` | 855 LOC | `contact.rs` + `session.rs` + `negotiation.rs` + `peer.rs` + `tunnel.rs` + `mod.rs` | JSON-RPC method group separation |
| `tarpc_server/server.rs` | 811 LOC | 9 domain modules + `mod.rs` | Crypto domain (keygen, signatures, key_exchange, aead, hashing, kdf, genetic, tls, introspection) |

All public APIs preserved via `pub use` re-exports. Zero breaking changes.

---

## 7. PKCS#11 Discovery Evolution

`discover_pkcs11_libraries()` in `beardog-config/domains/paths.rs` now checks
`BEARDOG_PKCS11_SEARCH_PATHS` (colon-separated) before falling back to
platform-default search paths.

---

## 8. Quality Gate Results

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-features -- -D warnings` | 0 warnings |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | 0 warnings |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace` | 14,769+ passed, 0 failed |

---

## 9. Metrics Snapshot

| Metric | Value |
|--------|-------|
| Version | 0.9.0 |
| Crates | 29 |
| Rust files | 2,089 |
| Tests | 14,769+ |
| Coverage | 90.51% (llvm-cov) |
| JSON-RPC methods | 95 |
| `unsafe` blocks | 0 (`forbid(unsafe_code)` workspace-wide) |
| C dependencies | 0 |
| TODO/FIXME/HACK | 0 |
| Files > 1000 LOC | 0 |

---

## 10. Remaining Known Debt (Hardware/Platform Dependent)

These items cannot be resolved without physical hardware or external services:

- **Android StrongBox/Keystore** — JNI integration requires Android device
- **iOS Secure Enclave** — Requires iOS build target
- **FIDO2 CTAP2** — Requires physical security key
- **PKCS#11 HSM** — Requires HSM hardware
- **BTSP Phase 3 HSM signing** — Documented upgrade path; software derivation is production-safe
- **Bond persistence** — NestGate owns `bonding.ledger.*` per PORTABILITY_DEBT_AND_NODE_DELEGATION

---

## 11. Addressed primalSpring Audit Items

| Audit Item | Resolution |
|------------|------------|
| Ionic bond runtime: propose→accept→seal e2e | Ed25519-signed full lifecycle with cryptographic verify |
| btsp.negotiate vs btsp.session.negotiate inconsistency | Docs aligned to `btsp.server.*`; legacy aliases preserved |
| HSM/BTSP Phase 3 signing path | Documented; software path production-safe (low priority) |
| Bond persistence (NestGate integration) | NestGate owns `bonding.ledger.*`; BearDog provides crypto enforcement |
