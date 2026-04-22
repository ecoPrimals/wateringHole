# petalTongue v1.6.6 — Deep Domain Refactoring Sprint 7 Handoff

**Date**: April 15, 2026
**Scope**: Deep debt resolution, domain refactoring, capability evolution, docs cleanup
**Status**: All items complete — 5,960+ tests passing, zero failures

---

## Summary

Sprint 7 executed deep domain refactoring across 14 production modules and 4 test
suites. All production files now under 400 LOC through smart decomposition by
domain concern, not mechanical splitting. Hardcoded primal identity defaults evolved
to capability-based naming. Root documentation unified and synchronized.

## Execution

### 1. Smart Domain Refactoring (14 modules)

Each module decomposed into single-responsibility submodules:

| Module | Before | After | Domain Split |
|--------|--------|-------|--------------|
| `wad_loader` | 696 | types, io, map_parse, endian, tests | WAD I/O vs parsing vs data |
| `raycast_renderer` | 679 | mod, math, tests | Rendering vs geometry |
| `sensory_matrix` | 678 | capability_sets, matrix, tests | Types vs logic |
| `visualization_handler/types` | 675 | 10 domain modules | Per-RPC-domain types |
| `graph_editor/rpc_methods` | 671 | graph, nodes, edges, templates | Per-entity handlers |
| `protocol_selection` | 668 | protocol, parse, connect, connection | Protocol vs connection |
| `system` (RPC handlers) | 665 | health, capabilities, topology, identity, provider | Per-domain handlers |
| `primal_panel` | 644 | state, mod, tests | State logic vs UI |
| `collector` (telemetry) | 632 | metrics, snapshot, mod | Aggregation vs export |
| `traffic_view/view` | 629 | render/toolbar, render/diagram, render/metrics_panel | Per-component rendering |
| `graph_canvas/rendering` | 619 | geometry, arrow, canvas_impl | Math vs drawing |
| `device_panel` | 616 | events, mod | Event handling vs UI |
| `config_system` | 615 | types, loader | Config types vs loading |
| `compiler` (scene) | 612 | core, plan, facets | Compilation phases |

### 2. Test Suite Refactoring (4 files)

| Test File | Before | Split |
|-----------|--------|-------|
| `app/tests` | 692 | 6 domain modules (mode, headless, state, update, keyboard) |
| `traffic_view/tests_extended` | 690 | 4 modules (proptest, flow, layout, intents) |
| `trust_dashboard/tests` | 688 | 6 modules (fixtures, display, style, dashboard) |
| `headless_panel_coverage_tests` | 641 | 8 integration modules |

### 3. Capability Evolution

- **BTSP provider default**: `"beardog"` → `"security"` (capability-based)
- **Socket path centralization**: Duplicate `/tmp` fallbacks now use `constants::LEGACY_TMP_PREFIX`
- **Provenance trio**: Confirmed already capability-based (`dag.session`, `braid.create`, `spine.create`)

### 4. Comprehensive Audit Results

| Area | Finding |
|------|---------|
| Production `.unwrap()` | Zero — all confined to `#[cfg(test)]` |
| TODO/FIXME/HACK | Zero markers |
| `ring` dependency | Not in tree for Linux; `deny.toml` ban operational |
| C dependencies | None — no `build.rs`, ecoBin compliant |
| Production mocks | All feature-gated (`mock`, `test-fixtures`) |
| Audio backends | Opt-in incomplete implementations behind features, well-documented |
| BarraCuda benchmarks | No Python benchmarks; Kokkos GPU parity in Rust; no Galaxy standard |

### 5. Documentation

- README, START_HERE, CONTEXT, CHANGELOG synchronized
- Test count: 5,960+ (verified via `cargo test --all-features --workspace`)
- File size policy: all production files under 400 LOC
- Sprint status: Sprint 7 current

## Verification

```
cargo fmt --all -- --check              # clean
cargo clippy --all-features --all-targets -- -D warnings  # clean
cargo test --all-features --workspace   # 5,960+ passed, 0 failed
```

## Remaining Backlog

- BTSP Phase 2 consumer wiring (cross-primal dep on BearDog)
- BTSP Phase 3 encryption (null cipher → real encryption)
- Audio backend wire protocols (PipeWire/PulseAudio native)
- aarch64 musl cross-compile for headless
- tarpc feature-gating refinement
- `async-trait` full migration blocked by `dyn` dispatch on 8 traits (awaiting `async_fn_in_dyn_trait` stabilization)

## For Ecosystem Teams

- petalTongue BTSP default provider is now `security` (env: `BTSP_PROVIDER`), no longer assumes `beardog`
- All socket path fallbacks use centralized constants — no more duplicate `/tmp/biomeos/` templates
- Production code has zero hardcoded primal names in runtime paths
