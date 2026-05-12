# Songbird v0.2.1 — Waves 175-176 Deep Debt + Documentation Handoff

**Date**: April 27, 2026
**Primal**: Songbird
**Waves**: 175 (PG-51 verified, env docs), 176 (deep debt: refactor, hardcoding, error types)

---

## Wave 175 — PG-51 Verified + Environment Variables Documentation

- **PG-51 RESOLVED UPSTREAM**: primalSpring confirmed Wave 173 family-scoped BearDog
  discovery is working live. No remaining issues.
- Created `docs/ENVIRONMENT_VARIABLES.md`: complete env var reference documenting the
  full security provider socket fallback chain (`SECURITY_PROVIDER_SOCKET` →
  `SECURITY_SOCKET` → `CRYPTO_PROVIDER_SOCKET` → XDG probing → `BEARDOG_SOCKET` →
  temp-dir fallback), CLI flag aliases, all network/IPC/capability env vars with defaults.
- Updated `README.md` with reference to the new doc.

## Wave 176 — Deep Debt: Large File Refactor, Hardcoding, Error Types

### Smart Refactored `information_layers.rs` (1121L → directory module)
- Split into `types.rs` (136L), `builders.rs` (214L), `tests.rs` (767L)
- **Zero files over 800 lines remain** across the workspace (largest: 763L)

### Hardcoded Fallback Elimination
- `RuntimeEndpointResolver::default_fallbacks()` now composes from `songbird_types::constants`
- Deprecated `DEFAULT_BIND_ADDRESS` const with `#[deprecated]` pointing to `get_bind_address()`

### `Result<_, String>` → `anyhow::Result`
- `validate_btsp_insecure_guard()` uses `anyhow::ensure!` instead of `Err(format!())`
- `start_service()` uses `anyhow::Context` instead of `.map_err(|e| format!(...))`

### Socket Path Centralization
- Added `security_provider_legacy_flat_path()` to `songbird_types::defaults::paths`
- Discovery code now uses centralized helper

---

## Validation

| Check | Result |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo test --workspace --lib` | 7,683 passed, 0 failures |
| Files >800L | 0 |

---

## Known Remaining Debt

- **Test coverage**: 73.41% (target 90%) — largest gap is integration/e2e coverage
- **BTSP Phase 3**: Encrypted framing (ChaCha20-Poly1305), blocked on BearDog key export
- **QUIC/TLS evolution**: Transitive `ring` in lockfile (not compiled), blocked on upstream
- **`#[allow(dead_code)]`**: ~30 items are reserved-for-future struct fields — intentional
- **Legacy primal names**: `beardog`, `toadstool`, `nestgate`, `squirrel` present only in
  deprecated backward-compatibility fallback chains with `tracing::warn!`
