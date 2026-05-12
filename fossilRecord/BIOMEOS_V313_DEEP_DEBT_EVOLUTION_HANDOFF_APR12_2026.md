# biomeOS v3.13 — Deep Debt Evolution Handoff

**Date**: April 12, 2026
**From**: biomeOS (self)
**Trigger**: Comprehensive deep debt audit — hardcoding, incomplete implementations, deprecated APIs, file-size governance

---

## Summary

Full-spectrum deep debt evolution pass across 6 crates. The codebase was already remarkably clean (zero `unsafe`, zero TODO/FIXME, all mocks test-gated, zero `ring`/`openssl` in main workspace), so this pass focused on the remaining debt: **hardcoded primal names**, **incomplete implementations**, **deprecated API lingering**, and **file-size governance**.

---

## Changes

### 1. Hardcoded primal names → capability-based constants

**Files**: `biomeos-spore/src/spore/config.rs`, `deployment.rs`, `verify.rs`; `biomeos-cli/src/bin/main.rs`, `commands/spore.rs`, `commands/verify.rs`

- Spore config generation now uses `primal_names::BEARDOG` / `primal_names::SONGBIRD` constants instead of string literals in generated TOML and shell scripts
- CLI UX strings evolved from specific names ("Songbird", "Toadstool", "BearDog") to capability-role descriptions ("discovery provider", "security provider", "deployment provider")
- Verification binary list uses capability-based labels, not hardcoded binary names

### 2. Deprecated API removal

**File**: `biomeos-core/src/btsp_client.rs`

- Removed `beardog_socket_path()` — zero callers across entire workspace
- Was deprecated in favor of `security_provider_socket_path()` (capability-based)

### 3. Incomplete → complete: `learn_from_event`

**File**: `biomeos-graph/src/ai_advisor_core.rs`

- Was: built HashMap context then discarded it with `let _ = context;`
- Now: logs events at debug level for observability, forwards to Squirrel AI provider via `ai.learn_event` RPC when available, with configurable timeout

### 4. Topology: hardcoded "healthy" → live probe

**File**: `biomeos-atomic-deploy/src/handlers/topology.rs`

- Was: every discovered socket returned `"health": "healthy"` unconditionally
- Now: calls `NeuralRouter::check_endpoint_health()` to determine actual reachability, returns `"healthy"` or `"unreachable"`

### 5. File-size governance: capability.rs 804→744L

**Files**: `handlers/capability.rs` (804→744L), new `handlers/capability_mcp.rs` (70L)

- Extracted `mcp_tools_list` (MCP tool aggregation) into dedicated module
- Smart split: keeps MCP domain logic together rather than arbitrary line splitting
- `pub(crate)` visibility on `translation_registry` field to support cross-module access

### 6. Dependency audit: confirmed clean

- Main workspace: zero `unsafe` in any `.rs` file, `#![forbid(unsafe_code)]` on all crate roots
- `blake3` pure feature active, no `ring`/`openssl` in main workspace lock
- `tools/` workspace: `reqwest` with `default-features = false` confirmed ring-free
- Only known C-linked transitive dep: `serde_yaml_ng` → `unsafe-libyaml` (tracked, future migration to pure-Rust YAML parser)

---

## Audit Results (Full Codebase)

| Axis | Finding |
|------|---------|
| `unsafe` code | **Zero** — all crate roots have `#![forbid(unsafe_code)]` |
| TODO/FIXME/HACK | **Zero** in any `.rs` file |
| Mocks in production | **Zero** — all test-gated with `#[cfg(test)]` |
| `ring`/`openssl` | **Zero** in main workspace (only `serde_yaml_ng` → `unsafe-libyaml` remains) |
| Files >800L (production) | **Zero** — only test files exceed 800L (by design) |
| Deprecated APIs | **Zero** (removed `beardog_socket_path`) |
| Hardcoded primal names (prod) | **Zero remaining** in production code paths |

---

## Validation

- `cargo build`: clean
- `cargo clippy --workspace`: 0 warnings
- `cargo test --workspace`: 123 test suites, 0 failures
- `cargo fmt --all`: clean

---

## Downstream Impact

- **primalSpring**: No action needed — changes are internal to biomeOS
- **Spore consumers**: Generated `tower.toml` and `deploy.sh` are functionally identical (same binary paths resolve via constants)
- **CLI users**: UX strings now use capability-role language instead of specific primal names
