# barraCuda v0.3.5 — Doc Cleanup & Count Alignment

**Date**: March 13, 2026
**Type**: Maintenance handoff
**Scope**: Root doc accuracy, stale count correction, debris audit

---

## Summary

Post-IPC-first architecture evolution, all root docs, specs, scripts, and
showcase files audited for accuracy. No debris, no stale TODOs, no archive
candidates found — the codebase is clean.

---

## Count Corrections

| Metric | Old | Current | Files Updated |
|--------|-----|---------|---------------|
| Tests | 3,415 | 4,011 (3,941 lib + 70 core) | STATUS, README, REMAINING_WORK, test-tiered.sh |
| Rust files | 1,064 (was 1,062 in one place) | 1,088 | STATUS, README, REMAINING_WORK |
| WGSL shaders | 803 (in showcase) | 806 | demo.sh, main.rs |
| Showcase demos | 10 (in CHANGELOG) | 9 | CHANGELOG |
| Integration test files | 42 | 43 | README |

---

## Stale Reference Fixes

| File | Fix |
|------|-----|
| `showcase/README.md` | Date March 9 → March 13, 2026 |
| `CHANGELOG.md` | CoralReefDevice description → IPC-first (was "will wrap coral-gpu") |
| `STATUS.md` | Device management description → IPC-first sovereign backend |

---

## Debris Audit Results

| Category | Finding |
|----------|---------|
| TODO/FIXME in .rs | **Zero** (only constant names like `HARGREAVES_TEMP_OFFSET`) |
| TODO/FIXME in .md | **Zero** (only references to having zero TODOs) |
| Stale scripts | **None** — `scripts/test-tiered.sh` is current |
| Archive candidates | **None** — no archive/ directories, no orphaned files |
| Files over 1000 lines | **None** — largest is 761 lines |
| Hardcoded ports/primals | **None in production** — only in test fixtures (acceptable) |
| Blocked references | **All current** — PFIFO channel init (coralReef) is genuine remaining work |

---

## Quality Gates

- `cargo fmt --all -- --check` ✅
- `cargo clippy --workspace --all-targets -- -D warnings` ✅
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` ✅
