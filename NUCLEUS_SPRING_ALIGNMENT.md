# NUCLEUS Spring Alignment — Phase 58+

> This is the **canonical** inter-spring reference.
> Local copies exist in `primalSpring/wateringHole/` for spring context.

**Date**: May 5, 2026
**From**: primalSpring v0.9.21+ (Phase 58 — Spring NUCLEUS Composition Audit)
**License**: AGPL-3.0-or-later

---

## The Atomic Model

Every spring composes from the same NUCLEUS atomics. Each spring
stresses different portions based on its domain. As springs evolve,
they harden the primals they depend on — and those improvements
propagate to every other spring in the ecosystem.

| Atomic | Particle | Primals | Fragment |
|--------|----------|---------|----------|
| Tower | Electron | BearDog + Songbird + skunkBat | `tower_atomic` |
| Node | Proton | Tower + ToadStool + barraCuda + coralReef | `node_atomic` |
| Nest | Neutron | Tower + NestGate + rhizoCrypt + loamSpine + sweetGrass | `nest_atomic` |
| NUCLEUS | Atom | Tower + Node + Nest (9 unique primals) | `nucleus` |
| Meta-tier | Cross-atomic | biomeOS + Squirrel + petalTongue | `meta_tier` |
| **Desktop NUCLEUS** | Full 12 | All atomics + meta, petalTongue `live` | `nucleus_desktop_cell` |

### Genetics Layer

Each atomic inherits a genetics posture from the three-tier identity model:

| Tier | Type | Role | Cloneable | Bond Minimum |
|------|------|------|-----------|--------------|
| 1 | Mito-Beacon | Discovery, NAT, metadata | Yes | Metallic, Ionic |
| 2 | Nuclear | Permissions, auth, sessions | No (spawn fresh) | Covalent |
| 3 | Tag | Open channels (deprecated FAMILY_SEED) | Yes | — |

All covalent bonds (same-family, same-trust) require **NuclearLineage** trust —
nuclear genetics must be spawned fresh per generation, never copied. Ionic and
metallic bonds require at minimum **MitoBeaconFamily** trust — mito-beacon
membership for discovery without sharing nuclear credentials. The two-phase
BTSP model (Phase 1: mito-beacon tunnel, Phase 2: nuclear session) ensures
discovery never exposes authorization material.

---

## Spring × Atomic Alignment Matrix

Each spring's proto-nucleate graph is parameterized via `graphs/downstream/downstream_manifest.toml`
using `proto_nucleate_template.toml`. The one exception is `healthspring_enclave_proto_nucleate.toml`,
which has a unique dual-tower ionic bridge pattern and is kept as a standalone graph.

| Spring | Version | gS | Tests | Primary Atomics | Proto-Nucleate | Status |
|--------|---------|------|-------|-----------------|----------------|--------|
| **hotSpring** | 0.6.32 | **5** | 993 | **Node** (proton-heavy) + Nest | `downstream_manifest.toml` | **Active** — Phase 46 absorbed, deep debt complete |
| **neuralSpring** | V157 | **5** | 910 (IPC-first) | **Node** + Meta | `downstream_manifest.toml` | **Active** — S205: NestGate weight persistence wired, Squirrel inference pipeline complete, 37 capabilities, 7 IPC modules, wire hygiene verified, plasmidBin ready |
| **wetSpring** | V151 | **4+** | 1,594 | Node + **Nest** + Meta | `downstream_manifest.toml` | **Active** — Phase 46 absorbed, deep debt, `wetspring_composition.sh` |
| **airSpring** | 0.10.0 | 0 | 1,364 | Node + **Nest** | `downstream_manifest.toml` | **Pinned** — paths fixed |
| **groundSpring** | V124 | 0 | 1,020+ | Node + **Nest** | `downstream_manifest.toml` | **Pinned** — paths fixed |
| **healthSpring** | V59 | **5** | 948 | **Nest** (neutron-heavy) + Meta | `healthspring_enclave_*` | **Active** — Phase 46 absorbed (18/24), deep debt, `healthspring_composition.sh` |
| **ludoSpring** | V53+ | **4** | 820 | Node + **Meta** + Nest | `ludospring_cell.toml` (12-node pure composition) | **Active** — evolution partner, needs more time |

### Key

- **Bold atomic** = primary domain stress point
- **Pinned** = at current guideStone level; science evolution continues independently
- **Active** = focused evolution bandwidth; Phase 46 composition patterns absorbed

---

## Library-to-Binary Rewiring Status (Phase 58 Audit)

During earlier evolution, springs were the laboratories where primal math was
developed. Work started local (hotSpring built precision mixing and df64, wetSpring
evolved spectral analysis), then upstream primals pulled, reviewed, and absorbed.
The spring-local `barracuda/` and `ecoPrimal/` directories are artifacts of this
process. `metalForge/` is architecturally distinct — it is the spring's hardware
abstraction layer (GPU/CPU/NPU) that informs toadStool dispatch and stays local.

| Spring | Rewiring Tier | Local Crate | IPC% | `src/ipc/` | petalTongue | sweetGrass |
|--------|---------------|-------------|------|-----------|-------------|------------|
| primalSpring | **4** (binary-only) | `primalspring` (no barraCuda) | ~100% | Full | — | — |
| **ludoSpring** | **3** | `ludospring-barracuda` | ~40-60% | Full + provenance/ | `game_scene` | Session braids |
| **healthSpring** | **3** | `healthspring-barracuda` | ~30-50% | Full + dispatch/ | DataChannel | Partial |
| **airSpring** | **2** | `airspring-barracuda` | ~25-40% | Full + rpc/ | Not wired | Not wired |
| **wetSpring** | **2** | `wetspring-barracuda` | ~10-20% | Full + handlers/ | Partial | Partial |
| **hotSpring** | **2** | `hotspring-barracuda` | ~5-15% | Scattered | Not wired | Not wired |
| **neuralSpring** | **5** | optional `barracuda` (IPC-first, `default = []`) | 0% direct | `src/ipc/` tree (7 modules, CapabilityRouter, 37 caps) | Wired (deploy graphs) | Wired (composition.status) |
| **groundSpring** | **1** | `groundspring` (optional feature) | ~1-5% | `ipc.rs` only | Not wired | Not wired |

### Rewiring Tiers

- **Tier 1**: Minimal IPC surface; barraCuda is optional or library-only
- **Tier 2**: IPC routing exists; bulk science still links barraCuda library
- **Tier 3**: IPC parity validation active; library and IPC lanes run side-by-side
- **Tier 4**: Library dep dropped; all compute through IPC to ecobin primals

### Standardization Patterns (cross-spring adoption targets)

| Pattern | Origin | Adopt By |
|---------|--------|----------|
| Per-trio-primal IPC modules (`ipc/provenance/{rhizocrypt,loamspine,sweetgrass}.rs`) | ludoSpring | All springs |
| Multi-primal IPC wrappers (`ipc/{coralreef,toadstool,nestgate}.rs`) | ludoSpring | All springs |
| `primal-proof` Cargo feature flag (library vs IPC compilation) | healthSpring | All springs |
| `composition.rs` dual-lane validation model | hotSpring | All springs |
| `PRIMAL_PROOF_IPC_MAPPING.md` method-by-method IPC surface | hotSpring | All springs |
| `primal_bridge.rs` socket scan + `NucleusContext` | hotSpring | All springs |
| Optional `barracuda` feature gate | groundSpring | Tier 1-2 springs |
| Rich handler dispatch tree (`ipc/handlers/`) | wetSpring | All springs |
| Deploy graph per science pipeline (`composition/*.toml`) | ludoSpring | All springs |

### Rewiring Priority

1. **ludoSpring** (3→4) — pure composition model, cleanest test case
2. **healthSpring** (3→4) — `primal-proof` feature already gates compilation
3. **hotSpring** (2→3) — biggest barraCuda contributor validating its own absorption
4. **wetSpring** (2→3) — rich IPC handlers, route compute through ecobin
5. **airSpring** (2→3) — good IPC foundation despite pre-delta
6. **neuralSpring** (5) — `src/ipc/` tree complete (7 modules), CapabilityRouter discovery (37 capabilities, 20 hints), NestGate weight persistence wired (S205), Squirrel inference pipeline complete, Tier 2 COMPLETE, deep debt zero (V157, 910 tests)
7. **groundSpring** (1→2) — expand `ipc.rs` into `src/ipc/` tree

See `SPRING_NUCLEUS_AUDIT_MAY2026.md` for the full per-spring rewiring inventory.

---

## neuralSpring: AI Provider for the Ecosystem

neuralSpring has a unique cross-cutting role: as it evolves the WGSL shader
composition for ML inference, **every other spring gains AI capabilities**.

```
neuralSpring evolves inference.complete / inference.embed / inference.models
    ↓ registers as Squirrel provider
Squirrel discovers neuralSpring (or falls back to Ollama)
    ↓ ai.query / ai.complete / inference.*
Every spring with Squirrel in its composition gets AI
```

### What Each Spring Gains from neuralSpring

| Spring | AI Capability | Use Case |
|--------|--------------|----------|
| **hotSpring** | `inference.complete` | AI-guided simulation parameter selection, anomaly detection in QCD measurements |
| **wetSpring** | `inference.complete` + `inference.embed` | AI sample triage, specimen classification, anomaly detection in sensor streams |
| **airSpring** | `inference.complete` + `inference.embed` | Ecological prediction, sensor anomaly detection, crop stress classification |
| **groundSpring** | `inference.complete` | AI-guided calibration, inverse problem parameter estimation |
| **healthSpring** | `inference.complete` + `inference.embed` | Clinical decision support, drug interaction classification, biosignal analysis |
| **ludoSpring** | `inference.complete` | AI Dungeon Master narration, NPC dialogue, game-science optimization |
| **esotericWebb** | `inference.complete` | Narrative generation, session context, AI-driven world building |

### The Inference Evolution Path

```
Phase 1 (now):   Squirrel → Ollama (external vendor, HTTP)
Phase 2 (next):  Squirrel → neuralSpring → WGSL shader composition
                 (tokenization + attention + FFN as barraCuda shaders)
Phase 3 (later): Squirrel → neuralSpring → domain-specific models
                 (each spring contributes domain training data)
```

Every spring that adds Squirrel to its composition immediately benefits
from neuralSpring's inference evolution — without any code changes.

---

## Per-Spring NUCLEUS Composition Detail

### hotSpring — Lattice QCD / HPC Physics

**Atomics**: Tower + **Node** (proton-heavy) + Nest

```
hotSpring domain layer
    ├── coralReef: QCD-specific WGSL (gauge update, Wilson/Dirac, HMC)
    ├── toadStool: metallic GPU fleet dispatch (lattice partitioning)
    ├── barraCuda: df64 tensor shaders (SU(3) matmul, FFT, CG solver)
    ├── NestGate: gauge configuration cache
    └── Provenance trio: reproducibility witness per configuration
```

**What hotSpring evolves for the ecosystem**:
- df64 double-precision GPU emulation → benefits any spring needing high precision
- Multi-GPU metallic dispatch → benefits any spring needing fleet compute
- Shader pipeline scaling → benefits neuralSpring's multi-stage inference
- HPC deployment patterns → benefits CERN/cloud-scale compositions

---

### neuralSpring — ML / AI Inference

**Atomics**: Tower + **Node** + Meta (Squirrel)

```
neuralSpring domain layer
    ├── coralReef: ML-specific WGSL (tokenizer, attention, KV-cache)
    ├── toadStool: inference pipeline scheduling
    ├── barraCuda: transformer shaders (matmul, attention, softmax, gelu)
    ├── Squirrel: inference routing (registers as provider)
    └── NestGate (optional): model weight cache
```

**What neuralSpring evolves for the ecosystem**:
- Tokenization as WGSL shader → vendor-free tokenization for all springs
- Attention/FFN forward pass → native inference without Ollama/CUDA
- `inference.*` wire standard → unified AI interface for all compositions
- Model routing → Squirrel discovers best provider per-request

---

### wetSpring — Life Science & Analytical Chemistry

**Atomics**: Tower + Node + **Nest** + Meta (Squirrel + petalTongue)

```
wetSpring domain layer
    ├── coralReef: domain WGSL (spectral deconvolution, phylogenetics)
    ├── toadStool: GPU/NPU dispatch (Akida edge classification)
    ├── barraCuda: spectral analysis, peak detection, statistical clustering
    ├── NestGate: specimen/sensor time-series storage
    ├── Provenance trio: sample chain-of-custody
    ├── Squirrel: AI-driven triage and anomaly detection
    └── petalTongue: real-time lab monitoring dashboards
```

**What wetSpring evolves for the ecosystem**:
- Time-series storage patterns → benefits any spring with sensor data
- Streaming pipeline composition → benefits real-time processing springs
- NPU/edge dispatch (Akida) → benefits fieldMouse deployments
- Biodiversity attribution → enriches provenance trio patterns

---

### airSpring — Ecological & Agricultural Science

**Atomics**: Tower + Node + **Nest**

```
airSpring domain layer
    ├── coralReef: ecology WGSL (ET₀, soil moisture, canopy resistance)
    ├── toadStool: GPU/NPU dispatch (edge sensor nodes)
    ├── barraCuda: PDE solvers, FFT, statistical analysis
    ├── NestGate: IoT sensor time-series + model outputs
    └── Provenance trio: measurement attribution for compliance
```

**What airSpring evolves for the ecosystem**:
- PDE solver shaders → benefits physics and biology springs
- IoT sensor ingestion patterns → benefits fieldMouse and edge deployments
- NPU dispatch for edge → validates Akida/Coral composition paths
- Environmental compliance attribution → enriches provenance patterns

---

### groundSpring — Geoscience & Measurement Science

**Atomics**: Tower + Node + **Nest**

```
groundSpring domain layer
    ├── coralReef: geology WGSL (noise filters, inverse solvers)
    ├── toadStool: compute dispatch
    ├── barraCuda: FFT, matrix decomposition, Anderson-Darling, WDM
    ├── NestGate: geospatial data + calibration records
    └── Provenance trio: calibration audit trails
```

**What groundSpring evolves for the ecosystem**:
- Statistical shader library → benefits any spring needing data quality checks
- Inverse problem solvers → benefits physics and signal processing
- Long-duration storage patterns → benefits any spring with archival needs
- Calibration traceability → enriches provenance trio for metrology

---

### healthSpring — Clinical / Compliance

**Atomics**: **Tower** (dual-tower) + **Nest** (neutron-heavy) + Meta

```
healthSpring domain layer
    ├── Tower A (data custody): NestGate-A + Provenance Trio A
    │   └── ionic fence: data cannot leave Tower A as raw
    ├── Tower B (analytics): Squirrel + NestGate-B (model cache)
    │   └── ionic bridge: receives only de-identified aggregates
    └── BearDog: cross-family ionic bond enforcement
```

**What healthSpring evolves for the ecosystem**:
- Ionic bond runtime enforcement (MitoBeaconFamily trust across towers) → benefits any spring with trust boundaries
- Data egress fences → benefits any composition handling sensitive data
- Dual-tower enclave pattern (separate nuclear lineages per tower, shared mito-beacon for discovery) → benefits financial, regulatory, government
- `crypto.sign_contract` capability → enables metered capability sharing
- HIPAA audit trail patterns → enriches provenance trio for compliance
- Nuclear genetics isolation proof → validates that Tier 2 credentials never cross ionic boundaries

---

### ludoSpring — Game Science / HCI

**Atomics**: Tower + Node + **Meta** (Squirrel + petalTongue)

```
ludoSpring composition (pure — no spring binary, 12-node cell graph v2.0)
    ├── coralReef: game WGSL (Fitts, Perlin, WFC)
    ├── toadStool: 60Hz tick-budget dispatch
    ├── barraCuda: game math (Fitts/Hick PG-38 variant params, noise, physics)
    ├── Squirrel: AI Dungeon Master (narration, NPC dialogue)
    ├── petalTongue: scene rendering, TUI
    ├── NestGate: session persistence
    └── Three-layer validation: Python→Rust→composition parity
```

**What ludoSpring evolves for the ecosystem**:
- 60Hz composition budget → tests graph execution latency limits
- Five-layer validation + guideStone → canonical Python→Rust→IPC composition→`ludospring_guidestone`
- guideStone readiness 4 (V53): `ludospring_guidestone` three-tier — 20 bare + 15 IPC + 8 NUCLEUS cross-atomic. GAP-07/10/11 resolved. Live: 18/20 capabilities, game.tick 0.6ms. `cell_launcher.sh` portable deployment
- AI narration under latency → tests Squirrel real-time performance
- Session lifecycle (create/save/restore/fork) → benefits any stateful composition
- Composition drift detection → `composition_targets.json` golden chain

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

Each arrow represents a pattern that flows from one spring's domain work
to harden a shared primal. The network is not hierarchical — it's a
feedback web where every spring solving its problem makes every other
spring's composition more capable.

---

## Phase 46 Composition Evolution (April 27, 2026)

primalSpring extracted a reusable NUCLEUS composition library (`tools/nucleus_composition_lib.sh`, 41 functions).
Each spring receives a lane assignment for domain-specific exploration:

| Spring | Lane | Template Script | Status |
|--------|------|----------------|--------|
| **hotSpring** | Event-Driven Computation + DAG Memoization | `tools/hotspring_composition.sh` | **ABSORBED** — 5 domain hooks, async tick, DAG, braids, compute dispatch |
| **healthSpring** | Ionic-Fenced Clinical Composition | `tools/healthspring_composition.sh` | Absorbed |
| primalSpring | Composition Template Author | `tools/composition_template.sh` | Reference implementation |
| Other springs | Per-lane assignment | Copy template, fill hooks | Available |

### hotSpring Deep Debt Evolution (April 27, 2026)

Alongside Phase 46, hotSpring completed a deep debt cleanup targeting modern idiomatic Rust:

- **Capability-based primal discovery**: `composition.rs` derives all primal requirements from `niche::DEPENDENCIES` (single source of truth). Hardcoded name→domain maps eliminated.
- **Deprecated named accessors**: `primal_bridge.rs` named methods (`toadstool()`, `beardog()`, etc.) deprecated with `#[deprecated]`; all 8 production call sites migrated to `by_domain()`.
- **Data-driven aliases**: `PRIMAL_ALIASES` constant replaces hardcoded fallback checks.
- **Smart file refactoring**: `rhmc.rs` (989L) → `rhmc/mod.rs` (802L) + `rhmc/remez.rs` (190L). `nuclear_eos_helpers.rs` (978L) → `mod.rs` (824L) + `objectives.rs` (174L).
- **Pre-existing compile fixes**: `DiscoveredDevice` API migration in `nuclear_eos_l2_*` binaries.
- **Result**: 993/993 lib tests pass, zero compilation errors, zero `dyn` dispatch on production paths.

---

## Spring Pinning and Evolution Status (May 2026)

**Phase 58 update**: primalSpring has absorbed projectNUCLEUS work. The ecosystem
enters a convergence phase where all springs begin evolving toward full NUCLEUS
compositions for their science papers, with library-to-binary rewiring as the
primary task.

- **Active composition evolution**: ludoSpring, healthSpring, hotSpring
- **Active science with partial composition**: wetSpring, neuralSpring
- **Pre-delta (ready to unpause)**: airSpring, groundSpring
- **Phase 46 composition template is available for all springs** — copy template, fill domain hooks
- **Path dependency fixes from Phase 45 are already applied** (all springs)
- **projectNUCLEUS absorption**: primalSpring has absorbed provenance pipeline
  validation (Nest Atomic, 9 primals). Patterns flow downstream.

Each spring's evolution path:
1. Pull latest primalSpring and plasmidBin
2. Adopt `src/ipc/` directory structure (ludoSpring reference)
3. Create `PRIMAL_PROOF_IPC_MAPPING.md` for domain methods (hotSpring reference)
4. Add `primal-proof` Cargo feature (healthSpring reference)
5. Expand IPC parity validation (Tier 2→3→4)
6. Wire petalTongue DataBinding channels for science outputs
7. Wire sweetGrass braids for experiment attribution
8. Express science papers as end-to-end NUCLEUS composition graphs

### Garden Potential

Each spring may produce its own garden when its science is certified:

| Spring | Potential Garden | Product |
|--------|-----------------|---------|
| hotSpring | milcGarden | MILC results dashboard for physicists |
| wetSpring | labGarden | Environmental sensor monitoring |
| airSpring | fieldGarden | Agricultural decision support |
| groundSpring | geoGarden | Geoscience data browser |
| healthSpring | clinicGarden | Clinical decision support (ionic-fenced) |
| neuralSpring | inferenceGarden | AI model serving dashboard |
| ludoSpring | **esotericWebb** | CRPG composition (**active**) |

---

## Getting Started (for any spring)

1. **Read your manifest entry**: `graphs/downstream/downstream_manifest.toml` or standalone graph
2. **Build your guideStone**: `<spring>_guidestone` binary using `primalspring::composition` API
3. **Validate bare**: confirm P1–P5 properties without any primals running (exit 2)
4. **Deploy NUCLEUS**: `biomeos deploy --graph <your_proto_nucleate>`
5. **Validate NUCLEUS**: guideStone discovers primals, validates IPC parity, exit 0
6. **Use `primalspring::checksums`**: generate and verify CHECKSUMS manifest for P3
7. **Add Squirrel**: when ready for AI, add `squirrel` to your composition
8. **Hand back**: document gaps and patterns → primalSpring → primal teams

---

**License**: AGPL-3.0-or-later
