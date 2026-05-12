# biomeOS v3.32 — Deep Debt: Executor Refactor, Hardcoding Elimination, Dependency Bump

**Date**: April 29, 2026
**From**: biomeOS team
**Status**: Shipped and pushed

---

## Summary

v3.32 is a deep debt cleanup pass following the Phase 56 gap resolution (v3.31). Zero new features — purely structural improvements.

## Changes

### Smart refactor: neural_executor.rs (816 → 628 lines)
- Extracted rollback logic into `neural_executor_rollback.rs`: `resolve_node_type`, `rollback`, `rollback_primal_lifecycle`, `rollback_register_capabilities`
- The rollback module is a cohesive unit for reverse-topological-order node rollback
- Zero production files now exceed 800 lines

### Hardcoded `/tmp` fallback elimination
- `execute.rs` `register_capabilities_from_graph` and `load_translations_from_graph` now use `DEFAULT_SOCKET_DIR` constant instead of bare `"/tmp"` string literals
- Aligns with centralized constant in `biomeos-types::defaults`

### Dependency evolution
- Bumped `serde-saphyr` from 0.0.23 to 0.0.24 (latest stable pure-Rust YAML)

## Verification

- `cargo check`: PASS
- `cargo clippy -- -D warnings`: PASS (0 warnings)
- `cargo fmt --check`: PASS
- `cargo test --workspace`: 7,814+ pass (1 pre-existing env-dependent failure)

## Debt posture

| Category | Status |
|----------|--------|
| Production files >800L | **Zero** |
| TODO/FIXME/HACK/XXX | **Zero** |
| `todo!()` / `unimplemented!()` | **Zero** |
| `unsafe` blocks | **Zero** |
| `#[allow(` without reason | **Zero** |
| Mocks in production | **Zero** |
| Hardcoded `/tmp` literals | **Zero** |
| C/FFI deps | Only `rtnetlink` → `netlink-sys` (documented) |
