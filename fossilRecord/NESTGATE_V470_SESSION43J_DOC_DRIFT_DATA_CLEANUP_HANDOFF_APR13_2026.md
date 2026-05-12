# NestGate v4.7.0-dev — Session 43j Handoff

**Date**: April 13, 2026
**Session**: 43j — Doc drift fix, data.* cleanup, dead deprecated deletion
**Triggered by**: primalSpring downstream audit (PRIMAL_GAPS.md, April 13 update)

---

## primalSpring Audit Triage

The audit identified **2 medium gaps** plus internal debt. Triage:

| Claim | Actual State | Resolution |
|-------|-------------|------------|
| `storage.retrieve` for large/streaming tensors | **RESOLVED in Session 43h** | 5 new methods: `store_blob`, `retrieve_blob`, `retrieve_range`, `object.size`, `namespaces.list` |
| Cross-spring persistent storage IPC | **RESOLVED in Session 43h** | Namespace isolation: `{base}/datasets/{family_id}/{namespace}/{key}.json` with `"shared"` default |
| Doc drift (57 methods in STATUS vs 41 in code) | **REAL — FIXED** | `UNIX_SOCKET_SUPPORTED_METHODS` synced (now 47), `provided_capabilities` updated, `bonding.*` added |
| `data.*` capability inconsistency | **REAL — FIXED** | Fake `data.*` removed from registry and `provided_capabilities` (delegation-only, not implemented) |
| 181 deprecated APIs to clean | **Stale count** (actual was 193) | 6 dead functions deleted → 187 remaining (rest are intentional migration markers) |
| Coverage 80→90% | **80.08% measured** | Core crates 95%+; 90% target is multi-session targeted test effort |

### Items for primalSpring to update in PRIMAL_GAPS.md

The following NestGate entries should move to **RESOLVED**:

```
| Medium | `storage.retrieve` for large/streaming tensors | NestGate | **RESOLVED** — Session 43h: store_blob, retrieve_blob, retrieve_range, object.size, namespaces.list |
| Medium | Cross-spring persistent storage IPC | NestGate | **RESOLVED** — Session 43h: namespace isolation model, family-scoped directories |
```

NestGate internal debt summary (line 329 update):
- Doc drift: **RESOLVED** (Session 43j — UNIX_SOCKET_SUPPORTED_METHODS synced, data.* removed)
- `data.*` inconsistency: **RESOLVED** (Session 43j — delegation-only, not advertised as capability)
- Deprecated APIs: **187** (was 193; 6 dead functions deleted; remainder are intentional canonical-config migration markers)
- Coverage: **80.08%** (tools/unwrap-migrator drags ~1%; core crates individually 95%+; 90% requires multi-session test additions)

---

## Changes Made

### Doc drift resolution

- `UNIX_SOCKET_SUPPORTED_METHODS` const: added `storage.namespaces.list` (46→47 methods)
- `provided_capabilities` storage group: added `retrieve_range`, `object.size`, `namespaces.list` (3 methods added)
- `provided_capabilities`: added `bonding` group (3 methods: `ledger.store`, `ledger.retrieve`, `ledger.list`) — was in const but missing from L3 envelope
- `capability_registry.toml`: removed `data.*` group, added `bonding.*` group

### data.* inconsistency fix

NestGate does NOT implement data operations. The `data.*` wildcard catch-all returns a
structured "NotImplemented" response directing callers to discover a data capability provider
(NG-03). These were incorrectly listed as real methods in `capability_registry.toml` and
`provided_capabilities`. Removed from both.

### Dead deprecated code deletion

| Function | Crate | Why dead |
|----------|-------|----------|
| `api_endpoint_with_fallback` | nestgate-config | Zero callers; superseded by capability discovery |
| `websocket_endpoint_with_fallback` | nestgate-config | Zero callers; same |
| `auto_configure` | nestgate-api | Zero callers; storage now configured via canonical config |
| `get_orchestrator_url` | nestgate-config | Zero callers; orchestration discovered at runtime |
| `discover_bind_address_compat` | nestgate-discovery | Zero callers; replaced by CapabilityAwareDiscovery |
| `discover_port_compat` | nestgate-discovery | Zero callers; same |

---

## Verification

- **Build**: `cargo check --workspace` PASS
- **Clippy**: `cargo clippy --workspace --all-targets --all-features -- -D warnings` PASS (0 warnings)
- **Tests**: 11,816 passing, 0 failures, 451 ignored
- **Crosscheck**: `cargo test --test capability_registry_crosscheck` — 11/11 PASS
- **Coverage**: 80.08% line (cargo llvm-cov --workspace)
- **Registry**: 12 groups, 45 methods (bonding replaces data in group count)

---

## Remaining Internal Debt

| Area | Count | Notes |
|------|-------|-------|
| `#[deprecated]` annotations | 187 | Intentional canonical-config migration markers; 0 dead callers |
| Coverage gap | 80%→90% | Multi-session: targeted tests in REST handlers, tarpc adapter, installer |
| `#[async_trait]` | 8 usages | Low priority; primalSpring audit shows NestGate is light vs ecosystem |
| `Box<dyn Error>` | ~587 matches | ~5 in production API boundaries (rest in tests/archived); ongoing evolution |
