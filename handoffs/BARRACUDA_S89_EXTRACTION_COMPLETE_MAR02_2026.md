# barraCuda Extraction Complete — Session 89

**Date**: March 2, 2026
**From**: ToadStool / barraCuda (S89)
**To**: All Springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring)
**Classification**: Architectural milestone — barraCuda is now standalone

---

## Status

**barraCuda is live as a standalone primal** at `ecoPrimals/barraCuda/` (GitHub: `ecoPrimals/barraCuda`).

The full barracuda compute library has been extracted from ToadStool with
zero modifications to toadStool. Both repositories pass all tests independently.

---

## What Happened

- 956 Rust source files, 767 WGSL shaders, 61 test files copied from
  `toadStool/crates/barracuda/` to `barraCuda/crates/barracuda/`
- `toadstool-core` dependency gated behind optional `toadstool` feature
  (1 file: `device/toadstool_integration.rs`)
- `akida-driver` dependency gated behind optional `npu-akida` feature
  (1 file: `npu/ml_backend.rs` plus `npu/ops/` and bridge callsites)
- `DeviceSelection` and `HardwareWorkload` enums extracted to `device/mod.rs`
  (always available, no external dependencies)
- `barracuda-core` primal lifecycle wired to barracuda compute library
  (device discovery on `start()`, adapter info in health reports)

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo check -p barracuda` | Clean |
| `cargo clippy -p barracuda -- -D warnings` | Clean |
| `cargo test -p barracuda --lib` | 2,832 passed, 0 failed, 13 ignored |
| `cargo test -p barracuda-core` | 6 passed, 0 failed |
| `cargo fmt --check` | Clean |
| toadStool unchanged | `git status` clean, all tests still pass |

40 tests gated behind `toadstool`/`npu-akida` features (from toadStool's 2,872).

---

## What This Means for Springs

### Now possible

Springs can depend on barraCuda directly for GPU compute without pulling in
the full toadStool workspace:

```toml
# During development (path dep):
barracuda = { path = "../../barraCuda/crates/barracuda", features = ["gpu"] }

# After 1.0.0 release (versioned dep):
# barracuda = { version = "1.0", features = ["gpu"] }
```

### Multi-primal evolution

Springs can now evolve multiple primals in the same session:
- barraCuda (GPU compute) + BearDog (crypto) for FHE pipelines
- barraCuda + NestGate for data archival with GPU processing
- barraCuda + Squirrel for distributed inference

### What stays the same

- All existing APIs are identical — same function signatures, same shader names,
  same test expectations
- toadStool's internal `crates/barracuda/` is unchanged and continues to work
- Springs can continue to use toadStool's barracuda until ready to switch

---

## Next Steps

1. **API surface audit** — ensure all `pub` items are intentional before 1.0.0
2. **GPU validation binary** — `barracuda validate-gpu` (FHE + lattice QCD canary)
3. **Spring migration** — one Spring at a time switches to standalone barraCuda
4. **SemVer 1.0.0** — after Spring validation
5. **toadStool deprecation** — internal barracuda deprecated, depends on standalone

---

## Repository

- GitHub: `ecoPrimals/barraCuda`
- Spec: `barraCuda/specs/BARRACUDA_SPECIFICATION.md`
- toadStool spec: `toadStool/specs/BARRACUDA_PRIMAL_BUDDING.md`
