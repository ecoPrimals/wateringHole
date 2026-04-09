# Squirrel v0.1.0-alpha.46 — Deep Debt Cleanup: BTSP Phase 2, Dependency Evolution, Smart Refactoring

**Date**: April 9, 2026
**Scope**: BTSP Phase 2 handshake-on-accept, production stub evolution, large file refactoring, dependency purge, doc ground truth
**Tests**: 7,203 passing (0 failures) | **Clippy**: 0 warnings | **fmt**: PASS | **doc**: PASS

---

## BTSP Phase 2 — Handshake-on-Accept (Wire Standard L2)

New module `crates/main/src/rpc/btsp_handshake.rs` implements server-side BTSP handshake per `BTSP_PROTOCOL_STANDARD.md` v1.0.

| Step | Description |
|------|-------------|
| 1 | Read `ClientHello` (protocol version, cipher suites) |
| 2 | Generate 32-byte challenge, send `ServerHello` (selected cipher, challenge) |
| 3 | Delegate crypto to BearDog via `btsp.session.create` / `btsp.session.verify` IPC |
| 4 | Read `ChallengeResponse`, verify, send `HandshakeComplete` |

- Conditional on `FAMILY_ID` set (production mode); dev mode bypasses
- Integrated into both `start()` (UniversalListener) and `accept_filesystem_socket()` (UnixListener)
- Wire framing: 4-byte big-endian length prefix per BTSP spec
- Phase 2 cipher: `BTSP_NULL` (authenticated plaintext); Phase 3 cipher negotiation pending
- 17 tests covering frame roundtrips, error handling, multi-frame sequencing

## Production Stub Evolution

| Component | Before | After |
|-----------|--------|-------|
| `OperationHandler.connected` | `dead_code` expect, `with_connection()` set `false` | Field read in all methods; `with_connection()` sets `true`; `is_connected()` accessor |
| `MCPAdapter.config` | `dead_code` expect | Wired into error messages and `discover_capabilities` structured logging |
| `PluginManager.dependency_resolver` | `dead_code` expect | Wired: plugins registered on add, `resolve_dependencies()` called in `init()` |
| `LearningManager.observe_contexts` | `Vec::new()` placeholder | `manager.list_sessions().await` + `get_context_state()` with fallback |

## Smart Large File Refactoring

| File | Before | After | Method |
|------|--------|-------|--------|
| `session/mod.rs` | 892 | 380 | Tests → `session_tests.rs` |
| `transport/client.rs` | 884 | 529 | Tests → `client_tests.rs` |
| `context_state.rs` | 896 | 505 | DTOs → `context_state_types.rs` |
| `api.rs` | 906 | 445 | DTOs → `api_types.rs`, tests → `api_tests.rs` |

Pattern: `#[cfg(test)] #[path = "..."] mod tests;` (matches existing codebase convention).

## Dependency Evolution

| Action | Crate | Reason |
|--------|-------|--------|
| **Removed** | `pprof` | 0 code references; deny.toml documents samply migration |
| **Removed** | `openai` (crate) | 0 code references; AI routing uses IPC/capability discovery |
| **Removed** | `libloading` | 0 code references; `plugins` feature emptied |
| **Evolved** | `flate2` | `default-features = false, features = ["rust_backend"]` — pure Rust miniz_oxide |
| **Retained** | `nvml-wrapper` | Feature-gated (`nvml`); wraps NVIDIA driver (no pure-Rust alternative) |
| **Retained** | `nix` | Unix syscall wrappers; widely used for `getuid()` / `gethostname()` |
| **Retained** | `zstd`, `lz4` | Feature-gated (`compression`); no code yet, future-use |

## Self-Knowledge Audit

- Production code uses `universal_constants::primal_names::*` constants for all primal references
- `PrimalType::as_str()` delegates to `primal_names::*` constants
- Port defaults centralized in `universal_constants::deployment::*` with env-var overrides
- Remaining raw primal name strings are in test assertions and doc comments only

## Doc Ground Truth

| Document | Updates |
|----------|---------|
| `README.md` | Tests 6,875→7,203 |
| `CURRENT_STATUS.md` | Version alpha.45→46, date Apr 8→9, tests 7,203, dep cleanup, file refactoring list |
| `CONTEXT.md` | Version alpha.46, tests 7,203 |
| `CHANGELOG.md` | New alpha.46 entry |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo test --all-features` | 7,203 passed, 0 failed |
| `cargo doc --all-features --no-deps` | PASS |
| Unsafe code | 0 (`unsafe_code = "forbid"`) |
| TODO/FIXME/HACK | 0 |
| Files >1000 LOC | 0 |
| Production mocks | 0 |

## What Remains

- Zero blocking debt
- BTSP Phase 3: cipher negotiation (pending BearDog `btsp.negotiate` method)
- `async_trait` → native async fn migration (tracked in `docs/DYN_DEPRECATION_ROADMAP.md`)
- Ecosystem blocker: BTSP Phase 2 rollout cascade (Songbird → NestGate → ToadStool)
- plasmidBin: Squirrel binary rebuilt and updated (alpha.46); other primals pending

---

**Squirrel**: v0.1.0-alpha.46 | **Tests**: 7,203 | **Clippy**: PASS | **License**: scyBorg (AGPL-3.0-or-later + ORC + CC-BY-SA 4.0)
