# ecoPrimals Ecosystem Blurb — Wave 138a

**Date**: Jul 13, 2026 19:00 EDT | **Wave**: 138a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** SOLOKEY-CEREMONY wired (bearDog `fido2.entropy` IPC live). PIXEL-STRONGBOX unblocked (Android compile fixed). HW-INVENTORY reconciled. primalSpring at 147 scenarios / 1,306 tests. 4 carried items remain.

---

## Wave 138a Delivered (this wave)

| Item | Delivered By | What |
|------|-------------|------|
| **SOLOKEY-CEREMONY** | bearDog (flockGate) | `beardog.fido2.entropy` IPC method wired. CTAP2 hmac-secret extension. Stateless `authenticate_with_credential()`. BLAKE3 entropy mixing of challenge + signature nonce. Pending: physical SoloKey test on eastGate. |
| **PIXEL-STRONGBOX** | bearDog (flockGate) | Android `compile_error!` in beardog-hid fixed — returns empty gracefully. Cross-compile unblocked for aarch64-linux-android. Pixel depot builds now possible. |
| **HW-INVENTORY-RECONCILE** | whitePaper | Canonical single-source inventory. Spec conflicts resolved (sporeGate RAM, ironGate ownership, subnet migration). pepti VPS added. |
| **primalSpring scenarios** | primalSpring | +3 scenarios: `s_fido2_entropy_ceremony`, `s_hardware_trust_pipeline`, `s_keygen_interaction_surface`. 147 total / 1,306 tests / 0 failures. |
| **bearDog** | bearDog | 11,175 tests / 0 fail. 6 files changed across FIDO2 stack. |

---

## Remaining — 4 carried items

### P1

| ID | Owner | What |
|----|-------|------|
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. |
| **FORGEJO-PERMS-RECUR** | sporeGate | Forgejo permission drift. Needs permanent fix (tmpfiles.d or hooks). |

### P2

| ID | Owner | What |
|----|-------|------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/`. |
| **BIOMEOS-TEMPLATE** | cellMembrane | Service template subcommand mismatch. |

*STALE-PEERS and TARPC-BIND absorbed into carried items — low priority, non-blocking.*

---

## Next Steps (Phase 1 → Phase 2)

### Phase 1 remaining (local on eastGate)

| Task | What | Status |
|------|------|--------|
| **SOLOKEY-PHYSICAL** | Plug SoloKey into eastGate, run `beardog.fido2.discover`, validate entropy harvest E2E. | Ready — code shipped, hardware present. |
| **LOCAL-CEREMONY-E2E** | Full arc: SoloKey entropy + bearDog keygen → Loam Certificate mint (loamSpine). | Next — requires SOLOKEY-PHYSICAL. |
| **PIXEL-ADB-CEREMONY** | Pixel StrongBox entropy via ADB port forward. Dual-HSM test with SoloKey. | After Android keystore transport wired. |

### Phase 2 (primal.eco inner membrane — sporeGate/golgi team)

| Task | What |
|------|------|
| **PRIMAL-ECO-SEPARATION** | `primal.eco` gets own Caddy routing, ceremony endpoints, private sporePrint. |
| **BEARDOG-GATEHOUSE-CUTOVER** | bearDog ACME replaces Caddy TLS on `primal.eco` inner membrane. |
| **PRIVATE-FOOTPRINT** | footPrint on `primal.eco` with Loam Certificate provenance for private data. |

### Phase 3 (universal substrate — cellMembrane + depot)

| Task | What |
|------|------|
| **ANDROID-NDK** | `aarch64-linux-android` depot target. Native NUCLEUS on Pixel. |
| **RISC-V / WASM / macOS** | Expand depot target matrix. Next glacial goal. |

---

## Team Model (Wave 138+)

**eastGate = primalSpring + hardware** — singular coevolution. primalSpring on eastGate owns local hardware integration (SoloKey, Pixel ADB, USB devices). Physical proximity to operator enables ceremony testing. primalSpring scenarios validate each hardware interaction before it evolves outward.

**sporeGate/golgi** — K-Derm extrication. `primal.eco` separation, bearDog gatehouse cutover, Forgejo permanent fix.

**flockGate** — Validation + upstream primal evolution (bearDog FIDO2, songBird).

---

## Gate Status

```
eastGate     — PRIMARY. primalSpring + hardware coevolution. SoloKey ready.
sporeGate    — NUCLEUS + K-Derm extrication. Forgejo PERMS to fix.
golgiBody    — Outer membrane. Wildcard DNS. Caddy routing.
flockGate    — bearDog FIDO2 shipped. 147 scenarios. songBird deep debt.
ironGate     — Compute. 13/13. SoloKey plugged (secondary).
grapheneGate — StrongBox target. Android compile unblocked.
```

---

*Wave 138a: SOLOKEY-CEREMONY wired, PIXEL-STRONGBOX unblocked, HW-INVENTORY reconciled. 4 carried items. Physical SoloKey test next. primalSpring + eastGate hardware = singular coevolution. 7,750+ tests / 0 fail.*
