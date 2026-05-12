# Squirrel v0.1.0 — Deep Debt: Hash Bug Fix, Stub Evolution, Doc Alignment

**Date**: April 27, 2026 (session AM)
**Primal**: Squirrel (AI coordination)
**Scope**: Hash correctness, silent arm elimination, SDK honesty, demo data isolation, doc alignment

## Changes

### Hash Correctness Bug Fix
`PrimalCapability` manual `Hash` impl had a `_ => {}` wildcard that silently skipped field hashing for `FileSystem`, `NaturalLanguage`, and `AgentFramework` variants. This violated the `Hash`/`Eq` contract — two structurally different values could hash identically. All enum variants now have explicit hash arms. `ServerlessExecution` and `NaturalLanguage` merged as identical-shape arms per clippy `match_same_arms`.

### Capability-Based Error Messages
Security manager (`squirrel-mcp`) error messages evolved from hardcoded primal references ("BearDog capability") to capability-based language ("crypto.encrypt capability provider"). Primal self-knowledge boundary maintained.

### Silent Match Arm Elimination
- **Anthropic message builder**: Unknown `MessageRole` variants now logged at `debug` instead of silently discarded
- **Reward calculator**: Unrecognized calculator names logged at `debug` with reward value
- **Fallback monitoring logger**: Unknown `log_level` strings default to `trace` instead of swallowing events (4 match sites)

### SDK MCP Honesty
`OperationHandler::list_resources()` and `list_prompts()` evolved from `Ok(Vec::new())` (misleading callers into thinking "no resources exist") to `Err(McpError)` when MCP transport is not wired. Callers can now distinguish "searched and found nothing" from "cannot search — not connected".

### Demo Data Isolation
`PluginMarketplaceClient::get_sample_plugins()` moved from production `impl` block to `#[cfg(test)]` impl block. Production `get_featured_plugins`, `get_trending_plugins`, and `search_repository` return empty results with an honest `"note": "plugin marketplace discovery not yet wired"` field instead of fabricated demo data with fake URLs.

### deny.toml Cleanup
Removed stale commentary about `wasmtime`, `sqlx`, and `pprof` (none present in dependency tree). Updated `cc` note to accurately reflect blake3 build-dep situation (unused with `features=["pure"]`).

### Dependency Audit Results (no action needed)
- `serde_yaml_ng` → `unsafe-libyaml`: NOT a C dependency — Rust code transpiled from C via c2rust. Compiles with rustc only, no C compiler needed.
- `blake3` with `features=["pure"]`: `cc` is a build-dep but `build.rs` skips all C/ASM compilation when `pure` is active.
- Both are consistent with the "zero C dependencies" / ecoBin v3 guarantee.

### Root Doc Alignment
- README, CONTEXT, ORIGIN: test counts unified to 7,182
- README: file limit aligned to 800L (was 1,000), `cargo test` Quick Start aligned with `--all-features` merge gate
- CURRENT_STATUS: stale `test-context` transitive dep references removed, `.rustfmt.toml` path corrected, section title date updated

## Quality Gates
- `cargo fmt` ✓
- `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` ✓ (0 warnings)
- `cargo test --workspace` ✓ (7,182 passed, 0 failures)
- `cargo deny check` ✓
