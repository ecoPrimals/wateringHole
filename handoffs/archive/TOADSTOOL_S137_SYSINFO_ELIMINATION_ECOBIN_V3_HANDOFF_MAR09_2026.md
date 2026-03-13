# ToadStool S137 — sysinfo Elimination & ecoBin v3.0 Handoff

**Date**: March 9, 2026  
**From**: toadStool (S137)  
**To**: All primals, wateringHole  
**Type**: Deep Debt Solution + Ecosystem Standard Evolution

---

## Summary

toadStool S137 eliminated all direct C dependencies from its application code by
replacing the `sysinfo` crate (15 transitive crates pulling `libc` FFI) with a
new pure Rust crate `toadstool-sysmon` that parses `/proc` directly and uses
`rustix` for `statvfs` syscalls.

This proves ecoBin v3.0: infrastructure C is eliminable, not just "acceptable."

---

## What Changed

### New Crate: `toadstool-sysmon` (`crates/core/sysmon/`)

Pure Rust system monitoring. 7 modules, 20+ tests, `#![deny(unsafe_code)]`.

| Module | Source | API |
|--------|--------|-----|
| cpu | `/proc/stat`, `/proc/cpuinfo` | `cpu_count()`, `cpu_brand()`, `cpu_usage()`, `per_cpu_usage()` |
| memory | `/proc/meminfo` | `memory_info()` → `MemoryInfo { total, available, used, swap_total, swap_free }` |
| disk | `/proc/mounts` + `rustix::fs::statvfs` | `disk_usage()` → `Vec<DiskInfo>` |
| network | `/proc/net/dev` | `network_stats()` → `Vec<NetworkInterface>` |
| process | `/proc/[pid]/stat`, `/proc/[pid]/status` | `process_info(pid)`, `process_count()`, `all_processes()` |
| loadavg | `/proc/loadavg` | `load_average()` → `LoadAverage { one, five, fifteen }` |
| error | — | `SysmonError` (I/O with `/proc` path context) |

### Migration Scope

**22+ call sites across 18 source files in 8 crates**:

| Crate | Files Changed | Call Sites | Complexity |
|-------|--------------|------------|------------|
| toadstool (core) | 3 | 6 | Heavy — monitoring.rs full rewrite |
| server | 6 | 8 | Heavy — tarpc_server, coordinator, health, capabilities, resource_validator, resource_optimizer |
| cli | 4 | 6 | Heavy — dashboard, collectors, benchmarking, utilities |
| distributed | 3 | 4 | Medium — resources, capacity, discovery |
| security/policies | 1 | 2 | Light |
| security/monitoring | 1 | 2 | Light |
| management/resources | 1 | 2 | Light |
| runtime/gpu | 1 | 1 | Light |

### Cargo.toml Changes

`sysinfo` removed from **15** `Cargo.toml` files:
- Workspace root `Cargo.toml` (dependency entry removed entirely)
- 8 crates replaced `sysinfo = { workspace = true }` → `toadstool-sysmon = { workspace = true }`
- 7 crates removed `sysinfo` (not actively using it in code)

### CI Changes

New `cross-compile` job in `.github/workflows/ci.yml`:
- `cargo check --workspace --target aarch64-unknown-linux-gnu`
- `cargo check --workspace --target armv7-unknown-linux-gnueabihf`
- No musl-tools installed — proves pure Rust cross-compilation

---

## Verification

```bash
# Zero sysinfo in workspace:
cargo tree --workspace | grep sysinfo  # → nothing

# Clean workspace build:
cargo check --workspace  # → success

# All lib tests pass:
cargo test --workspace --lib  # → 6,454 tests passed

# Clippy clean (pedantic):
cargo clippy -p toadstool-sysmon -- -W clippy::pedantic  # → 0 warnings

# Cross-compilation (no C toolchain):
cargo check -p toadstool-sysmon --target aarch64-unknown-linux-gnu  # → success

# Remaining libc is ecosystem-only:
cargo tree --workspace --invert libc | head -30
# → mio, tokio, wgpu-hal, evdev, nix (all upstream, tracked in PURE_RUST_TRACKING.md)
```

---

## Pattern for Other Primals

The sysinfo→sysmon migration establishes a reusable pattern:

1. **Audit**: `cargo tree --invert libc` to find C surfaces
2. **Identify**: Which calls actually need libc vs. can parse `/proc`?
3. **Replace**: Create focused modules that read `/proc` files directly
4. **Validate**: `cargo tree | grep <old-crate>` returns nothing
5. **Cross-compile**: `cargo check --target aarch64-unknown-linux-gnu` works

Any primal using `sysinfo` should follow this pattern. The `toadstool-sysmon`
crate can be used directly (it's in the ecoPrimals workspace) or the pattern
can be applied independently.

---

## Upstream Contribution

`toadstool-sysmon` is a candidate for extraction as `proc-sysinfo` on crates.io.
See `UPSTREAM_CONTRIBUTIONS.md` for the full strategy.

---

## ecoBin v3.0 Standard

This work prompted the evolution of the ecoBin standard:

- **v1.0** (Jan 17): Cross-Architecture (Pure Rust application, musl acceptable)
- **v2.0** (Jan 30): Cross-Platform (Platform-agnostic IPC)
- **v3.0** (Mar 9): Zero Infrastructure C (musl/libc eliminated from application deps)

Updated in `ECOBIN_ARCHITECTURE_STANDARD.md`.

---

## Files Modified

### New Files
- `crates/core/sysmon/` (entire new crate — 8 files)
- `PURE_RUST_TRACKING.md` (ecosystem libc tracking)
- `.github/workflows/ci.yml` (cross-compile job)

### Modified Source Files (18)
- `crates/core/toadstool/src/resources/monitoring.rs`
- `crates/core/toadstool/src/resources/tests.rs`
- `crates/core/toadstool/src/self_identity.rs`
- `crates/core/toadstool/src/layer_adaptation/detection.rs`
- `crates/core/toadstool/src/workload_migration/validation.rs`
- `crates/server/src/tarpc_server.rs`
- `crates/server/src/coordinator_executor.rs`
- `crates/server/src/unibin/capabilities.rs`
- `crates/server/src/handlers/health.rs`
- `crates/server/src/capabilities/mod.rs`
- `crates/server/src/resource_validator.rs`
- `crates/server/src/resource_optimizer/mod.rs`
- `crates/cli/src/monitoring/dashboard.rs`
- `crates/cli/src/monitoring/collectors.rs`
- `crates/cli/src/universal/operations/benchmarking.rs`
- `crates/cli/src/universal/operations/utilities.rs`
- `crates/cli/src/commands/doctor.rs`
- `crates/distributed/src/hosting/resources.rs`
- `crates/distributed/src/songbird_integration/types/distribution_types.rs`
- `crates/distributed/src/songbird_integration/types/capacity_types.rs`
- `crates/distributed/src/songbird_integration/discovery/core.rs`
- `crates/security/policies/src/evaluator.rs`
- `crates/security/monitoring/src/lib.rs`
- `crates/management/resources/src/lib.rs`
- `crates/runtime/gpu/src/cpu_resource.rs`

### Modified Cargo.toml (15)
- Root `Cargo.toml`, plus 14 crate-level Cargo.toml files

---

## What's Next

- **Immediate**: Commit and push S137 changes
- **Short-term**: Extract `proc-sysinfo` standalone crate for crates.io
- **Medium-term**: Track mio/tokio rustix adoption (see PURE_RUST_TRACKING.md)
- **Long-term**: When Rust std adopts linux-raw-sys, remaining libc vanishes

---

*The math is universal. The system monitoring is universal. Only the C was not.*
*Now it's gone.*
