<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.13 — Cross-Ecosystem Absorption Handoff

**Date**: March 18, 2026
**Sprint**: Cross-ecosystem absorption — MCP tool discovery, capability-first
sockets, centralized RPC extraction, ecoBin 14-crate ban, primal display names
**Tests**: 5,599 passing | **Coverage**: 71% | **Clippy**: 0 warnings | **TODOs**: 0

---

## Part 1: What Changed

### P1 — Critical (Ecosystem Wire-Up)

| Change | Detail |
|--------|--------|
| `capability.list` method name | Fixed typo `capabilities.list` → `capability.list` in `capability_crypto.rs` |
| Capability-first socket paths | `security.sock`/`crypto.sock` now preferred over `beardog.sock` — primals discover capabilities, not other primals |
| Spring MCP tool discovery | New `spring_tools.rs` module: runtime `mcp.tools.list` discovery from domain springs via socket registry; 60s TTL cache |
| `tool.list` enriched | Response now includes tools discovered from springs alongside builtins and announced tools |
| `tool.execute` routing | Checks spring routing table for forwarding before local execution |

### P2 — Ecosystem Absorption

| Change | Detail |
|--------|--------|
| `extract_rpc_result()` centralized | New function in `universal-patterns::ipc_client`; replaces 5 ad-hoc `.get("result")` extraction sites in `handlers_tool.rs`, `universal_adapter_v2.rs`, `anthropic.rs`, `openai.rs`, `adapter.rs` |
| ecoBin 14-crate ban list | `deny.toml` expanded from 2 to 14 banned crates: `openssl-sys`, `openssl`, `native-tls`, `aws-lc-sys`, `aws-lc-rs`, `ring`, `libz-sys`, `bzip2-sys`, `curl-sys`, `libsqlite3-sys`, `cmake`, `cc`, `pkg-config`, `vcpkg` — per groundSpring V115 |
| Consumed capabilities | 14 → 22: added `secrets.store/retrieve/list/delete` (BearDog), `compute.dispatch.capabilities/cancel` (ToadStool S158b), `model.exists` (NestGate 4.1), `mcp.tools.list` (domain springs) |
| 6 proptest IPC fuzz tests | `parse_request_never_panics`, `parse_capabilities_never_panics`, `extract_rpc_result_never_panics`, `extract_rpc_error_never_panics`, `dispatch_method_name_never_panics` |

### P3 — Quality of Life

| Change | Detail |
|--------|--------|
| `primal_names` module | `universal-constants::primal_names` with 13 machine IDs, `display` submodule with branded names (`BearDog`, `ToadStool`, `biomeOS`, etc.), `display_name()` lookup |

---

## Part 2: Absorption Sources

| Pattern | Source | Squirrel Adoption |
|---------|--------|--------------------|
| `mcp.tools.list` schema | healthSpring V37, wetSpring V128 | `spring_tools::SpringToolDiscovery` for runtime tool aggregation |
| `extract_rpc_result()` | wetSpring V127, healthSpring V37 | Centralized in `universal-patterns`, 5 migration sites |
| 14-crate C-dep ban | groundSpring V115 | Full adoption in `deny.toml` |
| `secrets.*` capabilities | BearDog latest | Added to `CONSUMED_CAPABILITIES` |
| `compute.dispatch.capabilities/cancel` | ToadStool S158b | Added to `CONSUMED_CAPABILITIES` |
| `model.exists` | NestGate 4.1 | Added to `CONSUMED_CAPABILITIES` |
| Proptest IPC fuzz | healthSpring V37, ludoSpring V24 | 6 new property-based fuzz tests |
| `display` names | neuralSpring V118 | `primal_names::display` module |
| Capability-first sockets | BearDog / Songbird pattern | `security.sock`/`crypto.sock` preferred over primal-named sockets |

---

## Part 3: Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all` | PASS |
| `cargo clippy --all-features --all-targets -D warnings` | PASS (0 warnings) |
| `cargo doc --all-features --no-deps` | PASS (0 warnings) |
| `cargo test --all-features` | PASS (5,599 tests, 0 failures) |
| Files > 1000 lines | 0 (max: 999 — `ipc_client.rs`) |
| TODO/FIXME in code | 0 |
| Mocks in production | 0 |
| Unsafe code | 0 (`#![forbid(unsafe_code)]`) |
| C dependencies | 0 (14 crates banned in `deny.toml`) |
| Hardcoded primal names in production | 0 |

---

## Part 4: Patterns Worth Adopting

1. **`extract_rpc_result()` centralization** — every primal doing ad-hoc `val.get("result")` should switch to the centralized extractor. Prevents silent data loss when error responses are ignored.

2. **Capability-first socket naming** — prefer `security.sock`, `crypto.sock`, `storage.sock` over primal-named sockets. A primal discovers capabilities, not identities.

3. **Spring tool discovery** — any primal coordinating tools should call `mcp.tools.list` on discovered springs and merge into its own tool list. The routing table pattern (`tool_id → socket_path`) enables transparent forwarding.

4. **`deny.toml` 14-crate ban** — portable ecoBin compliance. Copy the deny list from this or groundSpring V115.

5. **`primal_names::display`** — use for UI/logging instead of ad-hoc capitalization.

---

## Part 5: Known Issues

1. `chaos_07_memory_pressure` — flaky under parallel test load (environment-sensitive)
2. Coverage at 71% — gap to 90% target; incremental expansion underway
3. `adapter.rs` (974L) — unwired legacy protocol module

---

## Part 6: Files Changed

### New Files
- `crates/main/src/rpc/spring_tools.rs` — spring MCP tool discovery
- `crates/universal-constants/src/primal_names.rs` — primal machine IDs + display names

### Modified Files
- `crates/core/auth/src/capability_crypto.rs` — capability-first sockets + method name fix
- `crates/main/src/niche.rs` — 8 new consumed capabilities
- `crates/main/src/rpc/handlers_tool.rs` — spring tool integration + `extract_rpc_result`
- `crates/main/src/rpc/mod.rs` — wired `spring_tools` module
- `crates/main/src/universal_adapter_v2.rs` — `extract_rpc_result` migration
- `crates/main/src/api/ai/adapters/anthropic.rs` — `extract_rpc_result` migration
- `crates/main/src/api/ai/adapters/openai.rs` — `extract_rpc_result` migration
- `crates/main/src/api/ai/adapter.rs` — `extract_rpc_result` migration
- `crates/main/src/universal_primal_ecosystem/mod.rs` — `extract_rpc_result` migration
- `crates/universal-patterns/src/ipc_client.rs` — added `extract_rpc_result()` + 4 tests
- `crates/universal-patterns/src/lib.rs` — exported `extract_rpc_result`
- `crates/universal-constants/src/lib.rs` — wired `primal_names` module
- `crates/main/tests/proptest_roundtrip.rs` — 6 new IPC fuzz tests
- `deny.toml` — expanded to 14-crate ecoBin ban list
- `README.md` — updated test count
- `CHANGELOG.md` — alpha.13 entry
- `CURRENT_STATUS.md` — alpha.13 metrics

---

**Squirrel v0.1.0-alpha.13 | 22 crates | 5,599 tests | 71% coverage | AGPL-3.0-only**
