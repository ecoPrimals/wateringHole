# barraCuda v0.3.11 — Sprint 38: BTSP Phase 2, Capability-Based Discovery, Deep Debt & Idiom Sweep

**Date**: April 9, 2026
**Primal**: barraCuda
**Sprint**: 38
**Status**: Complete — all quality gates green
**Previous**: `BARRACUDA_V0311_DEEP_DEBT_TEST_REFACTOR_CLEANUP_HANDOFF_APR08_2026.md`

---

## Summary

BTSP Phase 2 connection authentication guard implemented and integrated into all
accept loops. BearDog discovery evolved from hardcoded primal name to fully
capability-based pattern. Comprehensive deep debt and idiom sweep: `Box<dyn Error>`
→ typed errors, `#[allow]` → `#[expect]`, smart file refactoring, musl-static
rebuild, GPU test serialization, dependency audit, doc ground truth reconciliation.
4,421 tests pass (was 4,207), all quality gates green.

---

## BTSP Phase 2 — Connection Authentication Guard

| File | Change |
|------|--------|
| `crates/barracuda-core/src/ipc/btsp.rs` | **New module**: `BtspOutcome` enum (DevMode/Authenticated/Degraded/Rejected), `guard_connection()` async orchestration, `discover_beardog_socket()`, `create_btsp_session()` |
| `crates/barracuda-core/src/ipc/mod.rs` | Added `pub mod btsp;` |
| `crates/barracuda-core/src/ipc/transport.rs` | Integrated `btsp::guard_connection().await` into `serve_unix`, `serve_tcp`, `serve_tarpc_unix` accept loops |
| `crates/barracuda-core/tests/btsp_socket_compliance.rs` | 4 new integration tests: DevMode guard, Degraded when BearDog absent, Rejected outcome, acceptance logic |

### Capability-Based Security Discovery

BearDog discovery evolved from hardcoded `beardog-core.json` to:

| Resolution Step | Pattern |
|-----------------|---------|
| 1. Scoped socket | `$BIOMEOS_SOCKET_DIR/{SECURITY_DOMAIN}-{family_id}.sock` |
| 2. Unscoped socket | `$BIOMEOS_SOCKET_DIR/{SECURITY_DOMAIN}.sock` |
| 3. Capability scan | `discover_by_capability()` scans all `*.json` discovery files for `btsp.session.create` |

`SECURITY_DOMAIN = "crypto"` — zero primal name literals in production code.

---

## Typed Error Evolution

| File | Before | After |
|------|--------|-------|
| `btsp.rs` `create_btsp_session()` | `Result<String, Box<dyn Error + Send + Sync>>` | `crate::error::Result<String>` with `BarracudaCoreError::ipc()` |
| `btsp.rs` non-unix stub | `Err("...".into())` | `Err(BarracudaCoreError::ipc("..."))` |

---

## Modern Idiomatic Rust

| File | Change |
|------|--------|
| `cpu_executor/executor.rs` | `#[allow(unreachable_code)]` → `#[expect(unreachable_code, reason = "fallback for architectures without cfg-gated returns")]` |
| `precision_brain.rs` | 703 → 421 LOC: 282L test module extracted to `precision_brain_tests.rs` via `#[path]` |

---

## Fault Injection SIGSEGV — Extended Serialization

4 additional GPU-intensive test binaries added to `gpu-serial` nextest group (`max-threads = 1`)
in both `default` and `ci` profiles, and excluded from `coverage` profile:

- `scientific_chaos_tests`
- `fhe_fault_tests`
- `hotspring_fault_special_tests`
- `multi_device_integration`

Root cause: Mesa llvmpipe concurrent GPU access (upstream limitation, serialization is correct mitigation).

---

## Musl-Static Rebuild

| Target | Change |
|--------|--------|
| `x86_64-unknown-linux-musl` | Removed `linker = "musl-gcc"` from `.cargo/config.toml` — was causing dynamic linking SIGSEGV. Now uses Rust default (static-pie). |
| `aarch64-unknown-linux-musl` | Retained `linker = "aarch64-linux-gnu-gcc"` + `crt-static`. Fixed `unreachable_code` warning in `detect_simd_width()`. |

Both binaries verified as `static-pie linked` via `file` and `--help` execution.

---

## Dependency Audit

All 15 direct dependencies are pure Rust:

| Dependency | Notes |
|-----------|-------|
| `blake3` | `features = ["pure"]` — no C SIMD assembly |
| `wgpu` 28 | WebGPU abstraction |
| `tokio`, `serde`, `thiserror`, `tracing` | Standard ecosystem |

Transitive: `cc` (blake3 build tool, not linked), `renderdoc-sys` (wgpu debugging), `linux-raw-sys` (pure Rust syscall defs). No C code linked into binary.

---

## Doc Ground Truth Reconciliation

| Document | Updates |
|----------|---------|
| `CHANGELOG.md` | Sprint 38 entry |
| `README.md` | Test count 4,207→4,421, Sprint 38 entry |
| `STATUS.md` | Date Apr 8→Apr 9, test count, BTSP Phase 2 in IPC grade, coverage 70% |
| `WHATS_NEXT.md` | Sprint 38 entry, date updated |
| `CONTEXT.md` | Test count 4,207→4,421 |
| `SPRING_ABSORPTION.md` | Date Apr 3→Apr 9 |
| `PURE_RUST_EVOLUTION.md` | Date Apr 1→Apr 9 |
| `SOVEREIGN_PIPELINE_TRACKER.md` | Date Apr 3→Apr 9 |
| `showcase/README.md` | Date Mar 29→Apr 9 |
| `showcase` demos | Shader count 806→826 (2 files) |
| `specs/REMAINING_WORK.md` | Test count table updated |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --workspace --all-features -- -D warnings` | PASS (0 warnings) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | PASS |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo nextest run --workspace --all-features` | **4,421 pass / 0 fail / 14 skip** |
| `cargo llvm-cov nextest --workspace --all-features --profile coverage` | 70% line / 78% function |

---

## Comprehensive Audit Results

| Axis | Status |
|------|--------|
| Production `unsafe` | Zero in barracuda + barracuda-core (`#![forbid(unsafe_code)]`); 1 irreducible in barracuda-spirv (wgpu upstream) |
| Production `.unwrap()` | Zero |
| Production `println!` | Zero |
| Mocks in production | Zero (all `#[cfg(test)]`) |
| Hardcoded primal names | Zero (capability-based discovery) |
| `TODO`/`FIXME`/`HACK` | Zero |
| `#[allow(` | Zero (all evolved to `#[expect(` with reason) |
| `Box<dyn Error>` | Zero (all typed `BarracudaCoreError`) |
| Files >800L | 1 (`wgpu_caps.rs` at 790L — pure data tables, no extractable tests) |
| External C deps | Zero (blake3 `pure`, all deps pure Rust) |
