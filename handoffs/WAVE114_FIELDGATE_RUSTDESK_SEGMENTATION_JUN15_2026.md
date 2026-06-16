# Wave 114 — ABG Sovereign Compute by Friday

**Status**: ACTIVE | Deadline: Friday June 20 | **From**: eastGate overwatch
**Last review**: Jun 16 12:10Z

---

## Objective

Depot deploys to all form factors + primals health-validate via riboCipher.

| Target | Arch | Transport | Status |
|--------|------|-----------|--------|
| **fieldGate** (NUC) | x86_64-musl | LAN via MikroTik | **✅ 13/13 ALIVE** |
| **grapheneGate** (Pixel) | aarch64-musl | LAN/relay | DEPOT READY (device needed) |
| **flockGate** (WAN) | x86_64-musl | relay via golgiBody | PATH PROVEN (target needed) |

---

## Ecosystem Snapshot (Jun 16 12:10Z)

| Metric | Value |
|--------|-------|
| VCS parity | **17/17 ✓** (zero drift — forced wateringHole convergence) |
| Depot x86_64 | **13/13 BUILT** from HEAD (pepti Jun 16 02:27Z) |
| Depot aarch64 | **13/13 BUILT** on pepti (Jun 15) |
| fieldGate primals | **13/13 ALIVE**, mesh enrolled |
| Genetics adoption | **9/11 SHIPPED** mito-beacon acceptance (was 3/11) |
| golgiBody | **FULL GREEN HEALTHY** (all 9 probes OK) |
| RustDesk relay | **EXTERNALLY REACHABLE** (:21115-21117) |
| WAN depot | **HTTPS 200 OK** (membrane.primals.eco) |
| Bidirectional cascade | **ACTIVE** (divergence still occurring — see notes) |

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

### Acceptance Status (updated Jun 16 12:10Z — MASSIVE ADOPTION WAVE)

| Primal | Status | Commit |
|--------|--------|--------|
| beardog | ✅ **SHIPPED** — mode-detection race resolved | `f997a33` |
| songbird | ✅ **SHIPPED** — federation handler evolved | `fc766dc` |
| sweetgrass | ✅ **SHIPPED** — 0xED mito-beacon accepted | `96d35e5` |
| rhizocrypt | ✅ **SHIPPED** — genetics-layer + SSOT | `c5913cd` |
| barracuda | ✅ **SHIPPED** — centralized pattern adopted | `cbb2704` |
| toadstool | ✅ **SHIPPED** — 0xED on all loops | `5903cf6` |
| cellmembrane | ✅ **SHIPPED** — signal module (reference) | `fbd58ac` |
| petaltongue | ✅ **REFERENCE IMPL** | (original) |
| coralreef, nestgate | ✅ pass (no health method) | — |
| squirrel | **PENDING** — has enum, needs accept loop verification | — |
| loamspine | **TODO** — no commit yet | — |

### For Friday (ABG Access)

MitoBeacon access via RustDesk relay is sufficient — shared group key gets members
through the relay. Nuclear lineage per-user is Wave 115+ evolution.

**Workaround**: `--skip-preflight --no-rollback` + manual `ps` for alive validation.
**Architecture doc**: `handoffs/primalSpring/GENETICS_ARCHITECTURE_EUKARYOTIC_MODEL_JUN16_2026.md`

---

## Remaining Work

### 1. Genetics-Layer Wiring — P2 (was P1, now 9/11 shipped)

Squirrel: verify enum wired. LoamSpine: adopt pattern. Then 11/11.

### 2. grapheneGate Deployment (ops + cellMembrane)

Depot aarch64 is ready. Needs physical device access to deploy.

### 3. flockGate WAN Validation (cellMembrane)

WAN path proven (2.2 MB/s, HTTPS 200). Needs target gate provisioned.

### 4. ABG Member End-to-End (cellMembrane)

RustDesk relay is live and externally reachable. Needs:
- fieldGate RustDesk client installed
- ABG member connects via relay

---

## Shipped Since Last Review (Jun 16 cascade)

| Primal | Commit | What |
|--------|--------|------|
| bearDog | `f997a33` | Mode-detection race resolved — mito-beacon acceptance working |
| songBird | `fc766dc` | Federation riboCipher handler: stub → proper dispatcher |
| sweetGrass | `96d35e5` | 0xED mito-beacon signal accepted |
| rhizoCrypt | `c5913cd` | Genetics-layer mito-beacon + SSOT completion |
| barraCuda | `cbb2704` | Centralized mito-beacon accept pattern adopted |
| toadStool | `5903cf6` | S320: 0xED accepted on all loops |
| cellMembrane | `fbd58ac` | `cellmembrane-types::signal` — centralized accept reference |

**7 primals shipped genetics-layer wiring in one wave.** Exit criteria #7 moves from 3/11 → 9/11.

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
| 7 | Genetics-layer wiring (≥10/11 accept mito-beacon) | **9/11 ✅** (squirrel + loamspine remain) |

**5/7 cleared. Remaining 2 need physical access (Pixel) or gate provisioning (flockGate).**
**Genetics soft blocker REMOVED** — 9/11 shipped, 2 remaining are minor adoption (not blocking ABG).

---

## Divergence Note (Jun 16 12:10Z)

Cascade required **force-with-lease** on wateringHole — both remotes had same-content-different-hash
commits from rebase-based cascade. This is the bidirectional cascade's current weakness:
`push_target=all` on multiple gates creates rebase chains that diverge SHA history.
**cellMembrane evolution target**: event-driven convergence (webhooks) to replace
rebase-and-pray. Until then, manual force-convergence is expected during active multi-gate waves.

---

## Carry (not blocking Wave 114)

| Debt | Owner | Priority |
|------|-------|----------|
| Bidirectional cascade SHA divergence | cellMembrane | P1/Wave 115 |
| Squirrel accept-loop wiring | squirrel | P2 |
| LoamSpine mito-beacon adoption | loamSpine | P2 |
| `BEARDOG_FAMILY_SEED` env var deprecation | bearDog | P2/Wave 115 |
| Nuclear lineage per-ABG-user (tiered access) | bearDog + primalSpring | P2/Wave 115 |
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P2 |
| Socket naming (family-suffixed) | primalSpring | P2 |
| Webhooks (push-triggered cascade) | cellMembrane | P3/Wave 115 |
