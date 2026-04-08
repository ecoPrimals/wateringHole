# barraCuda v0.3.11 — Sprint 35: Deep Debt — Typed Errors, thiserror & Transport Refactor

**Date**: April 8, 2026
**Primal**: barraCuda
**Version**: 0.3.11
**Supersedes**: BARRACUDA_V0311_BTSP_SOCKET_NAMING_GAP_MATRIX_HANDOFF_APR08_2026 (archived)

---

## Summary

Sprint 35 resolves three deep debt items identified by a comprehensive 12-axis
audit, achieving a clean bill across all production code axes.

## Changes

### Error Evolution

- **`validate_insecure_guard()`**: Evolved from `Result<(), String>` to typed
  `crate::error::Result<()>` returning `BarracudaCoreError::Lifecycle`. This
  eliminates the last `Result<_, String>` return type in production code.
  Callers in the binary simplified (`.map_err(...)` removed).
- **`PppmError`**: Manual `impl Display` + `impl Error` (15 lines) evolved to
  `#[derive(thiserror::Error)]` with `#[error(...)]` attributes (8 lines).
  Identical runtime behavior, idiomatic Rust.

### Smart Refactoring

- **`transport.rs`** (866 → 490 LOC): 380-line `#[cfg(test)] mod tests`
  extracted to `transport_tests.rs` via `#[path = "transport_tests.rs"]`
  attribute. Test behavior unchanged. No production files exceed 800 lines.

### 12-Axis Deep Debt Audit — Clean Bill

| Axis | Status |
|------|--------|
| Large files (>800 LOC) | Clean (max: 490 production, 951 test) |
| Unsafe code | Clean (`#![forbid(unsafe_code)]` on 3 crates) |
| `#[allow(` usage | Clean (zero live instances) |
| `unwrap()`/`expect()`/`panic!()` in production | Clean (all test-only) |
| `println!`/`eprintln!` in libraries | Clean (none in production) |
| `Result<T, String>` / `Box<dyn Error>` | Clean (validate_insecure_guard fixed) |
| Production mocks | Clean (zero) |
| Hardcoded primal routing | Clean (provenance docs only) |
| TODO/FIXME/HACK | Clean (zero in .rs) |
| Commented-out code | Clean (zero) |
| External C dependencies | Clean (wgpu FFI unavoidable, blake3 pure) |
| Manual Display for errors | Clean (PppmError evolved) |

## Files Changed

- `crates/barracuda-core/src/ipc/transport.rs` (866→490 LOC)
- `crates/barracuda-core/src/ipc/transport_tests.rs` (new, 377 LOC)
- `crates/barracuda-core/src/bin/barracuda.rs` (simplified guard calls)
- `crates/barracuda-core/tests/btsp_socket_compliance.rs` (typed error adapt)
- `crates/barracuda/src/ops/md/electrostatics/pppm.rs` (thiserror evolution)

## Quality Gates

- **4,207 tests** pass, 0 fail, 14 skipped (nextest CI profile)
- `cargo fmt --all --check` — clean
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean

## Cumulative Sprint 32–35 Status

| Sprint | Focus | Tests |
|--------|-------|-------|
| 32 | SIGSEGV fix, 12-axis audit | 4,180 |
| 33 | Wire Standard L2, identity.get | 4,187 |
| 34 | BTSP socket naming, BIOMEOS_INSECURE guard | 4,207 |
| 35 | Typed errors, thiserror, transport refactor | 4,207 |

All GAP-MATRIX items resolved. No active gaps.
