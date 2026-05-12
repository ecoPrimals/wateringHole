# biomeOS v3.01 — primalSpring Gap Resolution + Deep Debt Overstep V

**Date**: April 11, 2026
**Primal**: biomeOS
**Version**: v3.01
**License**: AGPL-3.0-or-later

---

## Summary

v3.01 resolves all 7 gaps from the primalSpring cross-spring upstream gap
synthesis (April 11, 2026) and executes a deep debt evolution pass focused on
hardcoding elimination, API modernization, and sovereignty compliance.

**Tests**: 7,726 passed, 0 failed
**Clippy**: Zero warnings (`clippy::pedantic + nursery`, `-D warnings`)
**Fmt**: Clean
**cargo-deny**: Passing

---

## primalSpring Gap Resolution

### 1. `capability.resolve` Single-Step Routing (Medium — RESOLVED)

**Source**: wetSpring PG-03, healthSpring §3, all springs

New `capability.resolve` JSON-RPC method returns the single best provider
endpoint for a given capability — the IPC equivalent of DNS resolution.
Springs no longer need to parse a list from `capability.discover`.

- Handler: `crates/biomeos-atomic-deploy/src/handlers/capability.rs`
- Route: `"capability.resolve"` → `Route::CapabilityResolveSingle`

### 2. Deploy-Time `consumed_capabilities` Validation (Low — RESOLVED)

**Source**: wetSpring V143

When biomeOS deploys a graph, `validate_consumed_capabilities()` now verifies
that all `consumed_capabilities` declared by each node are satisfiable by
other nodes' `provided_capabilities` before launching. Unsatisfied deps emit
warnings (non-blocking, allowing partial deployments).

- Logic: `crates/biomeos/src/modes/deploy.rs`

### 3. `lifecycle.composition` for Live Dashboards (Low — RESOLVED)

**Source**: ludoSpring

New `lifecycle.composition` JSON-RPC method returns the current composition
state: active/degraded/dead primals, counts, and a health ratio for
real-time monitoring dashboards.

- Handler: `crates/biomeos-atomic-deploy/src/handlers/lifecycle.rs`
- Route: `"lifecycle.composition"` → `Route::LifecycleComposition`

### 4. Canonical `discovery.find_by_capability` (Low — RESOLVED)

**Source**: healthSpring §3

`discovery.find_by_capability` is now a canonical route alias for
`Route::CapabilityDiscover` in the Neural API routing table, eliminating the
`net.discovery.find_by_capability` dual-fallback issue.

### 5. Canonical `inference.*` Namespace (Medium — RESOLVED)

**Source**: primalSpring shared with Squirrel + neuralSpring

`inference.*` standardized as the primary AI/ML namespace in
`wateringHole/SEMANTIC_METHOD_NAMING_STANDARD.md` (§7). `model.*` is
acceptable for model-management. `ai.*` is legacy.

### 6. `deny.toml` Spring Compliance (Low — RESOLVED)

Added `deny.toml` requirement to `SPRING_COMPOSITION_PATTERNS.md` (§12) and
`SPRING_AUDIT_PROMPT.md`. Documents minimum viable `deny.toml` with C/FFI
bans and CI enforcement guidance.

### 7. CI `cargo deny check` Enforcement (Medium — ALREADY RESOLVED)

biomeOS already runs `cargo deny check` as Job 6 in CI (`.github/workflows/ci.yml`).
No change needed — documented in spring guidance for other primals.

---

## Deep Debt Overstep V

### Hardcoding → XDG / Capability-Based

| Before | After | File |
|--------|-------|------|
| `/tmp/neural-api-{id}.sock` | `SystemPaths::neural_api_socket()` | `neural-api-server.rs`, `neural-deploy.rs` |
| `/tmp/primals/*.log` hints | `SystemPaths::default_runtime_dir()` | `neural-deploy.rs` |
| `PathBuf::from("/tmp")` | `std::env::temp_dir()` | `genome-deploy/deployer.rs` |
| `/tmp/biomeos-verify.log` | `std::env::temp_dir().join(...)` | `biomeos-verify.rs` |
| `"nat0"` hardcoded family | `family_discovery::get_family_id()` | `neural-deploy.rs`, `verify.rs` |
| `alias = "beardog-socket"` | Removed (generic `--security-provider-socket`) | `enroll.rs` |
| "Use Songbird to fetch" | "Use mesh discovery to fetch" | `model_cache.rs` |
| `8.8.8.8` Google DNS | RFC 5737 `192.0.2.1` | `dns_sd.rs` |

### API Evolution

| Change | Impact |
|--------|--------|
| `BiomeOSStandardAPI`: `Box<dyn Error>` → `anyhow::Result<T>` | Idiomatic, zero boxing |
| `RendezvousState::new()`: removed `_deprecated_socket` param | Clean API |
| `ApiConfig`: removed `port_deprecated` field | HTTP fully deprecated |
| `SystemPaths::default_runtime_dir()` + `neural_api_socket()` | Public XDG path API |

### Zero-Copy

- `Bytes::from(rand::random::<[u8; 32]>().to_vec())` → `Bytes::copy_from_slice(...)` (eliminates Vec allocation)

### Sovereignty

- `dns_sd.rs` local IP detection: Google DNS `8.8.8.8` replaced with RFC 5737
  documentation address `192.0.2.1` — never routed, no third-party dependency

### Flaky Test Fix

- `test_detect_ecosystem_coordinated_when_two_primals_respond`: mock server
  refactored to handle concurrent connections via `tokio::join!`

---

## For Downstream Springs

All springs that consume `capability.resolve`, `lifecycle.composition`, or
`discovery.find_by_capability` can now use these as first-class JSON-RPC
methods. The `inference.*` namespace is canonical — update IPC dispatch
tables accordingly.

Springs without `deny.toml` should add one per §12 of
`SPRING_COMPOSITION_PATTERNS.md`.

---

## Quality Gates

| Gate | Status |
|------|--------|
| Tests | 7,726 passed, 0 failed |
| Clippy | PASS (pedantic + nursery, `-D warnings`) |
| Formatting | PASS |
| Doc | PASS |
| `cargo deny check` | PASS |
| Files >1000 LOC | 0 |
| Unsafe code | 0 |
| TODO/FIXME | 0 |
| Production mocks | 0 |
