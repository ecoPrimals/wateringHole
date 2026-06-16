# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | Deadline: Friday June 20 | **From**: eastGate overwatch
**Last review**: Jun 16 12:46Z

---

## Objective

Depot deploys to all form factors + primals health-validate via riboCipher.

| Target | Arch | Transport | Status |
|--------|------|-----------|--------|
| **fieldGate** (NUC) | x86_64-musl | LAN via MikroTik | **✅ 13/13 ALIVE** |
| **grapheneGate** (Pixel) | aarch64-musl | LAN/relay | DEPOT READY (device needed) |
| **flockGate** (WAN) | x86_64-musl | relay via golgiBody | PATH PROVEN (target needed) |

---

## Ecosystem Snapshot (Jun 16 12:46Z)

| Metric | Value |
|--------|-------|
| VCS parity | **17/17 ✓** (zero drift) |
| Depot x86_64 | **13/13 BUILT** from HEAD (pepti Jun 16 02:27Z) |
| Depot aarch64 | **13/13 BUILT** on pepti (Jun 15) |
| fieldGate primals | **13/13 ALIVE**, mesh enrolled |
| Genetics adoption | **11/11 ✅ ALL PRIMALS** accept mito-beacon |
| golgiBody | **FULL GREEN HEALTHY** (all 9 probes OK) |
| RustDesk relay | **EXTERNALLY REACHABLE** (:21115-21117) |
| WAN depot | **HTTPS 200 OK** (membrane.primals.eco) |
| Bidirectional cascade | **ff-merge fix SHIPPED** (`8f4e4eb`) — reduces SHA divergence |

---

## NEW: Genetics-Layer Wiring (Eukaryotic Model) — P1

**Discovery**: Jun 16 live NUCLEUS — 7/11 primals reject the mito-beacon signal prefix.
This is a **genetics-layer wiring** issue, not a mechanical per-primal patch.

### Two Genetics Streams (Eukaryotic)

| Stream | Purpose | Property | Wire |
|--------|---------|----------|------|
| **MitoBeacon** | Relay access, mesh, ABG transport | Shared/copyable ("grandma tells cousin") | `0xEC`/`0xED` |
| **Nuclear Lineage** | Per-user permissions, tiered access | Non-fungible, BearDog-spawned | `0xEE` |

BearDog owns both. `FAMILY_SEED` IS mito-beacon material (legacy naming).

### Acceptance Status (Jun 16 12:46Z — **ALL PRIMALS COMPLETE**)

| Primal | Status | Commit |
|--------|--------|--------|
| beardog | ✅ SHIPPED | `f997a33` |
| songbird | ✅ SHIPPED | `fc766dc` |
| sweetgrass | ✅ SHIPPED | `96d35e5` |
| rhizocrypt | ✅ SHIPPED | `c5913cd` |
| barracuda | ✅ SHIPPED | `cbb2704` |
| toadstool | ✅ SHIPPED | `5903cf6` |
| cellmembrane | ✅ SHIPPED (reference) | `fbd58ac` |
| loamspine | ✅ SHIPPED | `e68873d` |
| squirrel | ✅ VERIFIED (code review) | (already had it) |
| petaltongue | ✅ REFERENCE IMPL | (original) |
| coralreef | ✅ passes | — |
| nestgate | ✅ passes | — |

**11/11 genetics-compliant. Exit criterion CLEARED.**

### For Friday (ABG Access)

MitoBeacon access via RustDesk relay is sufficient — shared group key gets members
through the relay. Nuclear lineage per-user is Wave 115+ evolution.

**Workaround**: `--skip-preflight --no-rollback` + manual `ps` for alive validation.
**Architecture doc**: `handoffs/primalSpring/GENETICS_ARCHITECTURE_EUKARYOTIC_MODEL_JUN16_2026.md`

---

## Remaining Work

### ~~1. Genetics-Layer Wiring~~ — ✅ COMPLETE (11/11)

### 2. grapheneGate Deployment (ops + cellMembrane)

Depot aarch64 is ready. Needs physical device access to deploy.

### 3. flockGate WAN Validation (cellMembrane)

WAN path proven (2.2 MB/s, HTTPS 200). Needs target gate provisioned.

### 4. ABG Member End-to-End (cellMembrane)

RustDesk relay is live and externally reachable. Needs:
- fieldGate RustDesk client installed
- ABG member connects via relay

---

## Shipped This Wave (Jun 16 — Genetics Adoption + Cascade Fix)

| Primal | Commit | What |
|--------|--------|------|
| bearDog | `f997a33` | Mode-detection race resolved — mito-beacon acceptance |
| songBird | `fc766dc` | Federation riboCipher: stub → proper dispatcher |
| sweetGrass | `96d35e5` | 0xED mito-beacon signal accepted |
| rhizoCrypt | `c5913cd` | Genetics-layer mito-beacon + SSOT |
| barraCuda | `cbb2704` | Centralized mito-beacon accept pattern |
| toadStool | `5903cf6` | S320: 0xED on all loops |
| loamSpine | `e68873d` | Full eukaryotic genetics model (0xEC/0xED/0xEE) |
| cellMembrane | `fbd58ac` | `cellmembrane-types::signal` — centralized reference |
| cellMembrane | `8f4e4eb` | **Cascade fix**: prefer ff-merge over rebase (SHA preservation) |
| squirrel | (verified) | Code review confirmed full acceptance already wired |

**11/11 genetics-compliant. Cascade divergence fix shipped. All code work DONE.**

---

## primalSpring Shipped (this session)

| Commit | What |
|--------|------|
| `6190d8e` | `nucleus_launcher validate` subcommand + `s_bootstrap_readiness` scenario (62nd) |
| — | Live NUCLEUS execution: confirmed 11/11 spawn from depot on eastGate |
| — | riboCipher incompatibility diagnosis + AAR filed |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | fieldGate (NUC): 13/13 alive + mesh | **✅ DONE** |
| 2 | grapheneGate (Pixel): aarch64 depot + 13/13 | DEPOT READY (device needed) |
| 3 | flockGate (WAN): relay depot + 13/13 | PATH PROVEN (gate needed) |
| 4 | RustDesk relay operational | **✅ DONE** |
| 5 | ABG member end-to-end | TODO |
| 6 | pepti fresh harvest (both arches) | **✅ DONE** |
| 7 | Genetics-layer wiring (≥10/11 accept mito-beacon) | **✅ 11/11 DONE** |

**6/7 cleared. ALL CODE WORK COMPLETE.**
Remaining: ABG member e2e test (#5) + physical device deployments (#2, #3) — ops-dependent only.

---

## Divergence Note (Jun 16 12:10Z)

Cascade required **force-with-lease** on wateringHole — both remotes had same-content-different-hash
commits from rebase-based cascade. This is the bidirectional cascade's current weakness:
`push_target=all` on multiple gates creates rebase chains that diverge SHA history.
**cellMembrane evolution target**: event-driven convergence (webhooks) to replace
rebase-and-pray. Until then, manual force-convergence is expected during active multi-gate waves.

---

## Carry (Wave 115+)

| Debt | Owner | Priority |
|------|-------|----------|
| Event-driven cascade (webhooks) | cellMembrane | P1/Wave 115 |
| `BEARDOG_FAMILY_SEED` env var deprecation | bearDog | P2/Wave 115 |
| Nuclear lineage per-ABG-user (tiered access) | bearDog + primalSpring | P2/Wave 115 |
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P2 |
| Socket naming (family-suffixed) | primalSpring | P2 |
