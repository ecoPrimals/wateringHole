# rhizoCrypt v0.14.0-dev — Session 25 Handoff

**Date**: 2026-04-02
**Version**: 0.14.0-dev
**Session**: 25 — Comprehensive Audit & Evolution
**Primal**: rhizoCrypt (Ephemeral DAG Engine)

---

## Summary

Full-spectrum audit of rhizoCrypt against wateringHole standards followed by
systematic execution of all findings. The session covered dependency hygiene,
maximally pedantic clippy enforcement, concurrency improvements, portability
fixes, production mock audit, ecoBin/PIE verification, and documentation
refresh.

---

## Changes Executed

### 1. Workspace Dependency Hygiene
- `tower` 0.4 → 0.5 in workspace root; `rhizo-crypt-rpc` now uses
  `tower.workspace = true` — eliminates version split per
  `WORKSPACE_DEPENDENCY_STANDARD.md`
- Removed direct `hashbrown` dependency — migrated all usage to
  `std::collections::{HashMap, HashSet}` across 8 source files
- hashbrown 0.14 remains only as transitive dep via `dashmap`

### 2. Maximally Pedantic Clippy (78 lints fixed)
- 58 `doc_markdown` — backticks on identifiers in doc comments
- 10 `significant_drop_tightening` — lock scopes tightened (real concurrency win)
- 7 `must_use_candidate` — `#[must_use]` on pure functions
- 2 `unnecessary_literal_bound` — `&str` → `&'static str`
- 1 bare URL wrapped in angle brackets
- **Removed workspace lint allows** for these lints — now permanently enforced

### 3. Concurrency: Lock Scope Tightening
- Refactored RwLock/Mutex guard lifetimes in tarpc adapter, unix socket
  adapter, songbird client, mock providers, store, and main orchestrator
- Guards no longer held across `.await` points in IPC client paths

### 4. Tarpc Adapter Semantic Fix
- `is_healthy()` now returns `false` when `live-clients` feature is disabled
  (previously returned `true` on stub — misleading for monitoring)
- Dead code warnings eliminated with cfg_attr

### 5. Portability
- Removed hardcoded `/path/to/home/` target-dir from `.cargo/config.toml`
- Developers use `CARGO_TARGET_DIR` env var; CI already did

### 6. Documentation Refresh
- `CONTEXT.md` — updated coverage (94.34%), max file (928), binary size (5.4 MB PIE)
- `README.md` — updated coverage metrics
- `CHANGELOG.md` — session 25 entry added
- `showcase/05-performance/README.md` — replaced stale hashbrown/RwLock
  references with DashMap/std::collections
- `docs/ENV_VARS.md` — fixed broken IPC_COMPLIANCE_MATRIX.md reference,
  corrected `cargo run` example to include `-p rhizocrypt-service`

### 7. Archive Cleanup
- Moved `archive/dec-27-2025-*` (15 files) to
  `ecoPrimals/infra/fossilRecord/rhizoCrypt-dec-2025/`
- Removed `archive/` directory from rhizoCrypt tree

---

## Audit Findings (Verified Clean)

| Check | Result |
|-------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy --workspace --all-features` | 0 warnings (maximally pedantic) |
| `cargo clippy --release --workspace` | 0 warnings |
| `cargo doc --no-deps` | PASS |
| `cargo test --workspace --all-features` | 1,423 tests, 0 failures |
| `cargo llvm-cov` | 94.34% lines, 93.41% functions, 94.81% branches |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| PIE binary | Confirmed (5.4 MB stripped release) |
| unsafe blocks | Zero (`forbid(unsafe_code)` on all crates) |
| Files > 1000 lines | Zero (max: 928 lines) |
| TODO/FIXME/HACK in .rs | Zero |
| Production mocks | Zero (all test-gated) |
| SPDX headers | All 129 `.rs` files |
| scyBorg triple license | Compliant |
| UniBin/ecoBin | Compliant |
| Semantic method naming | Compliant |
| Sovereign compute | No cloud deps, no telemetry |

---

## Ecosystem Interaction Points

- **wateringHole compliance**: Verified against `STANDARDS_AND_EXPECTATIONS.md`,
  `WORKSPACE_DEPENDENCY_STANDARD.md`, `PRIMAL_IPC_PROTOCOL.md`,
  `UNIBIN_ARCHITECTURE_STANDARD.md`, `SEMANTIC_METHOD_NAMING_STANDARD.md`,
  `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md`
- **genomeBin manifest**: `wateringHole/genomeBin/manifest.toml` shows
  `latest = "0.13.0-dev"` and `pie_verified = false` — both stale
  (actual: 0.14.0-dev, PIE verified). Update needed in wateringHole.
- **Provenance trio**: rhizoCrypt + loamSpine + sweetGrass integration
  architecture unchanged; capability-based discovery operational

---

## Known Remaining Items

1. **genomeBin manifest stale** — `wateringHole/genomeBin/manifest.toml`
   needs version bump to 0.14.0-dev and `pie_verified = true`
2. **hashbrown 0.14 transitive** — remains via dashmap; awaiting dashmap v7
   stable release
3. **bincode v1 / opentelemetry_sdk advisories** — transitive via tarpc;
   tracked in deny.toml, awaiting tarpc upstream migration
4. **rustls-rustcrypto migration** — documented; awaiting stable release to
   eliminate ring (C/asm) from optional `http-clients` path

---

## Parallel Evolution Notes (primalSpring)

rhizoCrypt's concurrency improvements (lock scope tightening, DashMap patterns)
are validated by primalSpring Phase 0–14. The tarpc adapter health semantics
fix ensures accurate monitoring when composing with biomeOS health probes.

---

*Part of the ecoPrimals sovereign computing ecosystem.*
*License: AGPL-3.0-or-later / ORC / CC-BY-SA 4.0 (scyBorg Triple-Copyleft)*
