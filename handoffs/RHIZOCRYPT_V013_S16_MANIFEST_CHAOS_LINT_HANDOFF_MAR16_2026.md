# rhizoCrypt v0.13.0-dev — Session 16 Handoff

**Date**: 2026-03-16  
**From**: rhizoCrypt  
**To**: ecoPrimals ecosystem  
**Theme**: Ecosystem Absorption Execution — Manifest Discovery, Chaos Framework, Lint Migration

---

## Summary

Session 16 executed on all absorption candidates identified in the cross-ecosystem review (session 15). Deep debt solutions with modern idiomatic Rust, zero unsafe code, and capability-based design.

## Artifacts Created/Modified

### New Modules
- **`discovery::manifest`** — `$XDG_RUNTIME_DIR/ecoPrimals/*.json` manifest scanning (absorbed from toadStool S156 / barraCuda v0.3.5)
- **`testing::chaos`** — `ChaosEngine` framework with 7 fault classes (absorbed from squirrel)

### New Types
- `PrimalManifest` — primal, version, socket, address, capabilities
- `ChaosEngine`, `ChaosConfig`, `ChaosScenario` trait, `ChaosMetrics`
- `FaultClass` — NetworkPartition, Latency, ProcessCrash, ResourceExhaustion, ClockSkew, ConcurrencyStorm, CorruptInput
- `ValidationHarness` — composable check harness for `doctor`/`validate` binaries (absorbed from wetSpring V123)
- `SafeEnv::socket_env_var()`, `SafeEnv::address_env_var()`, `SafeEnv::get_socket_path()` (absorbed from sweetGrass V0717)

### Infrastructure Changes
- **Workspace lint consolidation** — All pedantic/nursery/cargo lint config moved to `[workspace.lints.clippy]` in root `Cargo.toml`. Crate `lib.rs` no longer overrides workspace config.
- **`#[expect(reason)]` for production code, `#[allow]` for test blankets** — Stale suppressions auto-surface in production; test files keep blanket freedom.
- 5 new workspace-level `"allow"` entries: `missing_errors_doc`, `missing_panics_doc`, `field_reassign_with_default`, `unnecessary_literal_bound`, `similar_names`

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt` | clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 warnings |
| `cargo doc --workspace --no-deps` | 0 warnings |
| `cargo test --workspace` | **1,080 passing** (0 failures) |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Absorption Sources

| Pattern | Source | Status |
|---------|--------|--------|
| Generic socket/address env var helpers | sweetGrass V0717 | Absorbed |
| Manifest-based discovery | toadStool S156 / barraCuda v0.3.5 | Absorbed |
| ChaosEngine/ChaosConfig/ChaosScenario | squirrel ChaosEngine | Absorbed |
| ValidationHarness (finish_with_code) | wetSpring V123 Validator | Absorbed |
| Workspace lint consolidation | ecosystem-wide standard | Absorbed |
| `#[expect(reason)]` / `#[allow]` split | ecosystem-wide standard | Absorbed |
| XDG_RUNTIME_DIR socket fallback | FAMILY_ID socket standard | Absorbed |

## Key Design Decisions

1. **Test `#[allow]` vs production `#[expect]`**: Test files use `#[allow]` (blanket suppression — tests may freely add `unwrap`/`expect` in future). Production code uses `#[expect(reason = "...")]` so stale suppressions auto-surface as unfulfilled-lint warnings.

2. **Manifest discovery as supplement, not replacement**: `scan_manifests()` provides filesystem-based capability discovery as a fallback when Songbird is unavailable. The primary discovery path remains the discovery adapter.

3. **ChaosEngine as test-only module**: The chaos framework is gated behind `#[cfg(test)]` and lives in `testing::chaos`. It provides infrastructure for structured fault injection without polluting the production binary.

4. **ValidationHarness collects before deciding**: Unlike `OrExit` (fail-fast), `ValidationHarness` accumulates all check results and produces a summary + exit code, making it suitable for multi-check binaries.

## What rhizoCrypt Now Provides to the Ecosystem

- **Manifest discovery protocol** — Other primals can adopt `PrimalManifest` format for peer-to-peer discovery
- **ChaosEngine pattern** — Reusable fault injection framework, adaptable to any primal's workload
- **ValidationHarness** — Generic composable validation for any primal's `doctor` subcommand
- **Lint governance model** — Workspace-level config + `#[expect]`/`#[allow]` split as reference

## Next Steps

- Integrate `ChaosEngine` scenarios with real DAG operations (session create under partition, vertex append under latency)
- Add fuzz testing targets (`cargo-fuzz`)
- ISSUE-012 (Content Similarity Index) and ISSUE-013 (Content Convergence) coordination
- Collision Layer integration with loamSpine
