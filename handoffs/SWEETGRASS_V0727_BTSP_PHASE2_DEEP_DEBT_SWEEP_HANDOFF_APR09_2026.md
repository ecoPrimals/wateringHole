<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# SweetGrass v0.7.27 — BTSP Phase 2, Deep Debt Sweep, Smart Refactoring

**Date**: April 9, 2026
**From**: SweetGrass
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,238 tests, 0 clippy/fmt/doc warnings, all checks green

**Supersedes**: `SWEETGRASS_V0727_LICENSE_ZEROCOPY_API_HARDENING_HANDOFF_APR06_2026.md` (archived)

---

## Summary

Deep debt sweep session completing BTSP Phase 2 (server-side handshake on
accept), smart module refactoring to reduce large files, magic number
elimination with named constants, proptest expansion for store traits, and
capability-based socket resolution for security provider IPC. All showcase
and documentation updated to match current binary API.

---

## Phase 1 — BTSP Phase 2: Server Handshake on Accept

sweetGrass now enforces the BearDog Secure Tunnel Protocol handshake on
incoming connections when `FAMILY_ID` is set and `BIOMEOS_INSECURE` is not `1`.

| Component | File | Purpose |
|-----------|------|---------|
| `btsp/mod.rs` | `sweet-grass-service` | `is_btsp_required()` activation gate |
| `btsp/protocol.rs` | `sweet-grass-service` | Wire types (`ClientHello`, `ServerHello`, etc.) and 4-byte BE length-prefixed framing (16 MiB max) |
| `btsp/server.rs` | `sweet-grass-service` | Server handshake orchestration, crypto delegation to security provider |

### Handshake Flow

1. **ClientHello** → read from wire
2. **`btsp.session.create`** → JSON-RPC to security provider → receives `ServerHello`
3. **ChallengeResponse** → read from wire
4. **`btsp.session.verify`** → JSON-RPC to security provider → receives `HandshakeComplete`
5. Post-handshake: length-prefixed JSON-RPC (replaces newline-delimited)

### Integration

- `uds.rs`: `start_uds_listener_at` checks `is_btsp_required()` at bind time; connections routed to `handle_uds_connection_btsp` or `handle_uds_connection_raw`
- `tcp_jsonrpc.rs`: Same pattern for TCP listeners

### Capability-Based Socket Resolution

Security provider socket resolved as `security.sock` (capability-domain
convention), not `beardog.sock`. Resolution chain:
`SECURITY_PROVIDER_SOCKET` env → `BIOMEOS_SOCKET_DIR/security.sock` → XDG/tmpdir fallback.

This means BearDog, or any future primal providing the security capability,
is discovered by capability domain — no primal name hardcoded.

---

## Phase 2 — Smart Module Refactoring

### `discovery/mod.rs` (613 → 250 lines)

| Extracted File | Contents |
|---------------|----------|
| `discovery/capabilities.rs` | `extract_capabilities()` — parses 5 JSON-RPC response formats for `capabilities.list` |
| `discovery/cached.rs` | `CachedDiscovery` decorator with TTL, LRU eviction, stable ordering |
| `discovery/registry.rs` | `RegistryRpc` tarpc service, `ServiceInfo`, `RegistryDiscovery` with fallback |

Public API unchanged — `mod.rs` re-exports all public items.

### `config/mod.rs` (648 → 567 lines)

| Extracted File | Contents |
|---------------|----------|
| `config/capability.rs` | `Capability` enum — routing abstraction for ecosystem services |

---

## Phase 3 — Hardcoding Elimination

| Constant | Crate | Replaces |
|----------|-------|----------|
| `DEFAULT_BATCH_CONCURRENCY` (10) | `sweet-grass-store` | Magic `20` in `get_batch` |
| `DEFAULT_CURATOR_ROLE_WEIGHT` (0.1) | `sweet-grass-factory` | Magic `&0.1` in `weight_for_role` |

---

## Phase 4 — Proptest Expansion

| Test | Crate | Property |
|------|-------|----------|
| `query_filter_serialization_roundtrip` | `sweet-grass-store` | `QueryFilter` survives serde JSON roundtrip |
| `query_filter_limit_respects_default` | `sweet-grass-store` | Pagination limit falls back to `DEFAULT_QUERY_LIMIT` |

proptest now in 6 crates: core, store, factory, query, compression, integration.

---

## Current State

```
cargo clippy --all-features --all-targets -- -D warnings   ✓ 0 warnings
cargo fmt --all -- --check                                  ✓ clean
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features  ✓ clean
cargo test --all-features --workspace                       ✓ 1,238 passed, 0 failed
```

| Metric | Value |
|--------|-------|
| Version | v0.7.27 |
| Tests | 1,238 |
| .rs files | 161 (44,036 LOC) |
| Max file | 862 lines (limit: 1000) |
| Unsafe blocks | 0 (`#![forbid(unsafe_code)]` workspace-level) |
| License | AGPL-3.0-or-later (scyBorg standard) |
| SPDX headers | 161/161 |
| Wire Standard | Level 3 (Composable) |
| BTSP | Phase 2 — server handshake on UDS + TCP |
| JSON-RPC methods | 28 |

---

## Remaining Debt (None Blocking)

- **BTSP Phase 2 negotiation** — `btsp.negotiate` cipher suite negotiation implemented in `server.rs` but untestable without BearDog implementing the server side of the negotiate method. Ready to activate.
- **aarch64 musl**: Target profile configured but not CI-verified (needs cross-linker in CI runner)
- **Coverage gap**: Postgres store tests require Docker runtime; excluded from llvm-cov
- **`sled` backend**: Optional, unmaintained upstream; `skip-tree` in `deny.toml`; redb is primary
- **`testcontainers` dev chain**: Pulls `bollard` → `rustls` → `ring` (C/ASM); dev-only
- **Remove `BraidSignature` (v0.7.29)**: Deprecated; remove after one release cycle
- **Radiating attribution across ionic bonds**: Derivation chain attribution is live, but cross-NUCLEUS traversal requires ionic bonding protocol (primalSpring Track 4)
- **Showcase scripts**: Some demos reference old CLI flags (`--default-agent`); demos are illustrative, not production paths

---

## Cross-Ecosystem Signals

- **BTSP Phase 2 active**: sweetGrass now enforces handshake when `FAMILY_ID` set. Security provider must be available at `security.sock` in the socket directory. Currently only BearDog implements this role.
- **Capability-domain socket naming**: sweetGrass connects to `security.sock`, not `beardog.sock`. Other primals implementing BTSP Phase 2 should follow the same convention per `CAPABILITY_BASED_DISCOVERY_STANDARD`.
- **Length-prefixed framing**: Post-BTSP connections use 4-byte BE length-prefixed JSON-RPC, not newline-delimited. Clients must match.
- **1,238 tests**: Up from 1,218. New coverage in store traits (proptest), BTSP wire types.
- **161 .rs files / 44,036 LOC**: Up from 151/42,684. New files from BTSP module and smart refactoring extractions.
