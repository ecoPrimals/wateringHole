# Songbird v0.2.1 — Wave 110: primalSpring Audit Response — Capability Naming Wave

**Date**: April 4, 2026
**Commit**: `3ecdfcfd` on `main`
**Previous**: Wave 109 (`af88cc08`) — root docs cleanup

---

## primalSpring Audit Findings Addressed

| Finding | Status |
|---------|--------|
| 935 primal-name refs / 178 files | **541 refs / 174 files** (42% total reduction from audit baseline) |
| SB-02: ring lockfile ghost | **Confirmed**: ring v0.17.14 only via optional `k8s` feature (`kube` → `rustls` → `ring`). Default build is ring-free. Lockfile ghost — Cargo limitation. |
| SB-03: sled default-on | **False positive**: sled is `default = []` (optional) in all 3 crates (orchestrator, sovereign-onion, tor-protocol). Feature-gated with `sled-storage` or `persistent-cache`. |
| 1 test failure (env-dep) | Resolved in Wave 107 — test renamed to `security_provider_mode_errors_when_unavailable` |

## Reference Count Evolution

| Wave | .rs Refs | Files | Reduction |
|------|----------|-------|-----------|
| Baseline (primalSpring) | 935 | 178 | — |
| Post-Wave 107 | 759 | — | 19% |
| Post-Wave 108 | 719 | 188 | 23% |
| **Post-Wave 110** | **541** | **174** | **42%** |

### By Primal Name

| Name | Before (W108) | After (W110) | Change |
|------|---------------|--------------|--------|
| beardog | 539 | 419 | -22% |
| toadstool | 71 | 44 | -38% |
| squirrel | 72 | 46 | -36% |
| nestgate | 40 | 33 | -18% |

## Changes (44 files across 15 crates)

### Config Crate
- `primal_discovery.rs`: Docs, test names evolved; `get_endpoint_by_capability` wording
- `environment.rs`: Added `compute_provider_endpoint()`, `ai_provider_endpoint()` with deprecated `toadstool_endpoint()`
- `agnostic_primal_config.rs`: Docs and test URLs use capability names
- `defaults/ports.rs`: New `provider_capability_scan_ports()`; `primal_scan_ports()` deprecated
- `canonical/constants/*`: Test data uses neutral names; comments updated

### IPC + Platform
- `platform/unix.rs`: Docs use capability language; socket stems include both legacy + capability names
- `capability/strategy.rs`: Tests use `security` instead of `beardog`
- `error.rs`: Test payloads use `security-provider`
- `lib.rs`: Examples use capability socket paths

### Networking + Federation
- `security/mod.rs`, `noop.rs`, `production.rs`, `mock.rs`: Docs and logs use capability language
- `rendezvous/client.rs`: Doc clarifies capability-first wording
- `lineage-relay/security.rs`: Logs/docs use capability language

### Test Files
- 16 orchestrator test files: Tag strings, issuer names, trust prefixes evolved
- `adapter_integration_tests.rs`: Factory URLs use capability names
- `integration_test.rs` (tor): `beardog` bindings → `security_provider`

### Test Infrastructure
- `fixtures/ports.rs`: New `capabilities` module; deprecated `primals` aliases
- `fixtures/security_provider.rs`: Docs capability-first
- `mocks/*`: Doc wording shifted to capabilities

## Verification

| Check | Status |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (zero warnings) |
| `cargo test --workspace` | **12,530 passed**, 0 failed |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Remaining

~541 .rs refs remain, primarily:
- `#[deprecated]` function bodies and annotations (~129 attrs)
- Serde wire-compatibility aliases (6)
- Env var names interfacing with external binaries (`BEARDOG_BIN`, `BEARDOG_SOCKET`)
- Legacy socket path fallbacks (`beardog.sock`) for real installs

Estimated 1 more wave to reach near-minimum (irreducible refs from deprecated + wire compat).
