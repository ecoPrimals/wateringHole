<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Semantic RPC, Coverage Expansion, CI Hardening

**Date**: March 15, 2026 (session 9)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Standards compliance + coverage expansion + CI hardening + debt resolution
**Supersedes**: `RHIZOCRYPT_V013_VERTEX_INDEX_CHECKOUT_ZEROCOPY_DID_HANDOFF_MAR15_2026.md`

---

## Summary

Comprehensive audit and execution pass against wateringHole standards. Renamed all
JSON-RPC methods to Spring-as-Niche semantic naming. Added `capability.list`
endpoint for runtime service discovery. Expanded test coverage from 907 to 1177
tests (91.47% line coverage). Hardened CI with `cargo-deny` job and `--all-features`
on doc/coverage gates. Fixed env var race condition in integration tests. Updated
all root documentation and deployment checklist to reflect current state.

---

## Changes

### Semantic JSON-RPC Method Naming (Spring-as-Niche Standard)

| Before | After |
|--------|-------|
| `dag.dehydrate` | `dag.dehydration.trigger` |
| `system.health` | `health.check` |
| `system.metrics` | `health.metrics` |
| — | `capability.list` (new) |

Updated across: handler dispatch, handler tests, integration tests, JSON-RPC types
tests, tarpc service trait, RPC client, metrics enum. Showcase scripts already used
semantic names — no changes needed.

### capability.list Endpoint

| Aspect | Detail |
|--------|--------|
| Struct | `CapabilityDescriptor { domain, methods, version }` |
| tarpc | New trait method `list_capabilities() -> Vec<CapabilityDescriptor>` |
| JSON-RPC | `capability.list` dispatches to tarpc impl |
| Client | `RpcClient::list_capabilities()` wrapper |
| Metrics | `RpcMethod::ListCapabilities` variant (count now 23) |

### Coverage Expansion (91.47% line coverage, 1177 tests)

| Target | Before | After | Tests Added |
|--------|--------|-------|-------------|
| `store_redb.rs` | 68% | 90%+ | 25 |
| `store_sled.rs` | 79% | 90%+ | 25 |
| `songbird/client.rs` | 75% | 90%+ | 16 |
| `doctor.rs` | 81% | 90%+ | 16 |
| `rhizocrypt-service/lib.rs` | 81% | 90%+ | 18 |
| **Total** | 907 | 1177 | 270 |

### Zero-Copy Evolution

- `vertex.rs::to_canonical_bytes()` → `bytes::Bytes` return type
- `signing.rs` and store backends consume `Bytes` directly (no intermediate `Vec<u8>`)

### CI Pipeline Hardening

- Added `cargo-deny` check job to `.github/workflows/ci.yml`
- Added `--all-features` to `cargo doc` and `cargo llvm-cov` CI steps
- All dependency advisories, license, and ban checks pass

### Dependency Audit

- Added `AGPL-3.0-only` to `deny.toml` allow list for `provenance-trio-types`
- Removed stale `ring` skip entry
- 5 tarpc transitive advisories — upstream, no action available

### Test Isolation Fix

- Added `clear_bind_addr_env()` helper in `service_integration.rs`
- All `resolve_bind_addr_*` tests now sanitize env state before and after
- Eliminated race condition where async tests leaked env vars into sync tests

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps -D warnings` | Clean |
| `cargo test --workspace --all-features` | 1177 pass, 0 fail |
| `cargo deny check` | Clean |
| `#![forbid(unsafe_code)]` | Workspace-wide |
| SPDX headers | All 106 `.rs` files |
| Max file size | All under 1000 lines |
| Production unwrap/expect | Zero |
| Production TODO/FIXME/HACK | Zero |

---

## Files Modified (rhizoCrypt)

```
crates/rhizo-crypt-rpc/src/jsonrpc/handler.rs       # semantic method dispatch
crates/rhizo-crypt-rpc/src/jsonrpc/handler_tests.rs  # updated method names + capability.list test
crates/rhizo-crypt-rpc/src/jsonrpc/mod.rs            # integration test method names
crates/rhizo-crypt-rpc/src/jsonrpc/types.rs          # type test method name
crates/rhizo-crypt-rpc/src/service.rs                # CapabilityDescriptor, list_capabilities
crates/rhizo-crypt-rpc/src/client.rs                 # list_capabilities client method
crates/rhizo-crypt-rpc/src/lib.rs                    # re-export CapabilityDescriptor
crates/rhizo-crypt-rpc/src/metrics.rs                # ListCapabilities variant
crates/rhizo-crypt-core/src/vertex.rs                # to_canonical_bytes → Bytes
crates/rhizo-crypt-core/src/clients/capabilities/signing.rs  # Bytes consumer
crates/rhizo-crypt-core/src/store_redb.rs            # Bytes slicing
crates/rhizo-crypt-core/src/store_sled.rs            # Bytes slicing
crates/rhizo-crypt-core/src/store_redb_tests_advanced.rs  # 25 new tests
crates/rhizo-crypt-core/src/store_sled_tests_advanced.rs  # 25 new tests
crates/rhizo-crypt-core/src/clients/songbird/tests.rs     # 16 new tests
crates/rhizocrypt-service/src/doctor.rs              # coverage target
crates/rhizocrypt-service/tests/service_integration.rs     # 18 new tests + race fix
.github/workflows/ci.yml                             # cargo-deny job, --all-features
deny.toml                                            # AGPL-3.0-only allow, ring skip removed
docs/DEPLOYMENT_CHECKLIST.md                         # semantic method names, updated metrics
README.md                                            # 1177 tests, 91.47% coverage, 106 files
CHANGELOG.md                                         # session 9 entry
```

## Files Modified (wateringHole)

```
handoffs/RHIZOCRYPT_V013_SEMANTIC_RPC_COVERAGE_EXPANSION_HANDOFF_MAR15_2026.md  # this
handoffs/archive/RHIZOCRYPT_V013_VERTEX_INDEX_CHECKOUT_ZEROCOPY_DID_HANDOFF_MAR15_2026.md  # archived
```

---

## Remaining Debt (documented, not urgent)

1. `collect_attestations` returns empty `Vec` — needs BearDog signing integration
2. 5 tarpc transitive advisories in cargo-deny — waiting on upstream
3. `SmallVec` evaluation for store key allocation — performance candidate
4. LMDB storage backend — `StorageBackend::Lmdb` returns startup error; redb and sled cover needs
5. sled → redb migration path — sled introduces libc; redb is pure Rust default

---

## Items Resolved from Previous Handoff

| Previous "Next Step" | Resolution |
|---------------------|------------|
| JSON-RPC method names need semantic alignment | Renamed: `dag.dehydrate` → `dag.dehydration.trigger`, `system.*` → `health.*` |
| Missing `capability.list` endpoint | Implemented with `CapabilityDescriptor` struct |
| Coverage gaps in store, client, service modules | 270 tests added, 91.47% coverage |
| CI missing `cargo-deny` | Added as dedicated CI job |
| Deployment docs reference old method names | Updated `DEPLOYMENT_CHECKLIST.md` |
