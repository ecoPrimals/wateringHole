# NestGate v0.4.70 — primalSpring Audit Resolution Handoff

**Date:** April 3, 2026
**Commit:** a75e9f2a (post-resolution)
**Session:** 17 — primalSpring audit gap closure

## Audit Findings Addressed

### 1. Primal Name References in 7 Non-Test Files — CONFIRMED & DOCUMENTED

All 7 files identified by primalSpring have been investigated and confirmed as
**config-layer service descriptors** or **anti-pattern documentation**, not routing logic:

| File | Category | Status |
|------|----------|--------|
| `nestgate-config/external/services_config.rs` | Deprecated compat fields + migration docs | DOCUMENTED — compliance note added |
| `nestgate-config/runtime/services.rs` | Module docs only (anti-pattern examples) | ACCEPTABLE |
| `nestgate-discovery/capabilities/mod.rs` | Anti-pattern "before/after" docs | ACCEPTABLE |
| `nestgate-discovery/capabilities/discovery/mod.rs` | Migration example in docs | ACCEPTABLE |
| `nestgate-discovery/capability_discovery.rs` | Problem statement in module docs | ACCEPTABLE |
| `nestgate-discovery/primal_discovery/runtime_discovery.rs` | "does NOT hardcode" doc | ACCEPTABLE |
| `nestgate-rpc/isomorphic_ipc/atomic.rs` | Ecosystem topology docs (NEST Atomic) | DOCUMENTED — compliance note added |

**Conclusion:** Zero primal names in routing logic or runtime code paths. All
references are intentional: deprecated config compatibility (with `#[deprecated]`
attributes and capability-based replacements), or architectural documentation
describing ecosystem topology.

### 2. NG-01: FileMetadataBackend Default Wiring — CONFIRMED

- `SemanticRouter::new()` defaults to `FileMetadataBackend` with
  `default_metadata_base_dir()`, falling back to `InMemoryMetadataBackend` only
  on filesystem error
- `InMemoryMetadataBackend` is used in tests and as error-only fallback
- The daemon currently uses `legacy_ecosystem_rpc_handler` (storage dispatch via
  `StorageState`); `SemanticRouter` will be the daemon's routing layer when the
  legacy dispatch migrates — `FileMetadataBackend` is already the production
  default for that path
- Documentation added to `SemanticRouter::new()` confirming NG-01 compliance

### 3. NG-03: data.* Handler Stubs — ALIGNED

- `data.*` is correctly **excluded** from all `capabilities.list` surfaces
  (semantic router, unix socket, JSON-RPC HTTP, isomorphic IPC)
- Regression test explicitly asserts no `data.*` in advertised capabilities
- `SELF_CAPABILITIES` does not include `"data"`
- **Fixed:** Unix socket `data_handlers.rs` error messages aligned with semantic
  router delegation story — now returns structured delegation errors pointing to
  `discovery.query` with `capability="data"` and `NESTGATE_CAPABILITY_DATA`
  (previously had stale "wire cross-crate dep" messages)
- Module documentation updated to explain the delegation pattern

## Verification

```
cargo fmt --all         ✅ clean
cargo clippy -D warnings ✅ clean
cargo test --all        ✅ 12,270 passed, 0 failed
```

## Compliance Matrix

| Requirement | Status |
|-------------|--------|
| Capability-based discovery | COMPLIANT — zero primal names in routing logic |
| Primal sovereignty | COMPLIANT — self-knowledge only, runtime discovery |
| FileMetadataBackend default | COMPLIANT — production default in SemanticRouter |
| data.* honest delegation | COMPLIANT — not_implemented with discovery guidance |
| data.* excluded from capabilities | COMPLIANT — regression-tested |
| Clippy pedantic | CLEAN |
| Format | CLEAN |
| Tests | 12,270 passing |
