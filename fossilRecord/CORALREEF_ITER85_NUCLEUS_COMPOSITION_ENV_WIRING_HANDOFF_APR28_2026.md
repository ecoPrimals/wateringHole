# coralReef Iteration 85 — NUCLEUS Composition Env Var Wiring

**Date**: April 28, 2026  
**From**: coralReef (Iteration 85)  
**Triggered by**: primalSpring v0.9.20 (Phase 55) audit

---

## What Changed

All 3 coralReef binaries (`coralreef`, `coral-ember`, `coral-glowplug`) now read
and act on the NUCLEUS composition launcher environment variables:

| Variable | Where Used | Purpose |
|----------|-----------|---------|
| `BEARDOG_SOCKET` | BTSP security-provider discovery | Preferred over filesystem scan — resolves BearDog socket directly |
| `BTSP_PROVIDER_SOCKET` | BTSP security-provider discovery | Checked first (before `BEARDOG_SOCKET`) |
| `DISCOVERY_SOCKET` | Ecosystem registry discovery | Songbird socket used before scanning `*.json` discovery files |
| `BIOMEOS_SOCKET_DIR` | Socket/discovery directory resolution | Overrides `$XDG_RUNTIME_DIR/{namespace}` |
| `CORALREEF_FAMILY_ID` | Family isolation | Alias for `BIOMEOS_FAMILY_ID` (composition launcher sets per-primal) |
| `FAMILY_SEED` | Crypto key derivation input | Read and logged; forwarded for future `shader` purpose-key derivation |

### Resolution Priority

**BTSP provider**: `$BTSP_PROVIDER_SOCKET` → `$BEARDOG_SOCKET` → `{sock_dir}/crypto-{family}.sock` → `{sock_dir}/crypto.sock` → discovery file scan

**Registry**: `$BIOMEOS_ECOSYSTEM_REGISTRY` → `$DISCOVERY_SOCKET` → discovery file scan

**Socket dir**: `$BIOMEOS_SOCKET_DIR` → `$XDG_RUNTIME_DIR/{namespace}` → `{temp}/{namespace}`

**Family ID**: `$CORALREEF_FAMILY_ID` → `$BIOMEOS_FAMILY_ID` → `"default"`

### Startup Diagnostics

`coralreef server` now logs all composition env vars at INFO (when set) or DEBUG
(when absent) on startup. Operators can verify wiring at a glance.

---

## Shader Signing — Deferred

Per primalSpring v0.9.20: "Low priority — shader signing is a nice-to-have."

The `shader` purpose key path is documented in `NUCLEUS_TWO_TIER_CRYPTO_MODEL.md`:
```
purpose_key = HMAC-SHA256(family_key, hex("purpose-v1:shader"))
```

coralReef is now wired to receive `BEARDOG_SOCKET` and `FAMILY_SEED` — the two
inputs needed for `crypto.sign` delegation. Implementation deferred to a future
iteration when the composition layer is ready for signed artifact verification.

---

## For Other Primals

If your primal has a BTSP module that scans the filesystem for `crypto-*.sock`,
consider adding `$BTSP_PROVIDER_SOCKET` / `$BEARDOG_SOCKET` as the first resolution
step. The composition launcher already sets both.

Similarly, `$DISCOVERY_SOCKET` provides a direct path to Songbird without needing
to scan `*.json` files.

---

## Verification

- 4,701 tests passing, 0 failed
- Zero clippy warnings (`clippy::pedantic` + `clippy::nursery`)
- Zero new dependencies added
- All changes are backwards-compatible (env vars are optional, fallback to previous behavior)
