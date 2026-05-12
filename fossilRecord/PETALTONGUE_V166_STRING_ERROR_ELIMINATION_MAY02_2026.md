# petalTongue v1.6.6 — String Error Elimination Handoff

**Date**: May 2, 2026
**Phase**: Deep Debt — Typed Error Evolution
**Scope**: Elimination of all `Result<_, String>` patterns in production code

---

## Summary

Comprehensive sweep of the petalTongue codebase identified **string-based error
propagation** (`Result<_, String>`, `Err(format!(...))`) as the single remaining
category of deep debt. All 13 affected modules have been evolved to typed
`thiserror` enums with structured, machine-readable error variants.

---

## Changes by Module

### IPC Crate (`petal-tongue-ipc`)

| Module | Before | After | Variants |
|--------|--------|-------|----------|
| `provenance_trio.rs` | `Result<Value, String>` | `ProvenanceRpcError` | Connect, Serialize, Io, Parse, RpcError, NoResult |
| `physics_bridge.rs` | 5 fns with `String` | `ComputeBridgeError` | SocketNotFound, Connect, Serialize, Io, Parse, Send(Box<Self>), ComputeError |
| `audio.rs` (RPC) | `Result<String, String>` | `WavEncodeError` | Hound (from hound::Error) |

### Core Crate (`petal-tongue-core`)

| Module | Before | After | Variants |
|--------|--------|-------|----------|
| `graph_builder/builder.rs` | `Result<(), String>` | `GraphEdgeError` | SourceNotFound, TargetNotFound, Duplicate |
| `event.rs` | `Result<usize, String>` | `SendError<EngineEvent>` | Direct tokio broadcast type |
| `capability_taxonomy.rs` | `FromStr::Err = String` | `ParseCapabilityError` | Single variant with input string |
| `biomeos_discovery/backend.rs` | `Result<(), String>` | `WebSocketBridgeError` | Connect, Protocol, ClosedByServer, StreamEnded |

### UI Crate (`petal-tongue-ui`)

| Module | Before | After | Variants |
|--------|--------|-------|----------|
| `status_reporter/reporter.rs` | `Result<String, String>` | `serde_json::Error` | Direct serde type |
| `startup_audio.rs` | 4 fns with `String` | `StartupAudioError` | AudioCanvas, FileRead, Decode |
| `data_source.rs` | 3 fns with `String` | `DataSourceError` | Discovery, Topology, LockPoisoned |
| `sandbox_provider.rs` | 3 fns with `String` | `SandboxError` | NotFound, Read, Parse, DirNotFound, CurrentDir |
| `audio/backends/network.rs` | `Result<(), String>` | `NetworkAudioError` | Connect, Serialize, Io, Parse, RemoteError |
| `tool_integration.rs` | `Result<(), String>` | `ToolActionError` | Single variant with message |

---

## Codebase Audit Results

The sweep confirmed petalTongue is clean on all other axes:

- **Zero files >800 lines** (max 714 lines)
- **Zero unsafe code** (`forbid(unsafe_code)` on all 18 crates)
- **Zero TODO/FIXME/HACK** markers
- **Zero `.unwrap()`/`.expect()` in production code**
- **All mocks properly `#[cfg(test)]`-gated**
- **Zero `-sys` dependencies** in Cargo.toml
- **Zero stale scripts, temp files, or debris**

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo clippy --workspace --all-features -- -D warnings` | 0 warnings |
| `cargo fmt --all -- --check` | 0 violations |
| `cargo test --workspace --all-features` | 6,191 passed, 0 failed |
| `cargo deny check bans` | Clean |
| `cargo doc --workspace --no-deps` | 0 warnings |

---

## Next Evolution Targets

- BTSP Phase 3 cipher negotiation (pending BearDog client-side + sourDough scaffold)
- Coverage expansion toward 95% (current ~90%)
- EVOLVED comment cleanup (optional editorial — ~10 instances across UI crate)
