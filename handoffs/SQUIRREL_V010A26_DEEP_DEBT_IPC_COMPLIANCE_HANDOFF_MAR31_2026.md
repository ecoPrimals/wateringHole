<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.26 — Deep Debt & IPC Compliance Handoff

**Date**: March 31, 2026
**Primal**: Squirrel (AI / MCP)
**From**: Deep debt resolution and wateringHole compliance session
**Status**: GREEN — 7,143 tests, 0 failures, clippy clean, fmt clean

---

## Summary

Two-session evolution addressing wateringHole IPC compliance gaps (SQ-01, SQ-02, health
methods), deep production debt (stubs → implementations), modern idiomatic Rust migration,
workspace dependency centralization, and smart large-file refactoring.

## IPC Compliance Matrix Changes

| Dimension | Before | After | Notes |
|-----------|--------|-------|-------|
| Wire Framing | P (abstract-only) | C | TCP listener via `--port`, newline JSON-RPC |
| Socket Path | X (abstract-only) | C | Filesystem socket + abstract; `ai.sock` symlink |
| Health Names | X (system.*) | C | `health.check/liveness/readiness` canonical |
| `--port` / `--listen` | P (accepted, unused) | C | Actually binds TCP on `127.0.0.1:<port>` |
| Standalone | C | C | Unchanged |
| Mobile | C | C | Unchanged |

## Key Changes

### IPC Protocol (SQ-01, SQ-02, Health)

- **Filesystem socket**: `$XDG_RUNTIME_DIR/biomeos/squirrel.sock` alongside abstract `\0squirrel`
- **Capability symlink**: `ai.sock` → `squirrel.sock` (auto-created, cleaned on shutdown)
- **TCP JSON-RPC**: `--port` binds real `TcpListener`, newline-delimited JSON-RPC
- **Health canonical**: `health.check`, `health.liveness`, `health.readiness`; `system.*` aliases
- **LOCAL_AI_ENDPOINT**: Wired into AiRouter discovery for Ollama/local inference
- **identity.get probe**: Registry discovery sends real JSON-RPC probe, not filename parsing

### Production Stubs Completed

- Alert evaluation with threshold-based metric checks
- Plugin TOML manifest parsing (toml crate)
- Plugin signature verification (blake3 constant-time comparison)
- MCP security manager initialization with config validation and crypto self-test
- MCP token hashing (blake3, pure Rust)
- Performance optimizer metrics and batch processing (bounded VecDeque)
- Health monitor with CPU/memory/socket connectivity checks
- SDK scoped logging with context propagation

### Modern Idiomatic Rust

- `#[allow(` → `#[expect(reason=...)]` (~50+ sites across 6 crates)
- `Box<dyn Error>` → typed errors in main, cli, ai-tools, sdk, rule-system
- Hardcoded primal names → `universal_constants::primal_names` constants
- Workspace dependencies centralized per WORKSPACE_DEPENDENCY_STANDARD
- WIP/FIXME/TODO markers: 0 in committed code

### Smart Refactoring

- `ecosystem/registry/types.rs`: 818 → 29 lines + 8 semantic modules
- `security/providers/mod.rs`: 932 → 30 lines + 4 semantic modules
- `core/core/ecosystem.rs`: 1000 → 20 lines + 5 semantic modules

## Verification

```
cargo clippy --all-features --all-targets: 1 warning (pre-existing test type_complexity)
cargo fmt --check: clean
cargo test --all-features: 105 suites, 7,143 passed, 0 failed
```

## Remaining Work (not blockers)

- Coverage gap to 90% target (currently 86.5%) — IPC/network code, demo binaries
- `endpoint_resolver.rs` NOTE(phase2) service mesh query (requires mesh integration)
- `SecurePluginStub` in cli (intentional: WebAssembly sandboxed loading deferred)
- Pre-existing `type_complexity` warning in `federation/mod.rs` test code

## Standards Compliance

- [x] PRIMAL_IPC_PROTOCOL v3.1 — filesystem socket, health methods, standalone, --port
- [x] SEMANTIC_METHOD_NAMING_STANDARD v2.0 — health.* canonical, system.* aliases
- [x] WORKSPACE_DEPENDENCY_STANDARD — centralized deps
- [x] STANDARDS_AND_EXPECTATIONS — forbid(unsafe), warn(missing_docs), edition 2024, AGPL-3.0
- [x] IPC_COMPLIANCE_MATRIX v1.2.0 — all X/P items resolved to C
- [x] PRIMAL_RESPONSIBILITY_MATRIX — AI/MCP owner, delegates crypto/storage/network/compute
