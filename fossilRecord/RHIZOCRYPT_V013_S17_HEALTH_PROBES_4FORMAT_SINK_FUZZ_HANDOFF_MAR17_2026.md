# rhizoCrypt v0.13.0-dev — Session 17 Handoff

**Date**: March 17, 2026  
**Primal**: rhizoCrypt (ephemeral DAG engine)  
**Session Focus**: Health probes, 4-format capability parsing, ValidationSink, JSON-RPC proptest fuzz

---

## What Changed

### 1. `health.liveness` + `health.readiness` JSON-RPC Methods

Absorbed from the emerging ecosystem pattern (sweetGrass V0.7.19, coralReef Iter52, healthSpring V32).

- `health.liveness` — zero-cost probe returning `{ "alive": true }`. Kubernetes-compatible, biomeOS health monitoring ready.
- `health.readiness` — checks whether the primal can accept work. Returns `{ "ready": bool, "primal": "rhizocrypt", "version": "..." }`.
- Registered in `CAPABILITIES`, `COST_ESTIMATES`, `SEMANTIC_MAPPINGS`, `CAPABILITY_DOMAINS` in `niche.rs`.
- Wired into JSON-RPC handler dispatch table (`handler.rs`).

### 2. `deny.toml` Yanked Crate Hardening

- Added `yanked = "deny"` to `[advisories]` section.
- CI now fails if any dependency uses a yanked crate version.

### 3. 4-Format Capability Parsing

Absorbed from airSpring v0.8.7 4-format parser. Extends previous dual-format parsing to handle all ecosystem response shapes:

- **Format A**: Flat string array `["dag.session.create"]`
- **Format B**: Nested objects `[{"name": "dag.session.create"}]`
- **Format C**: Wrapper `{"capabilities": [...]}` (biomeOS, neuralSpring)
- **Format D**: Double-nested `{"capabilities": [{"name": "..."}]}` (toadStool S155+)
- Also handles `{"methods": [...]}` variant (coralReef)
- Exported as `discovery::extract_capabilities()`

### 4. `ValidationSink` Trait

Absorbed from ludoSpring V22 pattern. Makes `ValidationHarness` output pluggable:

- `ValidationSink` trait with `header()` and `check()` methods
- `StderrSink` — default (backwards compatible)
- `StringSink` — captures output to string buffer (testing)
- `ValidationHarness::finish_to(sink)` — direct output to any sink
- `ValidationHarness::checks()` — programmatic access to raw results

### 5. JSON-RPC Proptest Fuzz (11 new property tests)

- JSON-RPC request roundtrip, error extraction, success non-extraction
- `IpcErrorPhase` mutual exclusion invariant
- `ValidationHarness` pass/fail sum invariant
- `ValidationSink` capture invariant
- 4-format capability parsing: one property test per format

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt` | Clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 warnings |
| `cargo doc --workspace --no-deps` | 0 warnings |
| `cargo test --workspace` | **1,102 tests**, 0 failures |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

---

## Audit Results

### Large File Audit
- 42 files >400 lines. Largest non-test files: `registry.rs` (840), `error.rs` (860+), `constants.rs` (772).
- Files are cohesive — large because they define complete domains, not because of poor factoring.
- Test files (`*_tests.rs`) are intentionally co-located and comprehensive.

### Mock Audit
- All mock implementations live in `integration/mocks.rs` with clear `#[cfg(test)]` / `test-utils` feature gating.
- `MockSigningProvider`, `MockPayloadStorageProvider`, `MockPermanentStorageProvider` are capability-based, not vendor-specific.
- Zero mock code in production paths. Test-only `DummyScenario` in `testing/chaos.rs`.

### Unsafe Code Audit
- Zero `unsafe` blocks in production code.
- All three crates use `#![cfg_attr(not(test), forbid(unsafe_code))]`.
- Binary crate uses `#![forbid(unsafe_code)]`.

### Hardcoded Address Audit
- All addresses in constants (`PRODUCTION_BIND_ADDRESS`, `DEFAULT_RPC_PORT`) have env var overrides via `SafeEnv`.
- Test addresses are in test modules only.
- Doc examples use `127.0.0.1` as illustrative only.

---

## What rhizoCrypt Now Provides to the Ecosystem

- **Health probes** for Kubernetes/biomeOS integration (`health.liveness`, `health.readiness`)
- **Universal capability parsing** via `extract_capabilities()` — any primal can use this to parse responses from any other primal
- **Pluggable validation** via `ValidationSink` — composable health checks with configurable output
- **11 property-based tests** covering JSON-RPC wire format, error handling, and capability parsing

---

## Absorption Sources

| Source | What Was Absorbed |
|--------|------------------|
| sweetGrass V0.7.19, coralReef Iter52, healthSpring V32 | `health.liveness`/`health.readiness` probe pattern |
| wateringHole standards | `yanked = "deny"` in cargo-deny |
| airSpring v0.8.7 | 4-format capability parsing |
| ludoSpring V22 | `ValidationSink` trait pattern |
| Ecosystem proptest convergence | JSON-RPC property-based fuzz testing |
