<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 77b Handoff: `#[allow]` Reason Hygiene & Workspace Dependency Drift

**Date**: April 30, 2026
**From**: BearDog Team
**To**: ecoPrimals ecosystem — informational, no consumer action required

---

## Summary

Internal code hygiene pass. Zero behavior changes, zero new RPC methods, zero API surface changes.
Consumers do not need to update anything.

## Changes

### `#[allow]` Reason Hygiene

19 bare `#[allow(...)]` attributes in production `.rs` files were given explicit `reason = "..."` metadata.
Affected lint categories:

- `async_fn_in_trait` (4 files) — native RPITIT; Send bounds match our impls
- `deprecated` (4 files) — bridging deprecated items during planned migration
- `missing_docs` (8 coordination config files) — serde-derived structs with self-documenting field names
- `cast_precision_loss` / `cast_possible_wrap` / `cast_sign_loss` (resilience, math) — intentional numeric conversions with checked bounds
- `dead_code` (infrastructure) — capability vectors populated at discovery time
- `wildcard_imports` / `missing_errors_doc` (consolidated traits) — re-export convenience
- `double_must_use` / `missing_errors_doc` (algorithms) — inherited Result wrapping
- `needless_doctest_main` (threat management) — standalone example code

### Workspace Dependency Drift

- `beardog-tower-atomic`, `beardog-discovery`, `beardog-installer`, `beardog-client` added to root `[workspace.dependencies]`.
- 11 explicit `version + path` pins in `beardog-client/Cargo.toml` and `beardog-integration/Cargo.toml` converted to `{ workspace = true }`.
- `mockito` (testing HTTP mock) unified: added to `[workspace.dependencies]` at `"1.2"`, both consumer crates switched to `{ workspace = true }`.

### Root Documentation Updated

- Dates → April 30, 2026 across README, STATUS, ROADMAP, ARCHITECTURE, CONTEXT, START_HERE.
- Wave 77/77b entries added to STATUS "Recent Improvements" and ROADMAP "Recently Completed".
- Method count updated: 101 → 102 (CryptoHandler 97, IonicBondHandler 5).

### Deep Debt Audit Results (Confirmed Clean)

| Metric | Count |
|--------|-------|
| Files >800 LOC | 0 |
| `unsafe` blocks | 0 |
| Production mocks (non-`#[cfg(test)]`) | 0 |
| Hardcoded peer primal names | 0 |
| `#[async_trait]` (replaced by RPITIT) | 0 |
| `Box<dyn Error>` in production | 0 |
| `todo!()` / `unimplemented!()` | 0 |
| `TODO` / `FIXME` / `HACK` comments | 0 |

## CI Status

- `cargo fmt --check` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo check --workspace` — clean
- Known pre-existing flaky test: `beardog-cli::handlers::key_export::tests::test_handle_key_export_roundtrip_uses_default_home_env`
