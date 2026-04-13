<!--
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# biomeOS v3.05 — primalSpring Upstream Gap Resolution

| Field | Value |
|-------|-------|
| **Primal** | biomeOS |
| **Version** | v3.05 |
| **Date** | 2026-04-13 |
| **Tests** | 7,784 |
| **Source** | primalSpring v0.9.14 downstream audit (3 items, all MEDIUM) |
| **Status** | All 3 items RESOLVED |

---

## Gaps Resolved

### 1. `capability.call` ignores `gate` parameter (BLOCKING multi-gate)

**Problem**: When `gate` was specified in `capability.call` params but the gate
was not registered in the `GateRegistry`, the handler silently fell through to
local routing. This broke multi-gate compositions — callers thought they were
targeting a remote gate, but requests were served locally.

**Fix**: Unknown gates now return an explicit error with the list of known gates.
`gate: "local"` is a documented way to force local routing.

**Files**: `crates/biomeos-atomic-deploy/src/handlers/capability.rs`

### 2. `--port` ignored in `api`/`nucleus` modes (BLOCKING mobile/Android)

**Problem**: `biomeos api --port N` logged a deprecation warning and ignored the
port. `biomeos nucleus` had no port flag at all. This blocked mobile/Android
deployment where Unix sockets are unavailable (SELinux denies `sock_file create`).

**Fix**:
- `biomeos api --port N` now binds a TCP listener alongside UDS via `biomeos_api::serve_tcp()`
- `biomeos nucleus --port N [--tcp-only]` flags added, passed through to Neural API
- `biomeos-api` gains public `serve_tcp()` function

**Files**: `crates/biomeos/src/modes/api.rs`, `crates/biomeos/src/main.rs`,
`crates/biomeos/src/modes/nucleus.rs`, `crates/biomeos-api/src/lib.rs`

### 3. biomeOS DOWN during testing (Neural API not launched in nucleus mode)

**Problem**: `biomeos nucleus --mode full` started primals but never started the
Neural API server. External probes (primalSpring, health monitors) connecting to
`graph.deploy` or `capability.call` found nothing listening. Additionally, primal
process stdout/stderr were sent to `/dev/null`, preventing crash diagnosis.

**Fix**:
- `nucleus full` mode now spawns the Neural API server alongside primals
- Neural API inherits `--port`/`--tcp-only` from the nucleus CLI
- Process output redirected to `{socket_dir}/logs/{primal}.stdout.log` and `.stderr.log`
- Nucleus summary prints the log directory path

**Files**: `crates/biomeos/src/modes/nucleus.rs`

---

## Validation

```
cargo clippy --workspace --all-targets -- -D warnings   → 0 warnings
cargo test --workspace                                   → 7,784 passed, 0 failed
cargo doc --workspace --no-deps                          → 0 warnings
cargo fmt --all -- --check                               → clean
```

---

## Impact on primalSpring

All three items from the v0.9.14 downstream audit are resolved:
- `capability.call` with `gate` now fails explicitly for unregistered gates
- `--port` works across all server modes (neural-api, api, nucleus)
- NUCLEUS Full mode launches Neural API — biomeOS will be ALIVE in future sessions

primalSpring can re-run `exp094` against a biomeOS NUCLEUS with `graph.deploy`
and `capability.call` reachable.

---

*Handoff authored in response to primalSpring v0.9.14 downstream gap audit.*
