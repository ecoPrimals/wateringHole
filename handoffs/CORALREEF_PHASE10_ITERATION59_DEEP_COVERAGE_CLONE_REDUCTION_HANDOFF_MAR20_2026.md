<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Phase 10 — Iteration 59 Handoff

**Date**: March 20, 2026
**Primal**: coralReef
**Phase**: 10 — Spring Absorption + Compiler Hardening
**Iteration**: 59

---

## Summary

Deep coverage expansion across all NVIDIA shader model encoder backends
(SM20–SM70), clone reduction in IR manipulation paths, `panic!` → `ice!`
evolution for structured ICE reporting, and comprehensive test additions
for glowplug socket/personality, unix JSON-RPC edge cases, and the
lower_copy_swap pass. Coverage jumped from 60.16% to 65.8% line
(79.6% non-hardware code). +358 tests (2680 → 3038).

---

## Changes

### 1. Encoder Test Coverage Expansion (+300 tests)

- **SM20/SM32/SM50 texture encoders**: All older texture backends now tested
  (bound/bindless TexRef, TexDim variants, TexLodMode, TexOffsetMode, ICE
  paths for CBuf and unsupported features). Each encoder gets `#[should_panic]`
  tests for `ice!` paths.
- **SM20–SM70 memory encoders**: OpLd/OpSt (Global A32/A64, Local, Shared),
  OpLdc (all LdcMode variants), OpAtom (all AtomOp variants including CmpExch),
  OpCCtl, OpMemBar, OpAL2P/OpALd/OpASt/OpIpa, OpSuLdGa/OpSuStGa.
- **SM32+SM70 control flow**: OpBra, OpExit, OpBar, OpVote, OpNop, predicated
  instructions.
- **SM70 ALU misc**: OpShf, OpShl, OpShr, OpPrmt, OpShfl, OpR2UR, OpBMsk.
- **SM20–SM70 integer ALU**: OpIAdd2/OpIAdd3, OpIMul, OpIMad, OpISetP
  (all comparison modes), OpIMnMx, OpLea, OpPopc, OpFlo, OpIAbs, OpINeg.
- **SM50 float64** (0% → covered): OpDAdd, OpDMul, OpDFma, OpDSetP, OpDMnMx
  with all FRndMode and FloatCmpOp variants.
- **SM70 float16** (0% → covered): OpHAdd2, OpHMul2, OpHFma2, OpHSet2,
  OpHSetP2, OpHMnMx2 with imm/CBuf paths.
- **Lower copy/swap**: GPR OpMov, Pred→GPR OpSel, UGPR+CBuf OpLdc, Mem↔GPR
  Ld/St, OpSwap XOR chain, OpPLop3, OpR2UR vs OpVote.

### 2. Glowplug + IPC Coverage

- **socket.rs**: Protocol parsing, dispatch for all device.* and health.*
  methods, error responses, unknown methods, TCP edge cases, concurrent
  connections.
- **personality.rs**: All personality traits (Nvidia, Xe, I915, Akida),
  PersonalityRegistry, aliases, HBM2 support flags, driver modules.
- **unix_jsonrpc advanced**: Socket creation failures (parent is file),
  stale socket removal, mid-line disconnect, 256KiB large payloads,
  16 concurrent connections, early peer close, drop join handle semantics,
  XDG_RUNTIME_DIR env path resolution.

### 3. Clone Reduction

- **lower_f64/newton.rs**: Eliminated unnecessary SSARef clones — compute
  `x_hi` first, then move `x` into `Src::from(x)`.
- **lower_f64/poly/trig.rs**: Single clone for `r_sq` instead of clone +
  `Src::from(r_sq.clone())`.
- **naga_translate/func_math*.rs**: `translate_math` now passes `&SSARef`
  and `Option<&SSARef>` to delegates — failed delegates no longer pay three
  SSARef clones per attempt.

### 4. `panic!` → `ice!` Evolution

All `panic!("Illegal instruction...")` calls in SM70/SM75/SM80/SM89/SM120
instruction latency tables converted to `crate::codegen::ice!(...)` for
structured ICE reporting with file/line information. Typo "instuction"
fixed to "instruction" across all files. `clippy::manual_assert`
`#![expect]` removed from `codegen/mod.rs` (no longer fires after
conversion).

### 5. File Compliance

- `tests_unix_edge.rs` (1088 lines) split into `tests_unix_edge.rs` (861)
  + `tests_unix_advanced.rs` (227) — all files under 1000 lines.
- New test files use `#[cfg(test)] #[path = "..."] mod tests;` pattern
  to keep production files compact.

### 6. CI Alignment

- `.github/workflows/ci.yml` updated: all steps now use `--all-features`
  and `--all-targets` to match local development workflow.

---

## Metrics

| Metric | Before (Iter 58) | After (Iter 59) |
|--------|-------------------|------------------|
| Tests passing | 2680+ | 3038+ |
| Tests ignored | 90 | 102 |
| Line coverage | 60.16% | 65.8% |
| Region coverage | 60.62% | 66.1% |
| Function coverage | 69.03% | 72.9% |
| Non-hardware coverage | 75.8% | 79.6% |
| coral-reef coverage | 73.4% | 78.3% |
| coralreef-core coverage | 95.8% | 95.8% |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Fmt drift | 0 | 0 |
| .rs files | 476 | 487 |
| Files >1000 lines | 0 | 0 |

---

## Coverage Ceiling Analysis

| Category | Lines | Coverage | Notes |
|----------|-------|----------|-------|
| coral-driver | 18,533 | 28.2% | Hardware-gated (VFIO/ioctl/DRM) |
| coral-ember | 1,002 | 15.5% | Hardware-gated (GPU runtime) |
| coral-gpu | 554 | 34.7% | Hardware-gated (dispatch) |
| **Hardware subtotal** | **20,089** | **27.7%** | Requires live GPU hardware |
| coral-reef | 42,865 | 78.3% | Compiler (testable) |
| coralreef-core | 5,243 | 95.8% | IPC + lifecycle |
| Other non-hw | 7,478 | 88.6%+ | Bitview, stubs, ISA, tools |
| **Non-hardware subtotal** | **55,586** | **79.6%** | |

**Ceiling**: Even 100% coverage of all non-hardware code yields ~81%
overall. The 90% target requires hardware test infrastructure (live GPUs
in CI) or must be scoped to non-hardware code only.

---

## Cross-Primal Impact

- **No API changes** — all changes are internal (tests, clone reduction,
  ICE reporting). JSON-RPC endpoints, tarpc services, compiler APIs all
  unchanged.
- **hotSpring**: No impact. VFIO stack unchanged.
- **toadStool**: No impact. IPC protocol unchanged.
- **barraCuda**: No impact. Compiler performance slightly improved via
  clone reduction in `translate_math`.

---

## Next Steps (Iteration 60+)

1. **Hardware test infrastructure**: Establish GPU-in-CI for coral-driver
   coverage (currently 28.2%)
2. **coral-reef optimizer pass coverage**: opt_copy_prop (59.9%),
   lower_copy_swap (40.6%), builder/emit.rs (32.3%)
3. **GP_PUT hardware validation**: Test cache flush on live Titan V VFIO
4. **UVM hardware validation**: RTX 5060 compute dispatch
5. **AMD MI50 hardware swap**: Validate GFX906 metal register offsets
