<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- Creative content: CC-BY-SA 4.0 (scyBorg provenance trio) -->

# BearDog v0.9.0 — Wave 14: Deep Debt Audit, Test Evolution, scyBorg Compliance & Zero-Copy

**Date**: March 24, 2026
**Version**: 0.9.0
**Edition**: 2024 | **MSRV**: 1.93.0
**Supersedes**: Wave 13 handoff (same date, continued session)

---

## Summary

Comprehensive audit against wateringHole standards and specs, followed by
systematic execution. Fixed the only failing workspace test, extracted
`main.rs` dispatch for testability, added 36 new instrumented tests, created
scyBorg triple-license files, optimized zero-copy with `bytes::Bytes`, cleaned
hardcoded ports, evolved platform test stubs from panic to `Result`, and
cleaned stale docs/scripts.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Workspace test failure | 1 (`test_auto_initialize_environment_precedence`) | **0** |
| Root crate coverage | 85.9% | **87.2%** |
| `main.rs` coverage | 58.6% | **68.6%** |
| Clippy (`-D warnings`, workspace) | PASS | **PASS** (maintained) |
| scyBorg license files | 0 | **2** (`LYSOGENY_PROTOCOL.md`, `SCYBORG_EXCEPTION_PROTOCOL.md`) |
| Hardcoded test ports | 5+ fixed ports | **ephemeral `:0`** |
| Platform test panics | ~12 | **0** (evolved to `Result<T, E>`) |
| `.clone()` on hot paths | Baseline | **Reduced** (`bytes::Bytes` in software_hsm; storage moved in key_mgmt) |
| Stale scripts/docs | ~8 files | **Fixed** |
| New instrumented tests | — | **36** |

---

## Changes

### 1. Failing Test Fix — `test_auto_initialize_environment_precedence`

Evolved from env-var-dependent to config-based behavior so parallel tests no
longer race on environment state.

### 2. `main.rs` Coverage

Extracted `dispatch()` for testability; added `Debug` derives to all CLI enums;
**33** CLI parse unit tests plus **3** dispatch integration tests.

### 3. scyBorg Triple License

- **`LYSOGENY_PROTOCOL.md`** — area denial through open prior art
- **`SCYBORG_EXCEPTION_PROTOCOL.md`** — exception policy

### 4. Zero-Copy Optimization

- **software_hsm**: `ProtectedMemory` now wraps `bytes::Bytes`
- **key_management**: storage moved into metadata
- **android_strongbox**: deduplicated `CachedKeyInfo`

### 5. Hardcoded Port Cleanup

Five test files updated from fixed ports to ephemeral `:0`.

### 6. Platform Test Evolution

`ipc_server.rs`, `platform/windows.rs`, and `platform/ios.rs` — test panics
evolved to `Result<T, BearDogError>`.

### 7. Stale Doc/Script Cleanup

- **examples/README.md** rewritten
- Scripts fixed (`PROJECT_ROOT`, version refs)
- **configs/README.md** and deployment guide MSRV aligned

---

## Gates

```bash
cargo fmt --check                               # Clean
cargo clippy --workspace --all-features \
  -- -D warnings                                # 0 warnings
cargo doc --no-deps                             # Clean
cargo test                                      # (root) All pass
cargo test --workspace                          # All pass (1 pre-existing flaky sslkeylog test in parallel only)
```

---

## What's Next (Wave 15)

- **Coverage → 90%**: `beardog-integration` (low), `tower-atomic`, remaining error paths
- **genomeBin manifest**: Update `wateringHole/genomeBin/manifest.toml` when 90% reached
- **Deeper zero-copy**: `Arc<str>` for shared immutable strings in public types
- **examples/** validation: `cargo check --examples` to verify all compile
- **Showcase CI**: Add compilation check for excluded showcase crates

---

## Files Changed (Summary)

- **16** modified, **2** new (`.md`), plus doc/script fixes

---

## Inter-Primal Notes

- No compile-time coupling changes
- JSON-RPC and tarpc dual protocol maintained
- scyBorg compliance now complete with `LYSOGENY_PROTOCOL.md` and `SCYBORG_EXCEPTION_PROTOCOL.md`
