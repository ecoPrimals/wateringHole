# SQUIRREL v1.7.0 — Comprehensive Audit & Deep Debt Resolution

**Date**: March 14, 2026
**Version**: 1.7.0
**Previous**: V1.6.x (Pre-audit baseline)
**Status**: PRODUCTION READY

---

## Summary

Comprehensive audit and deep debt resolution across three priority tiers:

1. **P0 — Critical** — Build fixes, clippy pedantic+nursery, license migration to AGPL-3.0-only, SPDX headers, gRPC/tonic removal, MCP evolution to JSON-RPC
2. **P1 — Important** — forbid(unsafe_code), sqlx rustls, 1000-line refactors, flaky test fix, coverage 60%→70%
3. **P2 — Significant** — tarpc handler completion, capability-based discovery, unwrap/expect audit, clone reduction, mock isolation

---

## Status

| Metric | Value |
|--------|-------|
| Build | GREEN |
| Tests | 3,969 passing, 0 failed |
| Coverage | ~70% (target: 90%) |
| Clippy | CLEAN (pedantic + nursery) |
| License | AGPL-3.0-only (all crates) |

---

## Changes

### P0 — Critical

| Change | Details |
|--------|---------|
| cargo fmt | Fixed invalid inner attribute in security lib.rs |
| Clippy | Fixed all pedantic + nursery warnings |
| License | Changed 4 MIT-licensed crates to AGPL-3.0-only |
| SPDX headers | Added to all 1,284 .rs files |
| gRPC removal | Removed gRPC/tonic/prost from workspace (evolved to JSON-RPC) |
| MCP evolution | Evolved MCP sync/task from tonic to JSON-RPC over Unix sockets |

### P1 — Important

| Change | Details |
|--------|---------|
| unsafe_code | Changed deny(unsafe_code) to forbid(unsafe_code) in 28 crates |
| sqlx TLS | Switched sqlx native-tls to rustls (ecoBin compliance) |
| 1000-line limit | Refactored 5 files exceeding 1000-line limit |
| Flaky test | Fixed flaky socket env var test with temp-env |
| Coverage | Pushed test coverage 60% → 70% |

### P2 — Significant

| Change | Details |
|--------|---------|
| tarpc handler | Completed tarpc handler (bincode + bytes::Bytes zero-copy) |
| Capability discovery | Evolved 150+ hardcoded primal names to capability-based discovery |
| unwrap/expect | Audited unwrap()/expect() in production code |
| #[allow] cleanup | Cleaned suppressions and dead code |
| Mock isolation | Isolated mocks to test-only |
| Deprecated APIs | Migrated deprecated APIs to capability-based equivalents |
| Clone reduction | Deep clone reduction (ArcStr, Copy on enums, reference parameters) |

---

## For Other Primals

### For biomeOS

- Squirrel now registers **capabilities** not primal names — use `capability.discover`
- gRPC/tonic removed — connect via JSON-RPC over Unix socket or tarpc

### For petalTongue

- `interaction.subscribe` events ready for AI adaptation

### For ToadStool

- `compute.discover_capabilities` consumption ready via capability discovery

### For BearDog

- Security integration via `SECURITY_CAPABILITY` constant, not `"beardog"` string

### For Songbird

- Service mesh integration via `SERVICE_MESH_CAPABILITY` constant

---

## Remaining Work

- **Coverage**: 70% → 90% (network-dependent modules need mock socket infrastructure)
- **grpc_port config field** still present (needs removal + constant migration)
- **SongbirdClient** deprecated wrapper still exists for backward compatibility

---

## Standards Compliance

| Standard | Status |
|----------|--------|
| uniBin | PASS |
| ecoBin | PASS (pure Rust, rustls, zero C deps) |
| JSON-RPC 2.0 | PASS (primary IPC) |
| tarpc | PASS (secondary binary IPC) |
| Semantic naming | PASS (domain.operation) |
| Zero-copy | PARTIAL (bytes::Bytes, ArcStr, Cow) |
| forbid(unsafe_code) | PASS (all crates) |
| AGPL-3.0-only | PASS (all crates + SPDX headers) |
| <1000 lines | PASS (all files) |
| Lysogeny | PASS (no TODO/FIXME in source) |

---

## Next Steps

1. **Coverage to 90%** — mock socket infrastructure for network-dependent modules
2. **grpc_port removal** — remove config field and migrate to constants
3. **SongbirdClient** — remove deprecated wrapper once consumers migrate to capability discovery
