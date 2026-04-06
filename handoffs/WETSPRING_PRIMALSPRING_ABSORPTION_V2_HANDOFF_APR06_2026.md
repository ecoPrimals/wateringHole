# wetSpring ← primalSpring Absorption v2 — Handoff

**Date**: 2026-04-06
**Author**: wetSpring science pipeline
**Previous**: `WETSPRING_SCIENCE_NUCLEUS_GAPS_HANDOFF_APR06_2026.md`
**Scope**: Absorption of primalSpring feedback + remaining ecosystem debt

---

## What Was Absorbed

### 1. Epoch-Based Circuit Breaker (provenance.rs)

**Status**: Implemented and tested.

`try_tier2` and `try_tier3` now use an atomic circuit breaker that opens after
3 consecutive failures and stays open for 30 seconds. Prevents the facade from
hammering the provenance trio when partially reachable. Pattern follows
primalSpring's recommendation.

- `TRIO_FAILURES` / `TRIO_BREAKER_OPENED` — `AtomicU64` counters
- `trio_breaker_open()` — checks cooldown and auto-resets
- `breaker_status()` — exposed via `/api/v1/system/composition` for diagnostics

### 2. Canonical Composition Health Methods

**Status**: Implemented and tested.

wetSpring now responds to all 5 canonical composition health methods:

| Method | Atomic | Probes |
|--------|--------|--------|
| `composition.science_health` | wetSpring-specific | IPC + math + GPU |
| `composition.tower_health` | Tower | BearDog + Songbird via `capability.discover` |
| `composition.node_health` | Node | BearDog + ToadStool |
| `composition.nest_health` | Nest | BearDog + NestGate |
| `composition.nucleus_health` | NUCLEUS | All 7 primals aggregated |

Each returns structured JSON with per-component status, matching the shape
primalSpring validators expect in `nucleus_atomics_validate.toml`.

### 3. Deploy Graph Structural Validation

**Status**: Implemented with 4 tests passing.

New `facade::graph_validate` module (`graph_validate.rs`) parses the deploy
graph TOML and validates:

- Every node has `by_capability` (required for capability-first discovery)
- No duplicate node names
- Dependency closure (all `depends_on` targets exist)
- Order consistency (dependencies have lower order)
- Capability domain uniqueness warnings

Validation result is included in the `/api/v1/system/composition` response.
Added `toml = "0.8"` as optional dep behind `facade` feature (pure Rust, ecoBin).

### 4. Deploy Graph Capability Alignment

**Status**: Converged with primalSpring's `wetspring_deploy.toml`.

Changes to `wetspring_science_nucleus.toml`:

| Field | Before | After |
|-------|--------|-------|
| biomeOS name | `biomeos` | `biomeos_neural_api` |
| beardog binary | `beardog_primal` | `beardog` |
| songbird binary | `songbird_primal` | `songbird` |
| nestgate binary | `nestgate_primal` | `nestgate` |
| toadstool binary | `toadstool_primal` | `toadstool` |
| rhizocrypt binary | `rhizocrypt_primal` | `rhizocrypt` |
| loamspine binary | `loamspine_primal` | `loamspine` |
| sweetgrass binary | `sweetgrass_primal` | `sweetgrass` |
| sweetgrass by_capability | `semantic_provenance` | `attribution` |
| wetspring by_capability | `ecology` | `biology` |
| songbird capabilities | `discovery.find_primals`, `mesh.announce` | Added `net.discovery`, `net.mesh` |
| beardog capabilities | — | Added `crypto.blake3_hash` |
| toadstool capabilities | `dispatch.gpu/npu/cpu` | Added `compute.dispatch.submit`, `shader.dispatch`, `ember.list` |
| rhizocrypt capabilities | `dag.create_session` etc. | Added `dag.session.create`, `dag.session.list` |
| loamspine capabilities | `commit.session` etc. | Added `entry.append`, `ledger.status` |
| sweetgrass capabilities | `provenance.create_braid` etc. | Added `attribution.claim`, `attribution.resolve` |

**Strategy**: wetSpring's graph now lists *both* naming conventions (primalSpring's
canonical names and our original names) for capabilities. This is forward-compatible:
when the canonical capability registry is published, we can prune the aliases.

---

## Remaining Debt — Handoff to Ecosystem

### DEBT-01: Bonding Policy as Rust Types

**Owner**: wetSpring + wateringHole
**Priority**: Medium
**Status**: Scaffolded (JSON only)

`bonding_metadata.json` declares `Covalent` and `Ionic` bond types, but these
are not represented as Rust types with validation. primalSpring recommends
runtime bonding policy types (`BondType`, `TrustModel`, `BondingPolicy`) that
can enforce access rules at the IPC level.

**Action**: wateringHole should publish canonical Rust types in a shared crate
(candidate: `biomeos-types` or `ecoPrimals-contracts`). wetSpring will absorb
once published.

### DEBT-02: Canonical Capability Registry

**Owner**: primalSpring + wateringHole
**Priority**: High (blocks ecosystem convergence)
**Status**: No registry exists

Capability method names diverge between springs. primalSpring uses
`dag.session.create` where wetSpring (and actual rhizoCrypt) uses
`dag.create_session`. Neither side knows who is canonical.

**Action**: wateringHole should publish `capability_registry.toml` as the
single source of truth for all capability method names. Every spring's deploy
graph should validate against it. wetSpring's `graph_validate` module is ready
to consume this once published.

### DEBT-03: Neural API Method Routing

**Owner**: biomeOS
**Priority**: High (blocks Tier 2/3 provenance)
**Status**: Documented in previous handoff

wetSpring calls `provenance.begin`, `provenance.record`, `provenance.complete`
directly on the Neural API socket. biomeOS currently only routes via
`capability.call` wrappers. Either:

- (a) biomeOS adds top-level route sugar for common patterns, or
- (b) all springs switch to `capability.call` wrappers exclusively

This must be decided ecosystem-wide. wetSpring has both patterns ready.

### DEBT-04: Structured Experiment Harness

**Owner**: primalSpring
**Priority**: Low (wetSpring has 300+ validation binaries already)
**Status**: Not started

primalSpring recommends a structured experiment runner with `run()`, `verify()`,
`report()` contract. wetSpring's current pattern (standalone validation binaries
with exit codes) works but doesn't feed results back to primalSpring's experiment
registry.

**Action**: primalSpring should publish the experiment trait/contract. wetSpring
will wrap existing binaries.

### DEBT-05: plasmidBin Binary Name Verification

**Owner**: plasmidBin + wateringHole
**Priority**: Medium
**Status**: Unverified

The deploy graph now uses short binary names (`beardog`, `songbird`, etc.) matching
primalSpring's convention. These must match the actual binary names in
`plasmidBin/primals/`. If plasmidBin uses different names (e.g., `beardog_primal`),
one side must converge.

**Action**: plasmidBin should publish a manifest of canonical binary names.

### DEBT-06: Ionic Contract Negotiation Protocol

**Owner**: primalSpring + wateringHole
**Priority**: Low (late-stage feature)
**Status**: Metadata scaffolded, protocol undefined

`bonding_metadata.json` declares that wetSpring supports Ionic bonds, but there
is no protocol for cross-family bond negotiation, metering, or consent. This is
needed before any external spring can consume wetSpring data via ionic contracts.

**Action**: primalSpring should define the ionic negotiation protocol (likely a
JSON-RPC handshake with BearDog signatures). wetSpring will implement.

---

## Files Changed in This Absorption

| File | Change |
|------|--------|
| `barracuda/src/facade/provenance.rs` | Circuit breaker + `breaker_status()` |
| `barracuda/src/facade/graph_validate.rs` | **NEW** — structural graph validator |
| `barracuda/src/facade/mod.rs` | Added `graph_validate` module |
| `barracuda/src/facade/routes.rs` | Composition endpoint: graph validation + breaker status |
| `barracuda/src/ipc/handlers/mod.rs` | 4 canonical health handlers + `probe_capability()` |
| `barracuda/src/ipc/dispatch.rs` | 4 new composition health dispatch arms |
| `barracuda/Cargo.toml` | Added `toml = "0.8"` behind facade feature |
| `graphs/wetspring_science_nucleus.toml` | Full capability alignment with primalSpring |
