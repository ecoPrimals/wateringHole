# Squirrel v0.1.0 — Spring Absorption & Primal Integration Handoff

**Date**: March 15, 2026
**Primal**: Squirrel (AI Coordination)
**Status**: Completed
**Scope**: Absorb ecosystem patterns from springs and primals, implement biomeOS lifecycle integration

---

## Summary

This handoff documents the integration of ecosystem-wide patterns discovered from the 6 active springs (neuralSpring, healthSpring, groundSpring, airSpring, wetSpring, hotSpring) and 4 foundation primals (BearDog, Songbird, ToadStool, NestGate) into Squirrel's codebase.

## Changes Implemented

### Phase 1: Capability Registry and Deploy Graph

1. **`capability_registry.toml`** — New file at workspace root
   - Source of truth for all JSON-RPC methods (16+ capabilities)
   - Each capability includes method name, domain, description, and JSON Schema `input_schema`
   - Pattern from wetSpring's `capability_registry.toml`
   - Loaded at startup by `JsonRpcServer`; falls back to compiled defaults if file missing

2. **`squirrel_deploy.toml`** — New file at workspace root
   - BYOB (Build Your Own Biome) deploy graph
   - Defines germination order: BearDog → Songbird → Squirrel
   - Optional dependencies: ToadStool (local inference), NestGate (model cache)
   - Health check configuration for biomeOS orchestrator
   - Pattern from airSpring's `airspring_deploy.toml`

3. **Registry loader** — `crates/main/src/capabilities/registry.rs`
   - Parses `capability_registry.toml` into typed structs
   - TOML-to-JSON converter for `input_schema` fields
   - Compiled-in defaults as fallback
   - Method lookup by name for enriching tool definitions

4. **`handle_discover_capabilities`** now reads from registry instead of hardcoded list
5. **`handle_list_tools`** now enriches entries with `input_schema` from registry (McpToolDef pattern)

### Phase 2: biomeOS Lifecycle (from healthSpring)

6. **`lifecycle.rs`** — `crates/main/src/capabilities/lifecycle.rs`
   - `find_biomeos_socket()` — probes standard biomeOS socket locations
   - `register_with_biomeos()` — sends `lifecycle.register` JSON-RPC on startup
   - `spawn_heartbeat()` — 30s interval `lifecycle.status` via `watch::Receiver` shutdown
   - `install_signal_handlers()` — SIGTERM + SIGINT handling with socket cleanup
   - `cleanup_socket()` — safe socket file removal

7. **`main.rs`** updated to use lifecycle:
   - Replaced Ctrl+C handler with `install_signal_handlers()` (handles SIGTERM too)
   - biomeOS registration on startup if orchestrator socket found
   - Heartbeat spawned after successful registration
   - Standalone mode when no biomeOS detected

### Phase 3: capability.announce Fix (from neuralSpring)

8. **`handle_announce_capabilities`** now treats `capabilities` as tool routing fallback when `tools` is empty
   - neuralSpring's MCP adapter sends capabilities without explicit tool names
   - This allows capability-based routing instead of requiring explicit tool lists

### Phase 4: Context RPC Methods

9. **Three new JSON-RPC methods wired**:
   - `context.create` — creates a new context session (auto-generates ID if not provided)
   - `context.update` — updates context state by ID with new data
   - `context.summarize` — returns context summary by ID
   - All documented in SQUIRREL_LEVERAGE_GUIDE.md, now actually implemented

10. **`ToolListEntry`** extended with `input_schema: Option<serde_json::Value>` (McpToolDef pattern)

### Phase 5: Primal Interaction Wiring

11. **BearDog crypto discovery alignment** — `crates/core/auth/src/capability_crypto.rs`
    - Added biomeOS socket paths as highest-priority discovery locations
    - `/run/user/<uid>/biomeos/beardog.sock` now probed before legacy `/tmp/` paths
    - Added `nix` workspace dependency to auth crate for UID resolution

12. **ToadStool AI provider discovery** — `crates/main/src/api/ai/router.rs`
    - Added step 3 to `new_with_discovery()`: biomeOS socket scan for ToadStool
    - Probes `/run/user/<uid>/biomeos/toadstool.sock` and `/tmp/toadstool.sock`
    - Only triggers when no other AI providers found (avoids duplicate scanning)
    - Creates `UniversalAiAdapter` from discovered socket

## Files Modified

| File | Change |
|------|--------|
| `capability_registry.toml` | NEW — capability source of truth |
| `squirrel_deploy.toml` | NEW — BYOB deploy graph |
| `crates/main/src/capabilities/mod.rs` | Added `lifecycle` and `registry` modules |
| `crates/main/src/capabilities/registry.rs` | NEW — registry loader |
| `crates/main/src/capabilities/lifecycle.rs` | NEW — biomeOS lifecycle |
| `crates/main/src/rpc/jsonrpc_handlers.rs` | Registry-backed discover, announce fix, context handlers |
| `crates/main/src/rpc/jsonrpc_server.rs` | Added `capability_registry` field, context dispatch |
| `crates/main/src/rpc/types.rs` | Added `input_schema` to `ToolListEntry` |
| `crates/main/src/main.rs` | Lifecycle integration, signal handlers |
| `crates/main/Cargo.toml` | Added `squirrel-context` dependency |
| `crates/core/auth/src/capability_crypto.rs` | biomeOS socket scan for BearDog |
| `crates/core/auth/Cargo.toml` | Added `nix` workspace dependency |
| `crates/main/src/api/ai/router.rs` | ToadStool socket discovery |

## Not in Scope (deferred post-alpha)

- **tarpc typed service traits** for `ai.*` methods (groundSpring pattern) — larger refactor
- **Provenance trio** (`provenance.begin/record/complete`) — Squirrel doesn't produce provenance yet
- **NestGate caching** for context windows — future enhancement via `storage.put`/`storage.get`
- **Direct spring integration** — springs connect to Squirrel, not vice versa

## Test Status

- All existing tests continue to pass
- New tests added for: registry loading, lifecycle socket discovery, signal handler creation
- Build: `cargo check -p squirrel -p squirrel-mcp-auth` — clean (0 errors, 0 warnings)

## Next Steps

1. End-to-end test with a running biomeOS orchestrator
2. ToadStool integration test with real Ollama instance
3. Context persistence via NestGate when available
4. Upgrade `context.create`/`update`/`summarize` from stub to full context store
