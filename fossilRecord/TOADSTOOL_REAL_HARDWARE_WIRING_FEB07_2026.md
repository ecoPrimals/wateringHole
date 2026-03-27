# ToadStool Real Hardware Wiring Handoff
## February 7, 2026

**From**: ecoPrimals White Paper Review (upstream)  
**To**: ToadStool Maintainers  
**Priority**: HIGH — Blocks white paper citable claims  
**Status**: Directive issued, action required

---

## Executive Summary

The ecoPrimals white paper audit of BarraCuda's showcase benchmarks found a consistent pattern:

- **BarraCuda's core ops are real and validated** — NTT, INTT, PolyAdd, FFT, complex arithmetic, MD force kernels all execute on actual GPU hardware via WGSL. Cross-vendor correctness (NVIDIA + AMD) is confirmed.
- **Several showcase benchmarks fake NPU execution** — using `tokio::time::sleep()`, CPU busy-loops, or throughput multipliers instead of actual Akida chip execution. Some GPU benchmarks use `thread::sleep()` or `forward_cpu()` while claiming GPU.
- **FHE scheme-level work (BFV/CKKS, encrypted training) is now pinned to NUCLEUS** — BearDog owns the ciphertext layer. ToadStool should stop investing in FHE scheme implementation and redirect to completing real hardware wiring.

### Policy Change

```
BEFORE:  ToadStool implements FHE schemes + compute primitives
AFTER:   ToadStool implements compute primitives ONLY
         BearDog owns FHE ciphertext encoding/decoding
         Composition via NUCLEUS (biomeOS capability.call)
```

This is consistent with the primal model: BearDog owns cryptography, ToadStool owns compute. Neither should embed the other's responsibilities.

---

## What the Audit Found

### ✅ Real — Validated (No Action Needed)

| Component | Evidence |
|-----------|----------|
| FHE NTT/INTT/PolyAdd on GPU | 110× speedup at N=4096 on RTX 3090 |
| Cross-vendor GPU (NVIDIA + AMD) | 18/18 FHE ops produce identical results |
| Complex number ops (mul, exp) | Euler's identity verified |
| FFT 1D/2D/3D shaders | Evolved from NTT, validated |
| MD force kernels | Coulomb, Yukawa, LJ, Morse, Born-Mayer |
| PBC distance | Minimum image convention |
| LeNet5 GPU demo | Real OpenCL execution |
| wgpu/Vulkan executor | Real compute dispatch |
| MNIST NPU inference | Real `akida_driver::InferenceExecutor::infer()` |
| K-mer NPU | Real `akida_driver` calls |
| Cross-platform FHE (CPU+GPU) | TFHE-rs + BarraCuda |
| Transformer/Vision/Audio | Real BarraCuda ops (simplified architectures) |

### ❌ Faking — Needs Wiring (Action Required)

| File | Problem | Evidence |
|------|---------|----------|
| `pipeline_validation_actual_hardware.rs:406` | NPU = `tokio::time::sleep()` | `// TODO: Wire actual Akida inference` |
| `npu_reservoir_computing.rs:196` | NPU = CPU busy-loop | 384 billion samples/sec (impossible) |
| `hybrid_raytracing.rs` | NPU+GPU = CPU busy-loop | 1.4 quadrillion rays/sec (impossible) |
| `dense_vs_sparse.rs` (NPU entries) | `throughput * 3.0` multiplier | Not real Akida measurement |
| `homomorphic-computing/src/substrates/npu.rs:207` | `throughput * 3.0` multiplier | Not real Akida measurement |
| `encrypted_mnist_inference.rs` (NPU fn) | `simulate_fhe_matmul_time() * 0.6` | Modeled, not measured |
| `real_cuda_vs_barracuda.rs` | `thread::sleep()` | Your own audit flagged this Jan 12 |
| `vendor_agnostic_demo.rs` | `forward_cpu()` claiming GPU | Your own audit flagged this Jan 12 |
| `cross_platform_mlp.rs:92` | "GPU shader integration pending" | CPU fallback |
| `fhe_operation_validation.rs:194` | "TODO: Replace with actual BarraCuda" | Not wired |
| `measurement/power.rs:270` | "TODO: Use actual Akida detection" | Hardcoded values |
| `substrates/gpu.rs:526` | "TODO: Integrate with nvidia-smi" | `Some(150.0)` hardcoded |

### ⚠️ Simplified — Needs Architecture Completion

| Benchmark | Current | Target |
|-----------|---------|--------|
| Transformer inference | Single MatMul per "layer" | Full multi-head attention (Q/K/V + scaled dot-product) |
| Audio STFT | Tensor ops, no real FFT | Use `fft_1d.wgsl` (already implemented!) |
| Vision inference | Simplified Conv2D | Full MobileNet/ResNet layer composition |

---

## Required Actions (Prioritized)

### Week 1-2: Immediate (High Impact, Low Effort)

**1. Delete fake GPU demos** — 30 minutes

```
DELETE: showcase/gpu-universal/ml-inference/src/bin/real_cuda_vs_barracuda.rs
DELETE: showcase/gpu-universal/ml-inference/src/bin/vendor_agnostic_demo.rs
AUDIT:  showcase/gpu-universal/ml-inference/src/bin/cuda_vs_barracuda_benchmark.rs
UPDATE: Shell scripts → point to lenet5_demo.rs (the real one)
```

**2. Wire pipeline dispatch NPU** — 1-2 days

You already have the pattern in `mnist_npu.rs`:
```rust
// WORKING PATTERN (mnist_npu.rs):
let config = InferenceConfig::new(vec![INPUT_SIZE], vec![OUTPUT_SIZE], 1, 1);
let executor = InferenceExecutor::new(config);
let _result = executor.infer(&events, device)?;
```

Apply this to `pipeline_validation_actual_hardware.rs` lines 406-411, 427-428, 464-465. Replace every `tokio::time::sleep()` with real `akida_driver` inference.

**3. Wire Akida power measurement** — 1 day

Replace `Some(2.0)` with actual Akida SDK power query. This converts all NPU energy numbers from "datasheet" to "measured."

**4. Wire FHE operation validation** — 1 day

Replace TODO at `fhe_operation_validation.rs:194` with actual BarraCuda calls. The ops exist: `FhePolyAdd::new().execute()`, `FheNtt::new().execute()`, etc.

### Week 3-4: NPU Completion

**5. Wire reservoir computing NPU** — 3-5 days

Train a small SNN reservoir model in Python/Keras → `quantize_model()` → `convert_to_akida()` → save `.akd` → load via `akida_driver`. The conversion pipeline is documented in `showcase/neuromorphic/BENCHMARKS.md`. **You have 2× Akida AKD1000 chips on the tower. Use them.**

**6. Wire dense/sparse NPU** — 1-2 days

Replace `throughput * 3.0` multiplier with actual `akida_driver` sparse event processing.

**7. Wire cross-platform MLP GPU** — 1 day

`cross_platform_mlp.rs` currently says "GPU shader integration pending." Use `WgpuDevice::new()` + BarraCuda MatMul (same pattern as `transformer_inference.rs`).

**8. Wire GPU power measurement** — 2 hours

```bash
nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits
```

Or use NVML bindings. Replace `Some(150.0)` in `substrates/gpu.rs`.

### Week 5-6: ML Architecture Completion

**9. Audio STFT → real FFT shader** — 1-2 days

`fft_1d.wgsl` is already implemented! Wire it into `audio_processing.rs`. This should be trivial — the hard work (NTT→FFT evolution) is done.

**10. Transformer → full multi-head attention** — 3-5 days

All ops exist (MatMul, Softmax, LayerNorm, GELU, Add). Compose Q/K/V projections → scaled dot-product attention → concatenation → feed-forward.

**11. Vision → full Conv pipeline** — 2-3 days

All ops exist (Conv2D, MaxPool2D, BatchNorm, ReLU). Compose into real MobileNet/ResNet architecture.

### Week 7+: Complex NPU (Defer if Needed)

**12. Hybrid raytracing NPU** — 5-7 days

Deploy sparse BVH-traversal SNN to Akida for traversal phase. GPU shading uses real BarraCuda matmul/texture ops. This is the most complex NPU wiring task. Fine to defer until after 1-11 are done.

---

## Explicitly Deprioritized (Pin to NUCLEUS)

**Do not invest time in these until NUCLEUS enables BearDog↔ToadStool composition:**

| Item | Why | Owner After NUCLEUS |
|------|-----|---------------------|
| `schemes/bfv.rs` — BFV encrypt/decrypt/multiply | Ciphertext = BearDog's domain | BearDog |
| `schemes/ckks.rs` — CKKS encrypt/decrypt/multiply | Ciphertext = BearDog's domain | BearDog |
| Encrypted training pipeline | Requires BearDog ciphertext encoding | BearDog + ToadStool |
| Encrypted inference pipeline | Requires BearDog ciphertext encoding | BearDog + ToadStool |
| Inter-primal demos (all `sleep()`-based) | Requires biomeOS `capability.call` | biomeOS |

These are architecturally correct placeholders. Leave them as-is. The TODO comments in the code are accurate — they describe work that genuinely belongs to a future NUCLEUS integration, not to ToadStool alone.

---

## Success Criteria

When this handoff is complete:

- [ ] Zero `sleep()` calls in any benchmark that reports hardware timing
- [ ] Zero throughput multipliers (`* 3.0`, `* 0.6`, `* 5.0`)
- [ ] Zero CPU busy-loops claiming NPU performance
- [ ] All NPU benchmarks use `akida_driver::InferenceExecutor::infer()` on real Akida chips
- [ ] All GPU benchmarks use real BarraCuda WGSL dispatch
- [ ] Power from hardware telemetry (nvidia-smi, Akida SDK), not datasheets
- [ ] Fake GPU demos deleted
- [ ] ML architectures complete (multi-head attention, real FFT STFT, full Conv)

### The Sentence We're Working Toward

> "BarraCuda dispatches workloads to CPU, NVIDIA GPU, AMD GPU, and BrainChip Akida NPU from a single Rust codebase. All performance and energy measurements are from actual hardware execution."

Every item in this handoff exists to make that sentence true without caveat.

---

## What Upstream Provides

The white paper team has:
- Corrected `01_FHE_VALIDATION.md` — honest about what FHE benchmarks do and don't prove
- Corrected `02_HARDWARE_COMPARISON.md` — three-tier evidence classification (Real / Simplified / Modeled)
- Created `03_TOADSTOOL_WIRING_DIRECTIVE.md` — detailed file-level fix instructions
- Created `NTT_FFT_EVOLUTION_EVIDENCE.md` — constrained evolution documentation
- Copied all benchmark data to `ecoPrimals/whitePaper/barraCuda/data/`

When you complete this wiring, we regenerate the JSON/CSV data, update the white paper sections, and every claim becomes citable.

---

## Estimated Timeline

| Week | Tasks | Deliverable |
|------|-------|-------------|
| 1-2 | Delete fakes, wire pipeline NPU, power, FHE ops | Pipeline dispatch ✅ Real |
| 3-4 | Reservoir NPU, dense/sparse NPU, cross-platform MLP, GPU power | All NPU benchmarks ✅ Real |
| 5-6 | Audio FFT, full transformer, full vision | All ML benchmarks ✅ Complete |
| 7+ | Hybrid raytracing NPU (optional defer) | Full coverage |

**Total: ~6-8 weeks to convert every ❌ to ✅.**

---

**Contact**: ecoPrimals white paper team  
**Detailed directive**: `whitePaper/barraCuda/sections/03_TOADSTOOL_WIRING_DIRECTIVE.md`  
**Data location**: `whitePaper/barraCuda/data/` (local copies of all benchmark JSON/CSV)  
**Status**: Ready for ToadStool team to begin execution

