# Team Startup Blurb — Standard Template

**Wave**: 147b | **From**: eastGate overwatch
**Purpose**: Paste this (with project-specific section filled in) when spinning up
a new team session for any primal, garden, protist, or spring.

---

## The Blurb

> Review `specs/` and our codebase and docs at root, and the docs found at our
> parent `ecoPrimals/infra/wateringHole/` for inter-primal discussions and
> standards. Start with `wateringHole/STANDARDS_AND_EXPECTATIONS.md`,
> `fossilRecord/wave150s_standards/ECOBIN_ARCHITECTURE_STANDARD.md`, `protocols/SEMANTIC_METHOD_NAMING_STANDARD.md`,
> `foundations/LICENSING_AND_COPYLEFT.md`, and `handoffs/ECOSYSTEM_BLURB.md` for current
> ecosystem posture. Review primalSpring guidance in wateringHole/ as it
> enables parallel evolution.
>
> Audit the following dimensions — report status and fix what you can:
>
> **Code Quality**
> - Linting: `cargo clippy --all-targets -- -W clippy::pedantic -W clippy::nursery` (0 warnings)
> - Formatting: `cargo fmt --check` (clean)
> - Doc checks: `cargo doc --no-deps` (0 warnings, all public items documented)
> - Idiomatic Rust: no bad patterns, no unnecessary `unsafe`, no `unwrap()` in
>   non-test code — use `ErrorContextExt` or `anyhow`/`thiserror`
> - File size: 1,000 lines max per file — split if over
> - Compile efficiency: lean dependencies, clean module graph, no circular deps
> - Test speed: tests should run in seconds, not minutes — slow compiles are
>   often junk dependencies
>
> **Architecture Compliance**
> - JSON-RPC AND tarpc first: all IPC is `json-rpc` wire + `tarpc` service trait.
>   No raw TCP, no HTTP REST between primals.
> - uniBin and ecoBin compliant: single-binary architecture per
>   `fossilRecord/wave150s_standards/ECOBIN_ARCHITECTURE_STANDARD.md`
> - Semantic method naming per `protocols/SEMANTIC_METHOD_NAMING_STANDARD.md`
> - Zero-copy where possible: `Bytes`, `&[u8]`, avoid unnecessary clones
> - Silicon Atheism: platform differences use trait-based abstraction
>   (see `petal-tongue-platform` reference), NOT `#[cfg]` exclusion
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
> - Pure Rust crypto where possible (see `fossilRecord/wave150s_standards/PURE_RUST_CRYPTO_PURITY_STANDARD.md`)
>
> **What have we not completed?** Report all gaps, mocks standing in for real
> integrations, TODOs, deep debt, and upstream blockers. Prioritize as P0/P1/P2.

---

## Project-Specific Context (fill in per team)

### For primals (existing, debt sweep)

> **[PRIMAL_NAME]** — Wave 147b context:
> [Paste specific action items from ECOSYSTEM_BLURB.md here]
> [Paste any relevant handoff content here]

### For gardens (new spin-up)

> **[GARDEN_NAME]** — New garden, Wave 147b spin-up.
> Gate assignment: [GATE_NAME]
> Purpose: [one-line purpose]
> Upstream primals consumed: [list which primals this garden depends on]
> Key standards: [list relevant wateringHole standards]
> First milestone: [what "done" looks like for the first deliverable]

---

## Ready-to-Paste: Garden Spin-Up Contexts

### lithoSpore / pseudoSpore (ironGate)

> **lithoSpore** — New garden, Wave 147b spin-up.
> Gate assignment: ironGate (co-located with ABG work, science validation)
> Purpose: Portability layer — makes any ecoPrimals work USB-deployable and
> recreatable from a pseudoSpore seed file. A pseudoSpore is a content-addressed
> manifest that can reconstruct an entire working environment from depot binaries
> + git refs + config.
> Upstream primals consumed: plasmidBin (depot), rhizoCrypt (content hashing),
> loamSpine (manifest merkle), sweetGrass (provenance), bearDog (signing)
> Key standards: ECOBIN_ARCHITECTURE, DISTRIBUTED_COVALENT_DEPLOYMENT,
> PROVENANCE_TRIO_INTEGRATION_GUIDE
> First milestone: `pseudospore pack` + `pseudospore unpack` round-trip for
> initioChem (first consumer). A USB stick with a pseudoSpore file should
> recreate a working initioChem environment on any gate.

### esotericWebb (flockGate)

> **esotericWebb** — New garden, Wave 147b spin-up.
> Gate assignment: flockGate (co-located with footPrint, UI/interaction layer)
> Purpose: Living game state — the interactive UI layer that surfaces ecosystem
> state as an explorable experience. Consumes petalTongue for rendering,
> primals for live data, and presents the ecosystem as a "living organism"
> the operator can navigate and interact with.
> Upstream primals consumed: petalTongue (web UI), songBird (mesh data),
> nestGate (state), footPrint (GIS visualization)
> Key standards: COMPOSITION_ROUTING, BONDING_MODEL, K_DERM_TOPOLOGY
> First milestone: Static site on primals.eco/webb/ that renders live
> ecosystem topology (gates, bonds, health) from songBird mesh data.

### projectFOUNDATION (TBD)

> **projectFOUNDATION** — New garden, Wave 147b spin-up.
> Gate assignment: TBD (candidate: ironGate for science data, or eastGate
> for overwatch integration)
> Purpose: Data/knowledge foundation layer — thread lineage, validation
> evidence, structured knowledge that all other gardens and primals can
> query. The "memory" of the ecosystem.
> Upstream primals consumed: nestGate (CAS), rhizoCrypt (content identity),
> loamSpine (merkle structure), sweetGrass (provenance/attribution)
> Key standards: PROVENANCE_TRIO_INTEGRATION_GUIDE, CONTEXT_BRAID,
> CAPABILITY_BASED_DISCOVERY
> First milestone: Thread lineage store — given a conversation/session ID,
> reconstruct the full decision tree with provenance links to code commits,
> test results, and handoff artifacts.

### initioChem (ironGate)

> **initioChem** — New garden, Wave 147b spin-up.
> Gate assignment: ironGate (co-located with ABG, JupyterHub, science compute)
> Purpose: Computational chemistry product — first to prove the pseudoSpore
> pattern. Sovereign alternative to cloud chemistry compute.
> Upstream primals consumed: nestGate (state), hotSpring (compute dispatch),
> plasmidBin (depot), lithoSpore (pseudoSpore packaging)
> Key standards: ECOBIN_ARCHITECTURE, COMPOSITION_ROUTING,
> DISTRIBUTED_COVALENT_DEPLOYMENT
> First milestone: initioChem pseudoSpore that can be unpacked on any gate
> with the right hardware and run a chemistry job end-to-end.
