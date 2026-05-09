# hotSpring v0.6.32 — Primal Evolution & Upstream Handoff

**Date:** May 8, 2026
**From:** hotSpring team
**To:** Upstream primal teams, primalSpring, river delta springs

---

## hotSpring Primal Integration State

hotSpring consumes 10 primals via NUCLEUS IPC. All routing is capability-based
via `niche::DEPENDENCIES` → `by_domain()` → `call_by_capability()`.

| Primal | Domain | Usage | Status |
|--------|--------|-------|--------|
| bearDog | `crypto` | Ed25519 receipt signing via `crypto.sign_ed25519` | PRODUCTION — graceful degradation when absent |
| songbird | `discovery` | Service discovery via `discovery.register` | PRODUCTION |
| coralReef | `shader` | GPU sovereign compile, WGSL→SASS lowering | PRODUCTION — aliased `coral-glowplug` |
| toadStool | `compute` | GPU dispatch, capability query, perf surface | PRODUCTION — capability + bootstrap socket |
| barracuda | `math` | Required dep — physics compute core | PRODUCTION (local, optional in Cargo.toml) |
| nestgate | `storage` | Data persistence, provenance | OPTIONAL |
| rhizoCrypt | `dag` | DAG session/event/merkle | PRODUCTION |
| loamSpine | `ledger` | Ledger sealing | PRODUCTION |
| sweetGrass | `attribution` | Provenance braids | PRODUCTION |
| squirrel | `ai` | ML inference (embed, complete) | OPTIONAL |

### Deprecated Surface (remove in v0.7.0)

Named accessors `toadstool()`, `beardog()`, `rhizocrypt()`, `loamspine()`,
`sweetgrass()`, `coralreef()` in `primal_bridge.rs` are `#[deprecated]`
since v0.6.33. All now delegate purely to `by_domain()` — hardcoded name
fallbacks have been removed.

---

## Findings for Upstream Primal Teams

### bearDog (crypto team)

- hotSpring uses only `crypto.sign_ed25519` for receipt signing
- `receipt_signing.rs` gracefully degrades to unsigned when bearDog absent
- No issues or debt — clean integration

### coralReef (shader/ember team)

- hotSpring is the heaviest consumer of sovereign compile pipeline
- 128 WGSL shaders compiled to SASS via coral-glowplug (SM35/SM70/SM120)
- `fleet_client.rs` and ember experiment binaries still use `/run/coralreef/`
  as fallback paths after FleetDiscovery — this is the standard runtime-dir
  convention, not true hardcoding
- **Gap:** `PRIMAL_ALIASES` only maps `coralreef` → `coral-glowplug`; if
  coralReef renames its socket stem, hotSpring needs updating

### toadStool (compute team)

- hotSpring routes GPU dispatch + capability query + performance surface
  reporting through toadStool
- `toadstool_report.rs` socket resolution now uses `niche::socket_dirs()`
  with live probing (no more hardcoded `/tmp` fallback)
- **Gap:** `validate_nucleus_node.rs` still uses `ctx.call("toadstool", ...)`
  — works but doesn't follow capability-based pattern

### squirrel (inference team)

- `squirrel_client.rs` discovers via `"inference"` prefix match
- `niche.rs` declares squirrel's domain as `"ai"` — potential mismatch
  if live primals advertise `ai.*` instead of `inference.*`
- **Action:** Harmonize `ai` vs `inference` domain naming

### primalSpring (registry team)

- **13 methods pending upstream addition** to canonical registry:
  `composition.health`, `compute.df64`, `compute.dispatch.capabilities`,
  `compute.f64`, `physics.fluid`, `physics.hmc_trajectory`,
  `physics.lattice_gauge_update`, `physics.lattice_qcd`,
  `physics.molecular_dynamics`, `physics.nuclear_eos`, `physics.radiation`,
  `physics.thermal`, `physics.wilson_dirac`
- Cross-sync test (`tools/check_method_strings.sh` + Rust integration test)
  ready to validate when these are added
- `capabilities.list` vs `capability.list` naming inconsistency: hotSpring
  local registry exposes `capabilities.list`, NUCLEUS probe uses
  `capability.list` — needs harmonization in Wire Standard

---

## NUCLEUS Composition Patterns

### What hotSpring Proved

1. **Three-tier validation**: Python → Rust CPU → NUCLEUS IPC (same
   tolerances, same exit codes). 25 papers through this arc.
2. **Atomic composition health probes**: Tower/Node/Nest atomics with
   `health.liveness` + `capability.list` per primal
3. **Capability-based routing**: Single source of truth in `niche::DEPENDENCIES`
   drives all composition, discovery, and validation
4. **Graceful degradation**: `HOTSPRING_NO_NUCLEUS=1` disables all IPC;
   every IPC path has a skip/degrade fallback
5. **guideStone bare mode**: 30/30 checks pass with zero primals deployed

### Patterns for Sibling Springs to Absorb

- `niche.rs` pattern: `LOCAL_CAPABILITIES`, `ROUTED_CAPABILITIES`, `DEPENDENCIES`
  as static declarations, not runtime config
- `primal_bridge.rs`: `NucleusContext::detect()` → socket scan → probe →
  capability-indexed HashMap
- `composition.rs`: `required_primals()` derived from `DEPENDENCIES` —
  eliminates separate hardcoded manifest
- `ValidationHarness` + `TelemetryWriter`: check/skip-aware with exit code 0/1/2
- Deploy graphs: per-domain TOML (5 graphs for hotSpring: QCD, plasma, nuclear
  EOS, spectral, sovereign GPU)

---

## biomeOS / neuralAPI Deployment Notes

- hotSpring registers with biomeOS via `lifecycle.register` + per-capability
  `capability.register` (see `niche::register_with_target`)
- IPC is Unix domain socket only — no TCP ports in NUCLEUS path
- Socket naming: `hotspring-physics-{family_id}.sock` under `socket_dirs()`
- neuralAPI integration: squirrel provides `inference.*` methods; hotSpring
  uses `inference.complete` and `inference.embed` through squirrel_client

---

## For River Delta / Downstream Springs

See companion document: `HOTSPRING_V0632_DOWNSTREAM_PATTERNS_HANDOFF_MAY08_2026.md`

Key points:
- projectNUCLEUS workload TOML contract (metadata/execution/resources/security)
- foundation Thread 2 (plasma/QCD) anchors reference hotSpring
- Stable validation binary surface needed for plasmidBin
- Path portability: use ECOPRIMALS_ROOT or wrappers, not absolute paths
