<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Coverage 90%, Smart Refactoring, Dependency Evolution

**Date**: April 16, 2026
**Primal**: Squirrel (AI Coordination)
**Sessions**: X (coverage push) + Y (deep debt)
**Commit range**: `45de7807..b93e8ca7`

---

## Executive Summary

Two sessions achieving the **90% coverage target**, completing **smart refactoring** of all oversized production files, deepening **primal self-knowledge** naming, and evolving **C dependencies to pure Rust**.

---

## Session X — Coverage 86%→90.1%

### Coverage Target Met

| Metric | Before | After |
|--------|--------|-------|
| Region coverage | 88.98% | **90.10%** |
| Function coverage | 87.21% | 88.31% |
| Line coverage | 88.57% | 89.64% |
| Tests passing | 7,012 | 7,156 |

**144 new tests** across 15 production modules targeting highest missed-region files:
- jsonrpc_server, sdk/mcp/client, ai/router, sdk/plugin, btsp_handshake
- monitoring_provider, learning/manager, discovery, cli/config, cli/security
- ai/adapter, rule-system/manager, rule-system/evaluator, universal-patterns/config
- interning, universal_adapter_v2, ipc_routed_providers, shutdown, sdk/logging

### Real Bugs Found via Testing

1. **`set_rule_manager` held `RwLock::write()` across `await`** — deadlock risk under concurrent access. Fixed by splitting the critical section.
2. **`load_from_file` nested JSON branch silently discarded data** — `self.models` was not updated. Fixed to assign parsed registry.
3. **SDK `error/tests.rs` was 0% coverage** (334 missed regions) — tests used `#[wasm_bindgen_test]` only. Fixed with dual `#[test]` + `#[wasm_bindgen_test]` macro.

---

## Session Y — Deep Debt, Refactoring, Dependencies

### Smart Refactoring — 7 Production Files Under 800L

| File | Before | After | Extracted |
|------|--------|-------|-----------|
| `discovery.rs` | 945 | 596 | Tests → `discovery_tests.rs` |
| `http.rs` | 866 | 586 | HTTP types → `http_types.rs` (294L) |
| `config.rs` | 856 | 266 | Types → `config_types.rs`, tests → `config_tests.rs` |
| `btsp_handshake.rs` | 855 | 306 | Wire protocol → submodule + `btsp_handshake_wire.rs` |
| `adapter.rs` | 847 | 292 | Tests → `adapter_tests.rs` |
| `security.rs` | 816 | 377 | Tests → `security_tests.rs` |
| `ipc_routed_providers.rs` | 805 | 373 | Parsers + mocks + tests extracted |

**Combined with session W**: 12 production files smart-refactored. **0 production files >800L.**

### Primal Self-Knowledge Deepening

**BearDog → SecurityProvider:**
- `BeardogAuthContext`/`Permission`/`Session` → `SecurityProvider*` (deprecated aliases)
- `AuthMethod::Beardog` → `::SecurityProvider` with `serde(alias = "beardog")`
- `BeardogSecurityProvider` → `SecurityProviderIntegration`
- `create_beardog_client` → `create_security_provider_client`
- Config builder: `beardog_*` → `security_provider_*`

**Songbird → Discovery:**
- `SONGBIRD_SOCKET_NAME` deprecated for `DISCOVERY_SOCKET_NAME`
- Monitoring provider: `SONGBIRD` → `SERVICE_MESH_CAPABILITY`
- Env chains: `DISCOVERY_*` before `SONGBIRD_*` everywhere

**ToadStool → Compute:**
- Env chains: `COMPUTE_ENDPOINT` before `TOADSTOOL_ENDPOINT`

**Hardcoded ports:**
- All `localhost:8080`/`9090` → `get_service_port()` constants in production code

### Dependency Evolution

| Change | Impact |
|--------|--------|
| `nvml-wrapper` removed | GPU monitoring is ToadStool's responsibility, not Squirrel's |
| `nix` → `rustix` | Pure Rust Linux syscalls (hostname, UID) — no libc FFI |
| `zstd` | Documented as optional C exception (behind `compression` feature only) |
| `blake3` added to plugins | Content-addressed plugin dependency IDs (deterministic, not random UUIDs) |

### Mock Evolution

- Plugin discovery: random `Uuid::new_v4()` → deterministic **BLAKE3 content-addressed** IDs
- WASM FS stubs: documented as **capability-absent design** (not mocks)
- `SecurePluginStub`: documented as **security policy** (deny-native-execution)

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,158 passing / 0 failures |
| Coverage | 90.1% region / 89.6% line |
| `.rs` files | ~1,037 |
| Production files >800L | 0 |
| `async-trait` | 0 usage |
| `unsafe` code | 0 (forbid) |
| Clippy | 0 warnings (`-D warnings`, pedantic+nursery) |
| `cargo deny` | PASS (advisories, bans, licenses, sources) |
| `cargo fmt` | PASS |
| ecoBin | 3.5 MB pure Rust static-pie |

---

## Remaining Blocked Items

1. **Three-tier genetics adoption** — awaits `ecoPrimal >= 0.10.0` with `mito_beacon_from_env()`. Groundwork laid (comments, roadmap docs in btsp_handshake).
2. **Content curation via BLAKE3** — pure BLAKE3 in tree. Blocked on NestGate content-addressed storage API stability.
3. **Phase 3 cipher negotiation** — blocked on BearDog server-side `btsp.negotiate`.
4. **Wire compliance L2→L3** — Squirrel at L2/partial in PRIMAL_GAPS table. Needs full composable capability surface.

---

## Files Changed

- **Session X**: 40 files changed, 3,339 insertions
- **Session Y**: 56 files changed (12 new extraction files created)
- **Root docs**: README, CONTEXT, ORIGIN, CHANGELOG, CRYPTO_MIGRATION, CURRENT_STATUS all refreshed

---

*Handoff by Cursor agent — April 16, 2026*
