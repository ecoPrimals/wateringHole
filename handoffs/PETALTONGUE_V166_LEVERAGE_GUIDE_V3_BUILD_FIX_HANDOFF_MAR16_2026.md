# petalTongue v1.6.6 — Leverage Guide v3.0 + Build Fix Handoff

**Date**: March 16, 2026
**Primal**: petalTongue v1.6.6
**Session**: Leverage guide expansion, build fix, doc cleanup
**Status**: Complete — all checks pass

---

## What Changed

### 1. Leverage Guide v3.0 (wateringHole)

Updated `PETALTONGUE_LEVERAGE_GUIDE.md` from v2.0.0 → v3.0.0. Added 5 new sections:

- **Part 5 — petalTongue Alone (Self-Leverage)**: Standalone modes, self-monitoring, dev tool usage, CI/CD quality gate via `visualization.validate`
- **Part 6 — Novel Self-Referential Patterns**: Introspection loop, multi-modal bridge (sighted + blind share a session), capability explorer (live architecture diagrams from runtime state)
- **Part 7 — Emergent Duo Patterns**: 8 two-primal combinations (sourDough, skunkBat, groundSpring, rhizoCrypt, NestGate, biomeOS, Squirrel, BearDog)
- **Part 8 — Emergent Trio and Quartet Patterns**: Provenance pipeline, memory stack, sovereign SOC, AI research station, digital twin, accessible science lab
- **Part 9 — How Springs Should Use petalTongue**: 5-minute integration quickstart, full checklist, "what you do NOT need"

Also renamed Part 1 from "Using petalTongue Alone" to "One Spring + petalTongue" to avoid ambiguity with new Part 5.

### 2. Build Fix — Restored `web/index.html`

Previous cleanup session incorrectly moved `web/index.html` to `archive/docs-mar-2026/debris/web/`. This file is a compile-time asset referenced by `include_str!("../web/index.html")` in `src/web_mode.rs`. The build was broken. Restored the file to its original location.

### 3. Doc Cleanup

- **ENV_VARS.md**: Removed dead link to archived `docs/operations/QUICK_START.md`, updated date to March 16, 2026
- **README.md, START_HERE.md**: Verified accurate — 5,404 tests, 854-line largest file, zero TODO/FIXME/HACK, all files under 1000 lines

---

## Verification

| Check | Status |
|-------|--------|
| `cargo build --workspace` | **PASS** |
| `cargo fmt --check` | **PASS** (0 diffs) |
| `cargo clippy --all-features --all-targets -- -D warnings` | **PASS** (0 warnings) |
| `cargo test --all-features --workspace` | **PASS** (5,404 passed, 0 failed) |
| All files < 1000 lines | **PASS** (largest 854) |
| Zero TODO/FIXME/HACK in production code | **PASS** |

---

## Lesson Learned

`web/index.html` is not documentation — it is a compile-time asset embedded via `include_str!`. Future cleanup sessions must check for `include_str!` and `include_bytes!` references before archiving any file.

---

**License**: AGPL-3.0-or-later
