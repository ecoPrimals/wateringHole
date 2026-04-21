# Songbird v0.2.1 — Wave 152 Deep Debt Handoff

**Date**: April 20, 2026
**From**: Songbird (Waves 148–152)
**For**: Ecosystem teams, primalSpring, downstream springs

---

## Summary (Waves 148–152)

Five consecutive deep debt waves resolved 20+ categories across Songbird:

| Wave | Focus | Key Items |
|------|-------|-----------|
| **148** | PG-21 persistent NDJSON | Single-shot `break` removed from `handle_ndjson_session`; BTSP handler made persistent; parse errors `continue` instead of killing sessions |
| **149** | Comprehensive lint/hardcode/mock | 11 blanket `#![allow]` removed (57 clippy fixes); `/var/run/`, `/run/user/`, `/var/tmp/` → constants; duplicate constants consolidated; `test-mocks` standardized; stale CLI features removed; `expect()` annotated |
| **150** | Doc cleanup + debris | Stale `health-monitor.sh` removed (wrong API shape); false-positive metrics corrected; verification dates updated |
| **151** | PG-37 capability-first routing | `ipc.resolve` gets primal-name fallback; `ipc.resolve_by_name` alias; `name` param alias; 3 new tests |
| **152** | Deps + hardcode + test hygiene | Dead workspace deps removed (slab, wasi); yaml stripped from config feature; bluetooth test-utils → test-mocks; env-dependent TLS cert test fixed; last `/run/user/` hardcodes → constants; bare `#[expect]` given reason |

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,380 lib passed, 0 failed, 22 ignored |
| Clippy | pedantic + nursery, zero warnings (Apr 20) |
| cargo-deny | advisories ok, bans ok, licenses ok, sources ok |
| unsafe | 0 blocks, `forbid(unsafe_code)` all 30 crates |
| async-trait | 0 annotations, dep removed |
| Files >800L | 0 (largest 763L) |
| Production unwrap/todo/panic | 0 |
| Blanket lint suppressions | 0 |
| Hardcoded paths/IPs | 0 (all evolved to constants or env) |

---

## Remaining Evolution Targets (documented, not blockers)

1. **serde_yaml → TOML-only**: 5 call sites; archived upstream crate; yaml feature already stripped from workspace config dep
2. **bincode 1.x via tarpc**: RUSTSEC-2025-0141; blocked on tarpc ecosystem upgrade
3. **chrono scoping**: wide usage across crates; medium churn
4. **dyn dispatch in discovery streams**: architectural; contained to trait boundaries
5. **Coverage 72% → 90%**: orchestrator integration paths, config edge cases

---

**Verification**: `cargo check` + `clippy -D warnings` + `cargo fmt` + `cargo deny` + `cargo test --workspace --lib` all pass.

**Pushed**: songBird, wateringHole, primalSpring all up to date via SSH.

---

**License**: AGPL-3.0-or-later
