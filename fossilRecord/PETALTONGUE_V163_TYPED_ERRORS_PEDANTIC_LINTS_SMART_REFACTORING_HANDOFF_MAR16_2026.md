# petalTongue v1.6.3 — Typed Errors, Pedantic Lints & Smart Refactoring Handoff

**Date**: March 16, 2026
**Version**: 1.6.3
**Primal**: petalTongue (Universal Representation)
**Session**: Comprehensive audit and deep evolution — typed errors, pedantic lint enforcement, smart refactoring, CI alignment, doc cleanup

---

## Session Summary

Full audit of petalTongue against wateringHole standards followed by execution
of all findings. Migrated all production error handling from `anyhow` to typed
`thiserror` errors (14 new error types across 12 crates). Achieved zero clippy
warnings under pedantic + nursery lints with CI enforcement. Smart-refactored
5 large files into cohesive modules. Added `server` subcommand for headless IPC
daemon. Eliminated hardcoded GPU/ToadStool endpoints via env vars. Cleaned root
docs, fixed broken links, refreshed evolution roadmap.

---

## Key Changes

### anyhow → thiserror Migration (All Production Code)

| Crate | Error Type | Variants |
|-------|-----------|----------|
| petal-tongue-discovery | `DiscoveryError` | Extended with 7 new variants |
| petal-tongue-entropy | `EntropyError` | New |
| petal-tongue-graph | `AudioExportError` | New |
| petal-tongue-api | `BiomeOsClientError` | New |
| petal-tongue-ipc | `PrimalRegistrationError`, `SocketPathError` | New |
| petal-tongue-tui | `TuiError` | New |
| petal-tongue-cli | `CliError` | New |
| petal-tongue-core | `PetalTongueError` | Extended with 4 new variants |
| petal-tongue-ui-core | `UiCoreError` | New |
| petal-tongue-ui | `UiError` | New (8 sub-variants) |
| src/ (UniBin) | `AppError` | New |
| petal-tongue-headless | `HeadlessError` | New |
| doom-core | `DoomError` | New |

`anyhow` retained only in `[dev-dependencies]` for test convenience.

### Clippy Pedantic + Nursery — Zero Warnings

- `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` clean
- CI updated to enforce pedantic + nursery lints
- Workspace lint centralization: `[workspace.lints.clippy]` in root `Cargo.toml`
- Removed redundant crate-level `#![warn(clippy::pedantic)]` and `#![allow(...)]` from 6 crates
- Added `#[expect(..., reason = "...")]` for justified suppressions

### Smart Refactoring (5 Large Files)

| File | Before | After | Modules |
|------|--------|-------|---------|
| trust_dashboard.rs | 977 | 320 | types, compute, tests, mod |
| scene_bridge.rs | 960 | 67 | types, paint, tests, mod |
| awakening_coordinator.rs | 934 | 250 | types, timeline, tests, mod |
| visualization.rs (IPC) | 922 | 465 | mod, tests |
| domain_charts.rs | 914 | 308 | types, validation, tests, mod |

All public APIs preserved via re-exports.

### Server Subcommand

`petaltongue server` — runs IPC Unix socket server without any GUI.
Useful for headless daemon deployments where other primals need to
query petalTongue's visualization capabilities.

### Hardcoded Endpoint Elimination

- `PETALTONGUE_GPU_COMPUTE_ENDPOINT`: Configures barraCuda GPU compute endpoint
- `TOADSTOOL_PORT`: Configures ToadStool display backend port

### Doc Cleanup

- README.md: Updated quality table, added `server` subcommand, added error handling row
- START_HERE.md: Updated test count, coverage, clippy command, error handling rule
- ENV_VARS.md: Added GPU compute and ToadStool port vars, updated date
- CHANGELOG.md: New v1.6.3 entry with full change summary
- NEXT_EVOLUTIONS.md: Complete rewrite for v1.6.3 (was stale from v1.0-1.3 era)
- BIOMEOS_INTEGRATION_GUIDE.md: Fixed broken links to archived audit docs
- PROJECT_STATUS.md: Updated coverage numbers

---

## Verification State

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` | Zero warnings |
| `cargo test --workspace` | 5,076 passed, 0 failed |
| `cargo doc --workspace --no-deps` | Clean |
| Files over 1000 lines | None (largest: 876) |
| `anyhow` in production | Zero (dev-dependencies only) |

---

## Remaining Work

1. **Coverage**: 87% → 90% target (gap: petal-tongue-ui at 75.7%)
2. **Live integration testing**: End-to-end with running springs
3. **ToadStool display backend**: `display.*` methods wiring
4. **Cross-compilation**: armv7, macOS, Windows, WASM
5. **Fuzz testing**: `cargo-fuzz` harnesses for JSON-RPC, grammar, scenarios
6. **barraCuda compute parity**: math.stat.*, math.tessellate.*, math.project.* IPC clients

---

## wateringHole Compliance

| Standard | Status |
|----------|--------|
| PRIMAL_IPC_PROTOCOL | Compliant — 35 capabilities, ipc.register |
| ECOBIN_ARCHITECTURE_STANDARD | Compliant — zero C deps, pure Rust |
| UNIBIN_ARCHITECTURE_STANDARD | Compliant — 6 subcommands (ui, tui, web, headless, server, status) |
| SEMANTIC_METHOD_NAMING | 40+ methods, domain.operation[.variant] |
| GATE_DEPLOYMENT_STANDARD | Compliant — AGPL-3.0-only, SPDX headers |
| SCYBORG_PROVENANCE_TRIO | Client wired (rhizoCrypt + sweetGrass + loamSpine) |
| SPRING_AS_NICHE_DEPLOYMENT | Full niche.yaml with organisms/interactions |
