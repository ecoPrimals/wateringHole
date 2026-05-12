# ToadStool S173 — Deep Debt Evolution Handoff

**Date**: April 19, 2026
**Session**: S173
**Primal**: toadStool
**Scope**: runtime/edge compilation fixes, smart refactoring of 3 large specialty files, lint attribute evolution

---

## Summary

S173 resolved 61 compilation errors in the `toadstool-runtime-edge` crate, smart-refactored 3 monolithic files (>700L each) in `toadstool-runtime-specialty` into directory modules, and evolved bare `#[allow(dead_code)]` attributes to `#[expect(dead_code, reason)]` with explicit justifications.

---

## Changes by Phase

### Phase 1: Fix runtime/edge Compilation Errors (61 errors → 0)

| Error Category | Fix |
|---------------|-----|
| Error constructor API drift (`discovery_error`, `execution_error`, `connection_error`, `not_available`, `compilation_error`) | Aligned to current `ToadStoolError` API: `runtime`, `execution`, `network`, `not_supported` |
| Module path resolution (`toadstool::platform_paths`) | Corrected to `toadstool_common::platform_paths` |
| `Box<dyn CommunicationProtocol>: Clone` not satisfied | Refactored `send`/`receive` to borrow through read lock instead of cloning |
| `serialport::SerialPort` not `Sync` | Migrated `serial_port` field from `Arc<RwLock<…>>` to `Arc<Mutex<…>>` (only `Send` required) |
| Missing `Display` impl for `EdgePlatform` | Added `impl Display` with formatted output per variant |
| UUID `new_v5` not in scope | Added `"v5"` feature to `uuid` dependency |
| Borrowed data escapes in `start_continuous_discovery` | Changed to `self: &Arc<Self>` pattern with `Arc::clone` |
| `serialport::available_ports()` error conversion | Added `.map_err(\|e\| ToadStoolError::runtime(...))` |
| `ExecutionStatus::Failed` type mismatch | Updated to struct variant syntax (`{ error: e.to_string().into() }`) |

### Phase 2: Smart Refactoring (3 files)

| Original File | Lines | New Structure |
|--------------|-------|--------------|
| `cpu6502.rs` | 828 | `cpu6502/mod.rs` (core + memory), `alu.rs` (ALU helpers), `decode.rs` (opcode step), `tests.rs` |
| `emulator_impls.rs` | 717 | `emulator_impls/mod.rs` (shared helpers), `mos6502.rs` (6502 impl), `z80.rs` (Z80 impl), `tests.rs` |
| `programmer_impls.rs` | 712 | `programmer_impls/mod.rs` (shared parsers), `init.rs` (initialization), `generic.rs` (GenericProgrammer), `eprom.rs` (EPROMProgrammer), `tests.rs` |

All submodules use `pub(super)` visibility. Zero behavioral changes. All existing tests pass.

### Phase 3: Lint Attribute Evolution

| File | Change |
|------|--------|
| `security/sandbox/src/linux/proc.rs` | `#[allow(dead_code)]` → `#[expect(dead_code, reason = "variants constructed for completeness; consumers use ToadStoolError")]` |
| `runtime/specialty/src/embedded/programmers.rs` | `#[allow(dead_code)]` on `voltage_mv` → `#[expect(dead_code, reason = "stored from config; will be used by voltage-aware programming")]` |
| `runtime/specialty/src/embedded/programmers.rs` | `#[allow(dead_code)]` on `engine` → `#[expect(dead_code, reason = "stored from config; will drive actual EPROM protocol I/O")]` |

### Phase 4: Test Fix

- `edge_config_tests::test_edge_runtime_config_default` — assertion for `cross_compile_cache_path` updated from hardcoded `/tmp/toadstool_edge_cache` to `ends_with("edge_cache")` (XDG-compliant after `platform_paths` fix).

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | Pass |
| `cargo test -p toadstool-runtime-edge` | **102 passed, 0 failed** |
| `cargo test -p toadstool-runtime-specialty` | **38 passed, 0 failed** |
| `cargo test -p toadstool-security-sandbox` | **98 passed, 0 failed** |
| `cargo clippy -p toadstool-runtime-specialty -p toadstool-security-sandbox -- -D warnings` | 0 warnings |
| `cargo test --workspace --lib` (excluding server) | **7,124 passed, 0 failed** |

---

## Impact on Springs

- **wetSpring**: `compute.dispatch` JSON-RPC routing (PG-15) was fixed in prior commit; S173 fixes edge compilation which unblocks edge device discovery for any spring using `toadstool-runtime-edge`.
- **All springs**: No API changes. All existing IPC contracts preserved.

---

## Remaining Debt

| ID | Status |
|----|--------|
| D-COVERAGE-GAP | 83.6% → 90% target; hardware-gated gaps remain |
| D-EMBEDDED-PROGRAMMER | Protocol engines complete; USB/serial transport absent |
| D-EMBEDDED-EMULATOR | CPU cores implemented; decimal mode, full Z80, GDB transport remaining |
| D-HW-LEARN-VERIFY | Typed verification; nouveau DRM UAPI without BAR mmap remaining |
