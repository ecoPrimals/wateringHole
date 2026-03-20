<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef Phase 10 — Iteration 58 Handoff

**Date**: March 20, 2026
**Primal**: coralReef
**Phase**: 10 — Spring Absorption + Compiler Hardening
**Iteration**: 58

---

## Summary

Deep debt evolution completing the unsafe code audit, clone waste
elimination, coverage expansion (+83 tests), cross-primal e2e testing,
proc-macro test harness, libc→rustix completion, smart refactoring of
oversized files, and full CI compliance (fmt, clippy -D warnings, doc
-D warnings, all files <1000 LOC).

---

## Changes

### 1. Unsafe Code Evolution

- **DmaBuffer**: `container_fd: RawFd` → `container: Arc<OwnedFd>` — all `BorrowedFd::borrow_raw` calls eliminated, replaced with `.as_fd()` (safe)
- **VfioDevice**: New `vfio_group_open_device_fd()` wrapper consolidates the only `OwnedFd::from_raw_fd` into a single audited location
- **SCM_RIGHTS** (coral-ember/ipc.rs + coral-glowplug/ember.rs): **All unsafe eliminated** — `sendmsg`/`recvmsg` now use `impl AsFd` via rustix, no `borrow_raw` remains
- **VfioDevice**: `container_as_fd()`, `group_as_fd()`, `device_as_fd()` return `BorrowedFd<'_>` from stored `OwnedFd`/`File`
- **Stale docs**: `nv/ioctl/mod.rs` comment about "inline assembly" corrected to "rustix::ioctl"
- **Remaining unsafe**: All in coral-driver, all with SAFETY comments, all at irreducible kernel ABI boundaries (ioctl, mmap, volatile MMIO, page-aligned alloc, mlock)

### 2. Clone Audit

- **shader_model.rs**: `literal_materialization_overhead` refactored to take `&[&Src]` — **29 `.clone()` calls eliminated** (was allocating Src structs just for read-only size estimation)
- **DeviceSlot.bdf**: `String` → `Arc<str>` — ~35 per-log/per-error heap allocations in activate.rs, swap.rs, health.rs collapsed to cheap Arc refcount bumps
- **DeviceError**: All `bdf: String` fields → `Arc<str>`

### 3. Coverage Expansion (+83 tests, 2560 → 2643)

- **coral-driver**: Pure-logic tests for `NvVoltaIdentity::from_boot0` (table-driven across GPU generations), `diff_snapshots`/`diff_bar_maps` (bar cartography), `GrEngineStatus` (bitmask/Display), `build_dispatch_hints` (synthetic firmware-free knowledge via `insert_for_test`)
- **coralreef-core/main.rs**: CLI parsing (all subcommands + error cases), cmd_compile (tempfile WGSL), exit code conversions, discovery dir
- **nak-ir-proc**: 12 runtime integration tests (SrcsAsSlice, DstsAsSlice, DisplayOp, FromVariants, Encode) + 6 compile-fail trybuild cases
- **Cross-primal e2e**: Binary spawn + JSON-RPC `shader.compile.wgsl` + tarpc integration with discovery file coordination and clean SIGTERM shutdown

### 4. Smart Refactoring (Iter 57, carried forward)

- `device.rs` (1375 lines) → `device/` module: `mod.rs`, `types.rs`, `activate.rs`, `swap.rs`, `health.rs`, `tests.rs`
- `socket_tests.rs` (1007 lines) → `socket_tests/` directory: `mod.rs`, `parse_tests.rs`, `dispatch_tests.rs`, `tcp_tests.rs`, `chaos_tests.rs`, `fault_tests.rs`
- All submodules under 1000 lines, `pub(super)` for internal visibility

### 5. libc → rustix Completion (Iter 57, carried forward)

- `coral-glowplug` and `coral-ember`: `libc::sendmsg`/`recvmsg` → `rustix::net::sendmsg`/`recvmsg` with `ScmRights`
- `libc` removed from both Cargo.toml files, replaced with `rustix = { version = "1.1.4", features = ["net"] }`

### 6. CI Compliance

- `cargo fmt --all -- --check`: PASS
- `cargo clippy --workspace --all-features --all-targets -- -D warnings`: PASS (0 warnings)
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps`: PASS
- `cargo test --workspace --all-features`: 2680+ passed, 0 failed
- `cargo llvm-cov`: 60.16% line / 69.03% function / 60.62% region
- All `.rs` files under 1000 lines
- All 476 `.rs` files have `SPDX-License-Identifier: AGPL-3.0-only`
- `.cursor/rules/` created with `coralreef-standards.mdc` and `rust-patterns.mdc`

---

### 7. Audit Hardening (Mar 20 continuation)

- `#[forbid(unsafe_code)]` hardened on coral-ember + coral-glowplug (upgraded from `#[deny]`)
- `libc` eliminated from direct dev-deps: `ember_client.rs` SCM_RIGHTS migrated to `rustix::net`
- Hardcoded socket paths evolved: `EMBER_SOCKET` → `ember_socket_path()` with `$CORALREEF_EMBER_SOCKET` env override
- Stale placeholder comments fixed: AMD GPU arch "placeholder" → "RDNA2/3/4 backend", Intel → "planned — register addresses TBD"
- 14 `#[allow]` → `#[expect]` across 8 files (vendor_lifecycle, ember.rs, types.rs, page_tables.rs, support.rs, activate.rs, main.rs) — stale suppressions now warn at compile time
- 5 tarpc Unix socket roundtrip tests: status, health_check, capabilities, wgsl compile, liveness+readiness (coverage 80.84% → 94.88%)
- 9 vendor_lifecycle tests: description(), settle_secs(), rebind_strategy() for all 6 vendor types
- 11 IPC Unix error path tests: dispatch errors, blank lines, malformed JSON, invalid JSON-RPC version
- Unused `SendAncillaryBuffer` import removed from `ember_client.rs`
- Stale `.analysis-command-output.txt` and `.analysis-rg-output.txt` debris files removed
- All root docs updated with current metrics (README, CHANGELOG, WHATS_NEXT, STATUS, EVOLUTION, CONTRIBUTING, START_HERE, specs)

---

## Metrics

| Metric | Before (Iter 57) | After (Iter 58) |
|--------|-------------------|------------------|
| Tests passing | 2560 | 2680+ |
| Line coverage | 59.98% | 60.16% |
| Region coverage | 60.44% | 60.62% |
| Function coverage | 68.73% | 69.03% |
| tarpc transport coverage | 80.84% | 94.88% |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Fmt drift | 0 | 0 |
| Unsafe in ember.rs/ipc.rs | ~4 blocks | 0 |
| shader_model.rs clones | 29 | 0 |
| DeviceSlot.bdf allocs/clone | String (heap) | Arc\<str\> (refcount) |
| BorrowedFd::borrow_raw sites | ~6 | 0 (all via AsFd) |
| `#[allow]` → `#[expect]` | 0 | 14 tightened |
| `#[forbid(unsafe_code)]` crates | 1 (glowplug) | 2 (ember + glowplug) |
| libc direct deps | 1 (dev-dep) | 0 |
| SPDX .rs files | 455 | 476 |

---

## Cross-Primal Impact

- **hotSpring**: VfioDevice API changed — `container_shared()` returns `Arc<OwnedFd>` (was `RawFd`). Update VFIO channel consumers if accessing container fd directly. `container_as_fd()` / `group_as_fd()` / `device_as_fd()` available for safe borrowing.
- **toadStool**: No API impact — JSON-RPC unchanged, capabilities unchanged
- **barraCuda**: No impact — compiler APIs unchanged, shader_model performance improved (fewer allocations)

---

## Next Steps (Iteration 59+)

1. **Coverage 60% → 90%**: Continue test expansion on low-coverage modules (GSP dispatch with synthetic knowledge, VFIO channel logic, codegen optimizer passes, main.rs binary entry point)
2. **GP_PUT hardware validation**: Test cache flush on live Titan V VFIO (hotSpring Exp 070)
3. **UVM hardware validation**: RTX 5060 compute dispatch
4. **Clone audit phase 2**: IR `Src`/`SSARef` clone reduction via helper functions in lower_f64 (newton/trig/exp2/log2)
5. **AMD MI50 hardware swap**: Validate GFX906 metal register offsets
