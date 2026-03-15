# barraCuda v0.3.5 — GPU Streaming & Comprehensive Audit Handoff

**Date**: 2026-03-15
**Primal**: barraCuda v0.3.5
**Chat**: [GPU streaming audit](1470fd53-d411-4148-bcd8-292dbc49aadc)

---

## Executive Summary

Comprehensive audit and GPU streaming refactor. The GPU submission pipeline was
blocking the CPU for up to 120 seconds after every dispatch due to a single lock
held across both `queue.submit()` and `device.poll(Wait)`. With 16-thread
nextest, this caused lock-convoy stalls and test hangs.

Three architectural fixes eliminate the blocking:

1. **Lock split** — submit and poll now use separate `gpu_lock` acquisitions
2. **Fire-and-forget** — 279 non-readback ops migrated from blocking
   `submit_and_poll` to non-blocking `submit_commands`
3. **Single-poll readback** — new `submit_and_map<T>` collapses the old
   double-poll (submit+poll then map+poll) into one `poll_safe` cycle

Additionally: `--all-features` clippy fixed (sovereign-dispatch compiles),
codebase audit confirms zero debris.

---

## Changes

### GPU Submission Pipeline (P1)

| Before | After |
|--------|-------|
| `submit_and_poll_inner`: single lock held across submit + poll(Wait 120s) | Split into `submit_commands_inner` (lock → submit → unlock) + `poll_wait_inner` (lock → poll → unlock) |
| 279 fire-and-forget ops: `submit_and_poll()` blocks CPU after every dispatch | `submit_commands()` — non-blocking submit, GPU work executes async |
| Readback: `submit_and_poll()` + `map_staging_buffer()` = 2 polls | `submit_and_map<T>()` = submit → `map_async` → 1 `poll_safe` |
| `read_buffer<T>`: `submit_and_poll_inner` + `map_staging_buffer` | Uses `submit_and_map` internally — single poll |

**Files changed**: `device/wgpu_device/mod.rs`, `device/wgpu_device/buffers.rs`,
~350 op files across `ops/`, `optimize/`, `gpu_executor/`, `linalg/`, `staging/`.

### `--all-features` Clippy Fix

- Added `is_coral_available()` to `coral_compiler/mod.rs` — synchronous
  discovery probe for `CoralReefDevice::new()`
- Added `CoralReefDevice::with_auto_device()` — creates device with IPC
  auto-detection
- Added `CoralReefDevice::has_dispatch()` — toadStool dispatch availability

### Codebase Audit Results

| Category | Finding |
|----------|---------|
| Archive dirs/files | None |
| Dead scripts | None (`test-tiered.sh` is active) |
| TODO/FIXME/HACK/XXX in production | None |
| .bak/.old/.tmp/.orig files | None |
| Files over 1000 lines | None (max ~794) |
| Invalid Cargo.toml paths | None |
| Hardcoded primal names/ports | None in production (test-only `127.0.0.1:5000` in discovery assertions) |
| `println!`/`eprintln!` in library code | None in production (all in `#[cfg(test)]` modules) |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all --check` | Green |
| `cargo clippy --workspace --all-targets -- -D warnings` | Green |
| `cargo clippy --workspace --all-features` | Green (dead_code warnings for in-progress sovereign dispatch only) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Green |
| `cargo test --workspace --lib` | **3,407 passed, 0 failed** (~27s) |

---

## Cross-Primal Impact

**None.** All changes are internal to barraCuda's GPU submission layer.
No IPC protocol changes, no API changes for consumers.

The `is_coral_available`, `with_auto_device`, and `has_dispatch` additions
enable `--all-features` compilation but do not change runtime behavior for
consumers not using the `sovereign-dispatch` feature.

---

## For toadStool

No action required. The `submit_commands` path does not change the dispatch
interface. When toadStool's `compute.dispatch.submit` IPC is live,
`CoralReefDevice::has_dispatch()` will probe it.

## For Springs

No action required. Springs that `cargo add barracuda` see faster GPU test
execution due to the fire-and-forget migration. The `Tensor` API is unchanged.

---

## Files of Interest

- `crates/barracuda/src/device/wgpu_device/mod.rs` — lock split implementation
- `crates/barracuda/src/device/wgpu_device/buffers.rs` — `submit_and_map<T>` method
- `crates/barracuda/src/device/coral_compiler/mod.rs` — `is_coral_available()`
- `crates/barracuda/src/device/coral_reef_device.rs` — `with_auto_device()`, `has_dispatch()`
- `CONTRIBUTING.md` — updated GPU concurrency rules
