# toadStool S139 -- Spring Absorption & Compute Triangle Evolution

**Date**: March 9, 2026
**From**: toadStool S139
**To**: All primals (barraCuda, coralReef, hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, healthSpring)

## Summary

S139 surveyed all six springs and absorbed key patterns to unblock the live compute triangle (toadStool / barraCuda / coralReef).

## Changes

### P0: Discovery Path Alignment (UNBLOCKS COMPUTE TRIANGLE)

**Problem**: coralReef scans `$XDG_RUNTIME_DIR/ecoPrimals/` for discovery entries; toadStool only wrote to `$XDG_RUNTIME_DIR/ecoPrimals/discovery/`.

**Fix**: `PrimalCapabilities::announce()` now dual-writes:
1. `$XDG_RUNTIME_DIR/ecoPrimals/discovery/{id}.json` (canonical)
2. `$XDG_RUNTIME_DIR/ecoPrimals/{id}.json` (coralReef-compatible)

`cleanup()` removes both files.

**Impact**: coralReef can now discover toadStool without any changes on the coralReef side.

### P0: `gpu.dispatch` Capability

`build_capabilities()` now emits `gpu.dispatch` and `science.gpu.dispatch` when GPUs are present. These are the capability strings coralReef and barraCuda search for.

New interned string constants:
- `capabilities::GPU_DISPATCH` = `"gpu.dispatch"`
- `capabilities::SCIENCE_GPU_DISPATCH` = `"science.gpu.dispatch"`
- `capabilities::SHADER_COMPILE` = `"shader.compile"`
- `capabilities::ORCHESTRATION` = `"orchestration"`

### P1: GPU Descriptor Enrichment

`GpuDevice` struct now includes three new optional fields:
- `render_node: Option<String>` -- e.g. `/dev/dri/renderD128`
- `driver: Option<String>` -- e.g. `amdgpu`, `nvidia`, `nouveau`, `i915`
- `arch: Option<String>` -- e.g. `rdna2`, `sm_86`

These are populated from Linux DRM sysfs (`/sys/class/drm/`, `/sys/module/`) and enable `GpuContext::from_descriptor(vendor, arch, driver)` in coralReef/barraCuda.

### P2: Streaming Dispatch (absorbed from hotSpring v0.6.24)

New module: `toadstool::universal::streaming_dispatch`

Provides backend-agnostic dispatch batching:
- `DispatchMode` -- Single, Streaming, MegaBatch
- `DispatchStats` -- dispatch/submission counts, amortization ratios
- `StreamingDispatchContext` -- tracks timing and batching decisions

This is the generalized version of hotSpring's `streaming_dispatch.rs`. Springs can use toadStool's version instead of maintaining local copies.

### P3: Pipeline DAG (absorbed from neuralSpring S134)

New module: `toadstool::universal::pipeline_graph`

DAG-based multi-stage compute coordination:
- `PipelineGraph` -- directed acyclic graph with topological sort (Kahn's algorithm)
- `StageNode` -- capability-addressed stages with substrate preferences
- `PipelineExecution` -- execution tracking with pass/fail and timing
- `compute_triangle_pipeline()` -- canonical discover -> compile -> dispatch pipeline

This is the generalized version of neuralSpring's `metalForge/forge/src/graph.rs`.

### P4: FFT Substrate (groundSpring)

`SubstrateCapabilityKind::Fft` already exists (added in S138). No action needed.

## Quality Gates

- `cargo fmt --all -- --check`: PASS (zero diffs)
- `cargo clippy --workspace -- -D warnings`: PASS (zero warnings)
- `cargo test -p toadstool --lib`: 1,405 tests PASS
- `cargo test -p toadstool-server --lib`: 545 tests PASS
- `cargo test -p toadstool-common --lib`: 947 tests PASS

## Spring Survey Results

| Spring | Version | toadStool Pin | Key Absorption |
|--------|---------|---------------|----------------|
| hotSpring | v0.6.24 | S138 | StreamingDispatch (absorbed) |
| groundSpring | V99 | S130+ | FFT substrate (already present) |
| neuralSpring | S134 | S130+ | PipelineGraph DAG (absorbed) |
| wetSpring | V101 | S130+ | Uses toadStool GPU dispatch |
| airSpring | v0.7.5 | S130+ | 14 JSON-RPC science methods validated |
| healthSpring | V13 | S130+ | PK/PD ops in barraCuda |

## Remaining Blockers for Live Compute Triangle

1. `coral-gpu` must be publishable as a normal crate dependency
2. Nouveau hardware validation (SM70 dispatch on Titan V)
3. NVIDIA proprietary DRM E2E validation

toadStool's side of the compute triangle is now unblocked. The dual-write discovery and GPU descriptor enrichment mean coralReef and barraCuda can discover and use toadStool's GPU information without any changes on their side.

## Doc Cleanup

- All 13 root docs updated from S138 to S139 headers
- `docs/README.md`, `docs/guides/TESTING.md`, `specs/README.md` updated to S139
- Pre-progressive showcase directories archived to `ecoPrimals/fossil/toadStool/showcase-hardware-S139/` (neuromorphic, gpu-universal, homomorphic-computing, akida-characterization, barracuda-validation, whitePaper)
- Showcase README updated to reference archived location
- Zero stale TODOs in production .rs files (1 TEMPORARY in GPU test code -- active segfault investigation, `#[ignore]`)

## File Changes

- `crates/server/src/capabilities/mod.rs` -- dual-write announce, GpuDevice enrichment, gpu.dispatch capabilities, DRM helper functions
- `crates/core/common/src/interned_strings.rs` -- GPU_DISPATCH, SCIENCE_GPU_DISPATCH, SHADER_COMPILE, ORCHESTRATION constants
- `crates/core/toadstool/src/universal/streaming_dispatch.rs` -- NEW (absorbed from hotSpring)
- `crates/core/toadstool/src/universal/pipeline_graph.rs` -- NEW (absorbed from neuralSpring)
- `crates/core/toadstool/src/universal/mod.rs` -- module registration and re-exports
- 13 root docs, 3 subdirectory docs -- session headers updated to S139
- 6 showcase directories archived to fossil
- Test files updated for new GpuDevice fields
