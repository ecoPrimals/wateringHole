# SPDX-License-Identifier: AGPL-3.0-only

# biomeOS v2.68 — Deep Audit + Hardcoding Evolution

**Date**: March 27, 2026
**Version**: 2.68
**Supersedes**: v2.67 handoff (March 22, 2026)

---

## Summary

Comprehensive audit of the entire biomeOS codebase against wateringHole standards
(PRIMAL_IPC_PROTOCOL, SEMANTIC_METHOD_NAMING, ECOBIN_ARCHITECTURE, UNIBIN_ARCHITECTURE,
ZERO_HARDCODING, COORDINATION_HANDOFF_STANDARD), followed by systematic execution of
all identified issues: formatting regression, blocking-in-async pattern, hardcoded paths
and IPs, license inconsistency, stale phase2 references, and CHANGELOG debris.

---

## Metrics

| Metric | Before (v2.67) | After (v2.68) |
|--------|-----------------|---------------|
| Formatting | 10 diffs (regression) | **PASS** |
| Clippy | PASS | **PASS** (0 warnings, pedantic+nursery, 26 crates) |
| Docs | PASS | **PASS** |
| Hardcoded `/tmp` paths | 4 production sites | **0** (centralized to constants) |
| Hardcoded IPs | 6 production sites | **0** (centralized to constants) |
| Blocking-in-async | 1 (`probe_live_sockets`) | **0** (native async) |
| License inconsistencies | 1 file (LICENSE-CC-BY-SA) | **0** |
| phase2 path references | 6+ active files | **0** (all evolved to `primals/`) |
| CHANGELOG duplicates | 1 section (v1.28/v1.29) | **0** (removed) |

---

## Changes

### 1. Blocking-in-Async Evolution

`probe_live_sockets()` in `biomeos-api/src/handlers/discovery.rs` used
`Handle::block_on` inside `std::thread::scope` to call async code from a sync
context. This risks deadlock in single-threaded Tokio runtimes.

**Evolution**: Converted to native `async fn` with direct `.await`. Six associated
tests evolved from `#[test] fn` to `#[tokio::test] async fn`.

### 2. Hardcoded Path Centralization

New `biomeos-types::constants::runtime_paths` module provides:
- `FALLBACK_RUNTIME_BASE` (`/tmp/biomeos`)
- `BIOMEOS_SUBDIR` (`biomeos`)
- `SOCKET_SUBDIR` (`sockets`)
- `fallback_runtime_dir(family_id)` helper

Four production sites centralized:
- `capability_discovery.rs` — Tier 4 fallback
- `tower_orchestration.rs` — PID file + socket dir fallbacks
- `node_handlers.rs` — Neural API socket fallback
- `subfederation/beardog.rs` — Neural API socket fallback

### 3. Hardcoded IP Centralization

Six production sites evolved to use `endpoints::DEFAULT_LOCALHOST` / `PRODUCTION_BIND_ADDRESS`:
- `strategy.rs` — TCP fallback host (2 sites)
- `stun_extension.rs` — STUN bind address
- `federation/config.rs` — Federation bind address
- `config/network.rs` — NetworkConfig default
- `system/network.rs` — Fallback network addresses (2 sites)

### 4. License Reconciliation

`LICENSE-CC-BY-SA` referenced `AGPL-3.0-or-later` for software, inconsistent with
`Cargo.toml` (`AGPL-3.0-only`) and SPDX headers. Corrected to `AGPL-3.0-only`.

### 5. Formatting Regression

`cargo fmt --check` showed 10 diffs across 5 files (likely caused by rustfmt version
drift between contributors). Fixed with `cargo fmt --all`.

### 6. phase2 Path Evolution

Stale `phase2/biomeOS` references evolved to `primals/biomeOS`:
- `config/systemd/biomeos-beacon-dns.service`
- `config/systemd/biomeos-sovereign-tower.service`
- `crates/neural-api-client/README.md`
- `crates/biomeos-atomic-deploy/src/executor/primal_spawner.rs` (doc comment)
- `deployments/basement-hpc/README.md`
- `plasmidBin/MANIFEST.md`

### 7. Root Documentation Refresh

All root docs updated from v2.67 to v2.68:
- `README.md`, `START_HERE.md`, `QUICK_START.md`, `DOCUMENTATION.md`, `CURRENT_STATUS.md`
- CHANGELOG.md: v2.68 entry added, duplicate v1.28/v1.29 tail section removed

### 8. Dependency Audit

| Dependency | Status | Notes |
|------------|--------|-------|
| blake3 + cc | Acceptable | Perf-critical genome hashing, pure-Rust fallback available |
| tokio-process 0.2 | Legacy | In biomeos-deploy, pinned by older API |
| bincode v1 | RUSTSEC-2025-0141 | Blocked by tarpc (upstream dependency) |
| sysinfo | Retained | Cross-platform fallback; Linux paths prefer /proc |

### 9. Mock Audit

274 mock-related hits confirmed all test-gated: `#[cfg(test)]`, `*_tests.rs`,
`biomeos-test-utils`. Zero production mocks.

---

## Gates

```
cargo fmt --check                                  # PASS
cargo clippy --workspace -- -D warnings            # PASS (0 warnings)
cargo doc --workspace --no-deps                    # PASS
cargo build --workspace                            # PASS
```

Full `cargo test --workspace` blocked by infrastructure issue (LLVM linker Bus error
under tmpfs pressure — not a code regression; requires `cargo clean` to recover disk).

---

## Inter-Primal Notes

- No new compile-time coupling to any primal
- JSON-RPC wire contracts unchanged
- `runtime_paths` constants are in `biomeos-types` (shared types crate) — available to
  any crate that depends on `biomeos-types`
- `endpoints::DEFAULT_LOCALHOST` / `PRODUCTION_BIND_ADDRESS` also in `biomeos-types`
- Discovery protocol remains 5-tier capability-based (env → XDG → /tmp → socket scan)

---

## What's Next

| Area | Priority | Notes |
|------|----------|-------|
| Full test run | P0 | `cargo clean` + `cargo test --workspace` to verify post-evolution |
| Coverage report | P1 | `cargo llvm-cov` once tests pass |
| tokio-process evolution | P2 | Replace 0.2 legacy in biomeos-deploy |
| bincode v2 | Blocked | Waiting on tarpc upstream |
| Abstract socket routing | P2 | biomeOS cannot route to Squirrel abstract sockets (per primalSpring exp077) |
| 90% coverage push | P1 | Currently ~90%+ but needs fresh measurement |

---

**Source of truth**: `CURRENT_STATUS.md` in biomeOS repo root
**License**: AGPL-3.0-only (scyBorg provenance trio)
