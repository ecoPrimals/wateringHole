<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# SweetGrass v0.7.27 — IPC Stability, Deep Debt Cleanup, Coverage Expansion

**Date**: April 11, 2026
**From**: SweetGrass
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,245 tests, 0 clippy/fmt/doc warnings, cargo deny fully clean

**Supersedes**: `SWEETGRASS_V0727_BTSP_PHASE2_DEEP_DEBT_SWEEP_HANDOFF_APR09_2026.md`

---

## Summary

Two-phase session addressing downstream `primalSpring` audit findings on
Provenance Trio (rhizoCrypt + loamSpine + sweetGrass) IPC stability, followed
by comprehensive deep debt cleanup. Springs reported intermittent UDS
connection failures and TCP-only HTTP; both resolved.

---

## Phase 1 — Trio IPC Stability (primalSpring Audit Response)

### Problem

Springs (wetSpring PG-02, ludoSpring, healthSpring) reported:
- sweetGrass UDS socket added, but intermittent connection failures under load
- TCP JSON-RPC not starting by default (compliance matrix: "HTTP-only TCP")
- No `--port` flag for UniBin standard compliance

### Root Causes Found

1. **Missing `flush()` on UDS writer** — `handle_uds_connection_raw` wrote responses via `write_all()` but never flushed. Under concurrent load, buffered writes caused client-side timeouts.
2. **Missing `flush()` on TCP writer** — same pattern in `handle_tcp_connection_raw`.
3. **TCP_NODELAY not set** — Nagle's algorithm adding latency to small JSON-RPC frames.
4. **`--port` was `Option<u16>`** — TCP JSON-RPC only started when explicitly provided.

### Fixes Applied

| File | Change | Impact |
|------|--------|--------|
| `uds.rs` | `writer.flush().await?` after every response | Eliminates intermittent failures |
| `tcp_jsonrpc.rs` | `writer.flush().await?` + `stream.set_nodelay(true)` in accept loop | TCP stability + lower latency |
| `bin/service.rs` | `--port` changed to `u16` with `default_value = "0"` | TCP JSON-RPC always starts |

### Verification

- New concurrent UDS load test: 8 clients × 5 requests, all responses received
- All 1,245 tests pass including existing e2e, chaos, and fault injection suites

---

## Phase 2 — Deep Debt Cleanup

### Smart File Refactoring

Not just splitting — semantically meaningful extraction of test modules:

| File | Before | After | Method |
|------|--------|-------|--------|
| `uds.rs` | 866 lines | 468 lines | Tests → `uds/tests.rs` via `#[path]` |
| `traversal.rs` | 766 lines | 256 lines | Tests → `traversal/tests.rs` via directory module |
| Max file size | 862 lines | 734 lines | `server/tests.rs` now largest |

### Demo Error Type Evolution

- `Box<dyn std::error::Error>` → `DemoError` enum with `thiserror`
- 5 typed variants: Store, Factory, Query, Compression, Json

### Security Advisory Resolution

| Crate | Old | New | Advisory |
|-------|-----|-----|----------|
| `time` | 0.3.44 | 0.3.47 | Stack exhaustion (RUSTSEC) |
| `rustls-webpki` | 0.103.8 | 0.103.11 | CRL distribution point (RUSTSEC-2026-0049) |

`cargo deny check` now fully clean: `advisories ok, bans ok, licenses ok, sources ok`

### New Test Coverage

- 6 CLI integration tests (capabilities, socket, --version, --help, invalid subcommand, server --help)
- 1 concurrent UDS load test (8 clients × 5 requests)

### Verified Already Clean (No Changes Needed)

- Zero `TODO`/`FIXME`/`HACK`/`unimplemented!`/`todo!` in production code
- All mocks gated behind `#[cfg(any(test, feature = "test"))]`
- No hardcoded primal names in production — only self-knowledge constants
- No hardcoded ports — all configurable via env/CLI
- Public APIs already use `impl Into<String>`, `impl AsRef<str>`, `&str`
- Zero unsafe code (`#![forbid(unsafe_code)]` workspace-level)

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,238 | 1,245 |
| Max file size | 862 | 734 |
| LOC | 44,036 | 44,069 |
| cargo deny | 2 advisories | clean |
| Line coverage | ~86% | 86.9% |
| Clippy warnings | 0 | 0 |
| Fmt issues | 0 | 0 |
| Doc warnings | 0 | 0 |

---

## Ecosystem Impact

### For Springs (wetSpring, ludoSpring, healthSpring)

- UDS connections are now reliable under concurrent load
- TCP JSON-RPC always available (OS-assigned port when `--port` omitted)
- `provenance.sock` capability-domain symlink created at UDS bind time

### For Compliance Matrix

These compliance matrix entries should be updated:

| Matrix Entry | Old | New |
|--------------|-----|-----|
| sweetGrass `--port` | "No `--port` (HTTP-only TCP)" | `--port` flag with default 0 (always starts) |
| sweetGrass TCP | "HTTP-only (Axum), not newline JSON-RPC" | Newline-delimited TCP JSON-RPC + HTTP JSON-RPC |
| sweetGrass UDS | "UDS socket added, intermittent" | UDS stable with flush + concurrent test |
| sweetGrass domain symlink | "No domain symlink" | `provenance.sock -> sweetgrass.sock` |

### For Trio Partners (rhizoCrypt, loamSpine)

Both should adopt the same flush-on-write pattern if not already applied.
The concurrent load test pattern (`8 clients × 5 requests`) can be reused.

---

## Remaining Known Gaps

1. **Postgres store coverage** — requires CI with Docker Postgres; 3% coverage is CI-only
2. **BTSP server coverage** — requires running BearDog security provider for integration test
3. **Coverage target** — 86.9% line; 90%+ achievable once Postgres CI and BTSP mock are in place

---

## Files Changed

```
crates/sweet-grass-service/src/uds.rs              (flush + test extraction)
crates/sweet-grass-service/src/uds/tests.rs         (NEW: extracted + concurrent load)
crates/sweet-grass-service/src/tcp_jsonrpc.rs       (flush + TCP_NODELAY)
crates/sweet-grass-service/src/bin/service.rs       (--port default 0)
crates/sweet-grass-service/tests/cli_bin.rs         (NEW: 6 CLI integration tests)
crates/sweet-grass-service/examples/demo.rs         (DemoError enum)
crates/sweet-grass-query/src/traversal/mod.rs       (test extraction)
crates/sweet-grass-query/src/traversal/tests.rs     (NEW: extracted tests)
Cargo.lock                                          (time, rustls-webpki updates)
README.md, CHANGELOG.md, CONTEXT.md                 (metrics refresh)
DEVELOPMENT.md, QUICK_COMMANDS.md, ROADMAP.md       (test count update)
showcase/00_START_HERE.md                           (test count update)
```
