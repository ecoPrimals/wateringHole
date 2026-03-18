# Handoff: primalSpring v0.1.0 — Deep Debt Audit + Evolution

**Date:** March 17, 2026  
**From:** primalSpring (Phase 0→1 deep debt audit)  
**To:** biomeOS, all NUCLEUS primals, ecosystem  
**License:** AGPL-3.0-or-later  
**Supersedes:** `PRIMALSPRING_V010_COMPREHENSIVE_AUDIT_EVOLUTION_HANDOFF_MAR17_2026.md`

---

## Executive Summary

primalSpring underwent a comprehensive audit against all ecosystem standards
(wateringHole), sibling spring patterns (hotSpring, wetSpring, airSpring,
groundSpring, healthSpring), and deep debt criteria. Every finding was
immediately resolved. The codebase is now zero-warning across all five
toolchain checks (fmt, check, clippy pedantic+nursery, test, doc) with full
public API documentation and honest validation in every experiment.

---

## What Changed

| Category | Change |
|----------|--------|
| **Dishonest scaffolding** | exp041/exp042 evolved from `check_bool(true)` to real discovery with `discover_for()`, `probe_primal()`, `check_skip()` |
| **Workspace lints** | `unsafe_code = "forbid"` and `missing_docs = "warn"` in `[workspace.lints.rust]` — single source of truth |
| **Documentation** | 98 doc comments added to library (all public fields, variants, methods, constants); 25 crate-level docs added to experiments |
| **Broken doc link** | `AtomicType::required_primals()` → fully qualified path in `ipc::discover` |
| **Server hardening** | `unwrap_or_default()` → typed error handling with `tracing::error` + JSON-RPC fallback |
| **Metadata** | `repository` field added to `[workspace.package]` |
| **Lint cleanup** | 40 redundant `#![forbid(unsafe_code)]` directives removed (workspace lint handles it) |

## Current State

| Metric | Value |
|--------|-------|
| Experiments | 38 (7 tracks) |
| Unit tests | 69 |
| clippy (pedantic+nursery) | 0 warnings |
| cargo doc (missing_docs) | 0 warnings |
| `#[allow()]` | 0 |
| unsafe_code | Workspace `forbid` |
| C dependencies | 0 |
| Dishonest scaffolding | 0 |
| Files over 1000 LOC | 0 |

## What Blocks Phase 1

1. Live primals (BearDog + Songbird) on Unix sockets
2. biomeOS graph executor for Track 2 experiments
3. Provenance Trio deployment for Track 3 (RootPulse)
4. Songbird registration (`ipc.register` at startup)

---

**License**: AGPL-3.0-or-later
