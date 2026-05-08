# BearDog v0.9.0 — Wave 88: Root Doc Refresh, Port Alignment Sweep & Debris Cleanup

**Date**: May 5, 2026
**Primal**: BearDog (security)
**Wave**: 88
**Status**: Complete — all CI gates green (clippy 0 warnings, 12,610 tests passing, fmt clean)

---

## Changes

### Root Documentation Refresh

All root docs updated to May 5, 2026:

- `README.md` — date, TCP example port 9900→9100
- `STATUS.md` — date, Wave 86-87 entries added
- `CHANGELOG.md` — Wave 86-87 entries added (TCP port alignment, crossterm 0.29, typed config errors)
- `ROADMAP.md` — date (2 locations)
- `ARCHITECTURE.md` — date (2 locations)
- `CONTEXT.md` — date
- `START_HERE.md` — date, TCP example port 9900→9100
- `SECURITY.md` — date
- `docs/README.md` — date
- `docs/references/ROOT_INDEX.md` — date (2 locations)
- `docs/PRIMAL_CONTRACTS.md` — date (2 locations)

### Port Alignment Sweep (9900→9100 TCP, 9090→9190 metrics)

**TCP IPC default (9900→9100)** — doc comments updated:
- `crates/beardog-cli/src/lib.rs` — `--listen` example
- `crates/beardog-tunnel/src/multi_transport_server.rs` — module doc
- `crates/beardog-tunnel/src/tcp_ipc/mod.rs` — usage example
- `docs/references/QUICK_START_ZERO_HARDCODING.md` — table default

**Metrics port (9090→9190)** — aligned to `DEFAULT_METRICS_PORT = 9190`:
- `crates/beardog-types/src/canonical/config/network.rs` — doc comment
- `crates/beardog-types/src/canonical/config/runtime_config.rs` — doc comments (3 locations)
- `crates/beardog-types/src/constants/domains/PORT_PHILOSOPHY.md` — example
- `configs/env-template.example` — `BEARDOG_METRICS_PORT`, `BEARDOG_PROMETHEUS_PORT`
- `configs/network-discovery.env.template` — 4 port references
- `specs/UNIFIED_CONFIGURATION_ARCHITECTURE.md` — config example
- `showcase/03-production-features/04-monitoring-integration/` — `demo.toml` + `README.md` (7 occurrences)

**Not changed (intentional)**:
- `beardog-types/src/constants/mod.rs::METRICS_PORT = 9090` — well-known Prometheus convention port (like `POSTGRESQL_PORT = 5432`), not BearDog's configured default
- Test fixtures with `metrics_port: 9090` — arbitrary test values, not default assertions
- `server.rs` test cases with port 9900 — tests explicit user-specified port passthrough, not defaults
- `coordination.rs` `last_seen: 9900` — timestamp, not port

### Debris Cleanup

- `configs/env-template.example` — `BEARDOG_SERVICE_VERSION` corrected from `3.0.0` to `0.9.0`
- `crates/beardog-types/CONFIGURATION_MIGRATION.md` — version corrected from `v3.1.0` to `v0.9.0`
- `crates/beardog-integration/README.md` — broken handoff file reference replaced with generic `infra/wateringHole/handoffs/` pointer

### Debris Audit (no action needed)

- **Shell scripts**: 28 in `showcase/`, all demo runners — not stale, expected layout
- **Archive directories**: None found
- **`.bak/.old/.tmp` files**: None found
- **CI workflows**: 2 files, Rust-only, no Node.js — Node 20 concern does not apply
- **Dockerfile**: `rust:1.93-slim`, `version=0.9.0` — current
- **Excluded crates**: `crates/beardog`, `crates/beardog-integration`, `crates/beardog-deploy` — documented exclusions, not orphans

---

## Ecosystem Notes

- `beardog-types/src/constants/mod.rs::METRICS_PORT` stays at 9090 (Prometheus convention). BearDog's actual default is `DEFAULT_METRICS_PORT = 9190` in `beardog-config`.
- Historical test counts in STATUS/ROADMAP/CHANGELOG (14,928+, 14,786+, etc.) are time-capsule entries — they record the count at that wave, not the current total.

---

## Validation

| Gate | Result |
|------|--------|
| `cargo check --workspace` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo test --workspace` | 12,610 passing, 0 failures |
| `cargo fmt --check` | Clean |
