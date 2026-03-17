# coralReef — Phase 10 Iteration 53 Handoff

**Date**: March 17, 2026  
**Iteration**: 53 — Deep Audit Execution + Safe Rust Evolution + Test Coverage  
**Tests**: 2241 passing (+48 VFIO), 0 failed, 90 ignored  
**Coverage**: 57.75% region / 58.16% line / 68.50% function (target 90%)  
**Clippy**: Zero warnings (pedantic + nursery)  
**Format**: Clean (`cargo fmt`)  
**Docs**: Zero warnings (`RUSTDOCFLAGS="-D warnings" cargo doc --no-deps`)

---

## Summary

Comprehensive codebase audit and execution pass. Enabled clippy nursery lints
workspace-wide, consolidated unsafe BAR0 access into a safe wrapper, extracted
magic numbers to named constants, evolved metal interface structs to
zero-allocation `&'static str`, added fault injection and unit test coverage
(+56 tests), enforced `#![forbid(unsafe_code)]` on coral-glowplug, adopted
XDG Base Directory for config paths, and added SPDX license headers to all
markdown files. All quality gates green.

## Changes

### 1. clippy::nursery Lints Enabled
- Added `nursery = "warn"` to `[workspace.lints.clippy]` in root `Cargo.toml`.
- Catches additional patterns: option-if-let-else, redundant clones, cognitive
  complexity, etc.
- All existing warnings resolved during enablement.

### 2. SysfsBar0 Safe Wrapper
- **New file**: `crates/coral-driver/src/vfio/sysfs_bar0.rs`
- Consolidates the repeated mmap→volatile-read→munmap pattern used by 3 oracle
  modules into a single safe API with bounds-checked `read_u32()`.
- `Send + Sync` with documented safety invariants.
- `Drop` impl for automatic `munmap`.
- **Refactored consumers**:
  - `vfio/channel/oracle.rs` — `from_live_card()`
  - `vfio/channel/glowplug/oracle.rs` — `apply_oracle_registers()`
  - `vfio/channel/hbm2_training/oracle.rs` — `capture_oracle_state()`

### 3. Magic Number Extraction
- `amd_metal.rs`: `MI50_HBM2_SIZE`, `MI50_HBM2_STACKS`, `MI50_L2_SIZE`,
  `MI50_L2_SLICES`, `BUSY_BIT_MASK` — replaces inline hex/arithmetic.
- `nv_metal.rs`: `PRAMIN_APERTURE_SIZE` — replaces `1024 * 1024`.
- `device.rs`: `PCI_READ_DEAD`, `PCI_READ_ALL_ONES`, `PCI_FAULT_BADF`,
  `PCI_FAULT_BAD0`, `PCI_FAULT_BAD1` + `is_faulted_read()` helper.

### 4. Zero-Allocation Metal Interface
- `gpu_vendor.rs`: `PowerDomain.name`, `MetalMemoryRegion.name`,
  `EngineInfo.name`, `WarmupStep.description` evolved from `String` to
  `&'static str` — eliminates heap allocation for static GPU metadata.
- All consumers in `amd_metal.rs`, `nv_metal.rs`, `warm.rs` updated.

### 5. Safety Enforcement
- `#![forbid(unsafe_code)]` added to `crates/coral-glowplug/src/main.rs`.
- Compile-time rejection of any unsafe code in the glowplug binary.

### 6. XDG Config Path
- `coral-glowplug` now resolves config via:
  1. `$XDG_CONFIG_HOME/coralreef/glowplug.toml` (if set)
  2. `$HOME/.config/coralreef/glowplug.toml` (fallback)
  3. `/etc/coralreef/glowplug.toml` (system-wide)
- Follows XDG Base Directory Specification.

### 7. IPC Fault Injection Tests
- **New file**: `crates/coralreef-core/src/ipc/tests_fault.rs`
- 12 async tests covering:
  - Client disconnect mid-request
  - Malformed JSON (missing closing brace)
  - Truncated JSON
  - Oversized payload (1 MB)
  - Empty body
  - Invalid JSON-RPC method names
  - Missing required fields
  - Concurrent stress (10 simultaneous requests)

### 8. coral-glowplug Unit Tests (+39)
- `config.rs`: Config loading, error variants, default values
- `health.rs`: Device health states, display, transitions
- `device.rs`: `is_faulted_read` logic, PCI fault constants, chip identification,
  `PersonalityRegistry` validation
- `socket.rs`: JSON-RPC message parsing and serialization

### 9. Idiomatic Rust Evolution
- `or_exit.rs`: `if let/else` → `unwrap_or_else` (clippy `option_if_let_else`)
- `unix_jsonrpc.rs`: `pub(crate)` in private modules → `pub` (clippy lint)
- `compile.rs`, `types.rs`: Same `pub(crate)` → `pub` evolution
- `ipc/mod.rs`: `BoundAddr::protocol()` visibility widened for binary usage
- Doc link fixes: `DeviceCompileResult` re-exported, `DriverPreference` full path

### 10. SPDX License Headers
- `<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->` added to 14 markdown files:
  README, CONTRIBUTING, START_HERE, STATUS, COMPILATION_DEBT_REPORT, ABSORPTION,
  WHATS_NEXT, EVOLUTION, CONVENTIONS, docs/HARDWARE_TESTING, docs/UVM_COMPUTE_DISPATCH,
  specs/CORALREEF_SPECIFICATION, specs/SOVEREIGN_MULTI_GPU_EVOLUTION, genomebin/README.

### 11. PersonalityRegistry Integration
- `DeviceSlot::activate` now validates personality via `PersonalityRegistry`,
  exercising the `dyn GpuPersonality` trait system in production code.
- Personality-aware health check logging (`name()`, `provides_vfio()`,
  `supports_hbm2_training()`).

## Test Impact

| Metric | Before | After |
|--------|--------|-------|
| Total passing | 2185 | 2241 |
| New tests | — | +56 |
| Failed | 0 | 0 |
| Ignored | 90 | 90 |
| Region coverage | 57.28% | 57.75% |
| Line coverage | 57.71% | 58.16% |
| Function coverage | 67.98% | 68.50% |

## Files Modified

### New Files
- `crates/coral-driver/src/vfio/sysfs_bar0.rs`
- `crates/coralreef-core/src/ipc/tests_fault.rs`

### Modified Files
- `Cargo.toml` — nursery lint
- `crates/coral-driver/src/vfio/mod.rs` — sysfs_bar0 module
- `crates/coral-driver/src/vfio/gpu_vendor.rs` — `&'static str` evolution
- `crates/coral-driver/src/vfio/amd_metal.rs` — magic number constants, `.into()` removal
- `crates/coral-driver/src/vfio/nv_metal.rs` — PRAMIN constant, field docs, `.into()` removal
- `crates/coral-driver/src/vfio/channel/oracle.rs` — SysfsBar0 refactor
- `crates/coral-driver/src/vfio/channel/glowplug/oracle.rs` — SysfsBar0 refactor
- `crates/coral-driver/src/vfio/channel/glowplug/warm.rs` — `&'static str` migration
- `crates/coral-driver/src/vfio/channel/hbm2_training/oracle.rs` — SysfsBar0 refactor
- `crates/coral-glowplug/src/main.rs` — `#![forbid(unsafe_code)]`, XDG config
- `crates/coral-glowplug/src/device.rs` — PCI constants, personality integration, tests
- `crates/coral-glowplug/src/personality.rs` — `#[allow(dead_code)]` with reason
- `crates/coral-glowplug/src/config.rs` — unit tests
- `crates/coral-glowplug/src/health.rs` — unit tests
- `crates/coral-glowplug/src/socket.rs` — unit tests
- `crates/coralreef-core/src/or_exit.rs` — idiomatic `unwrap_or_else`
- `crates/coralreef-core/src/ipc/mod.rs` — visibility, unused import allow
- `crates/coralreef-core/src/ipc/unix_jsonrpc.rs` — pub visibility, safer param extraction
- `crates/coralreef-core/src/service/compile.rs` — pub visibility, doc link fix
- `crates/coralreef-core/src/service/types.rs` — pub visibility
- `crates/coralreef-core/src/service/mod.rs` — DeviceCompileResult re-export
- `crates/coral-gpu/src/context.rs` — DriverPreference doc link
- `scripts/coverage.sh` — coral-glowplug added
- 14 markdown files — SPDX headers

## Root Docs Updated
- README.md, STATUS.md, WHATS_NEXT.md, EVOLUTION.md, CONTRIBUTING.md,
  COMPILATION_DEBT_REPORT.md, ABSORPTION.md, docs/HARDWARE_TESTING.md
- All test counts, coverage numbers, and iteration references updated to Iter 53.

## Remaining Evolution Targets

| Target | Priority | Detail |
|--------|----------|--------|
| Coverage 58% → 90% | P1 | Codegen paths (0% coverage on many encoder files), driver hardware-gated code |
| Titan V nouveau dispatch | P0 | Pipeline wired, needs on-site hardware validation |
| UVM hardware validation | P0 | Full dispatch pipeline implemented, needs RTX 3090 |
| barraCuda integration | P2 | `CoralReefDevice` wiring, SovereignCompiler routing |
| Wire new UAPI into NvDevice | P1 | Replace legacy `create_channel` with vm_init→vm_bind→exec |
| `script.rs` approaching 1000 LOC | P3 | Defer until test coverage enables safe refactoring |
| 4 `#[allow(dead_code)]` without reasons | P3 | In coral-driver VFIO modules — minor hygiene |
