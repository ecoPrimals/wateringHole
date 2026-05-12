# BearDog v0.9.0 — Wave 28 Deep Debt Evolution Handoff

**Date:** April 2, 2026
**Author:** AI pair (Claude) + eastgate
**Scope:** Self-knowledge cleanup, `Box<dyn Error>` → `BearDogError`, hardcoded address evolution, feature flag naming, stub documentation

---

## Summary

Addressed remaining deep debt: self-knowledge violations (hardcoded primal
names), error typing in AI module, hardcoded addresses in documentation,
cross-primal naming in feature flags, and stub language precision.

---

## Gate Status (April 2, 2026)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace -D warnings` | Pass (0 warnings) |
| `cargo test --workspace` | **14,366 passed, 0 failed** |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

---

## Changes

### Self-Knowledge Cleanup

| Item | Before | After |
|------|--------|-------|
| `SongbirdClient` type alias | Deprecated alias in `beardog-ipc` | Removed entirely |
| Tower-atomic docs | "delegates to Songbird" | "delegates to the network transport primal" |
| Discovery warnings | "biomeOS Neural API not reachable" | "ecosystem service registry not reachable" |
| Installer docs | "songbird" in CLI examples | Generic "other-primal" |
| Feature flag | `advanced-nestgate` | `advanced-registry` |

### Error Typing

| File | Before | After |
|------|--------|-------|
| `ai/hybrid_intelligence/core/orchestration.rs` | `Result<..., Box<dyn Error + Send + Sync>>` | `Result<..., BearDogError>` |
| `ai/hybrid_intelligence/core/integration.rs` | `Result<..., Box<dyn Error + Send + Sync>>` | `Result<..., BearDogError>` |

### Hardcoded Address Documentation

Annotated doc examples in tarpc client/server/types, node-registry, and BTSP
transport with capability-based discovery notes. No production logic changes
needed — all runtime addresses already come from config/env.

### Stub Documentation

PKCS#11 and TPM stub comments now reference target pure Rust crates
(`pkcs11`, `tss-esapi`) for Phase 2. Config management "placeholder" language
removed.

---

## Known Remaining Debt (Low Priority)

| Item | Status | Notes |
|------|--------|-------|
| `BiomeOSPaths` type alias in installer | Deprecated alias for `PlatformPaths` | Kept for backward compat |
| "biomeOS" in IPC namespace constants | Intentional | Actual filesystem directory name on disk |
| PKCS#11 / TPM Phase 2 crypto | Documented | Requires pure Rust bindings |
| FIDO2/CTAP2 Phase 2 stubs | Documented | Returns proper errors |
| `coverage_boost_wave10.rs` in `beardog-tunnel/src/` | Test helpers in src/ | Could be moved to tests/ |
