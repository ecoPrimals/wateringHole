# rhizoCrypt v0.13.0-dev — Resilience, DispatchOutcome, OrExit Handoff

**Date**: March 16, 2026 (session 15)  
**Primal**: rhizoCrypt  
**Version**: 0.13.0-dev  
**Scope**: Deep debt execution — resilience primitives, dispatch model, validation ergonomics

---

## Summary

This session absorbed patterns from 6 springs and primals to add IPC resilience,
structured dispatch outcomes, zero-panic validation, and dual-format discovery
parsing to rhizoCrypt.

## Artifacts Created/Modified

### New Files

| File | Purpose |
|------|---------|
| `crates/rhizo-crypt-core/src/clients/resilience.rs` | CircuitBreaker + RetryPolicy for IPC clients |

### Modified Files

| File | Change |
|------|--------|
| `crates/rhizo-crypt-core/src/error.rs` | +IpcErrorPhase helpers, +DispatchOutcome, +extract_rpc_error(), +OrExit<T> |
| `crates/rhizo-crypt-core/src/lib.rs` | Re-exports: DispatchOutcome, OrExit, extract_rpc_error |
| `crates/rhizo-crypt-core/src/clients/mod.rs` | Register resilience module, re-export CircuitBreaker/RetryPolicy |
| `crates/rhizo-crypt-core/src/clients/adapters/unix_socket.rs` | Refactored to use centralized extract_rpc_error() |
| `crates/rhizo-crypt-core/src/discovery/registry.rs` | Dual-format capability parsing (flat + nested), colon-delimited names |
| `crates/rhizo-crypt-core/tests/property_tests.rs` | +7 proptest blocks for new types |
| `CHANGELOG.md` | Session 15 entry |
| `README.md` | Updated metrics table |
| `wateringHole/PRIMAL_REGISTRY.md` | Updated rhizoCrypt entry |

## Absorption Sources

| Pattern | Source | Description |
|---------|--------|-------------|
| `IpcErrorPhase` convenience methods | healthSpring V28 | `is_method_not_found()`, `is_retriable()`, `is_timeout_likely()` |
| `DispatchOutcome` | airSpring V15 / biomeOS | Protocol vs application error separation |
| `OrExit<T>` | wetSpring V123 | Zero-panic validation binary support |
| Dual-format capability parsing | groundSpring / neuralSpring / airSpring / wetSpring | Flat string + nested object discovery responses |
| CircuitBreaker | healthSpring V28 | Consecutive-failure threshold with cooldown |
| RetryPolicy | airSpring V15 | Exponential backoff, transport-only retry |

## Quality Gates

All gates pass:

- `cargo fmt` — clean
- `cargo clippy` (pedantic + nursery + cargo, `-D warnings`) — 0 warnings
- `cargo doc` (`-D warnings`) — 0 warnings
- `cargo test --workspace` — 1056+ pass, 0 fail
- `cargo deny check` — advisories ok, bans ok, licenses ok, sources ok
- Zero `unsafe` in production code
- Zero `unwrap`/`expect` in production code

## Key Design Decisions

1. **CircuitBreaker only trips on transport errors** — Application errors (JsonRpcError, NoResult)
   don't trip the breaker because the remote primal is reachable and responding.

2. **OrExit implemented for both Result and Option** — Validation binaries can use either:
   `config.or_exit("config")` or `file.read().or_exit("read failed")`.

3. **Dual-format is serde Visitor, not try-parse** — The custom deserializer handles mixed
   arrays (`["string", {"name": "string"}]`) in a single pass without fallback parsing.

4. **extract_rpc_error() returns Option, not Result** — Callers check for error presence,
   not parse failures. Missing fields use safe defaults (-1, "Unknown error").

## Next Steps

- Wire CircuitBreaker into capability client `discover()` calls
- Add jitter to RetryPolicy backoff (currently left to caller)
- Update `ISSUE-012` (Content Similarity Index) and `ISSUE-013` (Content Convergence)
- Evolve `DispatchOutcome` into the JSON-RPC handler layer (rhizo-crypt-rpc)
