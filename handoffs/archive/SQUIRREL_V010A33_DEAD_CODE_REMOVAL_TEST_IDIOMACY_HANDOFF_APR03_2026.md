<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.33 — Dead-Code Removal, Test Idiomacy, Concurrency Model (2026-04-03)

## Summary

Comprehensive codebase hygiene session: removed ~66k lines of orphan dead code from
`squirrel-mcp`, fixed test concurrency patterns, evolved `CommandRegistry` from
`Mutex` to `RwLock`, and cleaned remaining Songbird name-coupling in doc comments.

## Changes

### Dead-code removal (65,910 lines / 246 files)

`squirrel-mcp` had ~246 `.rs` files that existed on disk but were **never compiled** —
not declared in any `mod.rs`. Entire orphan module trees removed:

- `observability/` (47 files, 12.4k lines)
- `tool/` (42 files, 10.3k lines)
- `resilience/` orphans beyond the 3 compiled modules (36 files, 10.6k lines)
- `transport/` orphans — TCP, memory, stdio, tests (13 files, 5k lines)
- `protocol/` orphans — adapter, loose test files (14 files, 4.1k lines)
- `monitoring/`, `plugins/`, `integration/`, `sync/`, `context_manager/`, `client/`,
  `session/`, `server/`, `port/`, `message/`, `registry/`, `message_router/`,
  `context_adapter/` (all entirely orphan)
- 12 root-level `.rs` files (metrics, compression, web_integration, etc.)

All preserved in git history as fossil record.

### Test idiomacy

- **IPC client timeout**: 60s `tokio::time::sleep` → `std::future::pending()` (zero wasted time)
- **Context adapter TTL**: 3s → 2.1s sleep with 1s TTL (saves ~1s per run)
- **Learning integration**: 120ms → 50ms background sync wait
- Full sleep audit: all `thread::sleep` in compiled code confirmed legitimate (sync tests,
  wall-clock); all `tokio::time::sleep` confirmed necessary (rate limiter, chaos, alerting)

### Concurrency model

- `CommandRegistry`: `Arc<Mutex<>>` → `Arc<RwLock<>>` for `commands` and `resources`
  (read-heavy maps); `execute` signature `&Vec<String>` → `&[String]`

### Doc comment cleanup

- Generalized remaining Songbird references in `orchestration_adapter.rs`,
  `orchestration/mod.rs`, `mcp_core_only.rs`, `discovery/mod.rs`,
  `discovery/self_knowledge.rs`, `universal.rs` AI adapter, `niche.rs`
- Fixed stale path reference in `primal_pulse/mod.rs`
- Updated `CONTEXT.md` file/line counts and version

## Verification

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace --all-features` | 7,165 passed, 0 failed, 110 ignored |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Metrics

| Metric | Before (alpha.32) | After (alpha.33) |
|--------|-------------------|-------------------|
| `.rs` files | ~1,250 | 1,004 |
| Lines of Rust | ~408k | ~342k |
| Tests | 7,165 | 7,165 (unchanged — removed code was never compiled) |
| Clippy warnings | 0 | 0 |

## Remaining debt

- ~325 `songbird` references remain in code — all classified as acceptable
  (`primal_names` constants for logging, `#[deprecated]` attributes, `#[serde(alias)]`
  for backward compat, env-var fallback chains, migration history comments)
- `v0.2.0` / `v0.3.0` tracking comments are valid roadmap markers
- No `TODO` / `FIXME` / `HACK` / `todo!()` / `unimplemented!()` in codebase
