# Squirrel v0.10 — Doc Reconciliation & Debris Review (April 20, 2026 — Consolidated)

## Root Doc Updates

| File | Change |
|------|--------|
| `README.md` | File count → ~1,032, lines → ~335k |
| `CONTEXT.md` | Same metric updates |
| `CHANGELOG.md` | Updated [Unreleased] summary with cross-arch fix, orphan removal, env var evolution; file/line counts corrected |
| `CURRENT_STATUS.md` | Added session AC entry (cross-arch, env evolution, orphan removal) |
| `CONTRIBUTING.md` | Removed stale "Optional HTTP API via axum" reference (eliminated in stadial gate) |
| `docs/CRYPTO_MIGRATION.md` | Removed stale `rustls` TLS entry (eliminated); fixed ecoBin ban list; corrected migration path items |

## Debris Review Results

| Category | Count | Details |
|----------|-------|---------|
| Scripts (`.sh`/`.py`/`.js`/`.bash`) | **0** | None in tree |
| Temp/backup files (`.bak`/`.orig`/`.tmp`/`.swp`/`~`) | **0** | None |
| Log files | **0** | None outside `target/` |
| `.env` | 1 | Untracked, `.gitignore` covers it |
| Stale config | **0** | `tarpaulin.toml` was deleted in previous session |
| `TODO`/`FIXME`/`HACK` in `.rs` | **0** | 11 false positives: `TaskStatus::Todo` (enum variant), `"timing hacks"` (test comments), `"sk-xxx"` (placeholder keys), `"-32xxx"` (JSON-RPC doc) |
| `TODO`/`FIXME` in docs | **0** | All references are policy statements ("no TODOs") or historical changelog entries |
| `EVOLUTION:`/`Phase 2`/`DEFERRED` markers | ~39 files | All are valid deferred-work documentation for upstream-blocked items (genetics, BLAKE3 curation, Phase 3 cipher) |

## Stale Doc Fixes Applied

1. **`CRYPTO_MIGRATION.md`**: `rustls` removed from crypto table (eliminated in stadial gate, not just moved to feature). ecoBin ban list updated to include `rustls`. Migration path corrected: no HTTP clients remain.
2. **`CONTRIBUTING.md`**: Architecture section removed "Optional HTTP API via axum" — all HTTP features were removed during stadial gate enforcement.
3. **`CHANGELOG.md`**: [Unreleased] summary line updated from `~1,039` to `~1,032` files, added cross-arch fix and env var evolution entries.

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,165 |
| Coverage | 90.1% |
| `.rs` files | ~1,032 |
| Lines | ~335k |
| Production files >800L | 0 |
| `unsafe` blocks | 0 |
| `TODO`/`FIXME`/`HACK` | 0 |
| `#[allow()]` in production | 1 (justified) |
| Scripts in tree | 0 |
| Temp/debris files | 0 |
| `cargo clippy -- -D warnings` | 0 warnings |
| `cargo fmt -- --check` | clean |

## Upstream Blocks (unchanged)

- Three-tier genetics: awaits `ecoPrimal >= 0.10.0` (`mito_beacon_from_env()`)
- BLAKE3 content curation: awaits NestGate content-addressed storage API
- Phase 3 cipher negotiation: awaits BearDog server-side
