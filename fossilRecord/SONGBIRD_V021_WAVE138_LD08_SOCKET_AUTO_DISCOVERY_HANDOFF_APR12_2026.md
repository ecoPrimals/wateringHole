# Songbird v0.2.1 — Wave 138 Handoff: LD-08 Socket Auto-Discovery

**Date**: April 12, 2026  
**Primal**: Songbird  
**Wave**: 138  
**Issue**: LD-08 — `ipc.resolve` returns empty because registry starts empty

---

## Problem

`ipc.resolve` and `capability.resolve` accept both `primal_id` and `capability` parameters (LD-02, Wave 137b), but return "not found" for all primals because none call `ipc.register` at startup. The service registry is empty — the wire-level protocol works but has no data to resolve against.

## Solution: Option (b) — Socket Directory Auto-Discovery

Rather than requiring every primal to self-register (which would need launcher coordination or changes to all primals), Songbird now scans the biomeos socket directory on startup and auto-registers what it finds.

### How It Works

1. **Stage 2c** (`stage_2c_socket_auto_discovery`) runs after servers are started
2. Scans `$XDG_RUNTIME_DIR/biomeos/*.sock` and `/tmp/biomeos/*.sock`
3. Skips Songbird's own sockets (`songbird.sock`, `network.sock`, and family-suffixed variants)
4. For each remaining socket, probes with:
   - `identity.get` (Wire Standard L3) → extracts `primal` name
   - `capabilities.list` → extracts capability tokens
   - Falls back to socket filename for name extraction
5. Registers each primal with its capabilities into the broker's `ServiceRegistry`
6. `ipc.resolve`, `capability.resolve`, `ipc.discover`, `lifecycle.composition` all now have data

### Architecture Changes

- **Registry sharing**: `start_broker_with_discovery` now returns `SharedServiceRegistry` (the broker's registry Arc). Startup captures it and passes it to auto-discovery.
- **`IpcServiceHandler::registry()`** accessor added for downstream access.
- **Startup pipeline**: 8 → 9 stages (new Stage 2c between IGD auto-configure and federation self-registration).
- **Platform-aware**: `#[cfg(unix)]` / `#[cfg(not(unix))]` — non-Unix platforms skip gracefully.

### Files Changed

| File | Change |
|------|--------|
| `songbird-orchestrator/src/primal_discovery/socket_auto_discovery.rs` | **New** — scan, probe, register logic + 7 tests |
| `songbird-orchestrator/src/primal_discovery/mod.rs` | Added `socket_auto_discovery` module |
| `songbird-orchestrator/src/primal_discovery/tcp_biomeos.rs` | `list_biomeos_sock_paths` → `pub(super)` |
| `songbird-orchestrator/src/app/startup_orchestration.rs` | Stage 2c, pipeline constant updated |
| `songbird-orchestrator/src/app/core/mod.rs` | `broker_registry` field on orchestrator |
| `songbird-orchestrator/src/ipc/universal_broker.rs` | Registry sharing, `SharedServiceRegistry` type |
| `songbird-universal-ipc/src/service/construction.rs` | `IpcServiceHandler::registry()` accessor |

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | 0 errors, 0 warnings |
| `cargo clippy --workspace -D warnings` | 0 warnings |
| `cargo fmt --check` | Clean |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace --lib` | 7,298 passed, 0 failed, 22 ignored |

---

## Ecosystem Impact

- **Springs**: `ipc.resolve({"capability": "crypto.sign"})` now returns live results when security provider socket exists in biomeos dir
- **BearDog**: Its existing `ipc.register` call to Songbird will **update** the auto-discovered entry (or succeed if auto-discovery already found it)
- **NUCLEUS mesh**: `capability.resolve` and `discovery.peers` now return populated data from the scan
- **Resilience**: Works regardless of primal startup order — late-arriving primals can still call `ipc.register`, and Songbird can be extended with periodic rescan if needed

## Remaining Debt (from primalSpring audit)

- **BTSP Phase 3**: Cipher negotiation, encrypted framing, multi-frame sessions
- **Tor/TLS**: Blocked on live security provider (`CryptoUnavailable` stubs)
- **Storage validation**: Needs live `storage.*` provider
- **Coverage**: 72.29% → 90% target
- **`ring` lockfile ghost**: Documented in `deny.toml`, not compiled
- **`async_trait`**: ~160 usages, all require `dyn Trait` dispatch
