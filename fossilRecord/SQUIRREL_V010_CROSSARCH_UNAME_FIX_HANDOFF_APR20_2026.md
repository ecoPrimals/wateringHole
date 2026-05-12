# Squirrel v0.10 — Cross-Arch `uname()` Fix (April 20, 2026)

## Problem

`primalSpring` audit flagged: **`universal-constants` crate fails `cargo check`
on macOS and Android targets**. Linux builds were unaffected.

Root cause: `rustix::system::uname()` returns `Uname` directly (infallible) in
rustix 1.x, but the code used `if let Ok(u) = rustix::system::uname()` — a
pattern from the 0.38.x API where it returned `Result<Uname>`. The code was
behind `#[cfg(all(unix, not(target_os = "linux")))]`, so it never compiled on
Linux — only surfaced when cross-checking macOS/Android targets.

## Fix

```rust
// Before (rustix 0.38 pattern — broken on 1.x):
if let Ok(u) = rustix::system::uname() {
    let s = u.nodename().to_string_lossy().into_owned();
    ...
}

// After (rustix 1.x — infallible):
let s = rustix::system::uname()
    .nodename()
    .to_string_lossy()
    .into_owned();
if !s.is_empty() {
    return Ok(s);
}
```

Also added doc comments for the three non-Linux stub functions
(`process_rss_mb`, `uptime_seconds`, `system_cpu_usage_percent`) that were
triggering `missing_docs` warnings on cross-platform builds.

## File Changed

| File | Change |
|------|--------|
| `crates/universal-constants/src/sys_info.rs` | Fix `uname()` call + add stub docs |

## Verification

- `cargo check -p universal-constants --target aarch64-apple-darwin` — **pass**
- `cargo check -p universal-constants --target x86_64-apple-darwin` — **pass**
- `cargo check -p universal-constants --target aarch64-linux-android` — **pass**
- `cargo clippy --workspace -- -D warnings` — **0 warnings**
- `cargo fmt --all -- --check` — **clean**
- `cargo test --workspace` — **7,165 passing**

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,165 |
| Coverage | 90.1% |
| `.rs` files | ~1,035 |
| Lines | ~336k |
| Production files >800L | 0 |
