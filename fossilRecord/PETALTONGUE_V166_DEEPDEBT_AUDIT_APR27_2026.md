# petalTongue v1.6.6 — Deep Debt Audit + Hardcoding Elimination

**Date**: April 27, 2026
**Commit**: `d2448f8`

---

## Audit Scope

Comprehensive audit of 847 `.rs` files across all 18 workspace crates + UniBin
root. Checked: file sizes, unsafe code, `dyn` usage, `unwrap()`/`expect()` in
production, `#[allow(]`, `TODO`/`FIXME`/`HACK`, clone storms, `pub String`
fields, dependency version skew, lockfile duplication, hardcoded values, mock
isolation, feature flag hygiene.

## Clean Findings (no action needed)

| Dimension | Status |
|-----------|--------|
| `unsafe` code | Zero across all crates |
| `dyn` trait objects (production) | Zero (only in doc comments) |
| `#[allow(]` in production | Zero (only in `#[cfg(test)]` modules) |
| `TODO`/`FIXME`/`HACK`/`XXX` | Zero |
| Files >650 lines | Zero (largest: 646L) |
| `todo!()`/`unimplemented!()` | Zero in production |
| Mocks in production | All gated behind `#[cfg(test)]` or `test-fixtures` feature |
| Production `unwrap()` | Zero (all in test code) |
| Production `expect()` | One justified with `#[expect]` attribute (`retry.rs`) |
| Production `panic!()` | Zero |
| Clone storms | `graph_validation/structure.rs` (26) is entirely test setup |

## Fixes Applied

### Dependency Consolidation

- **`tempfile`**: unified 3.8/3.10/3 version skew across 8 crates to single
  workspace dep (`3.10`)
- **`clap`**: `petal-tongue-cli` was standalone `4.5` without `env` feature —
  now uses workspace dep (gains `env` feature consistency)

### Magic Number Extraction

| Before | After | File |
|--------|-------|------|
| `viewBox="0 0 800 600"` | `SVG_VIEWPORT_WIDTH`/`SVG_VIEWPORT_HEIGHT` | `svg.rs` |
| `Duration::from_secs(15)` | `DEFAULT_SSE_KEEPALIVE_SECS` | `web_mode.rs` |
| `Duration::from_secs(600)` | `DEFAULT_SSE_STREAM_TIMEOUT_SECS` | `sse.rs` |
| `"web/static"` | `WEB_STATIC_DIR` | `web_mode.rs` |
| (new) | `DEFAULT_SVG_WIDTH`/`DEFAULT_SVG_HEIGHT` | `constants/display.rs` |

### Lockfile Duplication (non-actionable)

Transitive duplication identified but not controllable in petalTongue:
`hashbrown` (5 versions), `windows-sys` (4), `getrandom` (3), `thiserror`
(1.0/2.0), `syn` (1/2), `tower` (0.4/0.5), `rustix` (0.38/1.x).

## Pass 2: Dependency Consolidation + Discovery Evolution (April 27)

### Dependency Consolidation

| Crate | Dep | Before | After |
|-------|-----|--------|-------|
| petal-tongue-core | `toml` | `"0.8"` | `{ workspace = true }` |
| petal-tongue-tui | `tokio-util` | `"0.7"` | `{ workspace = true }` (gains `codec`) |
| petal-tongue-core | `rustix` | `"0.38"` per-crate | `{ workspace = true, features = [...] }` |
| petal-tongue-ui | `rustix` | `"0.38"` per-crate | `{ workspace = true, features = [...] }` |
| root dev-dep | `tempfile` | `"3.10"` | `{ workspace = true }` |

### Stale Feature Removal

- `external-display` feature alias in `petal-tongue-ui`: zero `cfg` references in `.rs` files.
  Removed.

### Discovery Evolution

- `universal_discovery.rs`: socket search paths now include `XDG_RUNTIME_DIR`
  (`/run/user/{uid}`) as priority-1, matching `unix_socket_provider.rs` pattern.
  Previously only searched `/tmp` and `/var/run`, missing the standard biomeOS
  socket location.

## Verification

- 0 clippy warnings (workspace, all-features)
- 6,156+ tests passing, 0 failures
- macOS aarch64 cross-check clean
- Edition 2024, stable toolchain
