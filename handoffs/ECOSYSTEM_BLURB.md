# ecoPrimals Ecosystem Blurb — Wave 137b (Deep Review)

**Date**: Jul 13, 2026 18:00 EDT | **Wave**: 137b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN.** Deep multi-dimensional review complete. 2 handoffs + 2 impulses fossilized. 5 stale docs updated. Hardware gaps inventoried. Forgejo perms recurrence flagged. 6 items remain + 4 hardware evolution targets.

---

## Remaining — 6 operational items

### P1

| ID | Owner | What |
|----|-------|------|
| **NAPI-LIFECYCLE** | biomeOS | LifecycleManager registration — `lifecycle.status` count=0. |
| **FORGEJO-PERMS-RECUR** | sporeGate | Forgejo permission denied writing objects — recurrence of FORGEJO-PERMS pattern. |

### P2

| ID | Owner | What |
|----|-------|------|
| **SOCKET-DIR-UNIFY** | biomeOS | Unify socket dirs → `/run/membrane/` only. |
| **BIOMEOS-TEMPLATE** | cellMembrane | `membrane-nucleus@.service` assumes `server` subcommand. biomeOS needs alias or exclusion. |
| **STALE-PEERS** | wateringHole | Gate head files not refreshed by cascade (golgi 154hrs, sporeGate 68hrs). |

### P3

| ID | Owner | What |
|----|-------|------|
| **TARPC-BIND** | songBird | tarpc listener address-in-use on startup. Non-fatal. |

---

## Hardware Evolution Targets (new from deep review)

| Target | What | Status |
|--------|------|--------|
| **SOLOKEY-CEREMONY** | Wire SoloKey FIDO2 → bearDog entropy mixing + Tier 2 ceremony. 4 keys exist (2 plugged: eastGate, ironGate). Zero production crypto use today. | ARCHITECTURE EXISTS — activation needed |
| **PIXEL-STRONGBOX** | Wire grapheneGate Titan M2 StrongBox → bearDog keystore for FAMILY_SEED + human entropy ceremonies. | NOT STARTED (16 compile errors at Wave 106) |
| **HW-INVENTORY-RECONCILE** | `HARDWARE_INVENTORY.md` (Wave 116) diverged from manifest + wave.toml. ironGate/eastGate specs conflict across 3 docs. Flint H1 router role undocumented. | Needs single-source reconciliation |
| **UNIVERSAL-SUBSTRATE** | Next glacial goal. Android NDK, RISC-V, Windows, WASM, macOS Silicon depot targets. | Elevated to GLACIAL_SHIFT_READINESS |

---

## Deep Review Findings (by dimension)

### Temporal
- Wave 137b. 5 stale docs updated (README, GLACIAL, manifest, flockGate head, impulses).
- 2 handoffs fossilized (FOOTPRINT_WIRING, JELLYFISH_TRIAGE). Only ECOSYSTEM_BLURB active.
- `DEPLOYMENT_INSTANCE.toml` still at Wave 134 — needs sporeGate/cellMembrane update.

### Ecological
- 14 primals, 8 springs, 7 gardens, 6 infra, 1 protist.
- Differential evolution rates documented (glossary). No primal at 1.0.
- rhizoCrypt (0.14.17) most iterated. biomeOS (0.1.0) youngest.

### Hardware / Topology
- **Leveraged today**: 7 gates online (sporeGate, eastGate, ironGate, flockGate, golgi, grapheneGate + Flint H1 edge router).
- **Present but not wired to trust model**: 2 SoloKeys plugged (eastGate, ironGate), Titan M2 (Pixel), 3 Akida NPU.
- **Documented but idle**: westGate (76TB ZFS), biomeGate (HBM2), strandGate (EPYC — offline), fieldGate (dead CMOS), 3 Intel NUC6CAY.
- **Spec conflicts**: ironGate listed as i9-14900K/96GB/5070 AND i9-12900K/128GB/5070Ti AND i9-12900K/96GB (3 different profiles across HARDWARE.md, manifest, Wave 137b).
- Pixel is Tower live + USB tether. Its highest-value entropy role (StrongBox-backed FAMILY_SEED) is not started.

### Sovereignty / Membranes
- K-Derm diderm model operational. Cloudflare external capsule (drawbridge). Caddy sovereign outer membrane.
- `*.primals.eco` wildcard DNS active — Caddy sole routing authority.
- Domain identity separation documented: `primals.eco` / `primal.eco` / `nestgate.io`.
- Loam Certificate vs TLS credential terminology fixed (glossary).

### Depot / Build Pipeline
- 100% Rust pipeline. `require-signed` enforced system-wide.
- 35 binaries / 3 architectures (x86_64-musl, aarch64-musl, nucleus_launcher).
- 2,801 lines of bash fossilized (jellyfish triage).
- Depot layout fixed: `depot/primals/arch/binary`.

### Website / Public Surfaces
- `primals.eco` — sporePrint + footPrint GIS proxy (10 hosts). Live.
- `live.primals.eco` — petalTongue TOPO-VIS dashboard. Live.
- `git.primals.eco` — Forgejo. Healthy (minus PERMS recurrence).
- `membrane.primals.eco` — Nest Atomic composition. Live.
- MacGuffin test: topology visualization public on live.primals.eco.

### Security
- HSTS, CSP, X-Frame, nosniff on all domains. fail2ban on Forgejo SSH.
- `require-signed` depot policy. SIGN-VERIFY-ON-FETCH in cellMembrane.
- SoloKeys + Titan M2: **biggest hardware-security gap** — present, architected, not production-wired.
- bearDog ACME gatehouse: shadow live, not cut over.

### Glacial
- ALL 8 CRITERIA CLEAR for stadial entry.
- Next glacial goal: Universal Substrate Evolution (multi-arch NUCLEUS).
- SHOW_HN publication rubric exists (whitePaper gen5/thesis/).

---

## Docs Updated This Review

| Doc | Action |
|-----|--------|
| `README.md` | Wave 128 → 137b header |
| `GLACIAL_SHIFT_READINESS.md` | Body "4-gate" → "3-gate WG mesh, PUBLIC + SOVEREIGN" |
| `GLOSSARY.md` | Loam Certificate entry, TLS credential distinction, versioning philosophy |
| `ecosystem_manifest.toml` | v2.9.0, Wave 137, 40 repos |
| `heads/flockGate.toml` | DRAWBRIDGE-CAP resolved, scenarios 144, tests 1190 |
| `handoffs/` | 2 fossilized → archive |
| `impulses/` | 2 discharged → archive (wave118, wave128) |

---

## Gate Status

```
eastGate     — Overwatch. 13 primals. Clean. SoloKey plugged (not wired).
sporeGate    — NUCLEUS. Public surfaces live. Depot 35/35. Forgejo PERMS recurrence.
golgiBody    — Full mirror. Wildcard DNS. Caddy routing authority.
flockGate    — 144 scenarios / 1,190 tests. songBird deep debt shipped.
ironGate     — REDEPLOYED Jul 13. 13/13. Mesh restored. SoloKey plugged.
grapheneGate — Tower live. USB tether. StrongBox NOT STARTED.
```

---

*Wave 137b deep review: 6 operational items. 4 hardware evolution targets (SoloKey ceremony, Pixel StrongBox, inventory reconciliation, universal substrate). All 8 glacial criteria clear. 7,750+ tests / 0 fail.*
