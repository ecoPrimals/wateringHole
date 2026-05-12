# barraCuda v0.3.12 — BC-07 Full Wiring, BC-06 Docs, TensorSession Migration Guide

**Date**: April 11, 2026
**Sprint**: 41
**Version**: 0.3.12
**Contact**: barraCuda team
**Previous**: `BARRACUDA_V0311_DEEP_DEBT_PRIMALSPRING_GAP_RESOLUTION_HANDOFF_APR11_2026.md`

---

## Summary

Sprint 41 resolves all remaining primalSpring-assigned gaps (BC-07 fully wired,
BC-06 documented) and publishes the TensorSession migration guide for spring
adoption. An 11-axis deep debt audit confirms clean bill across all axes.

---

## primalSpring Gap Resolution

| Gap | Severity | Status | Resolution |
|-----|----------|--------|------------|
| BC-07 | Medium | **Resolved** | `Auto::new()` returns `DiscoveredDevice` enum: wgpu GPU → wgpu CPU → SovereignDevice IPC → Err. `BarraCudaPrimal` stores `DiscoveredDevice`. IPC handlers report `sovereign_ipc` status. |
| BC-06 | Medium | **Resolved** | musl-static GPU constraint documented in README.md and CONTEXT.md with deployment matrix. |
| BC-08 | Medium | Resolved (Sprint 40) | `cpu-shader` default-on. |
| TensorSession | Open→Resolved | **Resolved** | Migration guide published in BREAKING_CHANGES.md 0.3.12 section. Stable API surface documented (20 methods + 5 SessionTensor methods). |

---

## Key Changes

### BC-07: `Auto::new()` → `DiscoveredDevice` enum

```
Before: Auto::new() -> Result<Arc<WgpuDevice>>
After:  Auto::new() -> Result<DiscoveredDevice>
        DiscoveredDevice::Wgpu(Arc<WgpuDevice>)
        DiscoveredDevice::Sovereign(Arc<SovereignDevice>)
```

- `Auto::new_wgpu()` convenience for code needing local tensor buffers
- `DiscoveredDevice::require_wgpu()` for consuming extraction
- `wgpu_device()`, `name()`, `has_f64_shaders()`, `is_sovereign()` delegation methods
- `BarraCudaPrimal.compute_device()` returns `Option<&DiscoveredDevice>`
- `device()` preserved for backward compat (extracts wgpu from DiscoveredDevice)

### BC-06: musl-static GPU constraint

| Deployment | GPU | CPU Shader | Sovereign IPC |
|------------|-----|------------|---------------|
| glibc host | wgpu Vulkan/Metal/DX12 | Yes (default) | Optional |
| musl-static (ecoBin) | **Unavailable** (`dlopen` blocked) | Yes (default) | **Yes** — GPU via IPC |
| WASM | wgpu WebGPU | Not yet | No |

### TensorSession Migration Guide

- `session::TensorSession`: Stable fused multi-op GPU pipeline API (20 public methods)
- `device::tensor_context::BatchGuard`: Low-level RAII batch guard (renamed from TensorSession)
- Full code examples and method table in BREAKING_CHANGES.md

### 11-Axis Deep Debt Audit

| Axis | Status |
|------|--------|
| println/eprintln in lib src | Zero (only bin/ CLI + doc examples) |
| `#[allow(` attributes | Zero (all `#[expect(` with reason) |
| `Result<T, String>` / `Box<dyn Error>` | Zero in production |
| `todo!()` / `unimplemented!()` | Zero anywhere |
| Production `unwrap()` / `expect()` | unwrap: 0. expect: 6 (Deref ownership invariants, correct) |
| Files >800 lines | Zero (largest 758) |
| Hardcoded primal names in runtime | Zero (evolved to capability-based) |
| Mocks in production | Zero |
| unsafe code | `#![forbid(unsafe_code)]` in barracuda + barracuda-core |
| External deps | All pure Rust (wgpu GPU-by-design, blake3 'pure') |
| Smart refactoring | No files need refactoring |

---

## Files Changed

21 files across barracuda, barracuda-core, root docs:

- `crates/barracuda/src/device/mod.rs` — `DiscoveredDevice` enum, `Auto::new()` returns it
- `crates/barracuda/src/lib.rs` — re-export `DiscoveredDevice`
- `crates/barracuda/src/tensor/mod.rs` — `from_vec`/`zeros`/`ones` use `Auto::new_wgpu()`
- `crates/barracuda/src/esn_v2/model.rs` — `Auto::new_wgpu()`
- `crates/barracuda/src/ops/{concat,gt,unsqueeze,where_op,onecycle}.rs` — `Auto::new_wgpu()`
- `crates/barracuda/src/session/mod.rs` — wetSpring added to stability doc
- `crates/barracuda-core/src/lib.rs` — `DiscoveredDevice` field, `compute_device()` accessor
- `crates/barracuda-core/src/ipc/methods/{device,health,primal}.rs` — sovereign IPC reporting
- `README.md` — Deployment Modes and GPU Constraints section
- `CONTEXT.md` — Deployment Constraints section
- `BREAKING_CHANGES.md` — 0.3.12 migration guide with TensorSession API table
- `CHANGELOG.md` — Sprint 40+41 entries
- `WHATS_NEXT.md` — updated with Sprint 40+41
- `specs/REMAINING_WORK.md` — Sprint 41 achievements

---

## Quality Gates

- `cargo fmt --all -- --check` ✓
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` ✓ (zero warnings)
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` ✓
- `cargo nextest run --workspace --profile ci` ✓ (4,251 passed, 14 skipped, 0 failures)

---

## Impact on Upstream Springs

Springs can now:
1. Use `Auto::new()` and match on `DiscoveredDevice` for sovereign-aware compute
2. Adopt `session::TensorSession` with documented stable API (migration guide published)
3. Reference deployment matrix for musl-static/ecoBin GPU constraints
4. Use `Auto::new_wgpu()` when specifically needing local tensor buffers
