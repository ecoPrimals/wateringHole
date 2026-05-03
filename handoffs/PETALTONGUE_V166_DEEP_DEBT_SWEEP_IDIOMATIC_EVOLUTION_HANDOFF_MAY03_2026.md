# petalTongue v1.6.6 — Deep Debt Sweep & Idiomatic Evolution

**Date**: May 3, 2026
**Version**: 1.6.6
**Primal**: petalTongue
**Session Type**: Comprehensive audit + deep debt cleanup

---

## Summary

Full codebase audit against wateringHole standards followed by systematic debt
elimination. All quality gates now pass with `--all-features` — a significant
hardening since CI previously only tested default features.

## Changes (30 files, -427/+166 lines net)

### Clippy `--all-features` Clean (25+ lints fixed)

Ran `cargo clippy --workspace --all-features -- -D warnings` for the first time
with all features enabled, surfacing lints previously hidden behind feature gates:

- **`map_unwrap_or`** (12 files): `.map().unwrap_or()` → `.map_or()` /
  `.map_or_else()` / `.is_ok_and()` — modern idiomatic Rust
- **`duration_suboptimal_units`** (5 files): `Duration::from_secs(60)` →
  `Duration::from_mins(1)` — Rust 1.95 lint
- **`sort_by` → `sort_by_key`** (4 files): idiomatic sort pattern
- **Stale `#[expect(dead_code)]`** (motor_state.rs): evolved to `#[allow]`
- **Trailing commas** removed (2 files)

### UniBin v1.1 `--port` Compliance

Web and Headless modes now accept `--port <PORT>` per UniBin Architecture
Standard v1.1. `--bind` takes precedence over `--port`. Added `resolve_bind()`
helper with bind > port > config default precedence. 4 new tests cover flag
parsing and precedence.

### Dead Code Elimination

- Deleted `audio_web.rs` (301 lines) — depended on `web_audio_api` crate not
  in Cargo.toml, never wired into module tree. Completely dead.

### Doc Link Fixes

- Fixed 4 broken intra-doc links (TextureRegistry, InputAdapter, SocketBackend,
  DirectBackend) and 2 unclosed HTML tags in doc comments.

### Hardcoding Evolution

- Tests in headless_mode.rs and web_mode.rs now use `constants::default_*_bind()`
  and named port constants instead of literal `"0.0.0.0:8080"` strings.

### CI Hardening

- clippy: `--all-features` added
- test: `--all-features` (was `--lib` only)
- doc: new step with `RUSTDOCFLAGS="-D warnings"`

### Root Doc Updates

- README.md: quality table updated, --port examples, --all-features commands
- CHANGELOG.md: full session entry
- web/index.html: "6 subcommands" → "7 subcommands"

## Current State

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-features -D warnings` | PASS (0) |
| `cargo test --workspace --all-features` | PASS (6,200+, 0 failures) |
| `cargo doc --workspace --no-deps` | PASS (0 warnings) |
| `cargo llvm-cov --workspace --lib` | 85.2% line coverage |
| Release build (clean) | 57s |
| Max file size | 714 lines |
| Unsafe blocks | 0 |
| TODO/FIXME/HACK | 0 |

## Standards Compliance

| Standard | Status |
|----------|--------|
| AGPL-3.0-or-later + scyBorg Trio | COMPLIANT |
| UniBin (single binary, --port) | COMPLIANT (v1.1) |
| ecoBin (pure Rust, no C deps) | COMPLIANT |
| JSON-RPC 2.0 primary + tarpc secondary | COMPLIANT |
| Capability-based discovery | COMPLIANT |
| Standalone startup | COMPLIANT |
| Files < 1000 lines | COMPLIANT (max 714) |
| No TODO/FIXME/HACK | COMPLIANT |
| Workspace dependency management | COMPLIANT |
| Semantic method naming | COMPLIANT |
| Sovereignty (no cross-primal imports) | COMPLIANT |

## Remaining Work

### Coverage (85.2% vs 90% target)

64 files below 80%, concentrated in `petal-tongue-ui` display/backend/integration
code. Lowest: panel_registry/factory (17%), biomeos_integration/provider_trait (21%),
app/events (23%). These modules require runtime environments (egui context,
framebuffer, display servers) for meaningful testing — headless harness expansion
is the path forward.

### Future Evolution Targets

- Expand headless harness to cover display backend initialization paths
- `bytes::Bytes` zero-copy expansion to remaining data pipelines
- `CONTRIBUTING.md` as standalone file (currently embedded in README)
- Advisory ignore review when upstream tarpc/bytes update

## Mocks/Fixtures Status

All mock code is properly isolated:
- `demo_provider`: `#[cfg(any(test, feature = "test-fixtures"))]`
- `sandbox_provider`: `#[cfg(any(test, feature = "mock"))]`
- `DemoDeviceProvider`: `#[cfg(feature = "mock")]`
- `sandbox/mock-biomeos/`: standalone development server, not compiled into main binary

## Dependencies

All production deps are pure Rust. `deny.toml` bans: ring, openssl, openssl-sys,
native-tls, aws-lc-sys, zstd-sys, lz4-sys, libsqlite3-sys, cryptoki-sys.
Two advisory ignores pending upstream: RUSTSEC-2024-0387 (tarpc transitive),
RUSTSEC-2025-0141 (bytes transitive).
