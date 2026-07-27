# cellMembrane Wave 155b — Fleet Convergence (Checksum + Topology)

**Date**: 2026-07-27 | **Wave**: 155b | **Author**: cellMembrane team (sporeGate)
**Trigger**: Track B Fleet Convergence — compositions fixed, blueGate joining as builder

---

## Summary

Checksum verification fix enables all depot formats (struct + plain-string) to
parse correctly during bootstrap enrollment. Topology updated for blueGate
(distributed builder) and westGate (cold storage). Build authority foreman
pattern already supported — no new code needed.

## Changes

### 1. Checksum Format Fix (P0)

`gate/verify.rs` had a private `ChecksumEntry` struct requiring `{ blake3, size }` —
could not parse legacy plain-string `"hash"` entries in `checksums.toml`. Migrated
to the shared `parse_checksums_toml()` from `plasmid/checksum.rs` which handles both
formats. `checksum` module promoted from `mod` to `pub(crate) mod`.

**Before**: bootstrap enrollment failed `checksum.local` phase on gates with
plain-string depot format.

**After**: all 5 enrolling gates pass 12/13 bootstrap phases.

### 2. Topology (blueGate + westGate)

| Gate | Zone | MESH_REGISTRY | WG IP |
|------|------|---------------|-------|
| blueGate | Backbone | Added | Pending allocation |
| westGate | House1 | Added | Pending allocation |

Both added to `KNOWN_GATES` const array. Zone fallback `for_gate()` updated.

### 3. Build Authority (verified)

Already implemented — no code changes needed:
- `ENV_BUILD_AUTHORITY` constant in `service/constants.rs`
- `build_authority` field in manifest `GateProfile`
- `is_build_authority()` check in cascade post-sync flow
- Foreman pattern is a deployment config, not a code pattern

### 4. Composition Profiles (verified)

Upstream manifest fix (compute/nest now include Tower base primals) is correct.
Code already handles this:
- `parse_name("compute")` → `Tower` (trust level)
- `parse_name("nest")` → `Nest` (trust level)
- Manifest profile controls which primals to deploy
- `CompositionSpec::from_registry()` builds primal lists from service registry

## Changed Files

| File | Change |
|------|--------|
| `gate/verify.rs` | Migrated to shared `parse_checksums_toml()`, tests updated |
| `plasmid/checksum.rs` | `parse_checksums_toml` promoted to `pub(crate)` |
| `plasmid/mod.rs` | `checksum` module promoted to `pub(crate)` |
| `cytoplasm.rs` | blueGate + westGate in `MESH_REGISTRY`, `KNOWN_GATES`, zone fallbacks |
| `gate/enroll.rs` | Clippy fix (uninlined format args in test) |

## Health Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,175 (was 1,167) |
| Clippy warnings | 0 |
| Files >800L | 0 |

## For eastGate Overwatch

cellMembrane Wave 155b: **DONE**. The checksum fix unblocks enrollment for all
depot formats. blueGate/westGate are known to the topology but need WG IP
allocation before mesh enrollment. sporeGate build authority is ready —
`MEMBRANE_BUILD_AUTHORITY=1` + `membrane plasmid.harvest` will trigger
auto-builds when cascade detects drift.
