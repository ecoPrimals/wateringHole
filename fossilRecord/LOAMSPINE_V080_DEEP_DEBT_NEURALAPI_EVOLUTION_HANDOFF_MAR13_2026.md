<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# LoamSpine v0.8.0 — Deep Debt & NeuralAPI Evolution Handoff

**Date**: March 13, 2026
**Primal**: LoamSpine (permanence layer)
**Version**: 0.8.0
**Type**: Deep debt evolution, NeuralAPI integration, production hardening

---

## Summary

Comprehensive deep debt pass on LoamSpine covering error propagation, canonical serialization, NeuralAPI ecosystem integration, provenance trio type bridging, and production code hardening. All quality gates green: 610 tests passing, zero clippy warnings, zero unsafe, zero C dependencies.

---

## What Changed

### NeuralAPI Integration (biomeOS Orchestration)

LoamSpine now participates in the biomeOS ecosystem via NeuralAPI:

- **`neural_api.rs`** module: 19 semantic capabilities registered (`permanence`, `commit.session`, `braid.commit`, `certificate.mint`, `health.check`, `capability.list`, etc.)
- **Lifecycle wiring**: `LifecycleManager::start()` registers with NeuralAPI via Unix socket IPC (non-fatal if unavailable); `stop()` deregisters
- **UniBin subcommands**: `loamspine capabilities` (JSON output) and `loamspine socket` (XDG-resolved path)
- **Transport layer**: `NeuralApiTransport` in `transport/neural_api.rs` for JSON-RPC over length-prefixed Unix sockets

Socket path resolution: `$XDG_RUNTIME_DIR/biomeos/neural-api.sock` (standard) or `/tmp/biomeos/neural-api.sock` (fallback).

### Provenance Trio Type Bridge

`trio_types.rs` provides explicit wrapper types for cross-primal data:

| Type | Purpose | Conversions |
|------|---------|-------------|
| `EphemeralSessionId` | rhizoCrypt session → LoamSpine | `TryFrom<uuid::Uuid>`, `TryFrom<String>` |
| `BraidRef` | sweetGrass braid → LoamSpine | URN parsing (`urn:braid:uuid:...`) |
| `EphemeralContentHash` | rhizoCrypt hash → LoamSpine | `TryFrom<EntryHash>` |
| `TrioCommitRequest` | Cross-primal commit envelope | Aggregates session + braid + content hash |
| `TrioCommitReceipt` | Permanence confirmation | Returns spine_id + entry_hash + timestamp |

### Canonical Serialization Evolution

`Entry::to_canonical_bytes()` evolved from JSON + `unwrap_or_default()` to:
- **bincode** for compact, deterministic serialization
- Metadata keys sorted via `BTreeMap` before serialization (HashMap ordering is non-deterministic)
- Returns `LoamSpineResult<Vec<u8>>` with proper error propagation
- All 20+ call sites updated: `compute_hash()`, `hash()`, storage layers, proof generation, backup verification

### Production Error Propagation

All `unwrap_or_default()` patterns eliminated from production code:

| Location | Before | After |
|----------|--------|-------|
| `entry.rs` `to_canonical_bytes` | `serde_json::to_vec().unwrap_or_default()` | `bincode::serialize().map_err(LoamSpineError::Serialization)` |
| `transport/neural_api.rs` POST body | `serde_json::to_string().unwrap_or_default()` | `.map_err(LoamSpineError::Serialization)?` |
| `cli_signer.rs` path handling | `Path::to_str().unwrap_or_default()` | `.ok_or_else(\|\| LoamSpineError::Internal(...))` |
| `neural_api.rs` network lengths | `u32 as usize` | `usize::try_from().map_err(...)` |

### Deprecated Code Removal

- Removed `pub use discovery_client as songbird` alias (deprecated since v0.7.0, zero consumers)
- `MockTransport` gated behind `#[cfg(any(test, feature = "testing"))]` (was `#[allow(dead_code)]`)

### JSON-RPC API Extensions

| Method | Purpose |
|--------|---------|
| `commit.session` | Semantic alias for `session.commit` (biomeOS routing) |
| `capability.list` | Returns primal capabilities as JSON (Spring-as-Niche standard) |

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 549 | 610 (+61) |
| Source files | 66 | 78 |
| JSON-RPC methods | 22 | 24 (+2) |
| `unwrap_or_default()` in production | 4 | 0 |
| `u32 as usize` network casts | 3 | 0 |
| Deprecated re-exports | 1 | 0 |
| Max file size | 863 | 899 (all < 1000) |
| Clippy warnings | 0 | 0 |
| Unsafe code | 0 | 0 |
| C dependencies | 0 | 0 |

---

## Inter-Primal Notes

### biomeOS
- LoamSpine now registers 19 capabilities with NeuralAPI at startup. biomeOS can route `commit.session`, `braid.commit`, `capability.list` etc. to LoamSpine's Unix socket.
- Socket path follows XDG standard: `$XDG_RUNTIME_DIR/biomeos/neural-api.sock`.
- Registration is non-fatal -- LoamSpine runs standalone if biomeOS is unavailable.

### rhizoCrypt
- `trio_types::EphemeralSessionId` bridges rhizoCrypt's UUID session IDs to LoamSpine's internal format.
- `permanent-storage.commitSession` compat layer unchanged and stable.
- Future: migrate to `session.commit` or `commit.session` for cleaner naming.

### sweetGrass
- `trio_types::BraidRef` handles URN-format BraidId parsing (`urn:braid:uuid:...`).
- `braid.commit` pathway stable with inclusion proof verification.
- `TrioCommitRequest` provides a structured envelope for cross-primal commits.

### ludoSpring
- Full pipeline testable: game session → rhizoCrypt dehydration → LoamSpine permanence → sweetGrass attribution.
- `capability.list` enables ludoSpring to discover LoamSpine's capabilities at runtime.

### All Primals
- `loamspine capabilities` CLI command enables CI/CD and orchestration tooling to inspect primal capabilities without starting the service.
- `loamspine socket` enables scripts and health checks to locate the IPC endpoint.

---

## Quality Gates

```
cargo fmt --all -- --check           ✅ clean
cargo clippy -D warnings             ✅ 0 warnings (all targets)
cargo test --workspace               ✅ 610 passed, 0 failed
cargo doc --workspace -D warnings    ✅ compiles
cargo deny check                     ✅ licenses, bans, sources pass
```

---

**Handoff by**: LoamSpine deep debt + NeuralAPI evolution session
