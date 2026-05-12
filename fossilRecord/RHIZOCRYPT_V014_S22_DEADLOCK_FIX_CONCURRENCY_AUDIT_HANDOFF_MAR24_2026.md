<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# rhizoCrypt v0.14.0-dev Session 22 — Production Deadlock Fix, Concurrency Audit, Sleep Elimination

**Date**: March 24, 2026
**From**: AI-assisted session (Cursor Agent)
**To**: Next rhizoCrypt session / ecosystem maintainers
**Status**: Complete
**Supersedes**: `RHIZOCRYPT_V014_S21_DEEP_AUDIT_ARC_DYN_STORE_REFACTOR_HANDOFF_MAR24_2026.md`

---

## Summary

1. **Fixed production RwLock deadlock** in `SongbirdClient::refresh_registration()` — root cause of infinite test hang
2. **Eliminated all sleep-based readiness patterns** in server/service tests — replaced with `Notify`-based signaling
3. **Made rate limiter testable** — switched to `tokio::time::Instant` for time-controlled tests (zero real-time waits)
4. **Made Songbird heartbeat interval configurable** — no more hardcoded 45s in production or test code
5. **Fixed `tracing_subscriber` double-init panic** in `run_server()` integration tests
6. **Cleaned stale version references** across k8s manifests, showcase scripts, and test fixtures

---

## Critical Fix: RwLock Deadlock

**File**: `crates/rhizo-crypt-core/src/clients/songbird/client.rs`

`refresh_registration()` held a read lock on `self.our_endpoint`, then called `register()` which tried to acquire a write lock on the same field. This is a classic RwLock deadlock that would have hung any production heartbeat refresh indefinitely.

**Fix**: Clone the endpoint value before releasing the read lock, then call `register()` without holding any lock.

**Impact**: This was the root cause of the test suite hanging forever (835+ core tests blocked). Tests now complete in ~2 seconds for the core crate.

---

## Code Changes

| File | Change |
|------|--------|
| `crates/rhizo-crypt-core/src/clients/songbird/client.rs` | Fixed RwLock deadlock in `refresh_registration()`; heartbeat uses configurable interval |
| `crates/rhizo-crypt-core/src/clients/songbird/config.rs` | Added `heartbeat_interval: Duration` field (default 45s) |
| `crates/rhizo-crypt-core/src/clients/songbird/tests.rs` | Heartbeat test uses `start_paused = true` + 50ms interval |
| `crates/rhizo-crypt-core/src/clients/songbird/tests_config.rs` | Updated stale version "0.11.0" → "0.14.0" in test fixture |
| `crates/rhizo-crypt-rpc/src/rate_limit.rs` | `std::time::Instant` → `tokio::time::Instant`; test uses `start_paused` + `advance()` |
| `crates/rhizo-crypt-rpc/src/server.rs` | Added `ready_notify`, `wait_ready()`, `ready_notifier()`, `running_flag()` |
| `crates/rhizo-crypt-rpc/Cargo.toml` | Added `test-util` to tokio dev-dependency features |
| `crates/rhizocrypt-service/src/lib.rs` | Added `run_server_with_ready()`; `tracing .init()` → `.try_init()` |
| `crates/rhizocrypt-service/tests/service_integration.rs` | Replaced all `sleep()` calls with readiness notification |
| `k8s/deployment.yaml` | Version 0.13.0 → 0.14.0 |
| `showcase/…/demo-service-mode.sh` | Version 0.13.0 → 0.14.0 |
| `showcase/…/demo-register-presence.sh` | Version 0.11.0 → 0.14.0 |
| `showcase/…/04-sessions/Cargo.lock` | Updated to resolve rhizo-crypt-core 0.14.0-dev |
| `docs/DEPLOYMENT_CHECKLIST.md` | Fixed SPDX file count 125 → 126 |
| `CHANGELOG.md` | Added session 22 entry |

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests (`--all-features`) | **1,387 passing**, 0 failures |
| Tests (default features) | **1,216 passing**, 0 failures |
| Test wall time (`--all-features`) | **~30s** (was: infinite hang) |
| Test wall time (default) | **~14s** |
| Clippy | 0 warnings (pedantic + nursery + cargo, `-D warnings`) |
| `cargo fmt` | Clean |
| `cargo doc --no-deps` | Clean |
| `.rs` files | 126 |
| Lines of Rust | ~44,200 |
| Max file size | 867 lines (limit: 1000) |
| Unsafe blocks | 0 |
| TODO/FIXME/HACK markers | 0 |

---

## Patterns Available for Absorption

### `Notify`-based Server Readiness (replaces `sleep(100ms)`)

```rust
let server = RpcServer::new(primal, addr);
let ready = server.ready_notifier();
let handle = tokio::spawn(async move { server.serve().await });
ready.notified().await; // instant, no sleep
```

### `tokio::time::Instant` for Testable Rate Limiting

Switch from `std::time::Instant` to `tokio::time::Instant`. Tests use `#[tokio::test(start_paused = true)]` and `tokio::time::advance()` for zero-latency time simulation.

### Configurable Heartbeat Intervals

Any spawned periodic task should take its interval from config, not hardcode it. Tests use short intervals with paused time to verify behavior instantly.

### `try_init()` for Tracing Subscriber

Always use `.try_init()` instead of `.init()` for `tracing_subscriber` in library/integration code. `.init()` panics on double-call; `.try_init()` is idempotent.

---

## What Other Primals Should Know

- **RwLock deadlock pattern**: Any code that holds a read lock and calls a method that write-locks the same field will deadlock. Clone/drop the guard before calling nested methods. This applies to all `Arc<RwLock<T>>` patterns in the ecosystem.
- **Sleep-based readiness is a production bug**: If your tests sleep to wait for server startup, they will be flaky and slow. Use `Notify`, `watch::channel`, or `AtomicBool` polling instead.
- **`tokio::time::Instant` vs `std::time::Instant`**: Use `tokio::time::Instant` in any code that needs to be testable with time control. Add `test-util` to tokio dev-dependencies.

---

## Verification

```bash
cargo fmt --all -- --check          # clean
cargo clippy --all-targets --all-features -- -D warnings  # 0 warnings
cargo doc --no-deps                 # clean
cargo test --workspace --all-features  # 1,387 pass, 0 fail, ~30s
cargo test --workspace              # 1,216 pass, 0 fail, ~14s
```

---

## Previous Handoff

[RHIZOCRYPT_V014_S21_DEEP_AUDIT_ARC_DYN_STORE_REFACTOR_HANDOFF_MAR24_2026.md](./RHIZOCRYPT_V014_S21_DEEP_AUDIT_ARC_DYN_STORE_REFACTOR_HANDOFF_MAR24_2026.md)
