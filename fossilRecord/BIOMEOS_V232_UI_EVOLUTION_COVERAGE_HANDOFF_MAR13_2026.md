# biomeOS V2.32 — UI Evolution + Deep Debt + Coverage Push

**Date**: March 13, 2026
**From**: biomeOS v2.32
**To**: petalTongue, all springs, toadStool teams
**Tests**: 4,033 passing (0 failures, 164 ignored)
**Coverage**: 75.36% region | 78.21% function | 74.09% line
**Clippy**: 0 warnings | **Format**: PASS | **C deps**: 0

---

## Summary

Three major deliverables:

1. **UI Evolution** — TUI deprecated, petalTongue canonical universal UI primal
2. **Deep Debt Resolution** — Logic/IO separation, credential security, capability discovery evolution
3. **Coverage Push** — 4,033 tests (+885), 75.36% region coverage (+3.9pp)

---

## Part 1: UI Evolution — petalTongue Canonical

### TUI Deprecation
- `crates/biomeos-cli/src/tui/` module (2,213 lines) feature-gated behind `deprecated-tui`
- `ratatui` 0.24 and `crossterm` 0.27 made optional dependencies (default: off)
- `biomeos monitor dashboard` prints deprecation guidance → petalTongue when TUI disabled
- `biomeos-ui` crate confirmed clean: orchestration + capability management only, no rendering
- Legacy examples marked deprecated in doc comments

### What petalTongue Needs
- biomeOS no longer ships its own TUI — petalTongue is the universal UI surface
- `biomeos-ui` provides the orchestration layer petalTongue connects to via JSON-RPC
- petalTongue can use `biomeos-ui`'s capability discovery, device management, and event system

---

## Part 2: Deep Debt Resolution

### Logic/IO Separation
~20 CLI commands and mode files refactored following petalTongue's pattern:
- Pure functions extracted: `format_*()`, `compute_*()`, `resolve_*()`
- Each returns data (strings, structs); thin wrappers handle `println!`/rendering
- All extracted functions have dedicated unit tests
- Files: health.rs, monitor.rs, fossil.rs, spore.rs, deploy.rs, discover.rs, nucleus.rs, plasmodium.rs, doctor.rs, enroll.rs, neural_api.rs, api.rs, main.rs, widgets.rs

### Capability Discovery Evolution
- `providers_for_capability()` now uses `CapabilityTaxonomy::resolve_to_primal()` (was hardcoded match)
- `capability_from_primal_name()` deprecated
- New `discover_by_capability()` in `biomeos-primal-sdk`
- `TOADSTOOL_ENDPOINT` env var → `BIOMEOS_COMPUTE_ENDPOINT` (legacy fallback retained)
- `socket_path_for_capability()` resolves socket paths via taxonomy

### Credential Security
- `family_credentials.rs`: HMAC-SHA256 integrity verification using family seed
- Versioned format: v2 (payload + HMAC) with v1 legacy backward compatibility
- File permissions: 0o600 on Unix
- Tests: legacy format loading, v2 save/load roundtrip, tamper detection

### System Metrics
- `live_service.rs` placeholder → real `/proc/uptime` via `SystemInspector`
- Real resource usage (CPU, memory, disk, network) via `biomeos-system`

### Dead Code Cleanup
- Wire format fields: standardized annotation
- Future-use items: doc comments explaining planned usage
- Removed truly dead production code

---

## Part 3: Coverage Push

63+ new test functions across 16 modules:

| Module | Tests Added | Focus |
|--------|-------------|-------|
| neural_executor | 4 | Topological sort, capability split, env substitution |
| genome (CLI) | 3 | Architecture parsing, storage dirs |
| universal_biomeos_manager | 5 | Service parsing, discovery construction |
| dark_forest | 3 | Beacon size, peer struct, version values |
| vm_federation | 4 | IP parsing, VM name extraction |
| bootable | 4 | Target equality, media builder, GRUB config |
| nucleus client | 3 | JSON-RPC response handling |
| p2p_coordination | 2 | Status computation |
| verify (CLI) | 2 | Status display variants |
| health (CLI) | 4 | Score calculation, boundaries |
| federation (CLI) | 3 | Member parsing, truncation |
| discovery (CLI) | 4 | Type filtering, categorization |
| chimera (CLI) | 5 | YAML ID parsing |
| server_lifecycle | 2 | Mode string detection |
| nucleus/discovery | 3 | Service-to-endpoint conversion |
| genome/build (API) | 6 | Architecture parsing |

### Dependency Assessment
- `docs/NIX_TO_RUSTIX_MIGRATION_ASSESSMENT.md` created
- `rustix` covers ~70% of current `nix` usage (statvfs, kill, signal, errno)
- Custom work needed: mount, mknod/makedev, ioctl
- Suggested migration order: low-risk crates first

---

## Quality Summary

| Metric | v2.30 | v2.32 | Change |
|--------|-------|-------|--------|
| Tests passing | 3,148 | 4,033 | +885 |
| Region coverage | 71.47% | 75.36% | +3.89pp |
| Function coverage | 74.32% | 78.21% | +3.89pp |
| Line coverage | 69.88% | 74.09% | +4.21pp |
| Clippy warnings | 0 | 0 | — |
| Unsafe code | 0 | 0 | — |
| Production panics | 0 | 0 | — |
| Production unwraps | 0 | 0 | — |

---

## For petalTongue Team

biomeOS no longer has a TUI. The `biomeos monitor dashboard` command now prints:
```
biomeOS TUI is deprecated. Use petalTongue for UI:
  petaltongue connect biomeos
```

The `biomeos-ui` crate remains as orchestration infrastructure:
- `InteractiveUIOrchestrator` — capability-based primal connections
- `DeviceManagementProvider` — device lifecycle
- `EventSystem` — push-based event broadcasting
- `SuggestionManager` — AI-powered suggestions

petalTongue should connect via JSON-RPC to these services.

---

## For toadStool Team

`TOADSTOOL_ENDPOINT` env var is deprecated. Use `BIOMEOS_COMPUTE_ENDPOINT` instead.
Legacy fallback is retained but will be removed in a future version.
