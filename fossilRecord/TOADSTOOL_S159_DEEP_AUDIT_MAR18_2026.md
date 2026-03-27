# ToadStool S159 — Deep Audit & Execution Handoff

**Date**: March 18, 2026
**Session**: S159
**Primal**: toadStool
**Type**: Deep audit, documentation, quality evolution

## Summary

Comprehensive codebase audit against wateringHole standards followed by systematic execution of all findings. All quality gates now pass.

## Changes

### Build Fixes
- 3 compilation errors resolved: toadstool-core (MockNpuDispatch), integration-protocols (Arc<str>/String mismatches), server (paths module import after extraction)
- Full workspace compiles: 58 crates, 0 errors

### Documentation (D-DOCS resolved)
- 694+ missing_docs warnings filled across all 58 crates
- `cargo clippy --workspace --all-targets -- -D warnings` passes with 0 errors
- Doc comment HTML warnings fixed (unescaped generic types → backtick-escaped)

### JSON-RPC Standardization
- Method names evolved to domain.verb per SEMANTIC_METHOD_NAMING_STANDARD:
  - `toadstool.provenance` → `provenance.query`
  - `ollama.*` → `inference.*` (list_models, execute, load_model, unload_model)
  - `gpu.telemetry/info/memory` → `gpu.query_telemetry/query_info/query_memory`
- Deprecated aliases retained for backward compatibility

### Sovereignty & Capability-Based Evolution
- Hardcoded primal names in auto_config evolved: "SONGBIRD" → "COORDINATION", "BEARDOG" → "CRYPTO", "NESTGATE" → "STORAGE"
- Production localhost strings evolved to named constants (DEFAULT_COORDINATION_ENDPOINT, DEFAULT_SERVER_ENDPOINT)

### Zero-Copy Expansion
- WorkloadSubmission and JsonWorkloadSubmission hot-path fields (workload_id, workload_type) evolved from String to Arc<str>

### Production Stub Elimination
- Security policy evaluator's unimplemented condition path evolved to typed ToadStoolError::validation errors

### Test Safety
- All unsafe env::set_var/remove_var in test code (~36 files) migrated to temp_env crate
- Nested tokio runtime anti-patterns fixed across 5+ test files

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 errors) |
| `cargo doc --all-features --no-deps` | PASS |
| `cargo test --workspace` | PASS (11,956+ tests, 0 failures) |
| Files > 1000 lines | 0 |
| Production TODO/FIXME/HACK | 0 |
| Unsafe env::set_var in tests | 0 |

## Ecosystem Impact

- JSON-RPC method names standardized — other primals calling toadStool should use new `domain.verb` names (deprecated aliases still work)
- Capability-based discovery fully enforced — no hardcoded primal names remain in production code
- Arc<str> on hot-path workload IDs — primals sending workload submissions benefit from zero-copy clone

## Remaining Debt

- D-COV: ~85% line coverage → 90% target
- Spec gaps: PcieTransport, streaming transport, display Phase 2-3, NPU multi-tenant implementation

## Cross-Primal Notes

- toadStool now uses `inference.*` instead of `ollama.*` for model lifecycle — aligns with domain.verb standard
- `provenance.query` replaces `toadstool.provenance` — primal name removed from method domain
- Capability key evolution in auto_config: other primals registering capabilities should use "COORDINATION"/"CRYPTO"/"STORAGE" not primal names
