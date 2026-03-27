<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- Creative content: CC-BY-SA 4.0 (scyBorg provenance trio) -->

# BearDog v0.9.0 — Wave 13: Deep Debt Elimination, Pedantic Clippy, Zero-Copy & Coverage Push

**Date**: March 24, 2026
**Version**: 0.9.0
**Edition**: 2024 | **MSRV**: 1.93.0

---

## Summary

Comprehensive deep-debt wave executing on a full audit of the codebase against
wateringHole standards. Eliminated 1,149 clippy errors across the entire
workspace, extracted 60+ magic numbers to named constants, performed zero-copy
optimization on clone-heavy production files, added 150 new tests, cleaned
stale docs and debris, created CONTEXT.md per PUBLIC_SURFACE_STANDARD, and
established scyBorg license compliance with LICENSE-DOCS.md.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 14,201 | **14,351** |
| Coverage | 87.0% | 87.0%+ (150 new tests; re-measure with llvm-cov) |
| Clippy errors (`-D warnings`) | **1,149** across 13+ crates | **0** workspace-wide |
| Magic number literals | 60+ bare | **Named constants** (`SECONDS_PER_HOUR`, etc.) |
| `.clone()` in hot paths | 24 per file (software_hsm, key_mgmt) | Reduced via destructuring/move |
| CONTEXT.md | Missing | **Created** (56 lines) |
| LICENSE-DOCS.md | Missing | **Created** (CC-BY-SA 4.0) |
| Stale test counts in docs | 5 files at 14,201 | **All aligned to 14,351** |
| showcase README freshness | Dec 2025, 1/38 demos | **Mar 2026, 29 demos** |

---

## Changes

### Clippy — 1,149 Errors Eliminated

Every workspace crate now passes `cargo clippy --all-targets --all-features -- -D warnings`.

**Test lint isolation** — Every crate `lib.rs` received
`#![cfg_attr(test, allow(clippy::expect_used, clippy::unwrap_used))]`. All
integration test files (`tests/*.rs`) received file-level
`#![allow(clippy::expect_used, clippy::unwrap_used)]`. Production code remains
fully strict.

**Mechanical fixes** (by category):
- `uninlined_format_args` (114) — `format!("{x}")` style
- `redundant_closure` (30) — function references
- `float_cmp` (8) — epsilon helpers in test code (`float_eq` / `near_f64`)
- `long_literal_lacking_separators` (8) — `1_735_000_000` style
- `redundant_clone` (5) — eliminated
- `hand_coded_ip_address` (4) — `Ipv4Addr::LOCALHOST` / `UNSPECIFIED`
- `single_char_pattern`, `empty_string_manually`, `needless_collect`,
  `io_other_error`, `default_constructed_unit_structs`, `module_inception`,
  `implicit_clone`, `case_sensitive_file_extension_comparisons`, and more

**Affected crates**: beardog-errors, beardog-config, beardog-deploy, beardog-hid,
beardog-capabilities, beardog-discovery, beardog-installer, beardog-threat,
beardog-tower-atomic, beardog-traits, beardog-types, beardog-workflows,
beardog-security, beardog-utils, beardog-compliance, beardog-adapters,
beardog-monitoring, beardog-genetics, beardog-auth, beardog-client,
beardog-core, beardog-tunnel, beardog-cli, beardog-ipc, beardog-integration,
beardog (root).

### Magic Number Extraction

60+ bare numeric literals in `beardog-types` default implementations → named
constants in `constants/mod.rs`:

- `constants::time::SECONDS_PER_HOUR` (3600)
- `constants::time::SECONDS_PER_DAY` (86400)
- `constants::defaults::DEFAULT_MAX_ENTRIES` (10,000)
- `constants::defaults::DEFAULT_MAX_RESPONSE_TIME_MS` (5000)
- `constants::defaults::DEFAULT_MAX_GENERATIONS` (1000)

Applied across 25+ production files: crypto, HSM, monitoring, security,
relationships, genetics, discovery, providers.

### Zero-Copy Optimization

Clone-heavy production files evolved:

- **key_export.rs**: Destructure `StoredKey`/`ExportedKey` — move fields, no
  per-field clone
- **key_management.rs**: Serialize-by-reference under read lock, move on insert
- **software_hsm/core.rs**: Reuse lookup key string for `KeyInfo::key_id`
- **android_strongbox/core.rs**: Move-from-spec instead of clone-then-build
- **api_server.rs**: Single `node_id` clone, move into map
- **deployment.rs**: `update_progress` takes `&PrimalName`, fewer clones per
  deploy iteration

### 150 New Tests

| Crate | Tests Added | Focus |
|-------|-------------|-------|
| beardog-cli | 26 | Clap parsing, endpoint URL branches |
| beardog-deploy | 25 | Mock ADB, device manager fallbacks |
| beardog-tunnel | 23 | BStpConfig, graph security serde, doctor |
| beardog-types | 26 | Receipt validation, key constraints, certificates |
| beardog-core | 25 | Socket config, capabilities, discovery serde |
| beardog-installer | 25 | Architecture display, errors, platform, binary validator |

### Documentation Alignment

- **CONTEXT.md** created at repo root (56 lines, per PUBLIC_SURFACE_STANDARD)
- **LICENSE-DOCS.md** created (CC-BY-SA 4.0 for docs/specs per scyBorg)
- **README.md**, **ARCHITECTURE.md**, **START_HERE.md**, **ROADMAP.md**,
  **CHANGELOG.md**, **specs/README.md**, **specs/PROJECT_STATUS.md** all
  updated to 14,351 tests
- **showcase/README.md**, **00_START_HERE.md**, **00_SHOWCASE_INDEX.md** updated
  from "6 unsafe / Dec 2025 / 1 demo" to "0 unsafe / Mar 2026 / 29 demos"
- **tests/README.md**, **docs/references/DEPLOYMENT_GUIDE.md** stale counts
  replaced with pointers to STATUS.md
- **showcase/05-mixed-entropy/README.md** created (was missing)

### Debris Cleanup

- Removed stale `audit.log` files (gitignored artifacts)
- Removed `showcase/**/target/` build artifacts
- No `.bak`, `.tmp`, `~` files found

---

## Gates

```bash
cargo fmt --all -- --check                      # Clean
cargo clippy --workspace --all-targets \
  --all-features -- -D warnings                 # 0 warnings
cargo doc --workspace --no-deps                 # Clean
cargo test --workspace                          # 14,351 passed, 0 failed
```

---

## What's Next (Wave 14 Candidates)

- **Coverage → 90%**: Re-measure with llvm-cov; target `beardog-integration`
  (32% lib.rs), `beardog-tower-atomic` (85%), remaining error paths in types/config
- **AGPL-3.0-only vs -or-later**: Clarify with ecosystem (scyBorg says "or-later",
  Cargo.toml says "only")
- **Deeper zero-copy**: `Arc<str>` in public types for shared immutable strings;
  `Cow<'_, str>` in config paths
- **beardog-integration evolution**: Tower Atomic UPA client coverage is low (32%);
  needs mock server or capability-based test harness
- **Semantic method naming audit**: Full pass against
  `SEMANTIC_METHOD_NAMING_STANDARD.md` v2.1.0 for any missing aliases
- **genomeBin manifest update**: If coverage reaches 90%, update
  `wateringHole/genomeBin/manifest.toml` checksums

---

## Files Changed (Summary)

- **~200+ files** across 26 crates (clippy fixes, test additions, constant extraction)
- **6 new files**: CONTEXT.md, LICENSE-DOCS.md, 4 test modules
  (coverage_expansion_march_2026.rs, deploy_coverage_wave2.rs,
  tunnel_coverage_wave2.rs, coverage_march26_types_wave.rs,
  coverage_march26_core_wave.rs, coverage_march26_installer_wave.rs)
- **~15 doc files** updated for metrics alignment
- **1 showcase README** created (05-mixed-entropy)
