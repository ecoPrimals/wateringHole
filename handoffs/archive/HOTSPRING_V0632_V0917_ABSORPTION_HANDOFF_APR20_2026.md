# hotSpring v0.6.32 — primalSpring v0.9.17 Absorption Handoff

**Date:** April 20, 2026
**From:** hotSpring (guideStone Level 5 CERTIFIED)
**For:** primalSpring upstream, sibling springs
**License:** AGPL-3.0-or-later

---

## Summary

hotSpring absorbed primalSpring v0.9.17 (Phase 45: genomeBin v5.1, deployment
validation, guideStone standard v1.2.0). The primalspring dependency updated
from v0.9.16 to v0.9.17 with zero code changes required — the composition
API is fully backward-compatible. The `validate-primal-proof.sh` script was
enhanced to auto-set all required NUCLEUS deployment env vars.

---

## What Changed in hotSpring

### 1. primalspring Dependency: v0.9.16 → v0.9.17

`hotspring_guidestone` compiles clean against v0.9.17. All APIs used by
hotSpring (`CompositionContext`, `validate_liveness`, `validate_parity`,
`checksums::verify_manifest`, `tolerances`, `IpcError::is_protocol_error`,
`IpcError::is_connection_error`) are unchanged. Bare mode: 30/30 PASS (with BLAKE3 CHECKSUMS manifest covering 15 source files).

### 2. guideStone Binary Module Doc

Updated reference from "primalSpring v0.9.16" to "primalSpring v0.9.17".

### 3. validate-primal-proof.sh — Deployment Env Var Auto-Setup

The script now auto-sets required env vars when `FAMILY_ID` is provided:

| Env Var | How Set | Source |
|---------|---------|--------|
| `BEARDOG_FAMILY_SEED` | SHA-256 of FAMILY_ID | Deterministic — same family, same seed |
| `SONGBIRD_SECURITY_PROVIDER` | Defaults to `beardog` | Required for Tower composition |
| `NESTGATE_JWT_SECRET` | Random Base64 (32 bytes) | Generated fresh each run |

This addresses three v0.9.17 known issues directly:
- beardog silently fails without FAMILY_SEED
- songbird refuses to start without security provider
- nestgate refuses insecure JWT configuration

---

## v0.9.17 Patterns — What hotSpring Absorbed vs Deferred

### Absorbed

| Pattern | Status |
|---------|--------|
| primalspring v0.9.17 backward-compatible API | Compiles clean, zero changes |
| guideStone standard v1.2.0 reference | Doc ref updated |
| BEARDOG_FAMILY_SEED auto-set | In validate-primal-proof.sh |
| SONGBIRD_SECURITY_PROVIDER default | In validate-primal-proof.sh |
| NESTGATE_JWT_SECRET generation | In validate-primal-proof.sh |
| coralReef iter84 `--port` → `--rpc-bind` | Noted in gaps; hotSpring doesn't launch coralReef directly |

### Deferred (not applicable to hotSpring yet)

| Pattern | Reason |
|---------|--------|
| genomeBin cross-architecture builds | hotSpring ecoBin already ships x86_64 musl-static; armv7/aarch64/RISC-V builds pending `cargo check` verification |
| `build_ecosystem_genomeBin.sh` migration | hotSpring uses `harvest-ecobin.sh` (spring-local, not ecosystem-wide) |
| TCP fallback ports | hotSpring uses UDS exclusively; TCP ports noted for future container deployments |
| Fragment-first deploy graph composition | hotSpring deploy graph is already standalone TOML (`hotspring_qcd_deploy.toml`) |

---

## Confirmed Patterns for Sibling Springs

1. **Backward compatibility is real.** v0.9.16 → v0.9.17 required zero code
   changes in the guideStone binary. If your guideStone compiled against v0.9.16,
   it compiles against v0.9.17.

2. **Env var auto-setup is essential.** NUCLEUS deployments require 3+ env vars
   that aren't obvious from `--help`. Every spring's validation script should
   auto-generate these from FAMILY_ID.

3. **The checklist from the Phase 45 handoff §6 is correct.** hotSpring verified:
   - [x] Update primalSpring dependency to v0.9.17
   - [x] coralReef `--port` → `--rpc-bind` noted
   - [x] BEARDOG_FAMILY_SEED handled
   - [x] SONGBIRD_SECURITY_PROVIDER handled
   - [x] Deploy graphs still resolve (no fragment-first changes needed)

---

## References

- Phase 45 handoff: `infra/wateringHole/handoffs/PRIMALSPRING_PHASE45_DEPLOYMENT_VALIDATION_HANDOFF_APR2026.md`
- genomeBin handoff: `infra/wateringHole/handoffs/PRIMALSPRING_V0917_GENOMBIN_CROSS_ARCH_HANDOFF_APR2026.md`
- guideStone standard v1.2.0: `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md`
- hotSpring gap registry: `hotSpring/docs/PRIMAL_GAPS.md` (GAP-HS-036 resolved)
