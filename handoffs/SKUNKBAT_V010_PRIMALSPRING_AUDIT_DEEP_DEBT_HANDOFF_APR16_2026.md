<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# skunkBat v0.1.0 — primalSpring Audit, Deep Debt Evolution

**Date**: April 16, 2026
**Previous**: (first handoff)

---

## Session Summary

Comprehensive primalSpring audit and deep debt execution across the full skunkBat
codebase. Two phases: (1) audit of specs, code, docs, and wateringHole compliance;
(2) systematic execution on all findings — clippy pedantic/nursery cleanup,
`#[allow]` → `#[expect(reason)]` migration, magic number elimination, JSON-RPC
batch + notification support, large function refactoring, cross-platform evolution,
test coverage expansion, and showcase/documentation cleanup.

## Build

| Metric | Value |
|--------|-------|
| Tests | 149 passing / 0 failures / 14 ignored (external-primal-gated) |
| Coverage | 81.9% line (cargo-llvm-cov; target: 90%) |
| Clippy | CLEAN — pedantic + nursery, `-D warnings`, zero warnings |
| Format | PASS |
| Docs | PASS — zero warnings |
| Deny | PASS — advisories ok, bans ok, licenses ok, sources ok |
| Unsafe | `forbid(unsafe_code)` workspace-wide |
| Files | 20 `.rs` production files, 6,000 lines total, max 719 lines |
| Edition | 2024 |
| License | AGPL-3.0-or-later (scyBorg triple-copyleft) |

## Changes

### JSON-RPC 2.0 Full Spec Compliance

Server now handles all three JSON-RPC message types:
- **Single requests** with standard error codes (-32700 through -32603)
- **Batch requests** — JSON array dispatch with per-spec error handling
- **Notifications** — id-less requests produce no response (§4.1)

`Request.id` changed from `serde_json::Value` to `Option<serde_json::Value>`.
Added `is_notification()` (const fn) and `id_or_null()` helpers.
`handle_connection` rewritten with `handle_single` and `handle_batch` helpers.
Server tests expanded from 0% to 86% coverage.

### `#[allow]` → `#[expect(reason)]` Migration

All `#[allow(...)]` attributes across the workspace converted to
`#[expect(..., reason = "...")]` with human-readable justifications:
- `dead_code` → "reserved for BTSP Phase 2 cipher scoping"
- `struct_excessive_bools` → "feature flags are naturally boolean"
- `cast_precision_loss` → "observation counts fit in f64"
- `unused_async` → "async signature for trait consistency/future implementation"
- `result_large_err` → "Response is the natural error for validation"
- `unreachable_pub` → "transport types used by main.rs via re-export"
- `float_cmp` → "exact literal comparison in test"
- `too_many_lines` → "self-contained demo" (examples only)

### Magic Number Elimination

All hardcoded thresholds replaced with named constants:

| Constant | Value | Location |
|----------|-------|----------|
| `DEFAULT_SIGMA_THRESHOLD` | 2.5 | threats/mod.rs |
| `SEVERITY_MODERATE_DEVIATION` | 5.0 | threats/mod.rs |
| `SEVERITY_CRITICAL_DEVIATION` | 3.0 | threats/mod.rs |
| `DOS_LOAD_THRESHOLD` | 0.9 | threats/mod.rs |
| `DOS_HIGH_CONFIDENCE` | 0.8 | threats/mod.rs |
| `CRITICAL_CONFIDENCE_THRESHOLD` | 0.9 | defense/mod.rs |
| `HIGH_CONFIDENCE_THRESHOLD` | 0.7 | defense/mod.rs |
| `DEFAULT_TIMEOUT_MS` | 5000 | songbird.rs, toadstool.rs |
| `DEFAULT_PORT` | 9140 | main.rs |

### Large Function Refactoring

`perform_server_handshake` (107 lines, too-many-arguments) decomposed into:
- `HandshakeState` struct for parameter grouping
- `btsp_exchange_hello` — initial hello exchange
- `btsp_read_challenge_response` — challenge/response read
- `btsp_verify_and_complete` — verification and completion

### Cross-Platform Evolution

Two production stubs evolved to real implementations:
- `check_system_load()` — reads `/proc/loadavg` on Linux, `uptime` fallback
- `proc_uid()` — reads `/proc/self/status` on Linux, `id -u` fallback

### Tokio Feature Trimming

Workspace `tokio` dependency reduced from `features = ["full"]` to selective:
`rt-multi-thread`, `net`, `io-util`, `sync`, `macros`, `time`, `fs`, `process`, `signal`.

### Integrations Cleanup

- Removed unused feature flags (`toadstool-integration`, `songbird-integration`, `full`)
  from `skunk-bat-integrations` — none were gated with `#[cfg(feature)]`
- Fixed broken intra-doc links in `songbird.rs` and `toadstool.rs`

### Showcase Debris Cleanup

Removed 19 empty scaffold directories from showcase (old layout artifacts):
- 3 top-level orphans (`03-federation-mesh`, `04-layered-security`, `05-integration-examples`)
- 2 README-only orphans (`01-violation-detection`, `02-defensive-vs-surveillance`)
- 5 empty dirs in `01-ecosystem-integration/`
- 5 empty dirs in `02-federation-mesh/`
- 4 empty dirs in `03-production/`

Rewrote `showcase/README.md` to reflect actual 4-tier structure.
Updated `showcase/99-gaps-analysis/README.md` with current ground-truth numbers.

### Documentation Updates

- `README.md` — updated feature list (batch/notification), test counts, quality metrics
- `CONTEXT.md` — added JSON-RPC section, updated test/status sections with coverage data

### Test Coverage Expansion

| Area | Before | After |
|------|--------|-------|
| `ipc/server.rs` | 0% | 86% |
| `ipc/transport.rs` | 0% | 42% |
| `ipc/jsonrpc.rs` | — | 100% |
| Overall | 79.5% | 81.9% |

New tests: BTSP config, socket paths, proc_uid, rand_u128, frame I/O,
JSON helpers, batch requests, notifications, parse errors, empty batches,
unknown methods.

## Remaining Debt

### Coverage Gap (81.9% → 90% target)

Transport accept-loops and main.rs entry point are hard to unit-test without
real sockets. Consider integration-level socket tests or `#[cfg(test)]` test
harnesses for the next push.

### Integration Gaps (blocked on peer primals)

These are architectural integration points, not code quality debt:
- BearDog live lineage verification (need `crypto.sock` peer)
- ToadStool live discovery (need ToadStool instance)
- Songbird live federation (need Songbird instance)
- Network-layer defense execution (need OS/firewall abstraction)
- User approval workflow (need notification channel)

All integration clients are written and `#[ignore]`-gated tests are ready
to activate when peer primals come online.

## For Other Teams

- **No IPC wire changes** — JSON-RPC now supports batch/notification, but
  single-request callers are unaffected (fully backward compatible).
- **No capability registry changes** — `capabilities.list` and `identity.get`
  responses unchanged.
- **No new dependencies** — workspace dep set unchanged (Tokio features trimmed).
- **BTSP Phase 2 handshake framework** ready for BearDog delegation when
  BearDog exposes challenge-response over `crypto.sock`.

## Verification

```bash
cargo fmt --all -- --check
cargo clippy --workspace -- -D warnings
cargo test --workspace
cargo doc --workspace --no-deps
cargo deny check
cargo llvm-cov --workspace
```

All gates green as of this handoff.
