<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# SweetGrass v0.7.27 — License Evolution, Zero-Copy, API Hardening

**Date**: April 6, 2026
**From**: SweetGrass
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,181 tests, 90.90% region coverage, all checks green

**Supersedes**: `SWEETGRASS_V0727_DEEP_DEBT_EVOLUTION_HANDOFF_MAR31_2026.md` (archived)

---

## Summary

Three-phase deep evolution session addressing primalSpring downstream audit
findings and remaining deep debt. License evolved to AGPL-3.0-or-later per
wateringHole/LICENSING_AND_COPYLEFT.md scyBorg standard. Zero-copy
improvements on hot paths. API hardened with `#[non_exhaustive]` on all
public enums. `deny.toml` tightened against protobuf codegen crates.

---

## Phase 1 — primalSpring Audit Resolution

| Finding | Resolution |
|---------|-----------|
| `cargo deny` fails (time 0.3.44) | Updated to 0.3.47 |
| Clippy unused imports in `tcp_jsonrpc.rs` | Test rewritten, imports removed |
| `.cargo/config.toml` hardcoded `target-dir` | Removed; env-var override pattern |
| `#[allow(cast_precision_loss)]` in `object_memory.rs` | Removed (lint not triggered) |

## Phase 2 — License Evolution

All artifacts evolved from `AGPL-3.0-only` to `AGPL-3.0-or-later` per
wateringHole LICENSING_AND_COPYLEFT.md ("-or-later delegates future version
trust to the FSF"):

| Artifact | Count |
|----------|-------|
| `.rs` SPDX headers | 154 |
| `Cargo.toml` files (workspace + 10 crates + fuzz) | 12 |
| `LICENSE` preamble + section header | 1 |
| `deny.toml` allow-list | 1 |
| `scyborg.rs` `LicenseId` enum variant | renamed `Agpl3Only` → `Agpl3OrLater` |
| Root docs, specs, config, `.cursor/rules` | all updated |

`unsafe_code` promoted from `deny` to `forbid` at workspace level.

## Phase 3 — Zero-Copy & API Hardening

### Zero-Copy Improvements

| Change | Impact |
|--------|--------|
| `traversal.rs` cycle detection: `HashSet<String>` → `HashSet<ContentHash>` | O(1) Arc clone vs heap alloc per node |
| `QueryError::NotFound`: `String` → `ContentHash` | O(1) clone at 3 call sites |
| `ActivityType` derives `Hash`; analyzer keyed by type not string | Eliminates per-vertex `.to_string()` in compression |

### Static Error Variants

| New Variant | Replaces |
|-------------|----------|
| `IntegrationError::MissingTarpcAddress` | 3 × `"Primal has no tarpc address".to_string()` |
| `CompressionError::NoCommittedVertices` | 1 × `"No committed vertices".to_string()` |

### API Hardening

- `#[non_exhaustive]` added to **35+ public enums** across all 10 crates
- Cross-crate match statements updated with forward-compatible wildcard arms
- `deny.toml`: added `tonic-build`, `prost-build`, `quick-protobuf`, `pbjson` to ban list

---

## Current State

```
cargo clippy --all-features --all-targets -- -D warnings   ✓ 0 warnings
cargo fmt --all -- --check                                  ✓ clean
cargo deny check                                            ✓ advisories ok, bans ok, licenses ok, sources ok
cargo doc --all-features --no-deps                          ✓ clean
cargo test --all-features --workspace                       ✓ 1,181 passed, 0 failed
```

| Metric | Value |
|--------|-------|
| Version | v0.7.27 |
| Tests | 1,181 |
| Coverage | 90.90% region (llvm-cov) |
| .rs files | 154 (41,883 LOC) |
| Max file | 734 lines (limit: 1000) |
| Unsafe blocks | 0 (`#![forbid(unsafe_code)]` workspace-level) |
| License | AGPL-3.0-or-later (scyBorg standard) |
| SPDX headers | 154/154 |

---

## Remaining Debt (None Blocking)

- **Coverage gap**: Postgres store tests require Docker runtime; excluded from llvm-cov
- **`sled` backend**: Optional, unmaintained upstream; `skip-tree` in `deny.toml`; redb is primary
- **`testcontainers` dev chain**: Pulls `bollard` → `rustls` → `ring` (C/ASM); dev-only, wrappered in `deny.toml`

---

## Cross-Ecosystem Signals

- **License alignment**: sweetGrass now matches wateringHole AGPL-3.0-or-later standard
- **API stability**: `#[non_exhaustive]` on all public enums means downstream crates need wildcard match arms
- **`LicenseId::Agpl3OrLater`**: Any code referencing `LicenseId::Agpl3Only` needs updating
- **`QueryError::NotFound(ContentHash)`**: Downstream match on `NotFound(String)` needs updating to `NotFound(ContentHash)`
