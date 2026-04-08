# biomeOS v2.81 — Fully Concurrent Testing + BM-04/05 + TCP-only + Gate Routing

**Date**: March 31, 2026
**Primal**: biomeOS
**Version**: 2.81
**Priority**: P0 (resolves ISSUE-014, BM-04, BM-05)
**Tests**: 7,212 passed | 0 failures | Fully concurrent (RUST_TEST_THREADS=16)

---

## Summary

This session resolves the ecosystem's highest-priority blocker (ISSUE-014 / BM-04 capability
registration timing) end-to-end, eliminates all `#[serial]` test annotations for fully concurrent
Rust testing, wires TCP-only mode into the CLI for mobile orchestration, and shares the
`GateRegistry` between `CapabilityHandler` and `InferenceHandler` for operational cross-gate
`capability.call` routing.

---

## Resolved Issues

### BM-04: Capability Registration Timing (RESOLVED)

**Problem**: `discover_and_register_primals()` ran once at startup with 500ms timeouts. Late-starting
primals were invisible — `capability.list` only returned 5 biomeOS self-capabilities.

**Fix (three convergent paths)**:
1. **`topology.rescan`** — JSON-RPC method re-runs discovery on demand
2. **Lazy rescan** — `discover_capability()` triggers `lazy_rescan_sockets()` on first registry miss
3. **`capability.register` / `route.register`** — Primals self-register at their own startup

**Files**: `neural_router/mod.rs`, `neural_router/discovery.rs`, `server_lifecycle.rs`, `routing.rs`

### BM-05: Probe Response Format (RESOLVED)

**Problem**: `probe_primal_capabilities` silently skipped primals returning non-matching JSON shapes.

**Fix**: `extract_capabilities_from_response()` in `cap_probe.rs` handles 4 wire formats:
- Format A: `{"result": {"capabilities": ["cap1", "cap2"]}}`
- Format B: `{"result": ["cap1", "cap2"]}`
- Format C: `{"result": {"capabilities": [{"name": "cap1"}]}}`
- Format D: `{"result": {"methods": ["cap1", "cap2"]}}`

Unrecognized shapes log at `warn!` level (was `debug!`). Probe timeout centralized to
`timeouts::PROBE_TIMEOUT` (500ms).

**Files**: `biomeos-core/src/socket_discovery/cap_probe.rs`, `biomeos-types/src/constants/mod.rs`

### TCP-only API Mode (CLI WIRED)

**Problem**: `biomeos neural-api --port` did not exist. TCP-only mode was library-only, blocking
mobile orchestration (Android/GrapheneOS: SELinux denies `sock_file create`).

**Fix**:
- `biomeos neural-api --port PORT` — TCP alongside UDS
- `biomeos neural-api --port PORT --tcp-only` — skip UDS, TCP only
- `serve()` uses `tokio::select!` across UDS and TCP listeners

**Files**: `biomeos/src/main.rs`, `biomeos/src/modes/neural_api.rs`

### Cross-Gate `capability.call` Routing (OPERATIONAL)

**Problem**: `CapabilityHandler` in `NeuralApiServer::new()` received a fresh empty `GateRegistry`,
separate from the one given to `InferenceHandler`. Gate routing in `capability.call` was non-functional.

**Fix**: Single `Arc<GateRegistry>` created first, shared via `.with_gate_registry()` to
`CapabilityHandler` and passed to `InferenceHandler`.

**Files**: `neural_api_server/mod.rs`

---

## `#[serial]` Elimination — Fully Concurrent Testing

All `#[serial_test::serial]` annotations removed from the codebase. `serial_test` dependency
removed from all `Cargo.toml` files.

**Approach**: Dependency injection via parameterized function variants (`_with`, `_in`,
`from_env_values`, config structs). Tests inject configuration directly — zero
`std::env::set_var`/`remove_var` mutations. Affected 30+ crates, 100+ functions, 200+ tests.

**Result**: 7,212 tests pass fully concurrent at `RUST_TEST_THREADS=16`.

---

## Other Deep Debt Resolved

| Category | Change |
|----------|--------|
| `mem::forget` | 4 production instances replaced with explicit `Child`/`JoinHandle`/guard ownership |
| Hardcoded `CORE_PRIMALS` | Replaced with dynamic socket directory scanning |
| Hardcoded spring names | Replaced with `primal_names` constants |
| `is_known_primal` gate | Removed — registration driven solely by capability probe |
| `SQUIRREL` AI fallback | Removed — capability-based AI provider discovery |
| UID "1000" fallback | 4 sites evolved to proper `env`/`/proc/self` resolution |
| `start_monitoring()` | Uncommented and wired in `live_service.rs` |
| Interactive mode | Returns explicit error in `execute_command_integration` |
| SPDX headers | 100% coverage verified on all `.rs` files |

---

## Verification

```
cargo clippy --all-targets --all-features -- -D warnings  → 0 warnings
cargo fmt --all -- --check                                 → clean
RUST_TEST_THREADS=16 cargo test --all                      → 7,212 passed, 0 failures
SPDX-License-Identifier                                    → 100% .rs coverage
```

---

## Cross-References

- **ISSUE-014** (SPRING_EVOLUTION_ISSUES.md): Can be marked RESOLVED
- **BM-04** (PRIMAL_RESPONSIBILITY_MATRIX.md): RESOLVED — 3 convergent discovery paths
- **BM-05** (IPC_COMPLIANCE_MATRIX.md): RESOLVED — 4 wire formats + warn logging
- **TCP-only** (IPC_COMPLIANCE_MATRIX.md): RESOLVED — CLI `--port` + `--tcp-only`
- **Gate routing** (IPC_COMPLIANCE_MATRIX.md): RESOLVED — shared GateRegistry

---

## Ecosystem Impact

- **+14 IPC compliance checks** resolved (per ISSUE-014 estimates)
- **Unblocks**: All multi-primal capability routing via Neural API
- **Unblocks**: Mobile orchestration (Android/GrapheneOS TCP-only)
- **Unblocks**: Cross-gate federation via `capability.call` with `gate` parameter
- **Unblocks**: Composition C7 (INTER_PRIMAL_INTERACTIONS.md Phase 4)
