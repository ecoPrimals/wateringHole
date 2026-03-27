# barraCuda Leverage Patterns

**Version**: 1.0.0
**Date**: 2026-03-17
**Status**: Active — inter-primal guidance for leveraging barraCuda's math compute

---

## What barraCuda Is

barraCuda is the GPU-accelerated math engine for the ecoPrimals ecosystem.
It owns **the math and nothing else**: WGSL shader authoring, precision
strategy (15-tier from Binary to DF128), naga IR optimisation, CPU fallback,
and numerical tolerance architecture.

barraCuda does not handle hardware discovery, shader compilation to native
ISA, networking, storage, encryption, UI, or orchestration. Each of those
belongs to the primal that owns that domain.

---

## Local Primal — barraCuda Standalone

Any spring can depend on the `barracuda` crate directly for local,
in-process math. No IPC, no other primals required.

### Direct Crate Dependency

```toml
[dependencies]
barracuda = { version = "0.3", default-features = false }
```

Feature flags control what is compiled:

| Feature | What it enables |
|---------|----------------|
| `gpu` | wgpu device, WGSL dispatch, GPU ops |
| `domain-nn` | Neural network layers, attention, ESN |
| `domain-pde` | PDE solvers, Richards, Crank-Nicolson |
| `domain-genomics` | DADA2, HMM, Smith-Waterman |
| `domain-esn` | Echo state networks |
| `domain-snn` | Spiking neural networks |
| `domain-timeseries` | Time series, autocorrelation |
| `domain-vision` | Convolution, pooling |
| `parallel` | rayon CPU parallelism |
| `serde` | Serialization for IPC types |

### What You Get Locally (no other primals)

- **806 WGSL shaders** covering linear algebra, spectral methods, statistics,
  special functions, molecular dynamics, optimization, FHE, and domain ops
- **CPU fallback** for every GPU op (automatic when no GPU available)
- **13-tier tolerance architecture** with named scientific tolerances
- **Precision routing** via `PrecisionBrain` — domain-aware tier selection
- **Zero unsafe code** — `#![forbid(unsafe_code)]`

### Local Usage Examples

```rust
// GPU-accelerated eigenvalue decomposition
let eigenvalues = barracuda::spectral::lanczos_extremal(&matrix, k)?;

// CPU-side special functions
let w = barracuda::special::plasma_dispersion::w(z);

// Dose-response modeling
let response = barracuda::ops::hill_function_f64(&doses, emax, k, n, &device)?;
```

---

## The Compute Trio — barraCuda + coralReef + toadStool

The compute trio is the sovereign GPU pipeline. Each primal contributes its
layer; no primal crosses into another's domain.

```
barraCuda (Layer 1 — WHAT to compute)
    Owns: WGSL shaders, precision strategy, naga IR optimisation
    Produces: Optimised WGSL source, shader metadata, tolerance specs
    ↓ shader.compile.* IPC
coralReef (Layer 2-3 — HOW to compile)
    Owns: SPIR-V/WGSL → native GPU binary (SASS, RDNA2+, coralDriver)
    Produces: Native binaries, architecture-specific optimisation
    ↓ compute.dispatch.* IPC
toadStool (Layer 3-4 — WHERE to run)
    Owns: Hardware discovery, GPU/NPU/CPU dispatch, VFIO, DMA
    Produces: Execution results, hardware capability manifests
    ↓ results
```

### How a Spring Uses the Trio

A spring never coordinates the trio directly. It calls barraCuda; barraCuda
discovers coralReef and toadStool at runtime via capability-based IPC.

```rust
// Spring code — only talks to barraCuda
let result = barracuda::ops::gemm_f64(&a, &b, &device)?;

// Internally, if sovereign-dispatch feature is active:
// 1. barraCuda sends WGSL to coralReef (shader.compile.wgsl)
// 2. coralReef returns native binary
// 3. barraCuda sends binary to toadStool (compute.dispatch.submit)
// 4. toadStool dispatches on best available GPU via VFIO
// 5. Results flow back through the same path

// If coralReef/toadStool unavailable, barraCuda falls back to wgpu
```

### Trio Capabilities

| Capability | Who Provides | Discovery Method |
|-----------|-------------|-----------------|
| `shader.compile` | coralReef | `$XDG_RUNTIME_DIR/ecoPrimals/*.json` capability scan |
| `compute.dispatch` | toadStool | Same capability scan |
| `math.*` | barraCuda | Local crate or barraCuda IPC |

---

## Wider Primal Combinations

### barraCuda + BearDog — Encrypted Compute

BearDog owns cryptography. barraCuda owns math. Together they enable
fully homomorphic encryption on GPU.

**Pattern**: BearDog encrypts → barraCuda computes on ciphertext → BearDog decrypts

```
Spring (e.g. healthSpring patient data)
    ↓ plaintext
BearDog: FHE encrypt (lattice-based)
    ↓ ciphertext polynomials
barraCuda: GPU NTT → pointwise mul → INTT (all on ciphertext)
    ↓ encrypted result
BearDog: FHE decrypt
    ↓ plaintext result
```

**barraCuda provides**: `fhe_ntt`, `fhe_intt`, `fhe_pointwise_mul` GPU ops,
NTT butterfly shaders, modular arithmetic.

**Novel combinations**:
- healthSpring: encrypted patient PK/PD on shared compute
- wetSpring: encrypted metagenomic diversity on multi-tenant cloud
- neuralSpring: private model inference without exposing weights

---

### barraCuda + Songbird — Distributed Compute

Songbird owns networking. barraCuda owns math. Together they enable
multi-node GPU compute without either primal knowing the other's internals.

**Pattern**: Songbird discovers remote nodes → toadStool routes to best GPU → barraCuda runs

```
Spring (e.g. hotSpring plasma simulation)
    ↓ dispatch request
biomeOS: routes to Songbird for cross-node
    ↓ BirdSong federation
Songbird: discovers remote barraCuda instances
    ↓ JSON-RPC over TLS
Remote toadStool: dispatches to best GPU
    ↓ VFIO
Remote barraCuda: executes WGSL shaders
    ↓ results via Songbird
```

**Novel combinations**:
- hotSpring: lattice QCD across GPU cluster (RHMC + multi-shift CG)
- neuralSpring: distributed training with gradient reduction shaders
- groundSpring: embarrassingly parallel bootstrap resampling across nodes

---

### barraCuda + NestGate — Deterministic Computation Cache

NestGate owns content-addressed storage. barraCuda produces deterministic
results from deterministic inputs. Together they eliminate redundant compute.

**Pattern**: Hash(shader + params + input) → NestGate lookup → miss → compute → store

```
Spring (e.g. groundSpring Anderson localization)
    ↓ same Hamiltonian parameters
barraCuda: blake3(shader_source || params || input_data)
    ↓ content hash
NestGate: storage.get(hash)
    ↓ cache hit → return cached eigenvalues
    ↓ cache miss → barraCuda computes → NestGate: storage.put(hash, result)
```

**Novel combinations**:
- hotSpring: Hofstadter butterfly cached by magnetic flux parameter
- airSpring: ET₀ cached by (date, station, method) tuple
- wetSpring: OTU tables cached by (sequence_hash, params)

---

### barraCuda + petalTongue — Visualised Computation

petalTongue owns representation. barraCuda owns math. Together they enable
real-time scientific visualisation without either crossing domains.

**Pattern**: barraCuda computes → petalTongue renders with compute offload

```
Spring (e.g. hotSpring spectral analysis)
    ↓ eigenvalue data
barraCuda: Lanczos + IPR + level spacing → spectral summary
    ↓ structured results
petalTongue: Grammar of Graphics renderer
    ↓ delegates heavy tessellation/projection back
barraCuda: math.tessellate.*, math.project.*
    ↓ vertex data
petalTongue: final render (GPU, terminal, web, audio)
```

**Novel combinations**:
- healthSpring: interactive population PK VPC plots with live Monte Carlo
- groundSpring: Anderson localization phase diagram with IPR heatmap
- ludoSpring: procedural terrain with GPU Perlin noise + real-time erosion

---

### barraCuda + sweetGrass — Attributed Computation

sweetGrass owns provenance. barraCuda produces results. Together they ensure
every computation has a traceable attribution chain.

**Pattern**: Record provenance braid before dispatch; record derivation after

```
Spring (e.g. wetSpring metagenomics)
    ↓ 16S amplicon reads
sweetGrass: prov.record(Agent=wetSpring, Activity=diversity_analysis)
    ↓ provenance braid ID
barraCuda: GPU Shannon/Simpson/Chao1 diversity indices
    ↓ results + braid ID
sweetGrass: prov.derive(input=reads, output=diversity, activity=braid_id)
    ↓ immutable attribution chain
```

**Novel combinations**:
- healthSpring: FOCE gradient provenance for regulatory audit trails
- neuralSpring: training provenance (data → model → prediction chain)
- airSpring: irrigation decision provenance (sensor → ET₀ → schedule)

---

### barraCuda + rhizoCrypt — Recoverable Computation

rhizoCrypt owns ephemeral working memory. barraCuda produces intermediate
results. Together they enable fault-tolerant long-running GPU pipelines.

**Pattern**: Checkpoint intermediate state → recover on failure → resume

```
Spring (e.g. hotSpring long RHMC trajectory)
    ↓ 10,000-step HMC integration
barraCuda: every N steps → checkpoint state to rhizoCrypt
    ↓ GPU device lost (driver crash, OOM)
rhizoCrypt: provides last checkpoint
    ↓ state restored
toadStool: migrates to next available GPU
    ↓ resumed
barraCuda: continues from checkpoint
```

**Novel combinations**:
- neuralSpring: training checkpoint/resume across GPU failures
- hotSpring: plasma simulation recovery (Vlasov 6D phase space)
- groundSpring: long eigensolve recovery (Lanczos with 10K iterations)

---

### barraCuda + Squirrel — AI-Guided Computation

Squirrel owns AI coordination. barraCuda owns compute. Together they enable
adaptive experiment design where AI proposes and math validates.

**Pattern**: Squirrel proposes → barraCuda computes → Squirrel interprets → next proposal

```
Spring (e.g. airSpring precision irrigation)
    ↓ soil sensor readings
Squirrel: interprets context → proposes ET₀ parameters
    ↓ parameter set
barraCuda: batch GPU ET₀ (8 methods × N fields)
    ↓ results
Squirrel: selects best method per field → proposes schedule
    ↓ irrigation schedule
```

**Novel combinations**:
- healthSpring: Bayesian dose optimization (Squirrel proposes dose → barraCuda simulates PK)
- groundSpring: adaptive sampling (Squirrel identifies uncertainty → barraCuda evaluates)
- wetSpring: metagenomic anomaly investigation (Squirrel flags → barraCuda deep-dives)

---

### barraCuda + skunkBat — Defended Computation

skunkBat owns defensive security. barraCuda computes. Together they ensure
computational integrity under adversarial conditions.

**Pattern**: skunkBat monitors → barraCuda computes → skunkBat verifies

**Novel combinations**:
- ludoSpring: anti-cheat physics validation (barraCuda replays, skunkBat compares)
- BearDog + barraCuda + skunkBat: encrypted compute with integrity monitoring
- healthSpring: tamper-evident clinical computation audit

---

## Multi-Primal Compositions

### Sovereign Encrypted Compute Stack

```
BearDog (encrypt) → barraCuda (compute) → coralReef (compile) →
toadStool (dispatch) → sweetGrass (attribute) → NestGate (store)
```

Six primals, zero shared state, each discovered by capability at runtime.

### Fault-Tolerant Distributed Science

```
Songbird (network) → toadStool (discover GPU cluster) →
barraCuda (compute) → rhizoCrypt (checkpoint) →
sweetGrass (provenance) → LoamSpine (permanent record)
```

### Interactive Real-Time Analysis

```
petalTongue (UI input) → Squirrel (interpret intent) →
barraCuda (compute) → petalTongue (render) →
sweetGrass (record interaction provenance)
```

---

## Guidelines for Springs

### Using barraCuda from Your Spring

1. **Depend on the crate** for local math: `barracuda = "0.3"`
2. **Use feature flags** to compile only what you need
3. **Let precision routing handle tiers** — call `PrecisionBrain::compile()`
4. **Tolerance architecture** — use named tolerances, never magic numbers
5. **GPU ops return `Result`** — handle `DeviceLost` gracefully

### Discovering barraCuda via IPC

If your spring runs as a separate process and needs barraCuda's compute:

1. Scan `$XDG_RUNTIME_DIR/ecoPrimals/*.json` for `"math.compute"` capability
2. Connect via JSON-RPC 2.0 (preferred) or tarpc (high-throughput)
3. Methods follow `barracuda.{operation}` semantic naming
4. All methods are idempotent; safe to retry on transient failure

### What NOT to Do

- Do not hardcode `"barraCuda"` as a primal name — discover by capability
- Do not import barraCuda's internal modules — use the public API
- Do not implement your own WGSL shaders if barraCuda has the op
- Do not bypass precision routing — it exists for numerical safety
- Do not store GPU state across IPC calls — GPU buffers are ephemeral

---

## References

- `PRIMAL_IPC_PROTOCOL.md` — JSON-RPC 2.0 + tarpc transport standard
- `UNIBIN_ARCHITECTURE_STANDARD.md` — single-binary conventions
- `ECOBIN_ARCHITECTURE_STANDARD.md` — pure Rust, zero C deps
- `SEMANTIC_METHOD_NAMING_STANDARD.md` — `domain.operation` method naming
- `SPRING_AS_PROVIDER_PATTERN.md` — capability-based discovery, sovereignty
- `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — AGPL-3.0 licensing
- `barraCuda/specs/BARRACUDA_SPECIFICATION.md` — crate architecture
- `barraCuda/specs/PRECISION_TIERS_SPECIFICATION.md` — 15-tier precision ladder
