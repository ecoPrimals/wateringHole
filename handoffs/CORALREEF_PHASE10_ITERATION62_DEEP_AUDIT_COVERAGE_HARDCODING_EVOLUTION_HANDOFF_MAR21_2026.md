<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Phase 10, Iteration 62 Handoff

**Date**: March 21, 2026
**Primal**: coralReef (sovereign Rust GPU compiler)
**Phase**: 10 — Iteration 62 (Deep Audit + Coverage + Hardcoding Evolution)
**From**: Iteration 61 (DI Architecture + Coverage Evolution)

---

## Summary

Comprehensive codebase audit against wateringHole standards (IPC v3, UniBin, ecoBin,
genomeBin, semantic naming, sovereignty, AGPL3). All quality gates verified. Coverage
expanded with 154 new tests, hardcoded paths evolved to env-overridable helpers,
doc warnings eliminated, and `#[expect]` suppressions cleaned.

## Metrics

| Metric | Before (Iter 61) | After (Iter 62) |
|--------|-------------------|-------------------|
| Tests passing | 3306 | **3460** (+154) |
| Tests failed | 0 | 0 |
| Tests ignored | 108 | 108 |
| Line coverage | 67.6% | **68.7%** |
| Function coverage | 75.7% | **76.3%** |
| Crates above 90% | 6 | **8** |
| Clippy warnings | 0 | 0 |
| Rustdoc warnings | 4 | **0** |
| File size violations | 0 | 0 |

## What Changed

### Rustdoc Warnings (4 → 0)
- Fixed `MockSysfs` intra-doc link scope (`sysfs_ops.rs`)
- Removed redundant explicit `SysfsOps` link targets (`lib.rs`, `device/mod.rs`)
- Fixed private item `verify_drm_isolation` doc reference (`swap.rs`)
- Fixed `SysfsOps` scope in `health.rs`

### Coverage Expansion (154 new tests)

**coral-glowplug**: MockSysfs method testing, health loop circuit breaker, IPC
dispatch, env path overrides. sysfs_ops 92%, health 91%, config 93%.

**coral-ember**: All vendor lifecycle match arms tested (NVIDIA, AMD Vega/RDNA,
Intel, BrainChip, Generic), IPC success paths, swap "unbound" success path.
vendor_lifecycle 84%, ipc 85%.

**coral-gpu**: Driver env defaults, cache error paths, SM arch mapping roundtrip,
FMA per-arch. fma/hash/kernel/preference at 100%, pcie 98%.

**coral-reef codegen**:
- SM32 float64: 0% → 52% (new encoder test suite)
- SM32 conv: 40% → 87%, float: 69% → 77%, misc: 40% → 75%
- SM50 conv: 33% → 75%, float: 62% → 73%, int: 67% → 69%, misc: 40% → 74%
- SM50 control: 23% → 47%, mem: 75% → 76%
- SM70 control: 50% → 54%, conv: 77% → 80%
- opt_bar_prop: 56% → 58%, opt_copy_prop: 57% → 59%

**coral-driver**: `linux_paths.rs` 58% → 100% (all env-overridable helpers tested)

### Hardcoding Evolution

New `coral_driver::linux_paths` module centralizes all sysfs/proc path construction:
- `CORALREEF_SYSFS_ROOT` (default `/sys`)
- `CORALREEF_PROC_ROOT` (default `/proc`)
- `CORALREEF_NVIDIA_FIRMWARE_ROOT` (default `/lib/firmware/nvidia`)
- `CORALREEF_HOME_FALLBACK` (default `/root`)

All sysfs/proc operations across coral-driver, coral-glowplug, coral-ember, and
coral-gpu now route through these helpers. Enables test isolation and non-standard
deployments without code changes.

### `#[expect]` Cleanup
- Removed dead code suppressions where code was actually used or removable
- Replaced JSON-RPC field `dead_code` suppressions with `#[serde(rename)]`
- Cleaned stale suppressions across workspace

### Dependency Analysis
- 227 production deps, all pure Rust
- Zero `*-sys`, `ring`, `openssl`
- `libc` transitive only: tokio → mio → signal-hook-registry (tracked mio#1735)
- OpenTelemetry unconditional in tarpc 0.37 (upstream tracked)

### Root Docs Updated
All root .md files (README, CONTRIBUTING, START_HERE, WHATS_NEXT, COMPILATION_DEBT_REPORT,
EVOLUTION, ABSORPTION, STATUS, CHANGELOG), plus docs/HARDWARE_TESTING.md and
specs/CORALREEF_SPECIFICATION.md synchronized to Iteration 62 metrics.

## wateringHole Compliance Assessment

| Standard | Status |
|----------|--------|
| PRIMAL_IPC_PROTOCOL v3.0 | **Compliant** — JSON-RPC 2.0 + tarpc, semantic methods, multi-transport |
| UNIBIN_ARCHITECTURE_STANDARD | **Compliant** — single binary, clap, --help/--version, signals |
| ECOBIN_ARCHITECTURE_STANDARD | **Compliant** — pure Rust, zero *-sys, platform-agnostic IPC |
| SEMANTIC_METHOD_NAMING_STANDARD | **Compliant** — `shader.compile.*`, `health.*`, `daemon.*` |
| CAPABILITY_BASED_DISCOVERY_STANDARD | **Compliant** — capability-based, zero hardcoded primal names |
| AGPL-3.0-only | **Compliant** — SPDX headers on all files |

### Partial Compliance
- **Songbird registration**: Not implemented (Songbird primal not yet available)
- **90% coverage target**: 68.7% overall. Main blockers: coral-driver (29.9%, hardware-gated),
  daemon main.rs files, deep codegen paths needing per-instruction test matrices

## Known Gaps

1. **Coverage distance to 90%**: Hardware-gated code in coral-driver dominates the gap.
   Non-hardware coverage is ~82%+.
2. **NVIDIA hardware validation**: Nouveau UAPI and UVM dispatch pipelines wired but
   awaiting on-site hardware testing (Titan V + RTX 5060).
3. **Intel backend**: Placeholder architecture variants only.
4. **`coral-reef-stubs` naming**: Historical name; 80+ files reference it. Rename
   deferred to dedicated iteration.
5. **OpenTelemetry weight**: tarpc 0.37 pulls opentelemetry unconditionally. Tracked
   for upstream feature-gating.

## Quality Gates

```
cargo fmt --all -- --check         ✅ PASS
cargo clippy --all-features -D warnings  ✅ PASS (0 warnings)
cargo test --all-features          ✅ PASS (3460+ pass, 0 fail, 108 ignored)
cargo doc --all-features --no-deps ✅ PASS (0 warnings)
cargo llvm-cov --workspace         68.7% line, 76.3% function
```

## Next Iteration Priorities

1. **Hardware validation**: Nouveau UAPI on Titan V, UVM dispatch on RTX 5060
2. **Coverage push**: Focus on non-hardware paths in coral-glowplug device modules,
   coral-ember swap/sysfs, remaining codegen encoder gaps
3. **Songbird registration**: Implement when Songbird primal is available
4. **OpenTelemetry trimming**: Track tarpc upstream for feature-gated OTel
