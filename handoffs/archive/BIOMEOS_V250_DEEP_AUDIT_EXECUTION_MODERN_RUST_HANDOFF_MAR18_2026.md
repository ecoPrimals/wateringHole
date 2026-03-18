# biomeOS v2.50 — Deep Audit Execution + Modern Idiomatic Rust Evolution

**Date**: March 18, 2026
**Session**: Full audit execution — deep debt solutions, modern Rust evolution, sovereignty hardening
**Status**: Complete — 5,203 tests passing, 0 failures, 0 clippy warnings

---

## Summary

Comprehensive execution of the v2.49 audit findings. Every critical, high, and medium
priority item has been addressed. The codebase has evolved from "passing" to "pedantic"
with workspace-wide lint inheritance, edition 2024 across all crates, tarpc runtime wiring,
sovereignty-first STUN configuration, and scyBorg triple-copyleft licensing.

## Changes

### Edition 2024 Migration (18 crates)
- Migrated 18 crates from `edition = "2021"` to `edition.workspace = true` (2024)
- Fixed `gen` keyword reservation: `rng.gen()` → `rng.r#gen()` (3 sites)
- Fixed `collapsible_if` let-chain suggestions where appropriate

### Workspace Lint Inheritance (23 crates)
- Added `[lints] workspace = true` to all 23 workspace member crates
- All crates now inherit `clippy::pedantic`, `clippy::nursery`, `unwrap_used = "deny"`
- Fixed ~300+ clippy errors surfaced by inheritance:
  - `must_use` / `const fn` annotations
  - `unused_self` → associated functions
  - `needless_pass_by_value` → references
  - `map().unwrap_or()` → `map_or()` / `is_some_and()`
  - `manual_let_else` → `let...else` patterns
  - `format_push_string` → `write!()`
  - `match_same_arms` merged
  - `ref_option` (`&Option<T>` → `Option<&T>`)

### tarpc Runtime Wiring
- Added `DefaultHealthService` — ready-to-use `HealthRpc` impl for any primal
- Added `start_tarpc_sidecar()` / `start_default_tarpc_sidecar()` in primal SDK
- Exported in SDK prelude for easy adoption
- Protocol escalation path is now functional: JSON-RPC → tarpc binary

### Zero-Copy Fixes (6 sites)
- `Bytes::from(x.to_vec())` → `Bytes::copy_from_slice(&x)` across:
  - family_discovery.rs, p2p_coordination/adapters.rs, spore/incubation/mod.rs
  - platypus/crypto.rs, platypus/fusion.rs

### Sovereignty Hardening
- Removed Google/Cloudflare STUN servers from all 4 config files + 1 template
- Replaced with community-operated servers (Nextcloud, stunprotocol.org, SIP.US)
- Sovereignty-first comment blocks added to each config

### scyBorg License Trio
- Added `LICENSE-ORC` (Open RPG Creative License for game mechanics)
- Added `LICENSE-CC-BY-SA` (Creative Commons for documentation/creative content)
- Completes the AGPL-3.0 + ORC + CC-BY-SA 4.0 triple-copyleft framework

### Large File Refactoring
- `atomic_client.rs` (963 → 835 lines): Extracted `AtomicPrimalClient` to `atomic_primal_client.rs`
- `socket_discovery/engine.rs` (963 → 899 lines): Extracted `path_builder.rs` + `neural_api.rs`

### Hardcoded Evolution
- `mode.rs`: `"beardog"` / `"songbird"` → `primal_names::BEARDOG` / `SONGBIRD` constants
- `primals.rs`: `format!("unix:/tmp/{id}")` → `SystemPaths::primal_socket(id)`
- Dead code: `#[allow(dead_code)]` → `#[expect(dead_code, reason = "...")]` on live_discovery.rs

### Code Cleanup
- Removed commented-out `ClientRegistry` code from universal_biomeos_manager
- Fixed broken doc link in retry.rs (`[`call`]` → `[`CircuitBreaker::call`]`)
- Archived `scripts/mini_stun_server.py` (Python STUN → ecoPrimals/archive/)

### Test Coverage (+39 tests)
- genome.rs: 10 new tests (build, verify, info, list, compose, error paths)
- modes/api.rs: 4 new tests (config resolution, socket priority)
- main.rs: 17 new tests (CLI parsing for all subcommands)
- modes/nucleus.rs: 4 new tests (primal commands, base64 encoding)
- modes/model_cache.rs: 4 new tests (import, resolve, size formatting)

### Root Documentation Updates
- CURRENT_STATUS.md: v2.49 → v2.50, updated all metrics
- README.md: Updated test count, coverage, clippy status, license
- START_HERE.md: Updated status line
- QUICK_START.md: Updated test count and coverage
- DOCUMENTATION.md: Updated version references

## Audit Findings (All Addressed)

| Finding | Before | After |
|---------|--------|-------|
| Edition 2024 | 18 crates on 2021 | All 23 on 2024 |
| Workspace lints | 1 crate inheriting | All 23 inheriting |
| tarpc wiring | Dead code | Functional sidecar |
| Google/Cloudflare STUN | 4 configs | 0 (community only) |
| scyBorg license files | AGPL only | AGPL + ORC + CC-BY-SA |
| Files >900 LOC | 2 files at 963 | Max 899 |
| Commented-out code | 6 blocks | 0 |
| Broken doc links | 1 | 0 |
| Zero-copy regressions | 6 sites | 0 |
| Python scripts | 1 (mini STUN) | 0 (archived) |
| TODO/FIXME in .rs | 0 | 0 (confirmed) |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 5,203 passing, 0 failures |
| Clippy | 0 warnings (pedantic+nursery, all crates) |
| Formatting | PASS |
| Doc warnings | 0 |
| Crates on Edition 2024 | 23/23 |
| Workspace lint inheritance | 23/23 |
| Files updated | ~200+ |
| New test files | 5 modules expanded |
| Handoffs archived | 1 |
| Scripts archived | 1 (mini_stun_server.py) |

## Known Items (Future Work)

- Port 3492 hardcoded in livespore/pixel8a deployment scripts (deploy-specific, not primal code)
- STUN config duplicated across 4 deployment targets (could be symlinked)
- Shell scripts in livespore-usb/ are deployment scaffolding (not production primal code)
- `build_primals_for_testing.sh` could evolve to cargo xtask
- Coverage at ~82%, target is 90% (remaining gaps in integration/deployment code)
