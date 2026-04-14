# ToadStool S194 Handoff — Capability-Based Field/Type/Doc Evolution

**Date**: April 8, 2026
**Session**: S194
**Author**: westgate
**Status**: Complete

---

## Summary

S192-S194 completed three focused sessions:

1. **S192**: GAP-MATRIX-12 — `validate_insecure_guard()` at server startup (BTSP Tier 2)
2. **S193**: Headless GPU crash isolation + BTSP field renames
3. **S194**: Deep debt — evolved remaining primal-named fields, types, and docs to capability-based

---

## S194 Changes (24 files)

### Struct Field Evolution
- `nestgate_integration` → `storage_integration` with `#[serde(alias = "nestgate_integration")]`
- `NestGateMount` → `StorageMount` in production return types (`integrator_impl.rs`)

### Doc Comment Cleanup
- `tarpc_client.rs`: "Songbird's pattern" → "the standard pattern"
- `cli/main.rs`: "BearDog cryptographic security" → "Cryptographic security"
- `auth.rs`: "BearDog integration" → "security service integration"
- `storage.rs`: "NestGate integration" → "storage service integration"
- `orchestration.rs`: removed specific service names from doc examples
- `visualization_client.rs`: "CORALREEF_*" → "visualization service" in doc tier description

### Test Function Renames
- `test_squirrel_mcp_interface_creation` → `test_intelligence_mcp_interface_creation`
- `test_squirrel_mcp_context_handling` → `test_intelligence_mcp_context_handling`
- Test data updated from primal names to capability names

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | 0 diffs |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 warnings |
| `cargo check --workspace --all-targets` | Clean |
| `cargo doc --workspace --no-deps` | 0 warnings |
| `cargo test --workspace --lib` | 7,415 passed, 0 failed |
| `cargo test --workspace --tests` | 21,526+ passed, 0 failed |
| Production TODOs | 0 |
| Production unsafe | ~66 (all in hw-safe/GPU/VFIO/display containment) |
| `#[allow]` count | ~80 (down from 342) |

---

## Remaining Primal Name Analysis

**~400 intentional legacy-compat references remain** across the codebase:

| Category | Count | Justification |
|----------|-------|---------------|
| Legacy env var fallbacks (`SONGBIRD_PORT`, `CORALREEF_SOCKET`, etc.) | ~80 | Backward compat — tried after capability-based names |
| `#[serde(alias = "...")]` on config structs | ~30 | JSON/TOML config compat |
| `parse_type` match arms in `primal_types.rs` | ~10 | Legacy type parsing |
| Interned string constants + deprecated type aliases | ~20 | Runtime compat during migration |
| Test fixtures verifying legacy compat works | ~200 | Testing the backward compat paths |
| `integration/protocols/src/bear_dog/` module | ~40 | Full protocol client (will evolve name in future) |

**All new code is capability-first.** No user-visible primal names remain.

---

## Cross-Primal Impact

- **primalSpring**: ToadStool now fully compliant with GAP-MATRIX-12 (BTSP insecure guard)
- **biomeOS**: Socket at `$XDG_RUNTIME_DIR/biomeos/toadstool.sock` with Wire Standard L3
- **Headless environments**: `TOADSTOOL_HEADLESS=1` for CI/servers without display

---

## References

- Commit: `05a4b8d5` (S194)
- Prior: `f38ff29a` (S193), `1d60234f` (S192)
- Standards: `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2, `BTSP_PROTOCOL_STANDARD.md`, `CAPABILITY_WIRE_STANDARD.md`
