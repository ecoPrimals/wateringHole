<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 41: Documentation Cleanup, Debris Removal, Metric Alignment

**Date**: April 13, 2026
**Primal**: BearDog (cryptographic service provider)
**Scope**: Root doc accuracy, stale link repair, migration debris removal, artifact cleanup

---

## 1. Summary

Wave 41 focused on documentation hygiene: unifying conflicting metrics across root docs, removing migration debris, fixing broken spec links that pointed to archived files, refreshing stale test READMEs, and cleaning untracked build artifacts.

---

## 2. Root Document Metric Alignment

Three numbers diverged across `README.md`, `ARCHITECTURE.md`, `CONTEXT.md`, and `STATUS.md`:

| Metric | Before (varied) | Canonical | Files Fixed |
|--------|-----------------|-----------|-------------|
| JSON-RPC methods | 97 (README, ARCH, CONTEXT) vs 99 (STATUS) | **99** | README.md, ARCHITECTURE.md, CONTEXT.md |
| Rust files | 1,967 (README quality table) vs 2,150 (STATUS) | **2,150** | README.md |
| Test count | 14,906+ (README quality table) vs 14,780+ (STATUS/headline) | **14,780+** | README.md |

The 14,906+ was a historical peak from Wave 38; test consolidation during later waves reduced the count. All root docs now report the same canonical floor.

---

## 3. Migration Test Debris Removed

| File | Status |
|------|--------|
| `tests/simple_core_tests_migrated.rs` | **Deleted** — older subset of `simple_core_tests.rs` |
| `tests/adapter_integration_tests_migrated.rs` | **Deleted** — byte-identical to `adapter_integration_tests.rs` |

---

## 4. Broken Spec Links Fixed

| Spec File | Broken Reference | Resolution |
|-----------|-----------------|------------|
| `specs/current/production/PRODUCTION_READINESS_SPECIFICATION.md` | `COMPREHENSIVE_AUDIT_OCT_3_2025_EVENING_FINAL.md` | Redirected to `STATUS.md` |
| `specs/current/testing/VENDOR_AGNOSTIC_TESTING_MATRIX.md` | `⭐_VENDOR_CLEANUP_COMPLETE_NOV_5_2025.md`, `TESTING_GUIDE.md`, `HARDWARE_SETUP.md` | Consolidated to `STATUS.md` |
| `specs/current/security/SECURITY_SENTINEL_SPECIFICATION.md` | `archive/2025-01-beardog-audit-completion/...` (2 files) | Annotated as ecoPrimals fossil record |

---

## 5. Test READMEs Refreshed

| File | Before | After |
|------|--------|-------|
| `tests/chaos/README.md` | 362 lines, emoji-heavy, October 2025 | Concise module table, April 2026 |
| `tests/e2e/README.md` | 432 lines, emoji-heavy, October 2025 | Concise scenario table, April 2026 |

---

## 6. `.env.example` Realigned

Removed HTTP-centric vars that don't match the JSON-RPC/NDJSON/Unix socket deployment:
- `BEARDOG_ADMIN_PASSWORD` (no HTTP admin surface)
- `BEARDOG_API_BIND_ADDRESS=0.0.0.0:8080` (Unix socket / IPC, not HTTP bind)
- `BEARDOG_MAX_CONNECTIONS` (connection pool is IPC-internal)
- `BEARDOG_ENABLE_CORS` (no HTTP/browser surface)
- `BEARDOG_TLS_ENABLED` (BTSP handles transport encryption, not TLS on HTTP)

Retained: `LOG_LEVEL`, `ENVIRONMENT`, `HSM_MODE`, `ENABLE_METRICS`, `ENABLE_TRACING`, `REQUEST_TIMEOUT`.

---

## 7. Build Artifacts Cleaned

- **163 receipt JSON files** under `crates/beardog-cli/receipts/` (untracked, gitignored) deleted from disk.

---

## 8. Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo test --workspace` | 14,780+ passing, 0 failures |
| `cargo doc --workspace --no-deps` | 0 warnings |

---

## 9. Remaining Notes

- **Songbird naming** in `specs/` and `showcase/02-ecosystem-integration/01-songbird-btsp/` is intentional historical naming. Songbird references in specifications are fossil-record documentation of the pre-BearDog architecture.
- **`beardog-integration` crate** remains excluded from workspace (overstep; HTTP/REST surface deprecated in favor of JSON-RPC).
- **Per-crate coverage table** in `STATUS.md` reflects April 12, 2026 `llvm-cov` run; future refreshes should update this date.
