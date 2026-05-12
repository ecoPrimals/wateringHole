# Squirrel v0.1.0 — Doc Cleanup & Debris Review Handoff

**Date**: April 20, 2026
**From**: Squirrel alpha.52+

## Root Doc Updates

- `README.md`, `CONTEXT.md`: Updated `.rs` file count (~1,039 → ~1,035) and total lines (~337k → ~336k) to reflect 4 orphan file deletions
- `CURRENT_STATUS.md`: Session AB entry added (deep debt: orphan removal, feature hygiene, capability naming)
- `MCP_INTEGRATION.md` (gen2 spec): Phase 3/4 headings updated — checked items preserved, unchecked items annotated as "delegated to gen3 architecture" (BTSP, capability discovery, plugin manager, SDK)
- `tarpaulin.toml`: Deleted — project uses `cargo-llvm-cov` exclusively; tarpaulin config was stale and never invoked

## Debris Review

| Check | Result |
|-------|--------|
| Scripts (.sh, .py, .js) | **Zero** in source tree |
| Temp/backup files (.bak, .orig, .tmp, .swp) | **Zero** |
| Build artifacts outside target/ | **Zero** |
| TODO/FIXME/HACK in .rs | **Zero** (confirmed) |
| TODO/FIXME/HACK in .toml | **Zero** |
| Stale CI configs | **None present** (CI lives in parent infra) |
| `.env` tracking | **Untracked** (covered by .gitignore `*.env`) |
| EVOLUTION markers | **1** in `btsp_handshake/mod.rs` — still relevant (blocked on primalspring 0.10.0) |
| Phase 2/3 markers in .rs | All **relevant** deferred-work docs (BTSP cipher, federation, plugin sandbox) |

## April 20 Session Summary (Two Commits)

### Commit 1: BTSP Auto-Detect (PG-14)
First-byte peek on UDS accept: `{` → plain JSON-RPC fallback. Resolves wetSpring PG-14. 5 new tests (7,165 total).

### Commit 2: Deep Debt — Orphan Removal, Feature Hygiene, Capability Naming
- Deleted orphaned `auth/` subtree (4 files, ~1,140 lines)
- Removed 10 placeholder features with zero `cfg` references
- Fixed SDK `console_error_panic_hook` → `console` feature name mismatch
- Niche `DEPENDENCIES` evolved from `primal_names::BEARDOG` → `"security"`, etc.
- Hardcoded primal names in logs → capability-based

### Commit 3: Doc Reconciliation & Debris Cleanup
- Root doc metric updates, gen2 spec Phase 3/4 annotation, tarpaulin.toml removal

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,165 passing / 0 failures |
| Coverage | 90.1% region |
| Clippy | CLEAN (`-D warnings`) |
| `cargo fmt` | PASS |
| `.rs` files | ~1,035 |
| Lines | ~336k |

## Upstream Blocks (Unchanged)

1. **Three-tier genetics** — blocked on `ecoPrimal >= 0.10.0`
2. **BLAKE3 content curation** — blocked on NestGate content-addressed storage API
3. **Phase 3 cipher negotiation** — blocked on BearDog `btsp.negotiate` server-side
