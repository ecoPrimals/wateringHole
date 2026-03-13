# coralReef Long-Term Vision: Rust Ingestion & Hardware Atheism

**Source**: hotSpring architectural discussion, March 13, 2026
**Scope**: Late-term guidance for coralReef, barraCuda, toadStool, and all springs
**Priority**: Vision document — iterative evolution, NOT one-shot redesign

---

## Executive Summary

coralReef's ultimate evolution is to become a **universal Rust backend** that
compiles Rust source to any substrate — GPU, CPU, NPU, future silicon. This
eliminates the language boundary between CPU code (Rust) and GPU code (WGSL),
making the stack fully hardware atheistic: one language, one compiler, any
target. The borrow checker and type system apply to GPU code, frontloading
an entire subclass of bugs (memory safety) that every other GPU programming
model suffers from.

**This is a long-term vision. The path is iterative, not revolutionary.**

---

## Current Success (Where We Are)

Before looking forward, anchor on what works NOW:

| Capability | Status | Evidence |
|-----------|--------|---------|
| WGSL → native SASS (NVIDIA) | Working | 46/46 shaders compile |
| WGSL → native GFX ISA (AMD) | Working | E2E verified on RX 6950 XT |
| VFIO sovereign dispatch | 6/7 tests pass | BAR0, DMA, upload/readback validated on Titan V |
| 806 WGSL shaders | Production | barraCuda #![forbid(unsafe_code)] |
| DF64 precision | Working | Hardware-atheistic double-float emulation |
| 27,000+ physics tests | Passing | 6 springs, reproducible science |

**We evolve FROM this base. Every step must maintain what works.**

---

## The Evolution Path

### Phase 1: Current (WGSL → native ISA) — NOW

```
WGSL source → coralReef → NAK → SASS (NVIDIA)
                        → ACO → GFX  (AMD)
```

**Focus**: Close the PFIFO channel init gap. Get 7/7 VFIO tests passing.
Complete the sovereign dispatch pipeline. Ship what we have.

**No language changes. No new input formats. Just finish the dispatch.**

### Phase 2: CPU Backend — NEAR TERM

```
WGSL source → coralReef → x86 AVX-512 / ARM NEON (CPU SIMD)
```

Add a CPU target to coralReef. The same WGSL shaders that run on GPU also
compile to CPU SIMD. This gives:

- CI testing without GPU hardware (deterministic, reproducible)
- Every machine becomes a compute node (no GPU required)
- CPU fallback for development and debugging
- Validation: same shader, same math, CPU and GPU produce identical results

**Implementation**: WGSL → NIR → cranelift (Rust-native) → x86/ARM.
cranelift already exists and generates CPU code. The bridge is NIR → CLIF.

### Phase 3: Rust Subset as Input — MEDIUM TERM

```
Rust source (#[compute]) → rustc frontend → CLIF → coralReef → any target
```

Accept cranelift IR (CLIF) as a coralReef input format. This means:

- Scientists write `#[compute]` Rust functions instead of WGSL
- rustc handles parsing, type checking, borrow checking, lifetime analysis
- coralReef handles lowering CLIF to native ISA (SASS, GFX, CPU SIMD)

**The borrow checker applies to GPU code.** This frontloads an entire subclass
of bugs to compile time:

| Bug Class | WGSL/CUDA/GLSL | Rust #[compute] |
|-----------|---------------|-----------------|
| Buffer out-of-bounds | Runtime panic / silent corruption | Compile-time bounds check |
| Data race on shared memory | Silent corruption, nondeterministic | Compile-time borrow check |
| Aliased mutable buffers | Undefined behavior | Compile-time exclusive borrow |
| Use-after-free | Silent corruption | Compile-time lifetime analysis |
| Type mismatch (buffer layout) | Runtime error or silent misinterpret | Compile-time type system |
| Uninitialized memory read | Garbage values | Compile-time initialization check |

Every other GPU programming model discovers these at runtime (if lucky) or
produces silently wrong results (if unlucky). Rust eliminates them at compile
time. For scientific computing where correctness matters more than anything,
this is transformative.

**Implementation**: Add CLIF → NAK lowering (NVIDIA), CLIF → ACO lowering
(AMD), CLIF → cranelift passthrough (CPU). The GPU-compatible Rust subset
is well-defined:

```
GPU-compatible:  f32, f64, u32, arrays, slices, structs, for loops,
                 traits (static dispatch), generics (monomorphized),
                 match (with divergence cost), const fn
NOT compatible:  Box, Vec, String, dyn Trait, async, closures capturing
                 heap, std::io, std::net, anything that allocates
```

The scientific math code — DF64, matrix ops, lattice QCD, Hill dose-response,
Anderson localization — lives entirely in the compatible subset.

### Phase 4: Automatic Target Selection — LONG TERM

```
Rust source → coralReef → optimal target auto-selected per function
```

No `#[compute]` annotation needed. The compiler analyzes the code and decides:

- Data-parallel loop over 10M elements with no dependencies → GPU
- Sequential data-dependent computation → CPU
- Inference workload matching NPU capabilities → NPU (via toadStool)
- Small workload below dispatch overhead threshold → CPU (no transfer cost)

**Implementation**: Cost model in coralReef that estimates dispatch overhead,
data transfer cost, and compute throughput for each target. toadStool provides
hardware capabilities. The compiler makes the optimal choice.

---

## How This Connects to Each Primal

### coralReef

The compiler grows in stages:
1. (Now) WGSL → SASS/GFX
2. (Phase 2) WGSL → CPU SIMD (add cranelift as output backend)
3. (Phase 3) CLIF → SASS/GFX (add CLIF as input format)
4. (Phase 4) Auto-routing (add cost model)

Each phase is additive. Nothing is removed. WGSL remains a supported input
format forever — it's simpler and sometimes more appropriate than full Rust.

### barraCuda

The math engine evolves:
1. (Now) 806 WGSL shaders, `#![forbid(unsafe_code)]`
2. (Phase 2) Same shaders also compile to CPU — validation + portability
3. (Phase 3) Shaders can be rewritten as Rust `#[compute]` functions — one
   language for the entire crate, borrow checker validates GPU memory access
4. (Phase 4) `GpuBackend` trait becomes `ComputeBackend` — CPU and GPU are
   interchangeable dispatch targets

Migration is gradual. Existing WGSL shaders keep working. New shaders can
be written in Rust. Both coexist. The Rust versions gain memory safety.

### toadStool

The hardware manager extends:
1. (Now) VFIO GPU bind, hw-learn, dispatch handler, thermal management
2. (Phase 2) Provides CPU capability info (core count, SIMD width, cache)
   to coralReef for CPU target optimization
3. (Phase 3) hw-learn recipes extend to CPU SIMD tuning (AVX width selection,
   cache-aware blocking)
4. (Phase 4) Cross-substrate scheduling — toadStool decides which functions
   go to GPU, CPU, or NPU based on current load and thermal state

### All Springs

The science code simplifies:
1. (Now) Rust application code + WGSL shader strings → barraCuda → GPU
2. (Phase 3) Rust application code with `#[compute]` functions — no embedded
   shader strings, no separate .wgsl files, just Rust
3. Physics validation tests become truly substrate-agnostic — same test runs
   on CPU and GPU, same results, same binary

---

## The Hardware Atheism Principle

### Agnostic vs. Atheistic

**Hardware agnostic**: "I don't know which hardware is best, so I support all."
Passive. Still thinks in hardware terms (warps, wavefronts, thread blocks).
Kokkos, OpenCL, SYCL.

**Hardware atheistic**: "Hardware does not exist in the math domain." The
mathematics is its own provable domain. A Wilson loop is a Wilson loop. The
shader IS the mathematics. Hardware is a compilation target, not a belief system.

### Two-Layer Architecture

```
Layer 1: Mathematics (hardware atheistic)
  - Algorithm-level optimizations (complexity, stability, precision)
  - Global: apply everywhere, improve the math itself
  - Owned by: scientists, mathematicians, springs

Layer 2: Hardware Optimization (last mile)
  - Substrate-level optimizations (register allocation, memory coalescing)
  - Local: per-hardware, per-architecture
  - Owned by: coralReef backends, toadStool hw-learn, hardware vendors
```

Separating these layers means:
- Mathematicians optimize math without knowing what a warp is
- Hardware engineers optimize dispatch without knowing what a Wilson loop is
- Both layers improve independently and compose cleanly
- Hardware vendors (NVIDIA, AMD, Intel) compete on Layer 2 merit
- The math layer creates demand for hardware optimization, not replaces it

### The NVIDIA Opportunity

This architecture INCREASES NVIDIA's competitive moat:
- Expands the GPU compute market from ~2-5M developers to ~50-500M
- Every new user is a potential NVIDIA hardware customer
- NVIDIA's Layer 2 optimization is superior — they win on merit
- The lock-in shifts from "can't run without CUDA" to "runs best on NVIDIA"
- The Linux/IBM precedent: lower market share, much larger market, higher revenue

See: `whitePaper/outreach/AN_INVITATION_TO_NVIDIA_V2.md`

---

## Iteration Discipline

**Critical principle: evolve iteratively, not revolutionarily.**

The constrained evolution methodology that built ecoPrimals applies to this
vision as well. Each phase must:

1. **Maintain everything that works** — never break existing WGSL compilation
2. **Add capability** — new input or output format, not replacement
3. **Validate against physics** — same 27,000+ tests must pass on new targets
4. **Ship incrementally** — each phase is usable independently

The one-shot approach (rewrite everything for Rust input) would violate the
methodology. The iterative approach (add CLIF input alongside WGSL, validate,
then gradually migrate shaders) follows it.

```
Current success → close VFIO dispatch gap → CPU backend → CLIF input
→ Rust #[compute] → auto-routing → self-optimizing compilation
```

Each arrow is a validated step. Each step maintains all prior capability.
Solution-satisfying, then improving. The methodology that built the stack
is the methodology that evolves it.

---

## Memory Safety on Shaders: The Frontloaded Bug Class

The most immediate practical value of Phase 3 is **compile-time memory
safety for GPU code**. Today, every GPU programming model (CUDA, OpenCL,
WGSL, GLSL, HLSL, Metal) has the same flaw: memory errors are runtime
errors (at best) or silent data corruption (at worst).

In scientific computing, silent data corruption means wrong physics.
Wrong physics means wrong conclusions. Wrong conclusions waste years of
research and millions in funding.

Rust on GPU eliminates this category entirely:

```rust
#[compute(workgroup_size = 64)]
fn lattice_update(
    gauge: &[SU3Matrix],      // immutable — compiler proves no data race
    result: &mut [SU3Matrix],  // exclusive — compiler proves no aliasing
    beta: f64,                 // Copy — no ownership issue
) {
    let idx = thread_id();
    // bounds check at compile time (with known workgroup size)
    // borrow check proves gauge and result don't alias
    // type system proves SU3Matrix layout matches buffer
    result[idx] = staple_sum(&gauge, idx) * beta;
}
```

This isn't a theoretical benefit. This is the difference between
"the lattice QCD ran but produced wrong results due to a buffer alias
in the stencil kernel" and "the code doesn't compile until the alias
is fixed."

For CERN-grade reproducible physics, this matters more than performance.

---

*Vision documented March 13, 2026. Iterative execution starts with Phase 1
completion (VFIO channel init). Each subsequent phase builds on validated
success.*

*The shaders are the mathematics. The mathematics is provable. The substrate
is irrelevant. The compiler is the bridge.*
