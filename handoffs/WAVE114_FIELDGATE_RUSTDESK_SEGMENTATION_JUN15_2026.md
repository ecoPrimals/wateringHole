# Wave 114 — ABG Sovereign Compute

**Status**: CODE COMPLETE | Deadline: Friday June 20 | **From**: eastGate overwatch
**Last review**: Jun 16 15:31Z

---

## Result: 6/7 Exit Criteria CLEARED — All Code Work DONE

| # | Criterion | Status |
|---|-----------|--------|
| 1 | fieldGate (NUC): 13/13 alive + mesh | **✅ DONE** |
| 2 | grapheneGate (Pixel): aarch64 depot + 13/13 | DEPOT READY (ops: device needed) |
| 3 | flockGate (WAN): relay depot + 13/13 | PATH PROVEN (ops: gate needed) |
| 4 | RustDesk relay operational + health-probed | **✅ DONE** |
| 5 | ABG member end-to-end | TODO (ops: first member test) |
| 6 | pepti fresh harvest (both arches) | **✅ DONE** |
| 7 | Genetics-layer wiring (11/11 accept mito-beacon) | **✅ DONE** |

**Remaining items are ops-only** (physical device access, first ABG member walkthrough).

---

## Ecosystem Snapshot (Jun 16 15:31Z)

| Metric | Value |
|--------|-------|
| VCS parity | **17/17 ✓** (zero drift, primalSpring pushed 14 local→origin) |
| Genetics | **11/11 ✅** ALL primals accept mito-beacon |
| Depot x86_64 | **13/13 BUILT** from HEAD (pepti Jun 16 02:27Z) |
| Depot aarch64 | **13/13 BUILT** on pepti (Jun 15) |
| fieldGate | **13/13 ALIVE**, mesh enrolled |
| ironGate | **DRY-RUN 11/11 PASS**, depot 14/14 verified, ready for live bootstrap |
| golgiBody | **FULL GREEN HEALTHY** (16 services, 28 sockets, 13/13 alive) |
| RustDesk relay | **EXTERNALLY REACHABLE** (:21115-21117) |
| WAN depot | **HTTPS 200 OK** (membrane.primals.eco) |
| Cascade | **ff-merge fix SHIPPED** (`8f4e4eb`) — SHA preservation in common case |

---

## Wave 114 Shipped (complete record)

### Genetics-Layer (11/11)

| Primal | Commit |
|--------|--------|
| bearDog | `f997a33` — mode-detection race resolved |
| songBird | `fc766dc` — federation handler: stub → dispatcher |
| sweetGrass | `96d35e5` — 0xED mito-beacon accepted |
| rhizoCrypt | `c5913cd` — genetics-layer + SSOT |
| barraCuda | `cbb2704` — centralized pattern adopted |
| toadStool | `5903cf6` — S320: 0xED all loops |
| loamSpine | `e68873d` — full eukaryotic model |
| cellMembrane | `fbd58ac` — signal module reference |
| squirrel | (verified) — already wired |
| petalTongue | (original) — reference impl |
| coralReef/nestGate | passes (no health method) |

### cellMembrane Deployment Hardening

| Commit | What |
|--------|------|
| `fed3335` | Robust bootstrap: systemd, install, secrets, permissions (7 hurdles) |
| `c032abf` | Mesh retry loop, docs |
| `8f4e4eb` | Cascade fix: ff-merge over rebase (SHA preservation) |
| `63a2130` | **Unified depot resolution**, env-configurable paths, capability-based freshness, multi-peer mesh |
| `9dc6a1d` | **Version reporting** (`membrane --version`), socket alias registry (28 sockets documented) |

### Infrastructure

| What | Detail |
|------|--------|
| pepti x86_64 harvest | 13/13 from HEAD (104min, exit 0) |
| pepti aarch64 harvest | 13/13 (toadstool manual for OOM) |
| RustDesk UFW | :21115-21117 opened |
| WAN depot | HTTPS 200 serving |
| ironGate dry-run | 11/11 PASS, depot verified |

---

## VPS Diderm Layer Audit (11 divergences found)

**Full AAR**: FRAGO `aar_jun16_1430_vps_divergence`

Key findings from ironGate audit of golgiBody + pepti:

| # | Divergence | Impact |
|---|-----------|--------|
| 1 | Three competing depot paths | Confusion during bootstrap |
| 2 | No cellMembrane clone on golgiBody | Cannot self-update |
| 3 | Binary version lag (pre-63a2130) | Missing all path fixes |
| 4 | Socket explosion (28 vs 13 expected) | Undocumented capability aliases |
| 5 | Systemd unit style mismatch | Hand-crafted vs bootstrap-generated |
| 6 | Environment/secrets model split | tower.env vs secrets.env |
| 7 | Unknown SONGBIRD_PEERS IPs | Undocumented mesh nodes |
| 8 | Legacy socat bridges (no TLS) | Fragile relay function |
| 9 | Deployment debris in /opt/membrane/ | Archive needed |
| 10 | pepti: no deployed binaries | Cannot self-validate harvest |
| 11 | pepti: source tree with no operational role | Needs tier decision |

---

## Wave 115 Shape (Deployment Hardening + VPS Convergence)

### P1: VPS Layer Convergence (cellMembrane/ironGate)

- Redeploy `membrane` binary on golgiBody (include `63a2130` + `9dc6a1d`)
- Consolidate depot paths to single canonical (`infra/plasmidBin/`)
- Clone cellMembrane on golgiBody for self-update capability
- Decide pepti operational tier (Tower Atomic minimum)

### P1: Event-Driven Cascade (cellMembrane)

- Replace manual force-convergence with webhook-triggered sync
- ff-merge fix (`8f4e4eb`) is interim — webhooks eliminate the race entirely

### P2: Socket Naming Standard (cellMembrane + primalSpring)

- Codify capability → socket name mapping in `cellmembrane-types`
- Bootstrap generates canonical + alias sockets from registry
- Eliminates ad-hoc FAMILY_ID suffixing

### P2: Deployment Atomicity (cellMembrane)

- Canary promote pattern: new binary → sandbox socket → health verify → atomic swap
- Replace bash `deploy_membrane.sh` with Rust-native `plasmid.refresh`

### P2: Environment Consolidation (cellMembrane)

- Unify tower.env + secrets.env → structured env.d/ approach
- Role-based files: tower.env, family.env, mesh.env

### P3: Bridge Evolution (cellMembrane + songBird)

- socat TCP bridges → Rust-native transport with mTLS
- songBird federation subsumes bridge function

### Carry

| Debt | Owner | Priority |
|------|-------|----------|
| `BEARDOG_FAMILY_SEED` deprecation | bearDog | P2 |
| Nuclear lineage per-ABG-user | bearDog + primalSpring | P2 |
| Network segmentation enforcement | cellMembrane | P2 |
| neuralAPI hollow (0 registrations) | biomeOS | P3 |
| Peer registry (mesh.peers RPC) | songBird | P3 |

---

## Genetics Architecture (reference)

| Stream | Purpose | Property | Wire |
|--------|---------|----------|------|
| **MitoBeacon** | Relay access, mesh, ABG transport | Shared/copyable | `0xEC`/`0xED` |
| **Nuclear Lineage** | Per-user permissions, tiered access | Non-fungible, BearDog-spawned | `0xEE` |

BearDog owns both. `FAMILY_SEED` = mito-beacon material.
Architecture doc: `handoffs/primalSpring/GENETICS_ARCHITECTURE_EUKARYOTIC_MODEL_JUN16_2026.md`
