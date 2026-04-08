# NestGate v4.7.0-dev — Ancestral Overstep Audit, Deep Debt Evolution & Coverage Push

**Date**: March 31, 2026  
**Primal**: nestgate (storage & permanence)  
**Session type**: Multi-phase deep debt execution — ancestral overstep audit, production mock evolution, hardcoding elimination, zero-copy patterns, targeted coverage push, doc cleanup

---

## What Was Done

### Ancestral Overstep Audit (Sessions 11–12)

Full audit of NestGate's accumulated functionality that belongs to dedicated primals. Executed across all priority tiers:

| Area | Priority | Action | Status |
|------|----------|--------|--------|
| **nestgate-security** (crypto) | P0 | `CryptoDelegate` routes to bearDog IPC; local RustCrypto deps remain as fallback | Delegated, deps retained for offline |
| **nestgate-discovery** (mDNS/Consul/K8s) | P0 | Removed `mdns-sd` dep, deleted mDNS backend, 6 orphaned modules, `discovery/` dir; replaced with env-var + songBird IPC | Complete |
| **nestgate-mcp** | P0 | Removed from workspace members; `nestgate-zfs` and `nestgate-bin` deps dropped | Shed from workspace |
| **nestgate-network** (HTTP) | P1 | Partial shed done; axum retained for 2-route admin surface; orchestration delegated to songBird | Evaluated, documented |
| **nestgate-automation** | P2 | ~4k LOC evaluated; storage-specific (tiering/lifecycle) stays; generic scheduling for biomeOS delegation | Evaluated, documented |
| **nestgate-installer** (ecoBin) | P2 | Switched `rustls` from `aws-lc-rs` (C dep) to `ring` (Pure Rust); crypto provider updated | Complete |

### Production Mock Evolution (7 stubs → real implementations)

| Mock | Before | After |
|------|--------|-------|
| `get_uptime_seconds()` | `const fn` returning `0` | `OnceLock<Instant>` — real process uptime |
| Performance scores | Hardcoded `75/80/85` | Derived from `SystemMetrics` (memory, disk IOPS, network) |
| System status counts | `snapshots += 5` per engine | Real filesystem scan via `get_snapshot_count_from_engine_impl()` |
| WebSocket metrics | `load_average: 0.5`, `uptime: 3600` | Reads `/proc/loadavg` and `/proc/uptime` |
| tarpc `execute_request` | No-op `Ok(success: true)` | Honest `Err(ServiceUnavailable)` with migration guidance |
| Dashboard pool metrics | Hardcoded health/capacity | Derived from actual pool state |
| Dataset per-engine stats | Fake 1MB/1GB per dataset | Engine count only; no fabricated sizes |

### Hardcoding Elimination (5 HIGH-severity fixes)

| File | Hardcoded | Fix |
|------|-----------|-----|
| `src/cli/mod.rs` | `run(8080, "127.0.0.1", ...)` | `get_api_port()` / `get_bind_address()` from config module |
| `dataset_handlers.rs` | `/tmp/nestgate_dataset_*` | `NESTGATE_TEMP_DIR` env → `std::env::temp_dir()` fallback |
| `helpers.rs` | `/tmp/nestgate/snapshots` | `NESTGATE_DATA_DIR` env → `temp_dir()/nestgate` fallback |
| `system.rs` | `/tmp/nestgate/snapshots` | Same pattern |
| `performance_dashboard/metrics.rs` | Placeholder health/capacity | Computed from actual pool state |

### Dead Code & Coverage

- Gated `validation_predicates.rs` (550 LOC) under `#[cfg(test)]`
- Zero-copy: `bytes::Bytes` for tarpc payloads, `Arc<str>` for IPC service names
- `#[allow(dead_code)]` reduced from 115 → 97 (remaining are planned API fields/enum variants)
- **205 new tests** across 11 modules:

| Module | Tests Added | Coverage After |
|--------|-------------|----------------|
| compliance/manager.rs | 8 | ~99% |
| rpc/socket_config.rs | 10 | ~97% |
| cache/types.rs | 6 | ~95% |
| cache/multi_tier.rs | 17 | ~85% |
| performance_dashboard/metrics.rs | 12 | ~75% |
| crypto/delegate.rs | 26 | ~80% |
| zfs/health.rs | 20 | ~80% |
| workspace_management/crud.rs | 15 | ~75% |
| storage/probes.rs | 11 | ~70% |
| zfs/pool/manager.rs | 8 | ~70% |
| zfs/failover.rs | 10 | ~70% |

### Doc Cleanup

- README.md: Fixed stale test counts (1,509 → 8,384), coverage (80.25 → 80.95), ring/aws-lc-rs narrative, removed nestgate-mcp from architecture, updated discovery story, fixed compliance table
- STATUS.md: Aligned metrics with measured state
- Verified zero `// TODO`, `// FIXME`, `// HACK` in production code
- ~45 `// Placeholder` comments are intentional stubs (feature-gated or documented)

---

## Current Measured State

**NOTE**: Superseded by `NESTGATE_V470_RING_ELIMINATION_CAPABILITY_SYMLINK_DOC_CLEANUP_HANDOFF_MAR31_2026.md`

```
Build:       24/24 workspace members, 0 errors
Clippy:      ZERO warnings (cargo clippy --workspace --all-features --all-targets)
Format:      CLEAN (cargo fmt --check)
Tests:       8,376 lib tests passing, 0 failures
Docs:        ZERO warnings (cargo doc --workspace --no-deps)
Coverage:    80.95% line (llvm-cov)
Max file:    879 lines
TLS/crypto:  Delegated to bearDog IPC; installer uses system curl (ring/rustls/reqwest ELIMINATED)
Discovery:   Env vars + songBird IPC (mDNS feature-gated)
MCP:         Removed from workspace (delegated to biomeOS capability.call)
```

---

## External Dependency Audit

| Dependency | Type | Status |
|------------|------|--------|
| `ring` | C/asm crypto (rustls in installer) | Only non-pure-Rust crypto; no pure-Rust TLS provider available yet |
| `inotify-sys` | Linux FFI (via notify) | Required for filesystem monitoring |
| `libc` | System FFI (via tokio, uzers) | Unavoidable for system programming |
| `openssl` / `aws-lc-rs` / `native-tls` | — | NOT in dependency tree |
| `-sys` crates | — | Only `linux-raw-sys` (rustix ABI defs) + `inotify-sys` |

---

## Remaining Debt (Prioritized)

| Priority | Item | Status |
|----------|------|--------|
| P1 | Coverage to 90% (~9pp gap, ~14k test lines) | 80.95% — multi-session effort |
| P1 | Complete crypto shed (remove local RustCrypto deps, fully delegate to bearDog) | CryptoDelegate wired; local deps remain as fallback |
| P2 | Wire `data.*` and `nat.*` semantic routes | Pending |
| P2 | Consolidate `// Placeholder` stubs (~45 across 31 files) | Intentional; evolve as features land |
| P3 | `#[allow(dead_code)]` reduction (97 remaining) | Planned API fields, enum variants |
| P3 | nestgate-automation: delegate generic scheduling to biomeOS | Storage-specific stays |
| P4 | Multi-filesystem substrate testing | Infra-dependent |
| P4 | Cross-gate replication | Design phase |

---

## Artifacts

- **Handoff**: This file
- **README**: `primals/nestgate/README.md` (updated)
- **Status**: `primals/nestgate/STATUS.md` (updated)
- **Coverage**: `cargo llvm-cov --workspace --lib --summary-only`
- **Fossil record**: `wateringHole/fossilRecord/nestgate/`
