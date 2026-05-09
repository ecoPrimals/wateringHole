# Interstadial Wave — Primordial Extinction Handoff

**Date**: May 9, 2026
**From**: primalSpring v0.9.25 (Phase 60+ INTERSTADIAL)
**For**: All delta spring teams, projectNUCLEUS integrators
**License**: AGPL-3.0-or-later

---

## What This Is

primalSpring has completed its eukaryotic evolution. This handoff defines the
**primordial extinction wave** — the evolutionary pressure that delta springs
must absorb over the next few days. The patterns are proven, the exemplar is
clean, and the fossil record is complete. Your turn.

---

## The Exemplar: What primalSpring Completed

| Dimension | Before (Prokaryotic) | After (Eukaryotic) |
|-----------|---------------------|---------------------|
| Binaries | 89 experiment bins + 3 standalone | Single `primalspring_unibin` |
| Guidestone | Standalone binary (`primalspring_guidestone`) | Absorbed as `certification/` organelle (L0-L8) |
| Experiments | Individual `main.rs` per experiment | 20 absorbed scenarios in `validation/scenarios/` with `ScenarioRegistry` |
| IPC | Mixed `PrimalClient`, `AtomicHarness`, `discover_primal()` | `CompositionContext` throughout (5-tier discovery) |
| Deprecated APIs | Scattered, bare `#[allow(deprecated)]` | All deprecated with `note`, all suppressions with `reason` |
| Fossil record | None | 3 dated snapshots in `fossilRecord/` |
| Tests | 661 | 680 (zero failures, zero warnings) |
| Debt markers | Some | Zero TODO/FIXME/HACK/DEBT |

### The UniBin CLI

```text
primalspring certify              # L0-L8 composition certification
primalspring certify --layer 3    # run up to layer 3
primalspring certify --bare       # L0 only, no primals needed
primalspring validate             # run all validation scenarios
primalspring validate --track atomic-composition
primalspring validate --tier rust  # Tier 1 only (no IPC)
primalspring validate --tier live  # Tier 2 only (requires primals)
primalspring validate --list      # list all scenarios
primalspring serve                # JSON-RPC 2.0 IPC server
primalspring status               # composition health summary
primalspring version              # version info
```

### Two-Tier Validation

- **Tier 1 (Rust)**: Pure structural validation, no IPC. Safe for CI.
- **Tier 2 (Live)**: Requires deployed primals from plasmidBin. Exercises live composition behavior.

---

## The Extinction: What Delta Springs Must Do

### Phase 1: Absorption (Days 1-2)

Pull and study the exemplar. Every spring team should:

1. `git pull` on primalSpring, infra/wateringHole, infra/plasmidBin, and all primals.
2. Read `primalSpring/ARCHITECTURE.md` — the eukaryotic cell model.
3. Read `primalSpring/wateringHole/PRIMALSPRING_V0925_UNIBIN_EUKARYOTIC_HANDOFF_MAY09_2026.md`.
4. Read `primalSpring/docs/VALIDATION_TIERS.md` — the two-tier model.
5. Run `primalspring_unibin validate --tier rust` to see the scenario registry in action.
6. Run `primalspring_unibin certify --bare` to see the certification engine.

### Phase 2: Primordial Extinction (Days 2-4)

Apply evolutionary pressure to your own spring:

#### 2a. Pin primalSpring v0.9.25

Update your guidestone and composition `Cargo.toml` dependencies. This is the
gate — v0.9.25 provides `CompositionContext`, `ScenarioMeta`, `ScenarioRegistry`,
and the certification engine API.

| Spring | Current Pin | Action |
|--------|------------|--------|
| healthSpring | v0.9.17 | **MUST upgrade** |
| All others | v0.9.21-v0.9.24 | Upgrade to v0.9.25 |

#### 2b. CompositionContext Migration

Replace all deprecated IPC patterns:

| Old Pattern | New Pattern |
|-------------|------------|
| `PrimalClient::connect(path)` | `CompositionContext::from_live_discovery_with_fallback()` |
| `discover_primal("name")` | `ctx.call("capability", "method", params)` |
| `discover_by_capability("cap")` | `ctx.call("capability", "method", params)` |
| `AtomicHarness::spawn(config)` | Deploy via plasmidBin + biomeOS |
| `spawn_primal(name, args)` | Deploy via plasmidBin + biomeOS |
| `probe_primal(addr)` | `ctx.health_check("capability")` |
| `neural_api_healthy()` | `NeuralBridge::discover()` + `ctx.call(...)` |

#### 2c. UniBin Consolidation

For each spring, absorb experiment bins into a single unibin:

1. **Create `certification/` module** — absorb your guidestone layers as library code.
   Reference: `primalSpring/ecoPrimal/src/certification/`.
2. **Create `validation/scenarios/` module** — absorb representative experiments as
   scenario modules with `ScenarioMeta` (id, track, tier, provenance).
   Reference: `primalSpring/ecoPrimal/src/validation/scenarios/`.
3. **Create the unibin** — single binary with `certify`, `validate`, `serve`,
   `status`, `version` subcommands. Reference: `primalSpring/ecoPrimal/src/bin/primalspring/`.
4. **Fossilize** — snapshot pre-extinction experiment sources to `fossilRecord/{name}_prokaryotic_may2026/`.

#### 2d. Deprecated API Cleanup

- All `#[deprecated]` annotations must include `note = "use ... instead"`.
- All `#[allow(deprecated)]` must include `reason = "..."`.
- Zero bare suppressions. This is a hard gate.

#### 2e. Fossil Record

Snapshot pre-extinction patterns to `fossilRecord/` with dated README:

```
fossilRecord/
  {pattern}_pre_interstadial_may2026/
    README.md  (provenance: what, when, why, what supersedes)
    src/       (snapshot of superseded code)
```

### Phase 3: Validation (Days 4-5)

After evolution, every spring must pass:

```bash
cargo build --workspace
cargo fmt --check
cargo clippy --workspace --all-targets  # zero warnings
cargo test --workspace --lib --tests     # zero failures
```

Plus spring-specific:
- `{spring}_unibin validate --tier rust` — all scenarios pass
- `{spring}_unibin certify --bare` — L0 certification passes

---

## Per-Spring Specific Guidance

### hotSpring

**Priority targets**: Create `src/ipc/` directory (scattered IPC needs a home),
absorb experiment bins into unibin, create `PRIMAL_PROOF_IPC_MAPPING.md`.
Your `composition.rs` dual-lane model is the rewiring template — consolidate it.

### wetSpring

**Priority targets**: Route handler compute through ecobin (15 IPC handlers serve
in-process results — route underlying compute through IPC). UniBin consolidation.
Your rich handler dispatch tree is the template for diverse-science springs.

### neuralSpring

**Priority targets**: Graduate `ipc_dispatch.rs` to full `src/ipc/` tree. UniBin
consolidation. Unique constraint: inference pipeline is latency-sensitive — batch
IPC calls where possible.

### healthSpring

**Priority targets**: Pin v0.9.25 (currently v0.9.17). Expand `primal-proof` feature
to full library surface. Flip default to IPC-only. Your `primal-proof` feature flag
is the most adoptable innovation — every spring should copy it.

### ludoSpring

**Priority targets**: Close remaining `barracuda::` calls not gated by `ipc` feature.
Make `ipc` the default. Verify 60Hz tick budget with IPC-only. UniBin consolidation
of 100 experiment crates. Your per-trio-primal IPC modules are the reference.

### airSpring

**Priority targets**: Add workspace-root `deny.toml` banning `aws-lc-sys`. Unpause
delta absorption — build guidestone against live NUCLEUS. Target gS L4+. Good IPC
foundation already (`src/ipc/` + `src/rpc/` + `src/biomeos/`).

### groundSpring

**Priority targets**: Expand `ipc.rs` into `src/ipc/` tree. Build guidestone against
live NUCLEUS. Your optional `barracuda` feature gate is the transitional pattern.
6 deploy graphs are surprisingly strong for pre-delta — validate them.

---

## Upstream Wave Goals (primalSpring + primals)

While delta springs absorb, the upstream is working on:

| Wave | Goal | Owner | Impact |
|------|------|-------|--------|
| **1** | JH-11: Cross-Primal Token Federation | bearDog + biomeOS | Unlocks Tier 4 rewiring, authenticated cross-atomic IPC |
| **2** | JH-5: Cross-Primal Audit Log Forwarding | skunkBat + rhizoCrypt + sweetGrass | Cross-primal security event audit trail |
| **3** | Remaining ~69 scenario absorptions | primalSpring | Full eukaryotic scenario coverage |
| **4** | Legacy binary retirement | primalSpring | Remove `primalspring_primal`, `primalspring_guidestone`, `validate_all` |
| **5** | PG-54: Adaptive Tick Model | primalSpring + biomeOS | Domain-specific tick modes (fixed, adaptive, event-driven) |

---

## Key References

| Document | Location |
|----------|----------|
| primalSpring Architecture | `primalSpring/ARCHITECTURE.md` |
| UniBin Eukaryotic Handoff | `primalSpring/wateringHole/PRIMALSPRING_V0925_UNIBIN_EUKARYOTIC_HANDOFF_MAY09_2026.md` |
| Two-Tier Validation | `primalSpring/docs/VALIDATION_TIERS.md` |
| Interstadial Fossilization | `primalSpring/wateringHole/INTERSTADIAL_FOSSILIZATION_HANDOFF.md` |
| Primal Gap Registry | `primalSpring/docs/PRIMAL_GAPS.md` |
| Cross-Spring Parity Scorecard | `primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` |
| Spring NUCLEUS Audit | `infra/wateringHole/SPRING_NUCLEUS_AUDIT_MAY2026.md` |
| Capability Registry | `primalSpring/config/capability_registry.toml` (389 methods) |
| CompositionContext docs | `primalSpring/ecoPrimal/src/composition/context.rs` |
| Fossil Record Index | `primalSpring/fossilRecord/README.md` |

---

## Timeline

```
May 9 (today)   — Handoff delivered. Pull everything.
May 10-11       — Absorption. Study exemplar, plan spring-specific evolution.
May 11-13       — Primordial extinction. UniBin consolidation, CompositionContext
                  migration, deprecated pattern fossilization.
May 13-14       — Validation. Zero warnings, zero failures, unibin passes.
May 14+         — Next stadial wave. JH-11 federation, full primal compositions.
```

**The eukaryotic cell is the target. The fossil record is the proof. The extinction event is now.**
