<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — scyBorg License Alignment, Zero-Copy Signing, Audit Cleanup

**Date**: March 15, 2026 (session 7)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: License compliance + zero-copy optimization + smart refactoring + docs cleanup
**Supersedes**: `RHIZOCRYPT_V013_DEEP_DEBT_IDIOMATIC_RUST_HANDOFF_MAR15_2026.md`

---

## Summary

Comprehensive audit against specs/ and wateringHole standards, executed on all
findings. Aligned licensing to scyBorg standard (AGPL-3.0-or-later) across all
105 source files and configs. Smart-refactored store_redb.rs to eliminate
`#[allow(too_many_lines)]`. Added zero-copy signing paths. Modernized async
trait implementations via RPITIT. Hardened metrics casting. Cleaned all root
docs, fixed stale ports/vars/counts, archived legacy spec, and removed showcase
debris. All quality gates green.

1. **882+ tests passing** (default features) — 0 failures.

2. **90.88% line coverage** (llvm-cov verified).

3. **AGPL-3.0-or-later** across all 105 `.rs` files, `Cargo.toml`, `deny.toml`,
   `Dockerfile`, CI workflow, and all documentation — aligned with scyBorg
   licensing standard.

4. **Zero-copy signing** — `sign_owned(Bytes)` / `verify_owned(Bytes)` paths
   in signing capability client; `sign_vertex` uses `Bytes::from(Vec<u8>)`
   (ownership transfer) instead of `copy_from_slice`.

5. **Smart refactor** — `store_redb.rs` `put_vertex` reduced via extracted
   `read_vertex_set` / `write_vertex_set` helpers, eliminating
   `#[allow(clippy::too_many_lines)]`.

6. **Modern async traits** — `loamspine_http.rs` `PermanentStorageProvider`
   impl converted from `fn -> impl Future { async move }` to `async fn`
   (RPITIT), removing pre-async-block cloning.

7. **Docs cleanup** — Rewrote `DEPLOYMENT_CHECKLIST.md` (port 9400, redb/sled,
   JSON-RPC health), fixed `ENV_VARS.md` (`RHIZOCRYPT_DISCOVERY_ADAPTER` as
   primary), updated `README.md` metrics, fixed broken spec links, updated
   showcase to port 9400, fixed Dockerfile image tag.

---

## Changes

### License Alignment (AGPL-3.0-only → AGPL-3.0-or-later)

| Scope | Count |
|-------|-------|
| `.rs` source files (SPDX headers) | 105 |
| `Cargo.toml` (workspace) | 1 |
| `deny.toml` | 1 |
| `Dockerfile` | 1 |
| `.github/workflows/ci.yml` | 1 |
| Documentation files | 5+ |

### Smart Refactoring — `store_redb.rs`

| Method | Before | After |
|--------|--------|-------|
| `put_vertex` | ~120 lines, `#[allow(clippy::too_many_lines)]` | ~45 lines, delegating to helpers |
| `read_vertex_set` | (new) | Reads + deserializes vertex set from any table |
| `write_vertex_set` | (new) | Serializes + writes vertex set to any table |
| `Debug` impl | `#[allow(clippy::missing_fields_in_debug)]` | `finish_non_exhaustive()` |

### Zero-Copy Signing (`signing.rs`)

| Method | Change |
|--------|--------|
| `sign_owned(Bytes, &Did)` | New zero-copy entry point |
| `verify_owned(Bytes, &Signature, &Did)` | New zero-copy entry point |
| `sign_vertex` | `Bytes::from(Vec<u8>)` instead of `copy_from_slice` |
| `verify_vertex` | `Bytes::from(Vec<u8>)` instead of `copy_from_slice` |

### Metrics Hardening (`metrics.rs`)

| Issue | Resolution |
|-------|------------|
| Duplicate padding in `ALL_METHODS` | `RPC_METHOD_COUNT` / `ERROR_TYPE_COUNT` constants |
| Unsafe `f64` → `u64` cast | `is_finite()` + positivity check, scoped `#[allow]` |

### Modern Async Traits (`loamspine_http.rs`)

| Before | After |
|--------|-------|
| `fn commit(...) -> impl Future { async move { ... } }` | `async fn commit(...)` |
| `#[allow(clippy::manual_async_fn)]` | Removed |
| Pre-async-block `.clone()` on all args | Eliminated (direct reference) |

### Idiomatic Patterns

| File | Before | After |
|------|--------|-------|
| `capability.rs` | `.map(\|x\| { warn; x })` + `#[allow(manual_inspect)]` | `Option::inspect()` |
| `store_sled.rs` | `#[allow(type_complexity)]` on `export()` | `SledExportEntry` type alias |
| `store_sled.rs` | `#[allow(missing_fields_in_debug)]` | `finish_non_exhaustive()` |
| `doctor.rs` | Missing `#[must_use]` and `# Errors` | Added per pedantic clippy |

### Documentation Cleanup

| File | Change |
|------|--------|
| `docs/DEPLOYMENT_CHECKLIST.md` | Major rewrite: port 9400, 882+ tests, redb/sled, JSON-RPC health |
| `docs/ENV_VARS.md` | `RHIZOCRYPT_DISCOVERY_ADAPTER` primary, `RHIZOCRYPT_PORT` matches code |
| `README.md` | Test count 882+, coverage 90.88%, 105 `.rs` files |
| `CHANGELOG.md` | Added session 7 entry |
| `specs/00_SPECIFICATIONS_INDEX.md` | Fixed broken link to archived integration spec |
| `specs/API_SPECIFICATION.md` | Fixed broken link to archived integration spec |
| `Dockerfile` | `rust:1.92-slim` → `rust:1.85-slim` |
| `rhizocrypt-service/README.md` | Docker example `rust:1.75` → `rust:1.85-slim` |
| `.gitignore` | Added `*.bak` |
| Showcase `08-production-features/` | Port 7777 → 9400, `SONGBIRD_ADDRESS` → `RHIZOCRYPT_DISCOVERY_ADAPTER` |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace` | 882+ pass, 0 fail (default features) |
| `cargo llvm-cov` | 90.88% line coverage |
| `#![forbid(unsafe_code)]` | Workspace-wide (all entry points) |
| SPDX headers | All 105 `.rs` files (AGPL-3.0-or-later) |
| Max file size | All under 1000 lines |
| `cargo-deny` | advisories ok, bans ok, licenses ok, sources ok |

---

## Files Modified

```
crates/rhizo-crypt-core/src/store_redb.rs
crates/rhizo-crypt-core/src/store_sled.rs
crates/rhizo-crypt-core/src/clients/capabilities/signing.rs
crates/rhizo-crypt-core/src/clients/loamspine_http.rs
crates/rhizo-crypt-core/src/safe_env/capability.rs
crates/rhizo-crypt-rpc/src/metrics.rs
crates/rhizocrypt-service/src/doctor.rs
All 105 .rs files (SPDX header update)
Cargo.toml
deny.toml
Dockerfile
.github/workflows/ci.yml
.gitignore
README.md
CHANGELOG.md
docs/DEPLOYMENT_CHECKLIST.md
docs/ENV_VARS.md
crates/rhizocrypt-service/README.md
specs/00_SPECIFICATIONS_INDEX.md
specs/API_SPECIFICATION.md
showcase/00-local-primal/08-production-features/demo-service-mode.sh
showcase/00-local-primal/08-production-features/README.md
```

---

## Next Steps

1. Update 11 stale showcase scripts from deprecated `Session::new` API
2. Monitor tarpc upstream for advisory resolution (5 transitive ignores)
3. Evaluate `SmallVec` for store key allocation to reduce heap pressure
4. Add vertex-to-session index for O(1) `verify_proof` lookup
5. Push test count back above 900 (some consolidated during refactor)
