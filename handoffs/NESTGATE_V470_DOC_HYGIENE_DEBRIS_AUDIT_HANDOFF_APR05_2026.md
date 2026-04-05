# NestGate v4.7.0-dev — Documentation Hygiene & Debris Audit

**Date**: April 5, 2026
**Commit**: (pending push)
**Scope**: Root docs alignment, debris cleanup, stale reference elimination

---

## Summary

Comprehensive documentation hygiene pass across 15+ files. All root docs now
reflect current measured state: 11,685 tests passing, 463 ignored, 0 failures;
20 code/crates in workspace (23 total members); `#![forbid(unsafe_code)]` on
ALL crate roots with zero exceptions.

---

## Changes

### Root doc alignment (11 files)

| File | Fixes |
|------|-------|
| START_HERE.md | Test counts, unsafe language, serial test state, architecture tree |
| STATUS.md | Test counts, unsafe language, crate count (24→23), ground truth section, architecture tree |
| README.md | Test counts, unsafe language, crate count (21→20), architecture tree, serial test state |
| QUICK_REFERENCE.md | Test counts, crate count |
| QUICK_START.md | Test counts |
| CONTEXT.md | Test counts, unsafe language, crate count, workspace crate list |
| CONTRIBUTING.md | Test counts, unsafe language, env isolation example (EnvSource/MapEnv) |
| DOCUMENTATION_INDEX.md | Crate count |
| CAPABILITY_MAPPINGS.md | Date |
| tests/README.md | Test counts |
| tests/DISABLED_TESTS_REFERENCE.md | Test counts |

### Debris cleanup (4 files)

| File | Issue | Fix |
|------|-------|-----|
| docs/guides/LOCAL_INSTANCE_SETUP.md | Referenced `scripts/start_local_dev.sh` (never existed) | Replaced with manual commands |
| docs/guides/ECOSYSTEM_INTEGRATION_GUIDE.md | Referenced `scripts/test-live-integration.sh` (never existed) | Replaced with `cargo test` |
| docs/UNIVERSAL_ADAPTER_ARCHITECTURE.md | Referenced `scripts/primal_hardcoding_elimination.sh` (never existed) | Replaced with completion note |
| docs/INFANT_DISCOVERY_ARCHITECTURE.md | Referenced `scripts/eliminate_all_hardcoding.sh` (never existed) | Replaced with completion note |

### Debris audit (confirmed clean)

- Zero empty `.rs` files in crate sources
- Zero orphaned JSON fixtures
- Zero TODO/FIXME/HACK markers in crate sources
- `nestgate-automation`, `nestgate-network`, `nestgate-mcp` — fossil on disk, not workspace members
- 79 `#[deprecated]` markers — legitimate API deprecation surface
- `scripts/setup-test-substrate.sh`, `.pre-commit-config.sh` — legitimate

---

## Key corrections

1. **Unsafe code**: "except env-process-shim" → "zero exceptions". The shim uses
   edition 2021 where `set_var`/`remove_var` are safe; it has `#![forbid(unsafe_code)]`.
2. **Crate count**: 21 code/crates → 20 (nestgate-network shed in Session 29).
3. **Test count**: 12,088 → 11,685 passing (reduction from nestgate-network removal).

---

## Current state

```
Build:    PASS (clippy, fmt, check — 2026-04-05)
Tests:    11,685 passing, 0 failures, 463 ignored
Coverage: ~80% line
Unsafe:   #![forbid(unsafe_code)] ALL crate roots
Serial:   5 total (4 env-process-shim, 1 CLI tracing)
Workspace: 23 members (20 code/crates + tools + fuzz + root)
Shed:     nestgate-network, nestgate-automation, nestgate-mcp (fossil on disk)
```

---

## Remaining debt

| Area | Status |
|------|--------|
| Coverage gap to 90% | ~10pp remaining |
| nestgate-security crypto delegation | Partially delegated; crate still in workspace |
| nestgate-mcp | Shed from workspace; fossil on disk |
| nestgate-automation | Shed from workspace; fossil on disk |
| Remote ZFS impl (714 lines) | Mechanical trait impl; could extract |
| handler_config.rs (709 lines) | Config schema + defaults; tests embedded |
