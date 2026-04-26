<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 84: ecoBin Cross-Arch Evolution + Deep Debt Solutions

**Date**: April 19, 2026
**Author**: coralReef team
**Status**: Complete — all verification gates pass

---

## Summary

Iteration 84 completes the ecoBin cross-architecture evolution and deep debt elimination for the coralReef primal. All 3 daemon crates (coral-ember, coral-glowplug, coral-gpu) now pass `cargo check` on macOS x86_64, macOS aarch64, and Linux aarch64-musl with zero errors. Production code has zero `.unwrap()`, zero hardcoded ports/addresses, all mocks test-isolated, and all `eprintln!` calls migrated to structured tracing.

## Cross-Architecture Compliance (ecoBin v3)

### coral-glowplug
- Linux-specific modules gated behind `#[cfg(target_os = "linux")]`: capture, sec2_bridge, device, ember, health, socket (most handlers)
- `PowerState` extracted to portable `power_state` module for cross-platform availability
- `coral-driver` dependency made target-specific in Cargo.toml (vfio feature Linux-only)
- Stub `main()` for non-Linux targets
- All Linux-only integration tests gated with `#![cfg(target_os = "linux")]`

### coral-gpu
- `probe_pcie_topology()` given cross-platform stub returning empty Vec on non-Linux
- Linux-specific `driver` import gated with `#[cfg(target_os = "linux")]`

### coral-ember (prior iteration, verified)
- Already gated from Iteration 83b — verified passing on all 3 non-native targets

### Verification
- `cargo check --target x86_64-apple-darwin`: 0 errors
- `cargo check --target aarch64-apple-darwin`: 0 errors
- `cargo check --target aarch64-unknown-linux-musl`: 0 errors

## Smart File Refactoring (>800L Production Library Files)

All 4 production library files over 800 lines were refactored using cohesive extraction:

| File | Before | After | Strategy |
|------|--------|-------|----------|
| `alloc.rs` | 996L | 536 + 473 (`alloc_channel.rs`) | GPFIFO/compute/channel/promote methods extracted |
| `sovereign_init.rs` | 984L | 457 + 411 + 132 | Pipeline stages + types extracted |
| `uvm/mod.rs` | 869L | 481 + 397 (`constants.rs`) | ioctl/RM/UVM constant surface extracted |
| `runner.rs` | 815L | 589 + 269 (`matrix_support.rs`) | Diagnostic matrix support functions extracted |

Remaining >800L files are test files, auto-generated ISA tables, `#[repr(C)]` ABI structs, or hardware latency models — all exempt from the split rule.

## Code Hygiene

- **eprintln/println → tracing**: 62 replacements across 10 coralctl handler files + union_find.rs. CLI user-facing output preserved as `println!`.
- **.unwrap() eliminated**: All production `.unwrap()` in nvdec_scrubber.rs converted to `.expect("4-byte slice")`. All remaining `.unwrap()` confirmed `#[cfg(test)]`-only.
- **Hardcoded socket group**: coral-ember socket group now uses `CORALREEF_SOCKET_GROUP` env var (matching coral-glowplug pattern).
- **Mocks**: All `MockSysfs`, `MockFirmwareSource`, `MockBar0`, `MockRegs` verified `#[cfg(test)]`-gated.

## Verification Gates

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo test --all-features` | 4541 passed, 0 failed, 155 ignored |
| `cargo check --target x86_64-apple-darwin` | 0 errors |
| `cargo check --target aarch64-apple-darwin` | 0 errors |
| `cargo check --target aarch64-unknown-linux-musl` | 0 errors |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Impact on Other Primals

### primalSpring
- Cross-arch gap from v0.9.17 genomeBin handoff is now resolved for coralReef
- coralReef can be included in all 9 target architecture builds

### toadStool / barraCuda
- No API changes — all `shader.compile.*` IPC contracts unchanged
- Internal module reorganization is transparent to consumers

### hotSpring
- `sovereign_init()` public API unchanged — stages extracted but re-exported at same paths
- `RM_ALLOC`/`RM_CONTROL` channel operations unchanged — extracted to `alloc_channel.rs` but still on `RmClient`

## Files Changed

### New files
- `crates/coral-driver/src/nv/uvm/rm_client/alloc_channel.rs`
- `crates/coral-driver/src/nv/uvm/constants.rs`
- `crates/coral-driver/src/vfio/sovereign_types.rs`
- `crates/coral-driver/src/vfio/sovereign_stages.rs`
- `crates/coral-driver/src/vfio/channel/diagnostic/runner/matrix_support.rs`
- `crates/coral-glowplug/src/power_state.rs`
- `crates/coral-glowplug/src/glowplug_main_linux.rs`
- `crates/coral-glowplug/src/bin/coralctl/coralctl_main_linux.rs`

### Modified files (key)
- `crates/coral-glowplug/Cargo.toml` — target-specific coral-driver dependency
- `crates/coral-glowplug/src/lib.rs` — cfg gates for Linux-only modules
- `crates/coral-glowplug/src/main.rs` — non-Linux stub
- `crates/coral-gpu/src/pcie.rs` — cross-platform stub
- `crates/coral-ember/src/runtime.rs` — CORALREEF_SOCKET_GROUP env var
- `crates/coral-driver/src/nv/vfio_compute/acr_boot/nvdec_scrubber.rs` — .unwrap() → .expect()
- 10+ coralctl handler files — eprintln → tracing

---

*coralReef Iteration 84 — ecoBin cross-arch evolution complete. 4541 tests, zero failures, zero clippy warnings. Cross-compiles cleanly across 3 non-native target triples. All production library files under 800 lines. All mocks test-isolated. All hardcoding evolved to env-var-backed. Pure Rust sovereignty.*
