# toadStool S179 — primalSpring Audit Remediation + Discovery Renames

**Date**: April 4, 2026
**Session**: S179 (primalSpring audit response, discovery capability renames)
**Status**: All quality gates green. 21,624 tests, 0 failures. Clippy clean.
**Previous**: `TOADSTOOL_S176_177_CAPABILITY_EVOLUTION_DEEP_DEBT_HANDOFF_APR04_2026.md` (archived)

---

## primalSpring Audit Response

| Audit Item | Status |
|------------|--------|
| Clippy FAIL (`aes_gcm::from_slice`) | **Already resolved** — no `aes_gcm` in codebase (removed in S175) |
| Test failure (`test_discovery_handles_timeout`) | **Already resolved** — test evolved/removed in prior session |
| Discovery renames in core/distributed | **Executed** — see below |

## Discovery Renames Executed

### Deprecated Socket Path Fallback Removal (5 files)

| Function | Action |
|----------|--------|
| `resolve_beardog_socket_fallback` | **Removed** → `resolve_capability_socket_fallback("crypto", env)` |
| `resolve_songbird_socket_fallback` | **Removed** → `resolve_capability_socket_fallback("coordination", env)` |
| `resolve_nestgate_socket_fallback` | **Removed** → `resolve_capability_socket_fallback("storage", env)` |
| `resolve_squirrel_socket` | **Removed** → `resolve_routing_socket(env)` |

### Deprecated IPC Alias Removal (4 files)

| Function / Var | Action |
|----------------|--------|
| `get_default_songbird_socket()` | **Removed** |
| `register_with_songbird()` | **Removed** |
| `SONGBIRD_SOCKET` env fallback | **Removed** from `resolve_coordination_socket()` |
| Re-exports in `ipc/mod.rs`, `ipc_helpers/mod.rs` | Cleaned; `#[allow(deprecated)]` removed |

### Validation Message Evolution (4 files)

| Before | After |
|--------|-------|
| "Songbird endpoint cannot be empty" | "Coordination service endpoint cannot be empty" |
| "BearDog endpoint cannot be empty" | "Security service endpoint cannot be empty" |
| "NestGate endpoint cannot be empty" | "Storage service endpoint cannot be empty" |
| "Squirrel endpoint cannot be empty" | "AI/routing service endpoint cannot be empty" |

### Discovery Reference Count

| Metric | S176 (pre-S177) | S177 | S179 |
|--------|-----------------|------|------|
| Primal name refs (audit) | 3,239 | 2,998 | ~2,900 (est.) |
| Deprecated functions removed | — | 4 socket, 2 IPC | 4 socket fallback, 2 IPC alias |

**Remaining**: Structural references (module names like `songbird_integration`, type names,
integration crate boundaries) and test fixtures. These are architectural — the modules
integrate with specific primals by design.

## Verification

```
cargo clippy --workspace --all-targets -- -D warnings   # 0 warnings
cargo test --workspace                                   # 21,624 passed, 0 failed
```

## Remaining Active Debt

| ID | Crate | Description |
|----|-------|-------------|
| D-TARPC-PHASE3 | integration/protocols | tarpc binary transport not wired |
| D-EMBEDDED-PROGRAMMER | runtime/specialty | Placeholder ISP/ICSP programmer impls |
| D-EMBEDDED-EMULATOR | runtime/specialty | Placeholder MOS6502/Z80 emulator impls |
| D-COV | workspace | Test coverage ~80-85%, target 90% |

---

Part of [ecoPrimals](https://github.com/ecoPrimals) — sovereign compute for science and human dignity.
