# Team Startup Blurb — Wave 155f

**From**: eastGate overwatch
**Purpose**: Paste this into any new IDE session on any gate. It bootstraps
overwatch (syncs workspace to current), then serves as context for spinning
up individual code teams on that gate.

**Two-phase flow**:
1. **Overwatch phase**: Sync workspace from Forgejo, review state, report divergences
2. **Code team phase**: Paste again with team-specific section for individual primals

---

## PHASE 1: OVERWATCH — Sync This Gate

### What is ecoPrimals

ecoPrimals is a sovereign, AGPL-3.0 mesh operating system built in pure Rust.
13 primals (autonomous binaries) compose into **atomics**: Tower (security +
discovery + defense), Node (Tower + compute), Nest (Tower + storage +
provenance), and NUCLEUS (all 13). biomeOS orchestrates via a Neural API
with 26 signal graphs and semantic dispatch (`tower.health`, `node.compute`,
`nest.store`, etc.). All binaries ("genomeBins") are served from a single
depot on golgiBody (`https://depot.primals.eco`). Gates are physical machines
running Tower Atomic or higher compositions.

### Current State (Wave 155f)

**Posture**: Gate workload distribution. Teams deploying to dedicated gates.
Tower Atomic hardening first — Nest Atomic after Tower is stable.

| Fact | Value |
|------|-------|
| Wave | 155f |
| Primals | 15 (13 active + 2 dormant) |
| Tests | ~56K `#[test]` attributes across primals |
| BTSP | 13/13 — all primals ship bearDog ClientHello |
| Signal graphs | 26 (Tower 8, Nest 8, Node 3, Meta 5, Braid 2) |
| Depot | 39 genomeBins (13 primals × 3 targets) on golgiBody |
| Gates online | 7 (northGate + ironGate RustDesk degraded) |
| Jelly strings | 6/7 deployment automation items resolved |
| Forgejo | `ssh://git@git.primals.eco:2222/` — canonical remote |

### Gate-Team Assignments

| Gate | Teams / Primals | Hardware |
|------|-----------------|----------|
| **eastGate** | Overwatch, biomeOS, primalSpring, Tower stack, cellMembrane | Code hub, 10G SFP+ |
| **westGate** | petalTongue, squirrel, nestGate, rhizoCrypt, loamSpine, sweetGrass | 5x14TB HDD, Nest testbed |
| **strandGate** | toadStool, barraCuda, coralReef | Dual EPYC, RTX 3090 |
| **sporeGate** | Build authority, deployment foreman | Full NUCLEUS |
| **golgiBody** | Depot, Forgejo, enrollment, relay | Sole depot |

### Workspace Structure

The workspace is at `~/Development/ecoPrimals/` with this layout:

```
ecoPrimals/
├── primals/        # 15 autonomous Rust binaries
│   ├── bearDog          # Trust foundation — crypto, BTSP, FIDO2, beacon
│   ├── songBird         # Discovery — mesh, IPC, relay, drawbridge
│   ├── skunkBat         # Defense — anomaly detection, protocol audit
│   ├── nestGate         # Content-addressed storage — CAS, provenance
│   ├── rhizoCrypt       # Lineage DAG — content identity, federation
│   ├── loamSpine        # Certificate ledger — lifecycle, verification
│   ├── sweetGrass       # Attribution braids — provenance chains
│   ├── toadStool        # Compute dispatch — GPU, wgpu, hardware learning
│   ├── barraCuda        # Tensor math — linear algebra, GPU compute
│   ├── coralReef        # Shader compilation — WGSL, SPIR-V
│   ├── biomeOS          # Orchestrator — Neural API, signal graphs, NUCLEUS
│   ├── squirrel         # AI assistant — MCP, ML
│   ├── petalTongue      # Visualization — WASM, WebGL, rendering
│   ├── sourDough        # (dormant)
│   └── bingoCube        # (dormant)
├── gardens/        # Products and integration layers
│   ├── cellMembrane     # Deployment fabric — gate config, harvest, push
│   ├── esotericWebb     # Interactive ecosystem visualization
│   ├── lithoSpore       # USB portability / pseudoSpore packaging
│   ├── projectFOUNDATION # Knowledge foundation layer
│   ├── projectNUCLEUS   # Full NUCLEUS product
│   └── ...
├── springs/        # Science and domain applications
│   ├── primalSpring     # Scenario validation + benchmarks
│   ├── wetSpring        # Biodiversity + spectral analysis
│   ├── hotSpring        # Compute dispatch
│   └── ...
└── infra/          # Infrastructure and documentation
    ├── wateringHole      # Standards, handoffs, blurbs, AARs, wave coordination
    ├── plasmidBin        # Depot binaries + enrollment scripts
    ├── fossilRecord      # Archived/completed documentation
    ├── whitePaper        # Research papers, JOSS publication
    ├── benchScale        # Topology benchmarking
    └── ...
```

### Sync From Forgejo

Every repo has its canonical remote on Forgejo at `git.primals.eco:2222`.
Run this to sync all repos to current:

```bash
cd ~/Development/ecoPrimals
for d in primals/* gardens/* springs/* infra/*; do
  name=$(basename "$d")
  echo "=== $name ==="
  (cd "$d" && git fetch origin 2>/dev/null && git pull --rebase origin main 2>/dev/null) || echo "SKIP: $name"
done
```

If a repo is missing, clone it. The Forgejo orgs are:
- `ecoPrimals/` — primals + infra
- `sporeGarden/` — gardens
- `syntheticChemistry/` — springs + benchScale + agentReagents

Example: `git clone ssh://git@git.primals.eco:2222/ecoPrimals/bearDog.git primals/bearDog`

### After Sync: Review State

1. Read `infra/wateringHole/handoffs/ECOSYSTEM_BLURB.md` — this is the
   universal handoff with current posture, glacial goals, team status
2. Read `infra/wateringHole/wave.toml` — current wave ID and posture
3. Read `infra/wateringHole/ORTHOGONAL_DIMENSIONS_REVIEW.md` — 11 active + 10 fossilized dimensions
4. Check for dirty repos: `for d in primals/* gardens/* springs/* infra/*; do name=$(basename "$d"); dirty=$(cd "$d" 2>/dev/null && git status --porcelain 2>/dev/null | wc -l); [ "$dirty" -gt 0 ] && echo "$name: $dirty dirty files"; done`

### Report Divergences

After syncing, report any:
- Repos that failed to pull (merge conflicts, missing remotes)
- Uncommitted local changes that diverge from Forgejo
- Missing repos that exist on other gates
- Binary version mismatches vs golgiBody depot

File your report as `wateringHole/handoffs/[GATE_NAME]_WAVE155f_OVERWATCH_SYNC.md`

---

## PHASE 2: CODE TEAM SPIN-UP

After overwatch has synced the gate, paste this blurb again with the
team-specific section below for the primal(s) you're spinning up.

### Audit Dimensions (all teams)

> **Code Quality**
> - Linting: `cargo clippy --all-targets -- -W clippy::pedantic -W clippy::nursery` (0 warnings)
> - Formatting: `cargo fmt --check` (clean)
> - Doc checks: `cargo doc --no-deps` (0 warnings, all public items documented)
> - Idiomatic Rust: no `unwrap()` in non-test code — use `anyhow`/`thiserror`
> - File size: 800 lines max per file — split if over
> - Lean dependencies, clean module graph, no circular deps
>
> **Architecture Compliance**
> - JSON-RPC + tarpc: all IPC is JSON-RPC wire + tarpc service trait
> - genomeBin compliant: single-binary per `ECOBIN_ARCHITECTURE_STANDARD.md`
> - Semantic method naming per `SEMANTIC_METHOD_NAMING_STANDARD.md`
> - Platform-native transport: songBird universal-ipc (UDS/named pipes/TCP)
> - BTSP: must ship bearDog ClientHello for authenticated IPC
> - biomeOS neuralAPI: capabilities discoverable via `capability.call`
>
> **Test Coverage**
> - Target: 90% line coverage via `cargo llvm-cov` (report actual)
> - Required tiers: unit, integration, E2E scenario (via primalSpring)
>
> **Debt & Gaps**
> - Find all `todo!()`, `FIXME`, `HACK`, `TODO` markers
> - Hardcoded ports/names/constants → extract to config
> - Dead code, unused imports, stale feature flags
>
> **Sovereignty**
> - AGPL-3.0 / scyBorg triple-license
> - No telemetry, no cloud lock-in, pure Rust crypto
> - All genomeBins from `https://depot.primals.eco`

### Key Standards (in `infra/wateringHole/`)

| Standard | Path |
|----------|------|
| Architecture | `fossilRecord/wave150s_standards/ECOBIN_ARCHITECTURE_STANDARD.md` |
| Method naming | `protocols/SEMANTIC_METHOD_NAMING_STANDARD.md` |
| Licensing | `foundations/LICENSING_AND_COPYLEFT.md` |
| Expectations | `STANDARDS_AND_EXPECTATIONS.md` |
| Pure Rust crypto | `fossilRecord/wave150s_standards/PURE_RUST_CRYPTO_PURITY_STANDARD.md` |
| Ecosystem posture | `handoffs/ECOSYSTEM_BLURB.md` |

### Convergence Rule

> **eastGate owns the codebase.** Gate teams are deployment validators
> and workload runners. Follow this workflow:
>
> 1. **DO NOT** push code changes from your gate (except wateringHole handoffs).
> 2. **Minimal edits only**: config tweaks, environment-specific settings.
> 3. **Report back**: File findings as handoffs in `infra/wateringHole/handoffs/`.
> 4. **Pull from Forgejo regularly** to stay converged.
> 5. Bugs: document in handoff with file, line, proposed fix — eastGate ships it.

---

## Team-Specific Contexts (paste the relevant one)

### westGate: petalTongue

> **petalTongue** — Wave 155f, deploying to westGate.
> Version: 1.7.0 | Tests: 5,812 | Status: Stable
> Purpose: Visualization engine — WASM WebGL rendering pipeline.
> BTSP ClientHello: SHIPPED.
> Next work: Validate genomeBin deployment cycle on westGate. Confirm WASM
> pipeline runs correctly on westGate hardware. Report any platform divergences.
> Upstream: bearDog (BTSP), songBird (discovery)

### westGate: squirrel

> **squirrel** — Wave 155f, deploying to westGate.
> Version: 0.1.0 | Status: Stable
> Purpose: AI assistant with MCP integration.
> Next work: Deploy to westGate. Validate startup, capability registration
> with biomeOS neuralAPI. Report deployment divergences.
> Upstream: bearDog (BTSP), songBird (discovery), biomeOS (orchestration)

### westGate: Provenance Trio (nestGate + rhizoCrypt + loamSpine + sweetGrass)

> **Provenance Trio** — Wave 155f, deploying to westGate.
> Status: G3 CONVERGING — foundation shipped, IPC wiring deferred until Tower stable.
>
> | Primal | Version | Tests | Key Delivery |
> |--------|---------|-------|--------------|
> | nestGate | 0.5.0 | 13,236 | BTSP peer wiring, NTFS CAS safety |
> | rhizoCrypt | 0.14.17 | 1,456 | Cross-gate provenance chain, BTSP→DAG bridge |
> | loamSpine | 0.9.16 | 1,702 | Entry extraction, certificate.history RPC, delegated minting |
> | sweetGrass | 0.7.64 | 1,676 | CertificateRef on braids, cross-gate attribution, G3 READY |
>
> **Storage Tiering on westGate**: nestGate's CAS should be validated against
> the real hardware — 5x14TB HDD (cold), plus SSD/NVMe if available.
> Profile read/write latencies per tier. This data feeds Nest Atomic design.
>
> **Deferred G3 work** (after Tower stable): Wire IPC callers between primals —
> rhizoCrypt calls loamSpine.certificate.verify, sweetGrass links CertificateRef
> to loamSpine certificates, loamSpine validates MintingAuthority.
> See `aars/PROVENANCE_TRIO_G3_CONVERGENCE_155b_AAR.md` for convergence gaps.

### strandGate: Compute Trio (toadStool + barraCuda + coralReef)

> **Compute Trio** — Wave 155f, deploying to strandGate.
> Hardware: Dual EPYC + RTX 3090
>
> | Primal | Version | Tests | Key Delivery |
> |--------|---------|-------|--------------|
> | toadStool | 0.2.0 | 21,913 | S343 wgpu cross-platform GPU pipeline |
> | barraCuda | 0.4.0 | — | Tensor math, linear algebra |
> | coralReef | 0.2.0 | — | WGSL → SPIR-V shader compilation |
>
> Next work: Deploy all three. Validate `node.discover_hardware` signal graph —
> toadStool should discover the RTX 3090 via wgpu. Run `node.compute` and
> `node.dispatch` on real GPU workloads. Profile dispatch latency, shader
> compile times, tensor throughput. Report via handoff.
>
> See `handoffs/TOADSTOOL_S342_CROSS_PLATFORM_GPU_JUL27_2026.md` for GPU context.

### eastGate: biomeOS (reference — already running)

> **biomeOS** — Wave 155f, eastGate overwatch hub.
> Version: 0.1.0 | Tests: 8,522+ | Signal graphs: 26
> Active work: Live `tower.health` signal graph validation as teams deploy
> to gates. Monitor capability registration from deploying primals.
> See `config/capability_registry.toml` for the 19 atomic-tier translations.

### eastGate: primalSpring (reference — already running)

> **primalSpring** — Wave 155f, eastGate.
> 197 scenarios, all PASS. Calibrated for 13-gate mesh.
> Active work: Calibrate scenarios for distributed gate topology.
> Track deployment results from westGate and strandGate.

### Any gate: Tower Atomic stack (bearDog + songBird + skunkBat)

> **Tower Atomic** — required on every gate before anything else deploys.
> This is the trust foundation. Deploy first, validate, then deploy workloads.
>
> | Primal | Version | Role |
> |--------|---------|------|
> | bearDog | 0.9.0 | Crypto, BTSP auth, FIDO2, beacon genetics |
> | songBird | 0.2.1 | Discovery, mesh, IPC, relay, drawbridge |
> | skunkBat | 0.2.18 | Anomaly detection, protocol audit, ConnectivityAnomaly |
>
> Validate: `tower.health` should return `{ "status": "healthy" }` from songBird.
> `tower.mesh_status` returns mesh peer count and transport info.
> Fetch genomeBins from `https://depot.primals.eco`.

---

## K-Derm Three-Layer Model (reference)

```
OUTER MEMBRANE — Human access (RustDesk → relay.primals.eco)
PEPTIDOGLYCAN  — LAN/HPC topology fabric (NAT, DNS, switches, cabling)
INNER MEMBRANE — Primal IPC (WireGuard wg0 + songBird :7700 + BTSP)
```

northGate + ironGate have degraded outer membrane (RustDesk issues).
Peptidoglycan anchors: sporeGate (house1) + blueGate (house2).

---

## Glacial Goals (what we're building toward)

| # | Goal | Status |
|---|------|--------|
| G1 | Tower on Windows | FRONTLOADED |
| G7 | Gate enmeshment | FRONTLOADED — workload distribution validates pipeline |
| G6 | bearDog public (crates.io) | READY — final audit |
| G3 | Nest Atomic Phase 0 | AFTER TOWER STABLE — westGate testbed |
| G5 | Chimera (single-process Tower) | AFTER G1 |
| G8 | Plasmodium (multi-gate bonding) | AFTER G7 |
| G9 | JOSS publication | AFTER G3+G7 |
