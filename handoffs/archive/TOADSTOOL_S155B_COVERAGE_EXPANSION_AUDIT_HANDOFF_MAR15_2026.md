# toadStool S155b — Coverage Expansion + Dependency/Unsafe Audit

**Date**: March 15, 2026
**From**: toadStool (S155b)
**To**: All primals (barraCuda, coralReef, hotSpring, biomeOS)
**Status**: All quality gates PASS

---

## Summary

Comprehensive coverage expansion and ecosystem audits. 806 new test functions across 12 integration test files. Full dependency and unsafe code audits completed.

## Key Changes

### Coverage Expansion (+558 Net New Tests)

- 20,285 → 20,843 total tests, 0 failures
- 12 new integration test files covering:
  - **Server**: hw_learn handlers (0%→85%+), transport/dispatch/science_domains/shader/ollama handlers, unibin/background services
  - **Core common**: error types/context/constructors, auth, capability discovery, platform paths, infant discovery engine/sources/capabilities, primal discovery, service discovery, universal adapter
  - **Config**: validation, runtime defaults, ports, env overrides, profiler builder
  - **Distributed**: cloud federation/pricing/compliance, crypto validation, security provider, network load_balancer/distributor, songbird integration, universal scheduler
  - **CLI**: commands, monitoring, templates, zero-config, ecosystem, executor, daemon, network config
  - **GPU runtime**: engine, scheduler, coordinator, strategy, memory pool, unified memory, distributed/job_tracker/tower_manager, frameworks
  - **Display**: input events, DRM device, IPC
  - **hw-learn**: distiller classify, knowledge store/baselines, observer
  - **toadstool-core**: hardware, npu_dispatch, transport_router, hardware_transport, npu_controller
- Fixed env var race conditions in config tests (temp_env → ENV_LOCK serialization)
- Fixed clippy pedantic in all new test files (hex separators, float_cmp, approx_constant)

### Dependency Audit (Pure Rust Mandate)

- **Confirmed**: ecoBin v3.0 Pure Rust mandate met for default builds
- C FFI limited to optional features: jit (wasmtime), esp32, cuda, opencl, macos-sandbox
- Kernel/platform interfaces: drm-sys, linux-raw-sys (acceptable)
- **Banned**: openssl, tungstenite (enforced in deny.toml)
- **Replaced**: sysinfo→toadstool-sysmon, dirs→etcetera, zstd→ruzstd, lz4→lz4_flex

### Unsafe Code Audit

- 22 crates: `#![forbid(unsafe_code)]`
- 15 crates: `#![deny(unsafe_code)]`
- ~150+ unsafe blocks, all in hardware drivers (DRM, V4L2, VFIO, MMIO, DMA, GPU FFI, secure enclave)
- 100% SAFETY comment coverage
- None can be evolved to safe Rust — all are kernel FFI or trait requirements

### Additional Fixes

- 12 new clippy pedantic errors fixed (hw_learn/unibin export: missing_errors_doc, new_without_default)
- HwLearnHandler now publicly exported with Default impl
- unibin format functions documented with `# Errors` sections
- Cleaned deprecated Prometheus/Grafana config from toadstool.toml
- Cleaned WebSocket reference from biome-production.yaml
- Fixed .clippy.toml broken BearDog reference
- Fixed mmiotrace script tracing path fallback
- Updated PRODUCTION_DEPLOYMENT_GUIDE.md

## Quality Gates

| Gate | Status |
|------|--------|
| cargo fmt | PASS |
| cargo clippy --pedantic | PASS |
| cargo test --workspace | PASS (20,843 / 0 failures) |
| cargo llvm-cov | ~83% line (182K instrumented) |
| License (AGPL-3.0-only) | PASS |
| Production panics/unwraps | 0 |
| Pure Rust (default features) | PASS |

## Cross-Primal Status

| Primal | Status |
|--------|--------|
| **toadStool** | S155b — Coverage expansion complete. 20,843 tests. ~83% coverage. Dependency + unsafe audits done. Pure Rust mandate met. |
| **coralReef** | Iteration 47 — Deep debt evolution. |
| **barraCuda** | v0.35 IPC-first — Sovereign wiring, zerocopy. |
| **hotSpring** | v0.6.31 — Glow plug discovery. VFIO PBDMA context load debugging. PowerManager handoff to toadStool pending. |

## Remaining Work

| Priority | Item | Status |
|----------|------|--------|
| P1 | Coverage 83% → 90% | Hardware-dependent code (neuromorphic, V4L2, DRM, VFIO) needs physical devices or deeper mock layers |
| P1 | Deep integration paths | Cross-primal coordination, cloud federation — needs multi-service test infrastructure |
| P2 | Property-based testing | Computation-heavy modules — candidates for property-based testing |
| P2 | Multi-primal integration test infrastructure | For cross-primal coordination coverage |
| P3 | Spring absorption tracking | Continue absorption tracking |

## Remaining D-COV Gap (83% → 90% Target)

Coverage gap concentrated in:

1. **Hardware-dependent code** (neuromorphic, V4L2, DRM, VFIO) — needs physical devices or deeper mock layers
2. **Deep integration paths** (cross-primal coordination, cloud federation) — needs multi-service test infrastructure
3. **Computation-heavy modules** — candidates for property-based testing

## Next Steps

1. Push coverage 83% → 90% with targeted hardware mocks
2. Property-based testing for numerical computation modules
3. Multi-primal integration test infrastructure
4. Continue spring absorption tracking

## Spring Pins

| Spring | Version |
|--------|---------|
| hotSpring | v0.6.31 |
| groundSpring | V103 |
| neuralSpring | V100/S147 |
| wetSpring | V112 |
| airSpring | v0.7.6 |
| healthSpring | V23 |
| coralReef | Iteration 47 |
| barraCuda | v0.35 IPC-first |

---

*AGPL-3.0-only. Sovereign infrastructure. Capability-based discovery. Self-knowledge principle.*
