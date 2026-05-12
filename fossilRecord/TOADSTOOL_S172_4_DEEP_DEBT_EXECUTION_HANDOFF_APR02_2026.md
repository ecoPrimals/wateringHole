# toadStool S172-4 — Deep Debt Execution + wateringHole Compliance

**Date**: April 2, 2026
**Session**: S172-4 (continuation of S172 deep debt)
**Status**: All quality gates green. 21,537 tests, 0 failures.

---

## Summary

Comprehensive deep debt execution across 8 dimensions: wateringHole compliance gaps,
placeholder evolutions, DMA consolidation, IPC naming, capability symlinks, security
client deduplication, and root documentation updates.

## Changes

### wateringHole Compliance (MUST/SHOULD)

| Item | Standard | Status |
|------|----------|--------|
| `identity.get` JSON-RPC method | CAPABILITY_BASED_DISCOVERY v1.1 MUST | **RESOLVED** — implemented on main server + daemon |
| Daemon health canonical names | SEMANTIC_METHOD_NAMING | **RESOLVED** — `health.liveness`/`readiness`/`check` accepted |
| Capability symlinks | CAPABILITY_BASED_DISCOVERY v1.1 SHOULD | **RESOLVED** — `compute.sock` → `toadstool.sock` on bind |
| Neural API naming | CAPABILITY_BASED_DISCOVERY | **RESOLVED** — `ipc.*` → `capability.register`/`resolve`/`find` |

### Deep Debt Evolutions

| Item | Before | After |
|------|--------|-------|
| `CryptoValidator` | Empty unit struct | Signature presence + temporal freshness validation |
| `DelegationValidator` | Empty unit struct | Depth enforcement + delegator/delegatee checks |
| `PermissionRevocationList` | Empty unit struct | `HashSet<Uuid>` backed revocation |
| `SecurityPublicKey` | Empty unit struct | Algorithm + raw key bytes |
| `AccessPolicies` | Empty marker `Copy` type | Real struct: restricted_capabilities, max_delegation_depth, allow_without_provider |
| VFIO DMA | Duplicated in nvpmu + akida-driver | Shared `hw-safe::vfio_dma` module |
| `SecurityClient` RPC methods | 5 near-identical method bodies | Generic `rpc<Req, Resp>()` helper |

### Previous S172 Work (included in this push)

- `syn v1` eliminated from dependency tree (`tarpc` 0.34→0.37, `statrs` 0.16→0.18)
- Blocking-in-async evolution (6 files: `coral_reef_client`, `unix.rs`, `silicon.rs`, `monitoring/lib`, `jsonrpc_server`, `service_discovery`)
- `tokio::sync::RwLock` migration in `SiliconHandler`
- `clippy::await_holding_lock` CI guard added
- Compiled units: 602 → 585, duplicate deps: 71 → 57

## Files Changed

### Server/Handler
- `crates/server/src/pure_jsonrpc/handler/core.rs` — `identity_get()` handler + capabilities list
- `crates/server/src/pure_jsonrpc/handler/mod.rs` — `identity.get` route
- `crates/cli/src/daemon/routes.rs` — `identity.get` + canonical health names

### IPC/Discovery
- `crates/core/toadstool/src/ipc/platform/unix.rs` — capability symlinks on bind
- `crates/core/toadstool/src/ipc_helpers/connection.rs` — `capability.*` Neural API naming

### Crypto/Security
- `crates/distributed/src/crypto_lock/validation.rs` — evolved validators + wired fallback
- `crates/distributed/src/crypto_lock/access_control/types.rs` — `AccessPolicies` real struct
- `crates/distributed/src/crypto_lock/access_control/manager.rs` — default() usage
- `crates/distributed/src/beardog_integration/client_evolved.rs` — generic `rpc()` helper

### Hardware
- `crates/core/hw-safe/src/vfio_dma.rs` — **NEW** shared VFIO DMA module
- `crates/core/hw-safe/src/lib.rs` — vfio_dma re-export

### Documentation
- `DEBT.md` — S172-4 resolved items
- `NEXT_STEPS.md` — updated status line
- `README.md` — updated footer
- `CONTEXT.md` — corrected socket path

## Verification

```
cargo check --workspace            # clean
cargo fmt --check                  # clean
cargo clippy --workspace           # pedantic clean
  --all-targets -- -D warnings -W clippy::pedantic
cargo clippy --workspace --lib     # await_holding_lock clean
  -- -D clippy::await_holding_lock
cargo test --workspace             # 21,537 passed, 0 failed, 220 ignored
```

## Remaining Active Debt

| ID | Crate | Description |
|----|-------|-------------|
| D-TARPC-PHASE3 | integration/protocols | tarpc binary transport not wired |
| D-EMBEDDED-PROGRAMMER | runtime/specialty | Placeholder ISP/ICSP programmer impls |
| D-EMBEDDED-EMULATOR | runtime/specialty | Placeholder MOS6502/Z80 emulator impls |

## IPC Compliance Update

The `IPC_COMPLIANCE_MATRIX.md` rows for toadStool should be updated:
- `health.liveness` / `health.readiness` / `health.check`: **P** (both server + daemon)
- `identity.get`: **P** (both server + daemon)
- `capabilities.list`: **P** (main server)
- Socket path: **P** (`$XDG_RUNTIME_DIR/biomeos/toadstool.sock` + `compute.sock` symlink)

---

Part of [ecoPrimals](https://github.com/ecoPrimals) — sovereign compute for science and human dignity.
