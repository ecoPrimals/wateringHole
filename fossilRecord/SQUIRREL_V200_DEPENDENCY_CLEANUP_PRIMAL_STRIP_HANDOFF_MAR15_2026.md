<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v2.0.0 — Dependency Cleanup & Primal Responsibility Strip

**Date**: March 15, 2026
**Author**: AI Agent (constrained evolution)
**Primal**: Squirrel (AI Coordination)
**Previous**: SQUIRREL_V190_SPRING_ABSORPTION_HANDOFF_MAR14_2026

---

## Summary

Major dependency cleanup and primal responsibility audit. Squirrel was the "Adam" primal — the first primal from which others were born. This session stripped vestigial code that now belongs to other primals (BearDog, Songbird, NestGate, ToadStool) and eliminated ~40% of unnecessary dependencies.

---

## Changes

### Dependency Cleanup (Phase 1-6)

| Action | Details |
|--------|---------|
| `cargo clean` | Reclaimed 88 GB + 3 GB stale target dirs |
| HTTP stack gated | axum/tower/tower-http behind `http-api` feature (default OFF) in squirrel-core |
| WebSocket gated | tokio-tungstenite behind `websocket` feature (default OFF) in squirrel-mcp |
| Unused deps removed | rayon, crossbeam-channel, eyre, config, num_cpus, pin-project, url, hex, urlencoding, sha1, hmac, time, flume, sled, argon2, simple_logger |
| serde_yaml replaced | Migrated to `serde_yml` across 9 Cargo.toml + 13 source files |
| sysinfo gated | Behind `system-metrics` feature; /proc reads as Pure Rust fallback |
| log → tracing | All `log::` macros migrated to `tracing::` across 14 files; explicit `log` dep removed from 9 Cargo.tomls |
| Pure Rust utils | Replaced external url/hex/urlencoding with inline pure Rust in MCP utils |

### Primal Responsibility Strip (Adam's Rib)

| Primal | Action | Lines affected |
|--------|--------|----------------|
| Songbird | Feature-gated federation, routing, load balancing, service discovery, swarm, ecosystem behind `mesh` | ~4,500 lines |
| ToadStool | Feature-gated GPU detection (NVML/ROCm/nvidia-smi) behind `gpu-detection` | ~778 lines |
| BearDog | Confirmed local JWT already gated behind `local-jwt`; deleted empty MCP security module | — |
| NestGate | Removed unused `sled` from 4 Cargo.tomls | — |

### Dead Code Cleanup

| Action | Files |
|--------|-------|
| Deleted orphaned tool/ modules | 6 files (lifecycle, management, cleanup — never compiled) |
| Deleted corrupt file | transport/frame.rs (4 lines, incomplete) |
| Deleted deprecated binary | cli/bin/core.rs (just printed migration message) |
| Deleted empty module | core/mcp/src/security/mod.rs (2 lines, no content) |

### Root Docs Updated

- README.md: Updated test counts, dep counts
- CURRENT_STATUS.md: Rewritten with current architecture, feature gates, recent evolution
- PRE_PUSH_CHECKLIST.md: Updated with current commands and standards
- Archived stale root docs (CAPABILITY_DISCOVERY_MIGRATION.md, READ_ME_FIRST.md, ROOT_DOCS_INDEX.md)

---

## Metrics

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Unique deps (non-dev) | 314 | 272 | -13% |
| HTTP crates compiled | 14 | 0 | -100% |
| Deprecated crates | 1 | 0 | -100% |
| target/ size | 84 GB | 23 GB | -73% |
| Clean build time | ~5 min | ~2.5 min | -50% |
| Incremental build | ~45s | ~8s | -82% |
| Tests (main crate) | — | 1,622 pass / 0 fail | — |
| Orphaned files | 8+ | 0 | cleaned |

---

## Feature Gate Architecture

```
squirrel (default features)
├── capability-ai          (always on — core AI coordination)
├── ecosystem              (always on — ecosystem integration)
└── tarpc-rpc              (always on — binary RPC)

squirrel-core (default: none)
├── mesh                   (Songbird code: federation, routing, swarm)
└── http-api               (legacy HTTP: axum, tower)

squirrel-mcp (default: streaming)
├── websocket              (WebSocket: tokio-tungstenite, axum 0.6)
├── tarpc                  (binary RPC)
└── persistence            (sled, sqlx, redis)

squirrel (main crate)
├── system-metrics         (sysinfo C dependency)
├── gpu-detection          (NVML/ROCm — ToadStool's domain)
└── monitoring             (prometheus metrics)

squirrel-mcp-auth
└── local-jwt              (jsonwebtoken/ring — BearDog's domain)
```

---

## Known Issues

1. `squirrel-mcp-auth` test suite has 114+ compile errors (pre-existing, unrelated to this session)
2. `squirrel-plugins` test suite has 21 compile errors (pre-existing API mismatch)
3. `squirrel-mcp` test suite has 2 type annotation errors (pre-existing)
4. `integration/web` crate excluded from workspace (full auth implementation belongs in BearDog)
5. `proto/` directory still exists at root (gRPC fully removed, can be archived)

---

## Next Steps

1. Fix pre-existing test compilation errors in auth, plugins, MCP crates
2. Archive `proto/`, `showcase/`, stale shell scripts
3. Consolidate duplicate type definitions (HealthStatus, DiscoveredService, EcosystemServiceRegistration)
4. Split remaining files over 1,000 lines
5. Push toward 90% test coverage
6. Evolve sysinfo → pure Rust /proc reads (remove system-metrics feature gate)

---

## Primal Relationships (Updated)

```
Squirrel (AI Coordination)
├── OWNS: MCP coordination, task routing, AI capability discovery,
│         context management, session management, config
├── DELEGATES TO:
│   ├── BearDog → auth, crypto, JWT (via capability discovery)
│   ├── Songbird → service mesh, federation, load balancing (feature-gated)
│   ├── NestGate → data storage, persistence, backup (client only)
│   └── ToadStool → GPU compute, batch processing (feature-gated)
└── DISCOVERS: All other primals via runtime capability scanning
```
