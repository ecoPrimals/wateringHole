<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 87: UDS JSON-RPC Protocol Fix

**Date**: April 30, 2026
**From**: coralReef team
**To**: primalSpring, all downstream springs, NUCLEUS composition

---

## Summary

Resolves **primalSpring v0.9.24 P1**: coralReef was the only NUCLEUS primal whose main UDS socket spoke tarpc binary instead of JSON-RPC 2.0. This caused 4 composition experiment failures (exp004 `health_shader`, `caps_shader`, `composition_all_healthy`; exp094 `shader_supported_archs`).

## Root Cause

When composition passes `--tarpc-bind unix://coralreef-{family}.sock`, tarpc occupied the main ecosystem socket. The JSON-RPC UDS server auto-computed a different path (`coralreef-core-{family}.sock` via `CARGO_PKG_NAME`) and was unreachable by standard composition tooling.

## Fix: `resolve_uds_binds`

New function in `cmd_server` startup path:

1. When `--tarpc-bind` is a Unix socket (composition case), the provided path becomes the **JSON-RPC** socket
2. tarpc is redirected to a `-tarpc` suffixed socket (e.g. `coralreef-alpha-tarpc.sock`)
3. JSON-RPC UDS starts **before** tarpc to claim the main path
4. Already-suffixed paths (`*-tarpc.sock`, from `default_tarpc_bind()`) are not redirected

Example for composition with `--tarpc-bind unix:///run/user/1000/biomeos/coralreef-alpha.sock`:
- **JSON-RPC**: `/run/user/1000/biomeos/coralreef-alpha.sock` (standard IPC path)
- **tarpc**: `/run/user/1000/biomeos/coralreef-alpha-tarpc.sock` (high-perf channel)

## Discovery

The discovery file now advertises three transports:
- `jsonrpc` — TCP (existing)
- `tarpc+unix` — tarpc on dedicated socket (address updated)
- `jsonrpc+unix` — JSON-RPC on main UDS (new)

## Impact on Composition

- `health.liveness`, `health.readiness`, `health.check` now reachable on the main socket
- `capability.list`, `capability.call` work through standard path
- `shader.compile.*` methods accessible via both JSON-RPC (UDS/TCP) and tarpc

## Impact on tarpc Clients

tarpc clients (e.g. barraCuda) should discover the tarpc endpoint via the `tarpc+unix` transport in the discovery file, not by assuming the main socket speaks tarpc.

## Tests

- 4 new `resolve_uds_binds` unit tests
- 4550 total tests passing, 0 failures
- Zero clippy warnings (pedantic + nursery)

## Files Changed

- `crates/coralreef-core/src/main.rs` — `resolve_uds_binds`, reordered server startup, `jsonrpc+unix` transport
- `crates/coralreef-core/src/main_tests/resolve_uds_binds.rs` — new test file
- `crates/coralreef-core/src/main_tests/mod.rs` — module registration
