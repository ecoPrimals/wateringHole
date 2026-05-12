<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.28 — primalSpring Audit Compliance & Deep Debt Evolution

| Field | Value |
|-------|-------|
| **Date** | 2026-04-02 |
| **Primal** | Squirrel (AI Coordination) |
| **From** | Deep debt evolution session |
| **Version** | 0.1.0-alpha.28 |
| **Status** | GREEN — 7,161 tests / 0 failures / 110 ignored / 85.3% coverage / zero clippy / zero rustdoc warnings |

---

## Summary

Comprehensive audit and deep debt resolution session. Started with a full-spectrum
codebase audit (build, lint, fmt, doc, coverage, compliance, patterns, security),
then executed the primalSpring audit recommendation (SQ-04: workspace-level
`unsafe_code = "forbid"`), followed by systematic evolution of all identified gaps.

## primalSpring Audit Resolution

All gaps from the upstream primalSpring audit are now **RESOLVED**:

| Gap | Resolution |
|-----|------------|
| SQ-01 socket | Previously resolved |
| SQ-02 local AI endpoint | Previously resolved |
| SQ-03 feature flag docs | Previously resolved |
| SQ-04 `unsafe_code = "forbid"` | **NEW** — Added to workspace `[lints.rust]`; removed 21+ redundant per-file attributes |

## Changes Made

### Workspace Lint Evolution
- `unsafe_code = "forbid"` added to `[workspace.lints.rust]` in root `Cargo.toml`
- Same added to `adapter-pattern-tests/Cargo.toml` (uses local lints, not workspace inheritance)
- Removed `#![forbid(unsafe_code)]` from 21+ individual files — single source of truth

### Rustdoc Fixes
- Fixed 3 broken `[Error]` intra-doc links in `ecosystem_service.rs`
- `cargo doc --all-features --no-deps` now produces zero warnings

### Hardcoded Value Evolution
- `ecosystem_service.rs` port 8080 → `universal_constants::network::squirrel_primal_port()` (env-aware, default 9010)
- Vestigial `--bind` CLI flag removed (Squirrel is zero-HTTP; Unix socket + localhost TCP only)
- Config `bind` field retained for backward compat but documented as unused

### Production Placeholder Evolution
- `unregister_from_ecosystem()` was empty `const fn` — now calls `manifest_discovery::remove_manifest()`
- `unreachable!` in `testing/mod.rs` → `panic!` with proper `# Panics` docs (assertion helpers)
- `unreachable!` in `presets.rs` → `#[expect]` annotated `expect()` with documented reason

### deny.toml Cleanup
- Removed stale `libsqlite3-sys@0` skip (no longer in dep tree)
- Removed `cc` skip (unnecessary, caused cosmetic warning)
- Documented ecoBin v3 migration paths for ring (sqlx → rustls-rustcrypto) and cc (pprof → samply)
- `cargo deny check` now passes with zero warnings

### Test Coverage
- `cli/status.rs` went from 0% to covered (5 new tests)
- Total: 7,161 passing, 110 ignored, 85.3% line coverage

### Documentation
- README, CONTEXT, CURRENT_STATUS, CONTRIBUTING all updated with accurate metrics
- CONTRIBUTING.md license fixed: AGPL-3.0-only → AGPL-3.0-or-later (matches SPDX headers)
- CHANGELOG entry for alpha.28

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests passing | 7,156 | 7,161 |
| Clippy warnings | 0 | 0 |
| Rustdoc warnings | 3 | 0 |
| `cargo deny` warnings | 2 | 0 |
| Workspace unsafe_code lint | missing | `"forbid"` |
| Per-file `#![forbid]` attrs | 30+ | 0 (workspace covers all) |
| `cli/status.rs` coverage | 0% | covered |
| Hardcoded port 8080 | 1 site | 0 |
| CLI `--bind` flag | present (vestigial) | removed |
| Production placeholders | 1 (`unregister`) | 0 |
| License inconsistency | CONTRIBUTING had "only" | Fixed to "or-later" |

## Remaining Work (Future Sessions)

- **Coverage lift** — 85.3% → 90% target. Low files: `plugins/security.rs` (56%), `rule-system/evaluator.rs` (71%), `rule-system/manager.rs` (69%)
- **110 ignored tests** — audit and either fix or document
- **ecoBin v3 C elimination** — ring via sqlx/rustls needs `rustls-rustcrypto` migration
- **Clone audit** — ~1,500+ `.clone()` calls; review top-10 production files for unnecessary clones
- **SDK MCP operations** — placeholder implementations need real server I/O
- **Compute providers** — `create_compute_from_type` returns NotAvailable for all types

## Quality Gates

```
cargo fmt --all -- --check         ✅ PASS
cargo clippy --all-features -- -D warnings  ✅ PASS (0 warnings)
cargo doc --all-features --no-deps ✅ PASS (0 warnings)
cargo test --all-features          ✅ PASS (7,161 / 0 / 110)
cargo deny check                   ✅ PASS (0 warnings)
cargo llvm-cov                     85.3% line coverage
```
