# Glacial Shift Readiness

**Status**: Active tracking document  
**Phase**: Interstadial exit → Stadial entry  
**Last updated**: 2026-05-25 (post-tightening re-audit)

---

## Position

The ecosystem has cleared the interstadial exit gate (~9.5/10). 13/13 primals
at zero debt. cellMembrane VPS operational (relay + TLS/content shadows).
Shadow tracks S1-S3 proven. 4-gate NUCLEUS operational (eastGate, ironGate,
southGate, biomeGate) with Songbird TCP :7700 federation — cross-gate
`discovery.peers` verification is **NEXT** (peer seeding shipped Wave 49).

**Wave 47 milestone**: 13/13 behavioral convergence — all primals accept
`--socket`, return `{"status":"alive"}` from `health.liveness`, handle
SIGTERM+SIGINT, and implement `lifecycle.status`.

**Wave 48 milestone**: Covalent spring mesh — **all 8/8 springs sounded off**.
4 gates operational with NUCLEUS + Songbird TCP :7700 federation.

**Wave 49 milestone**: Post-primordial + ecosystem tightening. plasmidBin-only
deployment enforced across all launchers. 8/8 primal showcases fossilized
(barraCuda, bearDog, loamSpine, petalTongue, rhizoCrypt, skunkBat, sweetGrass,
toadStool). 7 primals responded with tightening handoffs same-day (rhizoCrypt,
Songbird, biomeOS, coralReef, sweetGrass, toadStool, bearDog). Songbird wired
`mesh.init` with `bootstrap_peers` for cross-gate TCP discovery. rhizoCrypt
fixed startup latency (was >8s, pipeline debt item). bearDog Wave 113b:
orphan purge — cloud KMS/mobile HSM/PKCS11 discovery code removed (~15k LOC),
method count drift fixed (127). toadStool: orchestrator dispatch tests added,
Unix socket improvements. primalSpring: 789 tests, 53 scenarios, 458 methods,
95 deploy graphs, superseded specs archived, metric drift fixed across 15+ docs.

**Climate-sensitive sentinels** (primals whose readiness gates the glacial shift):

- **Songbird**: `mesh.init` + `bootstrap_peers` now wired (Wave 49). Cross-gate
  `discovery.peers` verification **NEXT** — same-subnet gates need live test.
  sled DB corruption on unclean shutdown remains a workaround-only issue.
- **bearDog**: ACME renewal daemon operational. Massive orphan purge (Wave 113b)
  cleared 15k LOC of dead discovery code. Vault (encrypted creds at rest) still
  PLANNED. S4 auth shadow depends on bearDog BTSP dual-auth.
- **toadStool**: Yield-to-owner dispatch enforced (S274). Orchestrator tests
  added (S275). 36 unmirrored wateringHole handoffs need archive hygiene.
- **biomeOS**: v3.75 clean — no showcase, no stale patterns. LiveSpore USB
  deploy script still uses `~/.local/bin` (conflicts with plasmidBin mandate).
  Neural API mesh dispatch ready for cross-gate `capability.call`.
- **petalTongue**: WASM client-side rendering live. musl binary still rejects
  `--family-id` (workaround: `FAMILY_ID` env). Local fossilRecord in-repo
  (not synced to central).

**Upstream leads, downstream lags**: Primals on the mountain (bearDog, Songbird,
toadStool, NestGate, biomeOS) are tightened and ready to push through the gate.
Springs lag on cleanup (neuralSpring still has stale `target/release/` hardcode,
hotSpring absorbed Wave 50 post-primordial mandate — NUCLEUS launched on biomeGate,
plasmidBin-only enforced, pseudoSpore v1.5.0 GuideStone-grade). The shift moves when
the sentinels clear — springs follow.

**LAN is live** — Cat6 1G backbone on unmanaged switch connects all gates.
10G (switch + NICs installed, Cat6a cables pending) is an elevation goal for
Tier 2+ large-dataset science, not a deployment blocker.

---

## Readiness Matrix

### Sovereignty Shadows (H2)

| Track | What | Sovereign | Commercial | Status | Cutover gate |
|-------|------|-----------|------------|--------|--------------|
| **S1** | TLS termination | BearDog :8443 (~10ms) | Cloudflare (~120ms) | **LIVE** | 7-day p95 <= 1.5x |
| **S2** | NAT relay | Songbird TURN :3478 | cloudflared tunnel | **LIVE** (100% 3+ days) | 7-day 100% reachable |
| **S3** | Content serving | NestGate + petalTongue (67ms TTFB) | GitHub Pages (111ms) | **LIVE** | 7-day TTFB parity |
| **S4** | Auth | BearDog BTSP dual-auth | OAuth2/PAM proxy | **READY** (code built) | 7-day p95 < 50ms |

**Remaining**: Complete S4 shadow period, then formal 7-day all-track cutover gate.

### cellMembrane (inner membrane)

| Component | Status |
|-----------|--------|
| VPS (157.230.3.183, DO nyc1) | **OPERATIONAL** |
| Channel 2: Songbird TURN relay | **LIVE** |
| Channel 2b: RustDesk hbbs/hbbr | **LIVE** |
| Channel 3: TLS surface (Caddy + ACME) | **LIVE** |
| Tower composition (BearDog + Songbird + SkunkBat) | **DEPLOYED** |
| Nest expansion (rhizoCrypt + loamSpine + sweetGrass) | Tooling shipped, **not deployed on VPS yet** |
| Channel 1: Sovereign DNS (knot-dns) | **PLANNED** |
| Caddy → BearDog ACME replacement | Shadow live, **not cut over** |
| BearDog Vault (encrypted creds at rest) | **PLANNED** (Phase 2) |

### LAN Gate Deployment

| Gate | Hardware | Role | NUCLEUS status | Springs | LAN |
|------|----------|------|----------------|---------|-----|
| **eastGate** | i9-12900, RTX 4070 + Akida, 32GB | Orchestrator, neuromorphic | **OPERATIONAL** | primalSpring, airSpring, groundSpring | 1G |
| **ironGate** | i9-14900K, RTX 5070, 96GB | Agentic dev, ABG | **OPERATIONAL** (23 UDS) | primalSpring, ludoSpring, healthSpring | 1G |
| **southGate** | 5800X3D, RTX 4060 + 3090s, 128GB | Gaming + compute | **OPERATIONAL** (9/9) | wetSpring, neuralSpring | 1G (10G NIC ready) |
| **biomeGate** | Threadripper 3970X, 256GB | HBM2 test bench | **OPERATIONAL** (62/62) | hotSpring | 1G |
| **strandGate** | Dual EPYC 7452 (64c), 256GB ECC | Bioinformatics | Hardware ready, **not deployed** | wetSpring (secondary) | 1G |
| **northGate** | Ryzen 9950X3D, RTX 5090, 96GB | Gaming primary, heavy compute | Hardware ready, **not deployed** | — | 1G (10G NIC ready) |
| **westGate** | i7-4771, RTX 2070 Super, 32GB | 76TB ZFS cold storage | Hardware ready, **not deployed** | — | 1G (10G NIC ready) |
| **swiftGate** | Ryzen 5800X, RTX 3070, 64GB | Mobile/compact | Hardware ready | — | 1G |
| **flockGate** | i9-13900K, RTX 3070 Ti, 64GB | Remote covalent (WAN) | Config ready, **not deployed** | — | WAN via cellMembrane |
| **kinGate** | i7-6700K, RTX 3070, 32GB | Staging | Hardware ready | — | 1G |

**Covalent mesh order** (over existing 1G LAN):
1. ~~Enable `SONGBIRD_FEDERATION_PORT=7700` on eastGate + ironGate + southGate + biomeGate~~ **DONE** (Wave 48)
2. ~~Peer seeding mechanism~~ **DONE** (Wave 49) — `SONGBIRD_PEERS` env + `--peers` CLI + `mesh.init` RPC
3. ~~Springs declare gates, deploy cells, cut primordial patterns~~ **DONE** (4/4 responding springs confirmed)
4. Verify cross-gate `discovery.peers` — **NEXT**: same-subnet gates (eastGate ↔ ironGate) seed peers, confirm peer count > 0
5. Cross-gate `capability.call` smoke test via primalSpring `s_covalent_mesh` scenario
6. Cross-subnet routing for southGate (192.168.4.x) — requires network config or TURN relay
7. westGate (Nest Atomic — cold storage), northGate (Node Atomic), strandGate (Full NUCLEUS)
8. Plasmodium collective validation (3+ gates meshed via live `capability.call`)

### Deployment Matrix (primalSpring)

| Cell | Status |
|------|--------|
| `tower-x86-homelan-uds` | **PASS** (golden path) |
| `lithospore-x86-vm-uds` | **PASS** |
| `nucleus-aarch64-mixed-tcp` | **BLOCKED** (nestgate aarch64-musl segfault) |
| 41 other cells | **UNTESTED** |

**P0 target**: `nucleus-x86-mixed-uds` — full NUCLEUS over LAN.

### Distributed Covalent (Phase 4)

| Item | Status |
|------|--------|
| Family seed + bootstrap tooling | **READY** |
| cellMembrane VPS rendezvous | **OPERATIONAL** |
| Songbird TCP/WAN fallback | **SHIPPED** (Wave 213-214) |
| Songbird TCP federation on LAN | **LIVE** — 4 gates with :7700 (Wave 48) |
| Rust `nucleus_launcher` `--federation-port` | **SHIPPED** — Wave 48 |
| NAT traversal (STUN/punch/TURN) | Shipped, **not field-tested** on residential NAT |
| toadStool yield-to-owner dispatch | **ENFORCED** (S274 + S275 orchestrator tests) |
| Cross-gate data dependency staging | **PROTOTYPED** (primalSpring `validation::dependency`) |
| Songbird peer seeding (`SONGBIRD_PEERS`) | **SHIPPED** — Wave 49, both launchers, CLI + env + RPC |
| Songbird `mesh.init` + `bootstrap_peers` | **WIRED** — Wave 49, Songbird team confirmed functional |
| Cross-gate `discovery.peers` verification | **UNBLOCKED** — peer seeding shipped, same-subnet test next |
| Cross-subnet mesh (southGate ↔ eastGate) | **BLOCKED** — different subnets, needs routing or TURN relay |
| Plasmodium collective status | **PENDING** — requires 3+ same-subnet gates meshed first |
| flockGate live deployment | **NOT DEPLOYED** |

### Wave 49 Ecosystem Issues (post-tightening re-audit, May 25)

| Issue | Reporter | Status |
|-------|----------|--------|
| loamSpine Tokio panic on health probe | wetSpring, neuralSpring | **UPSTREAM** — does not block mesh |
| rhizoCrypt slow startup (>8s) | wetSpring | **FIXED** Wave 49 — `announce_to_biomeos()` off critical path |
| sweetGrass/toadStool slow startup (>8s) | wetSpring | **KNOWN** — cold-start timing, not blocking |
| Songbird `--security-socket` rejected | wetSpring | **FIXED** Wave 49 — feature-guarded + env fallback |
| petalTongue stale socket on restart | primalSpring | **FIXED** Wave 49 — launcher pre-cleans dead sockets |
| `discovery.peers` returns empty | healthSpring | **FIXED** Wave 49 — Songbird `mesh.init` + `bootstrap_peers` wired |
| southGate ≠ eastGate subnet | neuralSpring | **DOCUMENTED** — needs routing or TURN relay |
| petalTongue musl rejects `--family-id` | primalSpring | **PIPELINE DEBT** — workaround: `FAMILY_ID` env |
| Songbird sled DB corruption (unclean) | neuralSpring | **WORKAROUND** — clean `task_lifecycle*` |
| biomeOS LiveSpore deploys to `~/.local/bin` | re-audit | **STALE PATTERN** — conflicts with plasmidBin-only |
| neuralSpring petalTongue `target/release/` | re-audit | **STALE PATTERN** — only diverging spring launcher |
| toadStool/loamSpine local wH unarchived | re-audit | **HYGIENE** — 37+14 flat handoffs need archive subdir |
| Central fossilRecord incomplete | re-audit | **SYNC GAP** — 7/8 primals archived, central repo sparse |
| hotSpring Wave 50 compliant | resolved | **CURRENT** — pseudoSpore v1.5.0, NUCLEUS launched, plasmidBin-only |

### Software Remaining

| Item | Owner | Priority | Status |
|------|-------|----------|--------|
| Cross-gate `discovery.peers` smoke test | primalSpring | **HIGH** | Peer seeding + `mesh.init` shipped — same-subnet test with `SONGBIRD_PEERS` next |
| Cross-gate `capability.call` smoke test | primalSpring | **HIGH** | biomeOS v3.75 mesh dispatch ready, `s_covalent_mesh` scenario written, needs live run |
| Cross-subnet routing (southGate ↔ eastGate) | infra/network | **MEDIUM** | Different subnets block direct federation; needs router config or TURN relay |
| Cross-gate `nest.sync` live orchestration | biomeOS | MEDIUM | v3.64 `nest.sync` graph shipped. Songbird mesh (v3.75) is the transport. Pending multi-gate connectivity. |
| Sovereign DNS (knot-dns) | cellMembrane | MEDIUM | PLANNED |
| `content.put` publish pipeline (SP-4) | sporePrint + bearDog | LOW | `publish_sporeprint.sh` implemented. E2E requires live NestGate + bearDog session. |
| Forgejo Actions CI | projectNUCLEUS | LOW | PLANNED |
| loamSpine Tokio runtime-in-runtime panic | loamSpine | MEDIUM | Upstream bug — blocks health probe on 2 gates |
| Central fossilRecord sync | all primals | LOW | 7/8 primals reference central paths that don't exist yet |
| neuralSpring composition_nucleus.sh fix | neuralSpring | MEDIUM | Only spring with stale `target/release/` primal hardcode |

**Resolved** (fossilized): Ionic bond runtime (WS-1), biomeOS mesh dispatch,
BearDog ACME renewal daemon, rhizoCrypt startup latency, Songbird `--security-socket`,
stale socket cleanup, 8/8 showcase fossilizations — see `fossilRecord/` for detail.

---

## Glacial Shift Criteria

The glacial shift (stadial entry) is reached when:

1. All 4 sovereignty shadows **cut over** (S1-S4 formal 7-day gate passed)
2. Multi-gate LAN mesh **operational** (3+ gates in Plasmodium collective) — Wave 49: peer seeding + mesh.init shipped, same-subnet verification **next**, cross-subnet routing **needed**
3. cellMembrane Nest expansion **deployed** on VPS
4. At least one remote covalent node (flockGate) **validated** over WAN
5. DNS pointed to sovereign infrastructure
6. Cloudflare/cloudflared **removed** from production data path

**Current assessment**: Criteria 1 is 3/4 (S4 shadow remaining). Criteria 2 is
unblocked — peer seeding and mesh.init are wired, live same-subnet test is next.
Primals on the mountain are tightened (Wave 49). The shift moves when sentinels
Songbird + bearDog clear the cross-gate verification and S4 auth shadow completes.

---

## References

- `INTERSTADIAL_EXIT_CRITERIA.md` — 5 pillars + shadow schedule
- `SOVEREIGNTY_STANDARDS.md` — calibrate → shadow → cutover protocol
- `CELLMEMBRANE_FIELDMOUSE_DEPLOYMENT.md` — VPS composition spec
- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — 3 channels + RustDesk
- `DARK_FOREST_GLACIAL_GATE_STANDARD.md` — 5 security invariants
- `DISTRIBUTED_COVALENT_DEPLOYMENT.md` — multi-household compute architecture
- `DESKTOP_NUCLEUS_DEPLOYMENT.md` — single-machine full stack
