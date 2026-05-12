# BearDog v0.9.0 — Wave 33: Deep Debt Cleanup & Evolution

**Date**: April 9, 2026
**Primal**: BearDog (BD)
**Domain**: Security / Crypto
**Phase**: BTSP Phase 2+3 complete (reference implementation)

---

## Summary

Wave 33 closes the remaining deep debt items from the primalSpring audit and pushes coverage past the 90% threshold.

## Changes

### T8: `#[allow()]` → `#[expect(reason)]` Migration
- 193 → 75 `#[allow(` (62% reduction)
- 361 → 476 `#[expect(` with contextual `reason` strings
- Where `expect` caused `unfulfilled_lint_expectations`, kept `allow` with documented `reason`

### T10: Standalone Startup Fix
- `NODE_ID` / `BEARDOG_NODE_ID` no longer required for startup
- Missing values generate `standalone-{uuid}` via `OnceLock`, logged once
- PRIMAL IPC Protocol v3.1 degraded/standalone mode compliant

### T4: Dynamic `ipc.register` with Songbird
- Server startup spawns non-blocking registration task
- Uses self-knowledge for capability tags (not hardcoded)
- Exponential backoff on failure; standalone mode continues
- Heartbeat loop maintained while connected

### T1: Commented-Out Code Cleanup
- 313-line orphan block removed from beardog-types
- Smaller blocks removed across 15+ files
- Total commented-out code: 0

### T8: PII Cleanup
- `/home/user/...` paths replaced with `$HOME/...` in test files and builder
- PII scanner clean: 0 hits

### BD-01: Per-Field Encoding Hints (Resolved)
- `crypto.verify_ed25519` accepts `message_encoding`, `signature_encoding`, `public_key_encoding`
- Semantic aliases: `crypto.ed25519.sign`, `crypto.ed25519.verify`

### Coverage Push
- 90.16% → 90.51% line coverage
- New tests across beardog-production, beardog-cli, beardog-compliance, beardog-config, beardog-core

### Smart Refactoring
- `runtime.rs` (1244→360 lines): extracted secrets.rs, defaults.rs, runtime_tests.rs
- `socket_config.rs` (1111→668 lines): test extraction to socket_config_tests.rs
- 0 files over 1000 LOC

## Gate Table

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy` (pedantic+nursery) | 0 warnings |
| `cargo test --workspace` | 14,593+ pass, 0 fail |
| `cargo llvm-cov` | 90.51% line |
| `cargo deny check` | 4/4 pass |
| Files > 1000 LOC | 0 |
| TODO/FIXME | 0 |
| `#[allow(` / `#[expect(` | 75 / 476 |
| PII hits | 0 |
| Commented-out code | 0 |

## Ecosystem Impact

- **BTSP Phase 2 rollout**: BearDog remains the reference implementation. `btsp.session.*` RPC methods available for all primals.
- **Standalone startup**: Other primals should adopt the same `OnceLock` ephemeral ID pattern for PRIMAL IPC v3.1 compliance.
- **`ipc.register`**: BearDog now registers dynamically with Songbird on startup. Priority cascade for other primals: Songbird → NestGate → ToadStool → rest.

## Debt Remaining

| Item | Status |
|------|--------|
| 75 `#[allow(` remaining | Documented with `reason`; `expect` unfulfilled on these |
| plasmidBin harvest | Ecosystem-wide — needs musl-static rebuild |
| BTSP Phase 2 rollout | Ecosystem-wide — other primals need handshake enforcement |
