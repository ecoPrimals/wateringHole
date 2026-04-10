# primalSpring v0.9.9 — NUCLEUS Alignment + Spring Evolution Handoff

**Date**: April 10, 2026
**From**: primalSpring Phases 31–33
**For**: All primal teams, spring teams, garden teams
**License**: AGPL-3.0-or-later

---

## What Changed

### Phase 31: Atomic Cleanup & Bonding Alignment (v0.9.7)

- Fixed 3 graphs with duplicate `[graph.bonding_policy]` tables (invalid TOML)
- Added coralReef to 5 graphs claiming `node_atomic` without it
- Upgraded `provenance_trio` → `nest_atomic` in 6 graphs where NestGate present
- Fixed 7 graph descriptions overstating "NUCLEUS"
- Aligned `fragments` metadata across ~20 graphs
- Added `[graph.bonding_policy]` to 9 cross-atomic deploy graphs

### Phase 32: NUCLEUS Validation Alignment (v0.9.8)

- Fixed `nucleus_atomics_validate.toml` — old graph refs, old atomic model
- Aligned `deployment_matrix.toml` v3.0.0 — all 21 topologies have `atomic` metadata
- Updated `PRIMALSPRING_COMPOSITION_GUIDANCE.md` — Node/Nest/NUCLEUS definitions
- Added spring evolution feedback guidance to ecosystem leverage guide

### Phase 33: Full Spring Alignment (v0.9.9)

- Created proto-nucleate graphs for **airSpring**, **groundSpring**, **wetSpring**
- All 7 science springs + esotericWebb now have downstream proto-nucleates
- Created `NUCLEUS_SPRING_ALIGNMENT.md` — comprehensive alignment matrix
- 96 deploy graphs + 6 fragments (was 93)

---

## The NUCLEUS Atomic Model (canonical)

| Atomic | Particle | Primals |
|--------|----------|---------|
| Tower | Electron | BearDog + Songbird |
| Node | Proton | Tower + ToadStool + barraCuda + coralReef |
| Nest | Neutron | Tower + NestGate + rhizoCrypt + loamSpine + sweetGrass |
| NUCLEUS | Atom | Tower + Node + Nest (9 unique primals) |
| Meta-tier | — | biomeOS + Squirrel + petalTongue |

---

## What This Means for Each Team

### Primal Teams

Your primal appears in one or more atomics. The springs listed as your
"primary drivers" in `NUCLEUS_SPRING_ALIGNMENT.md` are the teams that
will stress-test your capabilities most aggressively. Expect gaps and
pattern proposals from those springs.

**Action items**:
- Review the `[graph.bonding_policy]` sections in deploy graphs that
  reference your primal — these document how your primal binds within
  cross-atomic compositions
- The `fragments` metadata in deploy graphs now accurately reflects
  which primals are present — use this as a compliance checklist

### Spring Teams

Your proto-nucleate graph is now in `primalSpring/graphs/downstream/`.
This is your target composition — the primals you should be wiring IPC
to, and the capabilities you should be calling.

**Action items**:
1. Read your proto-nucleate and understand the composition
2. Wire your domain logic to call primals by capability
3. Add Squirrel to your composition when you want AI (neuralSpring
   provides inference as it evolves — no spring code changes needed)
4. Document gaps → primalSpring `docs/PRIMAL_GAPS.md`
5. Hand back patterns → `infra/wateringHole/handoffs/`

### neuralSpring (special role)

As you evolve WGSL shader ML inference, every spring with Squirrel in
its composition gets AI immediately. You are the AI provider for the
ecosystem. Your inference evolution path:

```
Phase 1 (now):   Squirrel → Ollama (HTTP, external vendor)
Phase 2 (next):  Squirrel → neuralSpring → WGSL shader composition
Phase 3 (later): Squirrel → neuralSpring → domain-specific models
```

### Garden Teams (esotericWebb)

Your proto-nucleate defines a pure composition — no downstream binary.
biomeOS IS your execution engine. The graph IS the product. All prior
"binary" work is validation structure.

---

## Key Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Atomic model | `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` | Spring × atomic alignment, cross-pollination |
| Composition guidance | `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` | How to compose, graph patterns |
| Ecosystem leverage | `primalSpring/wateringHole/PRIMALSPRING_ECOSYSTEM_LEVERAGE_GUIDE.md` | Library patterns, evolution cycle |
| Proto-nucleates | `primalSpring/graphs/downstream/*.toml` | Per-spring target compositions |
| Deployment matrix | `primalSpring/config/deployment_matrix.toml` | 43 validation cells |
| Primal gaps | `primalSpring/docs/PRIMAL_GAPS.md` | Known gaps per primal |
| Fragments | `primalSpring/graphs/fragments/` | Canonical atomic definitions |
| Profiles | `primalSpring/graphs/profiles/` | Deployable atomic slices |

---

## Cross-Pollination Summary

Each spring solving its domain makes every other spring more capable:

- **hotSpring** → df64 GPU precision benefits neuralSpring ML accuracy
- **neuralSpring** → AI inference benefits every spring with Squirrel
- **healthSpring** → ionic bonds benefit any spring with trust boundaries
- **wetSpring** → time-series storage benefits sensor-heavy springs
- **ludoSpring** → 60Hz composition budget tests graph execution limits
- **airSpring** → PDE/NPU patterns benefit edge deployments
- **groundSpring** → statistical shaders benefit data quality across ecosystem

---

**License**: AGPL-3.0-or-later
