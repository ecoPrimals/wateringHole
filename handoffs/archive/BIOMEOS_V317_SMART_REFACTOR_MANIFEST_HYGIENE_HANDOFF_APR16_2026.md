# biomeOS v3.17 — Smart Refactoring, Dependency Pruning, Manifest Hygiene

**Date**: April 16, 2026
**Primal**: biomeOS
**From**: biomeOS team
**Scope**: fractal.rs refactoring, unused dependency removal, manifest standardization

---

## Smart Refactoring: fractal.rs (804L -> 3 files, 719L)

The sole remaining production file >800 LOC was `crates/biomeos-compute/src/fractal.rs` (804 lines). Split into:

| File | Lines | Content |
|------|-------|---------|
| `fractal/mod.rs` | 229 | `FractalBuilder` + recursive construction |
| `fractal/leaf.rs` | 169 | `LeafNode` — direct workload execution |
| `fractal/parent.rs` | 321 | `ParentNode` — child delegation |

**Key insight**: `ParentNode` contained 12 methods that manually matched `ComputeNodeKind::Leaf(n) => n.method()` / `ComputeNodeKind::Parent(n) => n.method()` — identical to the dispatch already provided by `ComputeNodeKind` in `node/mod.rs`. Replaced all 12 with `child.method()`, eliminating ~85 lines of redundant pattern matching.

Additional improvements:
- Added `ResourceInfo::zeroed()` for cleaner accumulator initialization
- Fixed `future_not_send` nursery warning on `build_node_recursive` (`+ Send` bound)
- Test re-exports gated behind `#[cfg(test)]`

---

## Dependency Pruning

| Change | Crate | Rationale |
|--------|-------|-----------|
| Removed `tokio` | `biomeos-types` | Declared but never imported; only pulled transitively via tarpc |
| Removed `validation = []` feature | `biomeos-types` | Placeholder feature never gated on |
| Removed `metrics = []` feature | `biomeos-types` | Placeholder feature never gated on |

---

## Manifest Hygiene

### Repository URL Standardization
All crate `Cargo.toml` files now use `https://github.com/ecoPrimals/biomeOS`.

Previously inconsistent:
- `https://github.com/your-org/biomeos` (biomeos-types, biomeos-system, biomeos-manifest)
- `https://github.com/biomeOS/biomeOS` (workspace root)
- `https://github.com/ecoPrimals/biomeOS` (some crates — correct)

### Missing Description Fields Added
- `biomeos-api`: "HTTP/WebSocket API server for biomeOS Neural API and discovery"
- `biomeos-atomic-deploy`: "Atomic graph deployment, Neural API routing, and primal lifecycle management"
- `biomeos-test-utils`: "Shared test utilities, fixtures, and helpers for the biomeOS workspace"

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | PASS |
| `cargo clippy --workspace --all-targets` | PASS (0 warnings) |
| `cargo test --workspace` | 7,801 passing, 0 failures |
| `cargo fmt --all -- --check` | PASS |
| Production files >800 LOC | 0 (max: 799) |

---

## Audit Summary (no action needed)

The following were audited and found clean:
- **Unsafe code**: 0 (only `forbid(unsafe_code)` attributes)
- **TODO/FIXME/HACK**: 0 in production code
- **Mocks in production**: 0 (all `Mock*` types inside `#[cfg(test)]`)
- **Primal names**: All use `primal_names::` constants; description strings in niche catalog are intentional
- **Dependencies**: Already pure-Rust biased (blake3 pure, ureq without TLS)
- **`dead_code` suppressions**: All legitimate (serde deserialization in tests)

---

## Remaining Watch Items

| Item | Priority | Notes |
|------|----------|-------|
| `serde-saphyr` 0.0.x | Watch | Pre-1.0 semver; track releases |
| `rtnetlink` native subtree | Acceptable | Linux-specific, appropriate for RTNETLINK |
| `node_handlers.rs` (799L) | Monitor | One line under threshold; natural candidate if growth occurs |

---

**Tests**: 7,801 passing | **Clippy**: 0 warnings | **Files >800 LOC**: 0 production | **Unused deps**: pruned | **Manifests**: standardized
