# Songbird v0.2.1-wave41 Deep Debt S+ Tier Handoff

**Date**: March 21, 2026  
**Primal**: Songbird (Network Orchestration & Discovery)  
**Status**: Deep Debt S+ Tier — all 15 audit principles at S+ rating  
**Edition**: Rust 2024

---

## Session Summary

Full compliance audit executed across the Songbird workspace. All audit findings addressed in Waves 28–41, covering license compliance, dependency alignment, lint hygiene, production stub evolution, smart file refactoring, clone elimination, test expansion, and documentation.

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 9,983 passed, 0 failed, 271 ignored (16 threads, fully concurrent) |
| Clippy | Zero warnings (`clippy::pedantic + nursery + cargo`, `--all-targets --all-features`) |
| Build | Zero errors, zero warnings |
| Formatting | Clean (`cargo fmt --check`) |
| Docs | Clean (`cargo doc --all-features --no-deps`) |
| Files >1000 lines | 0 |
| Unsafe blocks | 2 (in `songbird-process-env`, Mutex-guarded, SAFETY-documented) |
| Production `.unwrap()` | 0 |
| Production `todo!()` / `panic!()` | 0 |
| TODO/FIXME/HACK in source | 0 |
| License | `AGPL-3.0-only` via workspace inheritance (all 29 crates) |
| SPDX headers | 100% of `.rs` files |
| `ring` dependency | Opt-in only (`ring-crypto` feature, not default in any crate) |
| Total Rust | ~401,000 lines across 29 crates |

---

## What Was Done

### License & Dependencies
- 22 crates migrated to `license.workspace = true` (AGPL-3.0-only)
- Duplicate dependency versions aligned: thiserror→2.0, base32→0.5, base64→0.22, hostname→0.4
- `ring-crypto` set to non-default in `songbird-quic`

### Lint Hygiene
- 5,325 unfulfilled `#[expect()]` migrated to `#[allow(reason)]` across 299 test files
- 66 Clippy warnings fixed in test code
- Zero warnings workspace-wide

### Production Stub Evolution
- Metrics: concrete `ComputeMetrics` + `AtomicU64` counters with real snapshotting
- AI workload classification: typed `WorkloadType`, `BatchPriority`, `ResourceRequirements`
- Lineage relay: `Arc<Mutex<u64>>` → `Arc<AtomicU64>` (lockless)
- Deprecated `start_http_server` stub removed

### Smart File Refactoring
- 5 files over 1000 lines refactored into domain-aligned submodules
- `constants.rs` (1,199 lines) → `constants/` with `directories.rs` + `primal_discovery.rs`
- `jsonrpc_api.rs` → 8 handler modules
- `client.rs` → 3 modules
- `capability_discovery.rs` → 4 modules
- Test extractions for `validator.rs`, `service.rs`, `canonical.rs`

### Zero-Copy / Clone Elimination
- 19 unnecessary `.clone()` calls eliminated in hot-path production files

### Test Expansion (+253 tests)
- 84 new tests across `songbird-universal-ipc`, `songbird-discovery`, `songbird-types`
- SSDP discovery module wired
- 81 `pub mod` declarations documented

---

## Pending Work (Priority Order)

1. **BearDog crypto wiring** — AES-128-CTR, running digest, HMAC-SHA256, ntor handshake via BearDog
2. **Coverage expansion** — Target pure-logic modules first (goal: 90%, current: ~68%)
3. **Ring-free workspace** — `rcgen` replacement + quinn feature reconfiguration
4. **Deep documentation** — Fill internal `#[allow(missing_docs)]` modules
5. **Real hardware tests** — Tower + Pixel cross-network validation
6. **Platform backends** — Mobile pairing, iOS, WASM
7. **Dependency pruning** — Reduce ~418 unique deps where possible

---

## Capability Discovery Status

All Songbird discovery paths use capability-based resolution:
- Environment → XDG → smart defaults
- `find_primals_with_capability` — real env-driven capability filter
- Zero hardcoded primal names, ports, or URLs in production code
- BearDog delegation: explicit `CryptoUnavailable` when BearDog not available

---

## Inter-Primal Dependencies

| Dependency | Protocol | Status |
|-----------|----------|--------|
| BearDog | JSON-RPC IPC (Unix socket / TCP fallback) | Capability discovery at runtime |
| Other primals | Discovered by capability, never by name | Self-knowledge only |

---

## Build & Run

```bash
cargo build --workspace --release
cargo run --bin songbird -- server
cargo run --bin songbird -- cli
cargo test --workspace --all-features
cargo llvm-cov --workspace --html
```
