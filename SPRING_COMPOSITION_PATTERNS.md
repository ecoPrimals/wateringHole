# Spring Composition Patterns — Absorbed Best Practices

**Date**: April 12, 2026
**From**: primalSpring v1.1.0 review of all 7 springs
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
validate_parity(
    &mut ctx, &mut v,
    "my_computation",
    "tensor",                    // capability (not primal name)
    "tensor.matmul",             // JSON-RPC method
    serde_json::json!({...}),    // params
    "value",                     // result key in response
    python_baseline,             // from documented Python run
    tolerances::CPU_GPU_PARITY_TOL,
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

**Update (April 12, 2026)**: Wire contracts now exist for tensor (barraCuda Sprint 42),
shader (coralReef Iter 80), and dispatch (toadStool S203). Remaining gap: crypto,
storage, and discovery response schemas.

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
                "my_computation",
                "tensor",
                "tensor.matmul",
                serde_json::json!({"a": my_a, "b": my_b}),
                "value",
                python_baseline,
                tolerances::CPU_GPU_PARITY_TOL,
            );
        });
}
```

**Live deployment tested** (April 12, 2026): exp094 discovered 8 capabilities
from a running NUCLEUS (security, discovery, compute, storage, shader, ai,
commit, provenance). Results: 7 PASS, 5 FAIL (wire format gaps), 7 SKIP
(barraCuda/rhizoCrypt not yet wired). All failures are upstream protocol gaps
being tracked in `primalSpring/docs/PRIMAL_GAPS.md`.

**Key findings for springs**:
- Health format varies: `{"alive":true}` vs `{"status":"alive"}` — handle both
- BearDog returns base64-encoded hashes (not hex)
- Songbird uses `ipc.resolve` (not `capability.resolve`)
- NestGate/ToadStool may close UDS after one response — reconnect pattern needed
- coralReef reports 11 GPU architectures via `shader.compile.capabilities`

**Niche starter patterns**: See `primalSpring/graphs/downstream/NICHE_STARTER_PATTERNS.md`
for domain-specific examples (hotSpring QCD, neuralSpring ML, healthSpring enclaves,
wetSpring genomics).

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
- [ ] Hand back gaps to primalSpring via wateringHole handoff

---

**License**: AGPL-3.0-or-later
