# SPDX-License-Identifier: AGPL-3.0-or-later

# primalSpring v0.7.0 Phase 21 — Deep Ecosystem Audit Results

**Date**: March 29, 2026
**From**: primalSpring v0.7.0 (Phase 21)
**To**: All ecosystem teams (primals, springs, infra)

---

## Context

primalSpring executed a comprehensive 8-axis audit against ecosystem standards
and performed full remediation. This handoff summarizes patterns and findings
relevant to the broader ecosystem.

## Audit Scope

1. **Completion Status** — TODOs, FIXMEs, mocks, hardcoding, provenance
2. **Code Quality** — clippy (pedantic+nursery), fmt, doc, unsafe, `#[allow()]`
3. **Validation Fidelity** — Python baseline match, tolerance centralization
4. **barraCuda Dependency Health** — primitive delegation, version currency
5. **GPU Evolution Readiness** — shader promotion tiers
6. **Test Coverage** — line coverage, unit/integration/validation/determinism
7. **Ecosystem Standards** — license, architecture, IPC, file size, provenance, sovereignty
8. **Primal Coordination** — discovery, registration, typed IPC, MCP tools

## Key Outcomes

- **411 tests** passing (was 385), 42 ignored live tests
- **63 experiments** across 13 tracks, 100% with structured provenance
- **59 deploy graphs**, all nodes `by_capability`
- **Zero** clippy warnings, TODOs, FIXMEs, `#[allow()]`, unsafe, C deps
- **4 new library modules**: `ipc::tcp`, `ipc::methods`, `ipc::capability`, launcher sub-modules
- **8 experiments** consolidated from local boilerplate to library helpers
- **~40 hardcoded method strings** → centralized `ipc::methods` constants
- **~12 hardcoded primal names** → `primal_names::*` constants

## Reusable Patterns for Other Springs

### 1. Method Name Constants (`ipc::methods` pattern)

Centralize all JSON-RPC method names as `pub const` in a methods module:

```rust
pub mod methods {
    pub mod health {
        pub const LIVENESS: &str = "health.liveness";
        pub const CHECK: &str = "health.check";
    }
    pub mod capabilities {
        pub const LIST: &str = "capabilities.list";
    }
}
```

Eliminates: string literal drift, typos, inconsistency between server and client.

### 2. TCP RPC Library Helper (`ipc::tcp` pattern)

If experiments probe primals over TCP, extract the boilerplate:

```rust
pub fn tcp_rpc(addr: &str, method: &str, params: Value) -> Result<Value, String> {
    // connect, write JSON-RPC, read response, parse result
}
```

With configurable timeouts from `tolerances/`.

### 3. Launcher Sub-Module Pattern

When a module grows beyond ~500 LOC, split by **responsibility** not line count:
- `discovery.rs` — binary resolution (env vars, path tiers)
- `profiles.rs` — launch profile TOML parsing
- `spawn.rs` — process spawning, socket waiting
- `biomeos.rs` — biomeOS-specific launch logic

Re-export public API from `mod.rs` to preserve the import surface.

### 4. Circuit Breaker Half-Open

For any circuit breaker protecting external IPC:
- Track `opened_at: Mutex<Option<Instant>>` for time-based recovery
- Use `AtomicBool` probe token — single concurrent probe during half-open
- On mutex poisoning, default to **open** (fail safe, not fail open)

### 5. Tracing Migration

Library code should use `tracing` macros, not `println!`/`eprintln!`.
Exception: validation harness terminal output (user-facing banner/summary).

## Primal Coordination Gaps (P0/P1)

| Team | Gap | Priority | Impact |
|------|-----|----------|--------|
| **biomeOS** | TCP `--port` ignored | P0 | Blocks all TCP-only deployment cells |
| **biomeOS** | Cross-gate `gate` field on `capability.call` | P1 | Multi-gate routing |
| **Squirrel** | Abstract socket vs filesystem discovery | P0 | Breaks 5-tier discovery |
| **BearDog** | No `--listen` TCP mode | P0 | Blocks cross-gate federation |
| **petalTongue** | Dialogue-tree scene type | P1 | Blocks RPGPT storytelling |
| **ludoSpring** | 6 `game.*` methods for esotericWebb | P0 | Blocks storytelling cells |

## 8-Axis Audit Methodology

The audit methodology is fully documented in:
`springs/primalSpring/wateringHole/handoffs/PRIMALSPRING_V070_ECOSYSTEM_AUDIT_GUIDANCE_HANDOFF_MAR27_2026.md`

Recommended for all springs before major version bumps.

---

**License**: AGPL-3.0-or-later
