# NestGate v4.7.0-dev — Coverage Push, Ring Elimination & Pure-Rust Evolution

**Date**: March 30, 2026  
**Primal**: nestgate (storage & discovery)  
**Session type**: Coverage target met, dependency purification, structural cleanup

---

## What Was Done

### Coverage: 77.05% -> 80.25% (wateringHole 80% minimum met)

- **1,457 tests** passing (up from ~1,390), 0 failures, 48 ignored
- 67+ new test functions across 30+ modules:
  - Config modernization (builders, idiomatic evolution, unified enums, capability config)
  - Canonical types (request/response)
  - API handlers (validation, tarpc, JSON-RPC, production placeholders, auth, REST routes)
  - Cache (multi-tier, UUID cache)
  - Automation (batch analysis, dataset analyzer)
  - ZFS engine (monitoring, engine, zero-cost manager, pool creation, production readiness, health, snapshot scheduler, parsers)
  - Security (cert manager, cert validator, transport security)
  - Transport (server lifecycle, Unix socket mock)
  - Discovery (universal adapter, capability discovery)
  - Core (load balancing, response traits, storage config/types/service, advanced optimizations)
  - Performance (adaptive optimization, zero-copy networking)
  - Types (unified enums, error constructors, utilities)

### Ring Eliminated

- Installer TLS switched from `rustls-tls` (which pulled ring) to `rustls-tls-webpki-roots-no-provider` + explicit `aws-lc-rs` crypto provider
- `cargo tree -i ring --workspace` returns nothing
- Process-default `CryptoProvider` installed before reqwest client construction
- HTTP behavior unchanged (same HTTPS GETs to GitHub API)

### Sysinfo Made Optional

- `nestgate-observe` and `nestgate-platform` default features no longer include `sysinfo`
- Linux builds use pure-Rust `/proc` parsing (already primary path)
- Non-Linux targets get sysinfo automatically via `nestgate-core`'s target-conditional dependency
- `cargo tree -p nestgate-observe` shows no sysinfo on Linux with default features

### Production Stubs Evolved to Real Implementations

- `get_communication_stats`: Returns live `CommunicationCounters` (Arc + AtomicU64) bumped by WebSocket/SSE handlers
- `get_events`: Returns real `event_log` from AppState (empty by default, not fabricated data)
- `AppState` gained `communication_counters` and `event_log` fields

### Dead Code Removed

- Removed entire `events` module tree from nestgate-observe (15 files: bus, dlq, pubsub, routing, streaming) — unused, real event types live in canonical_types
- Removed `pub use nestgate_observe::events` from nestgate-core
- `nestgate-zfs::dev_environment` feature-gated behind `dev-stubs`
- `nestgate-observe::stubs` renamed to `compat` for clarity

### Documentation & Quality

- Zero `cargo doc` warnings (fixed broken intra-doc links in runtime_fallback_ports, runtime_defaults, linux_proc)
- Zero clippy warnings with `--all-features -D warnings`
- Root docs updated: README, STATUS, CONTEXT, START_HERE, CHANGELOG
- Test isolation hardened for environment-sensitive tests

---

## Current Measured State

```
Build:       25/25 workspace members, 0 errors
Clippy:      ZERO errors (--all-features -D warnings)
Docs:        ZERO warnings
Tests:       1,457 lib, 0 failures, 48 ignored
Coverage:    80.25% line, 79.67% function (llvm-cov)
TODO/FIXME:  ZERO in .rs files
ring:        ELIMINATED
sysinfo:     OPTIONAL (Linux: /proc; non-Linux: sysinfo)
Stubs:       Feature-gated behind dev-stubs
```

---

## Remaining Debt (Prioritized)

| Priority | Item | Status |
|----------|------|--------|
| P1 | Coverage to 90% (~9.75pp gap) | 80.25% — wateringHole minimum met |
| P2 | Wire `data.*` and `nat.*` semantic routes | Pending |
| P3 | `#[allow(dead_code)]` reduction (~95 remaining) | Incremental |
| P4 | Multi-filesystem substrate testing | Infra-dependent |
| P4 | Cross-gate replication | Design phase |

---

## Artifacts

- **Handoff**: This file
- **Changelog**: `primals/nestgate/CHANGELOG.md` Session 8
- **Coverage**: `cargo llvm-cov --workspace --lib --summary-only`
- **Fossil record**: `wateringHole/fossilRecord/nestgate/`
