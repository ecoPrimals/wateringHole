---

**ecoPrimals Downstream Evolution — May 9, 2026 (Updated)**
**From**: primalSpring v0.9.25 (Phase 60+ INTERSTADIAL — Eukaryotic UniBin Evolution)
**For**: All spring teams

**What happened**: primalSpring completed its eukaryotic evolution — single UniBin binary absorbing guidestone certification (L0-L8), 20 validation scenarios (9 tracks, Rust/Live tiers), and IPC server. All 89 experiments rewired to `CompositionContext`. All deprecated patterns (`AtomicHarness`, `PrimalClient`, `spawn_primal`, old probes) fossilized with reasons. 680 tests, zero clippy warnings, zero unsafe, zero bare `#[allow]`. BTSP Phase 3 13/13. 13/13 primals at zero debt. The primordial extinction wave now targets delta springs: absorb UniBin pattern, pin v0.9.25, undergo the same evolutionary pressure primalSpring completed.

**Pull primalSpring, infra/wateringHole, and infra/plasmidBin before starting and all primals/ repos.**

## What this means for you

The Phase 45 deployment pipeline you absorbed is still your foundation — 46 pre-built genomeBin binaries across 6 target triples, live NUCLEUS deployable from plasmidBin. What's new is the **rewiring imperative**: your spring-local `barracuda/` and `ecoPrimal/` directories still link barraCuda as a library. That was correct during mountain season when you were evolving the math. Now that primals have absorbed it, you rewire to binary-only IPC. The computation flowing through ecobin primals is simultaneously visualizable by petalTongue and provenance-trackable by sweetGrass — rewiring, visualization, and attribution converge.

## YOUR NEXT STEP — LIBRARY TO BINARY

Your primal proof proved science runs through NUCLEUS primals via IPC. Now the scope expands: move your entire domain math off the library and onto IPC.

```
Python baseline (L1) → Rust proof (L2) → guideStone bare (L3) → NUCLEUS validated (L4) → primal proof (L5)
                                                                                             YOU ARE HERE
                                                                                                  ↓
                                                          Tier 2 (IPC routing) → Tier 3 (parity) → Tier 4 (binary-only)
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

## WHERE EVERYONE STANDS (Phase 58 Audit)

| Spring | gS | Tests | Rewiring Tier | Next Step |
|--------|-----|-------|---------------|-----------|
| primalSpring | **8** | 680 | **4** (eukaryotic UniBin) | Exemplar complete — absorb this pattern |
| hotSpring | **5** | 993 | **2** | Create `src/ipc/` dir, expand Tier 3. You pioneered `composition.rs` — now consolidate |
| healthSpring | **5** | 948 | **3** | Expand `primal-proof` coverage to full library surface, flip default to IPC |
| wetSpring | **4+** | 1,594 | **2** | Route handler compute through ecobin. You have 15 IPC handlers — make them IPC-first |
| neuralSpring | **3** | 1,234 | **2** | Graduate `ipc_dispatch.rs` to full `src/ipc/` tree. Mind inference latency |
| ludoSpring | **4** | 820 | **3** | Close remaining `barracuda::` calls, make `ipc` default. Verify 60Hz budget |
| airSpring | **0** | 1,364 | **2** | Unpause delta. Build guideStone against live NUCLEUS. Good IPC foundation already |
| groundSpring | **0** | 1,020 | **1** | Expand `ipc.rs` into `src/ipc/` tree. Optional barraCuda feature is a head start |

### Rewiring Priority

1. **ludoSpring** (3→4) — pure composition, cleanest test case
2. **healthSpring** (3→4) — `primal-proof` feature already gates compilation
3. **hotSpring** (2→3) — biggest barraCuda contributor validating its own absorption
4. **wetSpring** (2→3) — richest IPC handler surface, route compute through ecobin
5. **airSpring** (2→3) — good foundation despite pre-delta
6. **neuralSpring** (2→3) — needs `src/ipc/` dir; latency-sensitive inference
7. **groundSpring** (1→2) — minimal IPC, but optional feature gate is a start

## WHAT'S NEW SINCE PHASE 45

- **BTSP Phase 3 complete**: 13/13 primals FULL AEAD (ChaCha20-Poly1305, May 2). Encrypted channels are the default.
- **projectNUCLEUS absorbed**: Nest Atomic (9 primals), full provenance pipeline (rhizoCrypt DAG → loamSpine commit → sweetGrass braid) validated via RPC on ironGate.
- **primalSpring v0.9.21 Phase 55b**: guideStone Level 4, 187/187 live NUCLEUS ALL PASS, 13/13 BTSP authenticated, 8 cellular graphs BTSP-enforced.
- **Spring NUCLEUS Audit**: 7-dimension audit of all 8 springs. Library-to-binary rewiring inventoried per spring. petalTongue DataBinding channel types mapped. sweetGrass braid patterns defined.
- **Standardization patterns identified**: `primal-proof` feature (healthSpring), `src/ipc/` tree (ludoSpring), `PRIMAL_PROOF_IPC_MAPPING.md` (hotSpring), `composition.rs` dual-lane (hotSpring), deploy graph per pipeline (ludoSpring).
- **petalTongue science map**: Every spring's science output maps to existing DataBinding channels. No new channel types needed.
- **sweetGrass braid patterns**: Per-spring agent/activity/entity definitions. ludoSpring is reference implementation.

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
