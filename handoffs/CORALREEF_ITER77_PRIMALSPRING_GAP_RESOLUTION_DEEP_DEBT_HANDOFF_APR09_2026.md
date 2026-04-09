# coralReef Iter 77 — primalSpring Gap Resolution + Deep Debt Evolution Handoff

**Date**: April 9, 2026
**Primal**: coralReef
**Iteration**: 77
**Matrix**: ECOSYSTEM_COMPLIANCE_MATRIX v2.7.0

---

## Summary

Three gaps flagged by primalSpring team audit resolved: CR-01 (HIGH) BIOMEOS_INSECURE guard,
CR-02 (MEDIUM) Wire Standard L2 compliance, CR-03 (MEDIUM) BTSP Phase 2 scaffolding.
Deep debt systematically resolved across 6 categories: typed errors, lint evolution,
commented-out code cleanup, eprintln→tracing, domain overstep documentation, and
smart file refactoring. All quality gates green.

---

## Changes

### CR-01 (HIGH): BIOMEOS_INSECURE Guard

- `validate_insecure_guard()` added to coralreef-core, coral-glowplug, coral-ember
- Refuses startup when `BIOMEOS_FAMILY_ID` (non-default) + `BIOMEOS_INSECURE=1` both set
- Per `PRIMAL_SELF_KNOWLEDGE_STANDARD` v1.1
- Exit code 2 (ConfigError) on all 3 binaries
- Evolved from `Result<(), String>` to typed `ConfigError` via `thiserror`

### CR-02 (MEDIUM): Wire Standard Level 2

- `capability.list` now returns Wire Standard L2 envelope: `{primal, version, methods, capabilities}`
- `methods` flat array: 10 fully-qualified JSON-RPC methods (shader.compile.spirv, .wgsl, .status, .capabilities, .wgsl.multi, health.check, .liveness, .readiness, identity.get, capability.list)
- `primal` field: canonical name from CARGO_PKG_NAME
- Backward-compatible: `capabilities` domain array preserved for existing consumers

### CR-03 (MEDIUM): BTSP Phase 2 Scaffolding

- `btsp` module added to coralreef-core, coral-glowplug, coral-ember
- `BtspMode` enum: `Development` (passthrough) vs `Production { family_id }` (handshake required)
- `btsp_mode()` cached resolution from `BIOMEOS_FAMILY_ID`
- `gate_connection()` wired into all accept loops: Unix socket + TCP newline (coralreef-core), Unix + TCP (coral-glowplug SocketServer), Unix + TCP (coral-ember threaded)
- Development mode: raw JSON-RPC passthrough (current behavior preserved)
- Production mode: connection refused with diagnostic (pending hotspring-sec2-hal BearDog integration)

### Deep Debt Evolution

- **Typed errors**: `validate_insecure_guard` evolved from `Result<(), String>` to `Result<(), ConfigError>` with `#[derive(thiserror::Error)]` in all 3 crates. coral-glowplug/coral-ember use `ConfigError::InsecureWithFamily { family_id }`
- **Lint evolution**: `codegen/mod.rs` `#![allow(wildcard_imports, enum_glob_use)]` → `#![expect(...)]`. Documented why `ipc/mod.rs` must stay `#[allow(` (dual lib+bin build)
- **Commented-out code (T1 DEBT)**: 13+ files in `coral-reef/src/codegen/nv/` cleaned. Disabled match arms converted to architectural doc comments: tex encoders, memory ops, latency tables, HMMA types
- **eprintln → tracing**: 5 files in `coral-driver/src/vfio/channel/diagnostic/experiments/` (~50+ calls → tracing::info!)
- **Domain overstep (T6 DEBT)**: Audited `discovery.rs` (GPU target resolution for shader.* — legitimate) and `ecosystem.rs` (client role calling registry — legitimate). Clarifying module docs added
- **Smart refactoring**: `shader_header.rs` (905→5 submodules, max 385 lines). `personality.rs` (809→2 submodules, max 469 lines). Public API unchanged via `pub use` re-exports
- **Clippy fix**: match→matches!() in sm75_instr_latencies/mod.rs. Doc backtick fix in discovery.rs

---

## Quality Gate

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-features -- -D warnings` | PASS (0 warnings) |
| `RUSTDOCFLAGS='-D warnings' cargo doc --all-features --no-deps` | PASS |
| `cargo test --all-features` | 4,341 passed, 0 failed, 153 ignored |
| All files <1000 lines | PASS (max 982, test file) |
| Zero TODO/FIXME/HACK in production | PASS |
| SPDX headers | PASS |

---

## Compliance Matrix Update

| Tier | Before | After | Notes |
|------|--------|-------|-------|
| T1 Build | A ↑ | A | Commented-out code DEBT → resolved (13+ files cleaned) |
| T2 UniBin | A | A | No change |
| T3 IPC | A | A | Wire Standard L2 added |
| T4 Discovery | B | B | capability.list now Wire Standard L2; no self-register change |
| T5 Naming | A | A | No change |
| T6 Responsibility | A (DEBT) | A | Overstep audited: discovery.rs + ecosystem.rs documented as legitimate |
| T7 Workspace | A | A | No change |
| T8 Presentation | B | A | CONTEXT.md exists; root docs updated; 98%+ expect over allow |
| T9 Deploy | C | C | musl-static not yet verified |
| T10 Live | N/T | N/T | Not deployed |
| **Rollup** | **A** ↑ | **A** ↑ | T1/T6/T8 debt resolved |

---

## Remaining Work

- **BTSP Phase 2 full**: Blocked on BearDog `btsp.session.*` availability (hotspring-sec2-hal branch)
- **coral-driver `Result<_, String>`**: ~30 VFIO functions still use String errors; deep refactor to typed `DriverError`
- **musl-static verification (T9)**: Cross-compile both x86_64 and aarch64
- **plasmidBin submission (T9/T10)**: Requires musl-static builds
- **Coverage push**: Target 90% via `cargo llvm-cov`; hardware tests need local GPU
- **coralctl println→tracing**: CLI stdout output intentionally uses println; assess tracing applicability

---

## Files Changed

### New files
- `crates/coralreef-core/src/ipc/btsp.rs`
- `crates/coral-glowplug/src/socket/btsp.rs`
- `crates/coral-ember/src/btsp.rs`
- `crates/coral-reef/src/codegen/nv/shader_header/` (5 submodules)
- `crates/coral-glowplug/src/personality/` (2 submodules)

### Modified files
- `crates/coralreef-core/src/config.rs` — insecure guard + ConfigError
- `crates/coralreef-core/src/service/types.rs` — Wire Standard L2 CapabilityListResponse
- `crates/coralreef-core/src/service/mod.rs` — handle_capability_list with methods array
- `crates/coralreef-core/src/ipc/mod.rs` — btsp module registration
- `crates/coralreef-core/src/ipc/unix_jsonrpc.rs` — BTSP gate in accept loop
- `crates/coralreef-core/src/ipc/newline_jsonrpc.rs` — BTSP gate in TCP accept loop
- `crates/coralreef-core/src/main.rs` — insecure guard call
- `crates/coralreef-core/src/discovery.rs` — T6 doc clarification
- `crates/coralreef-core/src/ecosystem.rs` — T6 doc clarification
- `crates/coral-glowplug/src/config.rs` — insecure guard + family_id pub(crate)
- `crates/coral-glowplug/src/socket/mod.rs` — btsp gate in accept loop
- `crates/coral-glowplug/src/main.rs` — insecure guard call
- `crates/coral-glowplug/src/error.rs` — ConfigError::InsecureWithFamily
- `crates/coral-ember/src/config.rs` — insecure guard + family_id pub(crate)
- `crates/coral-ember/src/error.rs` — ConfigError::InsecureWithFamily
- `crates/coral-ember/src/lib.rs` — btsp module + ConfigError re-export
- `crates/coral-ember/src/runtime.rs` — BTSP gate in accept loops
- `crates/coral-reef/src/codegen/mod.rs` — allow→expect
- `crates/coral-reef/src/codegen/nv/sm75_instr_latencies/mod.rs` — matches!() fix
- 13+ codegen files: commented-out code cleanup
- 5 diagnostic experiment files: eprintln→tracing
