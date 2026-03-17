# ecoPrimals Glossary

**Purpose**: Definitive terminology for the ecoPrimals ecosystem. If a term is used
in any document, handoff, or conversation, its meaning is defined here.

**Last Updated**: March 16, 2026

---

## The Physical Layer

### Gate

A **gate** is a physical computer — a deployment target that runs the ecoPrimals
stack. Gates are named using camelCase (`firstLast`) like all ecoPrimals entities.
The project operates on 10 towers + 4 small form factor nodes:

| Gate | Display GPU | Work / HBM2 | Role |
|------|-------------|-------------|------|
| **northGate** | RTX 5090 | — | Flagship AI/LLM compute |
| **southGate** | RTX 4060 | swappable | Gaming + heavy compute |
| **eastGate** | RTX 4070 | — | Utility + neuromorphic (1× Akida) |
| **gate-04** | — | RTX 3090 + RX 6950 XT | Bioinformatics (1× Akida) |
| **biomeGate** | RTX 5060 | 2× Titan V + 2× MI50 | HBM2 test bench (1× Akida) |
| **westGate** | RTX 2070S | — | Cold storage (76 TB ZFS) |

Each gate has a **display tier** (small GPU, permanent) and **PCIe slots for
swappable work cards**. Every gate is a PCIe-parallelizable system — work cards
physically move to where the science is.

A gate runs an operating system (Pop!\_OS / Linux), a toolchain (Rust, Cursor),
and the biomeOS substrate. Gates are sovereign — no cloud, no allocation queue,
no institutional dependency. You own the hardware, you own the compute.

When Plasmodium is active, multiple gates bond into a collective. Any gate can
query the collective; workloads route to the best gate by capability match.

### Operational Substrate

The software environment a gate provides to the ecoPrimals stack:

| Layer | Standard |
|-------|----------|
| **OS** | Pop!\_OS (Ubuntu-based, System76). Linux kernel. |
| **Shell** | bash |
| **Toolchain** | Rust (stable + nightly), `cargo`, `clippy`, `rustfmt` |
| **Editor** | Cursor (VS Code fork with AI agent) |
| **GPU** | Vulkan (via wgpu for portable path, VFIO for sovereign path) |
| **NPU** | AKD1000 (BrainChip Akida) via pure Rust driver |
| **Version control** | git, GitHub (SSH), one repo per primal/spring |
| **Package manager** | apt (system), cargo (Rust), pip (Python cross-validation only) |

No Docker. No Kubernetes. No cloud VMs. The gate IS the infrastructure.

---

## The Software Layer

### Primal

A **primal** is a self-contained Rust binary that provides a collection of
**primitives** — small, focused capabilities solving one domain well. Primals
are autonomous: each knows only itself. Complexity is solved through
**coordination**, not by making a primal larger.

Key properties:
- Self-knowledge only (never imports another primal's code)
- Capability-based discovery at runtime
- Zero compile-time coupling between primals
- Pure Rust (no C dependencies in application code)
- UniBin architecture (one binary, multiple modes via subcommands)

Examples: bearDog (cryptography), songBird (networking), toadStool (hardware),
barraCuda (math), coralReef (shader compilation), Squirrel (AI coordination).

**Naming convention**: Canonical capitalization is camelCase with firstLast —
`bearDog`, `songBird`, `toadStool`, `sweetGrass`, `wetSpring`, `hotSpring`.
In prose, initial caps are common (BearDog, ToadStool) and acceptable.
The camelCase structure is intentional — even names like songBird and toadStool
leverage the semantic naming (song+Bird, toad+Stool) for discoverability.

### Primitive

A **primitive** is the atomic unit of capability a primal provides. BearDog's
primitives include Ed25519 signing, BLAKE3 hashing, X25519 key exchange.
barraCuda's primitives include f64 WGSL shaders for dot products, FFT,
eigensolve, and statistical functions. A primitive is the smallest thing a
primal can do.

### Spring

A **spring** is a science primal — a Rust binary that reproduces published
scientific papers and validates computational methods against known results.
Springs are named after natural water sources: wetSpring, hotSpring, airSpring,
neuralSpring, groundSpring, healthSpring, ludoSpring.

Springs evolve through a defined pipeline:

```
Python baseline → Rust validation → GPU acceleration → sovereign pipeline → niche deployment
```

Each spring has:
- Its own git repository
- A `specs/PAPER_REVIEW_QUEUE.md` tracking papers to reproduce
- Numbered experiments with counted checks
- A faculty anchor (a professor whose publications drive the science)

Springs are the first niches being built. They were sketched and validated as
standalone binaries before the evolution step to biomeOS graph deployments.

### Atomics

**Atomics** are the core primal interaction patterns — the named compositions
that larger niches are built on. They are not separate software; they are
what happens when specific primals coordinate.

| Atomic | Composition | What Emerges |
|--------|-------------|-------------|
| **Tower Atomic** | BearDog + Songbird | Pure Rust HTTPS (crypto + TLS + network) |
| **Node Atomic** | Tower + toadStool + barraCuda | Hardware-aware compute (+ GPU math) |
| **Nest Atomic** | Tower + NestGate | Secure content-addressed storage |
| **Full NUCLEUS** | All foundation primals + Squirrel | Complete AI-coordinated ecosystem |

Atomics are the building blocks. You don't deploy "Tower Atomic" — you deploy
a niche that uses Tower Atomic's capabilities because it needs crypto + networking.

### Niche

A **niche** is a biomeOS BYOB (**Build Your Own Biome**) deployment — a composed
set of primals, chimeras, and interactions deployed as a unit via a deploy graph.
A niche is what you actually run.

Examples:
- A field genomics niche: wetSpring + toadStool (NPU) + NestGate + BearDog
- A game science niche: ludoSpring + petalTongue + toadStool + barraCuda
- A precision health niche: healthSpring + barraCuda + petalTongue + NestGate

A niche is defined by:
- A **deploy graph** (TOML DAG) — germination order and capability wiring
- A **niche YAML** — organisms, interactions, customization options
- **Capability domains** — semantic namespaces (`ecology.*`, `precision.*`)

### Deploy Graph

A **deploy graph** is a TOML-encoded directed acyclic graph (DAG) that tells
biomeOS how to start and wire a niche. It specifies:
- Which primals to germinate (start)
- In what order (dependency edges)
- What capabilities to wire together
- What resources to allocate

biomeOS reads the graph, germinates the primals, waits for their sockets, and
wires their capabilities together. The graph is the deployment contract.

### Chimera

A **chimera** is a fused multi-primal organism with a unified API. Unlike a
niche (which coordinates separate processes), a chimera is a single binary that
combines capabilities from multiple primal lineages.

Example: `gaming-mesh` = Songbird networking + ludoSpring game logic, fused
into a single binary with one API surface.

Chimeras are rare and intentional — most composition should happen via IPC
coordination, not fusion.

### Germination

**Germination** is the process of starting a primal and waiting for it to become
ready. A primal germinates when its `server` subcommand starts, its IPC socket
appears, and it responds to `health.check`. biomeOS monitors germination via
deploy graphs.

Analogy: a seed (binary) germinates (starts) in a niche (deployment) on a
gate (computer).

---

## The Coordination Layer

### biomeOS

The **ecosystem substrate** — the orchestration layer that discovers primals,
routes capabilities, composes niches, and manages the lifecycle of everything
running on a gate. biomeOS does not compute science; it coordinates the primals
that do.

Key subsystems:
- **Neural API**: Semantic capability routing (170+ translations, 16 domains)
- **NUCLEUS composition**: Layered atomic patterns
- **Dark Forest coordination**: Zero-metadata discovery
- **Provenance trio wiring**: rhizoCrypt + loamSpine + sweetGrass orchestration

### NUCLEUS

The **full primal composition** orchestrated by biomeOS. NUCLEUS is not a
binary — it is the emergent state when all foundation primals are running and
coordinated on a gate.

```
Tower Atomic (BearDog + Songbird)
  + Node Atomic (+ toadStool + barraCuda)
  + Nest Atomic (+ NestGate)
  + Squirrel (AI)
  = Full NUCLEUS
```

### Plasmodium

The **over-NUCLEUS collective** formed when 2+ gates bond. Named after the
slime mold *Physarum polycephalum* — no central brain, collective intelligence,
pulsing coordination. Gates join and leave dynamically.

When Eastgate and biomeGate bond, their NUCLEUS instances merge into a
Plasmodium. Workloads route to the gate with the best capability match.

### Provenance Trio

The three primals that together provide the project's memory and attribution:

| Primal | Role | Temporal Domain |
|--------|------|-----------------|
| **rhizoCrypt** | Ephemeral memory | Present — working DAG, fast, lock-free |
| **loamSpine** | Permanent memory | Past — immutable linear history, certificates |
| **sweetGrass** | Attribution | Always — semantic provenance, W3C PROV-O braids |

When composed by biomeOS, these three create **RootPulse** — distributed
version control that emerges from primal coordination.

### RootPulse

**Distributed version control** that emerges from the provenance trio's
coordination. RootPulse is not a VCS binary — it is what primals DO together:
rhizoCrypt provides the workspace, loamSpine provides the history, sweetGrass
provides the attribution, BearDog signs it, NestGate stores it, Songbird
syncs it. biomeOS orchestrates the whole thing via Neural API.

---

## The Compute Triangle

Three primals form the sovereign compute stack:

```
barraCuda (WHAT to compute — f64 WGSL shaders, math primitives)
    ↓
coralReef (HOW to compile — WGSL → native GPU binary, naga IR)
    ↓
toadStool (WHERE to run — hardware discovery, dispatch, orchestration)
```

### barraCuda

**Pure math.** 712+ WGSL f64 shaders. Writes the math. Springs depend on
barraCuda directly for math without pulling toadStool's runtime or coralReef's
compiler. Budded from toadStool at Session 93.

### coralReef

**Sovereign shader compiler.** Compiles WGSL to native GPU binaries (SM70-SM89
SASS) without NVIDIA's NVVM or any vendor SDK. Includes VFIO dispatch with PFIFO
channels. The "compiler that frees the math from the vendor."

### toadStool

**Hardware infrastructure.** Discovers CPUs, GPUs, NPUs. Probes capabilities.
Dispatches workloads. Manages the Node Atomic deployment. 20,843 tests, 96+
JSON-RPC methods.

---

## The Science Layer

### metalForge

Where a spring is working on **hardware concepts** — GPU vs CPU routing, GPU to
NPU via PCIe, hardware dispatch architecture. metalForge is the exploratory
substrate where primals figure out how to talk to novel hardware. The brain
architecture in hotSpring evolved through metalForge before stabilizing.

metalForge is not a primal — it is an evolution context. When a spring needs to
push work across compute substrates (CPU → GPU, GPU → NPU) and the path doesn't
exist yet, that work happens in metalForge.

### baseCamp

The transition from **paper validation to real exploration**. baseCamp lives in
`whitePaper/gen3/baseCamp/` and is where springs move beyond reproducing a single
paper to mixing larger datasets and systems. QS-Anderson evolved this way — the
paper parity work validated the pieces, and baseCamp is where those pieces
combine into something new.

Currently 18 papers (01-18), spanning Anderson-QS, LTEE, bioag, sentinels,
symbiotic ecology, no-till, WDM, NPU edge, field genomics, dynamical QCD,
nautilus reservoir computing, immuno-Anderson, sovereign health, precision brain,
anaerobic-aerobic QS, game design as science, RPGPT.

### Paper Parity

The standard of evidence for spring experiments: the Rust implementation must
produce results that match the published paper's results within named tolerances.
Not "close enough" — paper parity means you could substitute the spring's output
for the paper's figures and a reviewer would accept them.

### Experiment

A numbered unit of scientific validation within a spring. Each experiment has:
- A number (e.g., Exp356)
- A defined objective
- Counted checks (e.g., "18/18 PASS")
- A connection to a baseCamp paper or paper queue entry

### Faculty Anchor

A professor whose published work drives a spring's science. Each spring has at
least one faculty anchor. The project reproduces their papers, then extends the
science. Faculty anchors are documented in `whitePaper/attsi/`.

| Spring | Faculty Anchor(s) |
|--------|-------------------|
| wetSpring | Faculty anchor (quorum sensing), faculty anchor (agriculture) |
| hotSpring | Faculty anchor (plasma physics), faculty anchor (lattice QCD), faculty anchor (gradient flow) |
| groundSpring | Faculty anchor (spectral theory) |
| healthSpring | Faculty anchor (pharmacology) |
| neuralSpring | (cross-domain — reproduces from all anchors) |
| airSpring | Faculty anchor (precision agriculture) |
| ludoSpring | Published authors (Flow theory, motor control, procedural generation) |

### attsi

The **faculty outreach program** (`whitePaper/attsi/`). Contains contact
packages, review materials, and outreach strategy for each faculty anchor.
Faculty identities are maintained in the non-anonymous whitePaper layer; anonymized
contacts use hashed identifiers.

---

## The Evolution Vocabulary

### Evolution

In ecoPrimals, **evolution** means directed improvement through validated steps.
A spring evolves from Python baselines to Rust validation to GPU acceleration.
A primal evolves by absorbing primitives upstream (into barraCuda) and
delegating downstream (to toadStool). Evolution is always validated — every
step passes tests.

### Absorption

When a spring's local implementation of a primitive is replaced by a call to
barraCuda's canonical version. The spring "absorbs upstream" — it stops owning
the math and starts consuming the shared version. This is how springs
collectively evolve barraCuda.

### Delegation

The inverse of absorption: when a primal delegates work to another primal.
A spring delegates hardware dispatch to toadStool, math to barraCuda, shader
compilation to coralReef. Delegation is always via IPC, never via code import.

### Deep Debt

Technical debt identified during evolution sessions. Tracked in handoffs, not
in TODO comments in code. Deep debt is actively reduced — the archive of
handoffs is full of "DEEP_DEBT" sessions where primals were systematically
improved.

### Handoff

A **session handoff** document in `wateringHole/handoffs/`. Records what was
done, what's next, what broke, what was discovered. Handoffs are the working
memory between sessions. After ~48 hours they are archived to
`handoffs/archive/` (the fossil record).

### Fossil Record

The `handoffs/archive/` directory. Never deleted, only accumulated. The
geological record of every evolution session the project has run. Currently
354+ documents spanning February 4 – March 15, 2026.

---

## The Meta Layer

### metaPrimal

A **metaPrimal** is a repository that is conceptual instead of functional — it
doesn't compile into a binary, but it is an essential organism in the ecosystem.
metaPrimals follow the same camelCase naming and have their own git repos.

| metaPrimal | Purpose |
|------------|---------|
| **wateringHole** | How primals intercommunicate. Standards, IPC protocols, leverage guides, handoffs. The coordination documentation layer. |
| **whitePaper** | Theses, concepts, and documentation of evolution. The scientific and strategic record — gen2/gen3 paper trails, attsi outreach, baseCamp papers. |
| **sourDough** | The nascent primal for rapid evolution of new primals. A starter culture for bootstrapping new primal projects. |

### Phase 1 / Phase 2

**Temporal artifacts**, not semantic categories. Phase directories were
organizational markers used while building between gates — keeping which primals
were on which gate clear during early development. They correspond loosely to
`gen2/` and `gen3/` in whitePaper. Not actively meaningful; treat them as
historical scaffolding if encountered.

### Version Numbers and Session Numbers

Springs and primals independently evolve their own progress markers. Some use
**session numbers** (e.g., neuralSpring S145), some use **version numbers**
(e.g., hotSpring v0.6.29, wetSpring V113). This divergence is fully
intentional — AI-assisted development means each project self-flavors over
time as its AI iterations accumulate. There is no global numbering standard
because primal autonomy extends to how they count.

---

## Licensing & Strategy

### Lysogeny Protocol

**Area denial through open prior art.** By publishing under AGPL-3.0, every
innovation becomes prior art that prevents patents. Named after bacteriophage
lysogeny — the viral DNA integrates into the host genome and persists.

### scyBorg

The **ecosystem licensing standard** — a triple copyleft framework:

- **AGPL-3.0-or-later**: All code, shaders, tools, infrastructure
- **ORC**: All mechanical interactions (primal coordination, IPC patterns, atomics, game rules)
- **CC-BY-SA 4.0**: All documentation, papers, methodology, reverse engineering findings

Each layer is governed by an independent nonprofit (FSF, Open RPG Creative
Foundation, Creative Commons). No single entity can revoke any layer.

scyBorg extends beyond "just code" to cover the entire body of work — the
papers, the methodology, the evolution trail, the reverse engineering
documentation. The intent is that everything published is permanently open and
untargetable.

### Symbiotic Exception

An **additional permission** (AGPL-3.0 Section 7) granted to a named
organization based on reciprocal benefit. The default scyBorg license applies to
everyone. Exceptions reduce licensing friction for allies — partners whose
tools, hardware, or knowledge benefit the ecosystem.

Exceptions are not for sale. They are diplomatic: granted based on symbiotic
value, revocable if the relationship ends. The public AGPL version is unaffected.

| Tier | Basis |
|------|-------|
| **Symbiotic** | Partner provides tools/hardware/knowledge (e.g., RustDesk, BrainChip) |
| **Reciprocal Open** | Partner publishes their own work under AGPL (e.g., GPU vendor opens architecture docs) |

See `SCYBORG_EXCEPTION_PROTOCOL.md` for the full protocol.

### Suppression Inversion

The strategic principle that by **owning nothing**, the project is untargetable.
No revenue to disrupt, no corporate entity to sue, no publisher to pressure, no
platform to suppress. Knowledge that has been published under copyleft cannot be
un-known. Reverse engineering of owned hardware is legal (*Sega v. Accolade*,
*Oracle v. Google*). The suppression vectors that companies use against
threatening work (legal, platform, commercial) all require a target — and
scyBorg eliminates the target.

### AI Authorship Paradox

All ecoPrimals code and documentation is AI-assisted, and this is disclosed
openly. Copyright law is unsettled on AI-assisted work. The paradox: if
AI-assisted work **is** copyrightable, the copyleft licenses apply normally and
the commons is protected. If AI-assisted work **is not** copyrightable, the
output enters public domain — an even stronger form of openness. Either outcome
preserves the commons. The only parties harmed by a negative ruling are those
claiming exclusive copyright on AI-assisted work for revenue. ecoPrimals has no
such claim, so the legal uncertainty is everyone else's problem.

See `gen3/about/LICENSING_STRATEGY.md` §8 for the full analysis.

### fieldMouse

The **minimal deployable structure** for the ecoPrimals ecosystem. Where a gate
runs a full NUCLEUS and a niche composes primals via a deploy graph, a fieldMouse
is the smallest stripped system — as few as a single atomic or chimera — purpose-built
for a constrained deployment niche.

fieldMouse is not a primal. It is a **deployment class** — a category of niche
deployments defined by how they fit their target hardware and environment. A
fieldMouse might be:

- A Tower Atomic chimera on a RISC-V microcontroller (crypto + network only)
- A Nest Atomic on a Raspberry Pi (crypto + network + storage)
- A sensor node streaming data via songBird to a gate
- A pipette-mounted data acquisition system handling provenance and streaming
- An environmental monitor (pH, temperature, GPS) publishing to the mesh
- An Akida NPU edge classifier on a Coral board

fieldMouse deployments share these properties:

| Property | Description |
|----------|-------------|
| **Minimal** | Smallest subset of atomics for the niche — no unused primals |
| **Embedded-first** | Targets RISC-V, ARM (aarch64/armv7), and constrained SoCs |
| **ecoBin compliant** | Pure Rust, zero C, cross-compiles with `cargo build --target` |
| **Mesh-native** | Connects to the broader ecosystem via songBird or TCP fallback |
| **Provenance-aware** | Even the smallest fieldMouse signs data via bearDog |

The evolutionary ladder extends downward:

```
NUCLEUS     (full primal composition — gate)
  ↓
Niche       (biomeOS deploy graph — selected primals)
  ↓
fieldMouse  (minimal atomic/chimera — embedded, sensor, edge)
```

A fieldMouse on a pipette handles data streaming for the instrument — sample ID,
timestamp, GPS, measurement, provenance signature — and publishes to the mesh.
A fieldMouse on a soil probe does the same for pH, moisture, temperature. A
fieldMouse on an Akida board classifies microbial communities in real time from
MinION streaming data. The primals are the same. The deployment is minimal.

See `FIELDMOUSE_DEPLOYMENT_STANDARD.md` for the specification.

### Novel Ferment Transcript (NFT)

Memory-bound digital objects using the provenance trio. Not blockchain NFTs —
ferment transcripts are provenance-tracked creative artifacts with attribution
chains via sweetGrass and permanence via loamSpine.

---

## Quick Lookup

| Term | One-Line Definition |
|------|---------------------|
| **Gate** | A physical computer running the ecoPrimals stack |
| **Primal** | A self-contained Rust binary providing domain primitives |
| **Primitive** | The atomic unit of capability a primal provides |
| **Spring** | A science primal reproducing published papers |
| **Atomic** | A named primal composition pattern (Tower, Node, Nest, NUCLEUS) |
| **Niche** | A biomeOS BYOB deployment — primals composed via deploy graph |
| **Deploy graph** | TOML DAG defining germination order and capability wiring |
| **Chimera** | A fused multi-primal binary with unified API |
| **Germination** | Starting a primal until its socket is ready |
| **biomeOS** | The orchestration substrate running on a gate |
| **NUCLEUS** | Full primal composition (all atomics + Squirrel) |
| **Plasmodium** | Multi-gate collective (2+ bonded NUCLEUS instances) |
| **metalForge** | Evolution context where springs work on hardware concepts (GPU/CPU/NPU) |
| **baseCamp** | Cross-spring paper program — validation to exploration (18 papers) |
| **metaPrimal** | Conceptual repo (wateringHole, whitePaper, sourDough) — pre-binary, documentaion |
| **Paper parity** | Spring output matches published figures within named tolerance |
| **Absorption** | Spring replaces local math with barraCuda canonical version |
| **Delegation** | Primal routes work to another primal via IPC |
| **Handoff** | Session continuity document in wateringHole |
| **Fossil record** | Archived handoffs — the project's geological history |
| **Lysogeny** | Area denial through open AGPL prior art |
| **scyBorg** | Triple copyleft: AGPL-3.0 (code) + ORC (mechanics) + CC-BY-SA (docs) |
| **Symbiotic exception** | AGPL Section 7 grant to allies based on reciprocal benefit |
| **Suppression inversion** | Owning nothing makes the project untargetable |
| **AI authorship paradox** | Copyright uncertainty harms exclusivity claimants, not the commons |
| **fieldMouse** | Minimal deployable ecoPrimals — smallest atomic/chimera for embedded/sensor/edge niches |
| **primalSpring** | Coordination spring — validates ecosystem composition, graph execution, emergent systems, bonding |
