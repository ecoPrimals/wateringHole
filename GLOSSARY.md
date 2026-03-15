# ecoPrimals Glossary

**Purpose**: Definitive terminology for the ecoPrimals ecosystem. If a term is used
in any document, handoff, or conversation, its meaning is defined here.

**Last Updated**: March 15, 2026

---

## The Physical Layer

### Gate

A **gate** is a physical computer — a deployment target that runs the ecoPrimals
stack. Gates are named. The project currently operates on two:

| Gate | Hardware | Role |
|------|----------|------|
| **Eastgate** | RTX 4070, desktop workstation | Primary development, daily driver |
| **biomeGate** | Threadripper 3970X + RTX 3090 + Titan V | Multi-GPU validation, lattice QCD, HPC workloads |

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

Examples: BearDog (cryptography), Songbird (networking), toadStool (hardware),
barraCuda (math), coralReef (shader compilation), Squirrel (AI coordination).

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

### baseCamp

The **cross-spring paper program** that lives in `whitePaper/gen3/baseCamp/`.
baseCamp papers are where springs meet — each paper draws from multiple springs,
and the science needs drive spring evolution. baseCamp is the indirect
coordination layer for the ecosystem's scientific output.

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
| wetSpring | Chris Waters (QS), Younsuk Dong (agriculture) |
| hotSpring | Michael Murillo (plasma), Alexei Bazavov (lattice QCD), TC Chuna (gradient flow) |
| groundSpring | Ilya Kachkovskiy (spectral theory) |
| healthSpring | Andrea Gonzales (pharmacology) |
| neuralSpring | (cross-domain — reproduces from all anchors) |
| airSpring | Younsuk Dong (precision agriculture) |
| ludoSpring | Csikszentmihalyi (Flow), Fitts, Yannakakis & Togelius |

### attsi

The **faculty outreach program** (`whitePaper/attsi/`). Contains contact
packages, email drafts, review materials, and outreach strategy for each
faculty anchor. Named contacts have non-anonymized directories; anonymized
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

## Licensing & Strategy

### Lysogeny Protocol

**Area denial through open prior art.** By publishing under AGPL-3.0, every
innovation becomes prior art that prevents patents. Named after bacteriophage
lysogeny — the viral DNA integrates into the host genome and persists.

### scyBorg

The **ecosystem licensing standard**: AGPL-3.0-only for code, ORC for
standards/specs, CC-BY-SA for documentation. All primals and springs follow
this triple license.

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
| **baseCamp** | Cross-spring paper program (18 papers) |
| **Paper parity** | Spring output matches published figures within named tolerance |
| **Absorption** | Spring replaces local math with barraCuda canonical version |
| **Delegation** | Primal routes work to another primal via IPC |
| **Handoff** | Session continuity document in wateringHole |
| **Fossil record** | Archived handoffs — the project's geological history |
| **Lysogeny** | Area denial through open AGPL prior art |
