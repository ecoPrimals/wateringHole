# biomeOS v3.08 — Zero C Dependencies & Deep Debt Audit Clean

**Date**: April 13, 2026
**From**: biomeOS primal team
**To**: primalSpring, downstream springs
**License**: AGPL-3.0-or-later

---

## Summary

biomeOS v3.08 eliminates the last remaining C dependency and confirms a
comprehensive deep debt audit across all dimensions.

## Changes

### gethostname → rustix::system::uname()

The `gethostname` crate (which uses libc FFI for hostname resolution) was the
last C dependency in the biomeOS workspace. Replaced with `rustix::system::uname()`
which uses the linux_raw backend (pure Rust syscall wrappers, no libc).

**Files changed**:
- `biomeos-spore/src/incubation/local_entropy.rs` — MAC entropy derivation
- `biomeos-system/src/lib.rs` — system hostname reporting
- `biomeos-core/src/capabilities.rs` — primal identity generation
- All 3 Cargo.toml files: removed `gethostname`, added `"system"` feature to `rustix`
- Root `Cargo.toml`: removed workspace `gethostname` definition

**Verification**: `cargo tree -i gethostname` returns "did not match any packages"

### Idiomatic Rust evolution

- `unreachable!()` in `modification.rs` `apply_batch()` evolved to `.expect()`
  with `#[expect(clippy::expect_used, reason = "...")]` lint attribute
- Graph benchmark `.unwrap()` calls evolved to `.expect()` with descriptive messages
- All production `.expect()` calls have descriptive reason strings

## Deep Debt Audit — Comprehensive Results

| Dimension | Count | Status |
|-----------|-------|--------|
| Actual unsafe code | 0 | 51 `#![forbid(unsafe_code)]` policies |
| TODO/FIXME/HACK | 0 | Zero in any .rs file |
| `todo!()`/`unimplemented!()` | 0 | Zero anywhere |
| Production mocks | 0 | All in `biomeos-test-utils` or `#[cfg(test)]` |
| Hardcoded primal names | 0 | All use `primal_names` constants |
| Hardcoded ports | 0 scattered | Centralized in `constants::ports` |
| Production `.unwrap()` | 0 | Zero in non-test src/ |
| Production `.expect()` | 11 | All documented invariant assertions |
| C/FFI dependencies | **0** | `gethostname` was last, now eliminated |
| External deps | All pure Rust | `blake3 features=["pure"]` |
| Files >1000 LOC | 0 | All <835 LOC |
| `#[allow(` in production | 0 | All use `#[expect(reason)]` |

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | **7,784 tests**, 0 failures |
| `cargo tree -i gethostname` | Empty (eliminated) |
| `cargo tree -i ring` | Not in biomeOS tree |

---

*Fossil record: `ecoPrimals/infra/wateringHole/handoffs/`*
