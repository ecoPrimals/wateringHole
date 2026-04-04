# Spring Evolution Issues — biomeOS Integration Surface

**Purpose**: Track issues, patterns, and evolution opportunities discovered by Springs
that require coordination from biomeOS, ToadStool, or cross-primal teams.
**Last Updated**: March 16, 2026
**Contributing Springs**: airSpring v0.7.5, neuralSpring S145, wetSpring V113, groundSpring V104, hotSpring v0.6.29, healthSpring V20, ludoSpring V37.1

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

**Status**: RESOLVED (March 13, 2026) — ecology domain with 30+ translations
added to `capability_registry.toml` (biomeOS v2.33+). Includes all 7 ET₀ methods,
soil physics, crop/irrigation, drought indices, biodiversity, and statistical
inference capabilities.

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

**Status**: RESOLVED (March 14, 2026) — `neural-api-client-sync` crate created in biomeOS
workspace. Zero-dep sync client using `std::os::unix::net::UnixStream`. 4-tier socket
discovery, `capability_call()`, `discover_capability()`, `health_check()`. All springs
can now use Neural API without tokio.

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

**Status**: RESOLVED (March 13, 2026) — `CapabilityHandler::call()` now accepts
all three formats with backward compatibility:
- Canonical: `{ "capability": "domain", "operation": "method", "args": {...} }`
- Dotted sugar: `{ "capability": "domain.method", "args": {...} }` (splits on first dot)
- Params alias: `"params"` accepted as alias for `"args"`
`NeuralApiCapabilityCaller` updated to emit canonical format.

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

**Status**: RESOLVED (March 13, 2026) — Created `cross_spring_soil_microbiome.toml`
graph (airSpring → wetSpring → provenance), registered `soil-microbiome` niche
template, and added `cross_spring_pipeline_e2e.rs` integration tests covering
capability chain calls and graph execution. Existing `cross_spring_ecology.toml`
also exercised by the test suite.

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

**Status**: RESOLVED (March 14, 2026) — `safe_uid()` function added to
`biomeos-types::paths`. Reads `/proc/self/status` Uid: line (safe, no libc).
Falls back to 65534 (nobody). Available as `SystemPaths::safe_uid()` and
`paths::safe_uid()`.

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

**Status**: RESOLVED (March 13, 2026) — Pattern documented in
`wateringHole/SPRING_AS_PROVIDER_PATTERN.md` with step-by-step guide,
example Rust code, deploy graph node template, and registry configuration.
wetSpring, airSpring, ludoSpring, neuralSpring, and healthSpring are
already registered in `capability_registry.toml`.

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

**Status**: RESOLVED (March 14, 2026) — Standard defined in `CROSS_SPRING_DATA_FLOW_STANDARD.md`.
Canonical format: `ecoPrimals/time-series/v1` with required fields (schema, variable, unit,
timestamps, values) and optional source/metadata. ISO 8601 timestamps, f64 values, SI units.

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
`hotSpring/experiments/044_BGK_DIELECTRIC.md`, validation binary
`validate_gpu_dielectric` (12/12 checks after fix).

**Status**: OPEN — hotSpring workaround in place; barraCuda absorption pending

---

### ISSUE-012: Content Similarity Index — Cross-Session Discovery Experiment

**Reporter**: rhizoCrypt (v0.13.0-dev)
**Affects**: All Springs that produce vertices in rhizoCrypt sessions
**Priority**: P3 — experimental, no production blocker

**Problem**: rhizoCrypt's DAG stores are session-scoped. Cross-session patterns
(similar vertices, similar agent behavior, similar event structures) are
invisible without full-scan analysis. Springs that produce multiple sessions
have no efficient way to discover structural similarities across them.

**Proposed fix**: A locality-sensitive content index (feature-gated behind
`content-index`) that creates intentional hash "collisions" for structurally
similar vertices. This enables O(1) cross-session similarity lookup.

Springs should participate by:
1. **Phase A (now)**: Audit vertex event types and metadata schemas for consistency
2. **Phase B**: Normalize event naming to `{domain}.{action}` convention
3. **Phase C**: Propose domain-specific LSH input features (see guide)

**Evidence**: `rhizoCrypt/specs/CONTENT_INDEX_EXPERIMENT.md` (full spec),
`wateringHole/CONTENT_SIMILARITY_EXPERIMENT_GUIDE.md` (Spring participation guide).

**Status**: OPEN — spec proposed, awaiting Phase 1 implementation in rhizoCrypt

---

### ISSUE-013: Content Convergence — Provenance Intersection as Data Science

**Reporter**: sweetGrass (v0.7.15)
**Affects**: All Springs that produce Braids via sweetGrass, rhizoCrypt (related to ISSUE-012)
**Priority**: P3 — experimental, no production blocker

**Problem**: sweetGrass indexes Braids by `ContentHash` using a 1:1 mapping
(last-write-wins). When two independent agents produce Braids with the same
content hash via different provenance paths, the earlier index entry is silently
overwritten. This "provenance convergence" carries semantic meaning — reproducibility,
consensus, independent agreement — that the current lossy index discards.

The concept extends a hash collision research insight: instead of resolving
collisions, examine **what data lies at the collision point**. By modifying
hash table sizes and hash functions, convergence rates can be controlled,
opening new data storage and data science techniques.

Additionally, this connects to the historical practice of cross-hatched letters
(rotating the page and writing over existing text when paper was scarce) — both
information layers persist. In our context: linear storage (loamSpine-style
append) and branching provenance (rhizoCrypt-style DAG) coexist at convergence
points, mirroring biological systems where linear hyphal growth and branching
anastomosis produce emergent network topology.

**Proposed fix** (split ownership):

1. **sweetGrass (Phase 1)**: Evolve content hash index from `HashMap<ContentHash, BraidId>`
   to `HashMap<ContentHash, ContentConvergence>`. New `ConvergentArrival` struct captures
   agent, timestamp, and derivation path for each convergent arrival. New `convergence.query`
   JSON-RPC method. Full spec: `sweetGrass/specs/CONTENT_CONVERGENCE.md`.

2. **Springs (Phase A — now)**: Audit data production patterns for scenarios where
   independent processes might produce identical content hashes. Document candidates.

3. **Springs (Phase B)**: After sweetGrass Phase 1, produce convergent Braid pairs
   via `braid.create` and verify convergence tracking via `convergence.query`.

4. **rhizoCrypt coordination**: Connect to ISSUE-012 (Content Similarity Index).
   rhizoCrypt LSH operates at the vertex level; sweetGrass convergence operates at
   the provenance level. Springs can cross-reference: do rhizoCrypt-similar vertices
   produce sweetGrass-convergent Braids?

**Evidence**: `sweetGrass/specs/CONTENT_CONVERGENCE.md` (full specification),
`wateringHole/CONTENT_CONVERGENCE_EXPERIMENT_GUIDE.md` (Spring participation guide),
`sweetGrass/crates/sweet-grass-store/src/memory/indexes.rs` (current lossy index).

**Status**: OPEN — specification proposed, sweetGrass Phase 1 targeted for v0.8.x

---

## Resolved Issues

### ISSUE-001: Ecology Capability Domain Missing from Registry
Resolved March 13, 2026. See Open Issues section for details.

### ISSUE-003: `capability.call` Parameter Format Inconsistency
Resolved March 13, 2026. See Open Issues section for details.

### ISSUE-004: Cross-Primal Pipeline Graph Execution Not Tested End-to-End
Resolved March 13, 2026. See Open Issues section for details.

### ISSUE-007: Springs as biomeOS Science Providers — Registration Pattern
Resolved March 13, 2026. See Open Issues section for details.

### ISSUE-002: Neural API Client Needs Synchronous Alternative
Resolved March 14, 2026. See Open Issues section for details.

### ISSUE-005: Safe UID Discovery Pattern
Resolved March 14, 2026. See Open Issues section for details.

### ISSUE-010: Cross-Spring Data Flow — θ(t) → Microbial Diversity
Resolved March 14, 2026. See Open Issues section for details.

---

### ISSUE-022: Root Privilege Dependency — Sovereignty Violation

**Reporter**: hotSpring (workspace migration 2026-03-28)
**Affects**: coralReef (coral-glowplug, coral-ember), all springs using GPU hardware
**Priority**: P2 — architectural debt against sovereignty

**Problem**: coralReef's GPU lifecycle management requires root privilege at
multiple points: VFIO group access, PCI driver bind/unbind via sysfs, systemd
service execution, udev rule deployment, and a sudoers file granting specific
sysfs write access. Every `pkexec`, `sudo`, or `CAP_SYS_ADMIN` requirement is
a point where the primal is bound to the host kernel's permission model rather
than operating as a sovereign, self-contained process.

**Proposed fix**: Evolve toward fd-passing architecture. coral-ember's
SCM_RIGHTS pattern (passing pre-opened VFIO fds to glowplug) is the right
direction. End state: primals receive pre-opened device handles at startup
and never touch sysfs or require elevated privilege. Intermediate step: a
single privileged launcher (thin, auditable) that opens devices and passes
fds to unprivileged primal processes. agentReagents VM isolation is the
containment strategy for operations that cannot yet shed root.

**Evidence**: `springs/hotSpring/scripts/boot/coralreef-sudoers`,
`springs/hotSpring/scripts/deploy_glowplug.sh`,
`infra/wateringHole/SOVEREIGN_COMPUTE_EVOLUTION.md` (Evolution Gap section).

**Status**: OPEN

---

### ISSUE-011: rhizoCrypt Has No Unix Domain Socket Transport

**Reporter**: ludoSpring (V37.1)
**Affects**: rhizoCrypt, all compositions requiring provenance
**Priority**: P1 — blocks 4 ludoSpring experiments (+9 checks), blocks any Trio composition via UDS

**Problem**: rhizoCrypt only binds TCP (port 9401). It does not create a Unix domain socket.
All other ecoBin primals (BearDog, NestGate, sweetGrass, barraCuda, etc.) follow the
`$XDG_RUNTIME_DIR/biomeos/{primal}.sock` convention. `start_primal.sh` passes `--socket`
but rhizoCrypt ignores it.

**Proposed fix**: Add `--unix [PATH]` CLI flag, default to `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`.
Follow barraCuda's pattern (`--unix` defaults to XDG, overridable).

**Evidence**: `ludoSpring/experiments/exp094_session_lifecycle/`, `exp095_content_ownership/`,
`exp096_npc_dialogue_composition/`, `exp098_nucleus_game_session/`.
Handoff: `LUDOSPRING_V371_PLASMIDBINLIVE_GAP_MATRIX_HANDOFF_MAR31_2026.md`

**Status**: OPEN

---

### ISSUE-012: loamSpine Panics on Startup (Runtime Nesting)

**Reporter**: ludoSpring (V37.1)
**Affects**: loamSpine, all compositions requiring certificates
**Priority**: P1 — loamSpine cannot start, blocks exp095 (+6 checks)

**Problem**: `loamspine server` panics at `crates/loam-spine-core/src/service/infant_discovery.rs:233`
with "Cannot start a runtime from within a runtime". This is a Tokio anti-pattern where
`block_on()` is called inside an already-running async runtime.

**Proposed fix**: Replace `block_on()` with `spawn` or restructure infant discovery to avoid
nesting runtimes. The async context already exists when `block_on` is invoked.

**Evidence**: `/tmp/loamspine.log` from ludoSpring V37.1 live run.
Handoff: `LUDOSPRING_V371_PLASMIDBINLIVE_GAP_MATRIX_HANDOFF_MAR31_2026.md`

**Status**: OPEN

---

### ISSUE-013: barraCuda Fitts/Hick Formula Mismatch vs Python Baselines

**Reporter**: ludoSpring (V37.1)
**Affects**: barraCuda `activation.fitts`, `activation.hick`
**Priority**: P2 — 4 checks fail in exp089

**Problem**:
- `activation.fitts(d=256, w=32, a=200, b=150)` → 800 (barraCuda) vs 708.85 (Python).
  barraCuda uses Welford `log2(D/W)`, Python uses Shannon `log2(2D/W + 1)`.
- `activation.hick(n=8, a=200, b=150)` → 675.49 (barraCuda) vs 650 (Python).
  barraCuda uses `log2(n+1)`, Python uses `log2(n)`.

**Proposed fix**: Add a `variant` parameter (default: "shannon" for Fitts, "standard" for Hick)
or align defaults to the most-cited formulations.

**Evidence**: `ludoSpring/experiments/exp089_psychomotor_composition/` — live IPC results.

**Status**: OPEN

---

### ISSUE-014: biomeOS Neural API Not Registering Primal Capabilities

**Reporter**: ludoSpring (V37.1)
**Affects**: biomeOS Neural API `capability.call`, all capability-routed experiments
**Priority**: P2 — 14 checks fail across exp084/087/088

**Problem**: Running primals (barraCuda, BearDog, NestGate, etc.) are alive on sockets but
the Neural API only shows 5 capabilities: `primal.germination`, `primal.terraria`,
`ecosystem.nucleation`, `graph.execution`, `ecosystem.coordination`. Missing: `math`,
`tensor`, `compute`, `noise`, `stats`, `activation`, `dag`, `visualization`, `crypto`,
`security`, `storage`. The v2.80 bootstrap graph has `register_barracuda` but it doesn't
appear to populate the capability registry for `capability.call` routing.

**Proposed fix**: Either (a) primals self-register on startup via `lifecycle.register` +
`capability.register`, or (b) biomeOS probes known sockets and populates the registry
from `capabilities.list` responses.

**Evidence**: `ludoSpring/experiments/exp087_neural_api_pipeline/`, `exp088_continuous_game_loop/`.

**Status**: OPEN

---

### ISSUE-015: plasmidBin start_primal.sh JWT Secret Too Short for NestGate

**Reporter**: ludoSpring (V37.1)
**Affects**: plasmidBin, NestGate
**Priority**: P3 — startup workaround available

**Problem**: The NestGate case block in `start_primal.sh` generates
`NESTGATE_JWT_SECRET="plasmidbin-${NODE_ID:-gate}-$FAMILY_ID"` = 25 bytes.
NestGate requires a minimum of 32 bytes and refuses to start.

**Proposed fix**: Use `openssl rand -base64 48` in the NestGate case block, or
persist a generated secret to a local config file.

**Evidence**: `/tmp/nestgate.log` from ludoSpring V37.1 live run.

**Status**: OPEN

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
