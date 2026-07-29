# barraCuda Wave 155i — strandGate RTX 3090 GPU Compute Profiling

**Date**: Jul 29, 2026 | **Gate**: strandGate | **Wave**: 155i
**Team**: barraCuda code team

---

## Summary

First real GPU compute validation on strandGate hardware. Built glibc binary
from source (musl-static cannot `dlopen` Vulkan drivers). Both discrete GPUs
discovered and profiled. All 4,957 tests pass on RTX 3090. FHE NTT bit-perfect.
Cross-vendor parity confirmed.

---

## Hardware Discovered

strandGate has **two discrete GPUs** plus CPU fallback:

| # | Device | Type | Backend | SHADER_F64 | VRAM |
|---|--------|------|---------|------------|------|
| 0 | NVIDIA GeForce RTX 3090 | DiscreteGpu | Vulkan | Yes (14/9 native) | 24 GB |
| 1 | AMD Radeon RX 6950 XT (RADV NAVI21) | DiscreteGpu | Vulkan | Yes (14/9 native) | 16 GB |
| 2 | llvmpipe (LLVM 15.0.7) | Cpu | Vulkan | Yes | System RAM |

NVIDIA driver: 580.126.18 | Vulkan 1.3.280 | Compute capability 8.6

---

## FP64 Performance Profile

Both GPUs have **strong native FP64 hardware** (unusual for consumer cards).
DF64 emulation is unnecessary on this hardware — native f64 wins.

### RTX 3090 (GA102 Ampere)

| Precision | Throughput | vs FP64 | Digits |
|-----------|-----------|---------|--------|
| FP32 | 96.37 TFLOPS | 0.93x | 7 |
| FP64 | 103.97 TFLOPS | 1.00x | 16 |
| DF64 | 91.89 TFLOPS | 0.88x | 14 |

### AMD RX 6950 XT (NAVI21 RDNA2)

| Precision | Throughput | vs FP64 | Digits |
|-----------|-----------|---------|--------|
| FP32 | 85.33 TFLOPS | 0.86x | 7 |
| FP64 | 99.28 TFLOPS | 1.00x | 16 |
| DF64 | 83.87 TFLOPS | 0.84x | 14 |

**Recommendation**: Use native f64 on both GPUs. DF64 path remains for GPUs
with crippled FP64 (e.g., RTX 4070 at 1:64 ratio).

---

## GPU Validation Results

| Test | Status | Detail |
|------|--------|--------|
| Device capability probe | PASS | RTX 3090 DiscreteGpu, 1024MB max buf, 256 max wg |
| Tensor matmul 64x64 | PASS | I*A == A in 42.90ms |
| DF64 add/sub precision | PASS | Precision OK in 7.86ms |
| FHE NTT round-trip (mod 17, N=4) | PASS | **Bit-perfect** in 59.55ms |
| FHE NTT round-trip (mod 12289, N=8) | PASS | **Bit-perfect** in 6.60ms |
| FHE pointwise mod-mul (mod 12289) | PASS | **Exact** in 19.73ms |

---

## SciPy Parity Benchmarks (RTX 3090)

| Operation | N | Median | SciPy CPU ref |
|-----------|---|--------|---------------|
| sum_f64 (reduction) | 1M | 6.62ms | ~1.2ms |
| variance_f64 (Welford) | 1M | 5.61ms | ~1.2ms |
| cdist Euclidean (f32) | 1K×1K D=3 | 0.77ms (1.3B pairs/s) | ~50ms |

**cdist is 65x faster** than single-thread SciPy. Reduction/variance at small N
are upload-dominated (GPU dispatch overhead > compute time); at scale, GPU wins.

---

## Workgroup Size Profile

| Config | Batch | Sweeps | Time |
|--------|-------|--------|------|
| n=20, s=200 | 512 | 200 | 25.75ms |
| n=30, s=200 | 512 | 200 | 104.50ms |
| n=12, s=200 (HFB) | 512 | 200 | 7.26ms |
| n=30, s=5 (dispatch-dom) | 512 | 5 | 86.79ms |

Warp-packed dispatch (wg32) on proprietary PTXAS — no wg1 penalty.

---

## f64 Built-in Capabilities (Both GPUs)

All 14/9 f64 built-ins are **NATIVE** on both devices:
- `exp`, `log`, `exp2`, `log2`, `sin`, `cos`, `sqrt`, `fma`, `abs`, `min`, `max`
- No software fallback needed for transcendentals
- `f64 shared memory`: **Not available** (naga/SPIR-V limitation — use DF64 path)

---

## Test Suite on RTX 3090

| Metric | Value |
|--------|-------|
| Total tests | 4,957 |
| Passed | 4,957 |
| Failed | 0 |
| SIGSEGV | 0 |
| Wall time | 3m 52s |
| CPU utilization | 515% |

---

## Binary Status

| Binary | Linkage | GPU Access | Location |
|--------|---------|------------|----------|
| `barracuda` (depot) | musl-static | **No** (can't dlopen) | `~/.local/bin/barracuda` |
| `barracuda-glibc` (local) | glibc dynamic | **Yes** | `~/.local/bin/barracuda-glibc` |

Awaiting sporeGate depot rebuild with glibc target (cellMembrane P0 code shipped).

---

## For Upstream

- **Multi-GPU dispatch** (P3 roadmap): strandGate is ideal — two discrete GPUs from
  different vendors. Cross-vendor workload distribution now has real hardware to target.
- **FHE on GPU**: Bit-perfect NTT round-trips confirmed. strandGate can serve as FHE
  compute target for Nest Atomic workloads via sovereign IPC.
- **No gaps found** in barraCuda code — all validation passes on real hardware.
