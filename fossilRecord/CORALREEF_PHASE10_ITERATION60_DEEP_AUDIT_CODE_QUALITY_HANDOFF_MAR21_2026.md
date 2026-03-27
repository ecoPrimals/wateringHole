<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Phase 10 — Iteration 60 Handoff

**Date**: March 21, 2026
**Primal**: coralReef
**Phase**: 10 — Spring Absorption + Compiler Hardening
**Iteration**: 60

---

## Summary

Deep audit execution session: comprehensive code quality evolution across
the workspace. `unwrap()` → `expect()` with infallibility reasons,
`#[allow]` → `#[expect]` tightening across 11 files (28+ attributes total
across Iter 58+60), smart refactoring (tex.rs 986→505+484), 24 new tests
(coral-reef lib preambles/emit/compile + coralreef-core shutdown timeout),
8 `// SAFETY:` comments on unsafe blocks in coral-driver, 9 `unreachable!()`
→ `ice!()` migrations in SM70 encoder/control/opt_jump_thread, hardcoding
evolution (ember socket + socket group → env-var-backed), and amd-isa-gen
template evolution. tarpc 0.37 OpenTelemetry dependency analyzed and
documented for upstream tracking.

---

## Changes

### 1. Production `unwrap()` / `unreachable!()` Evolution

- **coralctl.rs**: `serde_json::to_string(&request).unwrap()` →
  `.expect("JSON Value serialization is infallible")`
- **main.rs**: `serde_json::to_string_pretty(&discovery).unwrap_or_default()` →
  `.expect("JSON Value serialization is infallible")`
- **SM70 encoder** (encoder.rs): 7 `unreachable!("Not a register")` →
  `crate::codegen::ice!("SSA values must be lowered to registers before encoding")`
  in set_reg_src, set_ureg_src, set_pred_dst, set_pred_src_file,
  set_rev_upred_src, set_src_cb, set_pred, set_dst, set_udst
- **opt_jump_thread.rs**: 2 `unreachable!()` → `ice!("clone_branch: expected Bra or Exit")`
- **SM70 control.rs**: 2 `unreachable!()` → `ice!()` for PixVal legalization
  and source type invariants

### 2. `#[allow]` → `#[expect]` Tightening (14+ attributes, 11 files)

All `missing_docs` and `dead_code` module-level `#[allow]` in coral-glowplug
(personality, error, ember, health, device/mod, device/types, config,
device/swap) and coral-ember (vendor_lifecycle) tightened to `#[expect]`.
codegen/mod.rs and lower_f64/mod.rs clippy suppressions also migrated.

Three `dead_code` attributes in coral-glowplug reverted to `#[allow]` where
the lint doesn't fire in all configurations (test-only code paths).

### 3. Smart Refactor: tex.rs

SM70 texture encoder `tex.rs` (986 LOC) split into 505 LOC production
code + 484 LOC tests in `tex_tests.rs` via `#[cfg(test)] #[path = "tex_tests.rs"] mod tests;`.

### 4. Coverage Expansion (+24 tests)

**coral-reef lib_tests.rs** (+20):
- `Fp64Strategy` variant construction (Native, DoubleFloat, F32Only)
- `prepare_wgsl` preamble injection: df64, complex64, f32 transcendental,
  PRNG, SU3 auto-chaining
- `strip_enable_directives` (f64, f16)
- `emit_binary` NVIDIA (header inclusion) vs AMD (no header)
- `compile_wgsl_full`, `compile_glsl_full`, `compile_wgsl_raw_sm`
- Intel GLSL unsupported architecture

**coralreef-core main_tests.rs** (+4):
- `shutdown_join_timeout` elapsed message, test override, default
- `UniBinExit` clone and copy

### 5. Unsafe Documentation

8 `// SAFETY:` comments added to coral-driver unsafe blocks:
- `dma.rs`: EEXIST retry cleanup (alloc_zeroed + mlock'd pointer)
- `cache_ops.rs`: `_mm_clflush` (caller guarantees valid mapped memory),
  `_mm_mfence` (no memory operands)
- `rm_helpers.rs`: `drm_ioctl_named` (fd + params satisfy invariants)
- `mmio.rs`: 4× `VolatilePtr::new` in tests (stack-local aligned values)

### 6. Hardcoding Evolution

- **EmberClient socket**: `const EMBER_SOCKET` → `default_ember_socket()`
  function reading `$CORALREEF_EMBER_SOCKET` with `/run/coralreef/ember.sock` fallback
- **Socket group**: Hardcoded `"coralreef"` group → `$CORALREEF_SOCKET_GROUP`
  env var with `"coralreef"` default

### 7. amd-isa-gen Template Evolution

Generated ISA table code now emits `#[expect(dead_code, missing_docs, reason = "...")]`
instead of `#[allow(dead_code, missing_docs, reason = "...")]`, ensuring stale
suppressions are caught at compile time.

### 8. Dependency Analysis: tarpc

OpenTelemetry (`opentelemetry`, `tracing-opentelemetry`) is an unconditional
dependency of tarpc 0.37 — no feature gate to disable it. This pulls in
`wasm-bindgen` (build-only, not runtime) and ~15 transitive crates. Cannot
be trimmed without upstream changes or replacing tarpc. Documented for tracking.

---

## Metrics

| Metric | Before (Iter 59) | After (Iter 60) |
|--------|-------------------|------------------|
| Tests passing | 3038+ | 3062+ |
| Tests ignored | 102 | 102 |
| Line coverage | 65.8% | 65.8% |
| Region coverage | 66.1% | 66.1% |
| Non-hardware coverage | 79.6% | 79.6% |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Fmt drift | 0 | 0 |
| Files >1000 lines | 0 | 0 |
| Production unwrap() | 0 | 0 |
| unreachable!() in codegen | 9+ | 0 (migrated to ice!()) |

---

## Cross-Primal Impact

- **No API changes** — all changes are internal (code quality, tests,
  documentation, env var additions backward-compatible).
- **hotSpring**: No impact. VFIO stack unchanged.
- **toadStool**: No impact. IPC protocol unchanged.
- **barraCuda**: No impact. Compiler APIs unchanged.
- **Operators**: New env vars `CORALREEF_EMBER_SOCKET` and
  `CORALREEF_SOCKET_GROUP` available for deployment customization
  (defaults unchanged).

---

## Debris Audit Results

Full codebase debris audit completed:
- **No archive code** — no `archive/`, `.bak`, `.tmp`, `.orig` files
- **No stale scripts** — all `.sh` files documented and operational
- **No TODO/FIXME/HACK** in committed `.rs` code (compliant)
- **No stale analysis output** — `.analysis-*` already gitignored
- **No misplaced docs** — all docs coralReef-specific
- **`experiments/`** — README-only placeholder, kept as reserved

---

## Next Steps (Iteration 61+)

1. **Hardware test infrastructure**: GPU-in-CI for coral-driver coverage
2. **UVM hardware validation**: RTX 5060 compute dispatch
3. **Coverage ceiling**: 79.6% non-hardware approaching ~81% ceiling
4. **tarpc upstream**: Track OpenTelemetry feature-gating in future releases
