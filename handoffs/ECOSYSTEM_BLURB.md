# ecoPrimals Ecosystem Blurb — Wave 138a

**Date**: Jul 13, 2026 18:25 EDT | **Wave**: 138a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** Wave 137b closed. Wave 138: hardware trust activation. Local-first on eastGate, then evolve outward.

---

## Wave 138 — Entropy Ceremonies + Hardware Sovereignty

### Execution Strategy

**Local-first on eastGate.** primalSpring team on eastGate focuses on hardware integration and evolving systems to meet new standards. Available locally: SoloKey (USB), Pixel 8a (ADB), eastGate compute, local NUCLEUS. Get it working locally, validate with primalSpring scenarios, then evolve outward to golgi and `primal.eco` inner membrane.

**sporeGate/golgi team**: Continue extricating K-Derm layers — separate `primal.eco` routing from `primals.eco`, advance bearDog gatehouse cutover, fix FORGEJO-PERMS recurrence.

### Team Assignments

#### eastGate / primalSpring (local-first)

| ID | What | Local Hardware | Approach |
|----|------|---------------|----------|
| **SOLOKEY-CEREMONY** | Wire SoloKey FIDO2 → bearDog entropy mixing. Activate Tier 2 ceremony. | SoloKey USB on eastGate | bearDog FIDO2 IPC stubs exist (`fido2.discover\|register\|authenticate`). Wire CTAP2 hmac-secret. primalSpring scenarios to validate. |
| **PIXEL-STRONGBOX** | Wire Titan M2 → bearDog keystore. FAMILY_SEED + human entropy. | Pixel 8a over ADB | Fix 16 compile errors in `AndroidKeymaster`. Test via ADB port forwards. |
| **HW-INVENTORY-RECONCILE** | Single-source hardware inventory. Resolve spec conflicts. | All local hardware | Update `HARDWARE_INVENTORY.md` to be canonical. |
| **LOCAL-CEREMONY-E2E** | End-to-end local ceremony: SoloKey entropy + Pixel biometric + bearDog key gen → Loam Certificate mint. | SoloKey + Pixel + eastGate | Integration test. Validates full entropy → provenance pipeline locally before any WAN deployment. |

#### sporeGate / golgi (K-Derm extrication)

| ID | What | Approach |
|----|------|----------|
| **PRIMAL-ECO-SEPARATION** | `primal.eco` stops mirroring `primals.eco`. Own Caddy routing, own sporePrint, own ceremony endpoints. | Sovereign DNS already on knot-dns. Caddy block on sporeGate for `primal.eco`. |
| **BEARDOG-GATEHOUSE-CUTOVER** | bearDog ACME replaces Caddy TLS on inner membrane. Shadow live since 136. | Cut over `primal.eco` TLS first (inner only). `primals.eco` stays Caddy/LE. |
| **FORGEJO-PERMS-RECUR** | Fix ownership drift. Permanent solution (systemd tmpfiles.d or git hooks). | Root cause: processes writing as root into git-owned dirs. |

#### Team-owned (carried, not blocking)

| ID | Owner | What |
|----|-------|------|
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration. |
| **SOCKET-DIR-UNIFY** | biomeOS | Socket dir consolidation. |
| **BIOMEOS-TEMPLATE** | cellMembrane | Service template subcommand mismatch. |
| **STALE-PEERS** | cascade tooling | Head file refresh automation. |
| **TARPC-BIND** | songBird | Non-fatal startup error. |

---

## Evolution Path

```
Phase 1 — LOCAL (eastGate only)
  SoloKey → bearDog FIDO2 IPC → entropy mixing → key generation
  Pixel ADB → StrongBox → FAMILY_SEED store
  Local ceremony E2E: entropy → sign → Loam Certificate mint
  primalSpring scenarios validate each step

Phase 2 — INNER MEMBRANE (primal.eco)
  Ceremony endpoints on primal.eco (sporeGate Caddy)
  bearDog gatehouse TLS cutover on primal.eco
  Private footPrint instance with Loam Certificate provenance
  primal.eco sporePrint as personal site

Phase 3 — SUBSTRATE EXPANSION
  Android NDK depot target (NUCLEUS on Pixel native)
  RISC-V, Windows, WASM depot targets
  Universal substrate: any arch = potential sovereign node
```

---

## Domain Routing

| Domain | Layer | Wave 138 Focus |
|--------|-------|---------------|
| `primals.eco` | Outer membrane | Stable. Public platform. No changes needed. |
| `primal.eco` | Inner membrane | **ACTIVE** — separation from primals.eco, ceremony endpoints, bearDog gatehouse TLS. |
| `nestgate.io` | Content organelle | Horizon. Scales with federated data mesh. |

**footPrint routing**: Public GIS on `primals.eco/footprint/`. Private data on `primal.eco/footprint/` (Phase 2 — backed by Loam Certificates).

---

## Gate Status

```
eastGate     — PRIMARY. primalSpring + hardware integration. SoloKey + Pixel.
sporeGate    — K-Derm extrication. primal.eco separation. Depot authority.
golgiBody    — Outer membrane. Wildcard DNS. Caddy routing.
flockGate    — Validation. 144 scenarios / 1,190 tests.
ironGate     — Compute. 13/13. SoloKey plugged (Phase 1 secondary).
grapheneGate — StrongBox target. Tower live. ADB from eastGate.
```

---

*Wave 138a: local-first hardware sovereignty on eastGate. SoloKey + Pixel StrongBox → bearDog entropy → Loam Certificate ceremony. sporeGate/golgi extricate K-Derm layers for primal.eco. 7,750+ tests / 0 fail.*
