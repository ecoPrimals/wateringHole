# rhizoCrypt v0.14.0-dev — Session 29 Handoff

**Date**: April 8, 2026
**Session**: 29
**Focus**: BTSP Phase 1 (GAP-MATRIX-12), Wire L2 verification (GAP-MATRIX-10)

---

## Summary

Implemented BTSP Phase 1 socket naming for rhizoCrypt, closing GAP-MATRIX-12.
Socket path is now family-scoped when `FAMILY_ID` is set (`rhizocrypt-{fid}.sock`).
BIOMEOS_INSECURE guard prevents conflicting prod/dev configuration.
GAP-MATRIX-10 (Wire L2) verified as already resolved from sessions 26-27.

---

## Changes

### 1. GAP-MATRIX-12: BTSP Phase 1 — Family-Scoped Socket Naming

- **`read_family_id(prefix)`**: Reads `{PREFIX}_FAMILY_ID` (primal-specific) or `FAMILY_ID` (ecosystem); `"default"` treated as unset
- **`family_scoped_socket_path(name, prefix)`**: Returns `{name}-{fid}.sock` when FAMILY_ID set, `{name}.sock` when unset
- **`is_biomeos_insecure()`**: Truthy check for `BIOMEOS_INSECURE` (`1`, `true`, `yes`)
- **`btsp_env_guard(prefix)`**: Refuses to start when both FAMILY_ID and BIOMEOS_INSECURE are set
- **UDS default path**: `default_socket_path()` in `uds.rs` now uses `family_scoped_socket_path`
- **Service startup**: Guard check runs before DAG engine init; logs family_id and dev-mode warnings
- **16 new tests**: Comprehensive coverage of all BTSP Phase 1 behaviors

### 2. GAP-MATRIX-10: Wire L2 — Already Resolved

- `capabilities.list` returns `{primal, version, methods}` flat array (added in session 27)
- `identity.get` returns `{primal, version, domain, description}` (added in session 26)
- Existing tests `test_capability_list` and `test_identity_get` confirm compliance
- Audit may have been run against older binary — binary rebuild needed

---

## Quality Gates

- `cargo fmt` — clean
- `cargo clippy --workspace --all-features` — 0 warnings
- `cargo test --workspace --all-features` — **1,441 tests**, 0 failures
- All BTSP Phase 1 checklist items covered:
  - [x] Reads FAMILY_ID (or RHIZOCRYPT_FAMILY_ID) from environment
  - [x] Creates `rhizocrypt-{family_id}.sock` when FAMILY_ID is set
  - [x] Creates `rhizocrypt.sock` when FAMILY_ID is not set (development)
  - [x] Refuses to start when both FAMILY_ID and BIOMEOS_INSECURE are set

---

## BTSP Compliance Status

| Checklist Item | Status |
|---------------|--------|
| Reads FAMILY_ID from environment | PASS |
| Primal-specific override (RHIZOCRYPT_FAMILY_ID) | PASS |
| Family-scoped socket naming | PASS |
| Development fallback (no FAMILY_ID) | PASS |
| BIOMEOS_INSECURE guard | PASS |
| BTSP handshake (Phase 2+) | Not yet implemented |
| Cipher negotiation (Phase 2+) | Not yet implemented |

---

## Next Steps

- BTSP Phase 2: Handshake protocol implementation (when ecosystem standard stabilizes)
- Binary rebuild for primalSpring re-validation of GAP-MATRIX-10
