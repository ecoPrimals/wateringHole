# songBird — Windows Platform Gate Fix (P0, G1 Blocker)

**Date**: Jul 29, 2026 | **Wave**: 155i | **From**: eastGate overwatch
**Priority**: **P0** — blocks G1 (Tower on Windows) and all downstream Windows work
**Reported by**: blueGate Tower Atomic AAR

---

## The Problem

songBird's orchestrator has a compile-time platform gate that rejects Windows
entirely before evaluating `--listen`/`--bind` flags. blueGate deployed Tower
Atomic on Windows — bearDog and skunkBat work fine over TCP, but songBird
exits immediately with:

```
IPC server requires Unix domain sockets... On Windows use WSL2
```

This fires from `#[cfg(not(unix))]` in the orchestrator server init, **before**
the `--listen` and `--bind` flags are evaluated. The TCP and named pipe
transport code already exists in `songbird-universal-ipc` but isn't wired
into the orchestrator startup path.

## What Already Works

`songbird-universal-ipc` has complete Windows transport implementations:

| Module | Status | Lines |
|--------|--------|-------|
| `platform/unix.rs` | Production | ~200 |
| `platform/android.rs` | Production | ~150 |
| `platform/windows.rs` | **Written, not wired** | 341 |
| `platform/fallback.rs` | **Written, not wired** | 156 |

bearDog proves the pattern: `--bind-mode tcp --port 9100` works on Windows
with 200+ JSON-RPC methods responding. songBird should follow the same
TCP fallback approach.

## Where to Fix

**Primary**: `songbird-orchestrator/src/app/core/mod.rs` ~lines 474-486

The `start_ipc_server` function gates on `cfg!(not(unix))` and returns an
error before checking if `--listen` (TCP address) was provided. The fix:
only error if `!cfg!(unix) && listen_addr.is_none()` — if a TCP address is
specified, use the TCP transport path.

**Secondary**: `virtual_relay.rs:188` — same `#[cfg(not(unix))]` bail pattern.

## Proposed Fix

```rust
// In start_ipc_server:
// BEFORE (blocks all non-Unix):
#[cfg(not(unix))]
return Err(anyhow!("IPC server requires Unix domain sockets..."));

// AFTER (allow TCP/named pipes on Windows):
#[cfg(not(unix))]
if listen_addr.is_none() && !cfg!(windows) {
    return Err(anyhow!("IPC server requires Unix domain sockets or --listen"));
}
// On Windows: prefer named pipes if available, fall back to TCP via --listen
```

Wire the existing `platform/windows.rs` named pipe transport as the default
on Windows, with `platform/fallback.rs` TCP as the fallback when named pipes
aren't configured.

## Expected Outcome

After fix, songBird should start on Windows with:
```
songbird server --port 7700 --bind 0.0.0.0 --listen 127.0.0.1:9901
```

This unblocks:
- `tower.health` and `tower.mesh_status` on Windows
- Discovery beacons and inter-primal IPC
- `mesh.gate_enroll` for Windows gates
- ACME HTTP-01 challenge responder
- Full Tower Atomic validation (G1 completion)
- Downstream Nest Atomic and Node Atomic on blueGate

## What Overwatch Already Fixed

These items from blueGate's AAR were already resolved by overwatch before
the Tower deployment:

- primalSpring colon-in-filename: 6 files renamed (pushed to Forgejo)
- Windows Phase 0+1 prerequisites added to startup blurb
- springs/helixVision removed from workspace layout
- sporePrint noted as empty placeholder
- Windows depot bins documentation updated

---

*P0: songBird platform gate blocks G1 on Windows. Transport code exists in
universal-ipc (windows.rs + fallback.rs) but isn't wired into orchestrator.
bearDog TCP proves the pattern works. Fix is narrow — gate logic in
start_ipc_server + virtual_relay.*
