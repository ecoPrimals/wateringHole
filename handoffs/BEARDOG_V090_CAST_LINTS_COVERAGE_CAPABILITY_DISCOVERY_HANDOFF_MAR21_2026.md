# BearDog v0.9.0 — Cast Lint Tightening, Coverage Push & Capability-Based Discovery Handoff

**Date**: March 21, 2026
**Primal**: BearDog (cryptographic service provider)
**Session Focus**: Code quality hardening — cast lint evolution, coverage push, capability-based IPC discovery

---

## What Changed

### Cast Lint Evolution

Removed all 5 global `allow(clippy::cast_*)` entries from workspace `Cargo.toml`. All 301 cast
sites across the entire workspace now use either:

- `Type::from(x)` / `.into()` for lossless casts (34 sites — proper semantic fix)
- Per-site `#[expect(clippy::cast_*, reason = "...")]` for intentional casts (267 sites)

Cast lints are now `warn` at workspace level. New casts must annotate individually. The `#[expect]`
attribute fails compilation if the lint is NOT triggered, preventing stale annotations.

### Capability-Based Discovery

Hardcoded primal names (`biomeos`, `songbird`, etc.) in production IPC paths were replaced with
configurable, capability-aware resolution:

- `BIOMEOS_IPC_NAMESPACE` env var (default `biomeos`) for IPC subdirectory
- `PRIMAL_NAME` / `BEARDOG_PRIMAL_NAME` for socket stem (default `beardog`)
- `BIOMEOS_TMP_ROOT` for non-XDG tmp socket fallback
- `SongbirdClient::connect` now uses `IpcSocketDiscoveryOptions::from_env()` capability discovery
- Platform-specific (Android abstract, Windows pipe, Unix listen) paths all respect env overrides

Type names like `SongbirdClient` preserved for API stability; runtime connection follows discovery.

### Coverage Push

| Metric | Before | After |
|--------|--------|-------|
| Region coverage | 84.2% | 85.3% |
| Line coverage | 84.8% | 85.7% |
| Tests passing | 13,555 | 13,853 |
| Tests added | — | ~300 |

New tests across: CLI handlers (daemon, key_derive, key_export, entropy, HSM, streaming, birdsong,
kdf, key_revoke), tunnel crypto (TLS 1.2, Tor ntor, AES-GCM, BTSP, beacon, genetic enrollment,
ECDH, hashing, KDF), core (key_management, interaction_capture, primal_discovery), library crates
(capabilities, discovery, config hierarchy, types, auth genetics, threat conditions, monitoring,
compliance, installer).

### Test Stability

- Added `serial_test::serial` to all env-dependent tests in `beardog-capabilities`
- Eliminated intermittent test-pollution failures from parallel env var races

### Documentation

- All `rustdoc::broken_intra_doc_links` resolved; `RUSTDOCFLAGS="-D warnings" cargo doc` clean
- 17 reference/guide docs moved from repo root to `docs/references/`
- 335 session log files moved from `docs/sessions/` to `archives/sessions/`
- Tracked receipts removed from git (already in `.gitignore`)

---

## Quality Gates (all passing)

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-features -- -D warnings` | Clean (includes cast lints) |
| `cargo doc --workspace --all-features --no-deps -D warnings` | Clean |
| `cargo test --workspace --all-features` | 13,853 passed, 0 failed |
| Files > 1000 lines | 0 |
| `cargo deny check` | All 4 pass |

---

## Next Steps

- **Coverage to 90%** — Remaining uncovered code is integration-heavy (IPC handlers, HSM
  hardware paths, TUI interaction capture, daemon lifecycle). Reaching 90% needs mock server
  infrastructure or integration test harnesses.
- **genomeBin integration** — Manifest pinning with `ecoPrimals/plasmidBin/` not yet wired.
- **AGPL-3.0-only vs -or-later** — `wateringHole` docs reference both; team decision needed.
- **Integration tests** — E2e tests for full socket I/O paths, HSM hardware, encrypted export
  CLI paths.

---

## Verification Commands

```bash
cargo fmt --check
cargo clippy --workspace --all-features -- -D warnings
cargo test --workspace --all-features
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps
cargo deny check
cargo llvm-cov --workspace --all-features --summary-only
```
