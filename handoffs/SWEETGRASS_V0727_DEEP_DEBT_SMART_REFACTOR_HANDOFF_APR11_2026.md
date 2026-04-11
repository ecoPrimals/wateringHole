# sweetGrass v0.7.27 — Deep Debt Sweep + Smart Refactoring

**Date**: April 11, 2026
**Primal**: sweetGrass v0.7.27
**Commits**: 045774e (SG-02/TCP opt-in), dfcc8d2 (smart refactoring)
**Trigger**: Comprehensive deep debt sweep and primalSpring audit response

---

## Summary

Two-phase deep debt evolution: (1) Provenance Trio audit response resolving
SG-02, TCP opt-in, BTSP DI refactor, and Postgres/BTSP coverage expansion;
(2) comprehensive codebase audit and smart refactoring of all files >500 LOC.

---

## Phase 1: Trio Audit Response

### SG-02: `--socket` CLI Flag (RESOLVED)
`Commands::Server` now accepts `--socket <PATH>` (env: `SWEETGRASS_SOCKET`),
plumbed to `start_uds_listener_at()` / `cleanup_socket_at()`.

### Tower Atomic TCP Opt-in
`--port` changed from `u16` (default 0, always-on) to `Option<u16>`.
TCP JSON-RPC only starts when `--port` is explicitly provided.
All three Provenance Trio primals are now UDS-first, TCP opt-in.

### BTSP DI Refactor
New `perform_server_handshake_with(stream, security_socket)` — DI-friendly
variant avoids `unsafe set_var` (edition 2024, `forbid(unsafe_code)`).
4 integration tests with mock BearDog in `btsp_mock_beardog.rs`.

### Postgres Error-Path Coverage
Connection-refused, config boundary, and `ValidatedFilter` tests exercise
error paths without Docker.

---

## Phase 2: Deep Debt Audit + Smart Refactoring

### Comprehensive Audit (all clean)
- **Dependencies**: `cargo deny check` all clear; sqlx postgres-only; no C/FFI in production
- **Unsafe code**: Zero blocks, `forbid(unsafe_code)` workspace-level
- **`#[allow]`**: Only `demo.rs` — evolved to `#![expect(clippy::too_many_lines)]`
- **Hardcoded names/ports**: Zero in production; all env/CLI/config based
- **Mocks**: All properly `#[cfg(test)]` or `feature = "test"` gated
- **String ownership**: Public APIs use `impl Into<String>` or `&str`
- **TODO/FIXME/HACK**: Zero markers
- **`Box<dyn>`**: Only legitimate trait objects and recursive async

### Smart Module Splits (5 files)

| File | Before | After | Method |
|------|--------|-------|--------|
| `handlers/braids.rs` | 677 | 310 | Tests → `braids/tests.rs` |
| `handlers/health.rs` | 579 | 294 | Tests → `health/tests.rs` |
| `config/mod.rs` | 579 | 369 | Subsystem configs → `subsystems.rs` |
| `traits.rs` | 570 | 360 | Tests → `traits/tests.rs` |
| `resilience.rs` | 561 | 324 | Tests → `resilience/tests.rs` |

### Sled Store Clone Reduction
`.clone()` calls reduced 25→11 via `braid_index_trees()` helper,
`Arc::clone()` for clarity, and borrowing where possible.

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,315 |
| .rs files | 167 (44,516 LOC) |
| Max file | 734 lines (test file) |
| Max production file | 574 lines |
| Clippy | 0 warnings |
| Fmt | PASS |
| `cargo deny` | All clear |
| `#[allow]` instances | 0 (1 `#![expect]` in demo.rs) |
| Unsafe blocks | 0 |
| TODO/FIXME/HACK | 0 |

---

## Ecosystem Impact

### For Compliance Matrix
- SG-02 **RESOLVED** — `--socket` CLI flag implemented
- TCP opt-in aligned with rhizoCrypt/loamSpine (Tower Atomic)
- BTSP coverage significantly expanded (mock BearDog integration)

### For Trio Partners
- `perform_server_handshake_with` DI pattern recommended for adoption
- TCP opt-in means springs must pass `--port` to enable TCP

### Remaining Known Gaps
| Gap | Status | Notes |
|-----|--------|-------|
| Postgres CI coverage | Deferred | Needs Docker in CI |
| BTSP Phase 3 (encrypted framing) | Not started | Ecosystem-wide |
| `async-trait` → native RPITIT | Blocked | Traits used as `dyn` objects |
| `sled` deprecation | Feature-gated | `redb` is primary; sled optional |
