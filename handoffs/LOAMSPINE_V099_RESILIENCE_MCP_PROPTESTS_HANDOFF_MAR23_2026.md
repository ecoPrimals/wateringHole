# LoamSpine v0.9.9 — Resilience, MCP Tools, Certificate Proptests

**Date**: March 23, 2026  
**From**: LoamSpine  
**To**: All Springs, All Primals, biomeOS  
**Status**: Complete, pushed to origin/main

---

## Summary

LoamSpine v0.9.9 delivers three capabilities:

1. **ResilientSyncEngine** — Federation outbound IPC now wrapped with circuit-breaker (lock-free atomic Closed/Open/HalfOpen) and retry (exponential backoff with jitter). Absorbs resilience pattern used across healthSpring, primalSpring, rhizoCrypt.

2. **MCP `tools.list` / `tools.call`** — Model Context Protocol support for AI agent visibility. 11 tools with `inputSchema` definitions. Squirrel and biomeOS agents can discover and invoke LoamSpine operations through structured tool schemas. Recursive dispatch through JSON-RPC handler (dispatch/dispatch_inner split for async future sizing).

3. **Certificate lifecycle proptests** — 10 new property-based tests covering creation invariants, loan holder semantics, serde roundtrip, state transitions, loan terms builder preservation.

---

## Code Changes

| File | Change |
|------|--------|
| `crates/loam-spine-core/src/sync/mod.rs` | `ResilientSyncEngine` wrapper with `push_entries` and `pull_entries` resilient methods |
| `crates/loam-spine-core/src/neural_api.rs` | `mcp_tools_list()`, `mcp_tool_to_rpc()` — MCP tool schema generation and tool-to-RPC mapping |
| `crates/loam-spine-api/src/jsonrpc/mod.rs` | `tools.list` and `tools.call` dispatch, `dispatch`/`dispatch_inner` split |
| `crates/loam-spine-core/src/niche.rs` | `tools.list` and `tools.call` in METHODS, SEMANTIC_MAPPINGS, COST_ESTIMATES |
| `crates/loam-spine-core/src/certificate/mod.rs` | 10 new certificate lifecycle proptests |
| `crates/loam-spine-core/src/lib.rs` | `ResilientSyncEngine` re-export |

---

## For Ecosystem Partners

### Using ResilientSyncEngine
```rust
use loam_spine_core::{ResilientSyncEngine, sync::SyncEngine};

let engine = SyncEngine::new();
let resilient = ResilientSyncEngine::with_defaults(engine);
// push_entries and pull_entries now have circuit-breaker + retry
```

### MCP Tool Discovery
Send `tools.list` via JSON-RPC to get all available tools with schemas:
```json
{"jsonrpc": "2.0", "method": "tools.list", "params": {}, "id": 1}
```

Invoke a tool:
```json
{"jsonrpc": "2.0", "method": "tools.call", "params": {"name": "health_check", "arguments": {}}, "id": 2}
```

---

## Metrics

- **Tests**: 1,256 passing (up from 1,247)
- **Coverage**: 92%+ line / 90%+ region / 86%+ function
- **Clippy**: 0 warnings (pedantic + nursery, all features, cast deny)
- **cargo deny**: advisories ok, bans ok, licenses ok, sources ok
- **Unsafe**: 0 in production and tests
- **TODOs/FIXMEs**: 0
- **Production mocks**: 0
- **Max file**: 865 lines (all under 1,000)

---

## Remaining Evolution Targets

- Circuit breaker pattern applied to specific IPC clients (discovery_client already has resilience; sync engine now wrapped)
- `OnceLock` caching for static capability/method lookups
- Transport abstraction layer evolution
- `ValidationHarness`/`ValidationSink` pattern adoption from biomeOS
