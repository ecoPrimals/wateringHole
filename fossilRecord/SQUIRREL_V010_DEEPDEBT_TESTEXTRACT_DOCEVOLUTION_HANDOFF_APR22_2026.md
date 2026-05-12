# Squirrel v0.1.0 — Deep Debt: Test Extraction, Doc Evolution, Dep Hygiene

**Date**: April 22, 2026
**From**: Squirrel team
**Session**: AG (follows AF — BTSP JSON-line relay)

---

## What Changed

### Test Extraction

`adapter-pattern-tests/src/auth.rs` was 845 lines — the last production-path file
exceeding 800 lines. Extracted 382 lines of tests into sibling `auth_tests.rs`.
Production code: 465 lines. **Zero production files now exceed 800 lines.**

### Stale Evolution Comments

Removed 4 `// Evolution:` comments describing work that was already completed:

- 3 in `biomeos_integration/mod.rs`: "Use interval ticker instead of loop+sleep" —
  the code already uses `tokio::time::interval` with configurable env-var intervals.
- 1 in `security/orchestrator/mod.rs`: "Properly wait for active security checks to
  complete instead of arbitrary sleep" — the drain loop was already implemented.

### Doc Evolution

`unix_socket.rs` module docs evolved from "biomeOS" to "ecosystem" language
(11 changes in descriptive text). Env var names (`BIOMEOS_SOCKET_PATH`,
`BIOMEOS_INSECURE`, `BIOMEOS_FAMILY_ID`) and filesystem paths (`/biomeos/`)
are **preserved** as ecosystem-wide wire contracts.

### Dependency Hygiene

- `test-context`: Removed from `[workspace.dependencies]` — orphaned (no crate
  references it since the main crate removal in session AE).
- `zstd`: Bumped `0.12` → `0.13.3` (feature-gated off by default; only resolves
  under `squirrel-mcp` `compression` feature).

### Gitignore Tightening

Added `*.bak`, `*.orig`, `*.profraw`, `*.profdata` to `.gitignore`. Removed the
empty `# Build debris` heading.

### Debris Audit

Full repo scan confirmed:
- Zero script files (.sh, .py, .bash, .bat) in repo
- Zero temp/build artifacts outside `target/`
- Zero duplicate/backup files
- Zero TODO/FIXME/HACK/XXX markers in production code
- `.env` and `mcp-config.env` properly gitignored (not tracked)
- All root files accounted for and current

---

## Remaining biomeos References

~350 `biomeos` references remain across the codebase. Classified:

| Class | Count | Status |
|-------|-------|--------|
| **A: Wire/API constants** (env vars, socket paths, API_VERSION) | ~120 | **Preserved** — ecosystem-wide contracts |
| **B: Documentation** (module docs, comments) | ~100 | Partially evolved; env var references must stay |
| **C: Logs/diagnostics** | ~30 | **Evolved** in sessions AE + AG |
| **D: Env var fallbacks** | ~50 | ECOSYSTEM_* checked first; BIOMEOS_* as fallback |
| **E: Capability descriptions** | ~10 | **Evolved** in session AE |
| **Test-only** | ~40 | Acceptable — test fixtures reference env vars |

Wire-protocol references cannot change without ecosystem-wide coordination.

---

## Metrics

- **7,168** tests passing (0 failures)
- **0** clippy warnings (`-D warnings -W pedantic -W nursery`)
- **0** cargo deny issues (`advisories ok, bans ok, licenses ok, sources ok`)
- **90.1%** region coverage
- **0** production files > 800 lines
- **0** TODO/FIXME/HACK markers
- **0** unsafe blocks
