# petalTongue — Cross-Arch macOS Build Fix

**Date**: April 15, 2026
**Sprint**: petalTongue v1.6.6 (continued)
**Trigger**: primalSpring downstream audit — `cargo check` fails on macOS targets

---

## Audit Finding

> `crates/petal-tongue-ui/src/output_verification.rs:340` — type inference failure
> on `name.to_lowercase()` plus 5 other errors (E0034 ambiguous method, E0592
> conflicting implementations). 6 errors total in `petal-tongue-ui` on macOS targets.
> All Linux targets build successfully (x86_64, aarch64, armv7).

## Root Cause

`AudioCanvas` in `audio_canvas.rs` had an **unconditional** `discover()` method
scanning `/dev/snd` (Linux-specific) in the main `impl AudioCanvas` block, plus a
**second** `discover()` in `#[cfg(target_os = "macos")] impl AudioCanvas`. On macOS,
both `impl` blocks compiled simultaneously, producing E0592 (conflicting method
definitions). This cascaded to E0034 (ambiguous method) at every call site including
`output_verification.rs:340`.

## Fix

### `audio_canvas.rs` — Platform-exclusive method definitions

Moved `discover()` and `is_available()` into mutually exclusive `#[cfg(target_os)]`
`impl` blocks for Linux, macOS, Windows, and a catch-all for unsupported platforms.
The shared methods (`open`, `open_default`, `write_samples`, accessors) remain in the
unconditional `impl AudioCanvas`.

### `proc_stats.rs` — Dead-code warnings on non-Linux

- `CpuStatLine`, its `impl`, `ProcStats` fields, and `page_size()` gated with
  `#[cfg_attr(not(target_os = "linux"), allow(dead_code))]` since they are only
  exercised on Linux
- `std::fs::{self, File}` import moved to `#[cfg(target_os = "linux")]` only

### `display/backends/external.rs` — Unreachable expression

The `None` fallback in `detect_display_server()` was unreachable on macOS/Windows
due to preceding `return` in `#[cfg]` blocks. Gated with
`#[cfg(not(any(target_os = "windows", target_os = "macos")))]`.

## Verification

| Target                   | `cargo check` | `cargo clippy` | Tests |
|--------------------------|---------------|----------------|-------|
| x86_64-unknown-linux-gnu | PASS (0 warn) | PASS (0 warn)  | 6,144 pass |
| x86_64-apple-darwin      | PASS (0 warn) | —              | —     |
| aarch64-apple-darwin     | PASS (0 warn) | —              | —     |

## Files Changed

- `crates/petal-tongue-ui/src/audio_canvas.rs`
- `crates/petal-tongue-ui/src/proc_stats.rs`
- `crates/petal-tongue-ui/src/display/backends/external.rs`
