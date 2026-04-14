<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Deep Debt Smart Refactoring Sprint 3

**Date**: April 8, 2026  
**Primal**: loamSpine  
**Domain**: permanence  
**Version**: 0.9.16  
**Status**: COMPLETE

---

## Summary

Third and final deep debt refactoring sprint for v0.9.16. Focused on test extraction from production files and splitting the last remaining >1000-line file. All work follows the established `#[path]` external test module pattern.

---

## Changes

### 1. `certificate_tests.rs` Split (1,060 → 535 + 525)

The only file exceeding 1,000 lines was split by domain:

| File | Lines | Content |
|------|-------|---------|
| `certificate_tests.rs` | 535 | Core CRUD: mint, transfer, verify, history, provenance proofs |
| `certificate_tests_escrow.rs` | 525 | Escrow, loan expiry auto-return, return edge cases |

Both included via `#[path]` from `service/certificate.rs`.

### 2. Production File Test Extraction (6 files)

Inline `#[cfg(test)] mod tests { ... }` blocks extracted to dedicated `*_tests.rs` files:

| Production File | Before | After (production) | Test File |
|-----------------|--------|---------------------|-----------|
| `service/waypoint.rs` | 627 | 250 | `waypoint_svc_tests.rs` |
| `service/infant_discovery.rs` | 662 | 448 | `infant_discovery_svc_tests.rs` |
| `constants/network.rs` | 585 | 325 | `network_tests.rs` |
| `trio_types.rs` | 591 | 442 | `trio_types_tests.rs` |
| `types.rs` | 568 | 380 | `types_tests.rs` |
| `entry/mod.rs` | 617 | 530 | `entry_tests.rs` (merged with proptests) |

### 3. Documentation Reconciliation

Root docs (README, STATUS, CONTEXT, WHATS_NEXT, CHANGELOG, CONTRIBUTING) updated with canonical metrics. Showcase index updated to include demos 08–10. Specs index updated with `SERVICE_LIFECYCLE.md` and `DEPENDENCY_EVOLUTION.md` entries.

---

## Metrics

| Metric | Before Sprint 3 | After Sprint 3 |
|--------|-----------------|----------------|
| Tests | 1,316 | 1,316 (unchanged) |
| Source files | 152 | 163 (+11 extracted test files) |
| Max file (all) | 1,060 | 916 (tarpc_server_tests.rs) |
| Max production file | 773 | 711 (infant_discovery/mod.rs) |
| Clippy warnings | 0 | 0 |

---

## Verification

- `cargo clippy --all-targets`: 0 warnings
- `cargo test`: 1,316 passed, 0 failed
- All 163 `.rs` files under 1,000 lines
- No dead symlinks, no `.bak`/`.tmp`/`.old` debris
- No TODO/FIXME/HACK in source code

---

## Files Touched

### New Files
- `crates/loam-spine-core/src/service/certificate_tests_escrow.rs`
- `crates/loam-spine-core/src/service/waypoint_svc_tests.rs`
- `crates/loam-spine-core/src/service/infant_discovery_svc_tests.rs`
- `crates/loam-spine-core/src/constants/network_tests.rs`
- `crates/loam-spine-core/src/trio_types_tests.rs`
- `crates/loam-spine-core/src/types_tests.rs`
- `crates/loam-spine-core/src/entry/entry_tests.rs`

### Modified Files
- `crates/loam-spine-core/src/service/certificate.rs` (test module declarations)
- `crates/loam-spine-core/src/service/certificate_tests.rs` (trimmed)
- `crates/loam-spine-core/src/service/waypoint.rs` (test extraction)
- `crates/loam-spine-core/src/service/infant_discovery.rs` (test extraction)
- `crates/loam-spine-core/src/constants/network.rs` (test extraction)
- `crates/loam-spine-core/src/trio_types.rs` (test extraction)
- `crates/loam-spine-core/src/types.rs` (test extraction)
- `crates/loam-spine-core/src/entry/mod.rs` (test extraction + proptest merge)

### Deleted Files
- `crates/loam-spine-core/src/entry/tests.rs` (content merged into `entry_tests.rs`)

---

## Cumulative v0.9.16 Sprint Summary

| Sprint | Focus | Source Files Delta |
|--------|-------|-------------------|
| Sprint 1 (Apr 6–7) | Module evolution (types/, error/, neural_api/ dirs), StorageResultExt, parse helpers | 136 → 148 |
| Sprint 2 (Apr 8) | jsonrpc/ wire/server/dispatch split, capabilities/ dir, mDNS evolution | 148 → 152 |
| Sprint 3 (Apr 8) | Test extraction from 7 production files, certificate_tests split | 152 → 163 |
| GAP-MATRIX-12 (Apr 8) | Domain-based socket naming, BIOMEOS_INSECURE guard | (included in Sprint 3 count) |
| Wire Standard L2/L3 (Apr 8) | capabilities.list reshape, identity.get method | (included in Sprint 2 count) |

**Total v0.9.16**: Tests 1,270 → 1,316, Source files 136 → 163, Max production file 773 → 711.

---

*Reference: `CAPABILITY_WIRE_STANDARD.md`, `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §3*
