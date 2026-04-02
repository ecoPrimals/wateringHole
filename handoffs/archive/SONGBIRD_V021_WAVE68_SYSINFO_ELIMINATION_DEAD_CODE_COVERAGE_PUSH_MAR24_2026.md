<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2024-2026 ecoPrimals -->

# Songbird v0.2.1-wave68 — sysinfo Elimination, Dead Code Removal, Coverage Push

**Date**: March 24, 2026
**From**: Songbird session 15
**Primal**: Songbird (Network Orchestration & Discovery)
**Version**: v0.2.1-wave68
**Status**: All quality gates passing
**License**: AGPL-3.0-only (scyBorg triple)
**Supersedes**: SONGBIRD_V021_WAVE66_COMPREHENSIVE_AUDIT_CARGO_DENY_CI_COVERAGE_MAR23_2026

---

## Summary

Eliminated `sysinfo` dependency (ecoBin v3.0 compliance) — replaced with pure Rust
`sys_metrics` module reading `/proc/meminfo` and `/sys/block/*/size` directly. Removed
~48KB of dead code across 3 crate directories. Added 121 new tests across 8 modules.
Cleaned stale references and updated all root documentation.

## Quality Gate Table

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets --all-features -- -D warnings` | PASS (pedantic + nursery) |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | PASS |
| `cargo deny check` | PASS (advisories ok, bans ok, licenses ok, sources ok) |
| `cargo test --all-features --workspace` | 10,233 passed, 0 failed, 266 ignored |
| Coverage (llvm-cov) | 66.59% (target 90%) |
| Files >1000 lines | 0 (max 959 test, 578 production) |

## Changes

### sysinfo Elimination (ecoBin v3.0)
- Created `songbird_types::sys_metrics` — pure Rust `/proc` + `/sys` readers
- Memory: reads `/proc/meminfo` for `MemTotal`, `MemAvailable` (zero deps)
- Disk: reads `/sys/block/*/size` for physical block device capacity (zero deps)
- Replaced all `sysinfo` usage in songbird-orchestrator (5 sites), songbird-cli (2 sites), songbird-registry (1 site)
- Eliminated `sysinfo` + `rayon` + `crossbeam-*` from production dependency tree
- `#![forbid(unsafe_code)]` maintained — no syscalls needed

### Dead Code Removal (~48KB)
- `songbird-observability/src/monitoring/` — 4 files with broken syntax and deprecated sysinfo 0.29 API
- `songbird-registry/src/health/` — broken syntax, not wired into module tree
- `songbird-registry/src/scaling/` — broken syntax, not wired into module tree
- `songbird-universal-ipc/data/sovereign-onion/blobs/` — empty artifact directory

### Coverage Expansion (+121 tests)
- Circuit breaker: 13 new tests (state machine transitions, config validation)
- Connection pool: 17 new tests (lifecycle, concurrency, stale eviction)
- Consent enforcement: 12 new tests (dignity rules, timeout behavior, cost thresholds)
- Primal self-knowledge: 12 new tests (env discovery, error paths, mechanism names)
- Observability metrics: 24 new tests (collection, prometheus export, caching)
- TLS key schedule: 13 new tests (HKDF extract/expand, full schedule flow)
- Beardog birdsong provider: 13 new tests (mock TCP JSON-RPC, encrypt/decrypt roundtrip)
- Lineage beardog relay: 17 new tests (mock JSON-RPC, masking, fail-closed paths)

### Production Mock Audit
- All `Mock*` types confirmed isolated to `#[cfg(test)]` modules
- Zero production mocks found

## Inter-Primal Notes

### For BearDog
- `sys_metrics` module is self-contained — no BearDog crypto needed for system metrics
- BearDog crypto delegation paths unchanged

### For All Primals
- `sysinfo` crate removal is a template for other primals still using it
- Pattern: read `/proc/meminfo` directly, read `/sys/block/*/size` for disk
- Available as `songbird_types::sys_metrics` if shared via workspace dependency

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 10,100 | 10,233 |
| Dependencies (unique) | ~418 | ~412 |
| Dead code removed | — | ~48KB (6 files, 3 directories) |
| `sysinfo` in dep tree | Yes | No |
| Rust lines | ~407,242 | ~391,757 |

## Remaining Priority

1. **Coverage expansion** — 66.59% → 90% (pure logic modules, then integration)
2. **BearDog crypto wiring** — unblocks Tor circuit + onion encryption
3. **Ring-free workspace** — `rcgen` replacement + quinn feature reconfiguration
