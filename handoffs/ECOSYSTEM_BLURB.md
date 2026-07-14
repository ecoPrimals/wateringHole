# ecoPrimals Ecosystem Blurb — Wave 138a

**Date**: Jul 14, 2026 07:30 EDT | **Wave**: 138a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** SOLOKEY-CEREMONY wired. protoKarya composition routing formalized. ABG JupyterHub access guide shipped. Collaborator activation track defined. 4 carried items.

---

## Wave 138 — Three Tracks

### Track 1: Hardware Trust (eastGate / primalSpring)
SOLOKEY-CEREMONY code wired (`beardog.fido2.entropy` IPC). PIXEL-STRONGBOX unblocked (Android compile fixed). HW inventory reconciled. Physical SoloKey test next.

### Track 2: K-Derm Extrication (sporeGate / golgi)
`primal.eco` separation, bearDog gatehouse cutover, Forgejo PERMS permanent fix.

### Track 3: Live Compositions + Collaborator Activation (NEW)

**protoKarya projects as live compositions**: Each protoKarya project is a composition that consumes primal capabilities and registers its data feeds as drawbridge capabilities. Each gets a public subdomain via wildcard DNS.

| Project | Subdomain | What It Provides | Consumes |
|---------|-----------|-----------------|----------|
| **footPrint** | `primals.eco/footprint/` | GIS visualization, spatial data feeds, live map layers | nestGate (CAS), songBird (proxy), petalTongue (SPA) |
| **tideGlass** | `tideglass.primals.eco` | Drug perturbation reversal screening (GPS rebuild) | nestGate (compound data), barracuda (MATRIX), helixVision (expression) |
| **JupyterHub** | `lab.primals.eco` | Shared compute for RNA-seq, NF mining, ABG science | ironGate (GPU), songBird (drawbridge), bearDog (auth) |

**Data feeds register with drawbridge**: footPrint GIS data (USGS, ArcGIS, tile servers) enters through drawbridge weak bonds → NestGate CAS. Same data feeds serve NF spatial analysis, ABG environmental genomics, and the public GIS tool. The drawbridge is the universal data ingestion point.

**Cross-feeding**: footPrint provides spatial visualization that NF and ABG work needs. tideGlass provides drug reversal data that feeds back into healthSpring. JupyterHub provides compute that both collaborator groups use. All register as mesh capabilities.

---

## Collaborator Activation

| Collaborator | Status | Product(s) | What's Live | Next |
|-------------|--------|------------|------------|------|
| **ABG** | Producing | initioChem, JupyterHub | `lab.primals.eco` access guide shipped | Create user accounts (REALWORLD). conda/bioconda RNA-seq setup. |
| **Gonzales (NF)** | Engaged → producing | tideGlass, helixVision, healthSpring | 782/782 validated. Pre-grant pipeline. GPS assigned Jun 5. | tideGlass Phase 0 (Zenodo archaeology). NF Data Portal ingestion. sporePrint NF content. |
| **Jones (Bluefish)** | Active | blueFish | Product spec from data dumps | PFAS ETL pipeline. EPA 1633A targets. |
| **Chuna (QCD)** | Delivery-ready | hotSpring | guideStone 59/59. USB deployment. | TC delivery (REALWORLD). |

**sporePrint content needed**: NF case study, tideGlass product page, collaborator profiles, pre-grant pipeline methodology. These are public-facing pages that demonstrate ecosystem capability to PIs and foundations.

---

## Remaining — 4 carried items

| ID | Owner | What |
|----|-------|------|
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration. |
| **FORGEJO-PERMS-RECUR** | sporeGate | Permanent fix for ownership drift. |
| **SOCKET-DIR-UNIFY** | biomeOS | Socket dir consolidation. |
| **BIOMEOS-TEMPLATE** | cellMembrane | Service template subcommand mismatch. |

---

## Architecture: protoKarya Composition Routing

```
                    *.primals.eco (wildcard DNS)
                           │
                     Caddy (golgi)
                    ┌──────┼──────┐
                    │      │      │
        footprint/  │  tideglass  │  lab/
        (GIS SPA)   │  (reversal) │  (JupyterHub)
                    │      │      │
              ┌─────┴──────┴──────┴─────┐
              │     songBird mesh       │
              │   drawbridge routing    │
              │   capability.call()     │
              └─────┬──────┬──────┬─────┘
                    │      │      │
              nestGate  barracuda  ironGate
              (CAS)     (math)    (GPU/compute)
              
Data feeds:
  USGS, ArcGIS, NF Portal, Pluto.bio, LINCS
    → drawbridge weak bonds
      → nestGate CAS (content-addressed, BLAKE3)
        → available as capabilities across mesh
```

Each protoKarya project registers its data needs as drawbridge weak bonds. The data lands in NestGate CAS with full provenance (Loam Certificates). Other projects and springs consume it via `capability.call`. footPrint's GIS layers, tideGlass's compound libraries, and JupyterHub's datasets all live in the same CAS — different projects, same sovereign data mesh.

---

## Gate Status

```
eastGate     — PRIMARY. primalSpring + hardware coevolution. SoloKey ready.
sporeGate    — NUCLEUS. K-Derm extrication. Depot authority.
golgiBody    — Outer membrane. Wildcard DNS. Caddy routing for *.primals.eco.
flockGate    — bearDog FIDO2 + primalSpring scenarios. 147 scenarios.
ironGate     — ABG/NF compute. JupyterHub v5.4.5. GPU. 13/13.
grapheneGate — StrongBox target. Android compile unblocked.
```

---

## Evolution Path

```
NOW:    footPrint live at primals.eco/footprint/. JupyterHub at lab.primals.eco.
        ironGate = single-node compute for ABG + NF.
        tideGlass Phase 0 (GPS archaeology).

NEXT:   tideGlass at tideglass.primals.eco.
        NF Data Portal ingestion → NestGate CAS.
        sporePrint: NF case study, collaborator profiles.
        primal.eco separation (private compositions, ceremonies).

FUTURE: strandGate (EPYC + 256GB) as HPC backend.
        ABG/Gonzales gates federated via primal.eco mesh.
        nestgate.io as federated data gateway (NCBI, PubMed, USGS, CTF).
        Universal substrate: NUCLEUS on any architecture.
```

---

*Wave 138a: live compositions register with drawbridge. protoKarya projects get *.primals.eco subdomains. footPrint GIS feeds serve NF + ABG. Collaborator activation: ABG producing, Gonzales GPS assigned, Jones active, Chuna delivery-ready. 7,750+ tests / 0 fail.*
