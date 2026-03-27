<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Iteration 65 — Deep Debt Solutions + Ecosystem Integration

**Date**: March 24, 2026
**Phase**: 10+ (Iter 65)
**Tests**: 3956 passing, 0 failed, ~119 ignored (hardware-gated)
**Coverage**: ~66% workspace line coverage (llvm-cov)

---

## Summary

Full execution on all 20 audit action items from Iter 64's comprehensive audit.
Smart refactoring by domain (not just splitting), ecosystem protocol integration
(`identity.get`, `capability.register`, `ipc.heartbeat`), hardcoding evolution to
capability-based discovery, SAFETY comment evolution for all unsafe blocks,
and targeted test coverage expansion across all undercovered crates.

## What Changed

### Compiler Warnings — All Resolved

- `schedule.rs`: Prefixed debug-assertion-only `live_in_count` parameters with `_`
- `dma.rs`: Fixed 2 broken intra-doc links (`super::DmaBuffer` → `DmaBackend`, `VfioDevice::from_received` → backtick form)
- `registers.rs` + `types.rs`: Replaced 3 unfulfilled `#[expect(dead_code)]` with `#[allow(dead_code, reason = "...")]`
- `cargo build --release`: zero warnings

### Safety Evolution

- Added `#![forbid(unsafe_code)]` to `coral-ember/src/main.rs`
- Added `// SAFETY:` comments to all unsafe blocks in coral-driver: cuda launch, `Bar0Rw::from_raw`, volatile MMIO reads

### Smart Refactoring (Domain-Based, Not Just Split)

**handlers.rs (1519 lines → 4 modules)**

| Module | Lines | Domain |
|--------|-------|--------|
| `handlers/mod.rs` | ~80 | BDF validation, device_to_info, shared test infra |
| `handlers/device_ops.rs` | ~550 | Sync device lifecycle (list, swap, health, register access) |
| `handlers/compute.rs` | ~310 | Async compute dispatch + MMU oracle capture |
| `handlers/quota.rs` | ~430 | nvidia-smi vendor isolation + quota management |

**opt_copy_prop/tests.rs (1018 → 973 lines)**

- Extracted `make_shader_with_function` (55 lines, used across 4 test files) into shared `codegen/test_shader_helpers.rs`

### Ecosystem Protocol Integration (wateringHole Compliance)

**identity.get** — New JSON-RPC method per CAPABILITY_BASED_DISCOVERY_STANDARD

- Returns primal self-description (name, version, capabilities, transports)
- Wired on TCP JSON-RPC and Unix newline dispatchers
- `IdentityGetResponse` type in `service/types.rs`

**capability.register** — Fire-and-forget ecosystem registration

- New `ecosystem.rs` module in coralreef-core
- Discovers ecosystem socket at `$XDG_RUNTIME_DIR/biomeos/`
- Sends `capability.register` JSON-RPC on startup
- Degrades gracefully with `tracing::debug` if no ecosystem available

**ipc.heartbeat** — Periodic registration (45s interval)

- Background tokio task, same transport as registration
- Graceful degradation on failure

### Hardcoding Evolution → Capability-Based

- `HOTSPRING_DATA_DIR` → `CORALREEF_DATA_DIR` with `HOTSPRING_DATA_DIR` fallback (backward-compat)
- New `linux_paths::optional_data_dir()` helper centralizes env resolution
- Removed hardcoded "hotSpring" string from `coral-ember/src/swap.rs`
- Integration test for env var precedence

### Test Coverage Expansion

New tests across all undercovered crates:

| Crate | New Tests |
|-------|-----------|
| coral-driver | error Display/From, DRM paths, linux_paths env, GSP knowledge |
| coral-glowplug | config parsing edge cases, health check logic |
| coral-ember | IPC message parsing, config parsing |
| coral-gpu | context accessors, no-device error paths |

## Quality Gates

- `cargo fmt --all -- --check` — pass
- `cargo clippy --all-features -- -D warnings` — pass (0 warnings)
- `cargo build --release` — pass (0 warnings)
- `cargo test --all-features` — pass (3956 pass, 0 fail)
- `cargo doc --no-deps` — pass (0 warnings)

## wateringHole Compliance — Updated

| Standard | Status |
|----------|--------|
| CAPABILITY_BASED_DISCOVERY_STANDARD | **Compliant** — `identity.get` implemented, capability.register wired |
| Songbird registration | **Implemented** — capability.register + ipc.heartbeat (degrades gracefully) |
| No hardcoded primal names | **Compliant** — HOTSPRING_DATA_DIR evolved to generic CORALREEF_DATA_DIR |

## For Other Primals

- **Songbird/Neural**: coralReef now sends `capability.register` on startup and `ipc.heartbeat` every 45s. The registration looks for `*.json` discovery files in `$XDG_RUNTIME_DIR/biomeos/` with `provides` containing `capability.register`.
- **hotSpring**: `HOTSPRING_DATA_DIR` still works as a fallback. `CORALREEF_DATA_DIR` takes precedence when set.
- **barraCuda**: No API changes. `GpuContext` and `dispatch_precompiled` unchanged.
