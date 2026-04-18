# GPU and Compute Evolution — Sovereign Stack Guidance

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | April 4, 2026 |
| **Status** | Active |

---

## Sovereign Compute Vision

**Source lineage**: `SOVEREIGN_COMPUTE_EVOLUTION.md` (March 12, 2026 and updates).

### Goal

Replace every non-Rust dependency in the GPU compute path with sovereign Rust implementations, scaffolded from open-source systems. **Dual-use hardware**: the same machine runs gaming and science. Validation target: **CERN-grade reproducible physics at home**, scalable to CERN (`hotSpring/SOVEREIGN_VALIDATION_GOAL.md`).

### Security and performance posture (March 12)

- Software enclave via BearDog (encryption) + toadStool (VFIO exclusivity) + Rust (memory safety); no MIG required for trusted workloads.
- VFIO dispatch path projects **~4,000 steps/s** Yukawa vs Kokkos **2,630** (DF64 **9.9×** gain + direct GPFIFO). Precision-mix advantage is unique to ecoPrimals vs Kokkos.
- toadStool tree model: cross-GPU learning and software-defined GPU partitioning on any PCIe GPU.

### Stack comparison

**Current (March 2026)**

| Layer | Component | Language | Owner |
|-------|-----------|----------|-------|
| 6 | barraCuda | Rust | WE OWN |
| 5 | naga | Rust | Mozilla |
| 4 | wgpu | Rust | gfx-rs |
| 3 | Vulkan API | C | Khronos |
| 2 | NVK | C+Rust | Mesa |
| 1 | NAK | Rust | Mesa |
| 0 | nouveau | C | Linux |

**Target (Sovereign)**

| Layer | Component | Notes |
|-------|-----------|--------|
| 6 | barraCuda | Math, shaders, precision |
| 5 | naga (fork) | WGSL → SPIR-V + direct ISA |
| 4 | wgpu / coralGpu | WE OWN |
| 3 | (optional) | Minimal Vulkan-compatible dispatch |
| 2 | coralDriver | WE OWN (replaces NVK) |
| 1 | coralNak | WE OWN (replaces NAK) |
| 0 | vfio-pci / kmod | WE OWN |
| -1 | coral-power | Glow plug, PMU |

Every layer pure Rust in the target; hardware interchangeable; math sovereign.

### Primal ownership (summary)

| Layer | Component | Owner | Status (snapshot) |
|-------|-----------|-------|-------------------|
| 6 | WGSL f64/DF64, Fp64Strategy, sovereign compiler | barraCuda | Production |
| 5 | WGSL ↔ naga | barraCuda | Upstream naga |
| 5 | WGSL → ISA direct | coralReef | Level 3 roadmap |
| 4 | wgpu fork, hardware discovery | toadStool | Partial |
| 2 | Userspace driver | groundSpring | Level 4 |
| 1 | SPIR-V → ISA, f64 polyfills | barraCuda / coralNak | Mixed |
| 0 | VFIO, thin kmod | toadStool / groundSpring | In progress |

### Evolution levels (condensed)

| Level | Scope | Status |
|-------|--------|--------|
| **1** | WGSL polyfills, `compile_shader_f64`/`df64`, Fp64Strategy, NVK workarounds | Complete; gap vs Kokkos-CUDA closed **27× → 3.7×** (93%); Verlet/cell-list wired |
| **2** | coralReef sovereign compiler (NAK roots), DRM, coralGpu, tarpc/bincode | Complete — SM35/SM70/SM120 compile parity, QMD v5.0, f64 lowering all gens; remaining: dispatch wiring (GAP-HS-031), FECS path |
| **3** | Standalone coralNak, WGSL → ISA direct, multi-arch | Partial |
| **4** | coralDriver, coralMem, coralQueue, vfio backend, thin kmod | Core: VFIO glow plug + PBDMA context load proven; full runtime 3–6 mo class |

Estimated scaffolding: Level 1 days; Level 2 2–4 weeks; Level 3 1–2 months; Level 4 3–6 months (from source doc).

### Layer status (March 17 catchup)

- **Layers -1–1** (power, glow plug, BAR2): Complete; coral-glowplug production-grade; VFIO-first; boot-persistent.
- **Layers 2–4** (PFIFO, runlist, GR context): Blocked — MMU fault buffers → runlist encoding → PBDMA activation → FECS/GPCCS context (see Bring-Up Guide).
- **Layer 5** (shader compilation): Operational — coralReef 1314+ coral-reef tests, WGSL→SASS SM35/SM70/SM120 (Kepler→Blackwell), AMD gfx1030/1100/90a. f64 transcendental lowering fixed for all NVIDIA generations. QMD v5.0 for Blackwell. 10/10 HMC pipeline shaders compile on all 3 GPU generations (hotSpring Exp 176).
- **Layer 6** (math/shaders): barraCuda v0.3.5 class, large test counts per source.
- **toadStool**: Partial — GlowPlug socket client, VFIO sysmon, hw-learn feed gaps per source.

**Critical path**: coralReef Gaps 2→3→4→5 (P1); NVK bridge interim (Mesa build / `libvulkan_nouveau.so` on some distros).

### Cross-primal cycle

Springs validate → barraCuda (precision, shaders) → toadStool (discovery, vfio) → groundSpring (driver/DMA) → springs.

### Hardware strategy

Consumer GPUs **1/64 f64**; proprietary support for older HW may fade. **DF64** on f32 ALUs makes consumer GPUs viable for science; **coralDriver** keeps Titan V / deprecated HW usable.

| Hardware | Proprietary | Sovereign |
|----------|-------------|-----------|
| Titan V | nvidia.ko | coralDriver |
| RTX 3090/5090 | nvidia + CUDA | coralDriver + DF64 |
| AMD RDNA3 | amdgpu + ROCm | coralDriver + coralAco |
| Intel Arc | i915 + oneAPI | coralDriver + coralAnv |

### Validation targets (9 PP Yukawa DSF)

| Test | Python | barraCuda CPU | barraCuda GPU (L1 f64) | Kokkos-CUDA |
|------|--------|---------------|-------------------------|-------------|
| Steps/s | 33 | ~5,000 | 27 | 730–3,700 |
| Energy drift | 0.000% | 0.000% | 0.001% | TBD |

Targets: L1 DF64+cell ~1,400; L2 NAK fix ~2,500; L4 sovereign ~4,000+ steps/s.

### Dual-use (gaming + science)

Multi-GPU: one GPU nvidia/display, one VFIO/science. Single-GPU: toadStool switches bind (nvidia ↔ vfio). Phases: validate BAR0+nouveau → UVM → VFIO backend → `ecoprimals-mode` CLI → dynamic arbitration.

### Naming: **coral** prefix

coralNak, coralAco, coralDriver, coralMem, coralQueue, coralGpu.

### Sovereignty gap: root privilege

Open: VFIO, sysfs bind/unbind, systemd, udev, sudoers — evolution toward fd-passing, minimal syscalls, long-term VFIO-user/io_uring-style handles.

### Related (pointers)

`PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md`, handoffs: trio wiring, BAR0 dual-use, GPU security/VFIO/Kokkos, CUDA oracle debugging, `hotSpring/SOVEREIGN_VALIDATION_GOAL.md`, `barraCuda/PURE_RUST_EVOLUTION.md`.

---

## GPU Bring-Up Guide

**Source lineage**: `GPU_SOVEREIGN_BRING_UP_GUIDE.md` — VFIO / pure Rust, Volta-focused experiments 058–061; hardware: **2× Titan V (GV100, SM70), RTX 5060 (GB206, SM120)**; primals: coralReef, toadStool, barraCuda.

### Purpose

Bring GPU from cold silicon to sovereign dispatch: **no kernel driver, no firmware blobs, no proprietary libraries** (target architecture); patterns vendor-agnostic; specifics NVIDIA Volta where stated.

### Power is active

| Event | Time | Effect |
|-------|------|--------|
| Driver unbind | Immediate | PCIe runtime PM → D3hot (BAR0 → `0xFFFFFFFF`) |
| D3hot idle | ~2 s | Internal clock gating (PMC_ENABLE → `0x40000020`) |
| D3cold allowed | Variable | VRAM off (`0xBAD0ACxx`) |

VFIO on cold GPU: reads garbage unless warmed.

### Five-layer warm-up

```
Layer 0: PCIe Power     — D3 → D0 (PMCSR)
Layer 1: Engine Clocks  — PMC_ENABLE → 0xFFFFFFFF
Layer 2: BAR2 Aperture  — V2 MMU in VRAM, BAR2_BLOCK
Layer 3: PFIFO/PBDMA    — interrupts, fault buffers, scheduler
Layer 4: Channel Load   — instance block, runlist, INST_BIND, context switch
```

### BAR2 self-warm (Experiment 060)

Complete V2 MMU page table in VRAM via PRAMIN (BAR0 `0x700000`), program BAR2_BLOCK from Rust — **byte-identical** to nouveau warm-up: **12/54** experiments schedule, **0** faulted, **3** expected CHSW failures. Glow plug ~**60 ms** from cold; state can be cleaner than nouveau.

### Desktop Volta and PMU

**No signed PMU firmware** for desktop Volta (Titan V); nouveau uses stub; power = **BAR0 register writes**. **Not** true for Turing+ (GSP firmware).

### D3hot vs HBM2 (corrected 2026-03-15)

**D3hot does not erase HBM2 training.** BAR0 disabled (`0xFFFFFFFF` reads); **PMCSR[1:0]=00 → D0** restores BAR0; VRAM alive. **`0xBAD0ACxx`** was misread BAR0 in D3hot, not necessarily bad VRAM. **D3cold** loses training — remove/rescan / boot ROM devinit.

Workaround (fragile): `power/control=on`, `d3cold_allowed=0` before VFIO bind. **Sovereign long-term**: Rust-native MC init (largest gap historically).

### mmiotrace (Experiment 061)

**206,375** MMIO ops on nouveau bind: **18,928** BAR0 writes, **39,489** reads, **359** offsets; **zero** PMU FALCON uploads; **no** FBPA/LTC/PCLOCK/PMU memory init; nouveau assumes UEFI POST — **cannot cold-POST**.

### VBIOS scripts

PROM at BAR0+`0x300000`: BIT **'I'** init ~`0x4934`; boot scripts ~`0x76A2` (~18,100 bytes); opcode table ~`0x48F4`; PMU FW encrypted. Paths: FALCON upload or **~2000** lines host interpreter for plaintext scripts.

### Interpreter: 7-layer probe chain

L0 BAR → L1 Identity → L2 Power → L3 Engines → L4 DMA → L5 Channel → L6 Dispatch. Typed evidence between layers.

### Bug table (samples)

| Bug | Layer | Fix summary |
|-----|-------|-------------|
| PFIFO_ENABLE reads 0 | L2 | GV100: PFIFO via PMC bit 8 |
| BAR2_BLOCK invalid | L3 | Glow plug page tables |
| PBDMA-runlist map | L3 | `PBDMA_RUNL_MAP` bitmask |
| Runlist register | L4 | Per-RL `0x2270+id*0x10`, not global `0x2270` only |
| Runlist submit | L4 | `(count<<16)|upper_addr`, not `(rl_id<<20)|count` |
| MMU fault buffer | L3 | Sysmem DMA, not VRAM PRAMIN |
| PRAMIN `0xBAD0ACxx` | L4 | D3cold / FB off |

### Runlist (GV100)

```
BASE  = 0x2270 + runlist_id * 0x10   // lower_32(vram_addr >> 12)
SUBMIT = 0x2274 + runlist_id * 0x10  // upper_32(vram_addr >> 12) | (entry_count << 16)
```

### Full bring-up stack (status)

| Capability | Status |
|------------|--------|
| PCIe D0 | Done |
| PMC_ENABLE / clocks | Done (glow plug) |
| BAR2 V2 MMU | Done (glow plug) |
| PFIFO/PBDMA | Partial |
| MMU fault buffers | Partial/broken in probe path |
| Channel/dispatch | Gaps 2–4 |
| HBM2 after vfio | **Solved**: `devinit::force_pci_d0(bdf)` in `RawVfioDevice::open()`; GlowPlug D0; pipeline: vfio → D0 → VFIO → GlowPlug → BAR2 → warm |

### Priority order (sovereign dispatch)

1. ~~HBM2/FB init~~ — D0 force (normal); D3cold: rescan / VBIOS scripts (**577** writes, **237** HBM2-critical) / oracle / PMU where applicable.
2. Runlist submission (correct regs + encoding).
3. MMU fault buffers (sysmem, correct HI/enable).
4. GP_GET advance (PBDMA stall — likely tied to 2–3).
5. NOP dispatch → QMD compute.
6. Multi-arch (RTX 5060, MI50, etc.).

### Tools

| Tool | Status |
|------|--------|
| mmiotrace | Proven (**206K** ops) — persist to `hotSpring/data/`, not `/tmp` |
| VBIOS reader | Working |
| BIT parser | Working |
| Oracle diff | Working (not sufficient alone) |
| Diagnostic matrix | **54** experiments |
| BAR2 glow plug | Nouveau parity |

### Register quick reference (NVIDIA samples)

**Power**: PMC_ENABLE `0x0200` (cold `0x40000020`, warm `0x5fecdff1`, write `0xFFFFFFFF`); PFIFO_ENABLE `0x2200` N/A GV100; GPU_TEMP `0x20460`.

**PFIFO**: PBDMA_MAP `0x2004`; RL_BASE(id) `0x2270+id×0x10`; RL_SUBMIT(id) `0x2274+id×0x10`; SCHED_DISABLE `0x2630`.

**BAR**: BAR0_WINDOW `0x1700`; BAR2_BLOCK `0x1714`; etc.

**MMU fault**: FAULT_BUF0_LO `0x100E24`; FAULT_BUF1_LO `0x100E44`; FAULT_STATUS `0x100A2C`.

### GlowPlug Metal Explorer (vendor-agnostic)

Modules: `pci_discovery.rs`, `bar_cartography.rs`, `gpu_vendor.rs` (`GpuMetal`), `nv_metal.rs`, `amd_metal.rs` stub. `force_pci_d0()` in `pci_discovery.rs`. Tests: `vfio_metal_cartography`, `vfio_pci_discovery`, `vfio_power_bounds` with `CORALREEF_VFIO_BDF=...`.

### PCLOCK secure boot barrier (Volta)

Domains return PRI errors (`0xBADF5040` PLL, `0xBADF3000` LTC/FBPA0, etc.); **283** registers still readable in parts of `0x136200`–`0x137F44`. Oracle strategy: one Titan V on nouveau, one VFIO — differential register replay.

### D3hot→D0 VRAM (March 16)

`echo on > .../power/control` → full **12GB** HBM2 R/W, **15/18** domains, **24/26** hardware tests. **Fragility**: VFIO close + PM reset on GV100 (**no FLR**) can destroy training — **GlowPlug daemon** holds fd; future **coral-kmod** without reset on close; Phase 3 full Rust HBM2 training.

**Handoff pattern**: glowplug/kmod owns GPU from boot → toadStool via fd or `/dev/coral0` → springs. References: experiments `062`–`064`.

### Primal guidance (short)

- **toadStool**: absorb glow plug → `GpuPowerController`, `PowerManager`, ProbeReport profiles.
- **coralReef**: fix runlist, fault buffers, PBDMA; extract `glow_plug`; persist ProbeReports.
- **barraCuda**: pre-warm hints, power-aware multi-GPU scheduling.

---

## Numerical Stability

**Source lineage**: `GPU_F64_NUMERICAL_STABILITY.md` (Paper 44 / hotSpring v0.6.24) merged with `NUMERICAL_STABILITY_EVOLUTION_PLAN.md` (v0.6.19).

### Executive summary

**f64 on GPU can diverge from CPU f64** in algorithms with **catastrophic cancellation** — not wrong precision routing (polyfills verified) but **ULP differences** (FMA fusion, reordering on SPIR-V vs SSE2) **amplified** by `(large) - (large) = (small)`.

**Fix**: algorithmic — compute small quantities **directly** (asymptotics, stable forms), not as differences of large numbers.

### Case: Mermin / W(z) = 1 + z·Z(z)

For |z|>4, z·Z(z)≈-1.017 ⇒ **W = 1 + z·Z** is near-cancellation (**~60×**).

**GPU (RTX 3090, NVK/NAK, SPIR-V)**: FMA fusion, reordering, **~40–80 ULP** drift over ~40 iterations → **~5000 ULP** through cancellation → **125%** relative error at some points; absolute error still small vs peak.

**Stable asymptotic** (|z|≥4):

```
W(z) ≈ -1/(2z²) × (1 + 3/(2z²) + 15/(4z⁴) + ...) + i·z·√π·exp(-z²)
```

Ratio **< 0.2** for |z|>4.

**After fix**: **100%** DSF positivity (vs **98%** CPU), **100%** passive-medium compliance, f-sum **3–5%** of CPU, high-|ω| |loss| **< 3e-7**.

### Root cause checklist

| Hypothesis | Verdict |
|------------|---------|
| Precision routing | No — polyfills OK |
| f32/f64 width | No — ~99% ω points **1e-13** |
| DF64 required | No — native f64 enough if stable |
| Actual cause | FMA/reorder + cancellation in **1 + z·Z** |

### Ownership

- **barraCuda (P1)**: stable special functions in `special_f64.wgsl` (or equivalent).

| Function | Cancellation region | Stable algorithm |
|----------|---------------------|------------------|
| W(z) = 1 + z·Z(z) | \|z\| > 4 | Direct asymptotic of W |
| erfc(x) = 1 − erf(x) | x > 4 | Direct continued fraction |
| log(1+x) | \|x\| ≪ 1 | log1p pattern |
| exp(x)−1 | \|x\| ≪ 1 | expm1 pattern |
| Bessel J₀(x) − 1 | \|x\| ≪ 1 | Direct Taylor |
- **coralReef (P2)**: FMA control (`NoContraction` SPIR-V), precision manifest incl. FMA behavior.
- **Springs**: point diagnostics, identify cancellation, validate **physics** (DSF positivity, sum rules) not only CPU bitwise match.

### Stability-then-speed

```
Python → Rust CPU → GPU (stable algorithms before sovereign speed)
```

### Multi-precision (stable W(z)) — f32 at z=5.57

| Algorithm | Re[W(5.57)] |
|-----------|-------------|
| Naive 1+z·Z | **-8.03e7** (overflow path) |
| Stable asymptotic | **-1.689e-2** |
| f64 ref | -1.689e-2 |

**f32 vs f64 (stable only)**

| \|z\| | f32 Re[W] | f64 Re[W] | Rel err |
|-------|-----------|-----------|---------|
| 5.0 | -2.122413e-2 | -2.122414e-2 | **2.78e-7** |
| 5.57 | -1.689429e-2 | -1.689430e-2 | **3.21e-7** |
| 8.0 | -7.987774e-3 | -7.987773e-3 | **1.06e-7** |
| 10.0 | -5.070820e-3 | -5.070819e-3 | **1.42e-7** |

### Throughput / DF64

| GPU | f32 TFLOPS | f64 TFLOPS | Ratio | DF64 (est.) |
|-----|------------|------------|-------|---------------|
| RTX 3090 | 35.6 | 0.56 | 64:1 | ~8.9 |
| RTX 4090 | 82.6 | 1.29 | 64:1 | ~20.6 |
| A100 | 19.5 | 9.7 | 2:1 | ~4.9 |

Stable W(z) enables DF64 on consumer f32 cores at **~14** useful digits for many plasma workloads.

### Case: BCS v² (March 6, 2026)

**Naive**: v² = 0.5*(1 - ε/E_qp) — bad when |ε|≫Δ.

**Stable**: v² = Δ²/(2·E_qp·(E_qp+|ε|)).

| Tier | Naive (eps=100, Δ=1) | Stable |
|------|----------------------|--------|
| f32 | 0 (garbage) | 2.5e-5 |
| f64 | ~11 digits | ~15 digits |

**Impact**: **2,042**-nucleus GPU sweeps; fixed in `hfb_common.rs` + 3 WGSL shaders; **5** new tests (parity, symmetry, range, f32 naive vs stable).

### Cancellation inventory

Experiment **046**: **9** families over **70+** shaders — **2** Tier-A fixed, **1** guarded, **6** documented acceptable/mitigated. See `hotSpring/experiments/046_PRECISION_STABILITY_ANALYSIS.md`.

### Cross-spring impact

| Spring | Affected computations | Action |
|--------|----------------------|--------|
| hotSpring | Plasma dispersion, BCS v², Jacobi eigensolve | **RESOLVED** (W(z) asymptotic, stable BCS v², degenerate guard) |
| wetSpring | Shannon entropy H = −Σp·log(p) near p≈0 | log_f64 polyfill already handles |
| neuralSpring | Softmax: exp(x)/Σexp(x) near equal logits | log-sum-exp trick |
| groundSpring | Chi-squared CDF near tail | erfc-based computation needed |
| airSpring | Van Genuchten: (1+\|αh\|^n)^(−m) near h≈0 | Verify no cancellation |

---

### Evolution plan: four tiers

**Vision**: Stable math → fast math (cheapest precision) → safe (no silent corruption) → encrypted (CKKS noise) → sovereign.

| Tier | Topic | Status |
|------|--------|--------|
| **1** | Precision stability (f32/DF64/f64) | **Complete** (March 6, 2026): 10 tests, 3 shaders, 046 audit |
| **2** | Precision mixing | **Next**: round-trip at f64↔DF64↔f32, GPU↔CPU, Dekker identity |

**Tier 2 mixing scenarios** (test matrix):

| Source | Destination | Risk | Test |
|--------|-------------|------|------|
| f64 → DF64 → f64 | Round-trip precision loss | hi+lo ≠ original | Upload/readback identity |
| f32 → f64 promotion | Phantom precision | assert f32 noise floor | Known-value round-trip |
| f64 → f32 truncation | Catastrophic if near cancellation | Stable algorithms immune | W(z) at f32 after f64 compute |
| DF64 → f64 → DF64 | Double-float reassembly error | Two-sum correctness | Dekker/Knuth identity tests |
| GPU → CPU → GPU | FMA behavior change per hop | Accumulation mismatch | Multi-hop identity test |
| **3** | FHE noise stability | Future: BearDog + barraCuda — stable ops → lower CKKS depth (see table below) |
| **4** | Genetic entropy → FHE params | Future BearDog |

**Tier 1 deliverables (barraCuda)**: `plasma_w_f64`, `bcs_v2_stable`, `erfc_f64`, `log1p_f64`, `expm1_f64` in `special_f64.wgsl` class.

**Tier 3 FHE infra snapshot**: NTT, pointwise mul, key switch, modulus switch, Galois rotate (barraCuda); BFV/CKKS PoC (toadStool showcase); encrypted special functions roadmap.

**CKKS noise comparison for W(z) at z = 5.57** (multiplicative depth L):

| Algorithm | Multiplications | Max intermediate | Noise amplification | Required depth |
|-----------|-----------------|-------------------|----------------------|----------------|
| **Naive** | ~80 | ~10⁶ | 10⁹× (cancellation) | L ≈ 80+ |
| **Stable** | ~10 | ~1 | 1× (no cancellation) | L ≈ 10 |

**Phases**

1. Done: stable algorithms, 046, Tier 1 proof.  
2. Next: mixing tests + coralReef FMA control for CPU parity where needed.  
3. Future: CKKS circuits from same stable algorithms.  
4. Horizon: sovereign GPU FHE, BearDog entropy for keys, metalForge dispatch.

**Evidence paths**: `dielectric_mermin_f64.wgsl`, `validate_gpu_dielectric.rs`, `046`/`044` docs, `fhe_*.rs`, showcase homomorphic-computing.

---

## Fixed-Function Science

**Source lineage**: `GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md` (March 17, 2026, ludoSpring V24).

### Thesis

DF64 showed **fp32 ALUs** can emulate fp64 at **8–16×** native f64 throughput on consumer GPUs — a “hidden computer.” A modern die has **≥8 fixed-function units** beyond shader cores; each implements a general math/map; **map domain problems to the unit’s I/O contract**.

### Hidden computers (summary)

1. **Shader CUs/SMs** — known; DF64 pattern is the template.
2. **Rasterizer** — triangle coverage + barycentric interpolation → voxelization, FEM cell assign, PIC/SPH binning, conservative rasterization.
3. **Depth (Z-buffer)** — per-pixel **min** → Voronoi (cone depth = distance), distance fields, nearest-object queries.
4. **ROPs / alpha blend** — additive blend = **hardware scatter-add** → histograms, PIC deposition, splatting, Beer-Lambert (multiplicative), KDE.
5. **RT cores** — BVH ray traversal → MD neighbors, Monte Carlo transport, acoustics, LOS, solar/building. **RTX 2000+**, RDNA2+; not MI50/Titan V; emulatable in compute.
6. **TMUs** — filtered fetch → EOS tables, resampling, stencil gather, neural activations (~fp16 tables “cheap”).
7. **Tessellation** — adaptive subdivision → AMR/FEM-style refinement, LOD.
8. **NVENC/VCN** — block transforms + motion → simulation “video” compression, registration via motion vectors.

### DF64 discovery pattern

Bottleneck → hardware contract → math mapping (Dekker) → validate vs f64 → measure speedup (**8–16×** on RTX 3090 class).

### Cross-benefit matrix

Rows: discoverer → primitive. Columns: springs. **Read across a row**: one discovery, multiple beneficiaries. **Read down a column**: each spring gains from others.

| Discoverer → Primitive | hotSpring | wetSpring | airSpring | groundSpring | healthSpring | neuralSpring | ludoSpring |
|------------------------|-----------|-----------|-----------|-------------|-------------|-------------|-----------|
| **Rasterizer binning** (any spring) | PIC cell assign | SPH binning | Grid mapping | FEM cell assign | Tissue voxelization | Spatial attention | Entity-to-tile |
| **Z-buffer Voronoi** (any spring) | Distance fields | Free-surface tracking | Terrain analysis | Geological tessellation | Organ segmentation | Feature clustering | Pathfinding heuristic |
| **Additive blending** (any spring) | Charge deposition | Particle deposition | Optical depth | Mass accumulation | Back-projection | Gradient accumulation | Influence maps |
| **RT core neighbor search** (any spring) | MD neighbor list | SPH neighbor list | Radiation ray tracing | Seismic ray tracing | Dosimetry transport | kNN classification | Acoustic ray tracing |
| **TMU table lookup** (any spring) | EOS tables | Ocean resampling | Absorption coefficients | Material properties | PK/PD curves | Activation functions | Engagement curves |
| **Tessellation AMR** (any spring) | Thermal refinement | Flow refinement | Terrain LOD | Seismic refinement | Mesh refinement | — | Procedural terrain LOD |
| **Tensor core MMA** (any spring) | CG solver | Linear system solve | Matrix inversion | FEM stiffness solve | Image reconstruction | Training/inference | — |
| **Video encoder compression** (any spring) | MD trajectory compress | Ocean time-series | Climate data compress | Seismic waveform compress | Medical image compress | — | Replay compression |

### Per-spring experiment assignments

**hotSpring** — RT cores, rasterizer, TMUs, alpha blending for MD/plasma.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| RT core MD neighbor list | RT cores | BVH over particles → neighbor query | 10×+ over Verlet rebuild |
| Rasterizer PIC binning | Rasterizer | Triangle per particle → cell assignment | 10–50× over compute loop |
| TMU equation-of-state | TMU | Precomputed EOS table → hardware interpolation | 10–20× over exp() per pair |
| Blend charge deposition | ROPs | Additive blend → scatter-add onto grid | 5–10× over atomic add |
| Z-buffer distance field | Depth buffer | Cone rendering → Euclidean distance field | 100× over wavefront BFS |

**wetSpring** — Rasterizer, alpha blending, TMUs, depth buffer, video encoder.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| Rasterizer voxelization | Rasterizer | Obstacle mesh → occupancy grid | 10–50× over compute voxelizer |
| Blend SPH deposition | ROPs | Kernel splat → density/velocity field | 5–10× over atomic scatter |
| TMU ocean regridding | TMU | Bilinear interpolation on ocean grid | 10–20× over compute interpolation |
| Z-buffer free surface | Depth buffer | Level-set interface capture | 100× over marching cubes |
| Video encoder trajectories | NVENC/VCN | Time-series of fields as video frames | 6:1 compression, hardware speed |

**airSpring** — TMUs, RT cores, alpha blending, rasterizer.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| TMU absorption tables | TMU | Gas absorption cross-sections → lookup | 10–20× over compute evaluation |
| RT solar radiation | RT cores | Sunlight through building geometry | 1000× over CPU ray tracing |
| Blend Beer-Lambert | ROPs | Multiplicative blend → optical depth | 5–10× over compute accumulation |
| Rasterizer terrain shadows | Rasterizer | Sun-direction triangle fill → shadow map | 10–50× over compute ray march |

**groundSpring** — Rasterizer, depth buffer, tessellation, TMUs.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| Rasterizer FEM mapping | Rasterizer | Mesh elements → grid points | 10–50× over compute loop |
| Z-buffer Voronoi | Depth buffer | Cone per seed → geological cell decomposition | 100× over Fortune's algorithm |
| Tessellation AMR | Tessellation HW | Error estimate → refined seismic mesh | Hardware-speed mesh refinement |
| TMU material properties | TMU | Rock/fluid property tables → lookup | 10–20× over compute evaluation |

**healthSpring** — Alpha blending, RT cores, video encoder, TMUs.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| Blend CT reconstruction | ROPs | Back-projection splatting → image accumulation | 5–10× over compute scatter |
| RT dosimetry | RT cores | Radiation transport through anatomy | 100–1000× over CPU Monte Carlo |
| Video encoder registration | NVENC/VCN | Motion estimation → image alignment | Hardware-speed registration |
| TMU pharmacokinetics | TMU | PK/PD curve lookup → drug concentration | 10–20× over analytical eval |

**neuralSpring** — TMUs, alpha blending, tensor cores (DF64 variants), rasterizer.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| TMU activation functions | TMU | Precomputed sigmoid/GELU/swish → lookup | 10–20× over compute eval |
| Blend gradient accumulation | ROPs | Additive blend → distributed gradient reduce | 5–10× over atomic add |
| Tensor core DF64 | Tensor cores | Dekker arithmetic in MMA pipeline | Unknown — novel exploration |
| Rasterizer spatial attention | Rasterizer | Triangle-based attention mask generation | Unknown — novel exploration |

**ludoSpring** — See `whitePaper/baseCamp/exp076_gpu_graphics_hardware_for_game_science.md`.

| Sub-experiment | Hardware unit | Operation | Expected gain |
|----------------|--------------|-----------|---------------|
| Rasterizer fog of war | Rasterizer | Wall triangles → visibility mask | 10–50× over per-tile ray march |
| Z-buffer pathfinding | Depth buffer | Cone at destination → distance heuristic | 100× over wavefront BFS |
| Blend influence maps | ROPs | Entity quads → accumulated influence | 5–10× over CPU loop |
| RT acoustic ray tracing | RT cores | Sound propagation through map geometry | 1000× over analytical model |
| TMU engagement curves | TMU | Fitts/Hick/DDA precomputed → lookup | 5–20× over analytical eval |
| Compute-shader rendering | Shader cores | DDA raycaster → RGBA framebuffer | Closes the render gap |

### Exploration protocol

baseCamp experiment → Python baseline → WGSL compute → fixed-function version → validate → throughput → document `domain → unit → speedup` → handoff `*_HARDWARE_REPURPOSING_HANDOFF_*.md` → barraCuda op tag.

### Absorption path

Validate → document → second spring replicates → handoff → **barraCuda** dispatch op → **coralReef** pipeline state → **toadStool** submit graphics+compute.

### Portability ladder

```
Level 0: Python baseline           → portable across languages
Level 1: Rust CPU                  → portable across platforms
Level 2: WGSL compute shader       → portable across GPU vendors
Level 3: GPU infrastructure target → portable across hardware ON the card
Level 4: Silicon type              → portable across CPU / GPU / NPU / FPGA
```

Levels 0–2 proven. **Level 3**: same abstract math → **any unit on die**. **Level 4**: CPU/GPU/NPU/FPGA (toadStool orchestration).

### Performance surface — “wrong hardware” placements (illustrative)

| Placement | What you learn |
|-----------|----------------|
| Yukawa force on shader cores (DF64) | Baseline throughput at 14-digit precision |
| Yukawa force on tensor cores (FP16) | Precision loss bounds, throughput ceiling at 4× rate |
| Yukawa force on tensor cores (TF32) | Precision vs throughput tradeoff at 2× rate |
| Yukawa force via TMU (potential table) | Lookup throughput when function is precomputable |
| Force accumulation on ROPs (blend) | Scatter-add throughput without atomics |
| Neighbor finding on RT cores (BVH) | Spatial query ceiling for particle methods |

### Compute trio (WHAT/HOW/WHERE)

- **barraCuda**: math + tolerance semantics — **hardware-agnostic**.
- **coralReef**: compile to ISA / RT / blend / etc.
- **toadStool**: route using measured **(operation, unit, precision, throughput)**.

### Tensor cores (RTX 3090 illustrative)

| Precision | Tensor TFLOPS | Shader TFLOPS | Ratio |
|-----------|---------------|---------------|-------|
| FP16 | ~142 | 35.6 | 4.0× |
| TF32 | ~71 | 35.6 | 2.0× |

| Operation | Matrix reformulation | Tensor core viable? |
|-----------|---------------------|-------------------|
| CG solver (Ax=b) | Matrix-vector: A × x | Yes — 60–70% of HMC runtime |
| Pairwise distances | diag(AᵀA) + diag(BᵀB) − 2AᵀB | Yes — O(N²) part of MD |
| Convolution | Toeplitz × input | Yes |
| FFT butterfly | Batched 2×2 rotations | Yes |
| Finite differences | Banded matrix × state | Yes |
| Neural layers | W × X + B | Yes |
| Dot products | Aᵀ × B (1×N × N×1) | Yes |
| Basis transforms | Change-of-basis × coordinates | Yes |

hotSpring lattice QCD: CG is matrix-vector products — **~22×** TF32 (**71** TFLOPS) vs DF64 on shader cores (**~3.24** TFLOPS) for iterations where TF32 is acceptable; final refinement DF64.

### Tolerance vs hardware (RTX 3090 illustrative row)

| Tolerance | ~digits | Fastest HW class | ~Throughput |
|-----------|---------|------------------|-------------|
| 1e-2 | 3 | FP16 tensor | ~142 TFLOPS |
| 1e-7 | 7 | FP32 shader | ~35.6 |
| 1e-14 | 14 | DF64 on FP32 | ~3.24–8.9 |
| 1e-16 | 16 | Native FP64 | ~0.33 |

### vs other frameworks (summary)

CUDA/Vulkan/OpenCL/Kokkos: app often picks HW at code time; ecoPrimals trio targets **math + tolerance** and lets infrastructure place work (per source).

### Sovereign stack implications

Mixed command streams: tensor MMA, graphics PSO, draws, RT state, framebuffers — extension of sovereign path, not a full rewrite.

### Compound claim (source)

DF64 closed **93%** of Kokkos gap (**27× → 3.7×**). If seven other unit classes add **3–5×** each on their slice, effective science throughput could reach **50–100 TFLOPS equivalent** on one card (illustrative stacking).

### Per-spring assignments

Detailed sub-experiment tables (hotSpring RT/raster/TMU/blend/Z; wetSpring; airSpring; groundSpring; healthSpring; neuralSpring; ludoSpring exp076) with **expected gain** columns (**10×–1000×** ranges) — preserved in full in source doc; this consolidation retains the structure and representative entries above.

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| **1.0.0** | **2026-04-04** | **Consolidation** of `GPU_F64_NUMERICAL_STABILITY.md`, `GPU_FIXED_FUNCTION_SCIENCE_REPURPOSING.md`, `GPU_SOVEREIGN_BRING_UP_GUIDE.md`, `NUMERICAL_STABILITY_EVOLUTION_PLAN.md`, and `SOVEREIGN_COMPUTE_EVOLUTION.md` into this single active guidance document. Technical numbers, tables, hardware IDs, validation figures, and register references are preserved or explicitly pointed to source paths where scope required trimming. Prior file dates in-repo: March 2026. |

*Upstream licenses and maintainers per original files (AGPL-3.0 variants, hotSpring/ludoSpring attribution).*
