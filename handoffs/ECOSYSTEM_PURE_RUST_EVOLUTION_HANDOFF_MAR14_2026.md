# Ecosystem Pure Rust Evolution — Handoff (March 14, 2026)

**Date**: March 14, 2026
**Type**: Cross-Primal Dependency Evolution Handoff
**Scope**: ring removal, sled→redb migration, NestGate unsafe evolution, production mock isolation, hardcoded primal ref cleanup

---

## Summary of Changes Across All Primals

### ring Removal

| Primal | Status | Notes |
|--------|--------|-------|
| biomeOS | REMOVED from production | ureq default-features=false, Songbird delegation |
| Songbird | EVOLVED — rustls-rustcrypto default | ring still transitive via quinn (QUIC) |
| BearDog | USES ring via rustls/quinn | BearDog is the crypto provider; ring here is acceptable |
| rhizoCrypt | FEATURE-GATED | Only via http-clients feature (not default) |
| loamSpine | FEATURE-GATED | Only via discovery-http feature (not default) |
| sweetGrass | DEV-DEPS ONLY | testcontainers → ring (not in production) |
| Squirrel | NEEDS EVOLUTION | sqlx → rustls → ring |

### sled → redb Evolution

| Primal | Status | Notes |
|--------|--------|-------|
| rhizoCrypt | DONE | redb default since v0.12 |
| LoamSpine | DONE | redb default, sled optional (sled-storage feature) |
| sweetGrass | DONE | sweet-grass-store-redb created, sled store still available |
| biomeOS | DONE | biomeos-graph migrated to redb |
| Songbird | PENDING | sled in orchestrator, tor-protocol, sovereign-onion |
| BearDog | PENDING | sled in workspace |

### NestGate Unsafe Evolution

- 6 unsafe blocks replaced with safe alternatives (zero_cost_evolution, safe_ring_buffer, async_optimization)
- 8 unsafe blocks kept with SAFETY justification (lock-free data structures, FFI, SIMD)
- pin-project adopted for safe async pin projection

### Hardcoded Primal Reference Cleanup

- biomeOS rootpulse.rs: hardcoded primal arrays → capability-based discovery
- biomeOS primal_client.rs: named constructors deprecated in favor of `get_by_capability()`
- LoamSpine: already uses env-based discovery for ports/addresses

### Production Mock Isolation

- rhizoCrypt mocks already behind `#[cfg(test)]` / `test-utils` feature
- Squirrel MockNetworkConnection, MockServiceMeshClient, MockDatabaseClient isolated behind `#[cfg(any(test, feature = "testing"))]`

---

## What Remains

### Songbird sled→redb

- sled in orchestrator, tor-protocol, sovereign-onion crates
- Introduce redb as optional/default; add sled-storage feature for backward compat

### BearDog sled→redb

- sled in workspace crates
- BearDog is crypto provider; ring via rustls/quinn acceptable

### Squirrel ring evolution

- sqlx → rustls → ring in production path
- Options: feature-gate sqlx, evaluate rustls-rustcrypto support, or alternative SQL crates

### quinn ring dependency

- quinn (QUIC) depends on ring; no pure-Rust QUIC stack exists yet
- Songbird QUIC crate still pulls ring transitively
- Monitor `rustls-rustcrypto` maturity for quinn compatibility

---

*Handoff complete. See `PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md` for full dependency evolution status.*
