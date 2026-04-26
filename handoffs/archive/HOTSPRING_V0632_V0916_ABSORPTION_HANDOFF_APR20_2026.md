# hotSpring v0.6.32 — primalSpring v0.9.16 Absorption Handoff

**Date:** April 20, 2026
**From:** hotSpring
**To:** primalSpring auditors, sibling springs
**License:** AGPL-3.0-or-later

---

## Summary

hotSpring has absorbed primalSpring v0.9.16 patterns into its guideStone binary.
Three changes: BLAKE3 checksums for Property 3, protocol tolerance for
HTTP-on-UDS primals, and family-aware discovery (inherited automatically).

hotSpring remains at guideStone Level 5 CERTIFIED. The `hotspring_guidestone`
binary is validated as compiling against primalSpring v0.9.16 APIs.

---

## What Changed

### 1. Property 3 — BLAKE3 Checksums

**Before:** Manual `validation/CHECKSUMS` file-exists check with line count.

**After:** `primalspring::checksums::verify_manifest(&mut v, "validation/CHECKSUMS")`
— per-file BLAKE3 hash verification. PASS if hash matches, FAIL if tampered,
SKIP if manifest or file not found. Standard guideStone Property 3 pattern.

### 2. Protocol Tolerance — `is_protocol_error()`

**Before:** `validate_provenance_witness` and `validate_compute_dispatch` only
handled `is_connection_error()` (SKIP) and generic errors (FAIL).

**After:** Added `is_protocol_error()` arms to both functions. Songbird and
petalTongue speak HTTP on UDS sockets — this is classified as SKIP (reachable
but protocol mismatch), not FAIL. Matches v0.9.16 `validate_liveness()` semantics.

### 3. Family-Aware Discovery

**No code change needed.** `CompositionContext::from_live_discovery_with_fallback()`
inherits the v0.9.16 family-aware discovery automatically. When `FAMILY_ID` is set,
`{capability}-{FAMILY_ID}.sock` is resolved before `{capability}.sock`.

### 4. primalspring Dependency Version

Cargo.lock updated: `primalspring v0.9.15 → v0.9.16`. Path dependency
(`../../primalSpring/ecoPrimal`) auto-resolves to the pulled version.

---

## Patterns Confirmed (for sibling springs)

1. **BLAKE3 is a drop-in.** Replace your manual CHECKSUMS check with one line:
   `checksums::verify_manifest(&mut v, "validation/CHECKSUMS")`. It handles
   missing manifests (SKIP), empty manifests (FAIL), and per-file hash comparison.

2. **Protocol tolerance is two match arms.** For each `ctx.call()` or
   `ctx.hash_bytes()` that might hit Songbird/petalTongue, add:
   ```rust
   Err(e) if e.is_protocol_error() => {
       v.check_skip("check_name", &format!("protocol mismatch: {e}"));
   }
   ```

3. **Family discovery just works.** If you use `CompositionContext`, you get
   family-aware socket resolution for free. Set `FAMILY_ID` env var when
   deploying from plasmidBin.

---

## Files Changed

| File | Change |
|------|--------|
| `barracuda/src/bin/hotspring_guidestone.rs` | BLAKE3 verify_manifest, is_protocol_error() arms, v0.9.16 doc ref |
| `CHANGELOG.md` | v0.9.16 absorption session |
| `README.md` | v0.9.16 ref, BLAKE3 Property 3 evidence |
| `docs/PRIMAL_GAPS.md` | GAP-HS-034 resolved (v0.9.16 absorption) |

---

## Readiness

| Check | Status |
|-------|--------|
| `cargo check --bin hotspring_guidestone` | PASS (primalspring v0.9.16) |
| BLAKE3 checksums integration | verify_manifest() wired |
| Protocol tolerance | is_protocol_error() → SKIP |
| Family-aware discovery | Inherited via CompositionContext |
| guideStone Level | 5 — CERTIFIED (unchanged) |
