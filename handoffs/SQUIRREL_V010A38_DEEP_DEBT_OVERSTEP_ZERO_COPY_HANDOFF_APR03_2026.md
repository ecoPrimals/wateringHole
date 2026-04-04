# Squirrel v0.1.0-alpha.38 — Deep Debt, Overstep Cleanup & Zero-Copy Evolution

**Date**: 2026-04-03
**Session**: K — Deep debt, overstep cleanup, zero-copy, stub evolution
**Commit**: `bc52a22f` on `main`

## Summary

Continuing from alpha.37's T4/T6 capability-domain rename pass, this session
targets remaining deep debt: production stubs, overstep config presets,
primal-name coupling in test data, zero-copy evolution in sync hot paths,
and a comprehensive async-trait migration assessment.

## Changes

### 1. ConfigBuilder Overstep Cleanup

`ConfigBuilder::beardog()` in `universal-patterns/src/config/builder.rs`
embedded another primal's identity — an overstep. Replaced with generic
`ConfigBuilder::security()` that provides `PrimalType::Security` defaults
without hardcoding any primal name. `generate_template()` in `loader.rs`
updated accordingly.

### 2. CONSUMED_CAPABILITIES Domain Labelling

Comments in `niche.rs` CONSUMED_CAPABILITIES replaced primal-name parentheticals:
- `// Security (BearDog)` → `// Security domain (crypto, auth, secrets)`
- `// Compute delegation (ToadStool S158b)` → `// Compute domain (GPU dispatch, hardware)`
- `// Storage (NestGate)` → `// Storage domain (persistence, model cache)`

### 3. Test Data Primal-Name Decoupling (8 files)

Hardcoded primal names in test fixtures evolved to generic capability-domain IDs:
- `"songbird"` → `"discovery.find_primals"` / `"discovery-mesh"`
- `"toadstool"` → `"compute-provider"` / `"compute-provider-1"`
- `"nestgate"` → `"storage-primal"`
- `"squirrel"` (in peer test data) → `"ai-coordinator"` / `"primal-a"`

### 4. Production Stub Evolution

- `learning/manager.rs`: Placeholder `{"placeholder": true}` evolved to
  real context metadata (`context_type`, `observation_source`, `observed_at_epoch`)
- `ClientConfig::is_valid_for_provider()`: Stub returning hardcoded `false`
  evolved to real validation (`api_key.is_some() || endpoint.is_some()`)

### 5. Zero-Copy in Sync Hot Paths

`sync.rs` message processing chain evolved from owned → borrowed parameters:
- `process_message_internal(SyncMessage)` → `process_message_internal(&SyncMessage)`
- `handle_heartbeat(String, ...)` → `handle_heartbeat(&str, ...)`
- `handle_state_update(ContextState, ...)` → `handle_state_update(&ContextState, ...)`
- `handle_conflict_advanced(ConflictInfo)` → `handle_conflict_advanced(&ConflictInfo)`
- `handle_partition_detected(PartitionInfo)` → `handle_partition_detected(&PartitionInfo)`
- `handle_partition_recovered(Vec<String>)` → `handle_partition_recovered(&[String])`

Eliminates one full `SyncMessage` clone per message processing cycle.

### 6. async-trait Migration Assessment

Comprehensive audit found 403 `#[async_trait]` annotations across 148 files.
**All async traits are used with `dyn` dispatch** (`Arc<dyn Trait>`,
`Box<dyn Trait>`, `&dyn Trait`). Native Rust 2024 `async fn in trait` makes
traits non-object-safe, so migration requires architectural changes to all
consumers. **Deferred** to progressive evolution as ecosystem matures.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | ✓ |
| `cargo clippy -- -D warnings` | ✓ |
| `cargo clippy --all-features --all-targets -- -D warnings` | ✓ |
| `cargo test` | 6,856 passed / 0 failed / 107 ignored |
| `cargo doc --no-deps` | ✓ |
| `cargo deny check` | ✓ |

## Remaining Tracked Debt

| Item | Status | Notes |
|------|--------|-------|
| async-trait → native | Deferred | All 30+ traits use dyn dispatch; needs arch changes |
| Large files (900+ lines) | Acceptable | All <1000; mostly test files |
| .clone() in federation/service.rs | Low priority | 23 clones, most in Arc/construction paths |
| 384 std::env::var calls | Acceptable | Fallback chains for agnostic config |
