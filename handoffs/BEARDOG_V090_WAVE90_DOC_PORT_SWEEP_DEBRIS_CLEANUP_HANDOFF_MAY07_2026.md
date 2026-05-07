# BearDog v0.9.0 — Wave 90: Doc Consistency Sweep, Port Alignment Completion & Debris Cleanup

**Date**: May 7, 2026
**Primal**: BearDog (security)
**Wave**: 90
**Status**: Complete — all CI gates green

---

## Changes

### Doc Consistency Fixes

- `docs/references/ENVIRONMENT_VARIABLES.md` — footer date May 5 → May 7
- `docs/PRIMAL_CONTRACTS.md` — method total "100 JSON-RPC methods" → "103 JSON-RPC methods (98 CryptoHandler + 5 IonicBondHandler)"
- `ROADMAP.md` line 145 — IonicBondHandler count corrected from 9 → 5 (was wrong even historically)
- `ROADMAP.md` line 47 — removed stale test count from stadial parity gate bullet (was 14,928+ from Wave 53 era, conflicted with canonical 12,610)
- `crates/beardog-types/README.md` — version "v3.0.0" → "v0.9.0"

### Port Alignment Completion (9090 → 9190 metrics)

Second pass catching remaining 9090 references missed in Wave 88:

**Source code:**
- `crates/beardog-types/src/constants/domains/network/defaults.rs` — doc comment "fallback to 9090" → "9190"
- `crates/beardog-types/src/constants/domains/network/addresses.rs` — `DEFAULT_METRICS_BIND` constant `"0.0.0.0:9090"` → `"0.0.0.0:9190"`, doc comment updated

**Config templates:**
- `configs/network-discovery.env.template` — `BEARDOG_METRICS_PORT=9090` → `9190` (this was a half-update: URL was already 9190 but port was still 9090)
- `configs/production.toml` — `metrics_bind_address` 9090 → 9190
- `configs/beardog-config.toml` — metrics port 9090 → 9190, prometheus port 9090 → 9190
- `configs/network-defaults.toml` — `allowed_ports` list updated (added 9100 TCP IPC, changed 9090 → 9190)

**Not changed (intentional):**
- `beardog-types/src/constants/mod.rs::METRICS_PORT = 9090` — well-known Prometheus convention (like POSTGRESQL_PORT = 5432)
- `configs/SOVEREIGNTY_COMPLIANT_CONFIG_GUIDE.md` — 9090 refs are external compute/toadstool service endpoints, not BearDog metrics
- `#[deprecated(since = "3.1.0")]` annotations — Rust API migration metadata, ~50 locations, changing would be disruptive with no functional benefit
- Historical wave entries in STATUS/CHANGELOG — time-capsule records
- `specs/` directory — treated as reference/archive material, refreshed on demand

### Debris Audit Results

| Category | Finding |
|----------|---------|
| TODO/FIXME/HACK in .rs | **0** |
| TODO in .md | Only in `specs/` pseudocode examples (intentional placeholders) |
| Orphan configs | `configs/network-defaults.toml`, `configs/env-template.example` — unreferenced but useful as templates |
| Empty files | None found |
| Stale handoff refs | None (cleaned in Wave 88) |
| Stale `async_trait` claims | Only historical wave entries and `specs/` archive |

---

## Validation

| Gate | Result |
|------|--------|
| `cargo check --workspace` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo fmt --check` | Clean |
| Network tests (beardog-types) | 320 passing |
