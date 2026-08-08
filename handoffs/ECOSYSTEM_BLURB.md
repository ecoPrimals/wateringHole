# ecoPrimals Ecosystem Blurb — Wave 157a GATE REDEPLOY

**Date**: Aug 8, 2026 8:15AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **G68 COMPLETE. ALL PRIMAL TEAMS CLEAR.** 16/16 prod-clean, 16/16 cross-arch. 205→0 production violations. Depot current on golgi (Musl 17/17, Windows 15/15). Gate redeploy to modern next. primalSpring continues biomeOS Neural API evolution.

---

## WHERE WE ARE

Wave 157a G68 convergence is **DONE**. Every primal and cellMembrane has zero production G68 violations. The ecosystem is deploy-ready.

### G68 Audit — 16/16 PROD-CLEAN (sourDough scanner v2)

| Level | Primals |
|-------|---------|
| **G68** (zero violations) | sourDough, nestGate, petalTongue, bingoCube, loamSpine, barraCuda, cellMembrane, +1 |
| **G68-prod** (test-only) | squirrel, bearDog, songBird, rhizoCrypt, skunkBat, sweetGrass, coralReef, biomeOS, toadStool |

### Depot — ALL CURRENT ON GOLGI

- **Musl**: 17/17 at Forgejo HEAD (including toadStool S366)
- **Windows**: 15/15 (squirrel.exe added this wave)

### Health — 13/13 ALIVE on sporeGate

biomeOS 4.57.0 (Stage 2). toadStool S366 deployed with permanent socket fix. Cascade timer: synced=15, zero drift.

---

## WHAT'S NEXT

### 1. Gate Redeploy to Modern
All NUCLEUS gates pull G68-converged binaries from golgi depot. Targeted per-gate:
- **sporeGate**: Already current (13/13 ALIVE)
- **westGate, strandGate, blueGate, southGate, ironGate**: Pull from depot, restart services
- Each gate team owns their redeploy

### 2. primalSpring — Neural API Evolution
primalSpring guides the compositional evolution of biomeOS Neural API. Owns `capability_registry.toml`. Focus:
- **biomeOS** fixes `capability.call` dispatch timeout
- **sweetGrass** shipped `capability.call` handler (gap closed)
- **N2-N5 verification** — route `capability.call` to bearDog, Tower Atomic, Provenance Trio, squirrel
- See `specs/NEURAL_API_ATOMIC_ROUTING_SPEC.md`

### 3. Long-Tail (Active Teams)

| Team | Work | Status |
|------|------|--------|
| **toadStool** | Extending platform abstraction to all deployment types | Active — hw-safe owner of Node Atomic |
| **cellMembrane** | Platform abstraction shipped (15 cfg→3, 1,327 tests). `native_braid.py` → Rust next | Active — last Python in pipeline |

### 4. Live Trust Surfaces — sporePrint + nestgate.io + pseudoSpores

**Goal**: science and data are live, accessible, verifiable pseudoSpores at public URLs.

**sporePrint** (`sporeprint.primals.eco`) — the public face:
- Live, 338 pages, demonstration era. Zola auto-publish working.
- **Needs**: SU(2)→SU(N) relabel for QCD pages, real `.tar.gz` download links, LaTeX→web preprint page.
- **Owner**: sporePrint team.

**nestgate.io** — data identity / trust surface:
- Live, 10/12 dashboard sections on sporeGate. 20 primals discovered, mesh.peers wired.
- **Data Braids section exists in UI but is NOT live** — federation card is hardcoded static text, `/api/content/stats` backend route missing in petalTongue.
- **Missing for westGate braids**: NG-05 (westGate CAS not federated to mesh — needs nestGate TCP + songBird content registration), `/pseudospore/` route (404 today), `content.locate` (spec only).
- **Owner**: sporeGate topology team (Caddy routing, petalTongue dashboard) + westGate (TCP + content registration).

**pseudoSpore — QCD Rung 1** (`hotspring-qcd-sun`):
- pseudoSpore concept is mature in code (pseudospore-core, biomeos-pseudospore, 5-stage provenance chain)
- **QCD bundle NOT yet packaged, signed, or served.** URL resolves but serves homepage, not dedicated page.
- **Critical path**: lithoSpore packages outputs → CAS on ironGate → nestgate.io `/pseudospore/` handler → write `validate.sh` → sporePrint `hotspring-qcd-sun` page → freeze/sign v1.0.0-rung1

### 5. arXiv — Preprint 41/42

Paper is **science-complete**. SU(N) HMC (N=2→8), MILC Δ=3×10⁻⁹, 69 cached configs, NPU ESN demo.

**What blocks reviewer send** (all trust surface, not physics):
1. pseudoSpore at URL cited in paper (not yet served)
2. `validate.sh` (BLAKE3 + DAG + Ed25519 — not written)
3. sporePrint page: `hotspring-qcd-sun` replacing stale SU(2) content
4. Freeze/sign v1.0.0-rung1
5. Send PDF + link to Murillo, Chuna, Bazavov → feedback → arXiv hep-lat

### 6. Springs Activation (When Infrastructure Stable)
- **tideGlass**: Cell boot on westGate → NF drug repurposing pipeline
- **hotSpring**: QCD visualization via petalTongue
- **esotericWebb**: WebGL game surface via petalTongue pipeline

---

## WAVE CADENCE — TARGETED

Ecosystem-wide convergence days are DONE. Waves are now targeted:
- A couple primals push, rebuild, deploy
- Gate teams own their redeploy from golgi depot
- primalSpring evolves Neural API in parallel

---

## BLURB RECIPIENTS

| Recipient | Action |
|-----------|--------|
| **All primal teams** | Clear — absorb posture, no ecosystem-wide pushes |
| **Gate teams** | Redeploy from golgi depot to modern G68-converged binaries |
| **primalSpring** | Neural API evolution owner — capability registry, N2-N5 verification |
| **sporePrint team** | SU(2)→SU(N) relabel, pseudoSpore download pages, LaTeX→web preprint |
| **sporeGate topology team** | Wire 3 websites: nestgate.io data braids backend, `/pseudospore/` route, Caddy routing |
| **toadStool** | Long-tail cross-arch abstraction for all deployment types |
| **cellMembrane** | `native_braid.py` → Rust, NM hook unification |
| **westGate** | nestGate TCP + songBird content registration (NG-05) — unblocks data braids on nestgate.io |

---

*Wave 157a — G68 COMPLETE. 16/16 prod-clean, 16/16 cross-arch. 205→0 production violations. All primal teams clear. Depot current. Gate redeploy next. Live trust surfaces: sporePrint team relabels QCD (SU(2)→SU(N)), sporeGate topology wires nestgate.io data braids + pseudoSpore routes. arXiv 41/42 — science done, trust surface blocks reviewer send. primalSpring evolves Neural API. toadStool cross-arch long-tail. cellMembrane native_braid.py → Rust. Springs activate when ready.*
