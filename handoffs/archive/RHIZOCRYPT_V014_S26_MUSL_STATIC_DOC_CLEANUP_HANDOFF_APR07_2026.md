# rhizoCrypt v0.14.0-dev — Session 26 Handoff

**Date**: April 7, 2026
**Session**: 26
**Focus**: Musl-static deployment, Dockerfile evolution, sovereignty cleanup, documentation refresh

---

## Summary

Resolved the rhizoCrypt musl-static deployment debt identified by the primalSpring
downstream audit. Built, verified, and harvested a fully static x86_64 musl binary
to plasmidBin. Evolved the Dockerfile to a multi-stage musl-static build with Alpine
runtime. Cleaned stale documentation across rhizoCrypt and wateringHole.

---

## Changes

### 1. Musl-Static Binary (ecoBin Deployment Compliant)

- Built `x86_64-unknown-linux-musl` release binary — fully static, stripped (5.4 MB)
- BLAKE3 checksum computed and harvested to `plasmidBin/checksums.toml`
- `plasmidBin/manifest.toml` updated: `stripped = true`, `static = true`
- `wateringHole/genomeBin/manifest.toml`: `0.14.0-dev`, `pie_verified = true`

### 2. Dockerfile Multi-Stage Musl Evolution

- Builder: `rust:1.87-slim` + `musl-tools` + `x86_64-unknown-linux-musl` target
- Runtime: `alpine:3.20` with dedicated non-root user (UID 1000)
- Binary at `/app/rhizocrypt`, healthcheck via `status` subcommand
- OCI labels, SPDX license identifier

### 3. Documentation Cleanup

- `CHANGELOG.md`: Added session 26 entry with musl-static and Dockerfile work
- `CONTEXT.md`: Binary size now notes musl-static; genomeBin row updated
- `crates/rhizocrypt-service/README.md`: Docker example evolved from `rust:1.85` + `debian:bookworm-slim` to musl-static + Alpine pattern
- `docs/DEPLOYMENT_CHECKLIST.md`: Session reference updated (24 → 26), musl-static deployment note added

### 4. Blocking Fix: `dag.dehydrate` Alias

- Added `"dag.dehydrate"` alias for `"dag.dehydration.trigger"` in JSON-RPC handler dispatch and MCP `tools.call` dispatch
- Springs calling `capability.call("dag", "dehydrate")` via biomeOS prefix matching now reach the correct handler
- New test: `test_dehydrate_alias_routes_to_trigger`

### 5. Internal Vocabulary: `attested_at` → `witnessed_at`

- Renamed `Attestation.attested_at` to `witnessed_at` across 6 files to align with `WireWitnessRef` wire vocabulary

### 6. Sovereignty Cleanup

- Evolved 14 doc comments from primal-specific names to capability-neutral language across `service.rs`, `client.rs`, `handler.rs`, `mod.rs`, `uds.rs`, `dehydration_wire.rs`
- Removed misleading "LEGACY: Primal-Specific Traits" section from `integration/mod.rs`
- Evolved test mock IDs from primal names (`mock-beardog-1`, `toadstool.example.com`) to capability-neutral (`mock-signing-1`, `compute.example.com`) across 4 test files
- Extracted `beardog_http.rs` inline tests (330 lines) to `beardog_http_tests.rs` using `#[path]` pattern

### 7. GAP-MATRIX-05: Live IPC Validation (RESOLVED)

- Implemented `identity.get` method — biomeOS uses this for primal discovery
- Changed `capabilities.list` wire format to biomeOS Format E (`provided_capabilities` wrapper)
- Live-validated all probes on release binary: `identity.get`, full health triad, `capabilities.list` — all PASS on TCP newline (9401) and UDS
- ECOSYSTEM_COMPLIANCE_MATRIX Tier 10 grade: D → A
- GAP-MATRIX-05 for rhizoCrypt: RESOLVED
- New test: `test_identity_get`

### 8. wateringHole Updates

- `ECOSYSTEM_COMPLIANCE_MATRIX.md`: rhizoCrypt musl DEBT → PASS (Tier 2, Tier 9 x86_64), grade B in Tier 9, detail text updated
- `PRIMAL_REGISTRY.md`: rhizoCrypt 0.13.0-dev → 0.14.0-dev, 1,412 → 1,424 tests, musl-static shipped
- Cleaned stale musl-pending references in loamSpine and sweetGrass handoffs
- `PRIMALSPRING_TRIO_WITNESS_HARVEST_HANDOFF_APR07_2026.md`: plasmidBin status updated

### 8. Documentation Refresh

- `docs/DEPLOYMENT_CHECKLIST.md`: 1,424 tests, 130 `.rs` files, April 7 date
- `docs/ENV_VARS.md`: Last Updated → April 7, 2026
- `showcase/00_START_HERE.md`: 1,424 tests, 94.34% coverage, April 7 date
- `showcase/ENVIRONMENT_VARIABLES.md`: Clarified `SONGBIRD_TOWER` as showcase-only

---

## Quality Gates

- `cargo fmt` — clean
- `cargo clippy --workspace --all-features` — 0 warnings
- `cargo test --workspace --all-features` — 1,425 tests, 0 failures
- `cargo llvm-cov` — 94.34% lines (CI gate: 90%)
- Musl-static binary verified (file, ldd, BLAKE3)
- All `.rs` files under 1000 lines (max: 928)
- Zero unsafe, zero production unwrap/expect

---

## Remaining Trio Debt

- **loamSpine**: Still glibc in plasmidBin — needs musl-static build and harvest
- **sweetGrass**: Still glibc in plasmidBin — needs musl-static build and harvest
- rhizoCrypt aarch64 musl-static: CI cross-compile jobs exist, binary not yet harvested to plasmidBin

---

## Downstream Impact

- benchScale can now deploy rhizoCrypt via container (musl-static, no glibc dependency)
- loamSpine and sweetGrass remain blocked for container deployment until their musl-static builds are completed
- Springs can now call `dag.dehydrate` without 404 (blocking alias fix)
- rhizoCrypt production code has zero primal-specific doc comments in non-adapter modules
