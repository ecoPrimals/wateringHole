<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Songbird v0.2.1 — Wave 64: Cross-Ecosystem Absorption, Naming Convergence & Lint Unification

**Date**: March 23, 2026
**Session**: 11
**Primal**: Songbird (Network Orchestration & Discovery)
**Domain**: `network`
**License**: scyBorg (AGPL-3.0-only + ORC + CC-BY-SA 4.0)
**Baseline**: v0.2.1-wave63
**Result**: v0.2.1-wave64

## Summary

Cross-ecosystem audit of 7 springs and 13 primals drove method naming convergence,
identity-based discovery elimination, and workspace-wide lint unification. Added
`health.readiness` and `health.check` JSON-RPC methods with `normalize_method()`
for ecosystem naming drift tolerance. Unified lint inheritance across all 30 crates.
Created `CONTEXT.md` for wateringHole PUBLIC_SURFACE_STANDARD compliance.

## Quality Gate

| Check | Before (wave63) | After (wave64) |
|-------|-----------------|----------------|
| `cargo fmt --check` | PASS | PASS |
| `cargo clippy --all-targets -D warnings` | PASS (pedantic+nursery) | PASS (pedantic+nursery) |
| `cargo doc --no-deps` | PASS (0 warnings) | PASS (0 warnings, `-D warnings`) |
| `cargo test --workspace` | PASS (10,023 / 0) | PASS (10,020 / 0) |
| `cargo deny check` | PASS | PASS |
| File size max | 959 lines | 959 lines |
| Coverage (llvm-cov) | 66.02% | 62.27% |
| Unsafe code | 2 (justified) | 2 (justified) |
| SPDX coverage | 100% | 100% |
| JSON-RPC methods | 12 | 14 |
| Lint inheritance | 15/30 crates | 30/30 crates |
| CONTEXT.md | absent | present |

---

## What Was Done

### Ecosystem Method Naming Convergence
- Added `health.readiness` JSON-RPC method — subsystem status reporting
- Added `health.check` JSON-RPC method — full health with details
- Implemented `normalize_method()` in `songbird-universal-ipc/introspection`
- Canonicalizes: `capability.list` → `capabilities.list`, `ping` → `health.liveness`, `status`/`check`/`health` → `health.check`
- Both IPC service handler and HTTP JSON-RPC gateway dispatch through `normalize_method()`
- Updated `rpc_discover_standard()` to advertise all 14 methods
- 7 new tests for normalization, readiness, and health check

### Identity-Based Discovery Elimination
- Evolved `handle_health_standard` — removed hardcoded `BEARDOG_SOCKET` / `beardog.sock`
- Now uses capability-based 5-tier: `CRYPTO_PROVIDER_SOCKET` → `CRYPTO_SIGN_PROVIDER_SOCKET` → XDG family-scoped socket
- Response field renamed `beardog_connected` → `crypto_provider_available`

### Workspace Lint Unification
- Added `[lints] workspace = true` to 15 crates previously missing lint config
- All 30/30 crates now inherit workspace pedantic+nursery lints
- Fixed all clippy errors from lint inheritance

### Production Safety
- Fixed private intra-doc link in `health.rs`
- Evolved `unreachable!()` in `http_server.rs` → `Err(anyhow!(...))` return
- `RUSTDOCFLAGS="-D warnings" cargo doc` now passes clean

### wateringHole Standards
- Created `CONTEXT.md` at repo root (PUBLIC_SURFACE_STANDARD)
- AI-ingestible context: role, capabilities, IPC surface, dependencies, metrics

### Cross-Ecosystem Audit
- Reviewed 7 springs: hotSpring, groundSpring, neuralSpring, wetSpring, airSpring, healthSpring, ludoSpring, primalSpring
- Reviewed 13 primals: BearDog, NestGate, Squirrel, ToadStool, biomeOS, petalTongue, rhizoCrypt, LoamSpine, sweetGrass, sourDough, skunkBat, barraCuda, coralReef
- Absorbed primalSpring Phase 12 patterns: capability-based health methods, 5-tier discovery

---

## Verification

```
cargo fmt --all -- --check                                              # clean
cargo clippy --all-targets --all-features --workspace -- -D warnings    # zero warnings
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps              # clean
cargo test --workspace                                                  # 10,020 passed, 0 failed
```

---

## What's Next

1. **Coverage expansion** — 62% → 90% target (orchestrator adapters, universal adapters)
2. **DispatchOutcome<T> + IpcErrorPhase** — align outbound IPC with ecosystem resilience stack
3. **STUN sovereignty-first 4-tier escalation** — self → family → community → public STUN
4. **BearDog crypto wiring** — unblocks circuit build + onion encryption

---

## Inter-Primal Notes

### For All Primals
- `normalize_method()` now tolerates ecosystem naming drift — primals using `ping`, `status`, `check`, `capability.list` as method names will be routed correctly
- `health.readiness` returns subsystem component health (not just liveness)
- `health.check` returns detailed health with component breakdown
- All 30 crates now enforce `clippy::pedantic + nursery` via workspace inheritance

### For BearDog
- Health endpoint now discovers crypto provider by capability (`CRYPTO_PROVIDER_SOCKET`), not by name
- Zero references to `beardog.sock` or `BEARDOG_SOCKET` remain in Songbird production code

### For biomeOS / Squirrel
- `capability.list` alias routes to `capabilities.list` (Squirrel naming tolerance)
- `CONTEXT.md` available for AI-ingestible primal context

### For Spring Teams
- Songbird implements the primalSpring Phase 12 capability-based health pattern
- Method normalization handles naming divergence across springs without breaking existing callers
- Workspace lint unification pattern (15-crate migration) documented as reference for other primals

### Absorption Opportunities Identified
- primalSpring `DispatchOutcome<T>` + `IpcErrorPhase` for outbound IPC resilience (not yet implemented)
- primalSpring STUN sovereignty-first 4-tier escalation (not yet implemented)
- primalSpring bonding policy evolution (future work)
