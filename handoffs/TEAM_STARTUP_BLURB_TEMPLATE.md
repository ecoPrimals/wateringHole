# Team Startup Blurb — Standard Template

**Wave**: 150v | **From**: eastGate overwatch
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

---

## Ready-to-Paste: Tower Atomic Parity — primalSpring Spin-Ups (Wave 150v)

### primalSpring on sporeGate (backbone LAN peer — Tower Atomic benchmark)

> **primalSpring** — Wave 150v, Tower Atomic parity benchmark spin-up.
> Gate assignment: sporeGate (10.13.37.2, Backbone zone, 13/13 NUCLEUS LIVE)
> Purpose: Run Tower Atomic parity benchmarks as the **backbone LAN peer**.
> sporeGate is a NUCLEUS builder with full primal stack — it serves as one
> endpoint of the LAN benchmark pair (sporeGate ↔ eastGate on backbone).
>
> **Your mission**: Deploy and validate the Tower Atomic stack (bearDog +
> songBird + skunkBat) on this gate, then execute the parity benchmark
> against eastGate over the LAN backbone.
>
> **Context**: Tower Atomic is the sovereign transport composition replacing
> WireGuard. primalSpring on eastGate already shipped the structural
> validation scenario (`tower-atomic-parity`, 21/21 checks GREEN,
> commit `1ab0bfea`). This gate needs to run the **live benchmark**.
>
> **What to do (in order)**:
>
> 1. Review the standard blurb dimensions above (code quality, architecture,
>    tests, debt, sovereignty) — audit and fix what you can.
>
> 2. Read the Tower Atomic convergence brief at
>    `primals/songBird/infra/wateringHole/TOWER_ATOMIC_CONVERGENCE.md`
>    and the primalSpring AAR at
>    `infra/wateringHole/handoffs/PRIMALSPRING_WAVE150u_TOWER_PARITY_AAR.md`
>
> 3. Verify Tower Atomic primals are running on this gate:
>    - bearDog: `security.sock` — BTSP handshake + negotiate
>    - songBird: `songbird.sock` / `:7780` drawbridge — mesh.relay + mesh.connect
>    - skunkBat: via songBird BTSP dispatch — audit/anomaly/threat
>    If not running, deploy from plasmidBin depot.
>
> 4. Run the structural scenario to confirm local registry matches:
>    ```
>    cargo test --lib -- tower_atomic_parity
>    ```
>
> 5. Execute WAN parity benchmark through golgiBody TURN relay:
>    - sporeGate (.2) → golgiBody TURN (.1) → flockGate (.6)
>    - Throughput: target >50 Mbps (iperf3-equivalent through Tower relay)
>    - Latency: target <50ms RTT through Tower relay
>    - Compare against WireGuard WAN baseline on same path
>    - Report: `TOWER_WAN_PARITY_RESULTS.md` in wateringHole handoffs
>
> 6. When ironGate comes back online, execute LAN parity benchmark:
>    - sporeGate (.2) ↔ eastGate (.5) on 1Gbps backbone
>    - Throughput: target >800 Mbps
>    - Latency: target <5ms RTT
>    - Compare against WireGuard LAN baseline
>    - Report: `TOWER_LAN_PARITY_RESULTS.md` in wateringHole handoffs
>
> **Parity spec** (must meet or exceed WG baseline):
>
> | Metric | WG Baseline | Tower Target |
> |--------|-------------|--------------|
> | LAN throughput | ~900 Mbps | ≥800 Mbps |
> | LAN latency | ~0.3ms | <5ms |
> | WAN throughput | ~50 Mbps | ≥50 Mbps |
> | WAN latency | ~30ms | <50ms |
> | Connection setup | ~50ms | ≤500ms |
> | Reconnect | instant | ≤2s |
>
> **Topology**:
> ```
> WAN benchmark (NOW):
>   sporeGate (.2) ←→ golgiBody TURN (.1) ←→ flockGate (.6)
>
> LAN benchmark (when ironGate returns):
>   sporeGate (.2) ←→ Tower relay ←→ eastGate (.5)
> ```
>
> Upstream primals consumed: bearDog (crypto/BTSP), songBird (transport/mesh),
> skunkBat (protocol negotiation/IDS)
> Key standards: `TOWER_ATOMIC_CONVERGENCE.md`, `COMPOSITION_ROUTING_STANDARD.md`,
> `BTSP_PROTOCOL_STANDARD.md`
> First milestone: WAN parity benchmark results filed as handoff

### primalSpring on flockGate (WAN peer — Tower Atomic benchmark)

> **primalSpring** — Wave 150v, Tower Atomic parity benchmark spin-up.
> Gate assignment: flockGate (10.13.37.6, WAN zone, esotericWebb V22 LIVE)
> Purpose: Run Tower Atomic parity benchmarks as the **WAN peer**.
> flockGate is already running Tower Atomic (role=tower in mesh topology).
> It serves as the far-side WAN endpoint, reached through golgiBody's
> TURN relay from backbone gates.
>
> **Your mission**: Deploy and validate the Tower Atomic stack on this gate,
> then participate as the WAN peer in the parity benchmark against
> sporeGate through golgiBody.
>
> **Context**: Tower Atomic is the sovereign transport composition replacing
> WireGuard. primalSpring on eastGate already shipped the structural
> validation scenario (`tower-atomic-parity`, 21/21 checks GREEN,
> commit `1ab0bfea`). ironGate is temporarily offline, so we are doing
> **WAN-first testing** — flockGate is the WAN peer, golgiBody is the
> TURN relay hub.
>
> **What to do (in order)**:
>
> 1. Review the standard blurb dimensions above (code quality, architecture,
>    tests, debt, sovereignty) — audit and fix what you can.
>
> 2. Read the Tower Atomic convergence brief at
>    `primals/songBird/infra/wateringHole/TOWER_ATOMIC_CONVERGENCE.md`
>    and the primalSpring AAR at
>    `infra/wateringHole/handoffs/PRIMALSPRING_WAVE150u_TOWER_PARITY_AAR.md`
>
> 3. Verify Tower Atomic primals are running on this gate:
>    - bearDog: `security.sock` — BTSP handshake + negotiate
>    - songBird: `songbird.sock` / `:7780` drawbridge — mesh.relay + mesh.connect
>    - skunkBat: via songBird BTSP dispatch
>    flockGate should already have role=tower. Verify with:
>    ```
>    songbird mesh.peers  # should show flockGate as tower role
>    ```
>    If not running, deploy from plasmidBin depot.
>
> 4. Run the structural scenario to confirm local registry matches:
>    ```
>    cargo test --lib -- tower_atomic_parity
>    ```
>
> 5. Participate as WAN peer in parity benchmark:
>    - flockGate (.6) ← golgiBody TURN (.1) ← sporeGate (.2)
>    - Accept incoming Tower relay connections from sporeGate
>    - Run iperf3-equivalent server mode for throughput measurement
>    - Provide latency echo for RTT measurement
>    - Also run same tests over WireGuard for baseline comparison
>
> 6. Coordinate with sporeGate team — they drive the benchmark, you
>    serve as the far endpoint. Results go to sporeGate's report.
>
> **Additionally**: flockGate runs esotericWebb (webb.primals.eco). While
> here, confirm esotericWebb V22 is healthy and no regressions from
> Tower Atomic deployment. esotericWebb should not conflict — it runs
> on different ports and uses songBird's drawbridge for its own IPC.
>
> **Topology**:
> ```
> WAN benchmark:
>   sporeGate (.2) ←→ golgiBody TURN (.1) ←→ flockGate (.6) ← YOU ARE HERE
>                     vs.
>   sporeGate (.2) ←→ golgiBody WG hub (.1) ←→ flockGate (.6)
> ```
>
> Upstream primals consumed: bearDog (crypto/BTSP), songBird (transport/mesh),
> skunkBat (protocol negotiation/IDS)
> Key standards: `TOWER_ATOMIC_CONVERGENCE.md`, `COMPOSITION_ROUTING_STANDARD.md`,
> `BTSP_PROTOCOL_STANDARD.md`
> First milestone: WAN peer ready, responding to benchmark probes from sporeGate
