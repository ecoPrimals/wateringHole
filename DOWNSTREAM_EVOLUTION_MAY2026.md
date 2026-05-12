---

**ecoPrimals Downstream Evolution — May 12, 2026 (Phase 32 Atomic Model)**
**From**: primalSpring v0.9.25 (Phase 32 — Tower=3, Nest=provenance trio, 13 primals)
**For**: All spring teams

**What happened**: Tier 4 library-to-binary rewiring is **COMPLETE** — all 8/8
springs are IPC-first (`default = []`, barraCuda optional). Phase 32 evolves the
atomic model: skunkBat joins Tower (3 primals), Nest reconciled with provenance
trio (7 primals). All 13 primals at zero gate debt. Pillar 5 (river delta) MET.
The next frontier is **shadow run execution** and **Tier 2 convergence**
(`toadstool.validate`, `toadstool.list_workloads` via JSON-RPC).

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

## WHERE EVERYONE STANDS (Phase 32, May 12)

All 8/8 springs at **Tier 4 IPC-first** — rewiring COMPLETE. 13,100+ total tests.
The next evolution target is **Tier 2 convergence** (JSON-RPC via `toadstool.validate`
+ `toadstool.list_workloads`), blocked on upstream Tier 2 Science API.

| Spring | gS | Tests | Tier | LTEE | Next Step |
|--------|---:|------:|:----:|:----:|-----------|
| primalSpring | L8 | 602 | 4 | coord | Shadow run validation, CompositionContext L2 pass |
| hotSpring | L6 | 1,025 | 4 | B2 | Trio rewire, sovereign dispatch on warm GPUs |
| healthSpring | L5 | 999 | 4 | B5 | BTSP FAMILY_SEED interop, ionic bridge |
| neuralSpring | L5 | 892 (IPC-first) | 4 | B1 | Tier 2 wired (`toadstool.validate` + `list_workloads`), NestGate wired, CapabilityRouter IPC, deep debt audit all-clear, B1 NUCLEUS workload TOML, Thread 5 ML_SURROGATES wired. V154. |
| wetSpring | L4 | 1,613 | 4 | B7 | 4 PGs (trio live, `capability.resolve`, NestGate, sovereignty) |
| airSpring | L4 | 1,389 | 4 | — | AG-005–012 (Squirrel, coralReef, dispatch, toadStool API) |
| groundSpring | L4 | 1,125 | 4 | B1-B3 | lithoSpore module integration (B2+B1 COMPLETE) |
| ludoSpring | L4 | 854 | 4 | — | Composition-only niche, notebooks, Thread 9+10 |

### Convergence Priority (Tier 2 — next frontier)

Tier 2 convergence requires `toadstool.validate` + `toadstool.list_workloads`
upstream (specified in `primalSpring/docs/LIVE_SCIENCE_API.md`, not yet
implemented). Until that lands, springs focus on:

1. **lithoSpore integration** — groundSpring B2+B1, neuralSpring B1 Rust binaries ready (V154 handoff shipped, LTEE B1 README + NUCLEUS workload TOML for lithoSpore team)
2. **Foundation thread seeding** — Threads 3, 4, 8, 9, 10 need expressions/targets
3. **Shadow run participation** — BearDog TLS, NestGate content pipeline
4. **Domain-specific composition depth** — provenance trio, ionic bonds, petalTongue

## WHAT'S NEW (Phase 32, May 12)

- **Tier 4 rewiring COMPLETE**: 8/8 springs at `default = []`, barraCuda optional, IPC-first. The rewiring imperative from May 10 is **done**.
- **Phase 32 atomic model**: skunkBat in Tower (3 primals), Nest reconciled with provenance trio (7 primals), NUCLEUS = 10 core + 3 meta = 13 total. Fragment versions 3.0.0.
- **Pillar 5 (river delta) MET**: All exit conditions satisfied (May 11).
- **NestGate Session 60**: `content.*` transport parity — all 8 methods on all 4 surfaces. Last L1 upstream debt cleared.
- **skunkBat JH-5 Phase 3 shipped**: Cross-primal audit forwarding wired (rhizoCrypt + sweetGrass).
- **Temporal ecosystem review**: Full audit at `primalSpring/docs/TEMPORAL_ECOSYSTEM_REVIEW_MAY12_2026.md`.
- **Live Science API specified**: `primalSpring/docs/LIVE_SCIENCE_API.md` — Tier 2 wire contract for `toadstool.validate`, `toadstool.list_workloads` (NOT YET IMPLEMENTED upstream).
- **413 canonical methods** (301 exercised, 72%): primalSpring registry. Zero drift.
- **Wave 10 complete**: Phase 32 atomic evolution, compute trio temporal shift, scorecard updated.

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
