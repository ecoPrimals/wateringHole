# ToadStool S188 — Cross-Primal Doc Cleanup Handoff

**Date**: April 5, 2026
**Session**: S188
**Author**: westgate (ecoPrimals)

---

## Summary

Cross-primal doc comments and error strings cleaned to capability-based language across 61 files in all ToadStool crates. Full deep-debt audit confirmed all remaining items are at irreducible boundaries.

## Accomplishments

### Cross-Primal Name Evolution (550 → 425)

Replaced primal-specific names with capability-based language in doc comments, error messages, and user-facing strings:

| Old Name | New Name |
|----------|----------|
| Songbird | coordination service |
| BearDog | security service |
| NestGate | storage service |
| Squirrel | intelligence service |
| CoralReef | visualization service |
| BarraCuda | GPU compute / wgpu |

**61 files changed** across: `auto_config`, `toadstool-core`, `client`, `server`, `distributed`, `runtime` (gpu, universal, adaptive, secure_enclave, container, edge), `integration`, `management`, `neuromorphic`, `ember`, `glowplug`, `hw-learn`, `hw-safe`, `nvpmu`, and `cli`.

### Remaining 425 References (Intentional Backward-Compat)

All 425 remaining cross-primal references are in backward-compatibility mechanisms:

- **Serde aliases** — `#[serde(alias = "BearDogAuth")]` for existing config/manifest deserialization
- **Env var fallbacks** — `BEARDOG_URL`, `SONGBIRD_ENDPOINT`, `SQUIRREL_ENDPOINT`, `CORALREEF_SOCKET`
- **`interned_strings.rs`** — Legacy constants for IPC routing
- **`capability_helpers.rs`** — Mapping tables for legacy orchestrator labels
- **Wire-protocol constants** — `node_type::NESTGATE/BEARDOG/SONGBIRD` in discovery client
- **Test fixture data** — Legacy names used to verify backward-compat parsing

### Full Audit Results

| Metric | Value |
|--------|-------|
| Production `panic!()` | 0 |
| Production `todo!()`/`unimplemented!()` | 0 |
| Production mocks | All gated behind `#[cfg(any(test, feature = "test-mocks"))]` |
| Unsafe code | 15 blocks — all at FFI boundaries (V4L2, VFIO DMA, madvise, GPU memory, CUDA, OpenCL) |
| `thread::sleep` | 8 — all legitimate hardware patterns (udev, NPU register, CPU sampling, HW init) |
| `block_on()` | 10 — all legitimate sync→async bridges (CLI, installer, GPU lifecycle) |
| Largest production file | 679L (well under 800L threshold) |
| Doc warnings | 0 |
| Clippy warnings | 0 |
| Tests | 21,512 passed, 0 failed, 103 ignored |

## Quality Gates

- `cargo fmt --all -- --check` — 0 diffs
- `cargo clippy --all-targets -- -D warnings` — 0 warnings
- `cargo doc --no-deps --document-private-items` — 0 warnings
- `cargo test --all-targets` — **21,512 passed, 0 failed**

## Remaining Debt

| Item | Status |
|------|--------|
| D-COV: 90% test coverage | ~80-85% (hardware-dependent paths remain) |
| D-TARPC-PHASE3: tarpc binary transport | Not yet wired |
| D-EMBEDDED-PROGRAMMER: ISP/ICSP impls | Placeholder errors |
| D-EMBEDDED-EMULATOR: 6502/Z80 emulation | Placeholder errors |

## Files Changed

Commit `ac7a375f` — 61 files changed, 120 insertions, 119 deletions.

---

Part of [ecoPrimals](https://github.com/ecoPrimals) — sovereign compute for science and human dignity.
