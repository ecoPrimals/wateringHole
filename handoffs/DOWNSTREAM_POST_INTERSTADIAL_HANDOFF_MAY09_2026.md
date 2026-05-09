# Downstream Post-Interstadial Handoff

**Date**: May 9, 2026
**From**: primalSpring (ecosystem coordination)
**For**: projectNUCLEUS, esotericWebb, sporeGarden products, all downstream consumers
**Phase**: Post-interstadial — primordial extinction wave COMPLETE

---

## 1. What Happened

The entire river delta (8 springs) completed the eukaryotic evolution in a single
interstadial wave. Every spring now has:

- **UniBin** — single binary with `certify`/`validate`/`serve`/`status`/`version`
- **Certification organelle** — guidestone layers absorbed as library modules
- **Scenario registry** — `validation/scenarios/` with typed `ScenarioMeta`
- **Fossil record** — `fossilRecord/` with dated provenance
- **Zero debt** — zero TODO/FIXME/HACK, zero clippy warnings, zero bare `#[allow]`

| Spring | Version | Tests | gS Level | UniBin |
|--------|---------|------:|:--------:|:------:|
| primalSpring | v0.9.25 | 680 | L8 | full |
| hotSpring | latest | 1,002 | L5 | full |
| healthSpring | V61 | 999+ | L5 | full |
| wetSpring | V155 | 1,209 | L4 | full |
| neuralSpring | S195 | 1,432 | L3 | full |
| groundSpring | V127 | 965+ | L4 | full |
| airSpring | v0.10.0 | 1,364 | L2 | full |
| ludoSpring | V58 | 665+ | L4 | full |

**Total**: 9,317+ tests across 8 springs. 13/13 upstream primals at zero debt.

---

## 2. What This Means for Downstream Products

### For projectNUCLEUS

**Composition is now reliable.** Every spring binary you compose via deploy graphs
has been through the same quality gate: certification, scenario validation, zero
warnings, zero debt. The UniBin surface is consistent:

```bash
# Any spring binary now supports:
{spring} certify              # composition certification
{spring} validate             # validation scenarios
{spring} validate --tier rust # CI-safe, no primals needed
{spring} serve                # IPC server (where applicable)
{spring} status               # health summary
{spring} version              # version info
```

**Sovereign hosting validated.** primals.eco now dual-hosted via gate (Cloudflare
tunnel) with GitHub Pages fallback. DNS-over-TLS closes the ISP metadata leak.
One-command DNS switching (`deploy/sporeprint_dns.sh sovereign|external`).

**Open upstream gaps for your roadmap:**

| ID | Owner | What | Impact on NUCLEUS |
|----|-------|------|-------------------|
| JH-11 | bearDog/biomeOS | Cross-primal token federation | Blocks authenticated composition (Tier 4) |
| GAP-06 | rhizoCrypt | No UDS transport | Blocks provenance trio in 4 ludoSpring experiments |
| GAP-03 | biomeOS | Cell graph live deploy not tested | Blocks live cell deployment |
| GAP-09 | biomeOS | Neural API registration endpoint | Blocks neural routing for game methods |
| DF-2 | toadStool | `TOADSTOOL_AUTH_MODE` env var mapping | Minor |
| U1 | primalSpring | `CHECKSUMS` stale | Minor doc debt |

**Sovereignty progression** (from your own handoff):

```
Current: Gate → Cloudflare DoT → Cloudflare tunnel → gate
Next:    Gate → local unbound → root servers → tunnel → gate
Phase 3: Gate → Songbird mesh → peer resolution → direct P2P
```

### For esotericWebb / sporeGarden Products

**ludoSpring is now eukaryotic.** This is the biggest change for game products:

- 100 experiment crates → fossilized to `fossilRecord/`
- 5 representative scenarios absorbed into `validation/scenarios/`
- `ipc` is now the **default feature** — IPC-first for NUCLEUS deployment
- barraCuda GAP-13 resolved — `default-features = false` works cleanly
- `ludospring_cell.toml` (12 nodes) ready for biomeOS deployment

**Composition pattern for game products:**

```
biomeOS deploys ludospring_cell.toml
  → 12 NUCLEUS nodes (barraCuda, petalTongue, Squirrel, provenance trio, Tower)
  → 30 capabilities across 11 composed primals
  → ludospring binary = validation target only (not deployed)
  → lifecycle.composition handler for runtime proto-nucleate validation
```

**IPC methods available for game composition** (15 capabilities):
`game.evaluate_flow`, `game.fitts_cost`, `game.engagement`, `game.generate_noise`,
`game.wfc_step`, `game.analyze_ui`, `game.accessibility`, `game.difficulty_adjustment`,
`game.begin_session`, `game.record_action`, `game.complete_session`,
`game.mint_certificate`, `game.query_vertices`, `game.npc_dialogue`, `game.narrate_action`

### For Any New Product

**The composition pattern is now proven across 8 domains:**

1. Define a deploy graph (TOML) describing what capabilities you need
2. biomeOS deploys the graph via Neural API
3. Your product calls capabilities via IPC — never imports primal code
4. Validation runs at two tiers: structural (CI-safe) + behavioral (live)
5. Certification proves composition correctness (L0-L8)

**Key APIs:**

| Pattern | API | What It Does |
|---------|-----|-------------|
| Discovery | `CompositionContext::discover()` | 5-tier escalation: Songbird → Neural API → UDS → registry → TCP |
| IPC call | `ctx.call(capability, method, params)` | Route through discovered primal |
| Health | `ctx.health_check()` | Composition-wide health |
| Auth call | `ctx.call_authenticated(cap, method, params, token)` | Bearer token threaded through graphs |
| Validation | `primalspring validate --tier rust` | CI-safe, no live primals needed |
| Certification | `primalspring certify --bare` | Structural certification, no primals needed |

---

## 3. Patterns Learned During the Interstadial

### The Exemplar Model Works

primalSpring evolved first, became the seed crystal. All 7 delta springs
crystallized around the exemplar's patterns without cloning them — each adapted
to its niche. The handoff document was the inheritance mechanism.

### UniBin Consolidation Is Net Positive

ludoSpring went from 103 workspace members to 3. healthSpring consolidated 95
experiment crates. The result: faster builds, simpler CI, clearer architecture.
Fossil records preserve the old code for anyone who needs it.

### Two-Tier Validation Catches Real Issues

Tier 1 (Rust, no IPC) catches structural problems in CI. Tier 2 (live primals)
catches behavioral issues that only surface with real IPC. Running Tier 1 first
saves time on the expensive Tier 2. This pattern should be adopted by all products.

### The Certification Organelle Is the Quality Gate

Absorbing guidestone as a library module rather than a separate binary means
certification runs as part of the normal build/test flow. `primalspring certify --bare`
in CI catches regressions without needing a live NUCLEUS composition.

---

## 4. What You Should Do

### Immediate (this week)

1. **Pull all springs** — every spring has new handoffs and evolution commits
2. **Read the UniBin handoff** — `primalSpring/wateringHole/PRIMALSPRING_V0925_UNIBIN_EUKARYOTIC_HANDOFF_MAY09_2026.md`
3. **Test composition** — run `{spring} certify --bare` and `{spring} validate --tier rust` for any spring you consume

### Next Pass

4. **Update deploy graphs** — any graph referencing old spring binaries should
   reference the new UniBin names
5. **Wire two-tier validation** into your CI: `--tier rust` for fast checks,
   full validation for integration
6. **Prepare for JH-11** — when token federation ships, Tier 4 (authenticated
   IPC-only composition) becomes possible. Design your auth flow now.

### Long Term (next stadial gate)

7. **Monitor for barraCuda IPC-first migration** — springs will make `barracuda`
   optional with IPC-first defaults. Products should not import spring library
   code directly.
8. **Monitor for Songbird NAT traversal** — replaces Cloudflare tunnel for
   sovereign P2P hosting.

---

## 5. References

| What | Where |
|------|-------|
| primalSpring evolution handoff | `primalSpring/wateringHole/PRIMALSPRING_V0925_EVOLUTION_HANDOFF_MAY09_2026.md` |
| UniBin handoff | `primalSpring/wateringHole/PRIMALSPRING_V0925_UNIBIN_EUKARYOTIC_HANDOFF_MAY09_2026.md` |
| ludoSpring evolution handoff | `infra/wateringHole/handoffs/LUDOSPRING_V58_UPSTREAM_EVOLUTION_HANDOFF_MAY09_2026.md` |
| NUCLEUS sovereign hosting | `infra/wateringHole/handoffs/PROJECTNUCLEUS_SOVEREIGN_HOSTING_DNS_HANDOFF_MAY09_2026.md` |
| Gap registry | `primalSpring/docs/PRIMAL_GAPS.md` |
| Parity scorecard | `primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` |
| Interstadial wave handoff | `infra/wateringHole/INTERSTADIAL_WAVE_EVOLUTION_HANDOFF_MAY09_2026.md` |
| Gen4 stadial pattern | `infra/whitePaper/gen4/architecture/STADIAL_INTERSTADIAL_PATTERN.md` |
