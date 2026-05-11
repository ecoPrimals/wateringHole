# ludoSpring V63 — Upstream Handoff for Primals & Spring Teams

**From:** ludoSpring V63 (May 11, 2026)
**To:** All primal teams, all spring teams, primalSpring, projectNUCLEUS, foundation
**Quality gate:** 854 tests, zero clippy, zero fmt diffs, zero unsafe, zero `unreachable!` in production, all SPDX headers

---

## Executive Summary

ludoSpring is at V63 with deep debt fully resolved. 100 experiments validated and
fossilized. 8 validation scenarios absorbed into UniBin. Tier 4 IPC-first defaults
active (`default = ["ipc"]`). Composition parity at 130/141 (92.2%). Foundation
Threads 9 (Gaming) and 10 (Provenance/Economics) seeded. 13/15 primal gaps resolved.

This handoff documents: (1) composition patterns we've validated that other springs
should absorb, (2) what we need from upstream primals, (3) what we've learned about
NUCLEUS deployment via biomeOS neuralAPI.

---

## Part 1: Composition Patterns for Ecosystem Adoption

### Pattern 1: `crate::math` Dual-Path Module (Tier 4 IPC-first)

When `barracuda` is `optional = true` and IPC-first, math primitives need inline
fallbacks. ludoSpring's `crate::math` module provides both paths:

```rust
pub fn sigmoid(x: f64) -> f64 {
    #[cfg(feature = "local")]
    { barracuda::activations::sigmoid(x) }
    #[cfg(not(feature = "local"))]
    { 1.0 / (1.0 + (-x).exp()) }
}
```

Key: the inline fallback must match barraCuda's implementation exactly. We verified
LCG constants, bit extraction (`>> 33` for `u32::MAX`), and sigmoid precision
against barraCuda's Rust implementation and Python baselines.

**Adopt in:** hotSpring, healthSpring, wetSpring — any spring that calls `barracuda::`
math functions and needs IPC-only builds.

### Pattern 2: skunkBat Rust IPC Module

Five typed functions wrapping `security.audit_log` over JSON-RPC:

- `audit_log(event_type, source, details)` — general audit event
- `audit_certification(session_id, details)` — certification events
- `audit_session(session_id, details)` — session lifecycle events
- `audit_validation(session_id, details)` — validation events
- `query_audit_trail(filter)` — query past events

Source strings use `crate::niche::NICHE_NAME` (not hardcoded). All calls use
`is_skip_error` for graceful degradation when skunkBat is unavailable.

**Adopt in:** hotSpring, groundSpring — springs that only have skunkBat in deploy
graphs but no actual IPC module.

### Pattern 3: Constant-Invariant Tests for Tolerances

Every tolerance module should have `#[cfg(test)]` tests that validate:
- Positivity of all tolerance constants
- Ordering relationships (e.g., `STRICT < DEFAULT < LOOSE`)
- Formula derivations (e.g., Fitts MT = a + b * log2(2D/W))
- Range constraints (e.g., EMA alpha in (0, 1])
- Divisor safety (e.g., `NUMERICAL_FLOOR > f64::EPSILON`)

This catches constant drift at compile time. ludoSpring has 29 such tests across
8 modules.

### Pattern 4: Per-Primal IPC Module Structure

```
barracuda/src/ipc/
├── mod.rs           # Module declarations
├── methods.rs       # Method constants (10 domain modules)
├── envelope.rs      # JSON-RPC wire types
├── rpc_client.rs    # Shared UDS transport
├── server.rs        # Server loop
├── discovery/       # Capability-based primal discovery
├── handlers/        # Three-tier dispatch (lifecycle→infra→science)
│   ├── lifecycle.rs
│   ├── science.rs
│   ├── delegation.rs
│   ├── mcp.rs
│   ├── neural.rs
│   └── gpu.rs
├── btsp.rs          # BearDog Trust Protocol
├── coralreef.rs     # Shader compilation client
├── neural_bridge.rs # biomeOS neuralAPI client
├── squirrel.rs      # AI inference client
├── skunkbat.rs      # Audit logging client
├── toadstool.rs     # Compute dispatch client
├── composition.rs   # Proto-nucleate validation
└── params.rs        # Method parameter types
```

**Key:** per-primal typed clients with capability-based discovery, not identity-based.
All IPC calls use `is_skip_error` for graceful degradation.

### Pattern 5: Pure Composition Deployment Model

ludoSpring has NO spring binary in plasmidBin. Instead:
- `ludospring_cell.toml` defines a 12-node NUCLEUS cell graph
- biomeOS deploys the graph: barraCuda for math, petalTongue for viz, Squirrel for AI,
  provenance trio for DAG/certs/attribution, Tower Atomic for trust
- The `ludospring` binary is the validation/certification tool only

**Relevant for:** Any spring that doesn't need its own deployed process — just a
composition of existing primals.

---

## Part 2: What We Need From Upstream Primals

### coralReef (GAP-01: PARTIAL)

**Need:** Production-ready `shader.compile.wgsl` endpoint. ludoSpring has a typed
client (`ipc/coralreef.rs`) but production GPU paths still use `include_str!` WGSL
+ toadStool dispatch. When coralReef can compile WGSL reliably, we can eliminate
embedded shaders entirely.

### toadStool (GAP-02: PARTIAL)

**Need:** Hardware-adaptive `compute.dispatch.submit` that selects substrate based on
workload characteristics. Current: ludoSpring always submits to "best available". Want:
toadStool to accept compute profiles (latency-sensitive for game tick, throughput for
batch noise) and route accordingly.

### rhizoCrypt + loamSpine (GAP-04/05: PARTIAL)

**Need:** Live IPC validation of DAG vertex creation and certificate minting. Typed
clients exist; unit tests verify wire format. Live validation against deployed trio
awaits stable trio binaries in plasmidBin.

### biomeOS (GAP-14: LOW)

**Need:** Deploy graph validation feedback — when `composition.deploy(graph)` is
called, return structured validation (missing nodes, capability mismatches) rather
than silent degradation.

### skunkBat (JH-5 Phase 3)

**Waiting on:** Phase 3 cross-primal audit forwarding → rhizoCrypt DAG + sweetGrass
braid. When this ships, ludoSpring gets provenance-anchored audit trails for free.

---

## Part 3: NUCLEUS Deployment via biomeOS neuralAPI

### What We Learned

1. **`composition.status` is the health heartbeat.** biomeOS v3.51 exposes
   `{ active_users, primal_health, resource_pressure }`. ludoSpring absorbs this
   into the `ludospring status` command and the `lifecycle.status` handler.

2. **`method.register` enables dynamic capability advertisement.** At startup,
   ludoSpring calls `method.register` with all 28 `game.*` methods + metadata.
   This is how biomeOS builds the live capability graph.

3. **The neuralAPI call pattern is: discover → register → serve → deregister.**
   `NeuralBridge` handles all four phases. On SIGTERM, `capability.deregister`
   cleans up the graph. Other springs should adopt this lifecycle.

4. **Deploy graphs must declare `fallback = "skip"` on optional deps.** ludoSpring's
   cell graph marks all trio nodes and viz nodes as skip-on-unavailable. This allows
   the composition to function in degraded mode (no provenance, no viz) when those
   primals aren't deployed.

5. **The 60Hz tick budget is easily met over IPC.** `game.tick` composite handler
   runs in ~0.6ms (budget: 16.6ms). IPC round-trip overhead is negligible for
   science computation. Real-time game rendering would need different architecture,
   but validation and science serve fine over IPC.

6. **Foundation seeding is a geological layer.** Contributing validated data sources
   and targets to `sporeGarden/foundation` makes a spring's science load-bearing.
   Other springs that validate against real public datasets (NCBI, UniProt, FAO, PDB)
   should seed their domain threads.

### Deploy Graph Structure (Reference)

```toml
# ludospring_cell.toml (12 nodes)
[nodes.barracuda]     # math/science (required)
[nodes.toadstool]     # compute dispatch (required)
[nodes.beardog]       # crypto (required)
[nodes.songbird]      # discovery (required)
[nodes.petaltongue]   # visualization (fallback = "skip")
[nodes.squirrel]      # AI inference (fallback = "skip")
[nodes.rhizocrypt]    # provenance DAG (fallback = "skip")
[nodes.loamspine]     # certificates (fallback = "skip")
[nodes.sweetgrass]    # attribution (fallback = "skip")
[nodes.nestgate]      # storage (fallback = "skip")
[nodes.biomeos]       # orchestration (required)
[nodes.skunkbat]      # audit (fallback = "skip")
```

---

## Part 4: For Sibling Springs

### Patterns to Absorb

| Pattern | Source | Benefit |
|---------|--------|---------|
| `crate::math` dual-path | `barracuda/src/math.rs` | IPC-only builds without math library linkage |
| skunkBat Rust IPC | `barracuda/src/ipc/skunkbat.rs` | Typed audit logging with graceful degradation |
| Constant-invariant tests | `barracuda/src/tolerances/*.rs` | Compile-time tolerance validation |
| `NicheDependency` table | `barracuda/src/niche.rs` | Capability-first discovery with hint fallback |
| `is_skip_error` degradation | `barracuda/src/ipc/envelope.rs` | Graceful degradation when primals are unavailable |
| biomeOS v3.51 absorption | `barracuda/src/biomeos/mod.rs` | `composition.status` + `method.register` |

### Tier 4 Checklist

For any spring targeting Tier 4 IPC-first:
- [ ] `barracuda` in `Cargo.toml` has `optional = true`
- [ ] `default` features do NOT include `local`
- [ ] All `barracuda::` imports behind `#[cfg(feature = "local")]`
- [ ] Inline math fallbacks match barraCuda exactly (test with Python baselines)
- [ ] `cargo build` (default) produces IPC-only binary
- [ ] `cargo build --features local` links library
- [ ] All tests pass in both modes

### For projectNUCLEUS

Two workloads ready: `ludospring-game-validation.toml` and `ludospring-composition-parity.toml`.
ludoSpring follows the "composed" model — no binary in plasmidBin. The UniBin
(`ludospring validate`) can run locally but the deployment model is biomeOS composing
the cell graph from plasmidBin primal binaries.

### For foundation

- Thread 9 (Gaming/Creative): 14 data sources, 13 validation targets
- Thread 10 (Provenance/Economics): 10 data sources, 11 validation targets
- All targets have quantitative expected values, tolerances, and spring check references

---

## Remaining Evolution Targets

| Item | Severity | Blocked On |
|------|----------|-----------|
| GAP-01: coralReef sovereign shader compilation | Medium | coralReef maturity |
| GAP-02: toadStool hardware-adaptive dispatch | Medium | toadStool v0.5+ |
| GAP-04/05: rhizoCrypt/loamSpine live validation | Low | Stable trio in plasmidBin |
| GAP-14: biomeOS deploy graph validation feedback | Low | biomeOS evolution |
| Composition parity: 11 low-severity checks | Low | Various upstream fixes |
| Python baseline notebooks (.ipynb) | Stadial | Presentational, not functional |
| LTEE paper reproductions | Stadial | Ecosystem-wide target |
