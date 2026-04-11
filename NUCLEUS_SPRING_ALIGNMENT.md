# NUCLEUS Spring Alignment — Phase 34

**Date**: April 11, 2026
**From**: primalSpring v0.9.9
**For**: All springs, primals, and gardens
**License**: AGPL-3.0-or-later

---

## The Atomic Model

Every spring composes from the same NUCLEUS atomics. Each spring stresses
different portions based on its domain. As springs evolve, they harden the
primals they depend on — and those improvements propagate to every other
spring in the ecosystem.

| Atomic | Particle | Primals | Fragment |
|--------|----------|---------|----------|
| Tower | Electron | BearDog + Songbird | `tower_atomic` |
| Node | Proton | Tower + ToadStool + barraCuda + coralReef | `node_atomic` |
| Nest | Neutron | Tower + NestGate + rhizoCrypt + loamSpine + sweetGrass | `nest_atomic` |
| NUCLEUS | Atom | Tower + Node + Nest (9 unique primals) | `nucleus` |
| Meta-tier | — | biomeOS + Squirrel + petalTongue | `meta_tier` |

Fragments are canonical patterns defined in `primalSpring/graphs/fragments/`.
Deploy graphs declare their atomics via `fragments = [...]` metadata.
Bonding policies document how atomics bind within cross-atomic compositions.

---

## Spring × Atomic Alignment Matrix

Every science spring now has a proto-nucleate graph in
`primalSpring/graphs/downstream/` that defines its target NUCLEUS composition.

| Spring | Version | Tests | Primary Atomics | Proto-Nucleate | Particle Profile |
|--------|---------|-------|-----------------|----------------|------------------|
| **hotSpring** | 0.6.32 | ~870 | **Node** (proton-heavy) + Nest | `hotspring_qcd_proto_nucleate` | proton_heavy |
| **neuralSpring** | 0.1.0 | 1,403 | **Node** + Meta | `neuralspring_inference_proto_nucleate` | balanced |
| **wetSpring** | 0.1.0 | 1,902 | Node + **Nest** + Meta | `wetspring_lifescience_proto_nucleate` | balanced |
| **airSpring** | 0.10.0 | 986 | Node + **Nest** | `airspring_ecology_proto_nucleate` | balanced |
| **groundSpring** | 0.1.0 | 1,050+ | Node + **Nest** | `groundspring_geoscience_proto_nucleate` | balanced |
| **healthSpring** | 0.1.0 | 928 | **Nest** (neutron-heavy) + Meta | `healthspring_enclave_proto_nucleate` | neutron_heavy |
| **ludoSpring** | 0.1.0 | 222 | Node + **Meta** | `ludospring_proto_nucleate` | balanced |

Also: **esotericWebb** (garden) → `esotericwebb_proto_nucleate` — full NUCLEUS + Meta, pure composition.

---

## neuralSpring: AI Provider for the Ecosystem

neuralSpring has a unique cross-cutting role. As it evolves WGSL shader
ML inference, **every other spring gains AI capabilities** through Squirrel.

```
neuralSpring evolves inference.complete / inference.embed / inference.models
    ↓ registers as Squirrel provider
Squirrel discovers neuralSpring (or falls back to Ollama)
    ↓ ai.query / ai.complete / inference.*
Every spring with Squirrel in its composition gets AI
```

### What Each Spring Gains

| Spring | AI Capability | Use Case |
|--------|--------------|----------|
| **hotSpring** | `inference.complete` | AI-guided simulation parameter selection, anomaly detection in QCD |
| **wetSpring** | `inference.complete` + `inference.embed` | AI sample triage, specimen classification, sensor anomaly detection |
| **airSpring** | `inference.complete` + `inference.embed` | Ecological prediction, crop stress classification |
| **groundSpring** | `inference.complete` | AI-guided calibration, inverse problem parameter estimation |
| **healthSpring** | `inference.complete` + `inference.embed` | Clinical decision support, drug interaction classification |
| **ludoSpring** | `inference.complete` | AI Dungeon Master narration, NPC dialogue |
| **esotericWebb** | `inference.complete` | Narrative generation, AI-driven world building |

### Inference Evolution Path

```
Phase 1 (now):   Squirrel → Ollama (external vendor, HTTP)
Phase 2 (next):  Squirrel → neuralSpring → WGSL shader composition
                 (tokenization + attention + FFN as barraCuda shaders)
Phase 3 (later): Squirrel → neuralSpring → domain-specific models
                 (each spring contributes domain training data)
```

No spring needs to change code to benefit from neuralSpring's evolution.

---

## Per-Spring Composition Detail

### hotSpring — Lattice QCD / HPC Physics

**Atomics**: Tower + **Node** (proton-heavy) + Nest

| Primal | Role in hotSpring |
|--------|-------------------|
| coralReef | Compile QCD-specific WGSL (gauge update, Wilson/Dirac, HMC) |
| toadStool | Metallic GPU fleet dispatch (lattice partitioning) |
| barraCuda | df64 tensor shaders (SU(3) matmul, FFT, CG solver) |
| NestGate | Gauge configuration cache |
| Provenance trio | Reproducibility witness per configuration |

**Evolves for ecosystem**: df64 GPU precision, multi-GPU fleet dispatch,
shader pipeline scaling, HPC deployment patterns.

### neuralSpring — ML / AI Inference

**Atomics**: Tower + **Node** + Meta (Squirrel)

| Primal | Role in neuralSpring |
|--------|---------------------|
| coralReef | Compile ML-specific WGSL (tokenizer, attention, KV-cache) |
| toadStool | Inference pipeline scheduling |
| barraCuda | Transformer shaders (matmul, attention, softmax, gelu) |
| Squirrel | Inference routing (registers as provider) |
| NestGate | Model weight cache (optional) |

**Evolves for ecosystem**: WGSL tokenization, native inference without
Ollama/CUDA, `inference.*` wire standard, model routing.

### wetSpring — Life Science & Analytical Chemistry

**Atomics**: Tower + Node + **Nest** + Meta (Squirrel + petalTongue)

| Primal | Role in wetSpring |
|--------|-------------------|
| coralReef | Domain WGSL (spectral deconvolution, phylogenetics) |
| toadStool | GPU/NPU dispatch (Akida edge classification) |
| barraCuda | Spectral analysis, peak detection, statistical clustering |
| NestGate | Specimen/sensor time-series storage |
| Provenance trio | Sample chain-of-custody |
| Squirrel | AI-driven triage and anomaly detection |
| petalTongue | Real-time lab monitoring dashboards |

**Evolves for ecosystem**: Time-series storage, streaming pipelines,
NPU/edge dispatch, biodiversity attribution.

### airSpring — Ecological & Agricultural Science

**Atomics**: Tower + Node + **Nest**

| Primal | Role in airSpring |
|--------|-------------------|
| coralReef | Ecology WGSL (ET₀, soil moisture, canopy resistance) |
| toadStool | GPU/NPU dispatch (edge sensor nodes) |
| barraCuda | PDE solvers, FFT, statistical analysis |
| NestGate | IoT sensor time-series + model outputs |
| Provenance trio | Measurement attribution for compliance |

**Evolves for ecosystem**: PDE solver shaders, IoT ingestion patterns,
NPU edge dispatch, environmental compliance attribution.

### groundSpring — Geoscience & Measurement Science

**Atomics**: Tower + Node + **Nest**

| Primal | Role in groundSpring |
|--------|---------------------|
| coralReef | Geology WGSL (noise filters, inverse solvers) |
| toadStool | Compute dispatch |
| barraCuda | FFT, matrix decomposition, Anderson-Darling, WDM |
| NestGate | Geospatial data + calibration records |
| Provenance trio | Calibration audit trails |

**Evolves for ecosystem**: Statistical shader library, inverse problem
solvers, long-duration storage, calibration traceability.

### healthSpring — Clinical / Compliance

**Atomics**: **Tower** (dual-tower) + **Nest** (neutron-heavy) + Meta

| Component | Role in healthSpring |
|-----------|---------------------|
| Tower A (FAMILY_A) | Patient data enclave: NestGate-A + Provenance Trio A |
| Tower B (FAMILY_B) | Analytics: Squirrel + NestGate-B (model cache) |
| Ionic bridge | De-identified aggregates only cross the fence |
| BearDog | Cross-family ionic bond enforcement |

**Evolves for ecosystem**: Ionic bond runtime, data egress fences,
dual-tower enclave pattern, `crypto.sign_contract`, HIPAA audit trails.

### ludoSpring — Game Science / HCI

**Atomics**: Tower + Node + **Meta** (Squirrel + petalTongue)

| Primal | Role in ludoSpring |
|--------|-------------------|
| coralReef | Game WGSL (Fitts, Perlin, WFC) |
| toadStool | 60Hz tick-budget dispatch |
| barraCuda | Game math shaders (noise, procedural, physics) |
| Squirrel | AI Dungeon Master (narration, NPC dialogue) |
| petalTongue | Scene rendering, TUI |
| NestGate | Session persistence |

**Evolves for ecosystem**: 60Hz composition budget, pure composition
proof (graph-as-product), AI latency testing, session lifecycle.

---

## Composition Readiness Status

Each spring is evolving toward its proto-nucleate target. This table shows
where each spring currently stands in the **primal composition** maturity
ladder (see `SPRING_COMPOSITION_PATTERNS.md` for the standardized patterns).

| Spring | Method Norm | Capability Reg | Socket Discovery | Dispatch Routing | Graph Validation | biomeOS Gate | Provenance Graceful | Niche Identity |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **healthSpring** | YES | YES (science+infra, cost, deps) | YES (6-tier) | YES (two-tier) | — | — | YES | YES |
| **neuralSpring** | YES | YES (TOML + tarpc) | YES (5-tier) | partial | — | — | — | YES |
| **wetSpring** | YES (iterative) | partial | YES | YES | — | — | YES | YES |
| **hotSpring** | YES | partial | YES (NucleusContext) | partial | — | — | — | YES |
| **airSpring** | partial | partial | YES | partial | — | — | YES | YES |
| **groundSpring** | partial | partial | YES (metalForge) | — | — | YES | — | YES |
| **ludoSpring** | — | — | partial | — | YES (recipe.rs) | — | — | partial |

**Key**: YES = pattern adopted, partial = incomplete or needs update, — = not yet started

### What Each Spring Needs Next

| Spring | Next Step |
|--------|-----------|
| **healthSpring** | Deploy graph validation against proto-nucleate; biomeOS feature gate |
| **neuralSpring** | Complete dispatch routing (two-tier); register as Squirrel inference provider |
| **wetSpring** | Capability registration with cost/deps; deploy graph validation |
| **hotSpring** | Create `graphs/` directory with deploy TOMLs; full capability registration |
| **airSpring** | Method normalization in all paths; capability registration with cost/deps |
| **groundSpring** | Method normalization; dispatch routing; provenance graceful degradation |
| **ludoSpring** | Method normalization; capability registration; socket discovery (tiered) |

---

## Cross-Pollination Network

```
hotSpring ──df64/GPU fleet──→ barraCuda/coralReef ←──ML shaders── neuralSpring
    │                              ↕                                    │
    │                         toadStool                                 │
    │                              ↕                                    ↓
    │              ┌── airSpring (PDE/IoT)                         Squirrel
    │              ├── groundSpring (stats/geo)          (inference provider)
    │              ├── wetSpring (spectral/bio)                        ↓
    │              └── ludoSpring (game math)             ALL springs get AI
    │                              ↕
    └──metallic fleet──→ healthSpring ──ionic bonds──→ BearDog
                              ↕
                         NestGate / Provenance trio
                    (every spring benefits from
                     audit, storage, attribution)
```

---

## Feedback Protocol

When a spring discovers a gap or pattern:

1. **Document the gap** — what capability is missing, what the workaround is
2. **Propose the wire** — what JSON-RPC method signature would close the gap
3. **Build validation** — a primalSpring experiment or graph that tests the gap
4. **Hand back** — PR to primalSpring `docs/PRIMAL_GAPS.md` + graph in
   `graphs/downstream/`

primalSpring triages, refines, and routes gaps to the responsible primal team.
Handoffs go to `infra/wateringHole/handoffs/`.

---

## Evolution Priority by Primal

| Primal | Primary Spring Drivers | Key Evolution |
|--------|----------------------|---------------|
| **barraCuda** | hotSpring, neuralSpring, ludoSpring | df64 precision, ML shaders, tick-budget dispatch |
| **coralReef** | hotSpring, neuralSpring | Domain-specific shader compilation, pipeline optimization |
| **toadStool** | hotSpring, ludoSpring | Multi-GPU dispatch, tick-budget scheduling, federation |
| **NestGate** | healthSpring, wetSpring, groundSpring | Egress fences, time-series storage, geospatial indexing |
| **BearDog** | healthSpring | Ionic bond contracts, cross-family trust, regulatory crypto |
| **Songbird** | all (federation) | NAT traversal, mesh scaling, relay protocols |
| **Provenance trio** | healthSpring, wetSpring | Audit trails, attribution granularity, federation |
| **Squirrel** | neuralSpring, ludoSpring | Inference routing, model discovery, real-time AI |
| **petalTongue** | ludoSpring, esotericWebb | Scene rendering, dashboard patterns, TUI push |
| **biomeOS** | all (orchestration) | Graph execution performance, tick-loop scheduling |

---

## Getting Started (for any spring)

1. **Read your proto-nucleate**: `primalSpring/graphs/downstream/{yourspring}_*_proto_nucleate.toml`
2. **Check atomics**: which fragments does your proto-nucleate declare?
3. **Adopt composition patterns**: follow `infra/wateringHole/SPRING_COMPOSITION_PATTERNS.md` — method normalization, capability registration, tiered discovery, niche identity
4. **Wire IPC**: call primals by capability, not identity
5. **Validate composition**: run primalSpring experiments for your composition (Level 5-6 maturity)
6. **Evolve**: push domain-specific WGSL through coralReef, compute through toadStool
7. **Add Squirrel**: when ready for AI, add `squirrel` to your composition — neuralSpring's inference is immediately available
8. **Hand back**: document gaps and patterns → primalSpring → primal teams → `infra/wateringHole/handoffs/`

---

**License**: AGPL-3.0-or-later
