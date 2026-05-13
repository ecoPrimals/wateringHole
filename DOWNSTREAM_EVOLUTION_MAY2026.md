---

**ecoPrimals Downstream Evolution — May 13, 2026 (Phase 32 — Tier 2 DONE)**
**From**: primalSpring v0.9.25 (Phase 32 — Tower=3, Nest=provenance trio, 13 primals)
**For**: All spring teams

**What happened**: **Tier 2 convergence is COMPLETE** — all 7 delta springs have
wired `toadstool.validate` and `barracuda.precision.route` via JSON-RPC IPC.
Combined with Tier 4 (all 8/8 IPC-first), the delta is fully wired for NUCLEUS
deployment. Phase 32 atomic model: skunkBat in Tower (3 primals), Nest
reconciled with provenance trio (7 primals). All 13 primals at zero gate debt.
Pillars 1, 4, and 5 MET. **Atomic niche assignments formalized** — each spring
owns a specific composition tier for stress-testing before downstream handoff.
See `SPRING_ATOMIC_NICHE_ASSIGNMENTS.md`.

**hotSpring operates as a thermal niche** — own cadence on GPU hardware with
the compute trio. All other springs target the standard IPC pipeline.

**Spring UniBin binaries are now tractable for plasmidBin deployment** — each
spring produces a single binary with `certify`/`validate`/`serve`/`status`/`version`
subcommands. See `fossilRecord/PROJECTNUCLEUS_POST_INTERSTADIAL_FINDINGS_UNIBIN_HANDOFF_MAY10_2026.md`.

**Pull primalSpring, infra/wateringHole, and infra/plasmidBin before starting and all primals/ repos.**

## What this means for you

The Phase 45 deployment pipeline you absorbed is still your foundation — 46 pre-built genomeBin binaries across 6 target triples, live NUCLEUS deployable from plasmidBin. What's new is the **rewiring imperative**: your spring-local `barracuda/` and `ecoPrimal/` directories still link barraCuda as a library. That was correct during mountain season when you were evolving the math. Now that primals have absorbed it, you rewire to binary-only IPC. The computation flowing through ecobin primals is simultaneously visualizable by petalTongue and provenance-trackable by sweetGrass — rewiring, visualization, and attribution converge.

## YOUR NEXT STEP — SHADOW RUNS AND TIER 2

Library-to-binary rewiring is **DONE** (all 8 springs at Tier 4). The next
evolution target is interstadial exit — shadow runs executing, lithoSpore
integration, and Tier 2 science API convergence.

```
Python baseline (L1) → Rust proof (L2) → guideStone bare (L3) → NUCLEUS validated (L4) → Tier 4 IPC-first
                                                                                             YOU ARE HERE
                                                                                                  ↓
                                              Shadow runs → lithoSpore integration → Tier 2 (toadstool.validate)
                                                                                                 GO HERE
```

### Rewiring Tier Model

| Tier | What it means | What you do |
|------|--------------|-------------|
| **2** | IPC routing exists; bulk science still links library | Add IPC code paths gated by feature flag |
| **3** | Library and IPC lanes run side-by-side; parity validated | Compare library vs IPC results for every domain method |
| **4** | Library dep dropped; all compute through ecobin IPC | Flip default to IPC-only; library becomes opt-in fallback |

### Step 1 — Read the audit

Your full rewiring inventory is in `infra/wateringHole/SPRING_NUCLEUS_AUDIT_MAY2026.md`. Find your spring's section. It lists your local primal directories, Cargo path deps, IPC surface area, and specific evolution targets.

### Step 2 — Adopt the three standardization patterns

Every spring should adopt these patterns from siblings who pioneered them:

1. **`primal-proof` Cargo feature** (from healthSpring): Add a feature flag to your `Cargo.toml` that gates library vs IPC compilation. When enabled, domain math routes through ecobin primals over IPC. When disabled, falls back to in-process library. This lets you rewire incrementally without breaking CI.

2. **`src/ipc/` directory with per-primal modules** (from ludoSpring): Create `ipc/barracuda.rs`, `ipc/toadstool.rs`, `ipc/nestgate.rs`, `ipc/coralreef.rs`. Add `ipc/provenance/{rhizocrypt.rs, loamspine.rs, sweetgrass.rs}` for trio wiring. This is the canonical directory layout.

3. **`PRIMAL_PROOF_IPC_MAPPING.md`** (from hotSpring): Document every `barracuda::` call in your domain and map it to the corresponding barraCuda JSON-RPC method. This is your rewiring checklist.

### Step 3 — Wire petalTongue

Your science output maps to existing petalTongue DataBinding channel types. See `infra/wateringHole/petaltongue/PETALTONGUE_SPRING_SCIENCE_MAP.md` for your spring's channel mapping.

When you rewire to IPC, the JSON-RPC result payloads are already JSON-serialized and can be streamed directly to petalTongue as DataBinding inputs. The computation presents itself.

### Step 4 — Wire sweetGrass

Your experiments should produce attribution braids. See `infra/wateringHole/SWEETGRASS_SPRING_BRAID_PATTERNS.md` for your spring's braid pattern (agents, activities, entities, reproducibility claims).

ludoSpring's `ipc/provenance/{rhizocrypt.rs, loamspine.rs, sweetgrass.rs}` is the reference implementation. Copy the directory structure, adapt domain names.

### Step 5 — Document gaps and hand back

Any primal that misbehaves, returns unexpected formats, or is missing a capability — document it and hand back to primalSpring via `docs/PRIMAL_GAPS.md`.

## WHERE EVERYONE STANDS (Phase 32, May 13)

All 8/8 springs at **Tier 4 IPC-first** + **Tier 2 converged** — 14,000+ total tests.
Every delta spring has wired `toadstool.validate` and `barracuda.precision.route`.
**Atomic niche assignments** formalized (see `SPRING_ATOMIC_NICHE_ASSIGNMENTS.md`).

| Spring | gS | Tests | Tier | Atomic Niche | Next Step |
|--------|---:|------:|:----:|:-------------|-----------|
| primalSpring | L8 | 618 | 4+2 | Coordinator (all compositions) | Shadow run validation, CompositionContext L2 pass |
| hotSpring | L6 | 1,025 | 4+2 | **Node** (thermal niche — GPU sovereign) | Compute trio sovereignty, own cadence |
| healthSpring | L5 | 1,014 | 4+2 | **Nest** (provenance trio) | Ionic bridge, BTSP FAMILY_SEED interop |
| neuralSpring | L5 | 907 | 4+2 | **Meta-tier** (AI inference) | NestGate weight IPC, B1 lithoSpore module |
| wetSpring | L4 | 2,077 | 4+2 | **Full NUCLEUS** (all atomics) | 4 PGs (trio live, `capability.resolve`) |
| airSpring | L4 | 1,413 | 4+2 | **Tower+Node** (sensor→compute) | LTEE E3 lithoSpore packaging |
| groundSpring | L4 | 1,123 | 4+2 | **Tower+Nest** (data provenance) | lithoSpore module integration |
| ludoSpring | L4 | 858 | 4+2 | **Tower** (interactive trust) | Composition-only niche, Thread 9+10 |

### Convergence Priority (Niche Depth + Downstream Handoff)

Tier 2 convergence is **DONE** — all springs have wired `toadstool.validate`,
`toadstool.list_workloads`, and `barracuda.precision.route`. The next frontier
is **niche depth** and **downstream handoff** to sporeGarden products:

1. **Atomic niche stress-testing** — each spring validates its assigned composition tier (see `SPRING_ATOMIC_NICHE_ASSIGNMENTS.md`)
2. **lithoSpore module integration** — groundSpring B2+B1, neuralSpring B1 ready, wetSpring B7, healthSpring B5 packaging
3. **Shadow run participation** — BearDog TLS, NestGate content pipeline (projectNUCLEUS owns)
4. **Domain-specific composition depth** — provenance trio, ionic bonds, petalTongue

## WHAT'S NEW (Phase 32, May 13)

- **Tier 2 convergence COMPLETE**: All 7 delta springs wired `toadstool.validate` + `barracuda.precision.route`. 14,000+ total tests.
- **Atomic niche assignments formalized**: Each spring owns a composition tier for stress-testing (`SPRING_ATOMIC_NICHE_ASSIGNMENTS.md`).
- **hotSpring thermal niche**: Own cadence on GPU hardware. Compute trio sovereignty delegated to hotSpring on biomeGate.
- **primalSpring local debt swept**: Zero clippy warnings, docs reconciled, fossilRecord references updated, stale specs bannered.
- **plasmidBin automation hardened**: Idempotent harvest, post-harvest BLAKE3 validation, error propagation.
- **All sentinels RESOLVED**: toadStool Phase C COMPLETE (S250), Songbird VPS relay OPS-READY (W202), coralReef FECS STABILITY PROOF (Sprint 7).
- **lithoSpore Pillar 4 PASS**: Module 1+2 Tier 1+2 with BLAKE3 provenance. Now 4/7 modules passing.

**Previous milestones (May 12)**:
- Tier 4 rewiring COMPLETE: 8/8 springs IPC-first. Pillars 1, 4, 5 MET.
- Phase 32 atomic model: skunkBat in Tower, Nest reconciled. 13 primals at zero gate debt.
- 413 canonical methods (301 exercised, 72%). Wave 10 complete.

**Previous milestones (May 10)**:
- Primordial extinction: 8/8 UniBin, zero debt markers.
- All 11 upstream gaps resolved (JH-11, GAP-03/06/09/12, etc.).
- Sovereignty horizons: bearDog TLS, songbird NAT, petalTongue web, biomeOS `composition.status`.

## KNOWN ISSUES (SO YOU DON'T HIT THEM)

| Issue | Workaround |
|-------|-----------|
| beardog requires `BEARDOG_FAMILY_SEED` env | Export before launch |
| coralReef `--port` no longer works | Use `--rpc-bind` for TCP (iter84 change) |
| songbird needs security provider env | `export SONGBIRD_SECURITY_PROVIDER=beardog` |
| nestgate refuses insecure JWT | `export NESTGATE_JWT_SECRET="$(head -c 32 /dev/urandom \| base64)"` |
| sweetGrass requires BTSP handshake for TCP | Use UDS, or complete BTSP negotiation first |
| Songbird/petalTongue speak HTTP on UDS | Use `is_protocol_error()` or classify as SKIP |
| beardog resets connection without BTSP | Expected — BTSP handshake required for crypto calls |
| rhizoCrypt/loamSpine byte arrays vs hex | API ergonomics gap — use hex strings, trio team aware |

## KEY REFERENCES

| Topic | Location |
|-------|----------|
| **Spring NUCLEUS Audit** | `infra/wateringHole/SPRING_NUCLEUS_AUDIT_MAY2026.md` |
| **UniBin plasmidBin readiness** | `infra/wateringHole/fossilRecord/PROJECTNUCLEUS_POST_INTERSTADIAL_FINDINGS_UNIBIN_HANDOFF_MAY10_2026.md` |
| **Post-interstadial downstream** | `infra/wateringHole/handoffs/PRIMALSPRING_POST_INTERSTADIAL_DOWNSTREAM_HANDOFF_MAY10_2026.md` |
| **petalTongue Science Map** | `infra/wateringHole/petaltongue/PETALTONGUE_SPRING_SCIENCE_MAP.md` |
| **sweetGrass Braid Patterns** | `infra/wateringHole/SWEETGRASS_SPRING_BRAID_PATTERNS.md` |
| Ecosystem alignment (Phase 58) | `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` |
| Evolution cycle (v1.4.0) | `infra/wateringHole/ECOSYSTEM_EVOLUTION_CYCLE.md` |
| Depot workflow | `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md` |
| guideStone standard | `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` |
| Your manifest | `primalSpring/graphs/downstream/downstream_manifest.toml` |
| Provenance trio pattern | `infra/wateringHole/fossilRecord/consolidated-apr2026/SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` |
| Visualization integration | `infra/wateringHole/petaltongue/VISUALIZATION_INTEGRATION_GUIDE.md` |
| Gap registry | `primalSpring/docs/PRIMAL_GAPS.md` |
| Provenance handoff | `infra/wateringHole/handoffs/PROVENANCE_TRIO_OPERATIONAL_HANDOFF_MAY2026.md` |
| toadStool patterns | `infra/wateringHole/handoffs/TOADSTOOL_COMPOSITION_PATTERNS_HANDOFF_MAY2026.md` |

---

**The math is absorbed. The stack is deployed. The channels are encrypted. Now rewire, visualize, and braid.**
