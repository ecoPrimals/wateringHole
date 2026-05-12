# SPDX-License-Identifier: AGPL-3.0-only

# biomeOS v2.69 — Zero-Copy + Tokio Governance + Coverage Evolution

**Date**: March 28, 2026
**Version**: 2.69
**Supersedes**: v2.68 handoff (March 27, 2026)

---

## Summary

Continuation of the deep audit execution phase: zero-copy optimization on IPC hot
paths, dependency version governance (tokio workspace unification, base64 dedup),
`deny.toml` cleanup, targeted coverage expansion for weakest modules, and SPDX/rustdoc
compliance fixes. All five verification gates pass clean.

---

## Metrics

| Metric | Before (v2.68) | After (v2.69) |
|--------|-----------------|---------------|
| Tests | 7,135 | **7,160** (+25 new) |
| Clippy | PASS | **PASS** (0 warnings, pedantic+nursery) |
| Docs | PASS | **PASS** (0 warnings, `-D warnings`) |
| Formatting | PASS | **PASS** |
| cargo deny | PASS | **PASS** (advisories ok, bans ok, licenses ok, sources ok) |
| Hot-path `.clone()` | 2 `Value` subtree clones | **0** (`Value::take()`) |
| Hardcoded tokio versions | 11 crates | **0** (all `workspace = true`) |
| base64 version split | 0.21 + 0.22 | **0.22 unified** |
| deny.toml unused licenses | 3 (MPL-2.0, Unicode-DFS-2016, Zlib) | **0** |
| SPDX header gaps | 7 test modules | **0** |
| rustdoc warnings | 2 | **0** |

---

## Changes

### 1. Zero-Copy Hot-Path Evolution

**`biomeos-nucleus/src/discovery.rs`** — Both `discover_by_capability` and
`discover_by_family` cloned the entire `"primals"` JSON subtree before
`serde_json::from_value()`. Since `response` is owned, `Value::take()` moves the
subtree in-place with zero allocation.

**`biomeos-primal-sdk/src/provider.rs`** — `BiomeosProvider::fetch()` cloned
`response["result"]`. Evolved to `.take()` for zero-copy on every capability call.

### 2. Tokio Workspace Unification

Migrated 11 crates from hardcoded tokio version strings to `{ workspace = true }`:
- `biomeos-types`, `biomeos-system`, `neural-api-client` (deps + dev-deps)
- `biomeos-api`, `biomeos-deploy`, `biomeos-cli` (deps + dev-deps)
- `biomeos-boot`, `biomeos-atomic-deploy`, `biomeos-ui`
- Root `biomeos` package (deps + dev-deps)

This enforces single-source version governance. Workspace defines
`tokio = { version = "1.0", features = ["full"] }`.

### 3. base64 Version Unification

Unified `base64` from split 0.21/0.22 to 0.22 across all workspace crates.
Six crate Cargo.tomls migrated to `base64 = { workspace = true }`.

### 4. deny.toml Cleanup

Removed unused license allowances (`MPL-2.0`, `Unicode-DFS-2016`, `Zlib`) that
triggered `license-not-encountered` warnings during `cargo deny check`.

### 5. Coverage Expansion

**vm_federation** (was 39%): 10 new tests covering `benchscale_create_argv`,
`benchscale_subcommand_argv`, `topology_path_for_cli`, `validate_ssh_probe_output`
(success + failure), `collect_ips_for_vm_names` (mock, IO error, no IP),
`wait_for_vm_ssh_ready` (immediate success + max retries exceeded).

**trust** (was 42-52%): 3 new tests for all-variant serde roundtrip, copy semantics,
comprehensive Ord verification.

**constants/network** (env-driven branches): 14 new tests using `TestEnvGuard` to
exercise environment-variable-driven port functions (`http_port`, `https_port`,
`websocket_port`, `mcp_port`, `discovery_port`, `beardog_port`, `songbird_port`),
bind address functions, and `fallback_runtime_dir`.

### 6. SPDX + Rustdoc Fixes

- 7 test modules received `AGPL-3.0-only` SPDX headers
- `env_helpers.rs`: fixed public doc linking to private `ENV_MUTEX`
- `capability_taxonomy/definition.rs`: fixed broken intra-doc link path

### 7. Hardcoding Evolution

- `config_builder.rs`: production bind address → `endpoints::production_bind_address()`
- `config_builder.rs`: test port 8083 → `ports::TEST_DEFAULT`

---

## Dependency Audit Notes

- **thiserror 1.x vs 2.x**: Duplicate is entirely from transitive deps
  (netlink-proto → rtnetlink, opentelemetry → tarpc). Cannot be eliminated
  without upstream migration. Acceptable per `deny.toml` warn policy.
- **tokio-process 0.2**: Legacy dep from `biomeos-deploy`. Noted for future
  evolution to `tokio::process` (available in tokio `full`).
- **bincode v1**: Blocked by tarpc upstream. Tracked as known item.

---

## Clone Audit (Hot-Path Analysis)

Remaining `.clone()` calls in IPC/networking paths are categorized as **necessary**:
- `Arc::clone` for spawn boundaries and connection handlers
- `service.clone()` per tarpc accepted connection (required by tarpc model)
- Test-only clones for setup/spawn isolation

**Structural opportunities** identified but deferred (requires type changes):
- `Arc<str>` for event SSE string fields (events.rs)
- `Arc<CapabilityProvider>` for capability map entries
- Interned IDs for plasmodium aggregate maps

---

## Files Changed (28)

```
Cargo.toml, Cargo.lock, deny.toml
crates/biomeos-api/Cargo.toml
crates/biomeos-atomic-deploy/Cargo.toml
crates/biomeos-boot/Cargo.toml
crates/biomeos-cli/Cargo.toml
crates/biomeos-core/Cargo.toml
crates/biomeos-core/src/config_builder.rs
crates/biomeos-core/src/vm_federation/tests.rs
crates/biomeos-deploy/Cargo.toml
crates/biomeos-federation/src/nucleus/trust.rs
crates/biomeos-nucleus/src/discovery.rs
crates/biomeos-primal-sdk/src/provider.rs
crates/biomeos-spore/Cargo.toml
crates/biomeos-system/Cargo.toml
crates/biomeos-types/Cargo.toml
crates/biomeos-types/src/capability_taxonomy/definition.rs
crates/biomeos-types/src/constants/mod.rs
crates/biomeos-ui/Cargo.toml
crates/neural-api-client/Cargo.toml
crates/biomeos-test-utils/src/env_helpers.rs
crates/biomeos-api/src/handlers/discovery/tests.rs
crates/biomeos-api/src/lib_tests.rs
crates/biomeos-api/src/websocket_tests.rs
crates/biomeos-core/src/universal_biomeos_manager/discovery/tests.rs
crates/biomeos-graph/src/metrics/tests.rs
crates/biomeos-primal-sdk/src/capabilities/tests.rs
README.md, CURRENT_STATUS.md
```

---

## Verification

```bash
cargo fmt --all -- --check   # PASS
cargo clippy --workspace --all-targets   # PASS (0 warnings)
cargo test --workspace   # 7,160 passed, 0 failed
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps   # PASS
cargo deny check   # advisories ok, bans ok, licenses ok, sources ok
```

---

## Next Steps (Identified, Not Started)

- `tokio-process 0.2` → `tokio::process` migration in biomeos-deploy
- Structural `Arc<str>` evolution for SSE event fields (events.rs)
- `Arc<CapabilityProvider>` for capability routing maps
- Interned IDs for plasmodium aggregate maps
- Coverage push for remaining low-coverage modules (plasmodium/remote requires
  mock HTTP server, boot/rootfs requires hardware)
