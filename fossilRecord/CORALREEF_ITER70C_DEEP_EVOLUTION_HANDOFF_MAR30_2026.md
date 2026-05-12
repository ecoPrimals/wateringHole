# coralReef Iteration 70c — Deep Evolution Handoff

**Date**: March 30, 2026
**Primal**: coralReef (sovereign GPU compiler)
**Phase**: 10 — Iteration 70c
**Builds on**: Iter 70 (ludoSpring V35 gap resolution)

---

## Major Changes

### Typed Error System (coral-ember)

Public API evolved from `Result<_, String>` to structured `thiserror` errors:
- `SysfsError` — sysfs read/write/bind/reset operations
- `SwapError` — swap orchestration (preflight, DRM isolation, VFIO, sysfs, trace)
- `TraceError` — mmiotrace enable/disable/capture

IPC boundary converts to `String` at serialization point for JSON-RPC compatibility.

### Observer Refactoring (coral-glowplug)

`observer.rs` (934 lines) → `observer/` directory:
- `mod.rs` — trait, shared types, registry
- `nouveau.rs` — NouveauObserver
- `vfio.rs` — VfioObserver
- `nvidia.rs` — NvidiaObserver (evolved from stub: extracts PRIV resets, PMC enables, falcon boots, slow-bind anomaly)
- `nvidia_open.rs` — NvidiaOpenObserver
- `tests.rs` — 14 tests

### ECOSYSTEM_NAMESPACE Runtime Configuration

Both `coralreef-core` and `coral-glowplug` now resolve namespace via `$BIOMEOS_ECOSYSTEM_NAMESPACE` env var (default `"biomeos"`). Production code uses `ecosystem_namespace()` function with `OnceLock` pattern.

### Production Tracing Evolution

~100 `println!/eprintln!` → structured `tracing` across:
- 4 diagnostic/oracle files (diff.rs, nouveau_oracle.rs, memory_probe.rs, runner.rs)
- 6 library files (amd/mod, gsp/*, nv/nvidia_drm, nv/bar0)

### Cache Ops Consolidation

`uvm_compute.rs` inline `_mm_clflush` intrinsics routed through central `cache_ops` module.

---

## Build Health

| Check | Status |
|-------|--------|
| `cargo fmt --check` | **PASS** |
| `cargo clippy --all-features -D warnings` | **PASS** (0 warnings) |
| `cargo doc --all-features --no-deps` | **0 warnings** |
| Files > 1000 LOC (production) | **0** |
| Test failures | 2 pre-existing (upstream SSA regression) |

---

## Compliance Updates

All `#[allow]` attributes now have `reason = "..."` strings.
All `#[ignore]` test attributes now have documented reasons.
All production `unsafe` blocks in coral-driver have SAFETY comments.
`HOTSPRING_DATA_DIR` legacy env var emits deprecation warning.

---

## Remaining Debt (tracked)

| Item | Priority | Notes |
|------|----------|-------|
| MmioRegion safe RAII wrapper | P2 | Consolidate 79 unsafe sites into one abstraction |
| vendor_lifecycle `Result<_, String>` | P3 | Trait signature change across 6 implementations |
| sysmem_impl.rs (973 LOC) | Monitor | Approaching limit; extract step helpers when adding code |
| pci_discovery.rs (967 LOC) | Monitor | Split parse vs power APIs when touching |
| coral_ember::run() test coverage | P2 | Needs mock-able startup path |

---

*Evolution is measured not by what we add, but by what we make unnecessary.*
