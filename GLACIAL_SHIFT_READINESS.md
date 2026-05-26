# Glacial Shift Readiness

**Status**: Active tracking document  
**Phase**: Interstadial exit → Stadial entry  
**Last updated**: 2026-05-25 (Wave 50 — 7/7 springs covalent HPC)

---

## Position

The ecosystem has cleared the interstadial exit gate (~9.7/10). 13/13 primals
at zero debt. cellMembrane VPS operational (relay + TLS/content shadows).
Shadow tracks S1-S3 proven. 4-gate NUCLEUS operational (eastGate, ironGate,
southGate, biomeGate) with Songbird TCP :7700 federation. **7/7 delta springs
responded to Wave 50 covalent HPC blurb** — all gates have NUCLEUS running,
mesh seeded, post-primordial confirmed. Cross-subnet routing confirmed
(southGate ↔ eastGate, 4ms, no TURN needed). `discovery.peers` population
is the remaining Songbird evolution item.

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
Unix socket improvements. primalSpring: 791 tests, 53 scenarios, 458 methods,
95 deploy graphs, superseded specs archived, metric drift fixed across 15+ docs.
petalTongue: `--family-id` CLI now accepted (Wave 49 commit `bb5cdc9`),
showcase pointer updated to central fossilRecord. **All sentinel debt cleared.**
Full NUCLEUS 12/12 redeployed from plasmidBin musl binaries — barraCuda
pgrep collision bug fixed (spring cell binary false positive blocked startup).

**Wave 50 milestone**: Covalent HPC — **all 7/7 delta springs responded**.
4 gates running NUCLEUS with Songbird :7700. Cross-subnet routing confirmed
(southGate 192.168.4.29 ↔ eastGate 192.168.1.144, 4ms via router — no TURN
needed). neuralSpring fixed last `target/release/` hardcode (V175). hotSpring
absorbed post-primordial (pseudoSpore v1.5.0, 9 primals on biomeGate).
ludoSpring resolved GAP-01 coralReef (live `shader.compile.wgsl` validation).
healthSpring validated dual-tower + Nest Atomic against live NUCLEUS (14/17
sockets). plasmidBin CLI alignment fixed upstream by ludoSpring (barracuda
`--unix`, rhizocrypt `--unix`, nestgate `server --socket-only`).

| Gate | NUCLEUS | Springs | Mesh seeded |
|------|---------|---------|-------------|
| eastGate | 12/12 | airSpring, groundSpring, primalSpring | ironGate |
| ironGate | 12/12 | healthSpring, ludoSpring | eastGate |
| southGate | 12/13 | neuralSpring, wetSpring | eastGate (bidirectional verified) |
| biomeGate | 9 primals | hotSpring | Registry seeded |

**Remaining blocker**: `discovery.peers` returns empty on all gates after
`mesh.init` succeeds. Songbird v0.2.1 initializes mesh state but does not
populate the peer list. This is the next Songbird evolution item — not a
configuration or deployment issue.

**Climate-sensitive sentinels** (primals whose readiness gates the glacial shift):

- **Songbird**: `mesh.init` + `bootstrap_peers` wired (Wave 49). Cross-gate
  mesh tested Wave 50 — `mesh.init` succeeds bidirectionally across subnets,
  but `discovery.peers` returns empty (v0.2.1 feature gap — peer list not
  populated). sled DB corruption on unclean shutdown remains workaround-only.
  **NEXT**: Songbird evolution to populate `discovery.peers` after `mesh.init`.
- **bearDog**: ACME renewal daemon operational. Massive orphan purge (Wave 113b)
  cleared 15k LOC of dead discovery code. Vault (encrypted creds at rest) still
  PLANNED. S4 auth shadow depends on bearDog BTSP dual-auth.
- **toadStool**: Yield-to-owner dispatch enforced (S274). Orchestrator tests
  added (S275). 36 unmirrored wateringHole handoffs need archive hygiene.
- **biomeOS**: v3.75 clean — no showcase, no stale patterns. LiveSpore USB
  deploy script still uses `~/.local/bin` (conflicts with plasmidBin mandate).
  Neural API mesh dispatch ready for cross-gate `capability.call`.
- **petalTongue**: WASM client-side rendering live. `--family-id` now accepted
  (Wave 49, commit `bb5cdc9`). Showcase pointer updated to central fossilRecord.
  **CLEAR** — no remaining sentinel-blocking items.

**Delta has caught up**: All 7 springs at Wave 50. neuralSpring fixed its last
`target/release/` hardcode (V175). hotSpring absorbed post-primordial (NUCLEUS
on biomeGate, plasmidBin-only). The gap is now Songbird v0.2.1's `discovery.peers`
population — when that ships, cross-gate `capability.call` unlocks covalent HPC.
southGate primal instability (7/13 health-responding per wetSpring vs 12/13 per
neuralSpring) needs investigation.

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
3. ~~Springs declare gates, deploy cells, cut primordial patterns~~ **DONE** (7/7 springs confirmed Wave 50)
4. ~~Cross-subnet routing for southGate~~ **DONE** (Wave 50) — 4ms via router, no TURN needed
5. ~~Bidirectional `mesh.init` across subnets~~ **DONE** (Wave 50) — neuralSpring verified southGate ↔ eastGate
6. Songbird `discovery.peers` population — **BLOCKED** on Songbird v0.2.1 feature gap (mesh.init works, peer list empty)
7. Cross-gate `capability.call` smoke test via primalSpring `s_covalent_mesh` scenario — blocked on step 6
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
| Cross-gate `discovery.peers` verification | **BLOCKED** — Songbird v0.2.1 feature gap: mesh.init works but peer list stays empty |
| Cross-subnet mesh (southGate ↔ eastGate) | **RESOLVED** Wave 50 — 4ms routing, bidirectional mesh.init succeeds |
| Plasmodium collective status | **BLOCKED** — requires `discovery.peers` population for `capability.call` routing |
| flockGate live deployment | **NOT DEPLOYED** |

### Ecosystem Issues (Wave 50, May 25)

| Issue | Reporter | Status |
|-------|----------|--------|
| loamSpine Tokio panic on health probe | wetSpring, neuralSpring | **UPSTREAM** — does not block mesh |
| rhizoCrypt slow startup (>8s) | wetSpring | **FIXED** Wave 49 — `announce_to_biomeos()` off critical path |
| sweetGrass/toadStool slow startup (>8s) | wetSpring | **KNOWN** — cold-start timing, not blocking |
| Songbird `--security-socket` rejected | wetSpring | **FIXED** Wave 49 — feature-guarded + env fallback |
| petalTongue stale socket on restart | primalSpring | **FIXED** Wave 49 — launcher pre-cleans dead sockets |
| `discovery.peers` returns empty | healthSpring | **FIXED** Wave 49 — Songbird `mesh.init` + `bootstrap_peers` wired |
| ~~southGate ≠ eastGate subnet~~ | neuralSpring | **RESOLVED** Wave 50 — cross-subnet routing works natively (4ms) |
| petalTongue musl rejects `--family-id` | primalSpring | **FIXED** Wave 49 — commit `bb5cdc9` |
| Songbird sled DB corruption (unclean) | neuralSpring | **WORKAROUND** — clean `task_lifecycle*` |
| biomeOS LiveSpore deploys to `~/.local/bin` | re-audit | **STALE PATTERN** — conflicts with plasmidBin-only |
| ~~neuralSpring petalTongue `target/release/`~~ | re-audit | **FIXED** Wave 50 — V175/S219, `find_binary` only |
| toadStool/loamSpine local wH unarchived | re-audit | **HYGIENE** — 37+14 flat handoffs need archive subdir |
| Central fossilRecord incomplete | re-audit | **SYNC GAP** — 7/8 primals archived, central repo sparse |
| ~~hotSpring Wave 48~~ | resolved | **RESOLVED** Wave 50 — pseudoSpore v1.5.0, 9 NUCLEUS primals on biomeGate, plasmidBin-only |
| `discovery.peers` empty after `mesh.init` | all gates (Wave 50) | **SONGBIRD v0.2.1 FEATURE GAP** — mesh state initializes but peer list not populated |
| southGate primal instability | wetSpring (Wave 50) | **INVESTIGATING** — 7/13 health-responding (Songbird crashes, BearDog/biomeOS socket issues) |
| Bidirectional seeding required | healthSpring (Wave 50) | **DOCUMENTED** — both sides must `mesh.init`; coordinate seed swap across gates |

### Software Remaining

| Item | Owner | Priority | Status |
|------|-------|----------|--------|
| Songbird `discovery.peers` population | Songbird team | **HIGH** | v0.2.1 feature gap — `mesh.init` works, peer list stays empty. All 4 gates blocked. |
| Cross-gate `capability.call` smoke test | primalSpring | **HIGH** | biomeOS v3.75 mesh dispatch ready, `s_covalent_mesh` scenario written — blocked on `discovery.peers` |
| ~~Cross-subnet routing (southGate ↔ eastGate)~~ | infra/network | ~~MEDIUM~~ | **RESOLVED** Wave 50 — routed natively, 4ms |
| southGate primal stability | plasmidBin / southGate | **MEDIUM** | 7/13 vs 12/13 health-responding — Songbird/BearDog/biomeOS socket issues |
| Cross-gate `nest.sync` live orchestration | biomeOS | MEDIUM | v3.64 `nest.sync` graph shipped. Songbird mesh (v3.75) is the transport. Pending multi-gate connectivity. |
| Sovereign DNS (knot-dns) | cellMembrane | MEDIUM | PLANNED |
| `content.put` publish pipeline (SP-4) | sporePrint + bearDog | LOW | `publish_sporeprint.sh` implemented. E2E requires live NestGate + bearDog session. |
| Forgejo Actions CI | projectNUCLEUS | LOW | PLANNED |
| loamSpine Tokio runtime-in-runtime panic | loamSpine | MEDIUM | Upstream bug — blocks health probe on 2 gates |
| Central fossilRecord sync | all primals | LOW | 7/8 primals reference central paths that don't exist yet |
| ~~neuralSpring composition_nucleus.sh fix~~ | neuralSpring | ~~MEDIUM~~ | **FIXED** Wave 50 — V175/S219 |

**Resolved** (fossilized): Ionic bond runtime (WS-1), biomeOS mesh dispatch,
BearDog ACME renewal daemon, rhizoCrypt startup latency, Songbird `--security-socket`,
stale socket cleanup, 8/8 showcase fossilizations, cross-subnet routing, neuralSpring
petalTongue hardcode, hotSpring Wave 50 absorption, petalTongue `--family-id`,
ludoSpring GAP-01 coralReef — see `fossilRecord/` for detail.

---

## Glacial Shift Criteria

The glacial shift (stadial entry) is reached when:

1. All 4 sovereignty shadows **cut over** (S1-S4 formal 7-day gate passed)
2. Multi-gate LAN mesh **operational** (3+ gates in Plasmodium collective) — Wave 50: 4 gates running, mesh seeded, cross-subnet routing confirmed. **BLOCKED** on Songbird `discovery.peers` population (v0.2.1 feature gap)
3. cellMembrane Nest expansion **deployed** on VPS
4. At least one remote covalent node (flockGate) **validated** over WAN
5. DNS pointed to sovereign infrastructure
6. Cloudflare/cloudflared **removed** from production data path

**Current assessment**: Criteria 1 is 3/4 (S4 shadow remaining). Criteria 2 is
blocked on Songbird `discovery.peers` population (v0.2.1 feature gap) — mesh
infrastructure is deployed and routing works across all 4 gates, but peer list
stays empty after `mesh.init`. The shift moves when Songbird ships peer list
population and S4 auth shadow completes. All springs and primals are ready.

---

## References

- `INTERSTADIAL_EXIT_CRITERIA.md` — 5 pillars + shadow schedule
- `SOVEREIGNTY_STANDARDS.md` — calibrate → shadow → cutover protocol
- `CELLMEMBRANE_FIELDMOUSE_DEPLOYMENT.md` — VPS composition spec
- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — 3 channels + RustDesk
- `DARK_FOREST_GLACIAL_GATE_STANDARD.md` — 5 security invariants
- `DISTRIBUTED_COVALENT_DEPLOYMENT.md` — multi-household compute architecture
- `DESKTOP_NUCLEUS_DEPLOYMENT.md` — single-machine full stack
