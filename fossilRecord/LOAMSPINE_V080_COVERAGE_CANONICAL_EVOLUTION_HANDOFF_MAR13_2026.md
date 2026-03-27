<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# LoamSpine v0.8.0 — Coverage & Canonical Evolution Handoff

**Date**: March 13, 2026
**Primal**: LoamSpine (permanence layer)
**Version**: 0.8.0
**Type**: Coverage target achieved, canonical serialization evolution, file size compliance

---

## Summary

Second deep debt pass on LoamSpine achieving the 90%+ coverage target (90.62%, 700 tests). Fixed a latent canonical serialization non-determinism bug by evolving `Entry.metadata` from `HashMap` to `BTreeMap`. Refactored `tarpc_server.rs` to comply with 1000-line file limit. All quality gates green.

---

## What Changed

### Coverage Target Achieved: 90.62%

| Area | Tests Added | Coverage Gain |
|------|-------------|---------------|
| lifecycle.rs | 17 | 75% → 83% (heartbeat, shutdown, deregister paths) |
| spine.rs | 7 | 85% → 93% (chain validation, seal, state transitions) |
| entry.rs | 11 | 86% → 99% (all EntryType domains, canonical bytes, serde) |
| tarpc_server.rs | 13 | 89% → 95% (error paths, success paths, server bind) |
| integration_ops.rs | 13 | 85% → 92% (invalid inputs, commit/verify/get) |
| backup/mod.rs | 4 | 87% → 89% (roundtrip, corrupt data, truncated input) |

New test infrastructure:
- `SuccessTransport` in `transport/mock.rs` for testing deregister/heartbeat success paths
- `DiscoveryClient::for_testing_success()` for lifecycle success path coverage
- `LifecycleManager::start_heartbeat_for_testing()` for heartbeat task injection

### Canonical Serialization Bug Fix

`Entry.metadata` evolved from `HashMap<String, String>` to `BTreeMap<String, String>`:

- **Bug**: `to_canonical_bytes()` drained `HashMap` into `BTreeMap` for sorting, then collected back into `HashMap` — losing the sort. Identical entries with different metadata insertion order produced different canonical bytes.
- **Fix**: `BTreeMap` maintains sorted key order inherently. `to_canonical_bytes()` now serializes directly — no clone/sort/collect dance needed.
- **Impact**: All downstream consumers (hash computation, proof generation, backup verification) get deterministic serialization for free.

### File Size Compliance

`tarpc_server.rs` refactored from 1060 lines to 240 lines:
- Production code stays in `tarpc_server.rs` (240 lines)
- Tests extracted to `tarpc_server_tests.rs` (810 lines) via `#[path]` attribute
- All source files now under 1000-line limit (max: 949 lines in `entry.rs`)

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 635 | 700 (+65) |
| Line coverage | 88.64% | 90.62% (+1.98%) |
| Max file size | 1060 | 949 (all < 1000) |
| Source files | 78 | 80 |
| Clippy warnings | 0 | 0 |
| Unsafe code | 0 | 0 |
| C dependencies | 0 | 0 |

---

## Inter-Primal Notes

### All Primals
- `Entry.metadata` is now `BTreeMap<String, String>` — any primal deserializing LoamSpine entries should use `BTreeMap` for compatibility. Serialization format is unchanged (bincode/serde handles both transparently).
- No API changes. All JSON-RPC methods, tarpc methods, and wire formats are stable.

### rhizoCrypt
- `permanent-storage.commitSession` pathway unchanged and tested with new integration ops coverage.
- Verify/get paths now have explicit error coverage for invalid hex and missing IDs.

### sweetGrass
- `braid.commit` pathway stable. No changes to trio type bridge.

### biomeOS
- NeuralAPI registration/deregistration tested via mock transports (success + failure paths).
- Heartbeat retry logic now has dedicated coverage.

---

## Quality Gates

```
cargo fmt --all -- --check           ✅ clean
cargo clippy -D warnings             ✅ 0 warnings (all targets, all features)
cargo test --workspace               ✅ 700 passed, 0 failed
cargo doc --workspace --no-deps      ✅ compiles
cargo deny check                     ✅ licenses, bans, sources pass
cargo llvm-cov --workspace           ✅ 90.62% line coverage
```

---

## Remaining Uncovered Areas

| File | Coverage | Reason |
|------|----------|--------|
| `main.rs` | 0% | Binary entry point; tested via integration demos |
| `neural_api.rs` | 52% | Requires live NeuralAPI socket |
| `jsonrpc/mod.rs` | 68% | Macro-generated trait implementations |
| `infant_discovery.rs` | 81% | DNS SRV and mDNS require network |

These are structural coverage limits — async socket code and macro-generated implementations are not meaningfully testable without live external services.

---

**Handoff by**: LoamSpine coverage & canonical evolution session
