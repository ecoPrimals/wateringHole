<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# coralReef — Phase 10, Iteration 54 Handoff

**Date**: March 17, 2026
**Primal**: coralReef
**Phase**: 10 — Iteration 54 (Coverage Expansion + Doc Cleanup + Debt Resolution)

---

## Summary

Iteration 54 is a coverage expansion and cleanup pass following Iteration 53's deep audit. All findings from the comprehensive audit have been executed. This iteration focused on pushing test coverage deeper into low-coverage areas, cleaning root documentation with accurate metrics, auditing EVOLUTION markers, and removing debris.

## Key Metrics

| Metric | Iter 53 | Iter 54 | Delta |
|--------|---------|---------|-------|
| Tests passing | 2241 | 2364 | +123 |
| Line coverage | 58.16% | 59.92% | +1.76% |
| Region coverage | 57.75% | 59.39% | +1.64% |
| Function coverage | 68.50% | 69.45% | +0.95% |
| Doc warnings | 10 | 0 | -10 |
| EVOLUTION markers | 9 | 10 | +1 (AMD Metal) |
| Files over 1000 LOC | 0 | 0 | — |

Testable code coverage (excluding hardware-gated driver and generated ISA tables): **72.7%**

## Changes

### Test Coverage Expansion (+123 tests)

- **40 constant folding tests** (`fold.rs`): integer add/abs, identity elimination (add 0, mul 1), bitwise/logic (And, Or, Xor, PopC), shift operations, comparison/predicate (ISetP Eq/Lt/Ge/False/True, IMnMx), other ops (Lea, Prmt, Flo, Shf), FoldData equality
- **30+ coral-glowplug tests**: config sysfs hex parsing, device slot management, personality trait implementations (Amdgpu, Unbound), personality registry, JSON-RPC dispatch for all methods (device.list/get/health/swap, health.check/liveness, daemon.status/shutdown, unknown method), TCP bind to 127.0.0.1:0, BDF arg parsing
- **30+ coral-driver tests**: PCI config byte parsing (NVIDIA, AMD, too-short), GpuVendor detection and Display, PCI PM state, PciBar/PciCapability construction, PM capability parsing, PCIe link speed parsing, PM4 packet encoding, GEM buffer struct construction, RM alloc param construction and handle formulas
- **12 codegen tests**: opt_prmt (src_idx1 inline, imm source, nested prmt with inner imm), naga_translate (all/any vector, f64 add, array length, assign_regs via full compile), lower_f64 (exp2→DFMA, sqrt→Newton-Raphson), builder (prmt identity→copy_to, lop2 predicate, predicated builder, uniform builder)
- **7 api.rs + spiller.rs tests**: eprint_hex no-panic, debug re-export, two-block single-predecessor spill, very-low-limit spill stress, no-spill-needed high-limit, UPred spilling to UGPR, pinned value skip

### Doc Cleanup

- 10 unresolved `DriverError` doc links in `rm_client/alloc.rs` fixed with full crate path → zero `cargo doc` warnings
- README.md, STATUS.md, WHATS_NEXT.md, COMPILATION_DEBT_REPORT.md, CHANGELOG.md all updated with Iteration 54 metrics
- PRIMAL_REGISTRY.md updated: coralReef Iteration 50 → Iteration 54
- CORALREEF_LEVERAGE_GUIDE.md updated: Iteration 53 → Iteration 54

### EVOLUTION Markers Audit

10 total markers catalogued with feasibility assessment:
- 3 feasible now: SM32 .s modifier, reserved GPR modeling, jump threading
- 3 need ISA docs: CBuf ALU encoding, PrmtSel non-Index, OpBra .u form
- 3 need scheduling docs: co-issue latency, Kepler dual-issue, FU tracking
- 1 blocked by hardware: AMD Metal MI50 support

### Debris Cleanup

- `hotSpring/data/metal_maps/titan_v_gv100_metal_map.json` (106K lines, hardware test output) removed from git tracking, added to `.gitignore`
- No archive directories, stale files, TODO/FIXME/HACK markers, or orphaned scripts found

### File Size Compliance

- `pci_discovery.rs` tests extracted to `pci_discovery_tests.rs` (1027→890 LOC production)
- All files under 1000 LOC (excluding auto-generated ISA tables which are exempt)

## Coverage Breakdown

| Bucket | Lines | Coverage |
|--------|------:|--------:|
| coralreef-core | 4,610 | 94.6% |
| coral-reef (compiler) | 44,233 | 71.3% |
| coral-glowplug | 1,920 | 58.4% |
| coral-driver | 17,436 | 23.4% |
| Excl. hw-gated/generated | 51,760 | 72.7% |
| **TOTAL** | **70,010** | **59.9%** |

### Path to 90%

The gap is dominated by hardware-gated code:
- **coral-driver** (13,351 missed lines): requires GPU hardware for VFIO/DRM/ioctl paths
- **Arch-specific ISA encoders** (~6,000+ missed lines): require full shader compilation targeting each architecture

To reach 90%: bring up hardware-gated tests when GPUs are available, add E2E shader compilation tests through full pipeline.

## Verification

```
cargo fmt --all -- --check    → PASS
cargo clippy --workspace --all-targets -- -D warnings → PASS (0 warnings)
cargo doc --workspace --no-deps → PASS (0 warnings)
cargo test --workspace        → PASS (2364 tests, 0 failed, 0 ignored)
```

## Ecosystem Impact

- **barraCuda**: No API changes; coralReef coverage improvements increase confidence in the sovereign compute pipeline
- **toadStool**: No changes needed; coralReef IPC contract stable since Iteration 52
- **wateringHole**: PRIMAL_REGISTRY and CORALREEF_LEVERAGE_GUIDE updated

## Next Steps

- Hardware validation: Titan V (nouveau/VFIO), RTX 5060 (UVM dispatch)
- Coverage: exercise arch-specific encoders via E2E shader compilation tests
- EVOLUTION markers: implement feasible-now optimizations (#2 SM32 .s, #6 reserved GPRs, #10 jump threading) when prioritized
