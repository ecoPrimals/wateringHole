<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.45 — Deep Debt: Self-Knowledge Violations, Production Mocks, Dependency Cleanup

**Date**: 2026-04-08
**Author**: Agent (Cursor)
**Primal**: Squirrel
**Previous**: `SQUIRREL_V010A44_BTSP_INSECURE_GUARD_HANDOFF_APR08_2026.md`

---

## Summary

Comprehensive deep debt sprint addressing:
- 3 self-knowledge / hardcoding violations
- Production mock evolution (SDK WASM stubs, `DummyPluginManager`)
- 10 orphan workspace dependency removals
- Version alignment (`toml`, `glob`)
- Stale lint cleanup

## Changes

### Self-Knowledge Violations Fixed

1. **`BEARDOG_API_KEY` → `SECURITY_API_KEY`** (`crates/core/auth/src/providers.rs`)
   - `EncryptionService::new` and `ComplianceMonitor::new` now read `SECURITY_API_KEY` first, falling back to `BEARDOG_API_KEY` for legacy compat
   - Eliminates primal-specific env var in Squirrel's auth code

2. **`/tmp/token` → env-based resolution** (`crates/universal-patterns/src/security/providers/local.rs`)
   - Token path resolves: `SECURITY_TOKEN_FILE` → `$XDG_RUNTIME_DIR/biomeos/security.token` → `/tmp/biomeos-security.token`
   - No more hardcoded absolute path in production code

3. **`"primalspring"` → `primal_names::PRIMALSPRING`** (`crates/main/src/niche.rs`)
   - Added `PRIMALSPRING` constant + `display::PRIMALSPRING` to `universal-constants/primal_names.rs`
   - `niche.rs` DEPENDENCIES array now uses the constant consistently with all other entries

### Production Mock Evolution

4. **`DummyPluginManager` → `NoOpPluginManager`** (5 files)
   - Renamed to unit struct with honest documentation
   - "Returns errors for all lookups" — not a test double, but a legitimate default when no plugin system is configured

5. **SDK fs.rs WASM stubs** (`crates/sdk/src/client/fs.rs`)
   - `exists()` returns `false` (was `true` — lying)
   - `read_file_internal()` returns empty binary (was "Hello World" — fake data)
   - `upload_file()` returns `PluginError::McpError` (was fake upload ID)
   - All functions documented as "WASM sandbox stubs pending host wiring"

### Dependency Hygiene

6. **10 orphan workspace deps removed** from root `Cargo.toml`:
   `hex`, `uuid-serde`, `lru`, `indexmap`, `argon2`, `simple_logger`, `secrecy`, `tarpc-mcp`, `axum-mcp`, `axum-extra-mcp`

7. **rule-system version alignment**: `toml = "0.7"` → `toml.workspace = true` (0.8); `glob = "0.3"` → `glob.workspace = true`

8. **Stale lint**: removed `clippy::unnested_or_patterns` from SDK lib.rs `#[expect]`

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets` | PASS (0 warnings) |
| `cargo test --workspace` | PASS — 6,875 passed, 0 failed, 107 ignored |
| `cargo doc --workspace --no-deps` | PASS (0 errors) |

## Affected Files

| File | Change |
|------|--------|
| `crates/universal-constants/src/primal_names.rs` | Added `PRIMALSPRING` + display name + test coverage |
| `crates/main/src/niche.rs` | `"primalspring"` → `primal_names::PRIMALSPRING` |
| `crates/core/auth/src/providers.rs` | `BEARDOG_API_KEY` → `SECURITY_API_KEY` with fallback (2 sites) |
| `crates/universal-patterns/src/security/providers/local.rs` | `/tmp/token` → env-based resolution |
| `crates/universal-patterns/src/security/providers/tests.rs` | Registry test updated for dynamic token path |
| `crates/core/context/src/rules/mod.rs` | `DummyPluginManager` → `NoOpPluginManager` (struct + impl) |
| `crates/core/context/src/rules/actions.rs` | Rename references (8 sites) |
| `crates/core/context/src/rules/plugin.rs` | Rename references (7 sites) |
| `crates/core/context/src/rules/tests.rs` | Rename references |
| `crates/core/context/src/rules/plugin_tests.rs` | Rename references (16 sites) |
| `crates/sdk/src/client/fs.rs` | Stub evolution + test updates |
| `crates/sdk/src/lib.rs` | Removed stale lint expectation |
| `Cargo.toml` (root) | Removed 10 orphan workspace deps |
| `crates/tools/rule-system/Cargo.toml` | `toml`/`glob` → workspace |

## Remaining Known Gaps

- **Legacy env var aliases** (`SONGBIRD_*`, `TOADSTOOL_*`, `NESTGATE_*`): present as documented `.or_else()` fallbacks across config loaders; migration path to pure capability-domain names is tracked
- **`SONGBIRD_SOCKET_NAME`**: deprecated but retained for backward compat in `primal_names.rs`
- **Files >800 lines**: 15+ production files over 800 lines; smart refactoring opportunities remain (test extraction, domain decomposition)
- **GAP-MATRIX-05 residual**: Socket/daemon mode not yet live-tested through biomeOS Neural API routing

## References

- Wire Standard: `infra/wateringHole/CAPABILITY_WIRE_STANDARD.md`
- BTSP: `infra/wateringHole/BTSP_PROTOCOL_STANDARD.md`
- Self-Knowledge: `infra/wateringHole/PRIMAL_SELF_KNOWLEDGE_STANDARD.md`
