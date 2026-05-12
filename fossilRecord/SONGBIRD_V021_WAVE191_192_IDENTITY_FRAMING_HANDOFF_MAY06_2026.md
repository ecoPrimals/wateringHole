# Songbird v0.2.1 — Waves 191–192 Handoff

**Date**: May 6, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Waves**: 191–192  
**Status**: Complete — pushed

---

## Wave 191: `ipc.register` Identity Verification & Protocol Hardening

### Changes
1. **Identity verification on registration**: `handle_register` now probes the registering primal's endpoint via `identity.get` (async NDJSON). Hard-rejects spoofed primal names (identity mismatch). Falls back to trust-on-first-use when endpoint is unreachable (handles primals still starting up).
2. **Whitespace-tolerant protocol detection**: UDS multiplexer in `connection.rs` now skips leading ASCII whitespace before classifying the first meaningful byte as JSON-RPC (`{`) or binary BTSP.
3. **BufReader post-negotiate safety**: Explicit safety documentation in `connection.rs` and `bin_interface/server.rs` confirming Songbird is NOT affected by the barraCuda/coralReef BufReader bug class (BufReader is passed through, never `into_inner()`'d).

### Files Changed
- `songbird-universal-ipc/src/service/ipc_registry.rs` — `verify_registrant_identity()`, `probe_identity()`
- `songbird-orchestrator/src/ipc/pure_rust_server/server/connection.rs` — whitespace skip, safety docs
- `songbird-orchestrator/src/bin_interface/server.rs` — safety docs

---

## Wave 192: Sovereign Onion Frame Guard & Stale Import Cleanup

### Changes
1. **Memory-bomb prevention**: Added `MAX_ONION_FRAME` (16 MiB) size validation in `sovereign-onion/service.rs` before allocating buffers from untrusted `u32` wire-frame lengths. Returns error instead of OOM-panicking on oversized frames.
2. **Stale `use std::future::Future` removed** from `btsp/provider.rs` — trait already uses inline `std::future::Future` path in RPITIT signatures (the correct pattern when `Send` bounds are needed).

### Files Changed
- `songbird-sovereign-onion/src/service.rs` — `MAX_ONION_FRAME` constant + validation
- `songbird-network-federation/src/btsp/provider.rs` — stale import removal

---

## Verification
- 0 clippy warnings (`-D warnings`)
- `cargo fmt --check` clean
- All workspace lib tests pass
- All sovereign-onion (69), network-federation (132), tower_atomic (44) tests pass

---

## Remaining Debt (Post-Wave 192)
- Coverage 73.41% → 90% target (I/O-heavy paths)
- `Result<_, String>` in JSON-RPC handler layer (trait constraint — architectural)
- Transitive duplicate deps blocked on upstream (kube, tarpc, derivative)
- Tor/TLS crypto blocked on live security provider
- `bincode` 1.x (RUSTSEC-2025-0141) — blocked on tarpc upstream
