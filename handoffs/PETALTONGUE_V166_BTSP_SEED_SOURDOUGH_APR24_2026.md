# petalTongue — BTSP family_seed SOURDOUGH Alignment

**Date:** April 24, 2026
**From:** primalSpring Phase 45c audit finding
**Status:** Resolved — root cause was misleading doc + missing trim, not encoding

---

## Audit Finding

primalSpring reported `load_family_seed()` should base64-encode the raw
hex `FAMILY_SEED` before sending to BearDog. Guidestone error: "BTSP
verification failed: unknown."

## Investigation

Cross-referenced against two canonical documents:

1. **SOURDOUGH_BTSP_RELAY_PATTERN.md** (v1.0.0, April 24, 2026):
   > `FAMILY_SEED` from the environment is a hex string. Pass it to
   > BearDog as-is. Do NOT hex-decode or base64-encode it. Just `trim()`
   > whitespace and send the string.

2. **BTSP_WIRE_CONVERGENCE_APR24_2026.md**:
   > The `family_seed` parameter is the raw hex string from the
   > `FAMILY_SEED` environment variable — NOT base64-encoded bytes.
   > petalTongue — BearDog field alignment (Phase 45c). **PASS**

Both barraCuda (Sprint 44h) and Songbird (Wave 167) **removed** base64
encoding to converge. Adding it to petalTongue would break the standard.

## Root Cause

Two issues found in `load_family_seed()`:

1. **Misleading doc comment** said "Load the base64-encoded family seed"
   but the function returns the raw env string (which is correct per
   SOURDOUGH). Comment was causing confusion in audit.

2. **Missing trim()** — the function used `s.trim()` for the emptiness
   check but returned the untrimmed string. When `FAMILY_SEED` is set
   via shell command substitution (`export FAMILY_SEED=$(cmd)`), trailing
   newlines can survive and cause HMAC byte mismatches.

## Fix Applied

- Doc comment updated: "Load the raw family seed string from environment"
  with SOURDOUGH reference
- Added `.map(|s| s.trim().to_owned())` before the emptiness filter
- 3 new tests: raw hex passthrough, whitespace trimming, empty-after-trim

## Note for primalSpring

The audit finding to base64-encode contradicts the SOURDOUGH standard and
the convergence status of 9 primals. The "unknown" guidestone error may
stem from whitespace in the env var (now fixed by trim) or from a
different environmental factor. petalTongue does NOT base64-encode — this
aligns with barraCuda, Songbird, coralReef, and all other converged primals.
