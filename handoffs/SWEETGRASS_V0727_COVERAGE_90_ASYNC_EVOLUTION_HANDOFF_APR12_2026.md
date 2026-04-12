# sweetGrass v0.7.27 — Coverage 90%+, async-trait Evolution, Deep Debt Audit

**Date**: April 12, 2026
**Primal**: sweetGrass v0.7.27
**Trigger**: primalSpring downstream audit — coverage 87→90% target, remaining debt sweep

---

## Summary

Coverage sprint achieving 90.3% line coverage (from 87%), 1,416 tests (from
1,315), smart refactoring of the only >1000-line file, and evolution of two
async traits from `async_trait` crate to native Rust 2024 `impl Future + Send`.
Comprehensive deep debt audit across all dimensions found zero violations.

---

## Coverage Sprint: 87% → 90.3%

### Strategy
Targeted pure-Rust, unit-testable components first (store backends, core type
serialization, compression strategy branches), deferring Docker-dependent
Postgres integration tests. Used `cargo llvm-cov --lcov` with `DA:,0$` grep
to pinpoint exact uncovered lines for surgical test placement.

### New Test Categories (101 tests added)
- **Compression engine**: Split strategy (diamond DAG), Hierarchical strategy (with/without summary)
- **Compression analyzer**: Direct `SessionAnalysis` construction testing Single/Atomic hints, low-convergence Split, deep Hierarchical (2-level and 3-level)
- **Store backends (redb + sled)**: derived_from semantics with parent/child, multi-tag index cleanup, pagination edge cases, agent filter exclusion, time-based ordering, corruption handling
- **Core types**: JSON serde roundtrips for BraidType Collection/Delegation/Slice, AgentType variants, EntityReference variants (ById, ByLoamEntry, External with/without hash)
- **Config**: XDG and HOME config discovery paths, SWEETGRASS_CONFIG non-file, default_name, load delegation
- **Activity**: From<&str>/From<String> for ActivityId, Custom variant Display
- **Object memory**: with_metadata builder, Default impl, derivation export formatting
- **Witness chain**: store→witness→verify round-trip (primalSpring audit action)
- **BTSP**: write_frame oversized rejection, resolve_security_socket, env-wiring
- **Dehydration**: from_ed25519, is_signed, defaults, multi-witness round-trip

---

## Smart Refactoring: braid/types.rs

### Problem
`braid/types.rs` at 1,138 lines — only file exceeding the 1,000-line workspace standard.

### Solution
Extracted `BraidType` + `SummaryType` and all dual-format serialization
machinery (internally-tagged JSON via `BraidTypeJson`, externally-tagged
bincode via `BraidTypeBin`, four `From` impls, custom `Serialize`/`Deserialize`)
into `braid/braid_type.rs` (275 lines). Semantic split by domain boundary —
type classification system vs identity/metadata types — not mechanical
line-count splitting.

| File | Before | After |
|------|--------|-------|
| `braid/types.rs` | 1,138 | 856 |
| `braid/braid_type.rs` | — | 275 |

Re-exports via `pub use super::braid_type::{BraidType, SummaryType}` in
`types.rs` — zero changes to any downstream consumer imports.

---

## async-trait Evolution

### Migrated Traits (no `dyn` usage — safe to migrate)
- **`IndexStore`** (6 async methods) — `sweet-grass-store/src/traits/mod.rs`
- **`Signer`** (2 async + 1 sync method) — `sweet-grass-integration/src/signer/traits.rs`

### Pattern
```rust
// Before (async_trait crate — allocates Pin<Box<dyn Future>>)
#[async_trait]
pub trait Signer: Send + Sync {
    async fn sign_braid(&self, braid: &Braid) -> Result<Braid>;
}

// After (native Rust 2024 — zero-alloc, compiler-resolved)
pub trait Signer: Send + Sync {
    fn sign_braid(&self, braid: &Braid) -> impl Future<Output = Result<Braid>> + Send;
}
```

### Remaining (6 traits — need `dyn` dispatch, require async_trait)
`BraidStore`, `SigningClient`, `PrimalDiscovery`, `AnchoringClient`,
`SessionEventsClient`, `SessionEventStream` — all used as `Arc<dyn Trait>`
or `Box<dyn Trait>`. Migration requires `trait_variant::make` or equivalent
when ecosystem support matures.

---

## Deep Debt Audit Results

| Dimension | Result |
|-----------|--------|
| Hardcoded primal names/ports | Zero in production — all capability/env-based |
| Mocks in production | All gated `#[cfg(test)]` / `feature = "test"` |
| Unsafe code | Zero blocks; `#![forbid(unsafe_code)]` all 11 crate roots |
| TODO/FIXME/HACK | Zero markers |
| `#[allow(dead_code)]` | Zero instances |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| sqlx purity | Pure Rust wire protocol (no libpq); TLS not enabled |
| Files >1000 lines | Zero (max: 958 lines, test file) |
| Debris (.bak/.tmp/.orig) | Zero |
| archive/ directory | Does not exist |

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,315 | 1,416 |
| Line coverage | ~87% | 90.3% |
| Function coverage | — | 86.2% |
| Region coverage | — | 92.4% |
| .rs files | 167 | 168 |
| LOC | 44,516 | 48,719 |
| Max file (production) | 574 | 856 (types.rs, down from 1,138) |
| Max file (test) | 734 | 958 |
| Clippy warnings | 0 | 0 |
| async-trait traits | 8 | 6 (2 migrated to native) |

---

## Ecosystem Impact

### For primalSpring Compliance Matrix
- Coverage target **ACHIEVED** — sweetGrass 90.3% (target was 90%)
- Witness chain validation **DONE** — store→witness→verify round-trip test
- Deep debt audit **COMPLETE** — all dimensions clean

### For Trio Partners
- `IndexStore` and `Signer` native async pattern recommended for adoption
  in non-`dyn` traits across rhizoCrypt and loamSpine
- `braid_type.rs` extraction pattern usable for any >1000-line type module

### Remaining Known Gaps

| Gap | Priority | Notes |
|-----|----------|-------|
| Postgres CI coverage | Low | Needs Docker in CI; error paths covered |
| BTSP Phase 3 (encrypted framing) | Deferred | Ecosystem-wide decision |
| async-trait for 6 dyn traits | Deferred | Needs trait_variant or equivalent |
| sled deprecation | Feature-gated | redb is primary; sled optional |
| NUCLEUS mesh witness validation | Low | Per primalSpring audit; low urgency |
