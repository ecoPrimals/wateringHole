# barraCuda v0.3.12 — Composition Elevation & Deep Debt Evolution Handoff

**Date**: April 12, 2026
**Sprint**: 42
**Version**: 0.3.12
**Tests**: 4,296 passed (14 skipped), 0 failures
**IPC Methods**: 32 registered (was 31)
**Quality Gates**: fmt ✓ clippy ✓ doc ✓ deny ✓

---

## What Changed

### Composition Elevation (HIGH — driven by primalSpring audit)

1. **tensor.* response schema standardized** — All tensor-producing methods now return
   consistent `{status, result_id, shape, elements}`. Scalar-producing methods
   (`tensor.reduce`) return `{status, value, op}`. Eliminates ambiguity for
   primalSpring's typed extractors (`call_extract_f64`, `call_extract_vec_f64`).

2. **`tensor.batch.submit` IPC method** — Fused multi-op pipeline over JSON-RPC
   wrapping `TensorSession`. Springs can now run "matmul then softmax then readback"
   as a single composition call. All ops share one GPU command submission.
   - Supported ops: create, add, mul, fma, scale, matmul, relu, gelu, softmax,
     layer_norm, reshape, readback
   - Wire contract documented in `specs/TENSOR_WIRE_CONTRACT.md`
   - 10 new tests covering error paths and dispatch routing

### Deep Debt Evolution

3. **`primal.device()` returns `Arc<WgpuDevice>`** (was deep-cloned `WgpuDevice`) —
   Zero-copy refcount bump instead of cloning GPU device handles (pipeline caches,
   adapter info, device state) on every IPC call. Fixed 6+ call sites.

4. **Smart refactors**:
   - `sovereign_device.rs` 758→676 lines: discovery extracted to `sovereign_discovery.rs`
   - `transfer.rs` 748→610 lines: PCIe sysfs probe extracted to `pcie_probe.rs`

5. **Showcase hardcoding evolved to capability-based**:
   - `/tmp/ecoPrimals` → env-driven (`XDG_RUNTIME_DIR`/`TMPDIR`/`ECOPRIMALS_DISCOVERY_DIR`)
   - `toadstool` string detection → `has_capability()` scanning JSON manifests for
     `compute.dispatch` / `hardware.profile` capabilities

6. **Comprehensive debt audit confirmed CLEAN**:
   - Zero TODO/FIXME/HACK markers
   - Zero `todo!`/`unimplemented!` macros
   - Zero `#[allow(` — all use `#[expect(` with reasons
   - Zero production mocks (all in `#[cfg(test)]`)
   - Zero `.unwrap()` in library code (all in test modules)
   - All deps pure Rust (blake3=pure, wgpu required)
   - Single `unsafe` site: barracuda-spirv SPIR-V passthrough (documented, wgpu#4854)

---

## For Other Primals

### primalSpring
- `tensor.*` schemas now standardized — `call_extract_f64` can reliably read `result.value`,
  `call_extract_vec_f64` can reliably read `result.data`
- `tensor.batch.submit` enables fused pipeline composition without per-op IPC round-trips
- `primal.device()` API change: returns `Arc<WgpuDevice>` not `WgpuDevice` — most callers
  auto-deref, but remove any `Arc::new(dev)` wrapping

### coralReef
- No impact on compilation IPC — `shader.compile.*` methods unchanged
- barraCuda's `tensor.batch.submit` uses existing `TensorSession` API internally

### toadStool
- `proxy_to_barracuda` alias removal (your S202) confirmed — no references remain
- Showcase discovery now uses capability-based manifest scanning, not primal name strings

### neuralSpring
- `tensor.batch.submit` available for batched tensor workflows
- Version pin should move from v0.3.11 to v0.3.12

---

## Files Changed

### New files
- `crates/barracuda-core/src/ipc/methods/batch.rs` — `tensor.batch.submit` handler
- `crates/barracuda-core/src/ipc/methods_tests/batch_tests.rs` — 10 tests
- `crates/barracuda/src/device/sovereign_discovery.rs` — capability-based dispatch discovery
- `crates/barracuda/src/unified_hardware/pcie_probe.rs` — Linux sysfs PCIe probing
- `specs/TENSOR_WIRE_CONTRACT.md` — formal wire contract documentation

### Modified files
- `crates/barracuda-core/src/lib.rs` — `device()` returns `Arc<WgpuDevice>`
- `crates/barracuda-core/src/ipc/methods/tensor.rs` — schema standardization
- `crates/barracuda-core/src/ipc/methods/mod.rs` — batch module + 32nd method
- `crates/barracuda-core/src/ipc/mod.rs` — wire contract docs
- `crates/barracuda-core/src/rpc.rs` — Arc evolution (6 sites)
- `crates/barracuda-core/src/ipc/methods/{fhe,compute,health}.rs` — Arc evolution
- `crates/barracuda/src/device/sovereign_device.rs` — discovery extracted
- `crates/barracuda/src/device/mod.rs` — sovereign_discovery module
- `crates/barracuda/src/unified_hardware/transfer.rs` — probe extracted
- `crates/barracuda/src/unified_hardware/mod.rs` — pcie_probe module
- `crates/barracuda/src/tensor/mod.rs` — Display idiom
- `showcase/02-cross-primal-compute/03-sovereign-pipeline/src/main.rs` — capability-based

---

## Remaining Debt (LOW, not blocking composition)

- Sovereign pipeline readback validation (hardware-dependent)
- DF64 NVK verification (hardware-dependent)
- Coverage 80→90% target (requires real GPU hardware; 81.21% on llvmpipe)
- BufReader lifetime edge-case in handshake relay
- `invocation.rs` (753 lines) — cohesive interpreter, optional memory/stmt split
- `wgpu_device/mod.rs` (728 lines) — facade with 6 extracted submodules, optional poll/submit split
