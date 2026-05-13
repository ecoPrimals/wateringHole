---

**ecoPrimals Downstream Evolution — May 10, 2026 (Post-Interstadial)**
**From**: primalSpring v0.9.25 (Phase 60+ POST-INTERSTADIAL — Zero Open Upstream Gaps)
**For**: All spring teams

**What happened**: The primordial extinction is **complete** — all 8/8 springs
now have eukaryotic UniBin binaries. All 11 upstream gaps resolved by primal
teams. JH-11 (token federation), GAP-03/06/09/12 all closed. Sovereignty
horizons shipped: bearDog TLS + rate limiting, songbird full NAT chain,
petalTongue web sovereignty, biomeOS `composition.status` + `method.register`.
JH-5 audit forwarding and Tier 4 rewiring are now unblocked.

**Spring UniBin binaries are now tractable for plasmidBin deployment** — each
spring produces a single binary with `certify`/`validate`/`serve`/`status`/`version`
subcommands. See `handoffs/PROJECTNUCLEUS_POST_INTERSTADIAL_FINDINGS_UNIBIN_HANDOFF_MAY10_2026.md`.

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

## WHERE EVERYONE STANDS (Post-Interstadial, May 10)

All 8/8 springs completed primordial extinction — eukaryotic UniBin, zero debt.
Spring UniBin binaries are ready for plasmidBin tracking.

| Spring | gS | Tests | Rewiring Tier | UniBin | Next Step |
|--------|-----|-------|---------------|:------:|-----------|
| primalSpring | **8** | 680 | **4** (exemplar) | Yes | Reference complete |
| hotSpring | **6** | 1,036 | **4** | Yes | Tier 4 IPC-first complete; 9/12 scenarios; `--format json`; GAP-HS-092 `call_by_capability` proliferation |
| healthSpring | **5** | 999+ | **3** | Yes | Tier 4: flip `primal-proof` to IPC default |
| wetSpring | **4** | 1,209 | **2** | Yes | Tier 3: route handler compute through ecobin |
| neuralSpring | **3** | 1,432 | **2** | Yes | Tier 3: `src/ipc/` tree, latency-aware |
| ludoSpring | **4** | 665+ | **3** | Yes | Tier 4: close remaining `barracuda::` calls |
| airSpring | **2** | 1,364 | **2** | Yes | Tier 3: `aws-lc-sys` ban, guideStone L4 |
| groundSpring | **4** | 965+ | **1** | Yes | Tier 2: expand `ipc.rs` into `src/ipc/` tree |

### Rewiring Priority

1. **ludoSpring** (3→4) — pure composition, cleanest test case
2. **healthSpring** (3→4) — `primal-proof` feature already gates compilation
3. **hotSpring** (4 — done) — Tier 4 IPC-first, capability discovery complete, LTEE B2 shipped
4. **wetSpring** (2→3) — richest IPC handler surface, route compute through ecobin
5. **airSpring** (2→3) — good foundation despite pre-delta
6. **neuralSpring** (2→3) — needs `src/ipc/` dir; latency-sensitive inference
7. **groundSpring** (1→2) — minimal IPC, but optional feature gate is a start

## WHAT'S NEW (Post-Interstadial, May 10)

- **Primordial extinction complete**: 8/8 springs have eukaryotic UniBin binaries. Zero TODO/FIXME/HACK/clippy across all springs.
- **Zero open upstream gaps**: All 11 gaps resolved (JH-11, GAP-03/06/09/12, U1-U3, DF-2/3, U5). See `handoffs/PRIMALSPRING_POST_INTERSTADIAL_DOWNSTREAM_HANDOFF_MAY10_2026.md`.
- **Spring UniBin → plasmidBin**: Single binary per spring makes tracked deployment tractable for the first time. See `handoffs/PROJECTNUCLEUS_POST_INTERSTADIAL_FINDINGS_UNIBIN_HANDOFF_MAY10_2026.md`.
- **Sovereignty horizons shipped upstream**: bearDog TLS + rate limiting (H2-10/11), songbird full NAT chain (H2-13-16), petalTongue web sovereignty (PT-1-PT-5), biomeOS `composition.status` + `method.register`.
- **JH-5 audit forwarding unblocked**: skunkBat Phase 2 complete (7 event kinds). Phase 3 (cross-primal forwarding) ready.
- **Tier 4 rewiring unblocked**: JH-11 token federation live. `CompositionContext` is the canonical API.
- **`method.register` live**: biomeOS v3.51 — springs can register methods dynamically (no manual config).
- **projectNUCLEUS static observer**: Pre-rendered HTML, centralized dark theme, Rust-validated (darkforest v0.2.1).
- **403 canonical methods**: primalSpring registry (zero drift). CI cross-sync available for all springs.

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
| **UniBin plasmidBin readiness** | `infra/wateringHole/handoffs/PROJECTNUCLEUS_POST_INTERSTADIAL_FINDINGS_UNIBIN_HANDOFF_MAY10_2026.md` |
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
