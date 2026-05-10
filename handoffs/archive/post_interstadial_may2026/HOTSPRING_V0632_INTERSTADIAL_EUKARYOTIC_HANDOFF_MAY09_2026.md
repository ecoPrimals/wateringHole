# hotSpring v0.6.32 Interstadial Eukaryotic Evolution Handoff

**Date**: May 9, 2026  
**From**: hotSpring v0.6.32  
**Context**: Primordial Extinction Wave — primalSpring v0.9.25 interstadial  
**License**: AGPL-3.0-or-later

---

## Summary

hotSpring has completed its interstadial eukaryotic evolution following the
primalSpring v0.9.25 primordial extinction wave. The spring evolved from a
prokaryotic layout (scattered binaries, bare suppressions, no unified
certification) to an eukaryotic architecture (UniBin, certification organelle,
scenario registry, consolidated IPC namespace).

## What Changed

| Dimension | Before | After |
|-----------|--------|-------|
| Binary entry | 100+ separate `[[bin]]` targets | Single `hotspring_unibin` + legacy bins |
| Certification | `hotspring_guidestone` standalone binary | `certification/` library organelle (L0–L5) |
| Validation | Individual validate_* binaries | 6 absorbed scenarios in `validation/scenarios/` |
| IPC | Scattered across 8+ files | Consolidated `ipc/` namespace |
| `#[allow]` hygiene | 9 bare suppressions | Zero bare (all have `reason =`) |
| Deprecated patterns | None of the banned 6 present | Confirmed clean |
| TODO/FIXME markers | Zero | Zero (maintained) |
| Fossil record | `_fossilized/` only | `fossilRecord/experiments_prokaryotic_may2026/` |
| Tests | 1002 | 1002 (all pass) |

## Architecture

### UniBin CLI

```text
hotspring certify              # L0-L5 composition certification
hotspring certify --bare       # L0 only (structural, no primals)
hotspring validate             # all 6 absorbed scenarios
hotspring validate --track nuclear-physics
hotspring validate --tier rust  # Tier 1 only (no IPC)
hotspring validate --list      # list all scenarios
hotspring status               # composition health summary
hotspring version              # version info
```

### Certification Organelle (L0–L5)

| Layer | Name | Description |
|-------|------|-------------|
| 0 | Bare Properties | Deterministic, traceable, self-verifying, agnostic, tolerance-documented |
| 1 | Discovery | NUCLEUS primals reachable via CompositionContext |
| 2 | Scalar Parity | stats.mean IPC matches Rust baseline |
| 3 | Vector Parity | tensor.matmul IPC matches Rust baseline |
| 4 | Domain Science | SEMF end-to-end via IPC |
| 5 | Full Composition | Crypto witness + compute dispatch |

### Validation Scenarios (6 absorbed)

| Scenario | Track | Tier | Provenance |
|----------|-------|------|------------|
| semf-parity | nuclear-physics | rust | validate_nuclear_eos |
| lattice-plaquette | lattice-qcd | rust | validate_pure_gauge |
| spectral-lanczos | spectral-theory | rust | validate_lanczos |
| md-yukawa-ocp | molecular-dynamics | rust | validate_md |
| composition-health | composition-parity | rust | validate_nucleus_composition |
| tolerance-ordering | domain-science | rust | hotspring_guidestone |

### IPC Consolidation

New `barracuda/src/ipc/` module provides unified namespace:

| Submodule | Source | Key Types |
|-----------|--------|-----------|
| `ipc::discovery` | `primal_bridge` | `NucleusContext`, `PrimalEndpoint` |
| `ipc::composition` | `composition` | `AtomicType`, `validate_atomic` |
| `ipc::glowplug` | `glowplug_client` | `GlowplugClient` |
| `ipc::ember` | `fleet_ember` | `EmberClient`, `FleetEmberHub` |
| `ipc::fleet` | `fleet_client` | `FleetRouter` |
| `ipc::squirrel` | `squirrel_client` | `SquirrelError` |
| `ipc::toadstool` | `toadstool_report` | `PerformanceMeasurement` |
| `ipc::signing` | `receipt_signing` | `sign_receipt` |

## New Files

| File | Purpose |
|------|---------|
| `barracuda/src/bin/hotspring/main.rs` | UniBin entry point |
| `barracuda/src/bin/hotspring/cli.rs` | clap subcommands |
| `barracuda/src/certification/mod.rs` | Certification engine (L0–L5) |
| `barracuda/src/certification/bare.rs` | Bare properties validation |
| `barracuda/src/certification/composition_probes.rs` | IPC parity probes |
| `barracuda/src/ipc/mod.rs` | Consolidated IPC namespace |
| `barracuda/src/validation/scenarios/mod.rs` | Scenario module with registry |
| `barracuda/src/validation/scenarios/registry.rs` | ScenarioMeta, Track, Tier |
| `barracuda/src/validation/scenarios/s_*.rs` | 6 scenario modules |
| `docs/PRIMAL_PROOF_IPC_MAPPING.md` | Library↔IPC mapping table |
| `fossilRecord/experiments_prokaryotic_may2026/` | Fossil snapshot |

## Build Verification

```
cargo fmt --check           → clean
cargo clippy --lib          → zero warnings
cargo test --lib            → 1002 pass, 0 fail
hotspring_unibin --version  → compiles
```

## Remaining Gaps (Tier 2 → Tier 3)

1. **`barracuda` path dependency**: Not yet `optional = true` — required for Tier 3
2. **`primal-proof` feature flag**: Not yet implemented (reference: healthSpring)
3. **Live IPC scenarios**: All 6 current scenarios are Tier 1 (Rust) — need Tier 2 (Live) scenarios
4. **Remaining ~94 binaries**: Only 6 experiments absorbed; more candidates exist
5. **Legacy binary retirement**: `hotspring_guidestone` still active (transition target)

## Cross-Spring Parity Update

| Metric | Before | After |
|--------|--------|-------|
| Tier | 2 | 2 (targeting 3) |
| UniBin | No | Yes (hotspring_unibin) |
| Certification organelle | No | Yes (L0–L5) |
| Scenario registry | No | Yes (6 scenarios) |
| IPC consolidation | No | Yes (ipc/ namespace) |
| Fossil record | Partial (_fossilized/) | Yes (fossilRecord/) |
| Bare #[allow] | 9 | 0 |
| primalSpring dep | path (unversioned) | path → v0.9.25 |
