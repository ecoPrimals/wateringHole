<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 75 Handoff: Deep Debt — Purpose-Key Module Extraction, Dependency Drift & Debris Cleanup

**Date**: April 28, 2026
**From**: BearDog Team
**To**: primalSpring, all consuming primals
**Commit**: d4275ba42 (bearDog)

---

## What Changed

### 1. `aliases_and_beardog.rs` Refactored (927 → 452 LOC)

The NUCLEUS purpose-key operations added in Waves 72 and 74 pushed `aliases_and_beardog.rs` past the 800 LOC threshold. The following were extracted into a new `purpose_key.rs` submodule:

- `handle_derive_purpose_key` — `crypto.derive_purpose_key`
- `handle_sign_registration` — `crypto.sign_registration`
- `handle_purpose_encrypt` — `crypto.encrypt` with `purpose` param
- `handle_purpose_decrypt` — `crypto.decrypt` with `purpose` param
- `resolve_purpose_key` / `load_family_seed` — internal helpers

**Zero behavior change.** All 8 tests moved with the code. The `route()` function in `aliases_and_beardog.rs` delegates via `use super::purpose_key::*`.

### 2. Workspace Dependency Drift Normalized

| Crate | Dependency | Before | After |
|-------|-----------|--------|-------|
| `beardog-client` | `tokio-test` | `"0.4"` | `{ workspace = true }` |
| `beardog-integration` | `wiremock` | `"0.6"` | `{ workspace = true }` |

### 3. Stale `dns-sd` Feature Gate Removed

`beardog-discovery/tests/coverage_boost.rs` had `#[cfg(feature = "dns-sd")]` imports and a test, but the `dns-sd` feature was suspended and removed from `Cargo.toml`. Dead code deleted.

### 4. Date-Stamped Test Files Renamed

5 `coverage_boost_wave10.rs` files renamed to `coverage_boost.rs` (module declarations updated):
- `beardog-cli/src/handlers/`
- `beardog-discovery/src/`
- `beardog-installer/src/`
- `beardog-tunnel/src/`
- `beardog-types/src/`

### 5. Root Documentation Refreshed

- File-size threshold updated from 1000 to **800 LOC** across README, ROADMAP, ARCHITECTURE, START_HERE, STATUS
- Stale tarpc references removed from CONTEXT.md and STATUS.md (tarpc removed Jan 29, 2026)
- Waves 73–75 added to ROADMAP.md

---

## What Did NOT Change

- **Wire protocol**: All JSON-RPC methods unchanged
- **Method count**: Still 101 CryptoHandler + 9 IonicBondHandler
- **Purpose-key behavior**: `crypto.derive_purpose_key`, `crypto.sign_registration`, `crypto.encrypt`/`decrypt` with `purpose` — identical semantics
- **Secrets lazy derivation**: `secrets.retrieve("nucleus:{family}:purpose:{name}")` unchanged

---

## CI Status

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo deny check` | 4/4 pass |
| `cargo test --workspace` | 0 new failures (1 pre-existing flaky in beardog-cli) |

---

## For Downstream Primals

No action required. This is an internal refactoring wave. All published IPC methods and their semantics are unchanged.
