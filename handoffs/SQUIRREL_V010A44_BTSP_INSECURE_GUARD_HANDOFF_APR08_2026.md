<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.44 — BTSP BIOMEOS_INSECURE Guard Handoff

**Date:** April 8, 2026
**Primal:** Squirrel
**Version:** 0.1.0-alpha.44
**Sprint:** BTSP Protocol Standard compliance — GAP-MATRIX-12 resolution
**Previous:** `SQUIRREL_V010A43_WIRE_STANDARD_DEEP_DEBT_HANDOFF_APR08_2026.md`

---

## Summary

Implements the `BIOMEOS_INSECURE` startup guard required by BTSP Protocol
Standard v1.0.0 §Security Model and Primal Self-Knowledge Standard v1.1.0 §3.
This resolves GAP-MATRIX-12 (Medium) identified in the primalSpring audit.

**Core invariant:** A primal MUST refuse to start when both `FAMILY_ID`
(non-default) and `BIOMEOS_INSECURE=1` are set. Production mode requires
BTSP authentication; insecure mode is development-only.

---

## Changes

### 1. `validate_insecure_guard()` (GAP-MATRIX-12 resolution)

- **`crates/main/src/rpc/unix_socket.rs`** — new public functions:
  - `validate_insecure_guard()` — reads `SQUIRREL_FAMILY_ID` → `FAMILY_ID` and
    `BIOMEOS_INSECURE` from environment; returns `Err(String)` when both are set
  - `validate_insecure_guard_with(has_family, insecure)` — injectable variant
    for pure-function testing without env var side effects
- **`SocketConfig`** — new field `biomeos_insecure: Option<bool>` populated from
  `BIOMEOS_INSECURE` env var in `from_env()`

### 2. Startup gate

- **`crates/main/src/main.rs`** — `run_server()` calls `validate_insecure_guard()`
  as its first operation, before config load, socket resolution, or daemon fork.
  On failure, returns `anyhow::Error` which surfaces as `exit_code::CONFIG` (2).

### 3. Tests (9 new)

- 4 injectable unit tests: neither set, family-only, insecure-only, both-rejected
- 5 env-based tests via `temp_env`: no conflict, family-only, family+insecure,
  primal-specific-family+insecure, `"default"` family is not production
- All tests use `temp_env` for concurrent-safe env var isolation

---

## BTSP Compliance Checklist (Phase 1: Socket Naming Alignment)

```
Primal: Squirrel  Version: 0.1.0-alpha.44  Date: April 8, 2026

Socket Naming:
  [x] Reads FAMILY_ID (or SQUIRREL_FAMILY_ID) from environment
  [x] Creates squirrel-{family_id}.sock when FAMILY_ID is set
  [x] Creates squirrel.sock when FAMILY_ID is not set (development)
  [x] Refuses to start when both FAMILY_ID and BIOMEOS_INSECURE are set  ← NEW

Handshake (Phase 2+):
  [ ] BTSP handshake (requires BearDog btsp.session.* methods)

Cipher Negotiation (Phase 2+):
  [ ] Cipher suite support (requires BearDog btsp.negotiate)
```

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (6,875 passing / 0 failures / 107 ignored) |
| `cargo doc --workspace --no-deps` | PASS |

---

## Affected Files

| File | Change |
|------|--------|
| `crates/main/src/rpc/unix_socket.rs` | +`validate_insecure_guard()`, +`validate_insecure_guard_with()`, +`SocketConfig::biomeos_insecure`, +9 tests |
| `crates/main/src/main.rs` | +guard call at `run_server()` entry |

---

## Downstream Impact

- **primalSpring**: GAP-MATRIX-12 for Squirrel is resolved
- **biomeOS**: Squirrel now enforces BTSP Phase 1 socket naming rules fully
- **BearDog**: When BTSP Phase 2 ships (`btsp.session.create`), Squirrel's
  socket listener will need to wrap incoming connections in the handshake —
  the guard is the prerequisite for that work

---

## References

- `BTSP_PROTOCOL_STANDARD.md` v1.0.0 §Security Model, §Compliance Checklist
- `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` v1.1.0 §3 (Development mode guard)
- BearDog reference: `beardog-core/src/socket_config.rs::validate_insecure_guard()`
