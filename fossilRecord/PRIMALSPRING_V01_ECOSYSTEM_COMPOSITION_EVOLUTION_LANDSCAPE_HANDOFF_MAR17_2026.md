# PRIMALSPRING V0.1 — Ecosystem Composition Evolution Landscape

**Date:** 2026-03-17
**Author:** ludoSpring audit session (cross-spring survey)
**For:** primalSpring team — nascent coordination spring
**Source:** Full ecosystem survey of 13 primals + 8 springs

---

## Purpose

primalSpring is the spring whose domain IS coordination. This document gives
the primalSpring team the full landscape: every primal, every spring, what
composition patterns exist, what's missing, and where the absorption evolution
needs validation. primalSpring validates that primals compose correctly — it
does not own domain science.

---

## The Evolution Arc (Every Spring)

```
Spring (fat, exploratory)
  → Primals absorb the primitives (Write → Absorb → Lean)
  → Spring thins to orchestration
  → Spring becomes a BYOB niche deploy graph
  → Primals carry production code; spring is the deployment specification
```

primalSpring's job: validate every step of this arc across the ecosystem.

---

## Primal Registry — On-Disk Status

### Foundation Primals (phase1/)

| Primal | Version | Domain | Tests | Status |
|--------|---------|--------|-------|--------|
| **BearDog** | 0.9.0 | Cryptography (Ed25519, X25519, BLAKE3, ChaCha20, genetic lineage, Dark Forest) | Many crates | Production A+ |
| **Songbird** | 0.2.1 | Network (TLS 1.3, BirdSong, mDNS, STUN, relay, federation, Tor) | 25+ crates | Production S+ |
| **ToadStool** | 0.1.0 (S155b) | Hardware (GPU/NPU/CPU discovery, compute dispatch, shader proxy, Ollama lifecycle) | 21,156 | Production A++ |
| **NestGate** | 4.1.0-dev | Storage (content-addressed, BLAKE3, discovery, metadata) | 12,155 | Production A++ |
| **Squirrel** | 0.1.0 | AI (MCP coordination, inference routing, context management) | 4,862 | Production A++ |

### Sovereign Compute Stack

| Primal | Version | Domain | Tests | Status |
|--------|---------|--------|-------|--------|
| **barraCuda** | 0.3.5 | Pure math (806 WGSL shaders, linalg, stats, spectral, nn, ops, genomics, PDE) | 3,466+ | Production A+ |
| **coralReef** | 0.1.0 (Phase 10 Iter 52) | Shader compilation (WGSL → NVIDIA SM70–SM89, AMD RDNA2) | 2,185 | Production A+ |

### Orchestration + Provenance (phase2/)

| Primal | Version | Domain | Tests | Coverage | Status |
|--------|---------|--------|-------|----------|--------|
| **biomeOS** | v2.48 | Ecosystem orchestrator (Neural API, atomics, deploy graphs, Dark Forest) | 5,162+ | 78% line | Production A++ |
| **rhizoCrypt** | 0.13.0-dev | Ephemeral memory (content-addressed DAG, sessions, Merkle trees) | 1,327 | 92% line | Production |
| **sweetGrass** | v0.7.21 | Semantic provenance (W3C PROV-O braids, attribution engine) | 1,077 | — | Production |
| **loamSpine** | 0.9.5 | Immutable ledger (Loam Certificates, spine structure, proofs) | 1,226 | 90%+ func | Production |

### Not Cloned (Registry Only)

| Primal | Domain | Notes |
|--------|--------|-------|
| **petalTongue** | Universal UI (egui, ratatui, web, audio sonification, Tufte constraints) | Docs at `wateringHole/petaltongue/`. v1.6.6 in registry. Needs cloning. |
| **skunkBat** | Defensive security (threat detection, graduated response) | No Cargo.toml on disk. |

---

## Spring Absorption Status — What Moves Where

### airSpring (Ecology/Agriculture) — LEAN ACHIEVED

| What | Absorbs Into | Status |
|------|-------------|--------|
| 6 local GPU ops (ops 14–19) | barraCuda | **Done** — fully absorbed upstream |
| `local_dispatch` | retired | **Done** |
| `eco::diversity` | barraCuda stats | Candidate |
| `eco::drought_index` | barraCuda special | Candidate |
| bingoCube/nautilus ESN | stays local | Domain-specific |

**Composition needs:** Penny Irrigation deploy graph (vision → sensor → compute → irrigate), provenance trio, NestGate routing. petalTongue viz not wired.

---

### groundSpring (Measurement/Uncertainty) — ACTIVE ABSORPTION

| What | Absorbs Into | Status |
|------|-------------|--------|
| 102 barraCuda delegations (61 CPU, 41 GPU) | barraCuda | **Leaning** |
| `prng` (Xorshift64) | barraCuda rng (xoshiro) | Candidate |
| `linalg` (tridiag eigensolver) | barraCuda spectral | Candidate |
| `kinetics` (Hill, Monod) | barraCuda stats | Candidate |
| `bootstrap` | barraCuda stats | Candidate |
| rarefaction, rare_biosphere, quasispecies | barraCuda GPU | GPU-ready, not dispatched |
| band_structure, freeze_out, spectral_recon | barraCuda GPU | GPU-ready, not dispatched |
| 2 `anderson_lyapunov*.wgsl` | barraCuda shaders | In metalForge, candidate |

**Composition needs:** ET₀→Anderson propagation, no-till sampling, NUCLEUS stack, NestGate (NCBI, NOAA, IRIS).

---

### healthSpring (Health/PK-PD) — ACTIVE ABSORPTION

| What | Absorbs Into | Status |
|------|-------------|--------|
| 6 WGSL shaders (Hill, PopPK, Diversity, MM batch, SCFA batch, Beat classify) | toadStool → barraCuda | **Pending** |
| `mm_auc`, `scr_rate`, `antibiotic_perturbation` | barraCuda health | **Done** |
| `cholesky_solve()` 2×2/3×3 | stays local | Intentional (NLME-specific) |

**Composition needs:** Patient assessment (4 parallel tracks → cross-track → composite → visualize), consent-gated medical (BearDog ZKP), NestGate patient records. petalTongue live dashboards.

---

### hotSpring (Nuclear Physics) — ACTIVE ABSORPTION

| What | Absorbs Into | Status |
|------|-------------|--------|
| Staggered Dirac shader | barraCuda | **Pending** |
| CG solver shaders | barraCuda | **Pending** |
| Pseudofermion HMC | barraCuda | **Pending** |
| ESN reservoir + readout | barraCuda nautilus | **Leaning** |
| HFB shader suite | barraCuda | **Leaning** |
| Screened Coulomb (Sturm) | barraCuda spectral | Candidate |
| 85 WGSL shaders total | barraCuda shaders | Mix of absorbed/pending |

**Composition needs:** GPU→NPU physics pipeline (MD→ESN→NPU), lattice NPU phase classification, heterogeneous monitor (3090+Titan V+CPU+NPU), coralReef DRM dispatch.

---

### ludoSpring (Game Science) — ACTIVE ABSORPTION

| What | Absorbs Into | Status |
|------|-------------|--------|
| Perlin noise | barraCuda procedural | **Absorbed** (GPU path exists) |
| 9 exp030 parity shaders (sigmoid, relu, softmax, dot, reduce, perlin, abs, scale, lcg) | barraCuda | **Absorbed** — local copies are fossils |
| Raycaster DDA | barraCuda ops | **P1 candidate** |
| Engagement/flow/DDA batch eval | barraCuda | **P1 candidate** |
| WFC, BSP, L-system | barraCuda | **Tier B** (barrier sync / recursion) |
| fog_of_war, tile_lighting, pathfind_wavefront WGSL | barraCuda shaders | **P2 candidate** |
| Narration cues, audio cues | petalTongue | Protocol defined, no audio output |
| Entity/world/session | biomeOS niche graph | Future — orchestration layer |

**Composition needs:** Windowed rendering (ludoSpring logic + petalTongue surface + toadStool dispatch + coralReef compile), audio pipeline (cues → petalTongue PCM), RPGPT (Squirrel narration + NestGate cert storage).

---

### neuralSpring (Learning/Surrogates) — HEAVILY LEANING

| What | Absorbs Into | Status |
|------|-------------|--------|
| 28 barraCuda modules, 155 files | barraCuda | **Leaning** |
| 47 GPU ops via local `gpu_dispatch/` | barraCuda → toadStool | **Leaning** |
| coralForge (AlphaFold2/3 diffusion, Pairformer, confidence) | barraCuda + coralReef | **Active** |
| `blake3` `pure` feature | barraCuda ecoBin | **Requested** |

**Composition needs:** NUCLEUS (Tower→Node→Nest), petalTongue (16 scenario builders), WDM+coralForge mixed pipeline, Squirrel MCP tools.

---

### wetSpring (Life Science/PFAS) — LEAN ACHIEVED (GPU pending)

| What | Absorbs Into | Status |
|------|-------------|--------|
| 150+ barraCuda primitives | barraCuda | **Leaning** |
| 0 local WGSL | — | **Fully lean** |
| 5 ODE shaders (phage_defense, bistable, multi_signal, cooperation, capacitor) | toadStool → barraCuda | **Write phase** |
| Vault (ChaCha20, Ed25519, BLAKE3) | BearDog | Overlap — needs resolution |

**Composition needs:** NestGate NCBI→diversity pipeline, ToadStool GPU Anderson, petalTongue (9 DataChannel types, 33 scenario builders), cross-spring S79/S86/S87 evolution.

---

## Composition Pipelines primalSpring Must Validate

### P0 — Foundational (primalSpring already scaffolds these)

| Pipeline | Primals | Status in primalSpring |
|----------|---------|----------------------|
| **Tower Atomic** | BearDog + Songbird | exp001 — scaffolded |
| **Node Atomic** | Tower + ToadStool | exp002 — scaffolded |
| **Nest Atomic** | Tower + NestGate | exp003 — scaffolded |
| **Full NUCLEUS** | All 8 foundation + provenance | exp004 — scaffolded |

### P1 — Cross-Primal Compute (NOT yet in primalSpring)

| Pipeline | Primals | Springs Needing It |
|----------|---------|-------------------|
| **Sovereign Compute Triangle** | barraCuda (math) → coralReef (compile) → toadStool (dispatch) | hotSpring, neuralSpring, groundSpring |
| **GPU Shader Absorption** | Spring WGSL → barraCuda catalog → coralReef compile → toadStool deploy | All springs with shaders |
| **Mixed Hardware Dispatch** | toadStool (GPU + NPU + CPU routing) | hotSpring (4-layer brain), groundSpring |
| **Precision Routing** | barraCuda (f32/f64 strategy) → toadStool (device capability) | All scientific springs |

### P2 — Rendering + Audio (NOT yet in primalSpring)

| Pipeline | Primals | Springs Needing It |
|----------|---------|-------------------|
| **Windowed Rendering** | Spring (game state) → barraCuda (compute) → coralReef (compile) → toadStool (dispatch) → petalTongue (surface + present) | ludoSpring (primary), all springs (viz) |
| **Audio Output** | Spring (narration cues) → petalTongue (PCM synthesis + device output) | ludoSpring (primary), healthSpring (biosignal sonification) |
| **Live Dashboard Streaming** | Spring (telemetry NDJSON) → petalTongue (render stream) | All springs |

### P3 — Data + Provenance (partially scaffolded)

| Pipeline | Primals | Springs Needing It |
|----------|---------|-------------------|
| **Provenance Trio Round-Trip** | rhizoCrypt (workspace) → loamSpine (commit) → sweetGrass (attribute) | All springs |
| **NestGate Ingest Pipeline** | NestGate (fetch) → BearDog (verify) → Spring (process) → NestGate (store) | wetSpring (NCBI/SRA), groundSpring (NOAA/IRIS), ludoSpring (NCBI QS) |
| **Consent-Gated Access** | BearDog (ZKP) → NestGate (encrypted store) → Spring (decrypt + process) | healthSpring |
| **Content-Addressed Datasets** | NestGate (BLAKE3 addressing) → Spring (reproducible fetch) | All springs |

### P4 — Emergent / Multi-Spring (scaffolded, not validated)

| Pipeline | Primals | Description |
|----------|---------|-------------|
| **Cross-Spring Ecology** | airSpring → wetSpring → neuralSpring via biomeOS | Ecological data flows |
| **RootPulse VCS** | BearDog + NestGate + Songbird | Distributed version control |
| **RPGPT Game Engine** | ludoSpring (logic) + Squirrel (narration AI) + NestGate (certs) + petalTongue (rendering) + provenance trio | Multi-primal game |
| **Deploy Graph Execution** | biomeOS graph executor → primal constellation | Springs as BYOB niche deploys |

---

## primalSpring's Own Gaps (What to Build Next)

### Critical — Must validate for ecosystem to evolve

1. **Sovereign Compute Triangle validation** — barraCuda → coralReef → toadStool. This is the backbone. Every scientific spring depends on it. primalSpring exp050 mentions it but does not exercise it.

2. **Spring-to-Primal Absorption Tracker** — primalSpring has no concept of absorption tracking. It should track: which spring code is Write/Absorb/Lean status, which WGSL shaders have been absorbed upstream, which local math has been delegated. This is primalSpring's unique value.

3. **Graph Execution Validation** — primalSpring has 6 TOML deploy graphs but no graph executor integration with biomeOS. When springs thin to deploy graphs, primalSpring must validate that biomeOS can execute them.

4. **petalTongue Surface Pipeline** — No rendering or audio pipeline validation exists. This blocks every spring's visualization story and ludoSpring's game rendering.

### High — Needed for mature composition

5. **Shader Absorption Round-Trip** — Spring writes WGSL → barraCuda absorbs → coralReef compiles → toadStool dispatches → Spring validates parity. This is the Write→Absorb→Lean cycle. primalSpring should have an experiment that validates the full cycle.

6. **Protocol Escalation** — exp052 defines HTTP → JSON-RPC → tarpc but doesn't exercise it. Real escalation is needed for production.

7. **Multi-Family Bonding** — OrganoMetalSalt (multi-family with catalytic bridge) is defined but has no experiment.

8. **Cross-Tower Federation** — exp056 is scaffolded only.

### Medium — Ecosystem maturity

9. **PathwayLearner** — exp015 scaffolded. biomeOS graph optimization from runtime telemetry.

10. **Squirrel AI Coordination** — exp044 scaffolded. Squirrel + Spring intent routing.

11. **Bearer Token Auth** — exp054 scaffolded. BearDog-issued tokens for cross-primal auth.

12. **Supply Chain Provenance** — exp057 scaffolded. Full audit trail for primal dependencies.

---

## Cross-Spring IPC Wiring Matrix

Which springs talk to which primals today:

| | barraCuda | toadStool | NestGate | petalTongue | BearDog | Squirrel | Provenance Trio | biomeOS |
|---|---|---|---|---|---|---|---|---|
| **airSpring** | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | ✓ |
| **groundSpring** | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | ✓ |
| **healthSpring** | ✓ | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| **hotSpring** | ✓ | ✓ | — | — | — | — | — | — |
| **ludoSpring** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **neuralSpring** | ✓ | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| **wetSpring** | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | ✓ |
| **primalSpring** | — | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |

**Gaps to close:**
- hotSpring: NestGate (AME2020/EOS data), BearDog (provenance), biomeOS (Neural API), petalTongue (viz), provenance trio
- healthSpring: BearDog (consent ZKP)
- neuralSpring: BearDog (trust), provenance trio (rhizoCrypt streaming, sweetGrass convergence)
- wetSpring: provenance trio round-trip
- primalSpring: petalTongue (surface pipeline validation), barraCuda (compute triangle)

---

## WGSL Shader Absorption Status — Ecosystem Wide

| Spring | Total Local WGSL | Absorbed | Pending | P1 Candidates |
|--------|-----------------|----------|---------|---------------|
| airSpring | 0 | 6 (retired) | 0 | — |
| groundSpring | 2 (metalForge) | 0 | 2 | anderson_lyapunov |
| healthSpring | 6 | 0 | 6 | Hill, PopPK, Diversity, MM, SCFA, Beat |
| hotSpring | 85 | ~50 | ~35 | Dirac, CG, pseudofermion HMC |
| ludoSpring | 14 (3 game + 11 exp030) | 9 (exp030 fossils) | 5 | pathfind, DDA raycast, engagement, fog, lighting |
| neuralSpring | 0 local (wraps 47 barraCuda) | — | — | coralForge phases |
| wetSpring | 0 local | 0 | 5 ODE (write phase) | phage_defense, bistable, multi_signal, cooperation, capacitor |

**Total pending absorption:** ~53 WGSL shaders across ecosystem.

---

## The Endgame — Springs as BYOB Niche Deploy Graphs

When absorption is complete, each spring becomes:

| Spring | Deploy Graph | Primals Composed | What Remains Local |
|--------|-------------|-----------------|-------------------|
| airSpring | `airspring_deploy.toml` | barraCuda + toadStool + NestGate + petalTongue + provenance trio | Niche orchestration, validation harness |
| groundSpring | `groundspring_deploy.toml` | barraCuda + toadStool + NestGate + provenance trio | Measurement theory validation |
| healthSpring | `healthspring_deploy.toml` | barraCuda + toadStool + NestGate + BearDog + petalTongue + provenance trio | Clinical workflow orchestration |
| hotSpring | `hotspring_deploy.toml` | barraCuda + toadStool + coralReef + NestGate | Physics simulation orchestration |
| ludoSpring | `ludospring_deploy.toml` | barraCuda + toadStool + coralReef + petalTongue + Squirrel + NestGate + provenance trio | Game design law orchestration |
| neuralSpring | `neuralspring_deploy.toml` | barraCuda + toadStool + coralReef + Squirrel + NestGate + petalTongue | Learning pipeline orchestration |
| wetSpring | `wetspring_deploy.toml` | barraCuda + toadStool + NestGate + BearDog + petalTongue + provenance trio | Life science pipeline orchestration |

primalSpring validates that each of these deploy graphs actually resolves, that all
required capabilities are discoverable, that latency budgets hold, and that graceful
degradation works when primals are missing.

---

## Immediate Action Items for primalSpring Team

### Week 1 — Foundation

1. **Clone petalTongue** to `ecoPrimals/` (currently registry-only, docs in wateringHole).
2. **Wire exp050 (Compute Triangle)** to actually exercise barraCuda → coralReef → toadStool. Currently scaffolded.
3. **Add absorption tracking types** — `AbsorptionStatus { Write, Absorb, Lean }` per spring per primitive. No spring has this; primalSpring should own the ledger.

### Week 2 — Cross-Spring

4. **Add rendering pipeline experiment** — Validate: Spring → barraCuda compute → toadStool dispatch → petalTongue surface. Even if petalTongue isn't running, validate the capability chain resolves.
5. **Add audio pipeline experiment** — Validate: Spring narration cue → petalTongue audio sonification.
6. **Wire IPC matrix gaps** — hotSpring has the most gaps (no NestGate, BearDog, biomeOS, petalTongue, provenance trio).

### Week 3 — Maturity

7. **Implement graph executor integration** — Connect to biomeOS deploy graph execution. Validate that TOML graphs actually produce running primal constellations.
8. **Flesh out scaffolded experiments** — exp052 (protocol escalation), exp054 (bearer auth), exp056 (cross-tower federation), exp057 (supply chain provenance) are all scaffolds.
9. **Validate WGSL absorption round-trip** — Pick one pending shader (e.g., healthSpring Hill shader), track it from spring local → barraCuda catalog → coralReef compile → toadStool dispatch → spring validation.

---

## Notes for Co-Development with ludoSpring

ludoSpring stays in game science (Fitts, Hick, Steering, Flow, DDA, engagement,
Perlin, WFC, BSP, Tufte, Four Keys to Fun). Its 75 experiments and 1,692 validation
checks prove that game design laws port faithfully to Rust+GPU.

What ludoSpring needs from primalSpring:

- **Rendering composition validation** — ludoSpring has raycaster math, voxel data,
  fog/lighting/pathfinding shaders, entity/world systems. It does NOT have windowed
  rendering. That's a composition of ludoSpring + petalTongue + toadStool + coralReef.
  primalSpring should validate this composes.

- **Audio composition validation** — ludoSpring produces `NarrationCue` structs and
  `SoundEffect` tags. petalTongue is expected to handle actual audio output.
  primalSpring should validate the cue→playback pipeline.

- **RPGPT composition validation** — The RPGPT engine needs ludoSpring (game logic) +
  Squirrel (narration AI) + NestGate (ruleset certificate storage) + petalTongue
  (rendering) + provenance trio (session history). This is a 7-primal composition.

- **Shader absorption tracking** — ludoSpring has 5 pending shader absorptions
  (pathfind_wavefront, DDA raycast, engagement_batch, fog_of_war, tile_lighting).
  primalSpring should track these through the Write→Absorb→Lean cycle.

ludoSpring will continue to validate domain science independently. primalSpring
validates the wiring.

---

**License:** AGPL-3.0-or-later
