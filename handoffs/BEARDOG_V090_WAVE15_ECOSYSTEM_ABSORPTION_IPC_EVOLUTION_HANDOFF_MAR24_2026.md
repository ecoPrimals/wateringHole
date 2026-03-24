<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- Creative content: CC-BY-SA 4.0 (scyBorg provenance trio) -->

# BearDog v0.9.0 — Wave 15: Ecosystem Absorption, IPC Evolution, Semantic Naming v2.1.0 & Self-Knowledge

**Date**: March 24, 2026
**Version**: 0.9.0
**Edition**: 2024 | **MSRV**: 1.93.0
**Supersedes**: Wave 14 handoff (same date, continued session)

---

## Summary

Full cross-ecosystem review of all 8 springs, 11 primals, and wateringHole
standards, followed by systematic absorption of patterns and compliance
execution. Added IPC error types from rhizoCrypt/LoamSpine, differentiated
health endpoints per Semantic Method Naming Standard v2.1.0, removed all
hardcoded peer primal names from production code (self-knowledge principle),
migrated `#[allow]` to `#[expect(reason)]`, evolved production stubs to
explicit not-implemented errors, banned cross-primal type crates in deny.toml,
and added 60+ deep tests.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Coverage (lines) | 87.08% | **87.35%** |
| Coverage (functions) | 81.98% | **82.27%** |
| Tests | 14,387 | **14,447+** |
| Hardcoded peer primal names | ~75 in handlers | **0** (self-knowledge) |
| `#[allow(clippy::)]` in prod | ~45 | **~15** (rest migrated to `#[expect]`) |
| Production stubs | 5 files | **0** (evolved to `not_implemented` / real timing) |
| Cross-primal type bans | 0 | **8** (deny.toml) |
| Health endpoint shapes | 1 (all "healthy") | **3** (alive/ready/healthy per v2.1.0) |
| IPC error types | flat `String` | **`DispatchOutcome` / `IpcErrorPhase`** |

---

## Changes

### 1. IPC Error Types (from rhizoCrypt/LoamSpine)

Added `DispatchOutcome<T>` and `IpcErrorPhase` to `beardog-ipc`:
- `IpcErrorPhase::Transport` / `Protocol` / `Dispatch` / `Application`
- `route_with_outcome()` on `HandlerRegistry` for structured error returns
- `normalize_method()` for canonical method name normalization
- Full serde roundtrip tests

### 2. Health Handler v2.1.0

Differentiated per wateringHole Semantic Method Naming Standard:
- **Liveness** (`ping`, `health`, `health.liveness`) → `{"status":"alive"}`
- **Readiness** (`health.readiness`) → `{"status":"ready", "capabilities_count": N}`
- **Deep check** (`status`, `check`, `health.check`) → `{"status":"healthy", "timestamp": ...}`

Updated chaos, integration, and fault tests to match new response shapes.

### 3. Self-Knowledge (Primal Sovereignty)

Removed ~75 hardcoded "Songbird" references from production handler code:
- `btsp.rs`, `aliases_and_beardog.rs`, `tls12_dot.rs`, `capabilities.rs`,
  `relay.rs`, `introspection.rs`, `signatures.rs`, `hashing.rs`, `security.rs`,
  and crypto submodules
- Replaced with generic descriptions: "requesting primal", "network orchestration
  primal", "onion identity derivation", etc.
- BearDog now describes WHAT operations do, not WHO calls them

### 4. `#[expect(reason)]` Migration

30+ production `#[allow(clippy::...)]` → `#[expect(clippy::..., reason = "...")]`:
- `cast_precision_loss`, `struct_excessive_bools`, `too_many_arguments`,
  `unused_self`, `unreadable_literal`, `cast_possible_truncation`,
  `unnested_or_patterns`, `wrong_self_convention`
- 6 stale annotations removed (lint no longer fires)

### 5. Production Stub Evolution

- Migration adapters → `BearDogError::not_implemented(...)` with guidance
- Universal adapter → `Instant::now()` elapsed real timing
- BirdSong encrypt/decrypt → `ApiError::NotImplemented` (HTTP 501)
- Ecosystem status → explicit capability registry required error

### 6. deny.toml Cross-Primal Bans

8 primal type crates banned with `reason`:
`songbird-types`, `squirrel-types`, `toadstool-types`, `nestgate-types`,
`biomeos-types`, `coralreef-types`, `barracuda-types`, `provenance-trio-types`

### 7. Coverage Push (60+ Deep Tests)

| Crate | Focus |
|-------|-------|
| beardog-integration | Axum HTTP router, BTSP flow, error display, env config |
| beardog-production | Disaster recovery: missing paths, nested dirs, symlinks |
| beardog-errors | Result extensions: validation, option, error chain |
| beardog-deploy | Command runner: ADB mock branches, timeouts, spawn errors |
| beardog-installer | Env locking for genome target parallel safety |

### 8. Discovery Documentation

CONTEXT.md and ARCHITECTURE.md updated with:
- 5-tier discovery pattern (env → XDG → platform → primalSpring → mDNS)
- Credential resolution chain (env → file → BearDog `secret.resolve`)
- Wire-only contract principle (JSON-RPC schemas, no shared type crates)

---

## Gates

```bash
cargo fmt --check                               # Clean
cargo clippy --workspace --all-features \
  -- -D warnings                                # 0 warnings
cargo doc --no-deps                             # Clean
cargo deny check                                # 4/4 pass
cargo test --workspace                          # 14,447+ passed
```

---

## Ecosystem Absorption Sources

| Source | What was absorbed |
|--------|------------------|
| rhizoCrypt S20 | `DispatchOutcome` / `IpcErrorPhase` pattern, vendor-env removal |
| LoamSpine v0.9.12 | Protocol vs app error distinction |
| biomeOS v2.66 | 5-tier discovery documentation |
| wateringHole v2.1.0 | Health/capabilities differentiation, canonical aliases |
| sweetGrass v0.7.22 | Wire-only contract principle (no shared types) |
| Squirrel alpha.23 | `#[expect(reason)]` discipline |
| toadStool S134 | Credential resolution chain documentation |

---

## What's Next (Wave 16)

- **Coverage → 90%**: Main gaps in beardog-integration, tower-atomic
- **genomeBin manifest**: Update `wateringHole/genomeBin/manifest.toml`
- **`normalize_method()` in dispatch**: Wire into `HandlerRegistry::route`
- **Deeper `#[expect]` pass**: Remaining `#[allow]` in migration/canonical code
- **examples/ validation**: `cargo check --examples`
- **Showcase CI**: Compilation check for excluded showcase crates
- **Remaining biomeos path constants**: Evaluate extracting to config

---

## Files Changed (Summary)

- **56 files** changed, **1,267** insertions, **130** deletions
- **4 new files**: `dispatch.rs`, `method_names.rs`, `result_extension_deep_tests.rs`, `test_env_lock.rs`

---

## Inter-Primal Notes

- Health responses changed: `"health"` → `"alive"` (liveness), `"health.check"` → `"healthy"` (deep). Consumers expecting `"healthy"` from `"ping"` / `"health"` need to update.
- JSON-RPC wire contracts remain the only integration boundary
- No new compile-time coupling to any primal
- `beardog-ipc` now exports `DispatchOutcome` / `IpcErrorPhase` as public API

---

Part of ecoPrimals — sovereign, capability-based Rust ecosystem.
