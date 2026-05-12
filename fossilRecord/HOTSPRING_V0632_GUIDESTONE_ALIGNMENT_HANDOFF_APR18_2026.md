# hotSpring v0.6.32 — guideStone Alignment Handoff

**Date:** April 18, 2026
**From:** hotSpring
**To:** primalSpring auditors, barraCuda team, toadStool team, BearDog team, sibling springs, biomeOS team
**License:** AGPL-3.0-or-later

---

## Summary

hotSpring is the first downstream spring to implement the guideStone Composition
Standard (primalSpring v0.9.15). The `hotspring_guidestone` binary is a unified
Level 5 certified artifact that validates bare guideStone properties (no primals
needed) and probes NUCLEUS IPC parity using the `primalspring::composition` API.

**Validation Ladder Position:** Level 5 — guideStone CERTIFIED (reference
implementation). 166 binaries, 64/64 validation suites, 985 lib tests.

---

## What Changed

### 1. `hotspring_guidestone` Binary Created

**Path:** `barracuda/src/bin/hotspring_guidestone.rs`

Unified guideStone binary with two operating modes:

**Bare guideStone** (always runs, no primals needed):
- Property 1 — **Deterministic**: SEMF produces identical results on re-evaluation
- Property 2 — **Reference-Traceable**: SLY4_PARAMS, niche name, LOCAL_CAPABILITIES populated
- Property 3 — **Self-Verifying**: CHECKSUMS and deny.toml present and well-formed
- Property 4 — **Environment-Agnostic**: No network, no GPU required for bare checks
- Property 5 — **Tolerance-Documented**: Named constants defined, ordered correctly

**NUCLEUS additive** (when primals are deployed):
- Scalar parity via `stats.mean` (plaquette mean, observable mean)
- Vector parity via `tensor.matmul` (SU(3) identity, field arithmetic)
- SEMF end-to-end (local B.E. → barraCuda IPC round-trip)
- Crypto provenance witness (BLAKE3 hash determinism via BearDog)
- GPU compute dispatch (identity shader via toadStool)

**Exit codes:** 0 = all pass, 1 = failure, 2 = bare-only (no primals discovered)

### 2. primalSpring Composition API Adoption

Added `primalspring = { path = "../../primalSpring/ecoPrimal" }` to `barracuda/Cargo.toml`.

APIs used:
- `CompositionContext::from_live_discovery_with_fallback()`
- `validate_parity()` — scalar IPC parity with tolerance
- `validate_parity_vec()` — vector IPC parity
- `validate_liveness()` — capability domain discovery + health
- `primalspring::tolerances` — IPC_ROUND_TRIP_TOL, EXACT_PARITY_TOL, etc.
- `primalspring::validation::ValidationResult` — standard harness

hotSpring's own `NucleusContext` retained for the server binary and Tier 2
validators. The two contexts coexist — `primalspring::composition` is the
guideStone path; `NucleusContext` is the legacy path.

### 3. downstream_manifest.toml Updated

Added guideStone metadata to `primalSpring/graphs/downstream/downstream_manifest.toml`:

```toml
[hotspring]
guidestone_binary = "hotspring_guidestone"
guidestone_readiness = 5
guidestone_properties = { deterministic = true, traceable = true, self_verifying = true, env_agnostic = true, tolerance_documented = true }
```

### 4. validate_all.rs Updated

Suite count incremented from 63 to 64. `hotspring_guidestone` registered as a
Suite entry in the orchestrator.

### 5. Documentation Alignment

- `README.md` — guideStone Status section, 166/64 counts
- `CHANGELOG.md` — guideStone alignment session entry
- `EXPERIMENT_INDEX.md` — guideStone session + binary entry
- `docs/PRIMAL_GAPS.md` — GAP-HS-032 (binary unification) and GAP-HS-033 (API adoption) resolved
- `graphs/README.md` — guideStone Deployment section
- `whitePaper/README.md` — guideStone certification counts
- `whitePaper/baseCamp/README.md` — Python→Rust→Primal→guideStone validation arc
- `specs/README.md` — guideStone-aligned status

---

## Patterns Learned (for primalSpring/sibling springs)

### Pattern 1: Bare + Additive Decomposition

The guideStone binary naturally decomposes into two phases:

1. **Bare** — validates intrinsic properties using only local crate APIs. Always
   runs, produces meaningful results even in CI without primals. This is the
   "can I trust this deployable?" gate.

2. **Additive** — validates IPC parity using `primalspring::composition`. Only
   runs when primals are discovered. This is the "does this deployable compose
   correctly with NUCLEUS?" gate.

Exit code 2 (bare-only) is distinct from 0 (full pass) and 1 (failure). CI can
gate on `exit_code != 1` to accept both bare and full certification.

### Pattern 2: Domain Science as Parity Target

hotSpring validates physics (SEMF binding energy, SU(3) matrix products,
plaquette observables) rather than synthetic test vectors. This means:

- Tolerance values come from physics (measurement precision, numerical stability)
- Failures surface real IPC degradation, not synthetic edge cases
- The same baselines used in Python→Rust validation are reused for Rust→IPC validation

**Recommendation for sibling springs:** Use your domain's core computation as
the parity target. neuralSpring should use inference accuracy. wetSpring should
use phylogenetic distance. The tolerance constants should reflect the domain's
inherent precision requirements.

### Pattern 3: primalSpring Composition API is Sufficient

The `CompositionContext` + `validate_parity` + `validate_liveness` API surface
covers the common cases:

- Discovery with fallback (no crash if primals not running)
- Scalar parity with tolerance
- Vector parity with tolerance
- Capability-domain routing (no primal name hardcoding)
- Liveness checks per domain

**What was not needed:** Direct socket management, custom JSON-RPC framing,
manual `serde_json` response parsing for parity checks. The composition API
handles all of that.

**What might be needed for advanced springs:** Custom IPC methods not covered
by `validate_parity` (e.g., streaming results, multi-step pipelines). hotSpring's
own `NucleusContext` still handles these cases. Consider adding a
`validate_streaming_parity` helper to `primalspring::composition`.

### Pattern 4: Tolerance Hierarchy

hotSpring validates that tolerance constants are ordered correctly:

```
EXACT_PARITY_TOL < DETERMINISTIC_FLOAT_TOL < CPU_GPU_PARITY_TOL <= IPC_ROUND_TRIP_TOL
```

This ordering is a guideStone property (Property 5) and ensures IPC tolerance
is always the loosest bound. Springs should document and validate this ordering.

---

## Gaps Found During Alignment

### For primalSpring Team

1. **`validate_streaming_parity`** — The composition API handles scalar and vector
   parity well. Multi-step streaming pipelines (e.g., HMC trajectory → force →
   gauge update) need a higher-level helper. Currently hotSpring handles this via
   `NucleusContext` directly.

2. **`CompositionContext::call` error typing** — The `is_connection_error()`
   method on IPC errors is essential for graceful degradation. Document this
   pattern prominently — springs need to distinguish "primal not running" from
   "primal returned wrong answer."

3. **guideStone property validation helpers** — Properties 1-5 are validated
   with ad-hoc checks in each spring. Consider adding
   `primalspring::guidestone::validate_deterministic()` etc. as reusable helpers
   that springs can call with a closure.

### For barraCuda Team

1. **`stats.mean` as parity anchor** — hotSpring uses `stats.mean` as the primary
   scalar parity target because it's simple, deterministic, and available. More
   complex statistical methods (std_dev, correlation) should have documented
   precision guarantees for IPC round-trip.

2. **`tensor.matmul` precision contract** — The identity matrix test passes trivially.
   Non-trivial matrix products (e.g., [[1,2],[3,4]] * [[5,6],[7,8]]) need
   documented precision for f64 IPC round-trip. Current tolerance
   (IPC_ROUND_TRIP_TOL) covers it, but the contract should be explicit.

### For BearDog Team

1. **`crypto.hash` method stability** — hotSpring uses `crypto.hash` with algorithm
   parameter "blake3" for provenance witnesses. The method signature and output
   format (base64 string) should be stable. Any changes break guideStone crypto
   validation.

### For toadStool Team

1. **`compute.dispatch` contract** — The identity_f64 shader dispatch is used as
   a liveness check. The response format (JSON object with keys) should be stable.
   Document the minimal response contract for guideStone validation.

### For biomeOS Team

1. **guideStone as deployment gate** — `hotspring_guidestone` produces exit code 0
   only when all 5 properties pass AND NUCLEUS IPC parity confirms. biomeOS can
   use this as a pre-deployment health check: run the guideStone binary after
   spawning primals, gate service readiness on exit code 0.

2. **neuralAPI integration** — The guideStone binary is a CLI tool today. For
   neuralAPI deployment, consider a `guidestone.validate` JSON-RPC method that
   runs the same checks and returns structured results instead of exit codes.

---

## Active Primal Gaps (for upstream teams)

These gaps remain open in `docs/PRIMAL_GAPS.md`:

| ID | Description | Primal | Severity |
|----|-------------|--------|----------|
| GAP-HS-001 | Squirrel E2E validation | Squirrel | Low |
| GAP-HS-002 | by_capability discovery migration | biomeOS | Low |
| GAP-HS-005 | IONIC-RUNTIME cross-family GPU lease | BearDog/Songbird | Medium |
| GAP-HS-006 | BTSP-BARRACUDA-WIRE session crypto | barraCuda/BearDog | Medium |
| GAP-HS-027 | TensorSession adoption (deferred) | barraCuda | Low |
| GAP-HS-028 | LIME/ILDG zero-copy I/O | hotSpring | Low |
| GAP-HS-029 | Fork isolation pattern not standardized | coralReef/toadStool | Low |
| GAP-HS-030 | Ember absorption into toadStool | toadStool/coralReef | Medium |
| GAP-HS-031 | K80 VFIO legacy group EBUSY | coralReef | Medium |

---

## Three-Tier Validation Arc Summary

```
Tier 1: Python baselines (86/86 checks)
  → Tier 2: Rust CPU/GPU reproduction (985 tests, 64/64 suites)
    → Tier 3: NUCLEUS primal composition (hotspring_guidestone, guideStone Level 5)
```

Each tier validates the one below it:
- Rust results must match Python within documented tolerances
- IPC results must match Rust within IPC_ROUND_TRIP_TOL
- guideStone bare properties must hold without any external dependencies

This is the reference implementation for the guideStone Composition Standard.

---

## Files Changed

| File | Change |
|------|--------|
| `barracuda/Cargo.toml` | Added `primalspring` dep, `hotspring_guidestone` binary |
| `barracuda/src/bin/hotspring_guidestone.rs` | NEW — unified guideStone binary |
| `barracuda/src/bin/validate_all.rs` | Suite count 63→64, added guideStone entry |
| `README.md` | guideStone Status section, updated counts |
| `CHANGELOG.md` | guideStone alignment session |
| `EXPERIMENT_INDEX.md` | guideStone binary + session entry |
| `docs/PRIMAL_GAPS.md` | GAP-HS-032, GAP-HS-033 resolved |
| `graphs/README.md` | guideStone Deployment section |
| `whitePaper/README.md` | guideStone counts |
| `whitePaper/baseCamp/README.md` | Validation arc with guideStone tier |
| `specs/README.md` | guideStone status |
| `specs/PAPER_REVIEW_QUEUE.md` | 166 binaries |
| `specs/BARRACUDA_REQUIREMENTS.md` | 166 binaries, 64/64 suites |
| `barracuda/README.md` | 166 binaries, 64/64 suites |
| `barracuda/ABSORPTION_MANIFEST.md` | 166 bins, 64/64 suites |
| `whitePaper/METHODOLOGY.md` | 64/64 suites |
| `primalSpring/.../downstream_manifest.toml` | guideStone metadata |
| `wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` | guideStone Level 5 CERTIFIED |
| `wateringHole/ECOSYSTEM_EVOLUTION_CYCLE.md` | guideStone Level 5 CERTIFIED |
