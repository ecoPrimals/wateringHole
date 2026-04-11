# coralReef Iter 79 — Deep Debt Cleanup: ecoBin Deny, IPC Latency, Configurable Hardcoding Handoff

**Date**: April 11, 2026
**Primal**: coralReef
**Iteration**: 79
**Matrix**: ECOSYSTEM_COMPLIANCE_MATRIX v2.7.0

---

## Executive Summary

Deep debt cleanup across four axes: (1) ecoBin v3 `deny.toml` C/FFI ban list aligning
coralReef with ecosystem-wide pure-Rust supply chain enforcement, (2) IPC compile latency
and multi-stage ML pipeline documentation + machine-readable capability metadata,
(3) hardcoded values evolved to env-configurable patterns, (4) primal self-knowledge in
health responses. All quality gates green. 4,462 tests passing.

---

## Part 1: What Changed

### ecoBin v3 `deny.toml` C/FFI Bans (CR-01)

| Category | Banned Crates |
|----------|--------------|
| C crypto / TLS | `openssl-sys`, `openssl`, `native-tls`, `aws-lc-sys`, `aws-lc-rs`, `ring` |
| C build tooling | `cmake`, `pkg-config`, `bindgen`, `vcpkg` |
| C compression / system FFI | `bzip2-sys`, `curl-sys`, `libz-sys`, `zstd-sys`, `lz4-sys`, `libsqlite3-sys` |

Each entry includes `reason` and `use-instead` fields. `cargo deny check` passes.
coralReef is now aligned with barraCuda/NestGate/Songbird ban lists.

### IPC Composition & Latency Documentation

- `capability.list` metadata extended with `compile_latency` (p50/p99 per compile path)
  and `multi_stage_ml` (support for sequential compile-and-dispatch pattern)
- New doc: `docs/IPC_COMPOSITION_AND_LATENCY.md` — composition patterns for ML pipelines,
  latency budget tables per spring, scaling guidance, caching strategy
- Answers neuralSpring question: multi-stage ML pipelines supported by composition
  (call `shader.compile.wgsl` N times, cache binaries, dispatch sequentially)

### Hardcoding → Configurable

| Before | After | Env Var | Default |
|--------|-------|---------|---------|
| Hardcoded 45s heartbeat interval | Env-configurable | `CORALREEF_HEARTBEAT_SECS` | 45 |
| Hardcoded 5s Intel FLR settle | Env-configurable | `CORALREEF_INTEL_SETTLE_SECS` | 5 |
| Hardcoded `ECOSYSTEM_NAMESPACE` const in BTSP | Runtime env lookup | `BIOMEOS_ECOSYSTEM_NAMESPACE` | "biomeos" |
| Hardcoded primal name "coral-glowplug" in health | `env!("CARGO_PKG_NAME")` | compile-time | crate name |

### Intel Lifecycle Evolution

`IntelXeLifecycle` evolved from struct-literal stub to proper constructor (`::new(device_id)`)
with configurable settle time via `CORALREEF_INTEL_SETTLE_SECS`. `device_id` retained for
future Arc vs Battlemage differentiation.

### Lint & Coverage

- Conditional `#[expect]` → `#[allow]` for `clippy::wildcard_imports` and
  `clippy::enum_glob_use` in `codegen/mod.rs` (these lints fire conditionally between
  library and test compilation targets, making `#[expect]` fail under `--all-targets`)
- 3 new TCP IPC tests for coral-ember `handle_client_tcp` path

---

## Part 2: Quality Gate

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | PASS (0 warnings) |
| `RUSTDOCFLAGS='-D warnings' cargo doc --all-features --no-deps` | PASS |
| `cargo test --workspace --all-features` | 4,462 passed, 0 failed, 153 ignored |
| `cargo deny check` | PASS (ecoBin v3 bans active) |
| All files <1000 lines | PASS |
| Zero TODO/FIXME/HACK in production | PASS |
| SPDX headers | PASS |

---

## Part 3: Patterns Worth Absorbing

### Capability Metadata as IPC Contract

Rather than documenting compile latency only in markdown, we added machine-readable
`compile_latency` and `multi_stage_ml` fields to the `capability.list` response.
Springs can query this at runtime to plan composition budgets without hardcoded
assumptions about coralReef's performance.

### Env-Var Override Pattern

Configurable values use a consistent pattern:
```rust
let val = std::env::var("CORALREEF_FOO")
    .ok()
    .and_then(|v| v.parse().ok())
    .unwrap_or(DEFAULT);
```

For `&'static str` values (namespace, socket paths), use `OnceLock` for lifetime stability:
```rust
fn ecosystem_namespace() -> &'static str {
    static NS: OnceLock<String> = OnceLock::new();
    NS.get_or_init(|| std::env::var("BIOMEOS_ECOSYSTEM_NAMESPACE").unwrap_or_else(|_| "biomeos".into()))
}
```

### Self-Knowledge via Compile-Time Introspection

`env!("CARGO_PKG_NAME")` and `env!("CARGO_PKG_VERSION")` in health responses means the
binary always reports its true crate identity without hardcoded strings that drift.

---

## Part 4: Compliance Matrix Update

| Tier | Before | After | Notes |
|------|--------|-------|-------|
| T1 Build | A+ | A+ | ecoBin v3 deny.toml bans active |
| T2 UniBin | A | A | No change |
| T3 IPC | A | A+ | compile_latency + multi_stage_ml in capability metadata |
| T4 Discovery | B | B | No change (BTSP Phase 2 awaits BearDog e2e) |
| T5 Naming | A | A | No change |
| T6 Responsibility | A | A | No change |
| T7 Workspace | A | A | No change |
| T8 Presentation | A | A+ | Root docs synchronized to Iter 79; IPC composition guide |
| T9 Deploy | C | C | musl-static not yet verified |
| T10 Live | N/T | N/T | Not deployed |
| **Rollup** | **A+** | **A+** | T3 + T8 elevated |

---

## Remaining Work

- **coral-driver `Result<_, String>` wave 4+**: ~20 remaining functions in deep hardware interaction code
- **musl-static verification (T9)**: Cross-compile both x86_64 and aarch64
- **plasmidBin submission (T9/T10)**: Requires musl-static builds
- **Coverage push**: Target 90% via `cargo llvm-cov`; hardware tests need local GPU
- **BTSP Phase 2 end-to-end**: Needs BearDog `btsp.session.create` service for integration test
- **tarpc OTEL**: Hard dependency in tarpc 0.37 — awaiting upstream feature gate

---

## Files Changed (15 files, +180 / -35)

### New files
- `docs/IPC_COMPOSITION_AND_LATENCY.md` — IPC composition patterns and latency budgets

### Key modified files
- `deny.toml` — ecoBin v3 C/FFI ban list
- `crates/coralreef-core/src/capability.rs` — compile_latency + multi_stage_ml metadata
- `crates/coralreef-core/src/ecosystem.rs` — configurable heartbeat interval
- `crates/coral-ember/src/vendor_lifecycle/intel.rs` — IntelXeLifecycle configurable constructor
- `crates/coral-ember/src/vendor_lifecycle/detect.rs` — updated IntelXeLifecycle::new call
- `crates/coral-ember/src/vendor_lifecycle/tests.rs` — updated test constructors
- `crates/coral-ember/src/ipc/tests.rs` — 3 new TCP IPC tests
- `crates/coral-glowplug/src/socket/handlers/device_ops.rs` — CARGO_PKG_NAME in health
- `crates/coral-glowplug/src/socket/btsp.rs` — ecosystem_namespace() from env
- `crates/coral-reef/src/codegen/mod.rs` — #[expect] → #[allow] for conditional lints
