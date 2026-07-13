# ecoPrimals Ecosystem Blurb — Wave 138a

**Date**: Jul 13, 2026 18:10 EDT | **Wave**: 138a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** Wave 137b closed. Domain identity formalized. Entropy ceremony and hardware sovereignty evolution begin. 6 carried items + 4 evolution targets.

---

## Wave 137b Delivery Summary (closed)

Wave 137b delivered: DRAWBRIDGE-CAP resolved. DNS wildcard active. FP-API GIS proxy live. ironGate redeployed (14 binaries). 2,801 bash lines fossilized. `require-signed` system-wide. Terminology hardened (Loam Certificate vs TLS credential). Differential evolution versioning documented. Domain identity separation formalized (`primals.eco` public / `primal.eco` sovereign / `nestgate.io` federated data). 7 docs updated. 4 handoffs + 2 impulses fossilized. Multi-dimensional deep review complete.

---

## Wave 138 — Entropy Ceremonies + Hardware Sovereignty + Substrate Evolution

### Theme

The ecosystem is public and sovereign. The next evolution era is **hardware trust activation** — wiring the physical entropy sources (SoloKeys, Pixel StrongBox) that have been designed across 30+ whitePaper documents but never production-activated. Simultaneously, the domain identity separation enables `primal.eco` to become the sovereign ceremony host while `primals.eco` remains the public platform.

### Priority Matrix

#### P0 — Sovereignty Evolution (eastGate + hardware teams)

| ID | Owner | What | Blocks |
|----|-------|------|--------|
| **SOLOKEY-CEREMONY** | bearDog + eastGate | Wire SoloKey FIDO2 → bearDog entropy mixing. Activate Tier 2 ceremony protocol. 4 keys exist, 2 plugged. Zero production crypto use today. | `primal.eco` sovereign identity |
| **PIXEL-STRONGBOX** | bearDog + grapheneGate | Wire Titan M2 StrongBox → bearDog keystore. FAMILY_SEED + human entropy ceremonies. Fix 16 compile errors in `AndroidKeymaster` transport. | Dual-HSM ceremony, Tier 4 genetics carrier |

#### P1 — Carried Infrastructure (team-owned)

| ID | Owner | What |
|----|-------|------|
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. |
| **FORGEJO-PERMS-RECUR** | sporeGate | Forgejo `permission denied` writing objects — recurrence. Root cause: file ownership drift (`root:root` vs `git:git`). |

#### P2 — Carried Refinement (team-owned)

| ID | Owner | What |
|----|-------|------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. |
| **BIOMEOS-TEMPLATE** | cellMembrane | `membrane-nucleus@.service` assumes `server` subcommand. biomeOS needs alias or template exclusion. |
| **STALE-PEERS** | wateringHole / cascade | Gate head files not refreshed by cascade. Needs automation or manual refresh protocol. |
| **TARPC-BIND** | songBird | tarpc listener address-in-use on startup. Non-fatal. |

#### Evolution Targets (Wave 138+)

| ID | Owner | What | Horizon |
|----|-------|------|---------|
| **HW-INVENTORY-RECONCILE** | overwatch | Single-source hardware inventory. Resolve spec conflicts (ironGate 3 profiles, eastGate 2 profiles). Update `HARDWARE_INVENTORY.md` to be canonical. | 138a |
| **UNIVERSAL-SUBSTRATE** | cellMembrane + depot | Multi-arch NUCLEUS: Android NDK, RISC-V, Windows, WASM, macOS Silicon. Next glacial goal. | 138–140 |
| **PRIMAL-ECO-SEPARATION** | overwatch + sporeGate | `primal.eco` stops mirroring `primals.eco`. Own sporePrint instance, own Caddy routing, own ceremony endpoints. | 138–139 |
| **BEARDOG-GATEHOUSE-CUTOVER** | bearDog + sporeGate | bearDog ACME replaces Caddy TLS. Shadow live since Wave 136. Full cutover. | 139+ |

---

## Domain Routing (formalized Wave 137b)

| Domain | Layer | Purpose | Key Evolution |
|--------|-------|---------|--------------|
| `primals.eco` | Outer membrane | Public platform: depot, forge, sporePrint, footPrint (public), TOPO-VIS | Wildcard DNS active. Caddy sole routing authority. |
| `primal.eco` | Inner membrane | Sovereign substrate: key ceremonies, private footPrint, mesh API, HPC, personal sporePrint | Separation from primals.eco. Entropy ceremony host. |
| `nestgate.io` | Content organelle | Federated data gateway: CAS backbone, drawbridge weak bonds (NCBI, PubMed, USGS, ArcGIS) | Long-horizon. Scales with federated data mesh. |

**Same primals, different trust**: A footPrint on `primals.eco` = public GIS. A footPrint on `primal.eco` = private data + Loam Certificates + bearDog-signed sessions. The domain determines the membrane layer.

---

## Gate Status

```
eastGate     — Overwatch. 13 primals. SoloKey plugged (ceremony target).
sporeGate    — NUCLEUS. Public surfaces live. Depot 35/35. Forgejo PERMS to fix.
golgiBody    — Full mirror. Wildcard DNS. Caddy routing authority.
flockGate    — 144 scenarios / 1,190 tests. songBird DRAWBRIDGE-CAP shipped.
ironGate     — REDEPLOYED. 13/13 active. Mesh restored. SoloKey plugged.
grapheneGate — Tower live. USB tether. StrongBox ceremony target.
```

---

## Dimensional Posture (entering Wave 138)

| Dimension | Status |
|-----------|--------|
| **Temporal** | Wave 138a. All docs current. Only ECOSYSTEM_BLURB active. |
| **Ecological** | 14 primals, 8 springs, 7 gardens, 6 infra, 1 protist. 40 repos. |
| **Hardware** | 7 gates online. SoloKeys + StrongBox = biggest sovereignty gap. |
| **Topology** | 3-gate WG mesh. Wildcard DNS. Domain identity separated. |
| **Sovereignty** | K-Derm operational. Domain routing formalized. Ceremony activation next. |
| **Depot** | 100% Rust. `require-signed`. 35 bins / 3 arch. |
| **Security** | All headers. fail2ban. SIGN-VERIFY-ON-FETCH. HSM gap = P0 evolution. |
| **Glacial** | ALL 8 CRITERIA CLEAR. Next goal: Universal Substrate. |
| **Website** | 4 public surfaces live. MacGuffin test passing. |

---

*Wave 138a: entropy ceremonies and hardware sovereignty. The ecosystem is public and sovereign — now it evolves its physical trust roots. 7,750+ tests / 0 fail.*
