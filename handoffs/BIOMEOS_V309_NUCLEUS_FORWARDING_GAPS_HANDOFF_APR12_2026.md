# biomeOS v3.09 — NUCLEUS Composition Forwarding Gaps Resolved

**Date**: 2026-04-12
**Author**: biomeOS team
**Scope**: 5 gaps blocking full NUCLEUS composition in Docker
**Downstream audit**: primalSpring Phase 34

## Changes

### Gap 1: BTSP client-side handshake for socket forwarding
- `forward_request` now performs full 4-step BTSP client handshake on family-scoped sockets
- Delegates all crypto to BearDog: `x25519_generate_ephemeral`, `crypto.x25519_derive_secret`, `hmac_sha256`
- New `AtomicClient::call_btsp()` public API
- Graceful fallback to raw JSON-RPC when handshake fails or BearDog unavailable
- **Files**: `btsp_client.rs` (+144), `atomic_client/mod.rs` (+41), `atomic_transport.rs` (+19), `forwarding.rs` (+34)

### Gap 2: Method-prefix translation mangling
- `capability.call` no longer re-prefixes multi-segment operations in the no-translation path
- `tensor.stats.mean` → forwards `stats.mean` (not `tensor.stats.mean`) to barraCuda
- **File**: `capability.rs` — None branch checks for dotted operations

### Gap 3: Socket discovery for FAMILY_ID/default
- `get_socket_directories()` now includes `/tmp/biomeos-{BIOMEOS_FAMILY_ID}`, `/tmp/biomeos-{FAMILY_ID}`, and `/tmp/biomeos-default/`
- loamSpine, rhizoCrypt, and other primals discoverable in Docker/NUCLEUS
- **File**: `topology.rs` — 3 new directory tiers

### Gap 4: `ipc.resolve` wired
- Added `("ipc.resolve", Route::CapabilityResolveSingle)` to Neural API route table
- primalSpring can use canonical `ipc.resolve` for capability→endpoint resolution
- **File**: `routing.rs` — 1 line

### Gap 5: `graph.list` path resolution in tcp-only mode
- `graphs_dir` resolved to absolute path at `GraphHandler` construction time
- Prevents relative-path failures when cwd differs from launch dir
- **File**: `graph/mod.rs` — canonicalize relative paths, log when dirs unreadable

## Validation
- `cargo fmt --all -- --check`: PASS
- `cargo clippy --workspace --all-targets -- -D warnings`: PASS (0 warnings)
- `cargo test --workspace`: **7,784 passed, 0 failed**

## primalSpring workaround status
primalSpring currently uses `DirectTcp`/`HttpTcp` routes in `CompositionContext` to bypass all 5 gaps. With v3.09, the canonical biomeOS forwarding path should be functional for downstream springs.
