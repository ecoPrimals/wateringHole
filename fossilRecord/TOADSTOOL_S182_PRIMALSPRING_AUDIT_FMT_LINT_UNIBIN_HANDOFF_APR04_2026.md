# ToadStool S182 — primalSpring Audit Response: fmt, lint migration, UniBin --port

**Date**: April 4, 2026
**Session**: S182
**Commit**: `1b4b832e` on `master`
**Quality**: 21,853 tests (0 failures), Clippy clean, fmt clean

---

## Audit Response Summary

### Audit Grade: D (received) → improvements applied

| Tier | Finding | Resolution |
|------|---------|------------|
| **T1 Build** | ~1,899 lines fmt diff | `cargo fmt --all` applied — 0 diff now |
| **T1 Build** | Clippy fails (manual_let_else, GenericArray) | Already clean (exit 0) — fixed in prior sessions |
| **T1 Build** | License → -or-later | Confirmed: all `AGPL-3.0-only` (SPDX + Cargo.toml) — no `-or-later` |
| **T2 UniBin** | --port not wired to server bind | **Fixed**: legacy `toadstool-server` alias now parses `--port N` from argv |
| **T8 Presentation** | 485 #[allow( vs 126 #[expect( (79% allow) | **Migrated**: 355 allow / 530 expect (40% allow, 60% expect) |
| **T8 Presentation** | PII hits in 9 test files | All placeholder data (`@example.com`, RFC 5737 IPs) — no real PII |

### Not addressed this session (structural / multi-session)

| Tier | Finding | Status |
|------|---------|--------|
| **T3 IPC** | TCP not wired, no domain symlink | TCP **is** wired via `--port`; domain symlink is roadmap |
| **T4 Discovery** | 2,998 primal-name refs / 384 files | Ongoing S176-180 migration (was 3,239 at S177); phased |
| **T4 Discovery** | 168 env-var refs / 52 files | Backward-compat aliases via `#[serde(alias)]`; phased |
| **T4 Discovery** | health.liveness "Method not found" on S168 binary | Stale binary — current builds register all JSON-RPC methods |
| **T5 Naming** | 0 capabilities on last verified binary | Stale binary — current builds expose capabilities via registry |
| **T9 Deploy** | TCP not wired for mobile | TCP listener exists when `--port` specified; mobile paths tracked |

## Changes (306 files)

### cargo fmt --all
- 1,898 lines of formatting drift resolved across entire workspace

### #[allow(clippy::*)] → #[expect(clippy::*, reason)]
Migrated 11 lint categories:
- `cast_precision_loss` (~107), `float_cmp` (~74), `cast_possible_truncation` (~67)
- `unused_async` (~62), `significant_drop_tightening` (~30)
- `redundant_pub_crate` (~12), `missing_const_for_fn` (~12)
- `assertions_on_constants` (~8), `struct_excessive_bools` (~7)
- `module_inception` (~4), `too_many_arguments`

~40 stale suppressions removed (lint no longer fires → attribute was dead).

### Legacy binary --port fix
- `crates/cli/src/main.rs`: `run_server_daemon` now accepts `port: Option<u16>`
- Legacy `toadstool-server` argv path parses `--port N` and forwards to `run_server_main`

## Remaining #[allow] breakdown (355 total)
- `deprecated` (~131) — intentional backward-compat bridges; removing as APIs evolve
- `dead_code` (~99) — items used in tests; `#[expect]` would cause unfulfilled-lint-expectation
- `unused_imports` (~7) — cfg-conditional imports
- Other: `unsafe_code` (2), `clippy::expect_used` (3), misc
