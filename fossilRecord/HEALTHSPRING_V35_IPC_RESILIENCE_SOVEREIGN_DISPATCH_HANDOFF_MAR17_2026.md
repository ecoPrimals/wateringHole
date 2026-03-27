# healthSpring V35 — IPC Resilience & Sovereign Dispatch Handoff

**Date**: March 17, 2026  
**From**: healthSpring V35  
**License**: AGPL-3.0-or-later

---

## Summary

healthSpring V35 absorbs cross-ecosystem patterns from airSpring, groundSpring, neuralSpring, and rhizoCrypt into its IPC layer, adds sovereign GPU dispatch via barraCuda's `CoralReefDevice`, and publishes composition guidance for all springs and primals.

## Changes

### 1. Structured IPC Errors (thiserror)

**File**: `ecoPrimal/src/ipc/error.rs`

- `IpcError` enum with 8 variants: `SocketNotFound`, `Connect`, `Write`, `Read`, `Timeout`, `Codec`, `RpcReject`, `EmptyResponse`
- Query helpers: `is_retriable()`, `is_timeout_likely()`, `is_method_not_found()`, `is_connection_error()`
- `DispatchOutcome<T>` enum: `Success`, `Protocol`, `Application` with `should_retry()`
- `try_send()` in `rpc.rs` now returns `Result<serde_json::Value, IpcError>`

### 2. IPC Resilience (CircuitBreaker + RetryPolicy)

**File**: `ecoPrimal/src/ipc/resilience.rs`

- `CircuitBreaker`: `Closed` → `Open` (after N failures) → `HalfOpen` (after cooldown)
- `RetryPolicy`: exponential backoff with configurable max retries, initial delay, max delay
- Pattern absorbed from airSpring v0.8.8 / rhizoCrypt v0.13.0

### 3. 4-Format Capability Parsing

**File**: `ecoPrimal/src/ipc/socket.rs`

`extract_capability_strings()` now handles all ecosystem formats:
- Format A (healthSpring): `{"science": [...], "infrastructure": [...]}`
- Format B (flat): `{"capabilities": ["cap1"]}`
- Format C (nested): `{"capabilities": {"capabilities": ["cap1"]}}`
- Format D (raw array): `["cap1", "cap2"]`
- Format E (result wrapper): `{"result": {"capabilities": [...]}}`

### 4. Property-Based Testing (proptest)

**File**: `ecoPrimal/src/ipc/proptest_ipc.rs`

11 property tests for IPC protocol parsing, including fuzz testing that `extract_capability_strings` never panics on arbitrary JSON.

### 5. Safe Numeric Casts

**File**: `ecoPrimal/src/safe_cast.rs`

- `usize_u32()`, `usize_u64()`, `usize_f64()`, `f64_f32()` — checked conversions
- `CastError` with source/target type information

### 6. Sovereign GPU Dispatch

**File**: `ecoPrimal/src/gpu/sovereign.rs`

- `try_sovereign_dispatch()` routes GPU work through barraCuda `CoralReefDevice`
- Discovers coralReef via `discover_shader_compiler()` at runtime
- Falls back to wgpu path with `strip_f64_enable` if sovereign unavailable
- Feature-gated: `sovereign-dispatch = ["gpu", "barracuda/sovereign-dispatch"]`
- HillSweep implemented as first sovereign op

### 7. Supply Chain Hardening

**File**: `deny.toml`

- `multiple-versions = "deny"` (was "warn")
- `yanked = "deny"` added

### 8. Composition Guidance

**File**: `wateringHole/healthspring/HEALTHSPRING_COMPOSITION_GUIDANCE.md`

Comprehensive document describing:
- healthSpring solo capabilities (79 capabilities, 8 categories)
- Trio combos (rhizoCrypt + sweetGrass + loamSpine)
- Wider primal compositions (barraCuda, toadStool, coralReef, petalTongue, Squirrel, NestGate, BearDog, Songbird, biomeOS)
- Cross-spring compositions (air, neural, wet, ground, hot, ludo)
- Novel multi-primal pipelines (Full NUCLEUS, Cross-Spring Population Health, Real-Time Wearable)

## Verification

- **Tests**: 613 passed, 0 failed (up from 594)
- **Clippy**: Zero warnings (pedantic + nursery, workspace-wide, all targets)
- **Docs**: Zero warnings (RUSTDOCFLAGS="-D warnings")
- **Format**: Zero drift

## Ecosystem Absorption Sources

| Pattern | Source |
|---------|--------|
| `IpcError` + thiserror | airSpring v0.8.8, groundSpring V113 |
| `CircuitBreaker` | airSpring v0.8.8, rhizoCrypt v0.13.0 |
| `RetryPolicy` | airSpring v0.8.8, rhizoCrypt v0.13.0 |
| `DispatchOutcome<T>` | groundSpring V113, wetSpring V99 |
| 4-format capability parsing | neuralSpring S162 |
| proptest IPC fuzzing | airSpring v0.8.8 (22-property pattern) |
| `safe_cast` module | neuralSpring S162 |
| `CoralReefDevice` sovereign dispatch | barraCuda v0.3.5 + coralReef Phase 10 |
| `deny.toml` hardening | rhizoCrypt v0.13.0 |
