# Songbird v0.2.1 — Wave 119: Deep Debt Elimination, Zero-Copy, Docs Cleanup

**Date**: April 6, 2026
**Primal**: songBird
**Previous**: Wave 118 (archived)

---

## Summary

Wave 119 completed the remaining deep debt items: hardcoded IPs, `/tmp` paths, hardcoded ports, production `unwrap()`/`expect()`, large file refactoring, lint hygiene, zero-copy evolution, and coverage expansion. Root docs cleaned and aligned with current metrics. Stale tooling (`tarpaulin.toml`) removed, legacy-named scripts modernized.

## Hardcoding Elimination

### IP Addresses (0 remaining in production)
- `8.8.8.8:80` in `network/binding.rs`, `app/network.rs` → `netdev::get_default_interface()` + `SONGBIRD_ROUTE_DETECT_ADDR` (RFC 5737 `192.0.2.1:80`)
- `1.1.1.1` in `ip route get` command → `192.0.2.1` (RFC 5737 TEST-NET-1)
- New shared module: `network/route_detect.rs` with IPv4/IPv6 resolution

### Socket Paths (XDG-compliant)
- `connections/{limited,full_trust,federated}.rs`: `/tmp/{peer_id}.sock` → `XDG_RUNTIME_DIR`/`TMPDIR`/`/tmp` + `biomeos/` prefix
- `env_config.rs`: shared `runtime_or_tmp_base()` + `peer_fallback_socket_path()`

### Ports (env-configurable)
- Discovery broadcast: hardcoded `2300` → `SONGBIRD_DISCOVERY_PORT` (default 2300)
- STUN bind: hardcoded `3478` → `SONGBIRD_STUN_PORT` (default 3478)
- Relay bind: hardcoded `3479` → `SONGBIRD_RELAY_PORT` (default 3479)

## Production Safety

### unwrap()/expect() Elimination
- `HttpGatewayService::Default` → `try_default()` returning `Result`
- SIGTERM signal handler: documented with `#[expect(reason)]`
- Const address parses: documented with `#[expect(clippy::expect_used, reason = "compile-time constant")]`

## File Refactoring

- `tower_atomic.rs` (990 lines) → `tower_atomic/{mod,types,server,client}.rs` (max 212L production, 519L tests)
- Public API unchanged — all re-exports via `tower_atomic/mod.rs`

## Lint Hygiene

- Remaining `#[allow(` in production CLI/config/federation/http-client/bluetooth/orchestrator → `#[expect(` with reasons
- Unfulfilled `#[expect]` attributes removed (lint doesn't fire = no suppression needed)

## Zero-Copy Evolution

- `mesh_handler`: `node_id` → `Arc<RwLock<Arc<str>>>` (per-message clone is ref-count bump)
- `punch_handler`: `HashMap<Arc<str>, PunchAttempt>`, `PunchStatus::Failed { reason: Arc<str> }`
- `rendezvous_handler`: `RendezvousRegisterParams`/`RendezvousPeer` fields → `Arc<str>`
- `capability/strategy.rs`: `provider_id` → `Arc<str>`, `search_paths` → `Arc<Vec<PathBuf>>`

## Coverage Expansion

50+ new tests across 11 modules:
- Config: `bind_and_ports`, `register`, `announcement`, `remote_probes`
- Discovery: `anonymous/protocol`
- Orchestrator: `security_crypto_client`, `auth`, `enhanced_router`, `unix_transport`, `discovery_bridge`, `tarpc_server`

## Docs & Debris Cleanup

- `tarpaulin.toml` removed (stale — project uses llvm-cov)
- `scripts/btsp-health-monitor.sh` → `scripts/health-monitor.sh` (legacy BTSP naming eliminated)
- `README.md`: metrics aligned (12,764 tests, 72.16% coverage, 519L max file, new env vars documented)
- `CONTRIBUTING.md`: coverage updated, legacy `BEARDOG_SOCKET` example → `SECURITY_PROVIDER_SOCKET`
- `CONTEXT.md`: metrics aligned
- `REMAINING_WORK.md`: stale notes removed, all metrics current

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 12,713 | 12,764 |
| Line coverage | 71.42% | 72.16% |
| Production `unwrap()` | 4 | 0 |
| Hardcoded external IPs | 3 locations | 0 |
| Hardcoded ports | 3 locations | 0 (env-driven) |
| `/tmp` fallbacks | 4 locations | 0 (XDG-first) |
| Files near 1000L | 1 (990L) | 0 (refactored to 4 files) |
| `#[allow(` in production | ~30 | ~8 (where `#[expect]` causes unfulfilled errors) |
| Stale tooling files | 1 | 0 |

## Verification

- `cargo fmt --all -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 12,764 passed, 0 failed, 252 ignored
- `cargo deny check` — advisories ok, bans ok, licenses ok, sources ok

## Remaining Work

See `REMAINING_WORK.md` for full status. Key items:
- Coverage: 72.16% → 90% target (focus on pure-logic adapter modules)
- Security provider crypto e2e validation (blocked on live provider)
- Sled → storage provider migration (blocked on NG-01)
- Platform backends (Android, iOS, WASM)
- Real hardware IGD tests
