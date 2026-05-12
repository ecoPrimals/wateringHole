# Songbird v0.2.1 — Wave 109: Root Docs & Config Cleanup Handoff

**Date**: April 4, 2026
**Commit**: Pending (on `main`)
**Previous**: Wave 108 (`27f2e379`) — deep debt sweep

---

## Summary

Comprehensive cleanup of root documentation, config templates, and architecture docs.
Trimmed REMAINING_WORK.md from 1,871 lines to ~140 lines (92% reduction), removing
30+ completed wave sections while preserving active blockers and pending work.

## Changes

### Root Docs

| File | Change |
|------|--------|
| `REMAINING_WORK.md` | 1,871L → ~140L — removed 30+ completed wave sections (fossil record preserved in git history); kept Current Status, Active Blockers, Pending work, Priority Order |
| `README.md` | Test count 12,495 → 12,530 |
| `CONTEXT.md` | Date updated to April 4, 2026 |

### Architecture Docs

| File | Change |
|------|--------|
| `docs/architecture/SOVEREIGN_ONION_TRUE_PRIMAL_ARCHITECTURE.md` | Evolved from Feb 2026 BearDog-centric design doc to current capability-based naming; removed emojis from all section headers; updated code examples to `CryptoProvider`; added implementation status section |
| `docs/architecture/SECURITY_PROVIDER_CRYPTO_API_SPEC.md` | Title/header evolved; `beardog.crypto.*` method namespace → `crypto.*`; all BearDog refs → security provider |

### Config Templates

| File | Change |
|------|--------|
| `config/ecosystem-integration.toml` | Fixed swapped capability mappings (storage/networking) |
| `config/environment.env.template` | `toadstool`/`beardog`/`nestgate`/`squirrel` → capability names in endpoint comments |
| `config/production-config.toml` | Removed emoji from header |
| `config/production.env.example` | Removed emoji from echo output |
| `config/zero-knowledge.env.template` | Removed emoji; cleaned up mixed-case duplicates (`AiProvider_ENDPOINT` etc.) → 4 consistent `SCREAMING_SNAKE_CASE` entries |

### REMAINING_WORK.md False Positives Resolved

- Removed stale "Ring-free workspace — rcgen replacement" from Priority Order (rcgen already eliminated)
- Removed completed `sysinfo` elimination items from Dependency Evolution (already done)
- Updated coverage target from ~72% to ~77%
- Updated `ring` elimination status to reflect current state (optional k8s feature only)

## Verification

| Check | Status |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS |
| Code unchanged | No .rs files modified |

## What Remains

Specs directory (~60 .md files) contains emojis throughout — these are specification
fossil records and not worth bulk-editing. Active code and config are clean.
