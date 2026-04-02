# petalTongue Deep Debt + Evolution Phase 4 Handoff

**Date**: April 2, 2026
**Previous**: `PETALTONGUE_CAPABILITY_FIRST_DISCOVERY_COMPLIANCE_HANDOFF_APR02_2026.md`
**Commit**: `e2c88d4` → (this session's doc commit follows)

---

## Summary

Comprehensive deep debt elimination and modern Rust evolution pass across the entire
petalTongue codebase. Focused on completing deprecated field migrations, removing legacy
code, unifying dependencies, smart file refactoring, and completing stub implementations.

Net result: **-831 lines** (2,401 added / 3,232 removed across 55 files).

---

## Changes

### 1. Dependency Hygiene

| Before | After |
|--------|-------|
| `egui_graphs = "0.22"` in workspace | **Removed** (unused) |
| `petgraph = "0.6"` in workspace | **Removed** (unused) |
| `thiserror = "1"` in discovery, tui, entropy | `thiserror = { workspace = true }` → **2.0** |
| Loose dep versions in adapters | All `{ workspace = true }` |

Affected crates: `petal-tongue-discovery`, `petal-tongue-tui`, `petal-tongue-entropy`, `petal-tongue-adapters`.

### 2. PrimalInfo Deprecated Field Migration

**Biggest single debt item**: removed `trust_level: Option<u8>` and `family_id: Option<String>` struct fields from `PrimalInfo` entirely.

| Before | After |
|--------|-------|
| `#[deprecated] pub trust_level: Option<u8>` | **Removed from struct** |
| `#[deprecated] pub family_id: Option<String>` | **Removed from struct** |
| `#[expect(deprecated)]` × 100+ across 40+ files | **All eliminated** |
| `migrate_deprecated_fields()` | `migrate_metadata_to_properties()` (metadata only) |

**Backward-compatible deserialization** via `#[serde(from = "PrimalInfoWire")]`:
- `PrimalInfoWire` accepts legacy JSON `trust_level` / `family_id` fields
- `From<PrimalInfoWire>` auto-migrates them into `properties` HashMap
- Zero downstream JSON breakage

**New accessor API**:
- `info.trust_level()` → `Option<u8>` (reads from properties)
- `info.family_id()` → `Option<&str>` (reads from properties)
- `info.set_trust_level(level)` / `info.set_family_id(id)` (setters)
- `info.with_trust_level(level)` / `info.with_family_id(id)` (builders)

### 3. Legacy HTTP Provider Removal

| Before | After |
|--------|-------|
| `http_provider.rs` (351 lines) | **Deleted** |
| `legacy-http` feature flag | **Removed** |
| `HttpVisualizationProvider` type | **Gone** |
| `http_provider_tests.rs` (349 lines) | **Deleted** |

Discovery crate now Unix socket/JSON-RPC only. The `reqwest` dependency remains for mDNS HTTP calls.

### 4. Audio Backend Evolution

| Backend | Before | After |
|---------|--------|-------|
| `direct.rs` | `can_play: true` but `is_available: false` | `can_play: false`, honest capabilities |
| `socket.rs` | Vague "not implemented" | Clear PipeWire/PulseAudio stub, all caps zero |

### 5. Smart File Refactoring

| File | Lines | Split into |
|------|-------|-----------|
| `system_monitor_integration.rs` | 852 | `mod.rs`, `display_state.rs`, `display_compute.rs`, `tool.rs`, `tests.rs` |
| `neural_api_provider.rs` | 802 | `mod.rs`, `provider.rs`, `parse.rs`, `mock_server.rs`, `tests.rs` |

Splits follow logical concern boundaries, not arbitrary line counts.

### 6. Stub Completions

| Stub | Before | After |
|------|--------|-------|
| `DiscoveryServiceProvider::get_topology` | Always `Ok(vec![])` | Infers capability-based topology edges from shared capabilities |
| `SrvRecord::select_by_priority` | Dead `priority`/`weight` fields | RFC 2782 weighted selection implemented |
| `PipelineRegistry` title/order | Stored but unreadable | Accessor methods wired up |

### 7. Dead Code Cleanup

- `DisplayInfo` / `InputDeviceInfo` in display backend: wired to connected-display selection
- `event_handler` field in `BiomeOsUiManager`: removed (panels own their own handlers)
- `decrypt_entropy` in entropy crate: removed (YAGNI)

### 8. Documentation & Specs

- `START_HERE.md`: Updated module map (removed songbird_client.rs, http_provider.rs), test count, capability-first cross-primal section
- `sandbox/scenarios/README.md`: Fixed binary name from `./petal-tongue` to `petaltongue ui --scenario`
- Archived 3 superseded specs to `archive/specs-archive/`:
  - `DISCOVERY_INFRASTRUCTURE_EVOLUTION_SPECIFICATION.md`
  - `PETALTONGUE_TOADSTOOL_INTEGRATION_ARCHITECTURE.md`
  - `ECOBLOSSOM_EVOLUTION_PLAN.md`
- Updated 5 active specs with current type names (`DiscoveryServiceClient`, `DiscoveredDisplayBackend`, `GpuComputeProvider`, JSON-RPC priority)

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Zero warnings |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --workspace --all-features` | **6,075 passing**, 0 failures |

---

## Impact on Consumer Primals

- **JSON wire format**: Unchanged. `trust_level` and `family_id` still accepted in JSON, auto-migrated to properties on deserialization.
- **Rust API**: Consumers importing `PrimalInfo` must use accessor methods instead of direct field access for trust/family data. Builder pattern available.
- **Discovery**: HTTP fallback path removed. All primals should use Unix socket JSON-RPC or tarpc.
- **Feature flags**: `legacy-http` feature no longer exists. Remove from any `--features` invocations.
