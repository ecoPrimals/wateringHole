# SweetGrass v0.7.27 — Capability-Based Naming & Deep Debt Evolution

**Date**: April 16, 2026
**Primal**: sweetGrass (Provenance & Attribution)
**Version**: v0.7.27

---

## Summary

Systematic evolution from hardcoded primal names to capability-based naming
across the entire sweetGrass codebase. All primals are now referenced by their
capability role, not their ecosystem name. Serde aliases preserve full backward
wire compatibility for all renamed fields.

This pass also resolved all remaining file-size debt, doc-link errors, and
stale lockfile entries.

---

## Changes

### Capability-Based Field Renames (15 files, ~40 edits)

All renames include `#[serde(alias = "old_name")]` for backward deserialization.

| Old Name | New Name | Capability |
|----------|----------|------------|
| `toadstool_task` | `compute_task` | Compute provider task ID |
| `rhizo_session` | `session_ref` | Session events provider reference |
| `loam_entry` | `ledger_entry` | Permanent ledger entry reference |
| `loam_commit` | `ledger_commit` | Permanent ledger commit reference |
| `LoamCommitRef` | `LedgerCommitRef` | Type (alias preserved) |
| `by_loam_entry()` | `by_ledger_entry()` | Constructor (`#[deprecated]` alias kept) |
| `from_loam_entry()` | `from_ledger_entry()` | Factory method |
| `parse_loam_entry()` | `parse_ledger_entry()` | Internal parser |

### Files Changed

**Core types**: `activity/mod.rs`, `braid/types.rs`, `braid/mod.rs`,
`contribution.rs`, `entity/mod.rs`

**Factory**: `factory/mod.rs`, `factory/contribution.rs`, `factory/tests.rs`

**Service**: `handlers/jsonrpc/contribution.rs`, `tests/integration.rs`

**Compression**: `engine/mod.rs`, `engine/tests.rs`

**Doc fixes**: `agent.rs`, `braid/braid_type.rs`, `entity/mod.rs` (3 `rustdoc::private_intra_doc_links` errors fixed)

### Test File Refactors

`store-nestgate/src/store/tests.rs` (876 lines) → split by concern:
- `tests/mod.rs` (~460L): Mock infrastructure, CRUD, config, error, client, index tests
- `tests/queries.rs` (~370L): Query, filter, ordering, pagination, relationship tests

`entity.rs` (803 lines) → split by concern:
- `entity/mod.rs` (483L): Production code only
- `entity/tests.rs` (334L): Bincode roundtrips, constructors, inline data, serialization, errors

### Lockfile

Regenerated. Stale phantom `libsqlite3-sys` entry confirmed never-compiled
(no workspace member enables SQLite features). Dependency versions updated.

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,560 (1,502 local + 58 Docker CI) |
| Coverage | 90.4% without Docker / 91.7% with Postgres |
| Max file | 726 lines (`agent.rs`) |
| .rs files | 191 (51,355 LOC) |
| Clippy | 0 warnings (pedantic + nursery) |
| Rustdoc | 0 warnings (`-D warnings`) |
| Unsafe | 0 blocks |
| TODOs | 0 |

---

## Audit Posture

### Zero Violations
- **Unsafe code**: `#![forbid(unsafe_code)]` all crates
- **Production unwrap/expect**: denied by workspace lints
- **Mocks in production**: all isolated to `#[cfg(test)]` or `feature = "test"`
- **TODO/FIXME/HACK**: zero in source
- **Hardcoded primal names**: evolved to capability-based (this pass)

### Remaining Documented Trade-offs
- **sled**: deprecated backend, feature-gated, skip-tree in deny.toml (redb is primary)
- **BTSP Phase 3**: client-initiated handshake not yet implemented (Phase 2 server-side complete)

---

## async-trait Status (April 16, 2026)

**RESOLVED** — All 22 `#[async_trait]` attributes and `async-trait` crate eliminated.
All 6 traits converted to native RPITIT with enum dispatch backends
(`BraidBackend`, `SigningBackend`, `AnchoringBackend`, `SessionEventsBackend`,
`SessionEventStreamBackend`, `DiscoveryBackend`). ~130 `Arc<dyn Trait>` → 0.

See `SWEETGRASS_STADIAL_PARITY_HANDOFF_APR16_2026.md` for full resolution details.

---

## Wire Compatibility

All renamed fields use serde `alias` attributes. Old JSON payloads with
`toadstool_task`, `rhizo_session`, `loam_entry`, `loam_commit` continue to
deserialize correctly. New serialization uses the capability-based names.
The `ByLoamEntry` enum variant name is preserved in wire format; the
`by_loam_entry()` constructor is deprecated but functional.

---

## Previous Handoff

Archived: `archive/SWEETGRASS_V0727_PRIMALSPRING_AUDIT_DEEP_DEBT_HANDOFF_APR15_2026.md`
