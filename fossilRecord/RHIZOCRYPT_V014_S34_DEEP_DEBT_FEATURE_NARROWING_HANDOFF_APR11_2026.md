# rhizoCrypt v0.14.0-dev — Session 34: Deep Debt Feature Narrowing Handoff

**Date:** 2026-04-11
**Primal:** rhizoCrypt
**Context:** Deep debt cleanup, compile efficiency, primal-agnostic evolution

---

## Summary

Comprehensive deep debt audit and cleanup across all dimensions:
mocks, unsafe, hardcoding, dependencies, large files, idiomatic Rust, coverage.

## Audit Results (Clean Areas — No Action Needed)

| Area | Finding |
|------|---------|
| **Mocks** | All behind `#[cfg(test)]` or `test-utils` feature. Zero production mocks. |
| **Unsafe** | Zero `unsafe` blocks. `forbid(unsafe_code)` on non-test builds. |
| **TODOs** | Zero in production code. |
| **Idiomatic Rust** | Clean from prior session sweeps. No anti-patterns found. |
| **Large Files** | All under 1000 LOC. `handler.rs` (583) well-structured, no split needed. |
| **Duration Literals** | All centralized in `constants.rs`. Only test code has inline values. |
| **Cross-Primal Refs** | No hardcoded primal URLs. Discovery is capability-based. |

## Changes Made

### 1. Feature Flag Narrowing (Compile Efficiency)

| Dependency | Before | After | Dropped |
|-----------|--------|-------|---------|
| `tokio` | `"full"` | `rt-multi-thread, macros, net, sync, time, io-util, signal, fs` | `io-std`, `parking_lot`, `process`, `tracing` |
| `tarpc` | `"full"` | `serde-transport-bincode, tcp` | JSON transport, Unix transport |
| `hyper` | `"full"` | `http1, client, server` | HTTP/2 |

Also deduplicated `bincode` spec in `rhizo-crypt-core` to `workspace = true`.

### 2. Primal-Agnostic Naming

`loamspine_http.rs` error/log strings neutralized:
- `"LoamSpine rejected commit"` → `"Permanent storage provider rejected commit"`
- `"Health check response from LoamSpine"` → `"Health check response from permanent storage provider"`

### 3. Coverage Expansion (+31 Tests)

| Module | Tests Added | Coverage Areas |
|--------|-------------|----------------|
| `service_types.rs` | 8 | Capability descriptors, OnceLock caching, DTO serialization |
| `btsp/types.rs` | 10 | Protocol constants, cipher serde, handshake messages, errors |
| `songbird/config.rs` | 9 | Defaults, env parsing, address config, capability advertise |
| `discovery/endpoint.rs` | 4 | Empty capabilities, clone, static/owned service IDs |

## Code Health

- **1,502 tests** passing (`--all-features`)
- **~93%** line coverage (`llvm-cov`)
- **Zero** clippy warnings (pedantic + nursery)
- **Zero** unsafe blocks, TODOs, production mocks
- All dependencies pure Rust (ecoBin compliant)

## For primalSpring Gap Registry

- **Feature narrowing**: Applicable pattern for all primals using tokio/tarpc/hyper "full"
- **Primal-agnostic naming**: LoamSpine strings neutralized; all other cross-primal refs are doc/test only
