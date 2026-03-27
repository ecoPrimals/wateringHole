<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2024-2026 ecoPrimals -->

# Songbird v0.2.1-wave66 — Comprehensive Audit, cargo-deny, CI, Coverage & Stub Evolution

**Date**: March 23, 2026
**From**: Songbird session 13
**Primal**: Songbird (Network Orchestration & Discovery)
**Version**: v0.2.1-wave66
**Status**: All quality gates passing
**License**: AGPL-3.0-only (scyBorg triple)
**Supersedes**: SONGBIRD_V021_WAVE64_NAMING_CONVERGENCE_LINT_UNIFICATION_MAR23_2026

---

## Summary

Full codebase audit against wateringHole standards followed by systematic
resolution of all findings. cargo-deny now fully passing, CI modernized with
proper gating, all SPDX headers present, production stubs evolved to real
implementations, and 65 new tests added.

## Quality Gate Table

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --all-targets --all-features -- -D warnings` | PASS (pedantic + nursery) |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | PASS |
| `cargo deny check` | PASS (advisories ok, bans ok, licenses ok, sources ok) |
| `cargo test --all-features --workspace` | 10,366 passed, 0 failed, 271 ignored |
| Coverage (llvm-cov) | 66.96% (target 90%) |
| Files >1000 lines | 0 (max 959 test, 888 production) |

## Changes

### cargo-deny Evolution
- License allowlist: added MPL-2.0, Zlib for transitive deps
- Advisory IDs: corrected to actual RUSTSEC-2026-xxxx / 2025-xxxx identifiers
- Wildcards: `deny` → `allow` (workspace member deps are inherently wildcarded)
- Skip list for known transitive duplicates (windows-sys, syn, parking_lot, etc.)

### CI Modernization (quality-checks.yml)
- Coverage threshold: 58% → 66% (ratchets toward 90% target)
- Caching: `actions/cache@v3` → `Swatinem/rust-cache@v2`
- New jobs: `cargo-deny`, `rustsec/audit-check` (gates PRs)
- All jobs now use `--all-features`

### Lint Evolution
- `songbird-bluetooth`: `clippy::all = "allow"` → workspace lints (pedantic + nursery)
- `songbird-stun`: removed blanket crate-level suppressions; production `expect()` → `let-else`
- 30/30 crates on workspace lints; 2 justified custom tables

### Production Stub Evolution
- mDNS: empty stub → real multicast UDP PTR query (224.0.0.251:5353)
- Compute bridge: mock "accepted" → `SERVICE_UNAVAILABLE` with capability guidance
- IGD: hardcoded `8.8.8.8:53` → gateway-based local IP detection

### Coverage Expansion (+65 tests)
- TLS crypto.rs: JSON-RPC loopback, chacha20/ed25519/hmac/x25519 paths
- Orchestrator: broadcast discovery, workload classification, env config
- Config: providers, capability discovery, hardcoded_elimination

## Inter-Primal Notes

- **BearDog**: All crypto stubs return `CryptoUnavailable`; wiring unblocked when
  BearDog is available at runtime. No compile-time coupling.
- **primalSpring**: `normalize_method()` and semantic method naming from wave 64
  remain stable; primalSpring can validate these via `health.liveness` / `capabilities.list`
- **biomeOS / Neural API**: JSON-RPC gateway has 14 semantic methods ready for
  Neural API graph integration

## Pending

1. Coverage 66.96% → 90% (orchestrator ~56%, tls/crypto ~30% are biggest gaps)
2. BearDog crypto wiring (Tor circuit, TLS certs, onion encryption)
3. Ring-free workspace (rcgen replacement, quinn feature reconfiguration)
4. Platform backends (NFC, iOS, WASM, Android IPC)

---

Part of ecoPrimals — sovereign, capability-based Rust ecosystem.
