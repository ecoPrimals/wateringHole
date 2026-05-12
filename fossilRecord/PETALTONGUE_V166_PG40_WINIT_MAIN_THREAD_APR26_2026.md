# petalTongue v1.6.6 — PG-40: winit Main-Thread Panic Fix

**Date**: April 26, 2026
**Primal**: petalTongue v1.6.6
**Audit ref**: primalSpring Phase 45b — PG-40 (Tier 1)
**Status**: RESOLVED

## Problem

`petaltongue live` and `petaltongue ui` crashed immediately on Linux:

```
thread 'tokio-rt-worker' panicked at winit-0.30.13:
"Initializing the event loop outside of the main thread is a significant
cross-platform compatibility hazard."
```

**Root cause**: `main()` was `#[tokio::main] async fn main()`, which runs on the
tokio executor. Both `ui_mode::run()` and `live_mode::run()` called
`tokio::task::spawn_blocking(run_ui_blocking)`, executing eframe on a tokio worker
thread — not the actual main thread. winit 0.30 (used by eframe 0.29) enforces
main-thread event loop initialization on Linux (X11/Wayland).

## Fix

Restructured `main()` to build the tokio runtime manually:

1. **`fn main()`** — no longer `#[tokio::main]`. Creates `Runtime::new()` explicitly.
2. **Async setup** (config, data service, discovery) runs via `runtime.block_on()`.
3. **GUI modes** (`Ui`, `Live`): eframe runs directly on the main thread.
   - `ui_mode::run_on_main_thread()` — calls `run_ui_blocking` synchronously.
   - `live_mode::run_on_main_thread()` — spawns IPC server on `runtime.spawn()`,
     motor drain on `std::thread::spawn()`, discovery refresh on `runtime.spawn()`,
     then runs eframe on the main thread (blocks until window close).
4. **Non-GUI modes** (`tui`, `web`, `headless`, `server`, `status`): dispatch via
   `runtime.block_on(dispatch_async(...))` — unchanged behavior.

## Additional: PETALTONGUE_SOCKET env var binding

- `--socket` flag on `server` and `live` commands now reads `PETALTONGUE_SOCKET`
  env var as fallback via clap's `env` attribute.
- Socket path priority: `--socket flag > PETALTONGUE_SOCKET env > XDG default`.
- clap `env` feature added to workspace dependency.

## Files Changed

| File | Change |
|------|--------|
| `src/main.rs` | Replace `#[tokio::main]` with manual runtime, add `dispatch_async()`, `PETALTONGUE_SOCKET` env on socket args |
| `src/live_mode.rs` | `run_on_main_thread()` replaces `pub async fn run()` |
| `src/ui_mode.rs` | `run_on_main_thread()` replaces `spawn_blocking` path |
| `src/error.rs` | `#[expect(dead_code)]` on `TaskPanic` (no longer constructed in prod) |
| `Cargo.toml` | clap `env` feature added |
| `CHANGELOG.md` | PG-40 entry added |

## Verification

- `cargo clippy --workspace --all-features` — 0 warnings
- `cargo test --workspace --all-features` — 98 suites, 0 failures
- `cargo check --target x86_64-apple-darwin` — passes (macOS cross-check)
