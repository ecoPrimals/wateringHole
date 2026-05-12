# biomeOS v3.18 — Spring Audit Fixes Handoff

**Date:** 2026-04-20
**From:** biomeOS team
**Triggered by:** primalSpring v0.9.16 consolidated audit (5 springs, NUCLEUS validation)

---

## Resolved Issues

### 1. `biomeos-types` missing `secret` module — source build fails (wetSpring)

**Root cause:** `.gitignore` contained `*secret*` to prevent committing credential files, but this also excluded `crates/biomeos-types/src/manifest/storage/secret.rs` — a legitimate Rust source module declaring `SecretSpec`, `SecretMetadata`, `SecretType`, `SecretData`, and `SecretProvider`.

The file existed on the author's machine (untracked) and `mod.rs` declared `pub mod secret;` + `pub use secret::*;`, so local builds passed. Fresh clones failed with **E0583: file not found for module `secret`**.

**Fix:**
- Added negation rules to `.gitignore`: `!**/secret.rs` and `!**/secret/`
- Tracked `secret.rs` (150 LOC, AGPL-3.0 header, `serde` derives, no external deps)
- Verified `cargo check -p biomeos-types` passes on clean tree

### 2. TCP port binding conflicts (primalSpring)

**Root cause:** `ExecutionContext::next_tcp_port()` used a bare `AtomicU16::fetch_add(1)` starting at 9900. When two biomeOS instances ran simultaneously, or when external services occupied ports in the 9900+ range, child primals failed on `TcpListener::bind`.

**Fix:**
- `next_tcp_port()` now trial-binds each candidate port before returning it
- Occupied ports are skipped with a `tracing::debug` log
- Guard against counter exhaustion (>65500)
- New test: `test_next_tcp_port_skips_occupied_ports` verifies skip behavior

### 3. Running primals not auto-registered with Neural API (ludoSpring)

**Root cause:** After `spawn_primal_process` + `wait_for_socket`/`wait_for_tcp_port`, the primal was running but its capabilities were never probed and registered with the `NeuralRouter`. Discovery was:
- **One-shot at boot** (`discover_and_register_primals`)
- **Single lazy UDS rescan** on first `capability.call` miss
- **No post-spawn registration**

Primals spawned after boot discovery (graph execution, resurrection) were invisible to `capability.call` routing.

**Fix:**
- Added `NeuralRouter::register_spawned_primal(name, socket_path, tcp_port)` — probes capabilities via UDS or TCP and registers them with source `"post-spawn"`
- Added `ExecutionContext::neural_router` field (optional `Arc<NeuralRouter>`) with `with_neural_router()` builder
- Integrated post-spawn registration in `node_handlers::primal_launch` (graph execution path)
- Integrated post-spawn registration in `ResurrectionManager::respawn_primal` (lifecycle path)
- Made `discovery_init` module `pub(crate)` for TCP probe reuse

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | Pass |
| `cargo clippy --workspace --all-targets` | 0 warnings |
| `cargo test --workspace` | All pass, 0 failures |
| `cargo fmt --all -- --check` | Clean |

---

## For Springs

- **wetSpring:** `cargo build` from fresh clone should now succeed. Verify `biomeos-types` compiles.
- **primalSpring:** TCP port collisions should no longer occur in parallel test/deployment scenarios. The 9900+ base is still the default but occupied ports are skipped.
- **ludoSpring:** Primals spawned via graph execution or resurrection are now auto-registered. For primals started externally, `capability.register` JSON-RPC or `topology.rescan` remain the registration paths.

---

## Files Changed

| File | Change |
|------|--------|
| `.gitignore` | Added `!**/secret.rs`, `!**/secret/` negation rules |
| `crates/biomeos-types/src/manifest/storage/secret.rs` | Now tracked (was gitignored) |
| `crates/biomeos-atomic-deploy/src/executor/context.rs` | Port-availability check in `next_tcp_port()`, `neural_router` field |
| `crates/biomeos-atomic-deploy/src/neural_router/mod.rs` | `register_spawned_primal()` method |
| `crates/biomeos-atomic-deploy/src/executor/node_handlers.rs` | Post-spawn registration call |
| `crates/biomeos-atomic-deploy/src/lifecycle_manager/resurrection.rs` | Post-spawn registration call |
| `crates/biomeos-atomic-deploy/src/neural_api_server/discovery_init.rs` | `pub(crate)` TCP probe wrapper |
| `crates/biomeos-atomic-deploy/src/neural_api_server/mod.rs` | `discovery_init` visibility to `pub(crate)` |
