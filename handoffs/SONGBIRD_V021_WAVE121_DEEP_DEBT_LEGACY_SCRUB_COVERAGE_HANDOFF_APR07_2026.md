# Songbird v0.2.1 — Wave 121: Deep Debt, Legacy Name Scrub, Coverage Expansion

**Date**: April 7, 2026
**Primal**: songBird
**Previous**: Wave 120 (archived)

---

## Summary

Wave 121 addressed remaining deep debt: legacy primal name references evolved to capability-based with deprecated fallbacks, hardcoded legacy socket paths replaced with XDG-first discovery, coverage expanded across 8 sub-10% modules, and 2 large test files refactored into domain modules. Zero files over 800 lines.

## Legacy Primal Name Scrub

### TLS Socket Discovery (`songbird-tls/src/crypto.rs`)
- Discovery order now: `SECURITY_PROVIDER_SOCKET` env → `$XDG_RUNTIME_DIR/biomeos/security.sock` → `BIOMEOS_SOCKET` → legacy `/var/run` paths with `tracing::warn!("using legacy socket path")`

### Capability Strategy (`songbird-universal-ipc/src/capability/strategy.rs`)
- `XDG_RUNTIME_DIR` now searched BEFORE `/var/run` in filesystem discovery

### NFC Config (`songbird-nfc/src/config.rs`)
- `beardog.sock` path segment → `security.sock`

### Config Environment (`songbird-config`)
- `toadstool_endpoint` / `squirrel_endpoint` → `compute-provider` / `ai-provider` as primary, legacy as deprecated aliases
- Env var resolution: `*_PROVIDER_*` first, then `*_ENDPOINT`, then legacy (`TOADSTOOL_*`, `SQUIRREL_*`) with deprecation warnings

## Coverage Expansion (+39 tests)

New tests across 8 previously sub-10% modules:
- `songbird-tls/src/server.rs` — handshake error paths
- `songbird-cli/src/cli/ui.rs` — formatting, tables, display helpers
- `songbird-http-client` — `aead.rs` validation, `hash.rs` decode, `tls_secrets.rs` roundtrip
- `songbird-remote-deploy/src/deploy/tower.rs` — address parsing
- `songbird-observability/dashboard.rs` — analytics statistics
- `songbird-tor-protocol/src/crypto/mod.rs` — error mapping

## File Refactoring

- `load_balancer_error_paths_tests.rs` (851L) → 9 submodules (max 162L each)
- `storage_tests.rs` (813L) → 3 submodules (max 354L each)
- **Zero files over 800 lines** across entire workspace

## Lint Hygiene

- `#[allow(missing_docs)]` on `lib.rs` module declarations given explicit reason strings
- `storage_sled` test modules converted to `#[expect]`

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 12,772 | 12,811 |
| Line coverage | 72.16% | 72.29% |
| Files >800L | 2 | 0 |
| Legacy socket paths (hardcoded) | 3 locations | 0 (XDG-first, legacy as last resort with warn) |

## Verification

- `cargo fmt --all -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 12,811 passed, 0 failed
- `cargo deny check` — advisories ok, bans ok, licenses ok, sources ok
