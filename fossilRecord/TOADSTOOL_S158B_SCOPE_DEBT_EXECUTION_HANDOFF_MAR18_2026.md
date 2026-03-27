# ToadStool S158b — Scope + Deep Debt Execution + License Final Alignment

**Date**: March 18, 2026
**Session**: S158b
**Author**: toadStool team

---

## Summary

Continuation of S158 audit execution. Rewrote `specs/README.md` with scope, aims, and
four-phase silicon-targeting future ("Every Piece of Silicon"). Fixed build failures from
zero-copy `Arc<str>` expansion. Smart-refactored two large files. Evolved remaining
hardcoded IPs to centralized constants. Migrated unsafe `env::set_var` to `temp_env`.
Final SPDX sweep — all `.rs` and `.md` files aligned to `AGPL-3.0-or-later`.

## Changes

### specs/README.md — Scope & Aims Rewrite
- Replaced "Current Status" section with "Scope & Aims" — core principles (hardware
  atheism, self-knowledge, tolerance-based routing, sovereign by default, ecoBin v3.0,
  deep debt resolution), quality gates, key numbers, simplified architecture overview.
- Added "Every Piece of Silicon — Future Evolution (S158)" table: 4 phases (A: Sovereign
  Compute, B: Performance Surface Database, C: Multi-Unit Routing, D: Mixed Command
  Stream Submission) with dependencies.
- Updated TOADSTOOL_LEVERAGE_GUIDE.md in wateringHole with Section 11 matching the
  silicon-targeting roadmap.

### Build Fix — `toadstool-integration-protocols`
- 5 compilation errors from `Arc<str>`/`String` mismatches resolved in
  `crates/integration/protocols/src/client/mod.rs`.
- Unstable `str_as_str` API replaced with `&*arc` dereference pattern.

### Smart Refactoring — Two Large Files
- `infant_discovery/engine.rs` (817 → 715 lines): `ServiceDiscoveryConfig` extracted to
  `config.rs` (+ 4 tests), `DiscoveryEngineBuilder` to `builder.rs`.
- `server/src/capabilities/mod.rs` (760 → 406 lines): GPU detection (326 lines) to
  `gpu.rs`, path helpers to `paths.rs` (+ 4 tests).

### Hardcoding Evolution — IPs to Constants
- `runtime_ports.rs`: `"127.0.0.1"` → `LOCALHOST_IPV4`, `"0.0.0.0"` → `BIND_ALL_IPV4`.
- `runtime_discovery.rs`: `"localhost"` → `DEFAULT_HOSTNAME`.
- `zero_config/discovery.rs`: `"127.0.0.1"` → `LOCALHOST_IPV4`.
- `zero_config/service_discovery.rs`: local `BIND_ANY` const → `network::BIND_ANY`.
- `auto_config/ecosystem.rs`: `"0.0.0.0"` → `BIND_ADDRESS_DEFAULT`.
- `env_config/network.rs`: hardcoded literals → `BIND_ADDRESS_DEFAULT` + `DEFAULT_HOSTNAME`.

### Unsafe Evolution — `temp_env` Migration
- `server/src/unibin/format.rs`: `unsafe { env::set_var }` → `temp_env::with_var`.
- `server/src/capabilities/tests/discovery_dir.rs`: `unsafe { env::set_var/remove_var }` →
  `temp_env::with_vars` / `with_vars_unset`.
- `core/common/src/discovery_defaults.rs`: `unsafe { env::set_var }` → `temp_env::with_var`.

### Documentation — High-Impact Missing Docs Filled
- `toadstool-core`: 7 `HardwareDevice` fields documented.
- `toadstool-common`: 9 `ecosystem.rs` constants, 4 `pci_discovery::vendors` constants.
- `warn(missing_docs)` now enabled on 38 crates. 694+ warnings visible, fill-in ongoing.

### License — Final SPDX Alignment
- 47 `.rs` files still had `AGPL-3.0-only` SPDX headers — all migrated to `AGPL-3.0-or-later`.
- 25+ `.md` files (READMEs, specs, showcase, contrib) still referenced `AGPL-3.0-only` —
  all aligned to `AGPL-3.0-or-later`.
- `deny.toml` comment clarified: `AGPL-3.0-or-later` is the canonical scyBorg license.
- README.md, STATUS.md, DEBT.md, SPRING_ABSORPTION_TRACKER.md, DOCUMENTATION.md all
  updated to reflect `AGPL-3.0-or-later` canonically.

### Root Docs Refresh
- README.md: unsafe count 20 → 29 crates, license → `AGPL-3.0-or-later`, footer dated S158b.
- SPRING_ABSORPTION_TRACKER.md: session → S158b, license → `AGPL-3.0-or-later`, unsafe → 29.
- DEBT.md: temp_env marked resolved, SPDX sweep documented, license alignment entry clarified.
- STATUS.md: SPDX alignment entry updated for final sweep.

### Primal Self-Knowledge Audit — CONFIRMED CLEAN
- Zero cross-primal crate dependencies.
- Primal names appear only in legacy compatibility layers.
- All production dispatch is capability-based.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo build --workspace` | PASS |
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (pedantic + nursery) |
| `cargo doc --workspace --no-deps` | PASS |
| `cargo test --workspace` | 21,156+ tests, 0 failures |
| License | AGPL-3.0-or-later on 100% of .rs and .md files |
| `#![forbid(unsafe_code)]` | 29 crates forbid, ~10 deny |
| Production unsafe `env::set_var` | 0 — all migrated to `temp_env` |
| Hardcoded IPs/ports | 0 |
| File size limit | All < 1000 lines |

## Remaining Debt

| Item | Status |
|------|--------|
| D-COV: 83% → 90% line coverage | Ongoing — hardware mocks needed |
| D-DOCS: 694+ `missing_docs` warnings | Staged fill-in across 38 crates |
| Phase 2 dep migration (C bindings) | Future — `wgpu`/`naga` Rust-native path |
| Phase 3 tarpc binary transport | Future — zero-copy serialization |
| Barracuda path references in historical docs | 14+ docs reference `crates/barracuda/` (moved S94) — these are historical records |

## Cross-Primal Notes

- **wateringHole/TOADSTOOL_LEVERAGE_GUIDE.md** updated with Section 11: "Every Piece of
  Silicon — toadStool's Evolution Path". Details sovereign compute pipeline, performance
  surface database, multi-unit routing, and mixed command stream submission.
- **ludoSpring** guidance integrated: GPU fixed-function units (TMUs, ROPs, Rasterizer,
  Tessellator, Video Encode/Decode) identified as silicon surface for science repurposing.
- **coralReef** dependency for Phase A (sovereign pipeline) — needs USERD_TARGET fix and
  glowPlug boot persistence.

---

*AGPL-3.0-or-later — ecoPrimals sovereign community property.*
