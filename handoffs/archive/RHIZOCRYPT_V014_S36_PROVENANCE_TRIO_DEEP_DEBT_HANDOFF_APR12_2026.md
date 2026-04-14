# rhizoCrypt v0.14.0-dev — Session 36: Provenance Trio Debt + Deep Debt Cleanup

**Date:** 2026-04-12
**Primal:** rhizoCrypt
**Context:** primalSpring downstream audit — Provenance Trio (rhizoCrypt + loamSpine + sweetGrass)

---

## Summary

Closed the low-priority provenance trio debt identified by primalSpring, then
executed a full deep debt sweep resolving all pre-existing clippy blockers,
hardcoded constants, non-idiomatic patterns, and stale lint suppressions
across the workspace. SPDX coverage now 100% (148/148 .rs files).

## Changes

### Provenance Trio Debt (from primalSpring audit)

- **`notify_provenance` completed** — Stub in `provenance/client.rs` now sends
  a full `contribution.record_provenance` JSON-RPC call with vertex references,
  agent count, and source primal. Non-fatal on failure (graceful degradation per
  `SPRING_PROVENANCE_PATTERN.md` Section 7).
- **`TCP_NODELAY` + `flush` hardened** — `send_jsonrpc` in `provenance/client.rs`
  now sets `TCP_NODELAY` after connect and flushes after write, matching the
  hardening already present in `jsonrpc/mod.rs` and `btsp/framing.rs`. Addresses
  the loamSpine "connection closes after first response" workaround.
- **Witness chain round-trip e2e test** — 6 new tests in
  `tests/e2e/witness_roundtrip.rs` validating the store → witness mapping → wire
  format → deserialize chain without live trio peers (low urgency scope).
- **Operation dependencies drift guard** — New test
  `all_capabilities_have_dependency_entries` in `niche_tests.rs` asserts
  bidirectional consistency between `CAPABILITIES` and `operation_dependencies()`.

### Deep Debt Cleanup

- **Clippy blockers resolved (3 pre-existing):**
  - `dag_benchmarks.rs` — Refactored monolithic 170-line `bench_dag_store` into
    three focused functions under 100-line clippy limit; fixed 5 `unused-must-use`.
  - `service_types.rs` — `sort()` → `sort_unstable()` (primitive optimization).
  - `songbird/config.rs` — Removed unfulfilled `#[expect(clippy::unwrap_used)]`.
- **Hardcoded scheme evolved** — `format!("http://...")` in discovery registration
  → `constants::DISCOVERY_ENDPOINT_SCHEME` (wateringHole transport convention).
- **Zero-copy evolution** — `read_family_seed` return type: `Vec<u8>` → `Bytes`
  (O(1) clone when shared across UDS connections).
- **Test harness evolved** — `Box<dyn Error>` → `Result<(), PrimalError>`;
  hardcoded port 19400 → OS-assigned (port 0).
- **SPDX compliance** — Added headers to 6 missing test files (148/148 now).
- **Doc backtick fix** — `TCP_NODELAY` in `rpc_integration.rs` doc comment.

### Docs Updated

- **README.md** — Tests: 1,502 → 1,510; SPDX: 147 → 148; showcase: 70+ → 76
- **CONTEXT.md** — Tests: 1,502 → 1,510; files: 147 → 148; lines: ~47,500 → ~47,800
- **DEPLOYMENT_CHECKLIST.md** — Date: Apr 8 → Apr 12; tests: 1,441 → 1,510;
  SPDX: 136 → 148

## Code Health (Session 36 State)

| Metric | Value |
|--------|-------|
| Tests | 1,510 passing (`--all-features`) |
| Coverage | ~93% lines (CI gate: 90%) |
| Source files | 148 `.rs`, ~47,800 lines |
| Clippy | 0 warnings (workspace-wide `-D warnings`) |
| Unsafe blocks | 0 |
| Production TODOs | 0 |
| SPDX compliance | 148/148 (100%) |
| Max file | ~960 lines (test integration file; limit: 1000) |

## For Trio Partners (loamSpine, sweetGrass)

- rhizoCrypt now sends `contribution.record_provenance` JSON-RPC calls with
  `TCP_NODELAY` + `flush` on the outbound TCP connection. Partners should verify
  their JSON-RPC handlers accept this method.
- Witness chain round-trip validated locally (store → wire → deserialize). The
  primalSpring audit action "validate witness chain under NUCLEUS mesh" is now
  covered at the unit/e2e level. Full mesh validation deferred to NestGate
  composition parity.

## For primalSpring Gap Registry

- **TRIO-IPC (rhizoCrypt)**: RESOLVED — `notify_provenance` complete,
  `TCP_NODELAY` + `flush` hardened, witness round-trip tested.
- **DEEP-DEBT (rhizoCrypt)**: RESOLVED — All pre-existing clippy blockers
  cleared, zero warnings on `--all-targets --all-features`.
