# biomeOS v3.14 — TCP-Only Cross-Architecture Composition Fixes

**Date**: April 14, 2026
**From**: primalSpring v0.9.14 exp096 audit → biomeOS v3.14 fixes
**License**: AGPL-3.0-or-later

---

## Context

primalSpring validated biomeOS as the composition substrate for cross-architecture
NUCLEUS deployment (Pixel aarch64 via `biomeos neural-api --tcp-only`). 6/9 exp096
checks passed; the remaining 3 failures exposed 4 upstream gaps in biomeOS affecting
any TCP-only or cross-platform deployment.

## Gaps Addressed

### Gap 1: TCP Endpoint Propagation in NeuralRouter

**Root cause**: `discover_and_register_primals` only scanned for `.sock` files and
registered `TransportEndpoint::UnixSocket`. In `--tcp-only` mode, no sockets exist.

**Fix**:
- Discovery now branches on `tcp_only`: probes TCP ports 9900–9919 via JSON-RPC
- Added `probe_tcp_capabilities()` — sends `capabilities.list` over TCP
- Registers `TransportEndpoint::TcpSocket` for discovered primals
- `capability.call` routing now works over TCP on Android/Windows

**Files**: `neural_api_server/discovery_init.rs`

### Gap 2: Graph Environment Variable Substitution

**Root cause**: `operation.environment` values like `${FAMILY_ID}` were passed
literally to `Command::env()` without expansion.

**Fix**:
- Two-pass `${VAR}` expansion before spawn:
  1. `substitute_env()` — resolves against ExecutionContext env map
  2. `substitute_from_process_env()` — resolves remaining vars against process env
- Applied in both `primal_spawner` and `capability_handlers/primal_start`

**Files**: `executor/primal_spawner.rs`, `capability_handlers/primal_start.rs`

### Gap 3: Bootstrap Environment Inheritance

**Root cause**: `execute_bootstrap_sequence` only passed `FAMILY_ID`, `BIOMEOS_FAMILY_ID`,
`BIOMEOS_MODE` into the ExecutionContext. Primal binary discovery needs
`BIOMEOS_PLASMID_BIN_DIR` / `ECOPRIMALS_PLASMID_BIN`.

**Fix**: Bootstrap now inherits 5 additional keys from process env:
`BIOMEOS_PLASMID_BIN_DIR`, `ECOPRIMALS_PLASMID_BIN`, `XDG_RUNTIME_DIR`,
`FAMILY_SEED`, `BIOMEOS_SOCKET_DIR`.

**Files**: `bootstrap.rs`

### Gap 4: --tcp-only Cascade to Child Primals

**Root cause**: `--tcp-only` only affected the Neural API listener; spawned child
primals still defaulted to UDS binding.

**Fix**:
- `ExecutionContext` gained `tcp_only: bool` + `tcp_port_counter: AtomicU16`
- `GraphExecutor::with_nucleation` threads `tcp_only` into context
- `spawn_primal_process` injects `--port <auto>` and `PRIMAL_TRANSPORT=tcp`
- Added `wait_for_tcp_port()` for TCP readiness (replaces socket file check)
- `primal_launch` returns `tcp_port` in output JSON

**Files**: `executor/context.rs`, `neural_executor.rs`, `executor/primal_spawner.rs`,
`executor/node_handlers.rs`

## Validation

- `cargo build`: clean (0 errors)
- `cargo clippy --workspace`: 0 warnings
- `cargo test --workspace`: all pass (0 failures)
- exp096 expected: all 3 failing checks (Genetics RPC, BTSP Phase 3, HSM probe)
  should now route through TCP endpoints

## Expected primalSpring Revalidation

After deploying this biomeOS build to Pixel:
```
[PASS] Neural API alive (health.liveness)
[PASS] BearDog alive through proxy (primal.health)
[PASS] Songbird alive through proxy (primal.health)
[PASS] NestGate recognized (primal.health)
[PASS] BearDog capabilities (33 found)
[PASS] FAMILY_ID matches
[EXPECTED PASS] Genetics RPC via proxy → Gap 1+4 fix
[EXPECTED PASS] BTSP Phase 3 via proxy → Gap 1+4 fix
[EXPECTED PASS] HSM probe via proxy → Gap 1+4 fix
```

---

**License**: AGPL-3.0-or-later
