# Team Startup Blurb — Standard Template

**Wave**: 155f | **From**: eastGate overwatch
**Purpose**: Paste this (with project-specific section filled in) when spinning up
a new team session for any primal, garden, protist, or spring.

---

## The Blurb

> Review `specs/` and our codebase and docs at root, and the docs found at our
> parent `ecoPrimals/infra/wateringHole/` for inter-primal discussions and
> standards. Start with `wateringHole/STANDARDS_AND_EXPECTATIONS.md`,
> `fossilRecord/wave150s_standards/ECOBIN_ARCHITECTURE_STANDARD.md`,
> `protocols/SEMANTIC_METHOD_NAMING_STANDARD.md`,
> `foundations/LICENSING_AND_COPYLEFT.md`, and `handoffs/ECOSYSTEM_BLURB.md`
> for current ecosystem posture. Review primalSpring guidance in wateringHole/
> as it enables parallel evolution.
>
> Audit the following dimensions — report status and fix what you can:
>
> **Code Quality**
> - Linting: `cargo clippy --all-targets -- -W clippy::pedantic -W clippy::nursery` (0 warnings)
> - Formatting: `cargo fmt --check` (clean)
> - Doc checks: `cargo doc --no-deps` (0 warnings, all public items documented)
> - Idiomatic Rust: no bad patterns, no unnecessary `unsafe`, no `unwrap()` in
>   non-test code — use `ErrorContextExt` or `anyhow`/`thiserror`
> - File size: 800 lines max per file — split if over
> - Compile efficiency: lean dependencies, clean module graph, no circular deps
> - Test speed: tests should run in seconds, not minutes
>
> **Architecture Compliance**
> - JSON-RPC + tarpc first: all IPC is JSON-RPC wire + tarpc service trait.
>   No raw TCP, no HTTP REST between primals.
> - genomeBin compliant: single-binary architecture per ECOBIN_ARCHITECTURE_STANDARD
> - Semantic method naming per SEMANTIC_METHOD_NAMING_STANDARD
> - Zero-copy where possible: `Bytes`, `&[u8]`, avoid unnecessary clones
> - Platform-native transport: songBird universal-ipc handles UDS (Linux),
>   named pipes (Windows), abstract sockets (Android), TCP (fallback).
>   Use trait-based abstraction, NOT `#[cfg]` exclusion.
> - BTSP 13/13: all primals must ship ClientHello for bearDog BTSP auth
>
> **Test Coverage**
> - Target: 90% line coverage via `cargo llvm-cov` (report actual)
> - Required tiers: unit, integration, E2E scenario (via primalSpring)
> - Chaos and fault injection where applicable
> - All mocks documented — no mock that hides a real integration gap
>
> **Debt & Gaps**
> - Find all `todo!()`, `unimplemented!()`, `FIXME`, `HACK`, `TODO` markers
> - Hardcoded ports, primal names, constants — extract to config or constants module
> - Dead code, unused imports, stale feature flags
> - Archive code/docs are for reference and fossil record — ignore them
>
> **Sovereignty & Licensing**
> - License: AGPL-3.0 / scyBorg triple-license (check `Cargo.toml` + `LICENSE`)
> - No telemetry, no third-party analytics, no cloud lock-in
> - Human dignity: no dark patterns, no surveillance, no data exfiltration
> - Pure Rust crypto (see `fossilRecord/wave150s_standards/PURE_RUST_CRYPTO_PURITY_STANDARD.md`)
> - All genomeBins from golgiBody depot (`https://depot.primals.eco`) — no local depots
>
> **biomeOS neuralAPI Integration**
> - 26 signal graphs define Tower/Nest/Node atomic behaviors
> - Your primal's capabilities should be discoverable via `capability.call`
> - Semantic dispatch: `tower.*`, `node.*`, `nest.*` methods route through signal graphs
> - See `config/capability_registry.toml` in biomeOS for translation table
>
> **What have we not completed?** Report all gaps, mocks standing in for real
> integrations, TODOs, deep debt, and upstream blockers. Prioritize as P0/P1/P2.

---

## Project-Specific Context (fill in per team)

### For primals (existing, evolving)

> **[PRIMAL_NAME]** — Wave 155f context:
> Gate assignment: [GATE_NAME]
> [Paste specific action items from ECOSYSTEM_BLURB.md here]
> [Paste any relevant handoff content here]

### For gardens (new spin-up)

> **[GARDEN_NAME]** — New garden, Wave 155f spin-up.
> Gate assignment: [GATE_NAME]
> Purpose: [one-line purpose]
> Upstream primals consumed: [list which primals this garden depends on]
> Key standards: [list relevant wateringHole standards]
> First milestone: [what "done" looks like for the first deliverable]

---

## Gate-Team Topology (Wave 155f)

```
eastGate — Overwatch + Orchestration
├── biomeOS (signal graph orchestrator)
├── primalSpring (scenario validation)
├── bearDog (trust foundation)
├── songBird (discovery + IPC)
├── skunkBat (defense)
└── cellMembrane (deployment fabric)

westGate — Nest Atomic + Data (DEPLOYING)
├── petalTongue (visualization + WASM)
├── squirrel (AI + MCP)
├── nestGate (content-addressed storage)
├── rhizoCrypt (lineage DAG)
├── loamSpine (certificate ledger)
└── sweetGrass (attribution braids)

strandGate — Compute Trio (DEPLOYING)
├── toadStool (compute dispatch)
├── barraCuda (tensor math)
└── coralReef (shader compilation)
```

---

## Ready-to-Paste: Gate Deployment Spin-Ups (Wave 155f)

### westGate — Nest + Data Primals + Storage Tiering

> **westGate team** — Wave 155f, gate deployment spin-up.
> Gate assignment: westGate (5x14TB HDD, house2)
> Purpose: Deploy petalTongue, squirrel, and the Provenance Trio (nestGate,
> rhizoCrypt, loamSpine, sweetGrass) to westGate. This gate becomes the
> **Nest Atomic testbed** with tiered storage profiling.
>
> **DEPLOYMENT VALIDATION**: This migration validates the full deployment
> pipeline. Report every divergence, failure, and unexpected behavior as
> it IS the test.
>
> **Storage Tiering Model** — westGate has real hardware variance to profile:
> ```
> TIER 0 — AMD L3/L1 cache (if AMD CPU)      ← compute-adjacent, nanosecond
> TIER 1 — RAM (tmpfs / ramdisk)              ← volatile, microsecond
> TIER 2 — NVMe (if present)                  ← fast persistent, sub-millisecond
> TIER 3 — 2.5" SSD (SATA, can be added)      ← mid persistent, millisecond
> TIER 4 — HDD (5x14TB ZFS array)             ← cold/bulk, multi-millisecond
> ```
>
> **Sequencing**:
> 1. Enroll via `tower.enroll` (or `gate-enroll.sh` if pre-Tower)
> 2. Bootstrap Tower Atomic (bearDog + songBird + skunkBat)
> 3. Validate `tower.health` and `tower.mesh_status` respond correctly
> 4. Fetch genomeBins from `https://depot.primals.eco` for assigned primals
> 5. Deploy petalTongue + squirrel — validate they start, register capabilities
> 6. Deploy nestGate — configure CAS against HDD array, profile storage tiers
> 7. Deploy rhizoCrypt + loamSpine + sweetGrass — validate Provenance Trio IPC
>
> **After Tower stable on this gate**: Begin Nest Atomic Phase 1 validation —
> `nest.store` → `nest.retrieve` → `nest.verify` across tiers. Profile CAS
> latency per tier. Feed results back to primalSpring for scenarios.
>
> Upstream: bearDog (trust), songBird (discovery), golgiBody (depot)
> Report to: `wateringHole/handoffs/` — file as `WESTGATE_WAVE155f_DEPLOYMENT_AAR.md`

### strandGate — Compute Trio Deployment

> **strandGate team** — Wave 155f, gate deployment spin-up.
> Gate assignment: strandGate (Dual EPYC, RTX 3090, house2)
> Purpose: Deploy the compute trio (toadStool, barraCuda, coralReef) to
> strandGate. This gate validates **Node Atomic** on real GPU hardware.
>
> **DEPLOYMENT VALIDATION**: This migration validates the full deployment
> pipeline. Report every divergence, failure, and unexpected behavior.
>
> **Hardware**:
> - Dual EPYC CPUs — heavy multi-threaded compute
> - RTX 3090 — CUDA + Vulkan compute, shader compilation
> - Purpose-built for `node.compute` and `node.dispatch` signal graphs
>
> **Sequencing**:
> 1. Enroll via `tower.enroll` (or `gate-enroll.sh` if pre-Tower)
> 2. Bootstrap Tower Atomic (bearDog + songBird + skunkBat)
> 3. Validate `tower.health` responds correctly
> 4. Fetch genomeBins from `https://depot.primals.eco` for compute primals
> 5. Deploy toadStool — validate GPU discovery (`node.discover_hardware`),
>    confirm wgpu backend (Vulkan on Linux, DX12 on Windows)
> 6. Deploy barraCuda — validate tensor operations on RTX 3090
> 7. Deploy coralReef — validate WGSL → SPIR-V shader compilation
>
> **After Tower stable on this gate**: Begin Node Atomic validation —
> `node.compute` and `node.dispatch` signal graphs on real GPU workloads.
> Profile GPU dispatch latency, shader compile times, tensor throughput.
>
> Upstream: bearDog (trust), songBird (discovery), golgiBody (depot),
> toadStool (wgpu GPU, S343 cross-platform pipeline)
> Report to: `wateringHole/handoffs/` — file as `STRANDGATE_WAVE155f_DEPLOYMENT_AAR.md`

### eastGate — Overwatch + Orchestration (reference)

> **eastGate** — Wave 155f, overwatch hub.
> Gate assignment: eastGate (code hub, 10G SFP+ to backbone)
> Teams hosted: biomeOS, primalSpring, Tower Atomic stack (bearDog, songBird,
> skunkBat), cellMembrane
>
> **Role**: Coordination hub. Code evolution happens here. Other gates deploy
> genomeBins from golgiBody and report back via wateringHole handoffs.
>
> **Active work**:
> - biomeOS: live `tower.health` signal graph validation across gates
> - primalSpring: calibrate scenarios for distributed gate topology
> - bearDog: G6 public flip audit
> - songBird: `tower.health` + `tower.mesh_status` facade validation
> - skunkBat: `ConnectivityAnomaly` monitoring during gate migrations
> - cellMembrane: J6 `gate.configure` / `gate.apply` for declarative service config

---

## Ready-to-Paste: Garden Spin-Up Contexts (updated Wave 155f)

### lithoSpore / pseudoSpore (ironGate — when RustDesk fixed)

> **lithoSpore** — Garden, Wave 155f.
> Gate assignment: ironGate (4x HDD, JupyterHub, science validation)
> Purpose: Portability layer — makes any ecoPrimals work USB-deployable and
> recreatable from a pseudoSpore seed file. Content-addressed manifest that
> reconstructs working environments from depot binaries + git refs + config.
> Upstream: plasmidBin (depot), rhizoCrypt (content hashing),
> loamSpine (manifest merkle), sweetGrass (provenance), bearDog (signing)
> First milestone: `pseudospore pack` + `pseudospore unpack` round-trip

### esotericWebb (flockGate)

> **esotericWebb** — Garden, Wave 155f.
> Gate assignment: flockGate (co-located with footPrint, UI/interaction layer)
> Purpose: Living game state — interactive UI layer surfacing ecosystem state
> as an explorable experience via petalTongue rendering + primal live data.
> Upstream: petalTongue (web UI, moving to westGate), songBird (mesh data),
> nestGate (state, moving to westGate), footPrint (GIS visualization)
> First milestone: webb.primals.eco renders live gate topology from songBird mesh

### projectFOUNDATION (eastGate)

> **projectFOUNDATION** — Garden, Wave 155f.
> Gate assignment: eastGate (overwatch integration)
> Purpose: Data/knowledge foundation layer — thread lineage, validation
> evidence, structured knowledge. The "memory" of the ecosystem.
> Upstream: nestGate (CAS), rhizoCrypt (content identity),
> loamSpine (merkle), sweetGrass (provenance/attribution)
> First milestone: Thread lineage store — reconstruct decision trees with
> provenance links to code commits, test results, and handoff artifacts.

---

## Convergence Rule (for all non-eastGate gates)

> **eastGate owns the codebase.** Gate teams are deployment validators and
> workload runners, not code evolvers. Follow this workflow:
>
> 1. **DO NOT** make significant code changes on your gate.
> 2. **Minimal edits only**: config tweaks, environment-specific settings.
> 3. **Report back**: File findings, deployment results, and proposed fixes
>    as a **handoff** in `infra/wateringHole/handoffs/`.
>    eastGate integrates and evolves the code.
> 4. **Pull, don't push code**: `git pull` from Forgejo regularly.
>    Push only handoffs, results, and config to `wateringHole`.
> 5. Bugs and fixes: document in your handoff with file path, line, and
>    proposed fix — eastGate ships it.
>
> This ensures all gates converge on the same codebase. eastGate is the
> single source of truth for code evolution. golgiBody (Forgejo) is the
> canonical remote.
