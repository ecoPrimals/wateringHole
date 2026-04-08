<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# loamSpine — v0.9.15 Deep Debt & Evolution Handoff

**Date**: March 31, 2026
**Version**: 0.9.14 → 0.9.15
**Priority**: Informational — all blockers resolved
**Cross-reference**: LS-03 (resolved), `specs/DEPENDENCY_EVOLUTION.md`

---

## Summary

Comprehensive deep debt resolution session covering critical bug fix, deprecated API
removal, self-knowledge enforcement, dependency optimization, and +85 new tests bringing
coverage to 93.96% line / 92.60% region.

## Critical Fix: LS-03 Startup Panic (RESOLVED)

- **Root cause**: `tokio::runtime::Runtime::new()?.block_on()` inside already-running
  async context in `infant_discovery.rs`.
- **Fix**: Replaced with `tokio::spawn` — single-line change.
- **Validation**: `loamspine server` starts cleanly, provenance trio pipeline unblocked.
- **Supersedes**: `LOAMSPINE_STARTUP_PANIC_HANDOFF_MAR31_2026.md` (P1 Critical → Resolved).

## Changes

### API Evolution
- **`--port` flag**: Added as alias for `--jsonrpc-port` per UniBin CLI standard.
- **Deprecated API removal**: `discover_from_songbird`, `advertise_to_songbird`,
  `heartbeat_songbird`, `advertise_loamspine` and all tests removed.
- **Config cleanup**: `#[serde(alias = "songbird")]` on `DiscoveryMethod::ServiceRegistry` removed.

### Self-Knowledge Enforcement
- `primal_names.rs` stripped to `SELF_ID`, `BIOMEOS`, `BIOMEOS_SOCKET_DIR` only.
- External primal name constants (`SONGBIRD`, `NESTGATE`, `BEARDOG`, `TOADSTOOL`,
  `CORALREEF`, `RHIZOCRYPT`, `SWEETGRASS`, `SQUIRREL`) removed.
- Primals discover others at runtime via capability registry.

### Dependency Optimization
- **tokio features**: `"full"` → `["macros", "rt", "rt-multi-thread", "net", "io-util",
  "sync", "time", "signal"]` — faster compile times, smaller dependency footprint.
- **Dependency evolution plan**: `specs/DEPENDENCY_EVOLUTION.md` tracks `bincode v1 → v2`,
  `mdns → tokio-native`, and completed `sled → redb`.

### Test Coverage (+85 tests)
- UDS server (start, accept, stale socket, directory creation, drop, shutdown)
- Protocol-level JSON-RPC (method normalization, dispatch, tools.call, notifications, batches)
- Lifecycle (advertise, heartbeat states, state transitions)
- Discovery manifest (filesystem with tempfile/temp_env)
- CLI signer (bins directory discovery)
- Neural API (MCP tool mapping, capability list structure, socket path edges)

### Smart Refactoring
- `jsonrpc/tests.rs`: 1,136 → 610 + `tests_protocol.rs` (526 lines)

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Version | 0.9.14 | 0.9.15 |
| Tests | 1,312 | 1,397 |
| Line coverage | 92.11% | 93.96% |
| Region coverage | 90.33% | 92.60% |
| Source files | 131 | 129 |
| Max file size | 885 | 899 |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Unsafe blocks | 0 | 0 |

## Verification

```bash
cargo test --workspace --all-features    # 1,397 passing
cargo clippy --workspace --all-features --all-targets -- -D warnings  # 0 warnings
cargo fmt --all -- --check               # clean
```

## Remaining Ecosystem Work

- **Songbird references in comments/docs**: Several `.rs` files still reference Songbird
  in documentation comments (transport descriptions, architecture notes). These are accurate
  ecosystem documentation, not hardcoding — Songbird is the HTTP/TLS routing primal.
- **`service_registry_integration.rs`**: `REGISTRY_BIN` still references
  `../bins/songbird-orchestrator` — this is a test fixture for integration tests with the
  actual Songbird binary and should remain.
- **showcase/**: Contains demo scripts referencing Songbird TLS certs and startup scripts.
  These are demonstration infrastructure, not production code.
