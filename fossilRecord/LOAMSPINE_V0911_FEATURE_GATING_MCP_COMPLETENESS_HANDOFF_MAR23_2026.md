<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# LoamSpine v0.9.11 — Feature Gating, MCP Completeness & Streaming Evolution

**Date**: March 23, 2026  
**From**: LoamSpine  
**To**: All Springs, All Primals, biomeOS  
**Status**: Complete, pushed to origin/main

---

## Summary

LoamSpine v0.9.11 evolves the codebase across six areas identified in a deep audit: smart refactoring of sentinel patterns, resilient error classification, MCP tool completeness enforcement, dependency feature-gating, NDJSON streaming protocol evolution, and documentation license compliance.

1. **`ChainError` sentinel → `Option`** — `HashMismatch { expected, actual }` fields evolved from `[0u8; 32]` sentinel values to idiomatic `Option<EntryHash>`, eliminating a semantic ambiguity where "no previous hash" was indistinguishable from "all-zero hash."

2. **`ResilientAdapter::execute_classified`** — New method accepting an `is_transient` closure for selective retries. Permanent errors (e.g., auth failures, validation errors) fail fast on first attempt. Transient errors (e.g., network timeouts, connection resets) trigger exponential backoff. The existing `execute` method delegates with `|_| true` for backward compatibility.

3. **MCP tool completeness enforcement** — New test `mcp_tools_cover_all_methods_in_capability_list` ensures every method advertised in `capability_list()` has a corresponding MCP tool schema and `mcp_tool_to_rpc` mapping. Found and fixed 7 missing methods (`spine.seal`, `entry.get_tip`, `certificate.verify`, `slice.anchor`, `session.commit`, etc.).

4. **`hickory-resolver` feature-gated** — DNS SRV resolution now behind `dns-srv` feature (default-on). Builds clean with `--no-default-features --features redb-storage`, reducing binary size and compile time for deployments without DNS SRV discovery.

5. **NDJSON streaming evolution** — `NDJSON_PROTOCOL_VERSION` constant ("1.0") for protocol versioning. `read_ndjson_stream` async helper parses `StreamItem`s from any `AsyncBufRead`, handling blank lines, parse errors, and terminal items (End/Fatal).

6. **CC-BY-SA-4.0 documentation license** — All 15 `specs/` markdown files and 6 root documentation files now carry correct scyBorg documentation license SPDX headers (was AGPL-3.0 on some docs).

---

## Code Changes

| File | Change |
|------|--------|
| `crates/loam-spine-core/src/spine.rs` | `ChainError::HashMismatch` fields → `Option<EntryHash>` |
| `crates/loam-spine-core/src/resilience.rs` | `execute_classified()` + 2 tests (permanent/transient) |
| `crates/loam-spine-core/src/neural_api.rs` | 7 MCP tool mappings added; `capability.list` naming fix; `deregister` uses `extract_rpc_error`; `#[expect(too_many_lines)]` |
| `crates/loam-spine-core/src/neural_api_tests.rs` | 3 new tests (completeness, canonical names, unknown tool) |
| `crates/loam-spine-core/Cargo.toml` | `hickory-resolver` optional; `dns-srv` feature |
| `crates/loam-spine-core/src/infant_discovery/mod.rs` | `#[cfg(feature = "dns-srv")]` on DNS SRV paths |
| `crates/loam-spine-core/src/service/infant_discovery.rs` | `#[cfg(feature = "dns-srv")]` on DNS SRV paths |
| `crates/loam-spine-core/src/streaming.rs` | `NDJSON_PROTOCOL_VERSION` + `read_ndjson_stream` + 4 tests |
| `crates/loam-spine-core/src/sync/tests.rs` | 9 new tests (ResilientSyncEngine, wire edge cases) |
| `crates/loam-spine-core/src/storage/sqlite/tests.rs` | 8 new tests (corrupt data, invalid IDs, empty counts) |
| 15 `specs/*.md` + 6 root `*.md` | CC-BY-SA-4.0 SPDX headers |
| `Cargo.toml`, `primal-capabilities.toml` | Version 0.9.10 → 0.9.11 |

---

## Metrics

| Metric | v0.9.10 | v0.9.11 |
|--------|---------|---------|
| Tests | 1,256 | **1,283** (+27) |
| Coverage | 92.23% line / 90.46% region | unchanged |
| Clippy | 0 warnings | 0 warnings |
| Doc warnings | 0 | 0 |
| Unsafe | 0 | 0 |
| Max file | 865 lines | **878** (`sync/tests.rs`) |
| Source files | 124 | **127** |
| cargo deny | pass | pass |

---

## For Ecosystem Partners

### Patterns to Absorb

**Error classification in resilience adapters**: `execute_classified(operation, is_transient)` lets callers distinguish transient failures (retry) from permanent failures (fail fast). Avoids wasting retries on errors that will never succeed.

```rust
adapter.execute_classified(
    || async { do_rpc_call().await },
    |e| !e.to_string().contains("unauthorized"),
).await
```

**MCP completeness testing**: Enforce that every advertised capability has a corresponding MCP tool schema. Prevents silent drift between capability list and AI agent tooling.

**Feature-gated heavy deps**: `hickory-resolver` gated behind `dns-srv`. Pattern: make network-dependent discovery optional so minimal deployments compile faster and stay pure Rust.

**NDJSON protocol versioning**: `NDJSON_PROTOCOL_VERSION` constant enables future backward-compatible evolution of the streaming wire format.

### API Changes

- `ResilientAdapter::execute_classified` — new public method (additive, non-breaking)
- `ChainError::HashMismatch` — field types changed from `EntryHash` to `Option<EntryHash>` (breaking for direct pattern matches, but this type is internal)
- `NDJSON_PROTOCOL_VERSION` — new public constant
- `read_ndjson_stream` — new public async function

### Wire Format

No changes. JSON-RPC wire format, tarpc protocol, and NDJSON streaming format are unchanged.

---

## Next (v0.10.0)

Per WHATS_NEXT.md:
- Signing capability middleware
- Showcase demo expansion
- Collision layer validation (neuralSpring)
- mdns crate evolution
- `OnceLock` caching for capability/method lookups
- `ValidationHarness`/`ValidationSink` (partially addressed via `execute_classified`)
