# toadStool S154 — Deep Audit + Quality Gate Evolution

**Date**: March 14, 2026
**From**: toadStool (S154)
**To**: All primals (barraCuda, coralReef, hotSpring, biomeOS)

---

## Summary

Comprehensive deep audit of the toadStool codebase against wateringHole ecosystem standards.
Clippy pedantic fixes, SAFETY documentation, unsafe governance upgrades, smart file refactoring,
capability-based discovery evolution in examples, stale spec cleanup, and targeted test coverage expansion.

## Key Changes

### Quality Gates — All Passing

| Gate | Status |
|------|--------|
| `cargo build --workspace` | PASS |
| `cargo fmt --all -- --check` | PASS — 0 diffs |
| `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic` | PASS — 0 warnings |
| `cargo doc --workspace --no-deps` | PASS — 0 warnings |
| `cargo test --workspace` | PASS — **20,285 tests** (was 20,262), 0 failures, 222 ignored |
| `cargo llvm-cov` | **83.09% line** (target 90%) |
| License | AGPL-3.0-only — all Cargo.toml + all .rs files SPDX headers |
| File size | All production files under 1000 lines |

### Clippy Pedantic Fixes

| Crate | Fixes |
|-------|-------|
| `nvpmu` | Hex literal separators, `#[must_use]`, `# Errors` docs, `let-else`, `is_ok_and`, `Path::extension`, case-sensitive comparison |
| `toadstool-common` | `#[derive(Default)]` for `PciFilter`, doc indentation |
| `toadstool-display` | V4L2 `field_reassign_with_default` → struct update syntax |
| `toadstool-testing` | Mock `unwrap()` → `expect("mock mutex poisoned")`, `# Panics` docs |

### Unsafe Code Governance

- **20 crates upgraded** from `#![deny(unsafe_code)]` to `#![forbid(unsafe_code)]`: distributed, auto_config, security/*, management/*, integration/*, runtime/{orchestration, container, wasm, python, native, edge, specialty}, ml/burn-inference
- **Detailed `// SAFETY:` comments** added to all unsafe blocks in `akida-driver` (volatile_access, dma, ioctl, mod, mmap, mmio) and `runtime/gpu/unified_memory` (backend, buffer, cpu)
- Total: ~70+ unsafe blocks, all fully documented with invariants

### Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `hw_learn.rs` | 985 lines | 9 modules: mod.rs (61), helpers.rs (105), observe_distill.rs (94), apply.rs (118), share_recipe.rs (99), vfio.rs (70), status.rs (57), telemetry.rs (54), auto_init.rs (395) |
| `wgpu_backend.rs` | 974 lines | 4 modules: mod.rs (64), types.rs (299), initialization.rs (185), tests.rs (451) |

### Capability-Based Discovery Evolution

5 examples evolved from hardcoded primal names/ports to capability-based runtime discovery:
- `config_management_demo.rs` — env var + capability fallback
- `capability_discovery_demo.rs` — pure capability discovery
- `modern_patterns_showcase.rs` — `PrimalDiscovery::find_capability()`
- `production_universal_demo.rs` — dynamic endpoint resolution
- `simplified_distributed_demo.rs` — orchestration via config

### Stale Reference Cleanup

| Item | Action |
|------|--------|
| `specs/PRIMAL_CAPABILITY_SYSTEM.md` | REST API references → JSON-RPC 2.0 |
| `docs/reference/PRODUCTION_DEPLOYMENT_GUIDE.md` | Added staleness note (Nov 2025 metrics) |
| `docs/debt/README.md` | Consolidated into root `DEBT.md` pointer |
| `S142_EVOLUTION_PLAN.md` | Fossilized to `ecoPrimals/fossil/toadStool/` |
| `cli/commands/definitions.rs` | "REST endpoints" → "HTTP endpoints" |
| `runtime/adaptive/cache.rs` | Cache namespace `barracuda` → `toadstool-gpu` |
| `nvpmu_monitor.rs`, `nvpmu_apply.rs` | Escaped HTML tags in doc comments |

### Test Coverage Expansion (+49 tests)

| Module | Tests Added |
|--------|-------------|
| `cli/templates` | 21 (TemplateGenerator: new, list, parse, generate, errors, overwrite) |
| `cli/network_config` | 5 (OrchestrationConfigurator: new, default, summary, validate, apply) |
| `toadstool-core/hardware` | 12 (HardwareManager: discover, rescan, devices, counts, types, NPU, errors) |
| `core/config/mdns_discovery` | 11 (MdnsDiscoveryClient: ttl, parse, register, deregister, discover, health) |

## Cross-Primal Status

| Primal | Status |
|--------|--------|
| **toadStool** | S154 — Deep audit complete. 20,285 tests. 83.09% coverage. Pedantic clean. 20 crates `#![forbid(unsafe_code)]`. All SAFETY documented. |
| **coralReef** | Iteration 45 — Deep audit + refactor. VFIO PBDMA work ongoing. |
| **barraCuda** | v0.35 IPC-first — Zero compile-time primal deps. |
| **hotSpring** | v0.6.31 — Glow plug discovery. VFIO PBDMA context load debugging. PowerManager handoff to toadStool pending. |

## Remaining Work

| Priority | Item | Status |
|----------|------|--------|
| P1 | Test coverage → 90% | 83.09% → 90% target. Hardware-dependent code is the gap. |
| P1 | VFIO PBDMA dispatch | Blocked on coralReef USERD_TARGET encoding fix |
| P2 | PowerManager absorption | hotSpring glow plug → toadStool `nvpmu` |
| P2 | E2E sovereign pipeline test | Requires PBDMA dispatch + PowerManager |
| P3 | Conv2D/Pool shader parameters | GPU shaders lack full stride/padding/channels support |

## Spring Pins

| Spring | Version |
|--------|---------|
| hotSpring | v0.6.31 |
| groundSpring | V101 |
| neuralSpring | V100/S147 |
| wetSpring | V112 |
| airSpring | v0.7.6 |
| healthSpring | V19 |
| coralReef | Iteration 45 |
| barraCuda | v0.35 IPC-first |

---

*AGPL-3.0-only. Sovereign infrastructure. Capability-based discovery. Self-knowledge principle.*
