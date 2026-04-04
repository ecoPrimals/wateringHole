# toadStool S176-177 — Capability-Based Evolution + Deep Debt

**Date**: April 4, 2026
**Session**: S176-177 (deep debt evolution, capability-based naming migration)
**Status**: All quality gates green. 21,624 tests, 0 failures.
**Previous**: `TOADSTOOL_S175_UNSAFE_REDUCTION_PHASE12_HANDOFF_APR03_2026.md` (archived)

---

## Summary

Two consecutive sessions executing deep debt: deprecated API removal, semantic method
evolution, env_config primal name migration, deprecated socket/IPC cleanup, and 10 large
file smart-refactors. The codebase is now predominantly capability-named rather than
primal-named in its internal APIs.

---

## S176 Changes — Deep Debt Evolution

### Deprecated API Removal

| Item | Before | After |
|------|--------|-------|
| `config/network.rs` primal functions | 15 deprecated (`default_songbird_endpoint`, etc.) | **Removed** — callers use `capability_fallback` ports |
| `constants::ports` module | Present (zero callers) | **Removed** |
| `ConfigUtils` wrapper methods | `get_songbird_port` etc. | **Removed** — use `get_primal_default_port()` |

### Semantic Method Evolution

| Item | Before | After |
|------|--------|-------|
| Handler names | `ollama_list_models`, `ollama_inference`, etc. | `inference_list_models`, `inference_execute`, etc. |
| Deprecated aliases | — | `ollama.*` routing aliases still resolve |

### Large File Smart Refactoring (5 files)

| File | Lines | New Structure |
|------|-------|---------------|
| `capability_discovery.rs` | 686 | `{mod, types, tests}.rs` |
| `multi_workload_compositor.rs` | 643 | `{mod, types, scheduling, merging, tests}.rs` |
| `primal_capabilities.rs` | 640 | `{mod, parsing, registry, tests}.rs` |
| `mdns_discovery.rs` | 635 | `{mod, client, parser, tests}.rs` |
| `songbird_integration/integration.rs` | 661 | Extracted `messaging.rs`, `transport.rs`, `capacity.rs` |

### Dead Code Resolution (12 items)
- `parse_size_string` → moved to test scope
- `HardwareDetector::system_info` → removed (always `None`)
- `EntropyClient::endpoint` → removed (never read)
- `mdns_to_discovered_service` → moved to test scope
- 8 items evolved to `#[allow(dead_code, reason = "...")]`

### Other
- `std::fs` → `tokio::fs` in `serve_unix` async function
- Akida stub models feature-gated behind `cfg(any(test, feature = "dev-stubs"))`

---

## S177 Changes — Capability-Based Naming Evolution

### env_config Primal Name Migration (14 files)

| Field | Before | After |
|-------|--------|-------|
| `songbird_port` | Deprecated, primal-named | `coordination_port` + `#[serde(alias)]` |
| `beardog_port` | Deprecated, primal-named | `security_port` + `#[serde(alias)]` |
| `nestgate_port` | Deprecated, primal-named | `storage_port` + `#[serde(alias)]` |
| `squirrel_port` | Deprecated, primal-named | `ai_processing_port` + `#[serde(alias)]` |

Endpoint methods renamed similarly. `apply_to_config()` now uses capability-named methods
directly.

### Deprecated Socket API Removal (7 files)

| Function | Action |
|----------|--------|
| `get_beardog_socket_path()` | **Removed** → `get_socket_path_for_capability("crypto")` |
| `get_songbird_socket_path()` | **Removed** → `get_socket_path_for_capability("coordination")` |
| `get_nestgate_socket_path()` | **Removed** → `get_socket_path_for_capability("storage")` |
| `get_socket_path_for_service()` | **Removed** → `get_socket_path_for_capability()` |
| `get_squirrel_socket_path()` | **Renamed** → `get_routing_socket_path()` |

### IPC Helpers Cleanup (5 files)

| Function | Action |
|----------|--------|
| `connect_to_primal()` | **Removed** (zero production callers) |
| `resolve_primal()` | **Removed** (zero production callers) |
| Modern API | `find_by_capability()` |

### Large File Smart Refactoring (5 more files)

| File | Lines | New Structure |
|------|-------|---------------|
| `provider_registry/mod.rs` | 749 | `mod.rs` (35L) + `tests.rs` (714L) |
| `monitoring/lib.rs` | 712 | `lib.rs` (30L) + `tests.rs` (683L) |
| `protocols/client/mod.rs` | 675 | `protocol_client.rs` + `tests.rs` |
| `display/input/parser.rs` | 674 | `parser/{mod, keyboard, mouse, absolute_sync, tests}.rs` |
| `config_bases.rs` | 667 | `config_bases/{mod, timeout, health, resources_validation, endpoint_retry_pool, cache_telemetry, tests}.rs` |

---

## Verification

```
cargo clippy --workspace --all-targets -- -D warnings   # 0 warnings
cargo test --workspace                                   # 21,624 passed, 0 failed
```

## Remaining Active Debt

| ID | Crate | Description |
|----|-------|-------------|
| D-TARPC-PHASE3 | integration/protocols | tarpc binary transport not wired |
| D-EMBEDDED-PROGRAMMER | runtime/specialty | Placeholder ISP/ICSP programmer impls |
| D-EMBEDDED-EMULATOR | runtime/specialty | Placeholder MOS6502/Z80 emulator impls |
| D-COV | workspace | Test coverage ~80-85%, target 90% |

## Remaining Deprecated Surface

| Area | Count | Notes |
|------|-------|-------|
| `env_config/network.rs` | 0 | Fully evolved to capability names |
| `primal_sockets/api.rs` | 0 | Primal-named functions removed |
| `ipc_helpers/connection.rs` | 2 | `get_default_songbird_socket`, `register_with_songbird` (legacy Songbird aliases) |
| `primal_sockets/paths.rs` | 4 | Lower-level `resolve_*_socket_fallback` (internal) |
| `interned_strings.rs` | 3 | Primal name constants (centralized, not scattered) |
| `types/network.rs` | 4 | EndpointConfig serde aliases (backward compat) |

---

Part of [ecoPrimals](https://github.com/ecoPrimals) — sovereign compute for science and human dignity.
