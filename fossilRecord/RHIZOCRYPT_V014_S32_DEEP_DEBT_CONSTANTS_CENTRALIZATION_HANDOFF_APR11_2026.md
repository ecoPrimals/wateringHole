<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# rhizoCrypt v0.14.0-dev (Session 32) — Deep Debt Cleanup, Constants Centralization, Cohesion Refactoring

**Date**: April 11, 2026
**From**: rhizoCrypt
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,470 tests, 0 clippy/fmt/doc warnings, ~93% line coverage

**Supersedes**: `RHIZOCRYPT_V014_S31_BTSP_PHASE2_DEEP_DEBT_HANDOFF_APR09_2026.md`

---

## Summary

Full deep debt cleanup pass responding to `primalSpring` downstream audit
findings on Provenance Trio IPC stability (session 31½) and comprehensive
codebase evolution: constants centralization, cohesion-based file refactoring,
clone reduction, dependency evolution, coverage expansion, and idiomatic
Rust 2024 modernization.

---

## Phase 1 — Trio IPC Stability (Session 31½, Completed)

Addressed in the prior half-session (see `RHIZOCRYPT_V014_S31_BTSP_PHASE2_DEEP_DEBT_HANDOFF_APR09_2026.md` + incremental):

| Item | Status | Detail |
|------|--------|--------|
| RC-01 (UDS transport) | **Resolved** | Dual-mode TCP + UDS since session 23; `--unix` flag |
| TCP graceful shutdown | **Resolved** | `tokio::sync::watch` channel + `tokio::select!` accept loop |
| Connection limiting | **Resolved** | `tokio::sync::Semaphore` on both TCP and UDS (default 1000) |
| Composition load testing | **Resolved** | 50-client concurrent TCP + UDS stress tests |
| Max line length DoS | **Resolved** | `MAX_JSONRPC_LINE_LENGTH` (16 MiB) pre-parse guard |

---

## Phase 2 — Constants Centralization (Hardcoding → Agnostic)

### Problem

9 production files contained hardcoded timeouts, magic numbers, and capability
strings duplicating values that should live in `constants.rs`. Drift risk under
composition: if `CONNECTION_TIMEOUT` changes in constants, the loamspine HTTP
client and HTTP adapter wouldn't follow.

### 17 New Constants

| Constant | Value | Derivation |
|----------|-------|------------|
| `DEFAULT_GC_INTERVAL` | 60s | Session GC cadence |
| `DEFAULT_EXPIRATION_GRACE` | 1h | Post-timeout dehydration window |
| `DEFAULT_ATTESTATION_TIMEOUT` | 60s | Dehydration attestation |
| `DEFAULT_DEHYDRATION_RETRY_DELAY` | 5s | Retry between attestation attempts |
| `DEFAULT_MAX_PAYLOAD_BYTES` | 1 GiB | Per-session payload ceiling |
| `DEFAULT_SESSION_MAX_DURATION` | 1h | Individual session TTL |
| `DEFAULT_RETRY_MAX_BACKOFF` | 2s | IPC retry backoff cap |
| `CIRCUIT_BREAKER_FAILURE_THRESHOLD` | 5 | IPC circuit breaker trips |
| `CIRCUIT_BREAKER_COOLDOWN` | 30s | Matches `CONNECTION_TIMEOUT` |
| `DEFAULT_HEARTBEAT_INTERVAL` | 45s | Discovery registration refresh |
| `DEFAULT_HEALTH_CHECK_INTERVAL` | 30s | Endpoint health probe |
| `ADVERTISED_CAPABILITIES` | 5 entries | Single source for Songbird registration |
| `LOCALHOST_HOSTNAME` | `localhost` | HTTP Host header for UDS |

### Files Migrated

`config.rs`, `session.rs`, `loamspine_http.rs`, `adapters/http.rs`,
`adapters/unix_socket.rs`, `songbird/config.rs`, `discovery/endpoint.rs`,
`resilience.rs` (both `CircuitBreaker::default_ipc` and `RetryPolicy::default_ipc`)

---

## Phase 3 — Cohesion-Based File Refactoring

### `service.rs` → `service.rs` + `service_types.rs`

Wire types (DTOs) and capability descriptor builder extracted to
`service_types.rs` (222 LOC). `service.rs` retains the tarpc trait and server
implementation (485 LOC, down from 687). Rationale: types change independently
from RPC behavior, improving compile-time boundaries.

### `store.rs` Backend Dispatch Macro

114 lines of repetitive `match self { Memory(s) => …, Redb(s) => … }` in
`impl DagStore for DagBackend` replaced with `dispatch_backend!` macro.
Same behavior, fewer lines, trivially extensible when adding backends.

---

## Phase 4 — Clone Reduction & Dependency Evolution

- `cached_capability_descriptors()` returns `&'static [CapabilityDescriptor]`
  instead of `&'static Vec<_>` — eliminates allocation per `capabilities.list`
- Removed unused `toml` workspace dependency
- Confirmed: stack is already ecoBin-compliant (zero application C deps,
  `deny.toml` bans openssl/ring/reqwest/sqlite). No C/FFI in production paths.

---

## Phase 5 — Coverage Expansion (+9 Tests)

| Module | Tests Added | Gap Closed |
|--------|-------------|------------|
| `btsp/mod.rs` | 5 | `read_family_seed` (4 env variants) + `is_btsp_required` dev mode |
| `jsonrpc/uds.rs` | 4 | `socket_path` accessor, idempotent cleanup, sequential requests, parent dir creation |

---

## Phase 6 — Idiomatic Rust 2024

| File | Before | After |
|------|--------|-------|
| `safe_env/mod.rs` | `.map(…).unwrap_or(false)` | `.is_ok_and(…)` |
| `config.rs` | `.map(…).unwrap_or(true)` | `.map_or(true, …)` |
| `rhizocrypt/mod.rs` | `for`/`push` loop in `gc_sweep` | `.filter().map().collect()` |
| `store.rs` | Double-nested scope + redundant `drop()` | Flat scope, explicit `drop` only where needed |

---

## Code Health Snapshot

| Metric | Value |
|--------|-------|
| Tests | 1,470 passing |
| Coverage | ~93% lines (`llvm-cov`) |
| Clippy | 0 warnings (pedantic + nursery + cargo) |
| Max file | 664 LOC (`loamspine_http.rs`) |
| `.rs` files | 147 |
| TODOs | 0 in production code |
| Unsafe | 0 blocks, `deny` workspace-wide |
| `cargo deny` | Clean (advisories, bans, licenses, sources) |

---

## Mocks Audit

All `Mock*` types are behind `#[cfg(any(test, feature = "test-utils"))]` —
never compiled in default production builds. `MockSongbirdServer` is strictly
`#[cfg(test)]`. The `test-utils` feature is only enabled by the fuzz harness,
never in production dependency chains.

---

## Impact on Ecosystem

### For Trio Partners (loamSpine, sweetGrass)

- All IPC constants are now centralized; if values change, downstream clients
  inherit via `rhizo-crypt-core::constants::*`
- `ADVERTISED_CAPABILITIES` array is the single source for Songbird registration
- Connection limits (semaphore-based) protect both TCP and UDS under load

### For Springs

- `capabilities.list` returns `&'static` slice — no per-call allocation
- All magic numbers evolved to named constants with derivation docs
- Zero hardcoded primal names in production code (confirmed by scan)

### For primalSpring Gap Registry

- **RC-01**: Fully resolved (UDS + TCP dual-mode, graceful shutdown, connection limiting)
- **GAP-06 (ludoSpring V41)**: Should be marked **CLOSED** — UDS has been shipping since session 23
- **Composition load**: 50-client concurrent TCP + UDS tests passing

---

## Distribution

All Springs · All Primals · biomeOS · primalSpring (gap registry update)
