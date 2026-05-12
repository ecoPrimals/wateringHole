# NestGate — BTSP Phase 1: INSECURE Guard + Family-Scoped Socket Naming

**Date:** April 8, 2026
**Primal:** NestGate (storage domain)
**Commit:** `90c45cec`
**Standard:** `BTSP_PROTOCOL_STANDARD.md` v1.0 — Phase 1

---

## Summary

primalSpring audit flagged NestGate as "BTSP Tier 1 (native) ✓ — no blocking gaps."
Verification found **two false positives** — gaps the audit marked as complete but weren't implemented:

1. **`BIOMEOS_INSECURE` guard** — zero references in codebase before this session.
2. **Family-scoped socket naming** — Tiers 2/3 always used `nestgate.sock` regardless of FAMILY_ID.

Both are now implemented and tested.

---

## Changes

### 1. BIOMEOS_INSECURE Guard

**File:** `nestgate-rpc/src/rpc/socket_config.rs` — `from_env_source()`

- Reads `BIOMEOS_INSECURE` from environment.
- When `FAMILY_ID` is set (not "standalone"/"default") AND `BIOMEOS_INSECURE=1`, returns hard error and refuses to start.
- Also reads generic `FAMILY_ID` env (in addition to `NESTGATE_FAMILY_ID`), with NESTGATE-prefixed taking precedence.
- Error message: `"BTSP guard: FAMILY_ID is set ({fid}) but BIOMEOS_INSECURE=1..."`.

### 2. Family-Scoped Socket Naming

**File:** `nestgate-rpc/src/rpc/socket_config.rs`

New helpers:
- `is_family_scoped(family_id)` — returns `true` when family_id is not "standalone"/"default"/"".
- `socket_file_name(family_id)` — returns `nestgate-{fid}.sock` when family-scoped, else `nestgate.sock`.
- `storage_capability_sock_name(family_id)` — returns `storage-{fid}.sock` when family-scoped, else `storage.sock`.

Socket resolution updated:
- **Tier 2** (`BIOMEOS_SOCKET_DIR`): `{dir}/nestgate-{fid}.sock` when family-scoped.
- **Tier 3** (`XDG_RUNTIME_DIR`): `{xdg}/<eco>/nestgate-{fid}.sock` when family-scoped.
- **Tier 4** (fallback): already had `nestgate-{fid}-{node}.sock`.
- **Tier 1** (explicit override): unchanged (user-specified path).

Capability symlinks:
- `install_storage_capability_symlink()` and `remove_storage_capability_symlink()` now accept `family_id` parameter.
- `StorageCapabilitySymlinkGuard` stores `family_id` for cleanup on drop.
- Family-scoped symlinks: `storage-{fid}.sock` → `nestgate-{fid}.sock`.

### 3. Updated Call Sites

- `unix_socket_server/mod.rs`: install/remove symlink calls pass `self.family_id`.
- `isomorphic_ipc/server.rs`: threads `family_id` from `SocketConfig` to `StorageCapabilitySymlinkGuard`.

---

## Tests Added (13 new)

| Test | Validates |
|------|-----------|
| `btsp_guard_rejects_family_id_plus_insecure` | Hard error on conflicting config |
| `btsp_guard_allows_insecure_without_family_id` | Dev mode works |
| `btsp_guard_allows_insecure_with_standalone_family` | "standalone" is dev |
| `btsp_guard_allows_insecure_with_default_family` | "default" is dev |
| `btsp_guard_allows_family_id_without_insecure` | Production without INSECURE works |
| `family_scoped_socket_name_in_biomeos_dir` | Tier 2 uses `nestgate-{fid}.sock` |
| `standalone_uses_simple_socket_name_in_biomeos_dir` | Dev keeps `nestgate.sock` |
| `family_scoped_socket_name_in_xdg_tier` | Tier 3 uses `nestgate-{fid}.sock` |
| `generic_family_id_also_accepted` | `FAMILY_ID` (non-prefixed) triggers guard |
| `nestgate_family_id_takes_precedence_over_generic` | NESTGATE_FAMILY_ID wins |
| `install_creates_family_scoped_symlink` | `storage-{fid}.sock` symlink created |
| (+ 2 existing tests updated with `family_id` parameter) | |

---

## BTSP Phase 1 Compliance (Updated)

```
BTSP_PROTOCOL_STANDARD v1.0 — NestGate Checklist

Socket Naming:
  [x] Reads FAMILY_ID (or NESTGATE_FAMILY_ID) from environment
  [x] Creates nestgate-{family_id}.sock when FAMILY_ID is set
  [x] Creates nestgate.sock when FAMILY_ID is not set (development)
  [x] Refuses to start when both FAMILY_ID and BIOMEOS_INSECURE are set

Handshake (Phase 2+): Pending — requires BearDog btsp.session.create
Cipher Negotiation (Phase 2+): Pending
```

---

## Files Changed

- `code/crates/nestgate-rpc/src/rpc/socket_config.rs` — guard, naming helpers, symlink signatures
- `code/crates/nestgate-rpc/src/rpc/socket_config_tests.rs` — 13 new tests, updated existing
- `code/crates/nestgate-rpc/src/rpc/unix_socket_server/mod.rs` — family_id threading
- `code/crates/nestgate-rpc/src/rpc/isomorphic_ipc/server.rs` — family_id threading

---

**Verification:** `cargo test -p nestgate-rpc -- socket_config` — 49 passed, 0 failed.
