<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.30 — Capability-Based Discovery Compliance

| Field | Value |
|-------|-------|
| **Date** | 2026-04-02 |
| **Primal** | Squirrel (AI Coordination) |
| **From** | primalSpring audit compliance: PRIORITY 3 — Capability-Based Discovery |
| **Version** | 0.1.0-alpha.30 |
| **Status** | GREEN — 7,162 tests / 0 failures / 110 ignored / zero clippy / zero direct SONGBIRD_* env reads |

---

## Summary

Addressed primalSpring PRIORITY 3 audit finding: Squirrel was tightly coupled to Songbird
by name for discovery services (~129 SONGBIRD_* references). The `discover_songbird_socket`
export was in the public API surface. Squirrel should request the "discovery" capability,
not know that Songbird provides it.

## Audit Resolution

| Finding | Resolution |
|---------|------------|
| `pub use songbird::discover_socket as discover_songbird_socket` in public API | Renamed to `discover_discovery_socket` from `capabilities/discovery_service.rs` |
| `capabilities/songbird.rs` module named after a primal | Renamed to `capabilities/discovery_service.rs` |
| `SONGBIRD_SOCKET` env var in socket resolution | Primary is now `DISCOVERY_SOCKET`; `SONGBIRD_SOCKET` is deprecated fallback |
| `SONGBIRD_*` env vars in routing paths | All replaced with `DISCOVERY_*`/`SERVICE_MESH_*`/`MONITORING_*` primaries |
| Monitoring types named after Songbird | `SongbirdProvider` → `MonitoringServiceProvider`, `SongbirdMonitoringClient` → `ServiceMeshMonitoringClient`, etc. |
| Config field `songbird_endpoint` | Renamed to `discovery_endpoint` with serde alias for JSON compat |
| Ecosystem-api `SongbirdConfig` | Renamed to `ServiceMeshConfig`; field `songbird` → `service_mesh` |
| Bootstrap chicken-and-egg | Documented `discovery.sock` symlink pattern in `discovery_service.rs` |
| `primal_names` usage in socket/dispatch | Verified zero violations — all remaining refs are logging/type-mapping only |

## Env Var Migration

All SONGBIRD_* env vars now have modern primaries with deprecated fallbacks:

| Old (deprecated) | New (primary) | Purpose |
|-------------------|---------------|---------|
| `SONGBIRD_SOCKET` | `DISCOVERY_SOCKET` | Discovery service socket path |
| `SONGBIRD_ENDPOINT` | `SERVICE_MESH_ENDPOINT` | Service mesh HTTP endpoint |
| `SONGBIRD_PORT` | `SERVICE_MESH_PORT` | Service mesh port |
| `SONGBIRD_COLLECTION_INTERVAL` | `MONITORING_COLLECTION_INTERVAL` | Metrics collection interval |
| `SONGBIRD_BATCH_SIZE` | `MONITORING_BATCH_SIZE` | Metrics batch size |
| `SONGBIRD_TIMEOUT_MS` | `MONITORING_TIMEOUT_MS` | Monitoring client timeout |
| `SONGBIRD_ENABLE_TRACING` | `MONITORING_ENABLE_TRACING` | Tracing toggle |
| `SONGBIRD_TEST_PORT` | `MONITORING_TEST_PORT` | Test port override |
| `SONGBIRD_AUTH_TOKEN` | `MONITORING_AUTH_TOKEN` | Monitoring auth token |
| `SONGBIRD_FLUSH_INTERVAL` | `MONITORING_FLUSH_INTERVAL` | Buffer flush interval |

Zero direct `SONGBIRD_*` reads remain — all in `.or_else()` fallback position.

## Remaining Acceptable References

Remaining `Songbird` references in the codebase are all in acceptable categories per audit:
- `PrimalType::Songbird` enum variant (type mapping)
- `primal_names::SONGBIRD` constant (logging, interning, display)
- `niche.rs` consumed capabilities (Songbird is a dependency)
- Test data (ecosystem type tests, discovery tests)
- Documentation and comments

None are in socket resolution or method dispatch.

## Quality Gates

```
cargo fmt --all -- --check         ✅ PASS
cargo clippy --all-features -- -D warnings  ✅ PASS (0 warnings)
cargo test --workspace --all-features       ✅ PASS (7,162 / 0 / 110)
direct SONGBIRD_* env reads        ✅ ZERO (all behind .or_else fallbacks)
```

## Remaining Work (Future Sessions)

- **Coverage lift** — 85.3% → 90% target
- **110 ignored tests** — audit and either fix or document
- **ecoBin v3 C elimination** — ring via sqlx/rustls needs rustls-rustcrypto migration
- **Clone audit** — ~1,500+ `.clone()` calls; review top-10 production files
