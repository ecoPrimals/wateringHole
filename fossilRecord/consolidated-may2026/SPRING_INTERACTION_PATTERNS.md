# Spring Interaction Patterns — Cross-Evolution and Interoperability

**Version**: 1.0.0  
**Date**: April 4, 2026  
**Status**: Active  

This document consolidates: `SPRING_AS_PROVIDER_PATTERN.md`, `SPRING_CROSS_EVOLUTION_STANDARD.md`, `SPRING_INTEROP_LESSONS.md`, `SPRING_EVOLUTION_ISSUES.md`, `CROSS_SPRING_DATA_FLOW_STANDARD.md`, `CROSS_SPRING_SHADER_EVOLUTION.md`, `COMPUTE_TRIO_SPRING_GUIDE.md`.

---

## Spring-as-Provider

Science springs register as capability providers with biomeOS’s Neural API so `capability.call` routes to the spring, enabling cross-primal coordination, graph execution, and niche deployment.

### Prerequisites

- biomeOS Tower Node (BearDog + Songbird at minimum)
- Neural API socket: `$XDG_RUNTIME_DIR/biomeos/neural-api.sock`
- Spring: JSON-RPC 2.0 server over Unix domain socket

### Architecture

```text
Spring                        biomeOS Neural API            Consumer
  │                                │                           │
  │ 1. Bind UDS socket             │                           │
  │ 2. capability.register ──────► │                           │
  │                                │ ◄── capability.call ──── │
  │ ◄── forwarded JSON-RPC ─────── │                           │
  │ ──── response ───────────────► │ ──── response ──────────► │
```

### Step 1: Socket naming

```
$XDG_RUNTIME_DIR/biomeos/{spring_name}-{family_id}.sock
```

Fallback order:

1. `$XDG_RUNTIME_DIR/biomeos/{spring}-{family}.sock`
2. `/run/user/{uid}/biomeos/{spring}-{family}.sock`
3. `/tmp/{spring}-{family}.sock`

Minimum methods: `lifecycle.status` (`{ "name": "...", "capabilities": [...] }`), `health`, plus domain methods from capability translations.

### Step 2: `capability.register` on Neural API

```json
{
  "jsonrpc": "2.0",
  "method": "capability.register",
  "params": {
    "capability": "ecology",
    "primal": "airspring",
    "socket": "/run/user/1000/biomeos/airspring-abc123.sock",
    "source": "startup",
    "semantic_mappings": {
      "et0_fao56": "science.et0_fao56",
      "water_balance": "science.water_balance",
      "yield_response": "science.yield_response"
    }
  },
  "id": 1
}
```

- `capability` — domain name (`ecology`, `game`, `science`, …)
- `primal` — spring identifier
- `socket` — absolute UDS path
- `source` — e.g. `"startup"`, `"graph"`
- `semantic_mappings` — semantic name → JSON-RPC method

Multiple domains: separate calls.

### Step 3: Incoming `capability.call`

```json
{
  "jsonrpc": "2.0",
  "method": "science.et0_fao56",
  "params": {
    "temperature_max": 30.5,
    "temperature_min": 18.2,
    "wind_speed": 1.8,
    "solar_radiation": 22.4
  },
  "id": 42
}
```

### Step 4: Deploy graphs — `capability_call` nodes

```toml
[[nodes]]
id = "compute-et0"
action = "capability_call"
params = { capability = "ecology.et0_fao56" }
depends_on = ["verify-airspring"]
```

### Minimal provider sketch

```rust
use std::os::unix::net::UnixListener;

fn main() -> std::io::Result<()> {
    let socket_path = format!(
        "{}/biomeos/myspring-{}.sock",
        std::env::var("XDG_RUNTIME_DIR").unwrap_or_else(|_| "/tmp".into()),
        std::env::var("FAMILY_ID").unwrap_or_else(|_| "dev".into()),
    );
    let listener = UnixListener::bind(&socket_path)?;
    register_capabilities(&socket_path);
    for stream in listener.incoming() {
        // ... JSON-RPC 2.0 ...
    }
    Ok(())
}
```

Production reference: ludoSpring `barracuda/src/ipc/server.rs`.

### Deploy graph node template

```toml
[[nodes]]
id = "germinate_myspring"
depends_on = ["germinate_beardog", "germinate_songbird"]
output = "myspring_genesis"
capabilities = ["mydomain"]

[nodes.primal]
by_capability = "mydomain"

[nodes.operation]
name = "start"

[nodes.operation.params]
mode = "server"
family_id = "${FAMILY_ID}"

[nodes.operation.environment]
BIOMEOS_SOCKET_DIR = "${XDG_RUNTIME_DIR}/biomeos"
FAMILY_ID = "${FAMILY_ID}"

[nodes.constraints]
timeout_ms = 15000

[nodes.capabilities_provided]
"mydomain.operation_a" = "mydomain.operation_a"
"mydomain.operation_b" = "mydomain.operation_b"
```

### Registry (`config/capability_registry.toml`)

```toml
[domains.mydomain]
provider = "myspring"
capabilities = ["mydomain", "sub_capability_1", "sub_capability_2"]

[translations.mydomain]
"mydomain.operation_a" = { provider = "myspring", method = "actual.method_a" }
"mydomain.operation_b" = { provider = "myspring", method = "actual.method_b" }
```

### Currently registered springs (representative)

| Spring | Domain | Notes |
|--------|--------|--------|
| wetSpring | `science` | diversity, Anderson, qs_model, kinetics, NMF |
| airSpring | `ecology` | ET₀, soil, crop, drought, biodiversity |
| ludoSpring | `game` | UI analysis, flow, Fitts, noise, WFC, accessibility |
| neuralSpring | `science` (shared) | spectral, Anderson, Hessian, training trajectory |
| healthSpring | `medical` | anatomy, tissue, surgical, biosignal, PK, epidemiology |
| groundSpring | `measurement` | soil moisture, pH, NPK, water quality, canopy, GPS, calibration |
| hotSpring | `physics` | MD, force fields, thermodynamics, energy |

### Streaming (v2.43+)

NDJSON: multiple response lines per request; consumer uses `AtomicClient::call_stream()`.

```
Client:  {"jsonrpc":"2.0","method":"measurement.soil_moisture","params":{...},"id":1}\n
Spring:  {"type":"Data","payload":{"sensor":"SM-001","value":42.3}}\n
         {"type":"Data","payload":{"sensor":"SM-002","value":38.1}}\n
         {"type":"End"}\n
```

Pipeline graphs: `graph.execute_pipeline` or auto-detect `pipeline` coordination.

### Sovereignty principles

- Springs are autonomous; registration is voluntary.
- biomeOS routes by capability, not hardcoded primal name.
- Springs may serve multiple domains; no privileged spring; routing via Neural API only.
- Deregister by shutting down the socket.

---

## Cross-Evolution

**Authority**: WateringHole consensus (primalSpring coordination validation). **Reference**: primalSpring v0.4.0 patterns (40 experiments, 8 tracks, sibling-spring absorptions).

### Core principles

1. **Springs never import each other.** Learning flows via wateringHole handoffs, shared barraCuda primitives, ecosystem standards, primalSpring composition experiments.
2. **Coordination through composition, not coupling.** Each spring is a primal; biomeOS discovers by capability; Neural API routes semantically; primalSpring validates composition.
3. **Evolution flows upstream.** Spring validates locally → handoff to wateringHole → other springs absorb → barraCuda absorbs math.

### Maturity path

```
Phase 0: Python baseline
Phase 1: Rust validation (bit-exact / tolerance-bounded)
Phase 2: barraCuda CPU (delegation via IPC)
Phase 3: barraCuda GPU (WGSL, toadStool dispatch)
Phase 4: Fused TensorSession pipeline
Phase 5: Sovereign dispatch (coralReef native)
```

**Write → Absorb → Lean** (GPU/WGSL): write locally → validate vs Python → handoff as absorption candidate → barraCuda canonicalizes → spring delegates upstream.

### Pattern absorption

| What | Flow | Example |
|------|------|---------|
| Validation patterns | Spring → wateringHole | `check_skip()`, `ValidationSink` |
| IPC resilience | Spring → wateringHole | `CircuitBreaker`, `RetryPolicy` |
| Math kernels | Spring → barraCuda | WGSL, precision routing |
| Discovery | biomeOS/primalSpring → springs | 5-tier discovery, capability parsing |
| MCP tools | Spring → Squirrel | Domain MCP tools |

### Handoff naming

```
{SPRING}_V{VERSION}_{TOPIC}_HANDOFF_{DATE}.md
```

Live in `wateringHole/handoffs/`; archive superseded under `handoffs/archive/`.

Handoff contents: executive summary; what origin provides; adoption list for receivers; learnings; evolution path; metrics; references.

### Neural API graph evolution

Steps per spring: define niche capabilities → TOML deploy graph with `by_capability` on nodes → JSON-RPC server → `capability_registry.toml` → integration tests → wateringHole handoff.

Niche contexts (examples): wet lab, dry lab, data science, CI/CD, edge — same spring, different graph emphasis.

### primalSpring coordination hub

primalSpring validates composition before wide adoption; documents handoffs; re-validates cross-spring composition.

Tracked metrics: capability registration (`health.liveness` + `capabilities.list`); deploy graph `by_capability`; JSON-RPC UDS; 5-tier discovery; handoff currency.

### Experiment tracks (template)

| Track | Validates |
|-------|-----------|
| 1 Atomic Composition | Primals deploy together |
| 2 Graph Execution | Coordination patterns |
| 3 Emergent Systems | Higher-order behavior |
| 4 Bonding & Plasmodium | Multi-gate coordination |
| 5 coralForge | Neural object pipeline |
| 6 Cross-Spring | Cross-spring data flows |
| 7 Showcase-Mined | Mined patterns |
| 8 Live Composition | Real multi-primal composition |

Use `check_skip` when dependencies absent — no fake passes.

### Compliance checklist

- [ ] `health.liveness`, `capabilities.list`
- [ ] Deploy graph with `by_capability` on all nodes
- [ ] 5-tier socket discovery
- [ ] JSON-RPC 2.0 over UDS
- [ ] Integration tests for live composition
- [ ] Current wateringHole handoffs
- [ ] Write → Absorb → Lean for GPU code
- [ ] No cross-spring Rust deps (IPC only)
- [ ] Zero C in app code (ecoBin); `#![forbid(unsafe_code)]` in app code

---

## Spring Interoperability

**Context**: esotericWebb — first garden attempting live multi-primal composition (squirrel, petaltongue, sweetgrass, rhizocrypt, beardog, nestgate, loamspine). Partial success; lessons codified in standards.

### What worked

- **Graceful degradation**: circuit breakers + retries; `degraded: true`; sensible defaults — springs SHOULD treat all primal calls as fallible.
- **Capability discovery**: scan `$XDG_RUNTIME_DIR/biomeos/` for domain sockets; env overrides (`SQUIRREL_ADDRESS`, etc.).
- **plasmidBin**: sterile transfer — `fetch.sh` / `harvest.sh`, `manifest.lock`.
- **Newline-delimited JSON-RPC** over streams — debuggable, fast when peers match.

### What failed — fixes and lessons

| Issue | Symptom / cause | Fix / norm |
|-------|-------------------|------------|
| HTTP JSON-RPC on TCP | rhizocrypt HTTP vs raw NDJSON | `PRIMAL_IPC_PROTOCOL` v3.1: NDJSON canonical; HTTP for external APIs |
| Abstract namespace sockets | `ls` misses `@name`; `readdir` blind | `CAPABILITY_BASED_DISCOVERY` v1.1: filesystem sockets required on Linux; abstract only as extra |
| Custom socket dirs | petaltongue off `$XDG/.../biomeos/` | Sockets under `$XDG_RUNTIME_DIR/biomeos/`; domain symlinks |
| Inconsistent CLI | `--port` vs `--jsonrpc-port`, etc. | `UNIBIN_ARCHITECTURE` v1.1: `{binary} server --port {port}` universal |
| Missing env | beardog exits without `FAMILY_ID` | Standalone defaults: `FAMILY_ID=standalone`, `NODE_ID=local` |
| Health names | squirrel `system.health` vs `health.liveness` | `SEMANTIC_METHOD_NAMING` v2.2: `health.*` required; may fallback with warning |
| Tokio nested runtime | ~~loamspine panic~~ **RESOLVED** (v0.9.16) | Was primal bug; fixed via `mdns-sd` migration (no `async-std` / `block_on`). |

### Sterile transfer surface

```
plasmidBin: fetch.sh, manifest.lock, metadata.toml per primal
$XDG_RUNTIME_DIR/biomeos/: primal.sock, domain.sock symlinks
Startup: fetch → launch `{binary} server --port` → health.liveness → discover by domain → compose → degrade on failure
```

### Recommendations for spring developers

1. Design for partial availability (circuit breakers, defaults).
2. Capability-based discovery (domains, not primal names).
3. Env overrides `{PRIMAL}_ADDRESS`.
4. Launch with `FAMILY_ID=standalone` `NODE_ID=local` when spawning primals.
5. `health.liveness` before use.
6. Log interop failures (method, transport, error).
7. Pin primals via `manifest.lock`.
8. Mock primals for tests (minimal JSON-RPC: `health.liveness` + needed methods).

**Related**: `PRIMAL_IPC_PROTOCOL` v3.1, `UNIBIN_ARCHITECTURE` v1.1, `CAPABILITY_BASED_DISCOVERY` v1.1, `SEMANTIC_METHOD_NAMING` v2.2, `IPC_COMPLIANCE_MATRIX.md`.

---

## Cross-Spring Data Flow

Canonical schema for time series in `capability.call` arguments — no ad-hoc negotiation.

### JSON shape

```json
{
  "schema": "ecoPrimals/time-series/v1",
  "variable": "soil_moisture_vol",
  "unit": "m3/m3",
  "source": {
    "spring": "airSpring",
    "experiment": "exp022",
    "capability": "ecology.water_balance"
  },
  "timestamps": ["2023-05-01T00:00:00Z", "2023-05-02T00:00:00Z"],
  "values": [0.32, 0.29],
  "metadata": { "location": "optional", "sensor": "optional" }
}
```

### Required fields

| Field | Type | Rule |
|-------|------|------|
| `schema` | string | `ecoPrimals/time-series/v1` |
| `variable` | string | snake_case |
| `unit` | string | SI or documented |
| `timestamps` | string[] | ISO 8601 UTC |
| `values` | number[] | f64, same length as timestamps |

### Optional: `source`, `metadata`

### Example exchanges

| From | To | Variable | Unit |
|------|-----|----------|------|
| airSpring | wetSpring | soil_moisture_vol | m3/m3 |
| ludoSpring | healthSpring | player_heart_rate | bpm |
| wetSpring | airSpring | microbial_diversity_index | dimensionless |

### Wrapped in `capability.call`

```json
{
  "capability": "science",
  "operation": "analyze_diversity",
  "args": {
    "time_series": {
      "schema": "ecoPrimals/time-series/v1",
      "variable": "soil_moisture_vol",
      "unit": "m3/m3",
      "source": { "spring": "airSpring", "experiment": "exp022", "capability": "ecology.water_balance" },
      "timestamps": ["2023-05-01T00:00:00Z", "2023-05-02T00:00:00Z"],
      "values": [0.32, 0.29],
      "metadata": {}
    }
  }
}
```

### Provenance note

In trio pipelines (e.g. airSpring → wetSpring → ToadStool), `source` may evolve toward sweetGrass braid references.

**Resolves**: SPRING_EVOLUTION_ISSUES ISSUE-010.

---

## Shader and Primitive Evolution

groundSpring delegates 11 functions to barraCuda; those primitives were hardened by four springs (hot, wet, neural, air) plus groundSpring validation patterns.

### Contribution summary (abbreviated)

- **hotSpring**: f64/DF64 infrastructure (`df64_core.wgsl`, `Fp64Strategy`, spectral/Anderson, sum_reduce_f64, CG patterns); March 2026: GPU f64 catastrophic cancellation in special functions (see Evolution Issues ISSUE-011).
- **wetSpring**: bio-stats (`FusedMapReduceF64`, `log_f64` fix, Gillespie, ridge, bray_curtis, ODE patterns).
- **neuralSpring**: dispatch (`domain_ops.rs`), spectral/chi²/KL fused GPU, `PipelineGraph`, NUCLEUS GPU, df64 streaming, composition pipelines.
- **airSpring**: Richards PDE, stats metrics, `pow_f64`/`acos` fixes, reduce buffer fix, `compile_shader_universal()`, seasonal/agronomic validation.
- **groundSpring**: `if let Ok` + CPU fallback, `ValidationHarness`, capability discovery, tolerance documentation; 2 WGSL shaders pending absorption.

### Multi-spring convergence

f64 precision (hot+wet+neural); bio ops; spectral; PRNG; validation patterns — merged in barraCuda.

### groundSpring delegation lineage (11 fns)

Examples: `pearson_r` → `stats::pearson_correlation`; `lyapunov_exponent` → `spectral::lyapunov_exponent` (hotSpring); `analytical_localization_length` → `special::localization_length` (wetSpring S52); see source doc for full table.

### Spectral GPU status (March 2026 snapshot)

WGSL: `anderson_lyapunov_f64`, `batch_ipr_f64`, `lanczos_iteration_f64`, `anderson_coupling_f64`, `fft_radix2_f64`, etc. Gaps: fully GPU-resident Lanczos, `tridiag_eigh` GPU, large-N Lanczos, SciPy/Kokkos comparison harnesses.

### coralReef (Iter 23+) — inputs

| Language | API | Use |
|----------|-----|-----|
| WGSL | `compile_wgsl()` / `compile_wgsl_full()` | Primary; df64 preamble for WGSL |
| SPIR-V | `compile()` | Binary interchange |
| GLSL 450 | `compile_glsl()` | Legacy compute absorption |

Iteration 23 added: tanh, fract, sign, dot, mix, step, smoothstep, length, normalize, cross, trunc (among others). **Spring guidance**: author WGSL in barraCuda; use GLSL only for absorption; hotSpring/neuralSpring: GLSL fixtures in `tests/fixtures/glsl/`; WGSL corpus paths as in source doc.

Known SPIR-V frontend gaps: `Discriminant` switch-like patterns; non-literal const init — use WGSL or runtime init.

### Benchmark impact (groundSpring)

V7 pre-S50: +6% overhead vs local; V9 post-S62: ~0% — link/init overhead reduced.

### barraCuda v0.3.5+ evolution highlights

wgpu 22→28; `Fp64Strategy`; DF64 fused shaders; `TensorContext` fast path; 5-accumulator Pearson; 31 bio ops; 3-tier precision model; cross-pollination chains (hot→df64→neural/wet, etc.).

---

## Compute Trio Integration

**Primals**: barraCuda (math), coralReef (compiler), toadStool (hardware). Springs consume barraCuda; do not call coralReef/toadStool for math directly — trio coordinates internally.

### Roles

| Primal | Owns |
|--------|------|
| barraCuda | WGSL shaders, precision tiers, `PrecisionBrain`, `op_preamble` |
| coralReef | WGSL/SPIR-V/GLSL → native GPU binary |
| toadStool | VFIO, DMA, GPU lifecycle, tensor/RT cores |

### Decision tree

- Need GPU math → `barracuda` dependency → `PrecisionBrain::recommend(domain)`; sovereign-dispatch; `GpuPool` / `MultiDevicePool`; custom shaders → `compute.dispatch` IPC.

**Cargo** (examples):

```toml
barracuda = { path = "../barraCuda/crates/barracuda" }
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false, features = ["gpu"] }
barracuda = { path = "../barraCuda/crates/barracuda", default-features = false }
```

**IPC**: `barracuda server --bind 127.0.0.1:9000` → `compute.dispatch` via JSON-RPC.

### 15-tier precision (conceptual ladder)

Scale-down (Binary…TF32) → F32 → scale-up (DF64, F64, F64Precise, QF128, DF128). Springs use `PhysicsDomain` + `PrecisionBrain::route()` — **do not** hardcode tiers.

### Compile → dispatch chain (conceptual)

Spring → `barraCuda.compute.dispatch` → preamble/tier → coralReef compile → toadStool submit → result. On shader compile error: tier cascade; on `DeviceLost`: alternate GPU + recompile; on VRAM: halve batch.

### Springs must NOT

1. Call coralReef directly for compilation (barraCuda owns `shader.compile` path).
2. Call toadStool directly for dispatch.
3. Hardcode precision tiers.
4. Write raw WGSL without checking the shader library (~816 shaders at time of guide).
5. Parse primal names — use capabilities.

### Feature matrix (abbreviated)

| Feature | Library | IPC | Sovereign |
|---------|---------|-----|-----------|
| Math | Direct API | JSON-RPC | JSON-RPC |
| Precision | `PrecisionBrain` | `device.probe` | `PrecisionBrain` |
| Custom shaders | `compile_shader()` | `compute.dispatch` | compile → dispatch |

### Version compatibility (guide)

| barraCuda | coralReef | toadStool |
|-----------|-----------|-----------|
| v0.3.11+ | Iter 70+ | S168+ |
| v0.3.5–0.3.10 | Iter 50+ | S156+ |

**Coordinator routing**: math gaps → barraCuda; compilation → coralReef; hardware → toadStool; integration in spring → spring.

**References**: `PRECISION_TIERS_SPECIFICATION.md`, `ARCHITECTURE_DEMARCATION.md`, `BARRACUDA_LEVERAGE_GUIDE.md`, `CORALREEF_LEVERAGE_GUIDE.md`, `TOADSTOOL_LEVERAGE_GUIDE.md`.

---

## Evolution Issues

**Purpose**: Track cross-primal / biomeOS / ToadStool gaps. **Lifecycle**: OPEN → ACKNOWLEDGED → IN_PROGRESS → RESOLVED / WONT_FIX.

### Resolved (summary)

| ID | Topic | Resolution notes |
|----|-------|------------------|
| ISSUE-001 | Ecology domain missing | `ecology` in registry (biomeOS v2.33+), 30+ translations |
| ISSUE-002 | Async-only Neural API client | `neural-api-client-sync`; `NeuralBridge::discover()`, `capability_call()` |
| ISSUE-003 | `capability.call` param formats | Canonical `{capability, operation, args}`; dotted sugar; `params` alias |
| ISSUE-004 | Cross-primal pipeline E2E | Graphs + `cross_spring_pipeline_e2e.rs` |
| ISSUE-005 | Safe UID without `unsafe` | `biomeos-types::paths::safe_uid()` via `/proc/self/status` |
| ISSUE-007 | Spring-as-provider docs | This pattern (see Spring-as-Provider) |
| ISSUE-010 | Cross-spring θ(t) format | `ecoPrimals/time-series/v1` (Cross-Spring Data Flow) |

### Open (representative)

| ID | Priority | Problem / proposed direction |
|----|----------|------------------------------|
| ISSUE-006 | P2 | NPU convergence — absorb substrate model into ToadStool; `probe_npus()`, `SubstrateKind::Npu`, GPU>NPU>CPU |
| ISSUE-008 | P2 | ET₀ GPU: Thornthwaite, Makkink, Turc, Hamon — `BatchedElementwise` op codes |
| ISSUE-009 | P3 | JSON benchmark schema — shared `benchmark_schema.json` in wateringHole |
| ISSUE-011 | P1 | GPU f64 catastrophic cancellation in special functions — barraCuda stable primitives; coralReef `NoContraction`; springs: range diagnostics — see `GPU_F64_NUMERICAL_STABILITY.md` |
| ISSUE-012 (rhizoCrypt) | P3 | Content similarity index — LSH; spring participation phases A–C |
| ISSUE-013 (sweetGrass) | P3 | Content convergence / provenance intersection — `ContentConvergence`; coordinate with ISSUE-012 |
| ISSUE-022 | P2 | Root privilege in coralReef GPU lifecycle — fd-passing / thin privileged launcher |
| ~~ISSUE-011 (ludo)~~ | ~~P1~~ | ~~rhizoCrypt no UDS~~ — RESOLVED (session 23): `--unix` shipped, dual-mode TCP+UDS, `biomeos/rhizocrypt.sock` |
| ~~ISSUE-012 (ludo)~~ | ~~P1~~ | ~~loamSpine runtime nesting panic~~ — RESOLVED (v0.9.16): `mdns` 3.0 → `mdns-sd` 0.19; no `block_on`, no `async-std` |
| ISSUE-013 (ludo) | P2 | Fitts/Hick formula mismatch vs Python — `variant` param or align defaults |
| ISSUE-014 | P2 | Neural API not registering many primal capabilities — self-register or probe `capabilities.list` |
| ISSUE-015 | P3 | NestGate JWT secret length in `start_primal.sh` — use longer secret |

Note: numbering overlaps exist between biomeOS-integration block (ISSUE-001–015) and ludoSpring block (ISSUE-011–015) in the source doc — treat IDs as labeled in `SPRING_EVOLUTION_ISSUES.md` when filing.

### Contributing template

```markdown
### ISSUE-NNN: Title
**Reporter**: Spring (version)
**Affects**: ...
**Priority**: P1 / P2 / P3
**Problem**: ...
**Proposed fix**: ...
**Evidence**: ...
**Status**: OPEN | ...
```

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | 2026-04-04 | Consolidated seven wateringHole spring pattern documents into this single reference. |
| (prior) | 2026-03-16 — 2026-03-30 | Per-source file versions and dates preserved in git history of individual files. |
