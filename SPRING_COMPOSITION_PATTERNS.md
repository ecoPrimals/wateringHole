# Spring Composition Patterns — Absorbed Best Practices

**Date**: April 27, 2026 (updated from April 13, 2026)
**From**: primalSpring v0.9.17 — Phase 46: 187/187 ALL PASS, 13/13 BTSP authenticated, plasmidBin depot, cross-spring convergence analysis
**For**: All springs evolving toward primal composition
**License**: AGPL-3.0-or-later

---

## Purpose

As springs evolve in parallel, each discovers IPC, discovery, and composition
patterns independently. This document captures the **best patterns** from
across the ecosystem and standardizes them so every spring can absorb them.

These patterns were extracted from live spring codebases — they are proven,
not theoretical.

---

## 1. Method Normalization (MUST)

**Source**: healthSpring `ipc/rpc.rs`, wetSpring `ipc/protocol.rs`

Springs and primals accumulate method name prefixes over time
(`wetspring.health.liveness`, `barracuda.compute.execute`). All IPC
dispatch must normalize methods before routing.

**Standard**: Strip known prefixes iteratively until stable.

```rust
fn normalize_method(method: &str) -> Cow<'_, str> {
    let prefixes = ["healthspring.", "barracuda.", "biomeos.", "wetspring."];
    let mut m = method;
    loop {
        let before = m;
        for p in &prefixes {
            m = m.strip_prefix(p).unwrap_or(m);
        }
        if m == before { break; }
    }
    if m == method { Cow::Borrowed(method) } else { Cow::Owned(m.to_string()) }
}
```

**Why iterative**: Single-pass stripping fails on doubly-prefixed names
(`wetspring.barracuda.math.tensor`). The loop handles any nesting depth.

Every spring's RPC dispatch MUST normalize before matching.

---

## 2. Capability Registration as Contract (MUST)

**Source**: healthSpring `capabilities.rs`, neuralSpring `capability_registry.toml`

Capabilities are not just strings — they are **contracts** for orchestration.
Registration MUST include:

```rust
struct CapabilityEntry {
    method: &'static str,          // FQ method name
    domain: &'static str,          // "science" | "infrastructure" | "lifecycle"
    description: &'static str,     // human-readable
    cost_estimate: &'static str,   // "low" | "medium" | "high" | "gpu"
}
```

Additionally, provide:
- **Semantic mappings**: short name → FQ method (e.g., `"noise"` → `"science.noise_analysis"`)
- **Dependencies**: which primals are needed for this capability
- **Cost estimates**: for Squirrel/Pathway Learner scheduling

**TOML registry** (neuralSpring pattern) alongside code-level constants
provides human-readable documentation that stays in sync with the wire.

---

## 3. Tiered Socket Discovery (MUST)

**Source**: neuralSpring `validation/composition.rs`, hotSpring `primal_bridge.rs`

All primal socket discovery MUST follow the same tier order:

```
Tier 1: Explicit env var        ${PRIMAL}_SOCKET=/path/to/socket
Tier 2: XDG biomeos dir         $XDG_RUNTIME_DIR/biomeos/{primal}-{family}.sock
Tier 3: Plain socket fallback   $XDG_RUNTIME_DIR/biomeos/{primal}.sock
Tier 4: Temp fallback           /tmp/biomeos/{primal}.sock
Tier 5: Legacy/abstract         @biomeos_{primal} (Android)
Tier 6: Neural API sweep        biomeOS capability.discover
```

**Key pattern**: Return structured `DiscoveryResult` (neuralSpring):
```rust
enum DiscoveryResult {
    Found { path: PathBuf, tier: u8 },
    NotFound { primal: String, searched: Vec<PathBuf> },
}
```

**hotSpring enhancement**: `NucleusContext::detect` scans the entire
`biomeos/` directory, parses `{name}-{family}.sock` filenames, and probes
each for liveness. Returns a map of live primals. This pattern is ideal
for **runtime** mesh discovery (vs. the validator pattern above).

Springs MUST support **standalone mode** when no primals are found
(hotSpring's `HOTSPRING_NO_NUCLEUS` env var pattern).

---

## 4. Two-Tier Dispatch (SHOULD)

**Source**: healthSpring `routing.rs`

Separate **lifecycle/infrastructure** dispatch from **domain/science**
dispatch:

```
Request → normalize_method
       → match lifecycle (health.*, capabilities.*, lifecycle.*)
       → match infrastructure (primal.*, compute.*, inference.*, data.*)
       → match science (domain-specific methods)
       → proto-nucleate alias resolution (legacy → current)
       → MethodNotFound
```

This keeps domain science code **isolated** from IPC plumbing and makes
it easy to add new science capabilities without touching infrastructure.

---

## 5. Graph Validation Recipe (SHOULD)

**Source**: ludoSpring `deploy/recipe.rs`

Validating a deploy graph against live reality:

```
1. Parse TOML → DeployGraph
2. Structural validation (required fields, valid references)
3. Topological wave computation (dependency ordering)
4. Per-node: discover_primals → capability match
5. Per-node: health_method probe (or default health.liveness)
6. Aggregate: CompositionReport { satisfied, missing, degraded }
```

`CompositionReport` reports per-node status (`NodeStatus::Healthy`,
`NodeStatus::Missing`, `NodeStatus::Degraded`) so orchestrators know
exactly what's available.

Springs with their own deploy graphs SHOULD validate them using this
algorithm. The `DeployGraph` / `GraphNode` structs SHOULD match
primalSpring's schema (ludoSpring copies it without cross-imports).

---

## 6. Optional biomeOS Feature Gate (SHOULD)

**Source**: groundSpring `lib.rs`

Springs that need to build without NUCLEUS (CI, benchmarks, lightweight
testing) SHOULD gate orchestration behind a feature:

```toml
[features]
default = []
biomeos = ["serde_json", "tracing"]
```

```rust
#[cfg(feature = "biomeos")]
pub mod biomeos;
#[cfg(feature = "biomeos")]
pub mod dispatch;
#[cfg(feature = "biomeos")]
pub mod nestgate;
```

This keeps core science **lightweight** while the NUCLEUS integration
stack is opt-in. Default builds compile fast; CI can test both.

---

## 7. Graceful Degradation for Provenance (SHOULD)

**Source**: airSpring `ipc/provenance.rs`

The provenance trio (rhizoCrypt + loamSpine + sweetGrass) may not be
running. Springs MUST NOT fail when the trio is absent — they MUST
degrade gracefully:

```rust
struct ProvenanceResult<T> {
    available: bool,
    data: Option<T>,
}
```

Config supports transport override and env resolution. Domain logic
returns `Ok` with `available: false` when the trio is missing, not an
error. This lets experiments run without provenance while still
recording it when available.

---

## 8. Capability-Based Compute Dispatch (SHOULD)

**Source**: airSpring `ipc/compute_dispatch.rs`

When dispatching to toadStool for compute:

```rust
enum DispatchError {
    NoComputePrimal,     // toadStool not found
    TransportError(io::Error),
    RpcError { code: i64, message: String },
}
```

Discover toadStool via capability, not name. Map `SocketNotFound` →
`NoComputePrimal` for clear error semantics. This pattern applies to
any primal dispatch, not just compute.

---

## 9. Cross-Spring Time-Series Schema (SHOULD)

**Source**: airSpring `ipc/timeseries.rs`

When exchanging time-series data between springs:

```rust
const SCHEMA: &str = "ecoPrimals/time-series/v1";

struct TimeSeriesData {
    schema: String,           // MUST match SCHEMA
    source_spring: String,
    source_experiment: String,
    source_capability: String,
    timestamps: Vec<f64>,
    values: Vec<f64>,
    metadata: serde_json::Value,
}
```

Schema identity prevents ad-hoc JSON from being misinterpreted across
spring boundaries. All cross-spring data exchange SHOULD include a
schema version string.

---

## 10. Runtime NUCLEUS Mesh Discovery (MAY)

**Source**: hotSpring `primal_bridge.rs`

For springs that need to discover the full primal mesh at runtime
(not just specific primals):

```rust
struct NucleusContext {
    endpoints: HashMap<String, PrimalEndpoint>,
}

impl NucleusContext {
    fn detect() -> Self { /* scan biomeos/*.sock, probe each */ }
    fn get_by_capability(&self, cap: &str) -> Option<&PrimalEndpoint> { ... }
    fn call_by_capability(&self, cap: &str, method: &str, params: Value) -> Result<Value> { ... }
}
```

Supports **name aliasing** (`coralreef` ↔ `coral-glowplug`) and
**capability prefix matching** for dynamic meshes. This is heavier
than single-primal discovery but necessary for fleet/federation
scenarios.

---

## 11. Niche Identity (MUST)

**Source**: All springs (groundSpring pattern is cleanest)

Every spring MUST have a `niche.rs` (or equivalent) declaring:

```rust
const NICHE_ID: &str = "groundspring";
const CAPABILITIES: &[CapabilityEntry] = &[ ... ];
const SEMANTIC_MAPPINGS: &[(&str, &str)] = &[ ("noise", "science.noise_analysis"), ... ];
const DEPENDENCIES: &[NicheDependency] = &[
    NicheDependency { name: "beardog", role: "security", required: true, capability: "crypto" },
    NicheDependency { name: "toadstool", role: "compute", required: false, capability: "compute" },
];
```

The dependency table aligns with the proto-nucleate graph's node list
and makes capability-based discovery self-documenting.

---

## 12. Dependency Governance (`deny.toml`) (MUST)

**Source**: biomeOS `deny.toml`, primalSpring CI-01 audit

Every spring and primal MUST have a `deny.toml` at its workspace root that
enforces ecoBin compliance. Without this, dependency bans exist on paper but
nobody verifies them.

**Minimum viable `deny.toml`:**

```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"

[bans]
multiple-versions = "warn"
deny = [
    { name = "openssl-sys", wrappers = [] },
    { name = "ring", wrappers = [] },
    { name = "aws-lc-sys", wrappers = [] },
    { name = "native-tls", wrappers = [] },
]

[licenses]
allow = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Zlib",
         "Unicode-3.0", "Unicode-DFS-2016", "MPL-2.0", "AGPL-3.0-or-later",
         "OpenSSL", "BSL-1.0", "CC0-1.0"]
```

**CI enforcement**: `cargo deny check` MUST be a CI step. biomeOS has this as
Job 6 in its pipeline. Without CI enforcement, the `deny.toml` is decorative.

**Spring-specific additions**: Springs using compute (toadStool, coralReef) may
need additional bans for GPU vendor SDKs. Science springs should ban any
non-reproducible dependency sources.

---

## 13. Composition Parity Validation (SHOULD)

**Source**: primalSpring `composition/mod.rs` (v0.8.0+), ludoSpring `exp068`, hotSpring `validate_nucleus_composition`

The final validation layer: prove that **primal compositions** (NUCLEUS primals
orchestrated by biomeOS) produce the same results as the spring's original
Python baselines. At this level, the spring has **no local math** — all
computation is delegated to primals via IPC. The spring's Rust code
(Levels 2-4) already evolved the primals and is now fossil record.

**The library** (`primalspring::composition`):

```rust
use primalspring::composition::{CompositionContext, validate_parity};
use primalspring::tolerances;
use primalspring::validation::ValidationResult;

// Discover whatever NUCLEUS primals are running
let mut ctx = CompositionContext::from_live_discovery();
let mut v = ValidationResult::new("mySpring Composition Parity");

// Expected value from PYTHON BASELINE (documented provenance).
// The spring's own Rust math has retired — primals own it now.
let python_baseline = 42.0_f64;

// Does the primal composition produce the same result?
// Note: tensor.matmul requires session-based tensor IDs (tensor.create first).
// Use stats.mean / stats.std_dev for inline-data parity checks.
validate_parity(
    &mut ctx, &mut v,
    "my_mean_computation",
    "tensor",                    // capability (not primal name)
    "stats.mean",                // JSON-RPC method
    serde_json::json!({"data": [1.0, 2.0, 3.0]}),
    "result",                    // result key in response
    2.0_f64,                     // from documented Python run
    tolerances::EXACT_PARITY_TOL,
);

v.finish_and_exit();
```

**Key properties**:
- **Capability-based**: call by capability ("tensor"), not primal name ("barracuda")
- **Graceful**: if the primal isn't running, the check records SKIP, not FAIL
- **Named tolerances**: 7 documented tolerance constants covering exact parity through stochastic algorithms
- **No primal imports**: springs never `cargo add barracuda` — they call through the composition layer

**Named tolerance ladder** (`primalspring::tolerances`):

| Constant | Value | Use Case |
|----------|-------|----------|
| `EXACT_PARITY_TOL` | 0.0 | Deterministic integer math |
| `DETERMINISTIC_FLOAT_TOL` | 1e-15 | Pure CPU f64, same operation order |
| `DF64_PARITY_TOL` | 1e-14 | barraCuda df64 emulated precision |
| `CPU_GPU_PARITY_TOL` | 1e-10 | CPU f64 vs GPU WGSL (FMA/rounding divergence) |
| `IPC_ROUND_TRIP_TOL` | 1e-10 | JSON serialization edge cases |
| `WGSL_SHADER_TOL` | 1e-6 | f32 shader output vs f64 baseline |
| `STOCHASTIC_SEED_TOL` | 1e-6 | Seeded PRNG algorithms (Monte Carlo, HMC) |

**Update (April 13, 2026)**: All wire contracts validated live — 19/19 exp094 PASS.
Wire methods confirmed: `stats.mean` (barraCuda), `storage.store`/`storage.retrieve`
(NestGate), `crypto.hash` (BearDog, base64), `ipc.resolve` (Songbird, returns
`native_endpoint`/`virtual_endpoint`), `shader.compile.capabilities` (coralReef).
All 12 primals support UDS. `tensor.matmul` requires session-based tensor IDs
(`tensor.create` first) — use `stats.mean` for inline-data parity checks.

---

## §14: NUCLEUS Composition Parity Experiment (SHOULD)

After absorbing a proto-nucleate graph, each spring should create a composition
parity experiment. This is the **next layer of validation** — proving that the
same science works when composed from NUCLEUS primals rather than local Rust math.

**Reference implementation**: `primalSpring/experiments/exp094_composition_parity/`

**Pattern**:

```rust
use primalspring::composition::{CompositionContext, validate_parity};
use primalspring::tolerances;
use primalspring::validation::ValidationResult;

fn main() {
    ValidationResult::new("mySpring — NUCLEUS Composition Parity")
        .with_provenance("myspring_composition", "2026-04-12")
        .run("mySpring: NUCLEUS parity", |v| {
            let mut ctx = CompositionContext::from_live_discovery();

            // Tower: verify trust boundary
            v.section("Tower");
            tower_alive(&mut ctx, v);

            // Niche: your domain-specific composition checks
            v.section("Niche");
            validate_parity(
                &mut ctx, v,
                "my_mean_check",
                "tensor",
                "stats.mean",
                serde_json::json!({"data": [1.0, 2.0, 3.0]}),
                "result",
                2.0_f64,
                tolerances::EXACT_PARITY_TOL,
            );
        });
}
```

**Live deployment validated** (April 13, 2026): exp094 achieves **19/19 PASS, 0 FAIL,
0 SKIP** against a running NUCLEUS (12/12 primals ALIVE). All previously identified
gaps (LD-01 through LD-10) are RESOLVED upstream.

**Key findings for springs**:
- Health format: all primals now respond to `health.liveness` on UDS
- BearDog returns base64-encoded hashes (not hex) — `crypto.hash` deterministic
- Songbird uses `ipc.resolve` with `native_endpoint`/`virtual_endpoint` response
- NestGate/ToadStool have persistent UDS connections (no reconnect needed)
- coralReef reports GPU architectures via `shader.compile.capabilities`
- barraCuda: use `stats.mean` for inline-data checks; `tensor.matmul` needs session IDs
- Phase 5 registry seeding: `nucleus_launcher.sh` seeds Songbird with all 9 core primals
- `IpcError::is_transport_mismatch()`: gracefully handles tarpc sockets receiving JSON-RPC

**Niche starter patterns**: See `primalSpring/graphs/downstream/NICHE_STARTER_PATTERNS.md`
for domain-specific examples (hotSpring QCD, neuralSpring ML, healthSpring enclaves,
wetSpring genomics).

---

## §15: Cross-Spring Convergent Evolution Patterns (April 27, 2026)

Analysis of all seven springs reveals patterns that emerged independently in
multiple springs — confirming them as ecosystem-level truths, not local
accidents.

### Convergent Discovery: UDS Transport Portability

**Discovered by**: hotSpring, wetSpring, healthSpring, neuralSpring (independently)

All four delta springs hit the same issue: `socat` not installed on fresh
systems blocks JSON-RPC over UDS. primalSpring resolved this with the
`_uds_send()` fallback chain in `nucleus_composition_lib.sh`:

```
socat → python3 socket → nc (netcat)
```

**Absorbed by**: primalSpring `nucleus_composition_lib.sh` (PG-49 fix).
All springs using the composition library inherit the fix.

### Convergent Discovery: Missing Default Primals

**Discovered by**: healthSpring, neuralSpring (independently)

Both springs reported that `nestgate` and `squirrel` were missing from the
default `PRIMAL_LIST` in `composition_nucleus.sh`. Their compositions failed
on first run because storage and AI weren't started.

**Absorbed by**: primalSpring `composition_nucleus.sh` — `nestgate` and
`squirrel` added to defaults, plus `EXTRA_PRIMALS` env var for spring-specific
additions (PG-50 fix).

### Convergent Discovery: Temporal Heterogeneity

**Discovered by**: ludoSpring (60Hz ticks), hotSpring (convergence), airSpring (seasonal)

Three springs independently evolved different temporal models for their
compositions. ludoSpring needs fixed-timestep game ticks. hotSpring needs
convergence-driven iteration. airSpring uses seasonal time steps.

**Absorbed by**: `COMPOSITION_TICK_MODEL_STANDARD.md` — standardizes five
temporal classes (continuous, convergence, event, batch, seasonal) with
deploy graph declarations.

### Convergent Discovery: Cross-Spring Validation

**Discovered by**: healthSpring (five-way bridge), neuralSpring (`cross_spring_*` methods)

Two springs independently evolved cross-spring coordination — healthSpring
as a routing hub, neuralSpring as explicit RPC methods. Both prove the
same need: springs must validate across domain boundaries.

**Absorbed by**: `CROSS_SPRING_COORDINATION_STANDARD.md` — standardizes
`science.cross_spring_*` namespace, shared baselines, precision routing.

### Convergent Discovery: Deploy Graph Schema Divergence

**Discovered by**: ludoSpring (Format A: `[[graph.nodes]]`), primalSpring (Format A: `[[graph.node]]`)

ludoSpring independently implemented deploy graph parsing without importing
primalSpring. The `[[graph.nodes]]` vs `[[graph.node]]` divergence is a
symptom of evolution without coupling — both are correct implementations
of the same concept. biomeOS must accept both.

**Status**: Documented in `DEPLOYMENT_AND_COMPOSITION.md` §BYOB. biomeOS
ingestion handles both formats.

### Spring Unique Contributions Matrix

Each spring discovered something that only its domain could teach:

| Spring | Unique Discovery | Ecosystem Impact |
|--------|-----------------|-----------------|
| **hotSpring** | guideStone Level 5 certification (308 named tolerances) | Tolerance discipline absorbed by all springs |
| **wetSpring** | Largest validation surface (5,900+ checks, 44 GPU modules) | Scale-testing patterns for CI/CD |
| **neuralSpring** | `science.cross_spring_*` RPC methods, provenance as RPC | Cross-spring coordination standard |
| **healthSpring** | Five-way cross-spring bridge (84 IPC capabilities) | Multi-domain routing pattern |
| **ludoSpring** | Session lifecycle IPC, deploy recipe without importing primalSpring | Garden composition independence |
| **groundSpring** | `measurement.*` API surface, labeled dirty-data baselines | Uncertainty as a consumable service |
| **airSpring** | ET₀ 8-method ensemble, proptest invariants on physical quantities | Systems validation (not just equations) |

### Composition Absorption Status

| Status | Springs |
|--------|---------|
| **Absorbed `nucleus_composition_lib.sh` + have `*_composition.sh`** | hotSpring, wetSpring, neuralSpring, healthSpring |
| **Pre-absorption (pinned or needs more time)** | airSpring, groundSpring, ludoSpring |

airSpring and groundSpring are pre-delta — they have high coverage (90%+)
but no NUCLEUS wiring yet. ludoSpring evolved independently and has its own
composition model (pure composition, 12-node cell graph, 60Hz tick).

---

## Pattern Adoption Checklist

When starting a composition evolution session on any spring:

- [ ] Method normalization in all dispatch paths
- [ ] Capability registration with domain/cost/dependencies
- [ ] Tiered socket discovery (6 tiers, structured result)
- [ ] Two-tier dispatch (infra vs science)
- [ ] Deploy graph validation against proto-nucleate
- [ ] biomeOS feature gate for lightweight builds
- [ ] Graceful provenance degradation
- [ ] Capability-based compute dispatch (not name-based)
- [ ] Niche identity with dependencies
- [ ] Standalone mode support (no-primal fallback)
- [ ] `deny.toml` with C/FFI bans + CI enforcement (`cargo deny check`)
- [ ] Inference methods use `inference.*` namespace (not `ai.*`)
- [ ] Composition parity validation (§13) using `primalspring::composition`
- [ ] **NUCLEUS composition experiment (§14)** — live deployment parity test
- [ ] Cross-spring coordination methods (§15) where domain-appropriate
- [ ] Temporal model declaration in deploy graphs (`COMPOSITION_TICK_MODEL_STANDARD.md`)
- [ ] Hand back gaps to primalSpring via wateringHole handoff

---

## Related Documents (added April 27, 2026)

- `CROSS_SPRING_COORDINATION_STANDARD.md` — Cross-spring RPC patterns
- `COMPOSITION_TICK_MODEL_STANDARD.md` — Heterogeneous temporal requirements
- `INTERACTION_EVENT_TAXONOMY.md` — Unified interaction event taxonomy
- `PROVENANCE_TRIO_INTEGRATION_GUIDE.md` — Trio wiring guide
- `GARDEN_COMPOSITION_ONRAMP.md` — Garden product onramp

---

**License**: AGPL-3.0-or-later
