# ToadStool S200 Handoff — Deep Debt Modernization & Audit

**Date**: April 11, 2026
**Session**: S200
**Author**: westgate
**Status**: Complete

---

## Summary

S200 executed a comprehensive deep debt audit across all dimensions (unsafe, hardcoding, mocks, unwraps, deps, file size) and performed targeted modernization. The codebase was confirmed to be in strong shape with all prior debt resolutions holding.

---

## Changes

### Deep Debt Audit Results (All Clean)

| Dimension | Finding |
|-----------|---------|
| Production `.unwrap()` | **Zero** — every `.unwrap()` call is inside `#[cfg(test)]` or `#[test]` |
| Production mocks | **Zero** — all `MockProvider`, `MockPrimal`, `InMemoryAuthBackend` behind `#[cfg(test)]` or `#[cfg(any(test, feature = "test-mocks"))]` |
| Hardcoded primal names | **Zero** in production — all in `#[cfg(test)]` or centralized `interned_strings` constants |
| Hardcoded IPs/ports | All self-configuration constants (`BIND_ADDRESS_DEFAULT`, `LOCALHOST`) or test data; `defaults/network.rs` uses port 0 everywhere |
| Unsafe code | ~66 blocks, all in hardware containment (hw-safe, nvpmu, akida-driver, display) with SAFETY comments |
| TODO/FIXME/HACK/XXX | **Zero** in production code |
| Production `#[expect(clippy::expect_used)]` | 3, all justified (compile-time constant parse, catastrophic thread pool failure, assertion-guarded NonNull) |

### Service Discovery Refactoring

- Extracted `localhost_capability_fallback`, `services_from_eco_primals_runtime_sockets`, `biomeos_category` from `service_discovery/service.rs` into new `fallback.rs` module
- `service.rs` reduced from 755 → 552 lines (cache-based discovery only)
- `fallback.rs`: 186 lines, cleanly owns all fallback resolution
- New `DiscoveredService::discovered_now()` constructor + `.with_metadata()` builder — eliminates ~120 lines of repetitive construction boilerplate

### Dependency Evolution

- `toadstool-cli` dev-dep: rustix 0.38 → 1.1 (Signal API migration: `Int` → `INT`, `Term` → `TERM`)
- `toadstool-display` documented as pending V4L2 ioctl API migration (0.38 → 1.x `Ioctl` trait pattern)
- All other workspace crates already on rustix 1.x

### Documentation Updates

- `DOCUMENTATION.md` updated to S200 with ~69 methods, pipeline dispatch, deep audit results
- `DEBT.md` updated with `D-RUSTIX-DISPLAY-038`, `D-ASYNC-DYN-MARKERS`, and S200 resolved items
- `CHANGELOG.md` S200 entry with full change log
- `NEXT_STEPS.md` status line updated

### Debris Cleanup

- `contrib/mesa-nak/` (NAK deficiency docs + instruction latency tables) archived to `wateringHole/fossilRecord/toadstool-contrib-mesa-nak-S200/`
- `cargo clean` removed 221.8 GiB / 1.7M files of build artifacts

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --check` | PASS (0 violations) |
| `cargo clippy --workspace --all-targets --all-features` | PASS (0 warnings) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | PASS |
| `cargo test --workspace` | PASS (0 failures) |

---

## Remaining Known Debt

| Item | Status | Notes |
|------|--------|-------|
| `D-RUSTIX-DISPLAY-038` | Open | V4L2 ioctl wrappers need migration from `Getter`/`Updater`/`Setter` to `Ioctl` trait pattern |
| `D-ASYNC-DYN-MARKERS` | Blocked | ~55 `NOTE(async-dyn)` markers — awaiting Rust `dyn Trait` + native async fn stabilization |
| `D-COVERAGE-GAP` | Ongoing | 83.6% → 90% target |
| `D-EMBEDDED-PROGRAMMER` | Partial | Placeholder impls with typed errors; awaiting hardware transport layers |
| `D-FUZZ-TARGETS` | Partial | Infrastructure added; needs CI integration, seed corpus, extended campaigns |

---

## For Other Primal Teams

- **barraCuda / coralReef**: NAK deficiency analysis and instruction latency tables archived to `wateringHole/fossilRecord/toadstool-contrib-mesa-nak-S200/`
- **All springs**: Pipeline dispatch API (`compute.dispatch.pipeline.submit`) from S199 is stable — use for multi-stage ordered workloads
- **primalSpring**: All upstream gaps from cross-spring synthesis (PG-05, neuralSpring pipeline) confirmed resolved
