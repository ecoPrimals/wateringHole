# ToadStool S138 — Deep Debt Audit & Evolution + Coverage Push

**Date**: March 9, 2026
**Primal**: toadStool
**Session**: S138
**Branch**: master

---

## Summary

Comprehensive deep debt audit and evolution session. Full workspace verified with
`cargo fmt`, `cargo clippy -D warnings`, `cargo doc --no-deps`, `cargo test --workspace`
(19,900+ tests), and `cargo llvm-cov` (83.04% line coverage). License aligned to
AGPL-3.0-only. 126 new tests added. 62 unnecessary allow entries removed. 19 clone
reductions. All hardcoded primal names evolved to `interned_strings::primals::*`.

---

## Changes Relevant to Other Primals

### License Alignment: AGPL-3.0-or-later → AGPL-3.0-only

All toadStool SPDX headers and Cargo.toml `license` fields now read `AGPL-3.0-only`.
Other primals should align when convenient. `deny.toml` updated to allow `AGPL-3.0-only`.

### Interned Strings Evolution

All hardcoded primal name strings now use `toadstool_common::interned_strings::primals::*`
constants. Capability strings use `interned_strings::capabilities::*`. This means:

- `"songbird"` → `primals::SONGBIRD`
- `"beardog"` → `primals::BEARDOG`
- `"nestgate"` → `primals::NESTGATE`
- `"toadstool"` → `primals::TOADSTOOL`
- `"coordination"` → `capabilities::COORDINATION`
- `"security"` → `capabilities::SECURITY`
- `"intelligence"` → `capabilities::INTELLIGENCE`

**Note**: `capability_helpers.rs` now maps primal names to interned capability constants.
The string values of some capabilities changed from their prior well_known equivalents
(e.g., `"orchestration"` → `capabilities::COORDINATION`, `"ai"` → `capabilities::INTELLIGENCE`).
If any primal was matching on the old string values, they should update to use the
interned constants.

### Repository URL Standardization

All 33 crate `Cargo.toml` files now use `repository.workspace = true`, inheriting
from the root workspace URL: `https://github.com/ecoPrimals/toadStool`.

### toadstool-sysmon Coverage

The `toadstool-sysmon` crate (pure Rust `/proc` parser, replaces sysinfo) now has 53 tests
covering all parser modules. Other primals using sysmon can rely on tested parsing.

---

## Coverage Report (llvm-cov)

| Metric | Value |
|--------|-------|
| Line coverage | 83.04% (171,796 lines instrumented) |
| Function coverage | 85.88% |
| Region coverage | 84.81% |
| Remaining gap | Neuromorphic drivers, V4L2, DRM display (hardware-dependent) |

---

## Quality Gates (all passing)

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS |
| `cargo doc --workspace --no-deps` | PASS |
| `cargo test --workspace` | PASS (19,900+ tests) |
| Integration tests | 10/11 PASS |

---

## Progressive Showcase (15 demos, 4 levels)

toadStool now has a mature progressive showcase following ecosystem conventions:

| Level | Demos | Description |
|-------|-------|-------------|
| 00 — Local Primal | 5 | hello-compute, hardware-discovery, workload-lifecycle, resource-management, gpu-job-queue |
| 01 — Shader Pipeline | 3 | naga-fallback, coralreef-compile, compile-status |
| 02 — Compute Patterns | 4 | capability-discovery, science-dispatch, deploy-graph, **shader-to-gpu** (headline) |
| 03 — Ecosystem Integration | 3 | songbird-registration, beardog-secured-compute, nestgate-artifact-storage |

**Headline demo** (`02-compute-patterns/04-shader-to-gpu`): Demonstrates the full compute
triangle — coralReef compiles WGSL shader, toadStool orchestrates dispatch, barraCuda
executes on GPU. All demos gracefully degrade when optional primals are absent.

Level 03 demos reference songBird, bearDog, and nestGate interaction patterns. Other primals
can reference these demos when building their own inter-primal showcases.

---

## No Action Required From Other Primals

This session was internal toadStool debt resolution. The only external-facing change is
the license alignment (AGPL-3.0-only) and the interned string constant values, which
other primals should align to when convenient.
