# Glacial Shift Readiness

**Status**: Active tracking document  
**Phase**: PostPrimordial → Glacial Shift  
**Last updated**: 2026-05-26 (Wave 52b — Full NUCLEUS live, cephalization + Tower CNS experiments, glacial shift readiness confirmed)

---

## Position

The ecosystem has cleared the interstadial exit gate (~9.8/10). 13/13 primals
at zero debt. cellMembrane VPS operational (relay + TLS/content shadows).
Shadow tracks S1-S3 proven. 4-gate NUCLEUS operational (eastGate, ironGate,
southGate, biomeGate) with Songbird TCP :7700 federation. **7/7 delta springs
confirmed covalent HPC** (Wave 50). **`discovery.peers` SHIPPED** (Wave 51) —
Songbird mesh+registry merge, `SONGBIRD_PEERS` auto-seeds on boot. Live
gate validation is NEXT.

**Wave 52b milestone**: Full NUCLEUS live on eastGate — 13/13 primals from plasmidBin,
19/19 sockets alive, `plasmidbin doctor` 35/35 pass. primalSpring v0.9.30: 92 experiments
(21 tracks), certify 175/193, zero debt. Track 21 experiments: postPrimordial review (40/40),
cephalization plan (26/26), Tower CNS convergence (40/40). K-Derm topology + bonding model
standards published. sourDough v0.3.0 harvested. Deploy graph validation fragment-aware.
Provenance checksums regenerated (24 files, BLAKE3).

**Wave 51 milestone**: Songbird `discovery.peers` resolution + outer membrane hardening.

- **plasmidBin full Rust elevation** — all 20 bash scripts replaced by a single
  `plasmidbin` Rust CLI binary (`validate`, `harvest`, `fetch`, `doctor`,
  `deploy`, `start`, `stop`, `launch`). Dynamic harvest driven from `sources.toml`
  with `binary_name` and `build_args` fields — single-point primal onboarding.
  Checksum sync pipeline fixed (split `git add` for gitignored dirs). Release
  smoke test bash substitution bug fixed. biomeos (`biomeos-cli`) and skunkbat
  (`-p skunk-bat-server`) binary naming resolved. Release tags: v2026.05.25,
  v2026.05.26.
- **CI cost optimization** — daily full-sweep cron removed. New `check-updates.yml`
  does daily lightweight tag check (~1 min) and selectively dispatches harvest
  only for stale primals. Weekly Monday full sweep retained. Spending cap set
  at $100/month.
- **GitHub Actions outage (May 26)** — critical incident (authentication cascade,
  workflow triggers silently dropped). CI/CD pipeline went dark. All inner membrane
  components unaffected: 4 NUCLEUS instances running, Songbird mesh live, local
  `plasmidbin` CLI operational. Outage documented in
  `whitePaper/gen4/architecture/THE_GOLDEN_CAGE.md`.
- **cellMembrane self-hosted runners handoff** — issued during outage. Requires
  2+ LAN gates with lockout prevention. Forgejo-as-primary evolution path
  documented. See `handoffs/CELLMEMBRANE_SELF_HOSTED_RUNNERS_WAVE50_MAY26_2026.md`.
- **primalSpring wateringHole fossilized** — 42 files (7 standards, 2 living
  handoffs, 32 archived) moved to `fossilRecord/springs/primalSpring/wateringHole_wave50_may2026/`.
  Local `wateringHole/` replaced with pointer stub to `infra/wateringHole/`.
- **THE_GOLDEN_CAGE.md** — gen4 architecture paper written. Documents dependency
  audit (7 infrastructure cage bars + science stack cage), chrysalis thesis
  (bootstrap sequence from cage to sovereignty), evolution order (8 steps from
  self-hosted runners to barracuda science parity). Forgejo positioned as
  sovereignty baseline before NUCLEUS absorbs forge capabilities.

**Wave 47 milestone**: 13/13 behavioral convergence — all primals accept
`--socket`, return `{"status":"alive"}` from `health.liveness`, handle
SIGTERM+SIGINT, and implement `lifecycle.status`.

**Wave 48 milestone**: Covalent spring mesh — **all 8/8 springs sounded off**.
4 gates operational with NUCLEUS + Songbird TCP :7700 federation.

**Wave 49 milestone**: Post-primordial + ecosystem tightening. plasmidBin-only
deployment enforced across all launchers. 8/8 primal showcases fossilized.
7 primals responded with tightening handoffs same-day. Songbird wired
`mesh.init` with `bootstrap_peers`. **All sentinel debt cleared.** Full
NUCLEUS 12/12 redeployed from plasmidBin musl binaries.

**Wave 50 milestone**: Covalent HPC — **all 7/7 delta springs responded**.
Cross-subnet routing confirmed (southGate ↔ eastGate, 4ms, no TURN needed).
neuralSpring fixed last `target/release/` hardcode. hotSpring absorbed
post-primordial (pseudoSpore v1.5.0). ludoSpring resolved GAP-01 coralReef.
healthSpring validated dual-tower + Nest Atomic. plasmidBin CLI alignment
fixed upstream.

| Gate | NUCLEUS | Springs | Mesh seeded |
|------|---------|---------|-------------|
| eastGate | 13/13 | airSpring, groundSpring, primalSpring | ironGate |
| ironGate | 12/12 | healthSpring, ludoSpring | eastGate |
| southGate | 12/13 | neuralSpring, wetSpring | eastGate (bidirectional verified) |
| biomeGate | 9 primals | hotSpring | Registry seeded |

**~~Remaining blocker~~ RESOLVED (Wave 51)**: `discovery.peers` was returning
empty because orchestrator routed to registry-only. Songbird Wave 51 shipped
mesh+registry merge in `DiscoveryHandler`, `SONGBIRD_PEERS` auto-seeding via
`mesh_seed` module, and port-preserving `EndpointType::socket_addr()`. This is
code-complete; **live gate validation is NEXT** (deploy fresh Songbird from
plasmidBin on eastGate + ironGate, set `SONGBIRD_PEERS`, run `s_covalent_mesh`).

**Climate-sensitive sentinels** (primals whose readiness gates the glacial shift):

- **Songbird**: **`discovery.peers` VALIDATED LIVE (Wave 51)** — mesh+registry merge,
  `SONGBIRD_PEERS` env auto-seeds at boot, dual-format parser, remote_dispatch
  refactor with port-preserving addressing. 7+ new tests. Sled DB corruption
  **RESOLVED** (Wave 51b — auto-cleanup of orphaned artifacts on startup).
  **NEXT**: `s_covalent_mesh` + `s_cross_gate_capability_call` scenario validation.
- **bearDog**: ACME renewal daemon operational. Massive orphan purge (Wave 113b)
  cleared 15k LOC of dead discovery code. Vault (encrypted creds at rest) deferred
  to Phase 2 (not blocking — in-memory `secrets.*` IPC operational with lazy
  NUCLEUS purpose-key derivation). S4 auth shadow is a cellMembrane observation
  criterion; bearDog auth infra is **complete** (14,940+ tests, zero debt).
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
on biomeGate, plasmidBin-only). **Songbird `discovery.peers` shipped Wave 51** —
cross-gate `capability.call` is now code-complete. Live gate validation is NEXT.
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
6. ~~Songbird `discovery.peers` population~~ **DONE** (Wave 51) — mesh+registry merge, `SONGBIRD_PEERS` auto-seed, `mesh_seed` module
7. Cross-gate `capability.call` smoke test via primalSpring `s_covalent_mesh` scenario — **NEXT** (code ready, deploy fresh Songbird from plasmidBin)
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
| Cross-gate `discovery.peers` verification | **SHIPPED** (Wave 51) — orchestrator dispatch fixed + `SONGBIRD_PEERS` auto-seeds on startup. Live test NEXT. |
| Cross-subnet mesh (southGate ↔ eastGate) | **RESOLVED** Wave 50 — 4ms routing, bidirectional mesh.init succeeds |
| Plasmodium collective status | **UNBLOCKED** — `discovery.peers` now populates; needs live test with 3+ gates |
| flockGate live deployment | **NOT DEPLOYED** |

### Ecosystem Issues (Wave 51, May 26)

| Issue | Reporter | Status |
|-------|----------|--------|
| `discovery.peers` empty after `mesh.init` | all gates (Wave 50) | **VALIDATED** Wave 51 — orchestrator dispatch wired to mesh+registry merger; `SONGBIRD_PEERS` auto-seeds on startup. Live-verified on eastGate (primalspring01 :7701 ↔ nucleus01 :7700). |
| southGate primal instability | wetSpring (Wave 50) | **INVESTIGATING** — 7/13 health-responding (Songbird crashes, BearDog/biomeOS socket issues) |
| Bidirectional seeding required | healthSpring (Wave 50) | **DOCUMENTED** — both sides must `mesh.init`; coordinate seed swap across gates |
| loamSpine Tokio panic on health probe | wetSpring, neuralSpring | **INVESTIGATED** Wave 51b — loamSpine audited all 192 .rs files: zero Runtime::new/block_on in production. benchScale Phase 20 added (40 rapid-fire probes, all pass). Upstream suspects caller wraps in block_on. |
| sweetGrass/toadStool slow startup (>8s) | wetSpring | **KNOWN** — cold-start timing, not blocking |
| Songbird sled DB corruption (unclean) | neuralSpring | **RESOLVED** Wave 51b — auto-cleanup of orphaned sled DB artifacts on startup (sled removed in Wave 135, artifacts persisted). |
| biomeOS LiveSpore deploys to `~/.local/bin` | re-audit | **STALE PATTERN** — conflicts with plasmidBin-only |
| toadStool/loamSpine local wH unarchived | re-audit | **HYGIENE** — 37+14 flat handoffs need archive subdir |
| Central fossilRecord incomplete | re-audit | **NARROWED** — primalSpring wH archived Wave 51; remaining primals' local docs still sparse |
| GitHub Actions outer membrane dependency | primalSpring (Wave 51) | **HANDOFF ISSUED** — cellMembrane self-hosted runners; Forgejo-primary evolution path |
| plasmidBin metadata version drift | re-audit (Wave 51) | **HYGIENE** — manifest.toml (v5.5.0), checksums.toml (Wave 35), sources.toml (Apr 14) lag README (v5.6.0) |

**Resolved** (fossilized): Ionic bond runtime (WS-1), biomeOS mesh dispatch,
BearDog ACME renewal daemon, rhizoCrypt startup latency, Songbird `--security-socket`,
stale socket cleanup, 8/8 showcase fossilizations, cross-subnet routing, neuralSpring
petalTongue hardcode, hotSpring Wave 50 absorption, petalTongue `--family-id`,
ludoSpring GAP-01 coralReef, `discovery.peers` RPC wiring (Wave 49 — `mesh.init` +
`bootstrap_peers` functional; **RESOLVED Wave 51** — mesh+registry merge shipped), primalSpring wateringHole fossilized (Wave 51, 42 files to
fossilRecord) — see `fossilRecord/` for detail.

### Software Remaining

| Item | Owner | Priority | Status |
|------|-------|----------|--------|
| ~~Songbird `discovery.peers` population~~ | Songbird team | **DONE** | **SHIPPED Wave 51** — mesh+registry merge, `SONGBIRD_PEERS` auto-seed, 7+ tests |
| Cross-gate `capability.call` smoke test | primalSpring | **HIGH** | `s_covalent_mesh` scenario ready — deploy fresh Songbird from plasmidBin + set `SONGBIRD_PEERS` |
| Self-hosted CI runners (2+ LAN gates) | cellMembrane | **HIGH** | Handoff issued Wave 51. Eliminates GitHub Actions as outer membrane dependency. |
| southGate primal stability | plasmidBin / southGate | **MEDIUM** | 7/13 vs 12/13 health-responding — Songbird/BearDog/biomeOS socket issues |
| Cross-gate `nest.sync` live orchestration | biomeOS | MEDIUM | v3.64 `nest.sync` graph shipped. Songbird mesh (v3.75) is the transport. Pending multi-gate connectivity. |
| Sovereign DNS (knot-dns) | cellMembrane | MEDIUM | PLANNED |
| Forgejo as primary code host | projectNUCLEUS | MEDIUM | Mirrors operational. Forgejo is sovereignty baseline before NUCLEUS absorbs forge capabilities. |
| plasmidBin metadata sync | plasmidBin | LOW | manifest.toml/checksums.toml/sources.toml headers lag README — version and date drift |
| `content.put` publish pipeline (SP-4) | sporePrint + bearDog | LOW | `publish_sporeprint.sh` implemented. E2E requires live NestGate + bearDog session. |
| ~~loamSpine Tokio runtime-in-runtime panic~~ | loamSpine | **INVESTIGATED** | Wave 51b: loamSpine audit confirms zero runtime nesting in production. benchScale 54-phase validation passes. Suspects caller-side wrapping — wetSpring/neuralSpring to verify launcher. |
| Central fossilRecord sync | all primals | LOW | primalSpring wH archived; remaining primals' local docs still sparse |

---

## Glacial Shift Criteria

The glacial shift (stadial entry) is reached when:

1. All 4 sovereignty shadows **cut over** (S1-S4 formal 7-day gate passed)
2. Multi-gate LAN mesh **operational** (3+ gates in Plasmodium collective) — Wave 50: 4 gates running, mesh seeded, cross-subnet routing confirmed. **UNBLOCKED** Wave 51: `discovery.peers` shipped. Deploy fresh from plasmidBin + live validation NEXT.
3. cellMembrane Nest expansion **deployed** on VPS
4. At least one remote covalent node (flockGate) **validated** over WAN
5. DNS pointed to sovereign infrastructure
6. Cloudflare/cloudflared **removed** from production data path
7. CI/CD runs on **inner membrane** (self-hosted runners or Forgejo CI) — Wave 51: handoff issued, not yet deployed

**Current assessment**: Criteria 1 is 3/4 (S4 shadow remaining). Criteria 2 is
**unblocked** — Songbird shipped `discovery.peers` (Wave 51); needs live gate
fresh plasmidBin deploy and `s_covalent_mesh` validation to confirm operational. Criteria 7 added Wave 51 after GitHub Actions
outage exposed CI as an unmitigated outer membrane dependency. plasmidBin Rust
elevation (Wave 51) means the build toolchain itself is sovereign — only the
runners are not. The shift moves when Songbird ships peer list population, S4
auth shadow completes, and CI runs on inner membrane. All springs and primals
are ready.

---

## References

- `INTERSTADIAL_EXIT_CRITERIA.md` — 5 pillars + shadow schedule
- `SOVEREIGNTY_STANDARDS.md` — calibrate → shadow → cutover protocol
- `CELLMEMBRANE_FIELDMOUSE_DEPLOYMENT.md` — VPS composition spec
- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — 3 channels + RustDesk
- `DARK_FOREST_GLACIAL_GATE_STANDARD.md` — 5 security invariants
- `DISTRIBUTED_COVALENT_DEPLOYMENT.md` — multi-household compute architecture
- `DESKTOP_NUCLEUS_DEPLOYMENT.md` — single-machine full stack
- `whitePaper/gen4/architecture/THE_GOLDEN_CAGE.md` — dependency audit + chrysalis thesis
- `handoffs/CELLMEMBRANE_SELF_HOSTED_RUNNERS_WAVE50_MAY26_2026.md` — inner membrane CI
