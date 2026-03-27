<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# LoamSpine v0.8.2 — Certificate Storage Trait, Waypoint Types, Smart Refactoring

**Date**: March 14, 2026
**Primal**: LoamSpine (permanence layer)
**Version**: 0.8.1 → 0.8.2
**Type**: Architectural evolution, spec implementation, smart refactoring

---

## Summary

Certificate storage evolved from raw `Arc<RwLock<HashMap>>` to a proper
`CertificateStorage` async trait with `InMemoryCertificateStorage`
implementation. Waypoint data model implemented per WAYPOINT_SEMANTICS.md spec.
Two 783-line files (`discovery.rs`, `manager.rs`) smart-refactored into module
directories. `must_use_candidate` lint enabled crate-wide. Critical
`MintInfo.entry` bug fixed (was `[0u8; 32]`, now stores actual entry hash).
All quality gates green: 744 tests, 0 clippy/doc warnings, max file 422 lines.

---

## What Changed

### Certificate Storage Trait
- New `CertificateStorage` async trait in `storage/mod.rs` with `get`, `save`,
  `delete`, `list` methods
- `InMemoryCertificateStorage` in `storage/memory.rs`
- `LoamSpineService.certificates` field → `certificate_storage: InMemoryCertificateStorage`
- All certificate CRUD methods migrated to use the trait

### Certificate Spec Gaps Filled
- `verify_certificate`: Returns `CertificateVerification` with granular
  `VerificationCheck` enum (Exists, SpineExists, MintEntryExists, ChainValid)
- `certificate_lifecycle`: Filtered entry history for a specific certificate
  (renamed from `get_certificate_history` to avoid `ProvenanceSource` trait shadowing)

### Waypoint Types (per WAYPOINT_SEMANTICS.md)
- `WaypointConfig`: Spine configuration for waypoint spines
- `PropagationPolicy`: `None`, `OnReturn`, `OnExpiry`, `Always`
- `DepartureReason`: `Returned`, `Expired`, `Revoked`, `Transferred`
- `WaypointSummary`: Usage summary on departure
- `SliceOperationType`: `Read`, `Write`, `Transform`, `Annotate`
- `SliceTerms`: Duration, operation limits, propagation policy
- Service methods: `record_operation`, `depart_slice`

### Smart Refactoring
| Before | After |
|--------|-------|
| `discovery.rs` (783 lines) | `discovery/mod.rs` (337) + `dyn_traits.rs` (117) + `tests.rs` (345) |
| `manager.rs` (783 lines) | `manager/mod.rs` (299) + `tests.rs` (422) |

### Lint Evolution
- Removed `#![allow(clippy::must_use_candidate)]` from `lib.rs`
- `cargo fix` applied `#[must_use]` to 11 public functions
- All remaining `#[allow]` attributes audited and confirmed justified

### Bug Fix
- `MintInfo.entry` was hardcoded to `[0u8; 32]` — now correctly stores
  the computed entry hash from minting

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Version | 0.8.1 | 0.8.2 |
| Tests | 700 | 744 (+44) |
| Source files | 88 | 92+ (+4 from module refactoring) |
| Max file size | 810 | 422 |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| Unsafe code | 0 | 0 |
| C deps (default) | 0 | 0 |

---

## Inter-Primal Notes

### biomeOS
- NeuralAPI integration unchanged. 19 capabilities registered at startup.
- New waypoint types ready for biomeOS graph coordination.

### rhizoCrypt
- `permanent-storage.*` compat layer unchanged.
- `certificate_lifecycle` provides richer history for dehydration provenance.

### sweetGrass
- `braid.commit` unchanged.
- `CertificateVerification` enables stronger attribution chain validation.

---

## Known Remaining Items

1. **Sled/SQLite CertificateStorage**: Only in-memory impl exists.
   Sled and SQLite backends need `CertificateStorage` implementations.
2. **Waypoint relending**: `SliceTerms.allow_relend` defined but relend
   chain logic not yet implemented.
3. **Waypoint expiry sweep**: No background task for auto-returning expired anchors.
4. **Certificate escrow**: `TransferConditions` not yet implemented.
5. **Coverage**: ~91% estimated but not re-measured with llvm-cov this session.
6. **Showcase demos**: ~10% complete.

---

## Files Changed

Key files (not exhaustive):
- `Cargo.toml` (workspace version → 0.8.2)
- `primal-capabilities.toml` (version → 0.8.2)
- `crates/loam-spine-core/src/storage/mod.rs` (CertificateStorage trait)
- `crates/loam-spine-core/src/storage/memory.rs` (InMemoryCertificateStorage)
- `crates/loam-spine-core/src/storage/tests.rs` (new certificate storage tests)
- `crates/loam-spine-core/src/service/mod.rs` (certificate_storage field)
- `crates/loam-spine-core/src/service/certificate.rs` (verify, lifecycle, storage migration)
- `crates/loam-spine-core/src/service/waypoint.rs` (record_operation, depart_slice)
- `crates/loam-spine-core/src/waypoint.rs` (new — waypoint types)
- `crates/loam-spine-core/src/discovery/` (new directory — refactored)
- `crates/loam-spine-core/src/discovery/dyn_traits.rs` (extracted DynSigner/DynVerifier)
- `crates/loam-spine-core/src/manager/` (new directory — refactored)
- `crates/loam-spine-core/src/lib.rs` (must_use_candidate, waypoint module)
- `README.md`, `CHANGELOG.md`, `STATUS.md`, `WHATS_NEXT.md`, `CONTRIBUTING.md`
- `docs/planning/KNOWN_ISSUES.md`
