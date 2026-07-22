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
> ---
>
> **CONVERGENCE RULE — READ THIS FIRST**
>
> **eastGate owns primalSpring's codebase.** You are a benchmark runner,
> not a code evolver. Follow this workflow strictly:
>
> 1. **DO NOT** make significant code changes to primalSpring on this gate.
> 2. **Minimal edits only**: config tweaks, tolerance values, benchmark
>    harness scripts, and results files are acceptable local changes.
> 3. **Report back**: File findings, benchmark results, and any proposed
>    code changes as a **handoff** in `infra/wateringHole/handoffs/`.
>    The eastGate primalSpring team will integrate and evolve the code.
> 4. **Pull, don't push code**: `git pull` regularly to stay converged
>    with eastGate's latest. Push only handoffs, results, and config to
>    `wateringHole`. Do NOT push primalSpring code changes from this gate.
> 5. If you discover a bug or need a code fix, document it in your handoff
>    with file path, line, and proposed fix — eastGate will ship it.
>
> This ensures all primalSpring instances converge on the same codebase
> and eastGate remains the single source of truth for code evolution.
>
> ---
>
> **Your mission**: Validate the Tower Atomic stack on this gate and
> execute the parity benchmark against flockGate through golgiBody.
>
> **Context**: Tower Atomic is the sovereign transport composition replacing
> WireGuard. primalSpring on eastGate already shipped the structural
> validation scenario (`tower-atomic-parity`, 21/21 checks GREEN,
> commit `1ab0bfea`). This gate needs to run the **live benchmark**.
>
> **What to do (in order)**:
>
> 1. Review the standard blurb dimensions above (code quality, architecture,
>    tests, debt, sovereignty) — **audit and report** findings in your
>    handoff. Do not fix primalSpring code directly; report to eastGate.
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
> 6. Execute LAN parity benchmark (sporeGate ↔ eastGate — same backbone):
>    - sporeGate (.2) ↔ eastGate (.5) on 1Gbps backbone LAN
>    - Throughput: target ≥ WG baseline * 0.8x
>    - Latency: target ≤ WG baseline * 1.5x
>    - Compare against WireGuard LAN baseline on same link
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
> LAN benchmark (READY NOW — same backbone):
>   sporeGate (.2) ←→ Tower relay ←→ eastGate (.5)
> ```
>
> Upstream primals consumed: bearDog (crypto/BTSP), songBird (transport/mesh),
> skunkBat (protocol negotiation/IDS)
> Key standards: `TOWER_ATOMIC_CONVERGENCE.md`, `COMPOSITION_ROUTING_STANDARD.md`,
> `BTSP_PROTOCOL_STANDARD.md`
> First milestone: WAN parity benchmark results filed as handoff in wateringHole

### primalSpring on flockGate (WAN peer — Tower Atomic benchmark)

> **primalSpring** — Wave 150v, Tower Atomic parity benchmark spin-up.
> Gate assignment: flockGate (10.13.37.6, WAN zone, esotericWebb V22 LIVE)
> Purpose: Run Tower Atomic parity benchmarks as the **WAN peer**.
> flockGate is already running Tower Atomic (role=tower in mesh topology).
> It serves as the far-side WAN endpoint, reached through golgiBody's
> TURN relay from backbone gates.
>
> ---
>
> **CONVERGENCE RULE — READ THIS FIRST**
>
> **eastGate owns primalSpring's codebase.** You are a benchmark runner,
> not a code evolver. Follow this workflow strictly:
>
> 1. **DO NOT** make significant code changes to primalSpring on this gate.
> 2. **Minimal edits only**: config tweaks, tolerance values, benchmark
>    harness scripts, and results files are acceptable local changes.
> 3. **Report back**: File findings, benchmark results, and any proposed
>    code changes as a **handoff** in `infra/wateringHole/handoffs/`.
>    The eastGate primalSpring team will integrate and evolve the code.
> 4. **Pull, don't push code**: `git pull` regularly to stay converged
>    with eastGate's latest. Push only handoffs, results, and config to
>    `wateringHole`. Do NOT push primalSpring code changes from this gate.
> 5. If you discover a bug or need a code fix, document it in your handoff
>    with file path, line, and proposed fix — eastGate will ship it.
>
> This ensures all primalSpring instances converge on the same codebase
> and eastGate remains the single source of truth for code evolution.
>
> ---
>
> **Your mission**: Validate the Tower Atomic stack on this gate and
> participate as the WAN peer in the parity benchmark against sporeGate
> through golgiBody.
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
>    tests, debt, sovereignty) — **audit and report** findings in your
>    handoff. Do not fix primalSpring code directly; report to eastGate.
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
> First milestone: WAN peer ready, responding to benchmark probes from sporeGate.
> File handoff with findings to wateringHole — eastGate integrates code.

---

## Ready-to-Paste: Tower Atomic Blockers (Wave 150v)

### songBird on eastGate — TURN relay deploy + benchmark harness (P0/P1)

> **songBird** — Wave 150v, Tower Atomic parity unblock.
> Gate assignment: eastGate (code evolution) + golgiBody (TURN relay deploy)
> Purpose: Unblock the Tower Atomic WAN parity benchmark by delivering the
> two items both sporeGate and flockGate teams independently identified as
> blocking: **TURN relay deployment** and **benchmark harness**.
>
> ---
>
> **PARITY PHILOSOPHY**
>
> Initial goal is **WireGuard parity** — any tractable first solution that
> matches WG performance. WireGuard has years of development time on us.
> We aim to match first, then evolve past. Parity is the floor, not the
> ceiling. Targets are relative to WG baseline (not absolute thresholds),
> since physical path characteristics vary by topology.
>
> ---
>
> **Context**: sporeGate and flockGate teams both completed Wave 150v audits.
> Both gates have Tower Atomic 3/3 LIVE (bearDog, songBird, skunkBat — running
> since Jul 16). WireGuard baselines are measured:
>
> | Path | WG RTT |
> |------|--------|
> | sporeGate → golgiBody | 38ms |
> | flockGate → golgiBody | 31ms |
> | sporeGate → flockGate (2-hop) | 68ms |
>
> Both teams are GREEN/READY and waiting on these two deliverables.
>
> **What to do (in order)**:
>
> 1. Review the standard blurb dimensions above (code quality, architecture,
>    tests, debt, sovereignty) — audit and fix what you can.
>
> 2. Read the AARs from both benchmark gates:
>    - `aars/PRIMALSPRING_SPOREGATE_AAR_150v.md`
>    - `aars/FLOCKGATE_WAVE150v_TOWER_PARITY_AAR.md`
>    - `TOWER_ATOMIC_CONVERGENCE.md` (songBird's own convergence brief)
>
> 3. **P0 — Deploy TURN relay on golgiBody**:
>    - songBird's `songbird-lineage-relay` crate has `relay_server/`,
>      `relay.rs`, `relay_handler.rs`, `relay_protocol.rs` — code complete
>    - Create/verify systemd unit for `songbird relay` on golgiBody VPS
>      (157.230.3.183, accessible via `ssh golgiBody` or WG 10.13.37.1)
>    - Relay must accept connections from sporeGate (.2) and flockGate (.6)
>    - Relay must route traffic between peers (TURN-style)
>    - Verify relay is reachable from both gates after deploy
>    - If the relay binary is not in plasmidBin depot, build and stage it
>
> 4. **P1 — Build benchmark harness** (`songbird benchmark` CLI):
>    - The CLI already has a `tower.rs` command module in `songbird-cli`
>    - Needs subcommands:
>      ```
>      songbird benchmark --mode tower-atomic --peer <gate> --duration <secs>
>      songbird benchmark --mode wireguard --peer <gate> --duration <secs>
>      songbird benchmark --compare --output <path.json>
>      ```
>    - Metrics to capture per the parity spec:
>      - Throughput (iperf3-equivalent through relay stack)
>      - Latency (RTT through relay)
>      - Connection setup time (connect to first byte)
>      - Reconnect time (mesh re-discovery after link drop)
>      - CPU idle/saturated
>    - Output should be structured JSON for primalSpring to consume
>      in the `s_tower_atomic_parity_live` scenario
>    - A simple initial implementation is fine — we evolve from parity
>      toward exceeding WG. First working version unblocks everything.
>
> 5. **P2 — Flaky test** (from gate AARs):
>    - `s_depot_architecture_coverage` in primalSpring passes alone but
>      fails in full parallel suite — resource contention. Investigate
>      and fix if tractable (may need test mutex or isolated temp dir).
>      This is a primalSpring issue but songBird team may encounter it.
>
> **Topology** (what you're enabling):
> ```
> WAN benchmark (both gates READY, waiting on relay):
>   sporeGate (.2) ←→ golgiBody TURN (.1) ←→ flockGate (.6)
>                     ↑ YOU DEPLOY THIS
>
> LAN benchmark (READY NOW — same backbone):
>   sporeGate (.2) ←→ Tower relay ←→ eastGate (.5)
> ```
>
> **WAN latency targets** (relative to WG baseline, not absolute):
>
> | Metric | WG Baseline (measured) | Tower Target |
> |--------|----------------------|--------------|
> | RTT to golgiBody | 31-38ms | ≤ WG * 1.5x |
> | RTT end-to-end (2-hop) | 66-68ms | ≤ WG * 1.5x |
> | Throughput | TBD (iperf3) | ≥ WG * 0.8x |
> | Connection setup | ~50ms | ≤500ms |
> | Reconnect | instant | ≤2s |
>
> Upstream primals consumed: bearDog (crypto/BTSP), skunkBat (protocol)
> Key standards: `TOWER_ATOMIC_CONVERGENCE.md`, `COMPOSITION_ROUTING_STANDARD.md`
> First milestone: TURN relay live on golgiBody + `songbird benchmark` producing
> a JSON report. Once delivered, sporeGate drives benchmark, flockGate responds,
> primalSpring on eastGate ships the Live-tier scenario.
