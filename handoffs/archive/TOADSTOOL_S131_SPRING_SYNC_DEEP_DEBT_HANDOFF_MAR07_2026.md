<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# toadStool S131+ — Spring Sync + Deep Debt Evolution Handoff

**Date**: March 7, 2026
**From**: toadStool S131+
**To**: All springs, barraCuda, coralReef
**License**: AGPL-3.0-or-later
**Tests**: 19,777 (0 failures, 216 ignored hw)
**Coverage**: ~85% line (121K production lines)
**Clippy**: Pedantic zero, `#[expect]` evolution complete

---

## Executive Summary

toadStool S131+ completes a full spring sync and deep debt evolution cycle:

1. **Spring pin update**: All 5 springs pinned to latest versions with comprehensive absorption tracker update
2. **`#[allow]` → `#[expect]` evolution**: Modern idiomatic Rust lint suppressions. 3 stale suppressions discovered and removed.
3. **Deep debt scan**: Confirmed clean — all files <1000L, all unsafe=hardware FFI, no production hardcoding, mocks test-isolated, C deps optional
4. **IPC resolution**: `science.*` namespace confirmed canonical via toadStool proxy; springs may also call barraCuda directly
5. **Absorption confirmed**: `SubstrateCapabilityKind::Fft` already present, `shader.compile.*` already wired to live coralReef

---

## 1. Spring Pin Status

| Spring | Previous | Current | Tests | Key Evolution |
|--------|----------|---------|-------|---------------|
| hotSpring | v0.6.19→S130+ | v0.6.19→S131+ | 724+19 | DF64 delegation complete, Chuna papers |
| groundSpring | V95→S130+ | V96→S131+ | 925+390 | PrecisionRoutingAdvice 11 GPU paths |
| neuralSpring | V87/S129→S130+ | V89/S131→S131+ | 901+43+240 | 89.1% coverage, isomorphic 25/25 |
| wetSpring | V97d+→S130+ | V97e→S131+ | 1,346+200 | Builder patterns, provenance API |
| airSpring | V071→S130+ | V0.7.3→S131+ | 848+186 | Write→Absorb→Lean complete, zero local WGSL |

---

## 2. `#[expect]` Lint Evolution

Evolved production `#[allow(lint)]` to `#[expect(lint, reason = "...")]` following neuralSpring's pattern. The `#[expect]` attribute warns when the lint no longer fires, preventing stale suppressions.

### Stale Suppressions Discovered and Removed

| File | Stale Lint | Why Stale |
|------|-----------|-----------|
| `encryption/types.rs` | `clippy::cast_sign_loss` | `u64 as i64` is not sign loss in this direction |
| `byob/network_manager.rs` | `clippy::cast_possible_truncation` | `char as u32` is lossless (char fits in u32) |
| `auto_config/hardware/mod.rs` | `dead_code` | Field actually used in test code |

### Pattern Note

`dead_code` on struct fields cannot use `#[expect]` because the lint fires in `cargo check` (lib profile) but not in `cargo test` (lib test profile). These retain `#[allow(dead_code, reason = "...")]`.

### Successfully Evolved

| Lint | Count | Files |
|------|-------|-------|
| `clippy::unused_async` | 5 | handler/mod.rs, science.rs, capabilities.rs, resource_leak.rs, resources.rs |
| `clippy::unused_self` | 3 | native/lib.rs (×2), substrate.rs |
| `clippy::cast_precision_loss` | 7 | composition_engine.rs (×5), capabilities.rs, input/parser.rs (×2) |
| `clippy::cast_possible_truncation` | 3 | dispatch.rs (×2), discovery_integration.rs |
| `deprecated` | 3 | lifecycle_ops.rs, cli/lib.rs, ecosystem.rs |

---

## 3. Deep Debt Scan Results

| Category | Finding |
|----------|---------|
| Files >1000L | **0** (max 979 in tests) |
| Unsafe code | **15 files**, all hardware FFI (V4L2, VFIO, mmap, GPU backends, secure enclave) |
| Production hardcoding | **0** (all via constants; test fixtures use literals) |
| Mocks in production | **0** (all behind `#[cfg(test)]` or `test-mocks` feature) |
| External C deps | **Optional only** (core-foundation-sys macOS, esp-idf-sys edge boards) |
| Production `unwrap()` | **0** (infallible `expect()` only) |
| Production `todo!()` | **0** |
| Production `FIXME/HACK` | **0** |

---

## 4. For Other Primals

### For barraCuda team

- No API changes from toadStool side
- Fp64Strategy fused GPU regression tracked as ecosystem P0 (VarianceF64/CorrelationF64 return 0.0)
- `From<BarracudaError>` for `BarracudaCoreError` noted; toadStool can use for cleaner error chains

### For coralReef team

- coralReef E2E AMD dispatch milestone noted in toadStool's absorption tracker
- `shader.compile.*` proxy already routes to live coralReef when available
- NVIDIA E2E is next tracked milestone

### For all springs

- toadStool's `science.*` JSON-RPC namespace is the canonical proxy for science compute
- Springs may also call barraCuda directly for GPU dispatch (confirmed with wetSpring V97e)
- `SubstrateCapabilityKind::Fft` exists since S96 (groundSpring V96 request fulfilled)
- `#[expect(lint, reason)]` pattern adopted; recommend all springs evolve similarly

---

## Verification

```bash
cd toadStool
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic
cargo doc --workspace --no-deps
cargo test --workspace
```

All pass as of S131+ HEAD.
