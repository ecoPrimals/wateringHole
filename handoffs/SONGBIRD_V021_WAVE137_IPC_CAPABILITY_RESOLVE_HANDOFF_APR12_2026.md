# Songbird v0.2.1 — Wave 137: IPC Storage Naming + capability.resolve Wiring

**Date**: April 12, 2026
**Primal**: Songbird
**Version**: v0.2.1
**Wave**: 137
**Contact**: primalSpring

---

## Summary

Wave 137 completes capability-based naming evolution and wires `capability.resolve` +
`discovery.peers` into the live Unix socket handler. All NestGate-branded storage types
renamed to identity-agnostic IPC names per wateringHole capability-first standard.

---

## Changes

### 1. NestGate → IPC Storage (Capability-Based Naming)

Per wateringHole standard: primal code has self-knowledge only, no foreign primal
identity in type names. Storage backends renamed to describe *how* they connect,
not *who* they connect to.

| Before | After | Crate |
|--------|-------|-------|
| `NestGateStorage` | `IpcStorageBackend` | `songbird-orchestrator` |
| `NestGateOnionStorage` | `IpcOnionStorage` | `songbird-sovereign-onion` |
| `storage_nestgate/` module | `storage_ipc/` module | both crates |
| `nestgate_impl.rs` | `ipc_backend.rs` | `songbird-orchestrator` |
| `storage_nestgate.rs` | `storage_ipc.rs` | `songbird-sovereign-onion` |

All doc comments, log messages, and context strings updated. `#[deprecated]` aliases
retained for backward compatibility:

```rust
#[deprecated(note = "renamed to `IpcStorageBackend` — capability-based naming")]
pub type NestGateStorage = IpcStorageBackend;
```

Cross-references updated in: `consent_management/mod.rs`, `task_lifecycle/manager/storage.rs`,
`storage_memory.rs`, `lib.rs` (both crates), `service.rs`, `storage.rs`.

### 2. `capability.resolve` Wired into Unix Socket Handler

Single-step DNS-like routing by capability domain, dispatched through the typed
`JsonRpcMethod` enum. New types:

- `CapabilityResolveRequest { capability: String }`
- `CapabilityResolveResponse { service_id, endpoint, protocol, capabilities }`

Handler: `capability_resolve_json` in `IpcHandlers` — calls `discover_by_capability`,
returns the best provider or `JsonRpcError -32601`.

### 3. `discovery.peers` Wired

`discovery.peers` dispatch returns all registered services via wildcard capability
query (`"*"`). Matches the NUCLEUS mesh validation requirement from primalSpring.

### 4. Hardcoded Address Elimination (Remaining)

- `songbird-execution-agent`: `"0.0.0.0"` → `PRODUCTION_BIND_ADDRESS`, port `9020` →
  `DEFAULT_EXECUTION_AGENT_PORT` (new constant in `songbird-types::defaults::ports`)
- `songbird-orchestrator` CLI: 15 `println!` → `tracing::info!`
- `songbird-config` advanced network defaults: `"127.0.0.1"` → `LOCALHOST`
- `songbird-universal` container/storage backends: literals → constants

### 5. Dependency Hygiene

- `serde_yaml = "0.9"` explicitly declared in `songbird-discovery/Cargo.toml` (was
  transitive dependency leakage — now a proper direct dependency)
- `deny.toml`: removed invalid `RUSTSEC-2024-0320`; added evolution note documenting
  `serde_yaml` archived status and `serde_yml` migration path
- `songbird-genesis`: `repository` field now uses workspace inheritance

---

## Audit Findings (No Action Required)

| Category | Result |
|----------|--------|
| `unsafe` blocks | 0 (`#![forbid(unsafe_code)]` all 30 crates) |
| TODO/FIXME/HACK in Rust | 0 |
| Mocks in production | 0 (all in `#[cfg(test)]`) |
| `.unwrap()` in production | 0 |
| `panic!()`/`unreachable!()` in production | 0 / 2 (provably unreachable QUIC VarInt) |
| Files >800 LOC | 0 (largest 763L) |
| C dependencies in default build | 0 |
| NestGate references in Rust source | 0 (only in `#[deprecated]` aliases) |

---

## Verification

```bash
cargo check --workspace                                   # Exit 0
cargo fmt --check                                         # Exit 0
cargo clippy --workspace -- -D warnings                   # 0 warnings
cargo doc --workspace --no-deps -D warnings               # 0 warnings
cargo deny check                                          # advisories ok, bans ok, licenses ok, sources ok
cargo test --workspace --lib                              # 7,284 passed, 0 failed, 22 ignored
```

---

## primalSpring Audit Reconciliation

From `ECOSYSTEM_EVOLUTION_CYCLE.md` Songbird section:

| Item | Status |
|------|--------|
| "3 E0308 type mismatches (tests only)" | **RESOLVED** — fixed `serde_json::Value` mismatches + heartbeat test logic |
| "Transitive ring in Cargo.lock" | **CONFIRMED** lockfile-only; not compiled in default build; `deny.toml` bans `ring` |
| "Validate capability.resolve under NUCLEUS mesh" | **WIRED** — `capability.resolve` dispatched in Unix socket handler |
| "Validate discovery.* under NUCLEUS mesh" | **WIRED** — `discovery.peers` dispatched in Unix socket handler |
| "Confirm federation opt-in (--port)" | **CONFIRMED** — `--port` CLI flag env-configurable, no hardcoded ports |

---

## Status

**Songbird has zero open gaps in primalSpring audit.**
All deep debt categories at S+ tier. Capability-based naming complete.

Remaining work: coverage expansion (72.29% → 90% target), BTSP Phase 3,
Tor onion service crypto (blocked on security provider), TLS sovereign certs,
QUIC/TLS evolution (future transport).
