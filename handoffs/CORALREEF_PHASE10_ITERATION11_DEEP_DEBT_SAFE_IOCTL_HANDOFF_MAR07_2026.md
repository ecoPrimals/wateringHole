# coralReef — Phase 10 Iteration 11: Deep Debt Reduction + Safe Ioctl Surface

**Date**: March 7, 2026  
**Primal**: coralReef  
**From**: Iteration 10 (AMD E2E Verified) → Iteration 11 (Deep Debt Reduction)

---

## Summary

Iteration 11 focuses on deep technical debt reduction and modern Rust idiom
compliance. No new features — purely structural improvement to the codebase.

## Metrics

| Metric | Value |
|--------|-------|
| Total tests | 991 |
| Passing | 954 |
| Ignored | 37 |
| Clippy warnings | 0 |
| Production `unwrap()`/`todo!()` | 0 |
| `#[deny(unsafe_code)]` crates | 6/8 |
| AMD E2E status | Verified (RX 6950 XT) |

## Key Changes

### 1. AMD Ioctl Unsafe Surface Consolidation

**Before**: 9 raw `unsafe` blocks scattered across individual ioctl functions,
each containing `drm_ioctl_named()` calls plus 5 separate `unsafe { read_ioctl_output() }`
call sites.

**After**: 2 safe wrapper functions encapsulate all unsafe:
- `amd_ioctl(fd, request, arg, name)` — performs the ioctl syscall
- `amd_ioctl_read(fd, request, arg, name)` — ioctl + union output read

Plus 2 typed request builders: `amd_iowr::<T>(cmd)`, `amd_iow::<T>(cmd)`.

All public ioctl functions (`create_context`, `gem_create`, `submit_command`,
`sync_fence`, etc.) are now fully safe at the call site.

### 2. Dead Code Removal

`DriverError::Unsupported` variant removed — it was defined in production
code but only used in its own display test. No production code ever
constructed this variant.

### 3. Rust 2024 Idiom: `#[allow]` → `#[expect]`

9 `#[allow(dead_code)]` annotations migrated to `#[expect(dead_code, reason = "...")]`
with descriptive reason strings:
- Latency models for future SM targets (SM75, SM80)
- Debug/diagnostic functions (`save_graphviz`)
- IR methods used only in test code
- Enum variants reserved for completeness

23 remaining `#[allow(dead_code)]` are on derive-generated items where
the lint fires incorrectly (used through trait dispatch).

### 4. WGSL Test Corpus Expansion

+2 shaders from hotSpring MD suite:
- `vacf_dot_f64` — velocity autocorrelation dot product (f64, per-particle)
- `verlet_copy_ref` — Verlet reference copy (f64, simple memory ops)

Both compile successfully for SM70 target.

### 5. Cross-Spring Absorption Sync

ABSORPTION.md updated with:
- barraCuda P0/P1 blocker resolution status (all P0/P1 resolved)
- Spring pin versions: groundSpring V96, neuralSpring V89/S131, hotSpring v0.6.19, wetSpring V97e, airSpring V0.7.3
- New Iteration 10 absorption table (AMD E2E, CS_W32_EN, SrcEncoding, 64-bit FLAT, consolidated ioctl)

### 6. Primal Names Audit

All 11 external primal name references in production code are in doc
comments only (provenance documentation). Zero production logic violations.
The compliance test in `capability.rs` correctly enforces the self-knowledge
principle.

### 7. Code Quality

- `hw_amd_e2e.rs`: `Vec::new()` + `push()` chain → `vec![]` macro
- `cargo fmt` applied workspace-wide (import reordering, line wrapping)
- All 35 TODO/XXX comments audited: all are legitimate upstream NV backend ISA gaps

## Impact on Other Primals

**barraCuda**: No API changes. Cross-spring absorption tracking now confirms
all P0/P1 blockers resolved (f64 emission, coralDriver, uniform bindings,
BAR.SYNC).

**toadStool**: No API changes. `shader.compile.*` contract unchanged.

**Springs**: Updated spring pin versions in absorption tracker.

## Checks

- [x] `cargo check --workspace` — PASS
- [x] `cargo test --workspace` — 991 tests (954 passing, 37 ignored)
- [x] `cargo clippy --workspace --all-targets -- -D warnings` — 0 warnings
- [x] `cargo fmt --check` — PASS
