# NestGate — Deep Debt Session 40: primalSpring Gap Resolution + Dependency Evolution

**Date:** April 9, 2026
**Primal:** NestGate (storage domain)
**Predecessor:** Session 39 (Apr 8 — BTSP Phase 1, deep audit)

---

## Scope

Resolve all primalSpring audit gaps (NG-01, NG-03, BTSP Phase 2), evolve
external dependencies, eliminate hardcoded string literals, smart-refactor
large files, and audit production stubs for leakage.

---

## primalSpring Gap Resolution

| Gap | Description | Resolution |
|-----|-------------|------------|
| **NG-01** | `InMemoryMetadataBackend` default for metadata axis | `SemanticRouter::new()` returns `Result`; production (`FAMILY_ID` set) errors on `FileMetadataBackend` init failure instead of silent fallback |
| **NG-03** | `data.*` handler stubs with hardcoded NCBI/NOAA/IRIS names | Replaced with single wildcard `data_delegation()` — returns `NotImplemented` directing callers to discover data capability provider at runtime |
| **BTSP Phase 2** | Guard only, no handshake wired into socket accept | Server-side handshake (`btsp_server_handshake.rs`) wired into both `IsomorphicIpcServer` and `JsonRpcUnixServer`, gated by `is_btsp_required()` |

### BTSP Phase 2 implementation detail

- **New module:** `nestgate-rpc/src/rpc/btsp_server_handshake.rs`
- **Wire framing:** 4-byte big-endian length-prefixed JSON frames per `BTSP_PROTOCOL_STANDARD.md`
- **4-step handshake:** ClientHello → ServerChallenge → ClientResponse → ServerAccept
- **Crypto delegation:** All crypto ops (`btsp.session.create`, `btsp.session.verify`, `btsp.negotiate`) delegated to BearDog via `JsonRpcClient::connect_unix`
- **Gate:** `is_btsp_required()` — checks `FAMILY_ID` set AND `BIOMEOS_INSECURE` not "1"/"true"
- **Integration points:** `handle_unix_connection` in both server modules; JSON-RPC loop extracted to reusable `json_rpc_loop` function
- **Feature gate removed:** `btsp_client` module no longer behind `#[cfg(feature = "btsp")]`

---

## Dependency Evolution

| Before | After | Impact |
|--------|-------|--------|
| `uzers` 0.11 (UID/GID retrieval) | `rustix::process::getuid/getgid` | 1 fewer crate in dep tree; `rustix` already present; added `process` feature |
| `async-trait` | **Retained** | All 4 trait defs use `Arc<dyn Trait>` — dyn dispatch requires the macro until `dyn async Trait` stabilizes |
| `async-recursion` | **Retained** | Bounded 1-2 level recursion in fail-safe chain; `Box::pin` would be identical overhead |

### Files changed (uzers → rustix)

- `nestgate-platform/src/platform/uid.rs` — `rustix::process::getuid().as_raw()` / `getgid().as_raw()`
- `nestgate-rpc/src/rpc/isomorphic_ipc/atomic/discovery.rs` — same
- `nestgate-rpc/src/rpc/isomorphic_ipc/atomic/tests.rs` — same
- Workspace `Cargo.toml` — `uzers` commented out, `rustix` `process` feature added
- Crate `Cargo.toml` (nestgate-platform, nestgate-rpc) — `uzers` removed

---

## Hardcoding Elimination

**81 `self.base_url` string literals** across 21 files replaced with proper `format!()` interpolation:

| File | Count | Pattern |
|------|-------|---------|
| `remote/implementation.rs` | 17 | API path segments → `format!("/api/v1/pools/{name}")` |
| `native_real/parsing.rs` | 12 | Error messages → `format!("...{e}")` |
| `pools.rs` | 12 | Pool names → `format!("{pool_name}/...")` |
| `universal_pools.rs` | 7 | Error messages → `{e}`, `{pool_name}` |
| `optimization.rs` | 6 | Dataset paths → `format!("nestpool/workspaces/{workspace_id}")` |
| `storage.rs` | 4 | ZFS property args → `format!("compression={}", ...)` |
| `bidirectional_streams.rs` | 4 | Event IDs → `{counter}` |
| Remaining 14 files | 19 | Various error messages and path constructions |

**Post-fix verification:** `rg '"[^"]*self\.base_url[^"]*"' code/crates --glob '*.rs'` — **0 matches**.

---

## Smart Refactoring

- **`tarpc_server.rs` (635 lines) → directory module:** `tarpc_server/mod.rs` (497 lines) + `tarpc_server/tests.rs` (138 lines)
- **`jsonrpc_server/mod.rs` (777 lines): retained** — size reflects JSON-RPC method registration surface (18 methods); author's `#[expect(clippy::too_many_lines)]` annotation confirms intentional design

---

## Production Stubs Audit

**Result: CLEAN — zero production leakage.**

- All `dev_stubs/` modules gated with `#[cfg(feature = "dev-stubs")]` or `#[cfg(any(test, feature = "dev-stubs"))]`
- No `Cargo.toml` enables `dev-stubs` in `default` features
- `nestgate-bin` does not enable `dev-stubs`
- Parent-module gating (`#[cfg(feature = "dev-stubs")] pub mod basic;`) prevents compilation of stub-dependent children

---

## TODO/FIXME/Debt Marker Audit

**Result: ZERO markers in production `.rs` files.**

`rg '\b(TODO|FIXME|HACK|XXX)\b' code/crates --glob '*.rs'` — 0 matches.

Only `todo!()` appearances are in rustdoc examples (2 files, 3 lines) — not executable code.

---

## Validation

| Check | Result |
|-------|--------|
| `cargo check --workspace` | PASS (0 errors, 0 warnings) |
| `cargo fmt --all --check` | PASS |
| `cargo test -p nestgate-rpc --lib` | 435 passed, 0 failed |
| `cargo test -p nestgate-platform --lib` | 5 passed, 0 failed |
| `cargo test --workspace --all-features` | 2230 passed, 1 flaky (pre-existing test ordering issue, passes in isolation) |

---

## Remaining Work (not in scope for this session)

- Coverage push: 80% → 90% target
- `chrono` → `time`/`jiff` migration (374 uses, 122 files — large cross-crate effort)
- `reqwest` elimination (1 real use in `fetch_external.rs`)
- Multi-filesystem substrate testing
- plasmidBin musl-static rebuild (ecosystem-wide, not NestGate code)
