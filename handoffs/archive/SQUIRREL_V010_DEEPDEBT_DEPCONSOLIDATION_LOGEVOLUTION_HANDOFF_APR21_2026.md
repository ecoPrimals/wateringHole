# Squirrel v0.1.0 — Deep Debt: Dependency Consolidation + Log Evolution

**Date**: April 21, 2026
**From**: Squirrel v0.1.0-alpha.52+
**Session**: AE — comprehensive audit + execution

## Scope

Full eight-dimensional deep debt audit followed by targeted execution on all
actionable findings.

## Audit Results

| Dimension | Status | Detail |
|-----------|--------|--------|
| Large files (>800L) | **Clean** | Zero production files over threshold |
| Unsafe code | **Clean** | Zero `unsafe` blocks in production |
| `#[allow]` without reason | **Clean** | One justified `#[allow(dead_code, reason)]` |
| TODO/FIXME/HACK | **Clean** | Zero markers in codebase |
| Mocks in production | **Clean** | All 3 mock modules gated `#[cfg(test)]` |
| Hardcoded primal names | **Evolved** | See log evolution below |
| Dependencies | **Consolidated** | See dependency cleanup below |
| `cargo deny` | **Passing** | advisories ok, bans ok, licenses ok, sources ok |

## Dependency Consolidation

### Eliminated from Cargo.lock

- **`directories`** crate → replaced with `dirs` (already in workspace)
- **`test-context`** — dead dev-dep (declared in `squirrel` main but never imported)

### Workspace Alignment

6 crates migrated from pinned version strings to `workspace = true`:

| Crate | Dependencies aligned |
|-------|---------------------|
| `squirrel-cli` | `clap`, `uuid`, `tokio`, `serde`, `serde_json`, `toml`, `thiserror`, `tracing`, `tracing-subscriber`, `dirs` |
| `squirrel-mcp-config` | `serde`, `serde_json`, `toml`, `thiserror`, `tracing`, `uuid`, `dirs` |
| `universal-patterns` | `futures`, `dirs` |
| `ecosystem-api` | `futures` |
| `squirrel-context` | `glob` |
| `squirrel` (main) | removed `test-context` |

## Log / Description Evolution

Remaining "biomeOS" hardcoded strings evolved to capability-neutral:

| File | Before | After |
|------|--------|-------|
| `lifecycle.rs` | `"Registered with biomeOS at ..."` | `"Registered with ecosystem orchestrator at ..."` |
| `lifecycle.rs` | `"heartbeat sent to biomeOS"` | `"heartbeat sent to ecosystem orchestrator"` |
| `lifecycle.rs` | `"biomeOS may be down"` | `"orchestrator may be down"` |
| `main.rs` | `"Registered with biomeOS"` | `"Registered with ecosystem orchestrator"` |
| `main.rs` | `"No biomeOS socket found"` | `"No ecosystem orchestrator socket found"` |
| `niche.rs` | `"biomeOS lifecycle: ..."` | `"Ecosystem lifecycle: ..."` |
| `optimized_implementations.rs` | `"biomeOS/v1"` | `"ecosystem/v1"` |
| `registry.rs` | `"biomeos_socket_registry"` | `"ecosystem_socket_registry"` |

### Not Changed (wire/filesystem compat)

- `API_VERSION` in `biomeos_integration/mod.rs` — wire protocol version sent to orchestrator
- Filesystem paths (`/run/user/{uid}/biomeos/`) — ecosystem-wide IPC convention
- `BIOMEOS_SOCKET_DIR`, `BIOMEOS_SOCKET_NAME` — on-disk layout constants
- Legacy env var fallbacks (`BIOMEOS_*`) — backward compatibility chains

## Debris Review

| Category | Finding |
|----------|---------|
| Scripts (`.sh`, `.py`) | Zero |
| Temp files (`.tmp`, `.bak`, `.orig`) | Zero |
| Log files | Zero |
| Build artifacts outside `target/` | Zero |
| Stale TODO/FIXME | Zero |
| Tracked secrets | Zero (`.env`, `mcp-config.env` in `.gitignore`, untracked) |

## Metrics

- **7,167** tests passing (0 failures)
- **~1,032** `.rs` files, **~335k** lines
- **90.1%** region coverage
- `cargo clippy` pedantic+nursery: zero warnings
- `cargo deny check`: all four checks passing

## Root Docs Updated

- `README.md`: test count 7,165→7,167, removed stale HTTP feature-gated line, "biomeOS lifecycle" → "ecosystem lifecycle"
- `CONTEXT.md`: test count 7,165→7,167, "biomeOS lifecycle" → "ecosystem lifecycle"
- `CHANGELOG.md`: dep consolidation + log evolution entries added
- `CURRENT_STATUS.md`: session AE entry added
- `CRYPTO_MIGRATION.md`: date bumped to April 21

## Blocked Items (unchanged)

- Three-tier genetics: blocked on `ecoPrimal >= 0.10.0`
- BLAKE3 content curation: blocked on NestGate content-addressed storage API
- Phase 3 cipher negotiation: blocked on BearDog `btsp.negotiate` server-side
