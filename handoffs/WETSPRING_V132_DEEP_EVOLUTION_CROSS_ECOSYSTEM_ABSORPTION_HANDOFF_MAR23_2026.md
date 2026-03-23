# wetSpring V132 — Deep Evolution + Cross-Ecosystem Absorption Handoff

**Date:** 2026-03-23
**From:** wetSpring V132 (deep evolution sprint)
**To:** barraCuda team, toadStool team, All Springs
**License:** AGPL-3.0-or-later
**Supersedes:** WETSPRING_V131_DEEP_EVOLUTION_AUDIT_HANDOFF_MAR22_2026.md

---

## Executive Summary

wetSpring V132 is a deep evolution sprint that absorbed patterns from **7 springs**
and **12+ primals**. It is the **first spring** with **workspace-level lints**. The
crate migrated from deprecated `GpuDriverProfile` to **`DeviceCapabilities`**
(barraCuda **v0.3.7**). The sprint added **ValidationSink**, **PROVENANCE_REGISTRY**,
**`IpcError::is_recoverable`**, **`normalize_method`**, and ecosystem wiring for
validation, IPC, and GPU capability discovery.

---

## What Changed

### Phase 1: Workspace lint infrastructure

- Both crates inherit lint configuration from the **root `Cargo.toml`** (shared
  workspace policy).

### Phase 1b: Per-site safe casts

- Replaced crate-wide blanket casts with **per-site safe casts** (~**75** sites,
  ~**30** files).

### Phase 2: Validation, IPC, and determinism

- **`ValidationSink`** trait for pluggable validation output (CI-friendly).
- **`PROVENANCE_REGISTRY`** with **58** entries (baseline script tracking).
- **`IpcError::is_recoverable()`** for retry classification.
- **Per-test socket isolation** for parallel IPC tests.
- **`f64::total_cmp`** for consistent ordering where float ordering matters.

### Phase 3: IPC naming, GPU capabilities, hardcoding audit

- **`normalize_method()`** for bare IPC method names (aligned with barraCuda).
- **`DeviceCapabilities`** migration (replaces `GpuDriverProfile`).
- **Hardcode audit** — centralized primal names and related constants.

### Phase 4: Dependency and file health

- **Dependency audit** — clean tree.
- **File health** — no files **>800 lines**; **zero** debt markers in tracked policy.

### Phase 5: sweetGrass, streaming, performance, niche

- **sweetGrass** braids integration.
- **`StreamItem` NDJSON** protocol wiring.
- **`performance_surface.report`** (reporting surface for tooling / endpoints).
- **Niche capabilities** expanded to **24**.

---

## Quality Metrics

| Metric | Value |
|--------|-------|
| **Tests** | **1,776** passed (**1,524** + **252**), **0** failed |
| **Clippy** | **0** warnings (pedantic + nursery, workspace) |
| **Unsafe** | **0** (`#![forbid(unsafe_code)]`) |
| **barraCuda** | **v0.3.7**, **150+** primitives, **0** local WGSL |
| **Debt markers** | **0** TODO/FIXME/HACK; **0** `#[allow]` |

---

## barraCuda Primitive Consumption

- **150+** primitives consumed; **zero** local WGSL.
- **Key migration:** `GpuDriverProfile` → **`DeviceCapabilities`** (aligned with
  barraCuda v0.3.7 deprecation path).

---

## Patterns Worth Absorbing Upstream

1. **Workspace lints pattern** — first spring to implement; other springs should
   inherit lints from the workspace root for consistent policy.
2. **PROVENANCE_REGISTRY pattern** — SHA-256 for baseline scripts; reproducible
   audit trail for validation binaries.
3. **ValidationSink pattern** — pluggable output for CI and local runs without
   duplicating validation logic.
4. **`normalize_method()`** — now implemented in both **barraCuda** and **wetSpring**;
   bare or prefixed RPC method names normalize consistently.

---

## Open Items for Next Session

1. **`cargo-llvm-cov`** — line coverage measurement (target **90%**).
2. **License SPDX alignment** — `AGPL-3.0-or-later` vs `AGPL-3.0-only` (repo-wide
   consistency).
3. **`cargo doc --all-features`** — zero-warning documentation pass.
4. **Remaining `.unwrap()` reduction** in IPC/IO modules.
5. **`ComputeDispatch` migration** — P3 priority.
6. **`BatchReconcileGpu`** — request to barraCuda (`reconciliation_gpu` still CPU
   passthrough until upstream primitive lands).
