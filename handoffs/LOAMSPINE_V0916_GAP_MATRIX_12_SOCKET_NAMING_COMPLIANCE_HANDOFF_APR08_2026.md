<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — GAP-MATRIX-12 Socket Naming Compliance

**Date**: April 8, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Sprint**: GAP-MATRIX-12 resolution

---

## Summary

Resolved GAP-MATRIX-12 (socket naming non-compliance) and verified GAP-MATRIX-10
(UDS listener) and Wire Standard L2 (methods array + identity.get) were already
resolved from prior sprints.

## Changes

### 1. Domain-Based Socket Naming (PRIMAL_SELF_KNOWLEDGE_STANDARD §3)

**Before**: Socket path used primal name: `loamspine.sock` / `loamspine-{fid}.sock`  
**After**: Socket path uses capability domain: `permanence.sock` / `permanence-{fid}.sock`

New constant `primal_names::DOMAIN = "permanence"` is the single source of truth
for the socket domain stem. The `resolve_socket_path_with()` function and all
callers now use domain-based naming.

Resolution order (unchanged):
1. `LOAMSPINE_SOCKET` env override (explicit path wins)
2. `$XDG_RUNTIME_DIR/biomeos/permanence[-{family_id}].sock`
3. `/run/user/{uid}/biomeos/...` (Linux)
4. `temp_dir/biomeos/...`

### 2. BIOMEOS_INSECURE Security Guard

New `validate_security_config()` function enforces the spec invariant:

> If both FAMILY_ID (non-default) and BIOMEOS_INSECURE=1 are set, the primal
> MUST refuse to start.

Called at startup before any listeners bind. Uses `OrExit` trait for clean
fatal error with structured logging.

### 3. Legacy Symlink (Backward Compatibility)

On startup (after UDS bind succeeds): `loamspine.sock → permanence.sock`

The symlink supports consumers still using identity-based discovery (Tier 5–6
in `CAPABILITY_BASED_DISCOVERY_STANDARD.md`) during migration.

Both the primary socket and legacy symlink are cleaned up on graceful shutdown
per spec requirement.

### 4. Already-Resolved Gaps

- **GAP-MATRIX-10** (UDS listener alongside TCP): Already resolved — `main.rs`
  starts `run_jsonrpc_uds_server` alongside TCP since v0.9.15.
- **Wire Standard L2** (methods array + identity.get): Already resolved in
  Capability Wire Standard L2/L3 sprint (this session).

## Files Modified

| File | Change |
|------|--------|
| `crates/loam-spine-core/src/primal_names.rs` | Added `DOMAIN = "permanence"` constant |
| `crates/loam-spine-core/src/neural_api/socket.rs` | Domain-based naming, `BIOMEOS_INSECURE` guard, legacy symlink helpers |
| `crates/loam-spine-core/src/neural_api/mod.rs` | Re-exports for new public functions |
| `crates/loam-spine-core/src/neural_api/tests.rs` | 12 new tests for domain naming, security config, legacy symlink |
| `bin/loamspine-service/main.rs` | Security guard at startup, legacy symlink creation + cleanup |
| `bin/loamspine-service/tests/main_integration.rs` | Updated socket path assertion to domain-based |

## Verification

```
cargo clippy --all-targets  → 0 warnings
cargo test                  → 1,316 passed, 0 failed
```

## Downstream Impact

- **biomeOS**: UDS socket scan will now find `permanence.sock` (domain-based)
  instead of `loamspine.sock`. Legacy symlink provides backward compat during
  migration.
- **primalSpring**: GAP-MATRIX-12 can be marked RESOLVED for loamSpine.
  GAP-MATRIX-10 was already resolved.

## BTSP Tier Status

| Requirement | Status |
|-------------|--------|
| Wire Standard L2 (methods + identity.get) | PASS |
| UDS listener alongside TCP | PASS |
| Domain-based socket naming | PASS |
| BIOMEOS_INSECURE guard | PASS |
| Family-scoped socket naming | PASS |
| Legacy symlink | PASS |
| Socket cleanup on shutdown | PASS |
