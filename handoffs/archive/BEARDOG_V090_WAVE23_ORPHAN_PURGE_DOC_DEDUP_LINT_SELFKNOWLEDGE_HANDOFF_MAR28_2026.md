# BearDog v0.9.0 — Wave 23: Massive Orphan Purge, Doc Dedup, Lint Tightening & Self-Knowledge

**Date**: March 28, 2026
**Primal**: BearDog
**Version**: 0.9.0
**Coverage**: 90.16% line | 89.32% region | 84.94% function
**Tests**: 15,100+ passing, 0 failures

---

## Context

Continued systematic codebase evolution after Wave 22's hot-path fixes and iOS stub corrections. This wave focused on dead code elimination at scale, documentation quality, workspace lint evolution, dependency compliance audit, and self-knowledge constant centralization.

---

## What Changed

### 36 Orphan .rs Files Removed (~8,500+ LOC)

Systematic module-tree audit using `mod` declaration and `#[path]` attribute verification confirmed 36 files across 14 crates were never compiled — not referenced from any module tree. All archived to git history.

| Crate | Files Removed | LOC |
|-------|--------------|-----|
| beardog-core | 9 | ~3,300 |
| beardog-errors | 8 | ~2,264 |
| beardog-monitoring | 4 | ~1,238 |
| beardog-security | 3 | ~989 |
| beardog-types | 5 | ~804 |
| beardog-utils | 3 | ~773 |
| beardog-production | 1 | 234 |
| beardog-cli | 1 | 402 |
| beardog-config | 1 | 268 |
| beardog-integration-tests | 1 | 763 |

5 files initially flagged as orphans were confirmed wired via `#[path = "..."]` and retained.

### 858 Duplicated Doc Comment Lines Deduplicated

Automated scan across 196 files found consecutive identical `///` lines — a pervasive copy-paste artifact inflating doc output. All 858 duplicates removed.

### Workspace Lint Evolution

- `clippy::empty_docs` promoted from `allow` to `warn` — empty `///` comments provide no value
- 3 empty doc comments in `beardog-types/production/monitoring.rs` replaced with real descriptions
- Doc lint section header updated from "kept allow" to "promoted incrementally"

### Self-Knowledge Constants: `"beardog"` → `DEFAULT_SYSTEM_NAME`

7 production fallback sites hardcoding `"beardog"` as a string literal now reference `beardog_types::constants::domains::config::system::DEFAULT_SYSTEM_NAME`:

- `beardog-tunnel/src/platform/mod.rs`: 4 platform endpoint defaults (Android, Unix, Windows, WASM)
- `beardog-production/src/config_management/runtime.rs`: 3 defaults (app name, DB name, DB user)

### Empty Placeholder Modules Evolved

5 stub files containing only `// Placeholder for X` comments replaced with proper module-level `//!` documentation:

- `beardog-config/{discovery,validation,defaults}.rs`
- `beardog-traits/unified/{storage,network}.rs`

### Dependency Compliance Audit

| Dependency | ecoBin Status | Notes |
|-----------|---------------|-------|
| `serde_yaml` | Compliant (Rust-compiled, no C linker) | `unsafe-libyaml` is C→Rust translation; deprecated upstream, `yaml_serde` documented as successor |
| `hostname` | Compliant | Uses `libc` (standard OS FFI) |
| `bcrypt` | Compliant | Uses RustCrypto `blowfish` (pure Rust) |
| `pprof` | C-heavy | Already behind optional `profiling` feature |
| `mockall` | Pure Rust | Not in lockfile (unused) |
| `wiremock` | Pure Rust | Test-only |

`serde_yaml` deprecation documented in workspace `Cargo.toml` with migration note.

### Root Docs & Debris Cleanup

- Coverage metrics updated 90.05% → 90.16% across README.md, CONTEXT.md, ROADMAP.md, ARCHITECTURE.md, STATUS.md, specs/PROJECT_STATUS.md
- 6 shell scripts archived to `fossilRecord/beardog/scripts/` (security_audit.sh, security_hardening_validation.sh, validate-system.sh, birdsong_privacy_test.sh, beardog-local-showcase.sh, validate-local-primal.sh)
- 7 stale planning/spec docs archived to `fossilRecord/beardog/docs-historical/specs-mar2026/` (BEARDOG_BINARY_PATTERN_ANALYSIS.md, BEARDOG_ECOSYSTEM_EVOLUTION_PLAN.md, otherTeams/*, showcase planning docs)
- `specs/experiments/` directory (10 files, Sep-Dec 2025 experimental validation) archived
- Untracked debris removed: 3 `audit.log` files (test artifacts), `.env.production` (had hardcoded password)

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy -D warnings` | Pass (0 warnings) |
| `cargo doc -D warnings` | Pass (0 warnings) |
| `cargo test --workspace` | Pass (15,100+ tests, 0 failures) |
| `cargo llvm-cov` | 90.16% line coverage |
| AGPL-3.0 / scyBorg triple license | Compliant |
| ecoBin (zero C on non-Android) | Compliant |

---

## Remaining Debt (Known)

- **iOS Secure Enclave**: Phase 2 implementation (stubs return `not_implemented` errors)
- **Old HSM traits**: 5 legacy hierarchies have migration docs → `HsmKeyProvider`; removal at v0.10.0
- **~200 `placeholder` comments**: Production code still has ~36 `// Placeholder` comments in HSM stubs, config modules, and handler files — most are honest about deferred implementations
- **`serde_yaml` deprecation**: Track `yaml_serde` as maintained successor when ready to migrate
- **`missing_errors_doc` lint**: Currently `allow` — would add `# Errors` sections to ~50+ public functions returning `Result`

---

## For primalSpring

Wave 23 eliminates ~8,500 lines of dead code and 858 duplicated doc lines. Self-knowledge constants are now centralized. No behavioral changes — all changes are code hygiene, documentation accuracy, and lint tightening. All gates green.
