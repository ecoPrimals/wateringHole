# rhizoCrypt v0.14.0-dev — Session 33: Trio IPC Stability Handoff

**Date:** 2026-04-11
**Primal:** rhizoCrypt
**Context:** primalSpring portability debt audit — Trio IPC stability hardening

---

## Summary

Investigated and resolved remaining rhizoCrypt gaps from the primalSpring
downstream audit of the Provenance Trio (rhizoCrypt + loamSpine + sweetGrass).

## Audit Findings

| Gap | Status | Detail |
|-----|--------|--------|
| flush-on-write | **Already present** | `newline.rs:121` flushes after every `write_all`, BTSP framing likewise |
| TCP_NODELAY | **Resolved this session** | `set_nodelay(true)` on every accepted `TcpStream` in `handle_tcp_connection` |
| Tower Atomic TCP opt-in | **No action needed** | TCP JSON-RPC is always-on by default; no stale branches exist |
| UDS flush | **Already present** | UDS connections route through same `newline.rs` handler with flush |

## Changes

### TCP_NODELAY on Accepted Connections

`crates/rhizo-crypt-rpc/src/jsonrpc/mod.rs` — `handle_tcp_connection()`:

```rust
stream.set_nodelay(true)?;
```

Applied before protocol detection (peek), so both newline-delimited JSON-RPC
and HTTP paths benefit from NODELAY. Eliminates Nagle-algorithm latency on
small frames, consistent with sweetGrass's pattern.

### New Test

`crates/rhizo-crypt-rpc/tests/rpc_integration.rs`:
- `test_tcp_nodelay_set_on_connection` — connects, sends health.check over
  newline protocol, verifies response under NODELAY.

## Trio IPC Alignment Matrix

| Pattern | rhizoCrypt | loamSpine | sweetGrass |
|---------|-----------|-----------|------------|
| flush-on-write | Yes (S31) | Needs audit | Yes (S32) |
| TCP_NODELAY | **Yes (S33)** | Needs audit | Yes (S32) |
| Concurrent UDS load test | Yes (50 clients, S31) | Needs audit | Yes (8x5, S32) |
| Graceful shutdown under load | Yes (S31) | Needs audit | Needs audit |

## Code Health

- **1,471 tests** passing (`--all-features`)
- **~93%** line coverage (`llvm-cov`)
- **Zero** clippy warnings (pedantic + nursery)
- **Zero** unsafe blocks
- **Zero** TODOs in production code

## Remaining Trio-Wide Debt

- **loamSpine**: Needs flush-on-write + TCP_NODELAY audit and adoption
- **sweetGrass Postgres coverage**: Deferred until Docker Postgres in CI
- **sweetGrass BTSP coverage**: Deferred until BearDog integration available

## For primalSpring Gap Registry

- **TRIO-IPC (rhizoCrypt portion)**: Resolved — flush confirmed, TCP_NODELAY added
- **Tower Atomic TCP opt-in (rhizoCrypt)**: Resolved — TCP always-on, no stale state
