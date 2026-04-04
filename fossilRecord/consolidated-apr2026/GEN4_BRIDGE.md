# gen4 Bridge — How Primals Become Products

**Date**: March 26, 2026
**Status**: Active — first gen4 consumer (Esoteric Webb V4) operational
**Audience**: All primal teams, spring teams, and gen4 product developers

---

## What Changed

The ecoPrimals ecosystem has crossed the gen3→gen4 boundary. Primals are no
longer only subjects of scientific validation — they are now **invisible
infrastructure inside products people use.**

The first gen4 product, **Esoteric Webb** (sporeGarden/esotericWebb), is a CRPG
engine that composes 8 primal domains into a playable game. It consumes primals
via JSON-RPC IPC from `plasmidBin/` — zero spring imports, zero compile-time
coupling. When a primal is absent, Webb degrades gracefully to standalone mode.

This document explains what gen4 means for every team in the ecosystem.

---

## The Flow

```
Primal team builds binary
  → harvest.sh to github.com/ecoPrimals/plasmidBin (metadata + GitHub Release)
  → Spring validates via constrained evolution (gen3 science)
  → gen4 product runs fetch.sh → discovers binary → composes via IPC
  → Product discovers gaps → files EVOLUTION_GAPS.md
  → Gap pressure feeds back to primal team → primal evolves
  → Cycle repeats
```

---

## Three Organizations

| Org | Role | Gen | Examples |
|-----|------|-----|----------|
| **ecoPrimals** | Primal binaries + infrastructure | gen2 | BearDog, Songbird, biomeOS, plasmidBin |
| **syntheticChemistry** | Springs (science validation) | gen3 | hotSpring, wetSpring, ludoSpring, primalSpring |
| **sporeGarden** | Products (creative surface) | gen4 | esotericWebb, RPGPT Engine (planned) |

---

## What Primal Teams Need to Know

### Your binary is your product now

In gen3, springs consume your source. In gen4, **products consume your binary**.
The binary in `plasmidBin/` is the only interface gen4 products see. Your source
tree, your spring's experiments, your internal crate structure — all invisible.

### plasmidBin is the deployment surface

[github.com/ecoPrimals/plasmidBin](https://github.com/ecoPrimals/plasmidBin)
is the standalone repo. When you release a new version:

1. Build your binary (release mode)
2. Copy to your directory in a local plasmidBin clone
3. Run `./harvest.sh` — updates checksums, creates GitHub Release
4. `git push` — metadata goes to git, binaries go to Release assets
5. Consumers run `./fetch.sh` to get your latest

### Current plasmidBin inventory (v2026.03.25)

| Primal | Version | Domain | Status |
|--------|---------|--------|--------|
| beardog | 0.9.0 | crypto | Available |
| songbird | 0.2.1 | discovery | Available |
| squirrel | 0.1.0 | ai | Available (musl) |
| toadstool | 0.1.0 | compute | Available |
| nestgate | 2.1.0 | storage | Available |
| rhizocrypt | 0.14.0-dev | dag | Available |
| loamspine | 0.9.13 | lineage | Available |
| sweetgrass | 0.7.27 | provenance | Available |
| biomeos | 0.1.0 | orchestration | Available |
| petaltongue | 1.6.6 | visualization | Available |
| coralreef | 0.1.0 | shaders | Available |
| **ludospring** | — | game | **NOT YET DEPLOYED** |

**ludoSpring** is the highest-priority missing binary. It is esotericWebb's
primary game science dependency — the orchestrator for all `game.*` RPCs.

---

## What Spring Teams Need to Know

Springs validate primals via constrained evolution. This role is unchanged.
What's new: **gen4 products now create gap pressure that drives primal evolution.**

Esoteric Webb's `EVOLUTION_GAPS.md` currently tracks 7 open gaps:

| Gap | Primal | What's Needed |
|-----|--------|---------------|
| GAP-002 | petalTongue | `DialogueTreeScene` payload for CRPG UI |
| GAP-003 | Squirrel | Hard NPC personality constraint enforcement |
| GAP-004 | Provenance trio | Live E2E test against real binaries |
| GAP-006 | Songbird | Capability-filtered `discovery.query` |
| GAP-007 | Squirrel + Webb | Offline voice interjection preview |
| GAP-009 | ludoSpring + Webb | RulesetCert YAML authoring + validation |
| GAP-010 | ecosystem | plasmidBin population automation |

When a gap is filed, the spring that produces the affected primal should review
it and consider whether to absorb the capability. The spring validates the
science; the primal ships the binary; the product exercises it.

---

## What gen4 Product Teams Need to Know

### Consume binaries, not source

Your product runs `fetch.sh` to populate local plasmidBin, then discovers
primals via filesystem probe or Songbird `discovery.query`. You never import
a spring crate or a primal crate. All communication is JSON-RPC IPC.

### Graceful degradation is mandatory

Every primal call must degrade gracefully when the primal is absent. Webb's
`PrimalBridge` uses retry + circuit breaker + sensible defaults. When primals
aren't available, the product works in standalone mode — reduced capability,
never a crash.

### Gap pressure is your contribution

When your product discovers that a primal can't do what you need, file it in
your `EVOLUTION_GAPS.md` and craft a wateringHole handoff for the spring team.
This gap pressure is the primary feedback mechanism from gen4 to gen3.

### Deploy graphs define your niche

Your BYOB niche is defined by TOML deploy graphs that declare what capabilities
you need. biomeOS resolves providers at runtime. See
`NEURAL_API_GRAPH_DEPLOYMENT_STANDARD.md` for the format.

---

## The Generational Boundary

| Property | gen3 (springs) | gen4 (products) |
|----------|---------------|-----------------|
| Primary output | Papers, checks, catalogs | Tools, products, niches |
| Primary audience | Faculty, committees | Creatives, players, builders |
| Primal relationship | Subject of study | Invisible infrastructure |
| Coupling | Source-level (tighter, expected) | Binary-only (IPC, zero imports) |
| Deployment | cargo workspace, experiments | plasmidBin binaries, fetch.sh |
| Success metric | "Does it compute correctly?" | "Does someone ship with it?" |

gen4 does not replace gen3. Springs continue to evolve. The thesis will be
submitted. baseCamp papers will be published. gen4 is a **new layer** — the
fruit on the tree that gen3 grew.

---

## Spring Bridge Roles

Two springs have specific gen4 bridging responsibilities. They are gen3 entities
that validate the gen4 boundary — proving that primal composition works before
products ship it.

### primalSpring — Composition Validation

primalSpring validates that primals compose correctly. In gen4, this role
expands from "do primals talk to each other?" to "can a product build a
real pipeline from these primals?"

**What Webb already expects from primalSpring:**

Esoteric Webb's deploy graphs (`graphs/webb_*.toml`) include `validate_webb_*`
nodes that reference `primalspring_primal` with `spawn = false`:

```toml
[[graph.node]]
name = "validate_webb_full"
binary = "primalspring_primal"
order = 99
spawn = false
depends_on = ["beardog", "songbird", "nestgate", "toadstool", "squirrel",
              "petaltongue", "rhizocrypt", "loamspine", "sweetgrass",
              "esotericwebb"]
capabilities = ["composition.webb_full_health"]
```

Six composition health capabilities Webb expects primalSpring to expose:

| Capability | Graph | What It Validates |
|------------|-------|-------------------|
| `composition.webb_tower_health` | `webb_tower.toml` | BearDog + Songbird IPC baseline |
| `composition.webb_node_health` | `webb_node.toml` | Tower + ToadStool compute |
| `composition.webb_nest_health` | `webb_nest.toml` | Tower + NestGate storage |
| `composition.webb_ai_viz_health` | `webb_ai_viz.toml` | Tower + Squirrel + PetalTongue overlay |
| `composition.webb_provenance_health` | `webb_provenance.toml` | Nest + rhizoCrypt + loamSpine + sweetGrass |
| `composition.webb_full_health` | `webb_full.toml` | All domains composed |

These are **contracts**: Webb declares them, primalSpring must implement them.
None are wired yet — this is the highest-priority bridge work.

**What primalSpring brings to gen4:**

- Deploy graph structural + topological validation (22 graphs, Kahn's algorithm)
- Live atomic composition testing (Tower/Node/Nest/NUCLEUS, 87/87 gates)
- Capability drift detection (registry ↔ bridge ↔ graph consistency)
- IPC resilience validation (circuit breaker, retry, degradation)
- Transport priority testing (TCP-first, UDS fallback — matching Webb's `PrimalBridge`)
- Cross-domain pipeline ordering (narrate → dialogue → flow → render → DAG)

### ludoSpring — Game Science Validation

ludoSpring validates game mechanics, flow theory, dialogue systems, and ruleset
certification. In gen4, this role expands from "does game science model correctly?"
to "does this game science hold up under live composition?"

**What Webb expects from ludoSpring:**

- `game.*` RPC namespace: `game.narrate_action`, `game.npc_dialogue`,
  `game.evaluate_flow`, `game.voice.notes`, `game.ruleset.validate`
- `FlowResult`, `DialogueResponse` with degradation markers
- `RulesetCert` YAML authoring and per-plane validation (GAP-009)
- Deployed binary in plasmidBin (**currently missing — critical**)

**What ludoSpring brings to gen4:**

- Formal game flow models (Csikszentmihalyi / Schell frameworks)
- Dialogue tree science (branching narrative, NPC personality constraints)
- Ruleset certification (game balance proofs)
- VoiceNote integration and interjection systems
- Real-time flow evaluation during session composition

### The sporeGarden Pattern

esotericWebb is the first gen4 product, but it establishes a **reusable pattern**
for any spring's validated science becoming a deployable product:

```
Spring validates science (gen3)
  → Primals ship validated binaries to plasmidBin
  → gen4 product composes binaries via IPC
  → Product finds gaps → files EVOLUTION_GAPS.md
  → Spring absorbs gaps → evolves primal → ships new binary
  → Product composes improved binary → cycle repeats
```

This pattern applies beyond gaming:

| Domain | Spring | gen4 Product | Primals Composed |
|--------|--------|-------------|------------------|
| Gaming | ludoSpring + primalSpring | esotericWebb (CRPG engine) | Squirrel, petalTongue, toadStool, provenance trio |
| Genomics | wetSpring + neuralSpring | **helixVision** (sovereign genomics) | toadStool, coralReef, barraCuda, NestGate, provenance trio, Squirrel, petalTongue |
| GPU Compute | hotSpring | Sovereign shader runtime (planned) | coralReef, toadStool, barraCuda |
| Security | healthSpring | Audit/compliance surface (planned) | BearDog, Songbird, skunkBat |

Each product is a **niche** in the sporeGarden organization. Each niche defines
deploy graphs, capability requirements, and graceful degradation. Each niche
feeds gap pressure back to the springs that validate its primals.

---

## Action Items

| Priority | Item | Owner |
|----------|------|-------|
| **Critical** | Deploy ludoSpring binary to plasmidBin | ludoSpring team |
| **Critical** | Implement `composition.webb_*_health` capabilities (6 endpoints) | primalSpring team |
| **High** | Review esotericWebb EVOLUTION_GAPS.md | All affected primal teams |
| **High** | Springs add integration tests using plasmidBin binaries | All spring teams |
| **High** | Validate capability string consistency (registry ↔ bridge ↔ graph ↔ niche YAML) | primalSpring team |
| **High** | Add Webb session pipeline ordering tests (narrate→dialogue→flow→render→DAG) | primalSpring team |
| **Medium** | petalTongue: DialogueTreeScene support (GAP-002) | petalTongue team |
| **Medium** | Squirrel: NPC constraint enforcement (GAP-003) | Squirrel team |
| **Medium** | Harmonize metadata.toml format across plasmidBin | plasmidBin maintainer |
| **Medium** | TCP-first transport priority validation (matching Webb PrimalBridge behavior) | primalSpring team |
| **Low** | Songbird: capability-filtered discovery.query (GAP-006) | Songbird team |

---

*gen1 built the hardware. gen2 defined the protocol. gen3 proved the science.
gen4 is where the primals disappear into the product — and the product is what
someone actually uses.*
