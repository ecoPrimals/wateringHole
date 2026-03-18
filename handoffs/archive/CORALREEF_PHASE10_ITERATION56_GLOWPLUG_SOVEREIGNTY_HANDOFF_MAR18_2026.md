<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Phase 10 — Iteration 56 Handoff

**Date**: March 18, 2026  
**Primal**: coralReef  
**Phase**: 10 — Spring Absorption + Compiler Hardening  
**Iteration**: 56

---

## Summary

GlowPlug security hardening, chaos/fault/penetration testing, circuit
breaker and nvidia/DRM runtime guards, Titan V boot sovereignty via
kernel-level driver preemption, and boot safety validation. Resolved
repeated kernel panics caused by nvidia's open kernel module probing
GV100 hardware without GSP support.

## Changes

### Security Hardening (coral-glowplug socket.rs)

- **BDF validation**: `validate_bdf()` rejects path traversal (`../`), null bytes, shell metacharacters, and malformed BDF strings before any sysfs access
- **Connection limiting**: `MAX_CONCURRENT_CLIENTS = 64` enforced via `tokio::sync::Semaphore` in accept loop
- **Idle timeout**: `CLIENT_IDLE_TIMEOUT = 30s` — idle connections are dropped automatically
- **Max request line**: `MAX_REQUEST_LINE_BYTES = 65536` — prevents memory exhaustion from oversized requests

### Chaos, Fault, and Penetration Testing (+27 tests → 131 total)

- JSON fuzzing: malformed JSON, empty objects, null params, Unicode edge cases
- Connection chaos: rapid connect/disconnect, parallel flood, half-close, oversized requests
- BDF injection: path traversal (`../../etc/shadow`), null bytes, shell metacharacters, SQL-style payloads
- Method probing: unknown methods, empty methods, system.* reflection attempts
- Repeated shutdown resilience: 10x rapid shutdown cycles

### Circuit Breaker (health.rs)

- `CIRCUIT_BREAKER_THRESHOLD = 6` consecutive faults trips the breaker
- Once tripped: BAR0 MMIO reads halted, only safe sysfs power state checks performed
- Prevents kernel instability from repeated reads on nvidia-corrupted hardware

### nvidia Module Guard (device.rs, health.rs)

- `swap()` and `resurrect_hbm2()` refuse operations when `/sys/module/nvidia` exists
- Health loop auto-resurrection blocked when nvidia modules loaded — counter still climbs toward circuit breaker
- Prevents driver rebind attempts that cause kernel panics on GV100

### DRM Consumer Guard (device.rs)

- `activate()` and `release()` check `sysfs::has_active_drm_consumers()` before driver unbind
- Returns `DeviceError::ActiveDrmConsumers` if active DRM clients detected
- Prevents kernel crash from unbinding GPUs with active display sessions

### Boot Sovereignty (scripts/boot/)

- `coralreef-dual-titanv.conf`: `softdep nvidia pre: vfio-pci` forces vfio-pci to load before nvidia
- `options vfio-pci ids=10de:1d81 disable_idle_d3=1` claims both Titan V GPUs at module load time
- `vfio-pci.ids=10de:1d81` added to kernel cmdline via `kernelstub`
- initramfs rebuilt to embed modprobe configuration
- `99-coralreef-vfio.rules`: udev rules for post-VFIO-bind permissions and power management
- `deploy-boot.sh`: automated deployment script for all boot configs

### Boot Safety Validation (main.rs)

- `validate_boot_safety()` runs at coral-glowplug startup
- Checks `/proc/cmdline` for `vfio-pci.ids`
- Warns if nvidia module is bound to managed devices
- Validates `driver_override` settings for all configured devices

### Error Hierarchy (error.rs)

- `ActiveDrmConsumers` variant added to `DeviceError`
- Full JSON-RPC 2.0 error code mapping for all device errors

## Metrics

| Metric | Before (Iter 55) | After (Iter 56) |
|--------|-------------------|------------------|
| Tests passing | 2394 | 2527 (+133) |
| Glowplug tests | 72 | 131 (+59) |
| Line coverage | 60.89% | ~64% |
| Region coverage | 60.32% | ~63% |
| Function coverage | 69.72% | ~72% |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Fmt drift | 0 | 0 |
| Kernel panics | Frequent (18-23 min post-boot) | 0 (stable across reboots) |

## CI Gates

All green: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo doc --no-deps`, `cargo test --workspace`.

## Root Cause: Kernel Panics

nvidia's open kernel module (580.126.18) probes ALL nvidia PCI devices at
boot. GV100 (Titan V) has no GSP — it uses a PMU Falcon microcontroller.
The nvidia driver's GSP initialization path fails on Volta, leaving hardware
registers in a corrupted state. When vfio-pci subsequently binds and
coral-glowplug reads BAR0 registers for health checks, the corrupted state
triggers PCIe errors that escalate to kernel panics.

**Fix**: Three-layer defense:
1. **Boot preemption** — vfio-pci claims Titan V before nvidia loads
2. **Circuit breaker** — halts BAR0 reads after persistent faults
3. **nvidia module guard** — blocks driver swaps when nvidia.ko is loaded

## Cross-Primal Impact

- **hotSpring**: VFIO stability improved — no more kernel panics during device management. Boot sovereignty ensures clean hardware state for hotSpring's GPU pipeline.
- **toadStool**: glowplug JSON-RPC API unchanged — existing `device.get`, `device.swap`, `device.health`, `device.resurrect` methods work identically. New input validation may reject previously-accepted malformed BDF strings.
- **barraCuda**: No impact — compiler and driver APIs unchanged. VFIO dispatch benefits from stable hardware state.

## Next Steps

- Coverage ~64% → 90% (continue test expansion)
- Custom PMU Falcon firmware for GV100 in Rust (Phase 2 sovereignty)
- Sovereign HBM2 training via coral-driver typestate machine
- Vendor-agnostic GPU abstraction layer
