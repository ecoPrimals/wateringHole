# Spring Evolution Issues — biomeOS Integration Surface

**Purpose**: Track issues, patterns, and evolution opportunities discovered by Springs
that require coordination from biomeOS, ToadStool, or cross-primal teams.
**Last Updated**: March 10, 2026
**Contributing Springs**: airSpring v0.7.5, neuralSpring V92/S139, wetSpring V103, groundSpring V100, hotSpring v0.6.24, healthSpring V3

---

## How to Use This Document

Springs add issues here when they discover integration gaps, patterns that
need standardization, or evolution opportunities that cross primal boundaries.
biomeOS and ToadStool teams review and act. Issues follow the lifecycle:

```
OPEN → ACKNOWLEDGED → IN_PROGRESS → RESOLVED (or WONT_FIX with rationale)
```

---

## Open Issues

### ISSUE-001: Ecology Capability Domain Missing from Registry

**Reporter**: airSpring (V025)
**Affects**: biomeOS, all Springs that produce/consume ecological data
**Priority**: P1 — blocks Neural API integration for agriculture/ecology

**Problem**: biomeOS's `capability_registry.toml` defines domains for security
(BearDog), network (Songbird), storage (NestGate), compute (ToadStool),
ai (Squirrel), and science (wetSpring). There is no **ecology** domain for
agricultural and environmental capabilities.

**Proposed fix**: Add `[domains.ecology]` with 20+ translations. Full spec in
`airSpring/specs/BIOMEOS_CAPABILITIES.md`. Includes:
- 7 ET₀ methods (PM, PT, Hargreaves, Thornthwaite, Makkink, Turc, Hamon)
- Water balance, Richards PDE, Van Genuchten
- Yield response, GDD, dual Kc
- Pedotransfer functions
- IoT irrigation scheduling

**Status**: OPEN

---

### ISSUE-002: Neural API Client Needs Synchronous Alternative

**Reporter**: airSpring (V025)
**Affects**: All Springs, metalForge dispatch layers
**Priority**: P2

**Problem**: `neural-api-client` in biomeOS requires tokio (async runtime).
Springs that use synchronous validation harnesses (all current validation
binaries) can't use it without adding tokio to their dependency tree.
airSpring implemented a zero-dep sync client in `metalForge/forge/src/neural.rs`
using `std::os::unix::net::UnixStream`.

**Proposed fix**: Ship a `neural-api-client-sync` crate alongside the async
one, or make async optional behind a feature flag.

**Evidence**: airSpring's sync client works for all validation scenarios.
The pattern is:
```rust
let bridge = NeuralBridge::discover()?; // 4-tier socket resolution
let result = bridge.capability_call("ecology", "et0_pm", &args)?;
```

**Status**: OPEN

---

### ISSUE-003: `capability.call` Parameter Format Inconsistency

**Reporter**: airSpring (V025)
**Affects**: biomeOS, all capability callers
**Priority**: P1

**Problem**: Three different parameter formats exist for `capability.call`:

1. **Spec** (`NEURAL_API_ROUTING_SPECIFICATION.md`):
   `{"capability": "crypto.generate_keypair", "args": {...}}`

2. **Handler** (`capability.rs`):
   `{"capability": "crypto", "operation": "generate_keypair", "args": {...}}`

3. **beacon_genetics** (`NeuralApiCapabilityCaller`):
   `{"capability": "beacon.encrypt", "params": {...}}`

**Proposed fix**: Standardize on format 2 (separate `capability` + `operation`)
as primary, with format 1 (dotted) as sugar that the handler splits on `.`.
Document in the semantic naming standard.

**Status**: OPEN

---

### ISSUE-004: Cross-Primal Pipeline Graph Execution Not Tested End-to-End

**Reporter**: airSpring (V025)
**Affects**: biomeOS graph engine
**Priority**: P2

**Problem**: airSpring created two deployment graphs:
- `airspring_eco_pipeline.toml` (weather → ET₀ → water balance → yield)
- `cross_primal_soil_microbiome.toml` (airSpring → wetSpring → ToadStool)

These follow the `science_pipeline.toml` format but haven't been executed
through biomeOS's graph engine. The graph engine needs to support:
- `capability_call` operations routing to Spring-registered capabilities
- Cross-Spring sequential dependencies (airSpring output → wetSpring input)
- Variable interpolation for dynamic parameters (`${LATITUDE}`, etc.)

**Proposed fix**: Deploy on Eastgate tower node and run end-to-end. Create
a minimal test graph that validates one `capability.call` round-trip.

**Status**: OPEN

---

### ISSUE-005: Safe UID Discovery Pattern

**Reporter**: airSpring (V025)
**Affects**: All primals, metalForge, biomeOS socket resolution
**Priority**: P3

**Problem**: Socket path resolution at tier 3 (`/run/user/{uid}/biomeos/`)
requires knowing the current UID. `libc::getuid()` is `unsafe` in Rust.
airSpring discovered a safe alternative: read `/proc/self/status` and parse
the `Uid:` line.

**Proposed fix**: Standardize on `/proc/self/status` parsing for Linux,
with `libc::getuid()` as a documented fallback for non-procfs platforms.
Consider adding this to `biomeos-types::SystemPaths`.

**Evidence**: airSpring's implementation in `metalForge/forge/src/neural.rs`
(`uid_from_runtime_dir()`) works on Linux without any `unsafe` blocks.

**Status**: OPEN

---

### ISSUE-006: NPU Convergence — Multiple Springs Proposing Integration

**Reporter**: airSpring (V024), wetSpring, groundSpring
**Affects**: ToadStool, metalForge dispatch
**Priority**: P2

**Problem**: airSpring (AKD1000 crop stress classifier), wetSpring
(proposed biosensor inference), and groundSpring (proposed noise filtering)
all want NPU integration. Each is implementing its own discovery and dispatch.
airSpring's `metalForge` has a working `probe_npus()` + `SubstrateKind::Npu`
+ capability-based dispatch, but this isn't shared.

**Proposed fix**: Absorb the NPU substrate model into ToadStool's device
layer. Key primitives:
- Device discovery via `/dev/akida*` scan
- `Capability::QuantizedInference { bits: 8 }`
- `Capability::BatchInference { max_batch: N }`
- Dispatch routing (GPU > NPU > CPU)

**Evidence**: airSpring Exp 028+029 (35+32+28 = 95 checks) validate the
pattern on live AKD1000 hardware.

**Status**: OPEN

---

### ISSUE-007: Springs as biomeOS Science Providers — Registration Pattern

**Reporter**: airSpring (V025)
**Affects**: biomeOS, wetSpring, groundSpring, neuralSpring
**Priority**: P1

**Problem**: wetSpring has a `science` domain in the capability registry.
airSpring proposes an `ecology` domain. groundSpring and neuralSpring would
logically propose `measurement` and `optimization` domains. There is no
documented pattern for a Spring registering as a biomeOS capability provider.

**Proposed fix**: Document the "Spring as Provider" pattern:
1. Spring binds a JSON-RPC socket at `$XDG_RUNTIME_DIR/biomeos/{spring}-{family}.sock`
2. Spring calls `capability.register` on the Neural API
3. biomeOS graph engine can route `capability_call` operations to the Spring
4. Spring handles requests using its barracuda library internally

Include example code and a template graph node.

**Status**: OPEN

---

### ISSUE-008: ET₀ GPU Promotion — 4 Methods Pending Tier A

**Reporter**: airSpring (V025)
**Affects**: ToadStool / BarraCuda
**Priority**: P2

**Problem**: airSpring has 7 validated ET₀ methods. Only 3 have GPU
promotion (PM = Tier A, PT/Hargreaves = Tier B via BatchedElementwise).
4 new methods (Thornthwaite, Makkink, Turc, Hamon) are CPU-validated
but lack GPU shaders.

**Proposed fix**: All 4 map to `BatchedElementwise` (op codes):
- `op=thornthwaite`: Monthly heat index → ET₀
- `op=makkink`: Radiation → ET₀ (Δ/(Δ+γ) term)
- `op=turc`: Temperature + radiation + humidity → ET₀
- `op=hamon`: Temperature + day length → PET

**Evidence**: airSpring Exp 033-035 (21+22+20 Python / 16+17+19 Rust checks)
validate the math. The GPU shaders would be straightforward element-wise ops.

**Status**: OPEN

---

### ISSUE-009: JSON Benchmark Schema Standardization

**Reporter**: airSpring (V024)
**Affects**: All Springs using validation harnesses
**Priority**: P3

**Problem**: Each Spring creates `benchmark_*.json` files with different
structures. airSpring uses a pattern of:
```json
{
  "experiment": "...",
  "description": "...",
  "validation_checks": {
    "section_name": {
      "test_cases": [{ "param": value, "expected": value, "tolerance": value }]
    }
  }
}
```

wetSpring and hotSpring use different schemas. A shared schema would enable
cross-Spring validation tooling.

**Proposed fix**: Define a `benchmark_schema.json` in the top-level
wateringHole with the standard structure. Springs can extend but must
include the core fields.

**Status**: OPEN

---

### ISSUE-010: Cross-Spring Data Flow — θ(t) → Microbial Diversity

**Reporter**: airSpring (V025)
**Affects**: airSpring, wetSpring, biomeOS
**Priority**: P3

**Problem**: The `cross_primal_soil_microbiome.toml` graph defines a
pipeline where airSpring's soil moisture θ(t) feeds into wetSpring's
diversity analysis. This requires:
1. A common data format for time series exchange
2. wetSpring accepting external environmental drivers
3. biomeOS passing outputs from one `capability_call` as inputs to the next

**Proposed fix**: Define a minimal time series exchange format:
```json
{
  "variable": "soil_moisture_vol",
  "unit": "m3/m3",
  "timestamps": ["2023-05-01", "2023-05-02", ...],
  "values": [0.32, 0.29, 0.25, ...]
}
```

**Status**: OPEN

---

### ISSUE-011: GPU f64 Catastrophic Cancellation in Special Functions

**Reporter**: hotSpring v0.6.19
**Affects**: barraCuda (math primitives), coralReef (compiler), ALL springs doing GPU science
**Priority**: P1 — silent physics errors from ULP amplification

**Problem**: GPU f64 arithmetic produces ULP-level different results from CPU
due to FMA fusion and operation reordering in SPIR-V. For algorithms with
catastrophic cancellation (subtraction of nearly-equal values), these small
differences get amplified 50-1000×, producing visible percent-level errors
and even sign flips in output quantities.

Discovered during Paper 44 GPU promotion: the plasma dispersion function
W(z) = 1 + z·Z(z) showed 125% relative error at specific frequencies where
z·Z(z) ≈ -1.017, amplifying ULP-level GPU/CPU differences through the
subtraction 1 - 1.017 = -0.017.

This is NOT a precision routing issue — all f64 polyfills were verified
present and correct. It is a fundamental consequence of heterogeneous IEEE-754
arithmetic and MUST be addressed algorithmically.

**Proposed fix** (split ownership):

1. **barraCuda (P1)**: Ship numerically stable GPU special function
   primitives (`special_f64.wgsl`) that avoid cancellation by design.
   Pattern: compute the small quantity directly via asymptotic expansion
   instead of as a difference of large values. hotSpring's `plasma_w()`
   fix is the template — should be absorbed into barraCuda.

2. **coralReef (P2)**: Expose SPIR-V `NoContraction` decoration control
   to disable FMA fusion when bit-exact CPU parity is required. Add FMA
   behavior detection to driver profiling. Long-term: coralNak precision
   manifest with per-operation FMA policy.

3. **Springs (awareness)**: Test GPU special functions with point diagnostics
   across full input range, not just aggregate statistics. Validate physics
   properties (conservation laws, positivity, sum rules) rather than CPU
   bit-parity.

**Evidence**: `wateringHole/GPU_F64_NUMERICAL_STABILITY.md` (full writeup),
`hotSpring/experiments/044_CHUNA_BGK_DIELECTRIC.md`, validation binary
`validate_gpu_dielectric` (12/12 checks after fix).

**Status**: OPEN — hotSpring workaround in place; barraCuda absorption pending

---

## Resolved Issues

*None yet — this document is newly created.*

---

## Contributing

Any Spring can add issues. Use the format:

```markdown
### ISSUE-NNN: Title

**Reporter**: Spring name (version)
**Affects**: List of affected primals/teams
**Priority**: P1 (blocker) / P2 (important) / P3 (nice to have)

**Problem**: What is the issue?

**Proposed fix**: How should it be resolved?

**Evidence**: Links to code, experiments, or handoffs that demonstrate the issue.

**Status**: OPEN / ACKNOWLEDGED / IN_PROGRESS / RESOLVED / WONT_FIX
```
