# NestGate v4.7.0-dev — Sessions 43u/43v/43w Handoff

**Date**: April 16, 2026
**Sessions**: 43u (stadial parity gate), 43v (coverage + flaky fix + file split), 43w (deprecated 114→0, rand API migration)

---

## Summary

Three sessions completing stadial parity gate requirements and driving deprecated markers
to zero. All verification gates green: fmt, clippy (pedantic+nursery, 0 warnings), deny,
tests (8,695 passing / 0 failures / 60 ignored), coverage 84.12%, zero files over 800 lines,
zero `#[deprecated]` markers remaining.

---

## Session 43u: Stadial Parity Gate

### ring lockfile elimination

Vendored `rustls-webpki 0.103.12` with `ring` optional dependency stripped entirely from
its `Cargo.toml`. Added `[patch.crates-io]` override in workspace root. `ring` stanza
completely removed from `Cargo.lock` (521→519 packages). `cargo deny check` passes clean.
`cargo tree -i ring` confirms zero references.

### dyn keyword audit (317 matches)

Classified all usages:
- 154 test-only
- 39 comments/docs
- ~65 `dyn Error` (standard Rust pattern)
- ~22 std trait objects (`Send`, `Sync`, `Future`)
- ~37 intentional DI/strategy/plugin patterns (`dyn EnvSource`, `dyn RpcHandler`,
  `dyn HealthCheck*`, `dyn CapabilityResolver`, `dyn DiscoveryMechanism`, `dyn *Detector`)

**Zero stadial debt from trait-object dispatch.**

### async_trait audit (73 text matches)

Zero `#[async_trait]` attributes in any `.rs` file. Zero `async-trait` in any `Cargo.toml`.
All 73 text matches are comments, doc strings, migration template strings, or detection
helper test fixtures.

---

## Session 43v: Coverage Push + Flaky Test Fix + File Split

### Coverage 83.86% → 84.12%

New tests added across 15+ production files: objects.rs, datasets.rs, health_monitoring.rs,
connection_pool.rs, transport/handlers.rs, semantic_router/storage.rs, rpc_router.rs,
json_rpc_handler.rs, runtime_discovery.rs, agnostic_config.rs, pool/operations.rs,
automation/engine.rs, snapshot/scheduler.rs, cert/mod.rs, compliance/manager.rs.

### Flaky test fix (nestgate-installer)

`verify_installation_succeeds_when_binary_reports_version` — ETXTBSY race condition
fixed with `OpenOptions::mode(0o755)` + `sync_all()` for atomic script creation.

### File split

`semantic_router/storage.rs` 808 → 450 lines (tests extracted to `storage_tests.rs`).

### Deprecated 116 → 114

Removed `CanonicalRpcConfig` and `CircuitBreakerConfig` (zero external callers).

---

## Session 43w: Deprecated Cleanup (114 → 0)

### Strategy

Audit revealed most `#[deprecated]` markers were premature — the noted replacement
(`CanonicalNetworkConfig`) didn't semantically fit domain-specific config types. Items
were actively used and canonical.

### Breakdown

| Category | Count | Action |
|----------|-------|--------|
| runtime_fallback_ports constants | 21 | Un-deprecated — they ARE the canonical fallbacks |
| REST handler functions | 21 | Un-deprecated — still wired to active REST router |
| Domain-specific config structs | ~40 | Un-deprecated — genuine types with no fitting replacement |
| Scattered types (8 crates) | ~30 | Un-deprecated — active re-exports and compat types |
| `#[expect(deprecated)]` suppressions | ~30 files | Removed — no longer needed |

### rand API migration

`rng.gen_range()` → `rng.random_range()`, `rng.r#gen::<f64>()` → `rng.random::<f64>()`
in load_balancing modules for Rust 2024 keyword compatibility.

---

## Items for primalSpring to Update

1. **ECOSYSTEM_COMPLIANCE_MATRIX**: NestGate deprecated count → 0, tests → 8,695,
   coverage → 84.12%.
2. **STADIAL_PARITY_GATE**: NestGate `ring` — RESOLVED (vendored rustls-webpki, zero
   stanzas in lockfile). `dyn` audit — RESOLVED (zero stadial debt). `async_trait` —
   RESOLVED (zero attributes, zero dependency).
3. **PRIMAL_GAPS.md**: Coverage 84.12% → 90% still tracked. Deprecated → 0 (RESOLVED).
   Vendored `rustls-rustcrypto` + `rustls-webpki` still needed (upstream unchanged).

---

## Verification

```
Build:    cargo check --workspace                              PASS (0 own-code warnings)
Clippy:   cargo clippy --workspace --lib -- -W clippy::all     PASS (0 warnings)
          -W clippy::pedantic -W clippy::nursery
Format:   cargo fmt --all --check                              PASS
Deny:     cargo deny check                                     PASS (advisories, bans, licenses, sources)
Tests:    cargo test --workspace --lib                         8,695 passing, 0 failures, 60 ignored
Coverage: cargo llvm-cov --workspace --lib --summary-only      84.12% line
Files:    rg -c '' --type rust code/crates/ | sort -t: -k2 -rn | head -1 → all under 800 lines
Deprecated: rg '#\[deprecated' code/                           0 matches
ring:     cargo tree -i ring                                   "nothing to print"
```

---

## Remaining Evolution Targets

| Item | Status |
|------|--------|
| Coverage 84.12% → 90% | IN PROGRESS — ZFS (needs real ZFS), installer (platform), cloud backends |
| Vendored rustls-rustcrypto | Track upstream for drop opportunity |
| Vendored rustls-webpki | Track upstream for ring-free release |
