# Glacial Shift Readiness

**Status**: Active tracking document  
**Phase**: Interstadial exit → Stadial entry  
**Last updated**: 2026-05-31 (Wave 64: Sovereignty sprint started — S1 TLS 7-day gate running, DNS NS infrastructure ready (ns1+ns2 live), VPS Nest confirmed operational, Wave 64 handoffs distributed to ironGate/flockGate/biomeGate)

---

## Position

The ecosystem has cleared the interstadial exit gate (~9.5/10). 13/13 primals
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

**Wave 54 milestone**: Provenance-elevated checksums shipped — `provenance.toml` (Layer 2
composite fingerprint), sweetGrass `braid.create` post-harvest, `plasmidbin verify-provenance`
subcommand. primalSpring consumer tooling rewired. Full temporal/glacial/ecological review
completed (`TEMPORAL_ECOLOGICAL_REVIEW_MAY27_2026.md`). VPS NUCLEUS critical path mapped:
zero mountain debt blocking, `deploy_membrane.sh --composition nest` ready, NestGate v0.5.0
unified. cellMembrane deployment sprint is the sole remaining gate.

**Provenance pipeline live**: 3 primals (loamSpine, toadStool, Songbird) harvested with
full `provenance.toml` fingerprints (May 27). `rustc_version = "1.95.0"`, source commits
verified. Provenance-elevated checksums confirmed operational in CI.

**Wave 61 sovereign shadow functions** (May 29): `membrane-shadow` Rust crate replaces
bash VPS control scripts. Typed APIs for Forgejo repo/mirror management (`content.repo.*`,
`content.mirror.*`), token lifecycle (`auth.token.*`), systemd service control
(`gate.service.*`), and gate management (`gate.info`, `gate.pull`, `gate.check`).
Capability registries aligned across nestGate, bearDog, and biomeOS. Forgejo pull mirrors
operational for all 38 repos. Temporal sync spec published. Ecosystem standardization
audit: stale remotes cleaned, duplicate repos removed, branch naming normalized. 13/14
upstream Neural API methods shipped by primal teams.

**Wave 62 temporal sync operational** (May 30): waterFall temporal sync implemented in
Rust (`temporal.rs` — typed multi-remote DAG sync, `manifest.rs` — ecosystem manifest
reader replacing Python tomllib, `identity.rs` — capability-based gate detection).
5 Forgejo mirrors converted to bidirectional repos (biomeOS, coralReef, sweetGrass,
squirrel, wateringHole). `cascade-pull.sh --source temporal` now delegates to the Rust
`membrane` binary with bash fallback. Deep debt sprint: shell injection fix in
`token_create`/`token_revoke`, hardcoded paths→`ShadowConfig`, `unreachable!()`→`Result`,
magic numbers→named constants. Manifest bumped to v2.1.0 (Wave 62). 10 handoffs archived.

**Wave 63 K-Derm diderm deployment** (May 30): Three-node VPS envelope physically
deployed. golgiBody (inner membrane, 157.230.3.183): Forgejo + NUCLEUS, workspace cleaned
80%→66%. peptidoglycan (structural, 157.230.209.218): 2-vCPU/4GB/80GB, Rust 1.96, Zola 0.22.1,
39-repo workspace, membrane binary, temporal sync hub. golgiBody-ext (outer membrane,
137.184.197.151): Caddy 2.11.3, sporePrint live (HTTP 200, 143 pages). Cross-node SSH mesh.
ecosystem_manifest.toml v2.2.0 with `[topology]` section and three new gate profiles.
`GATE_SETUP_STANDARD.md` published — standardizes physical gate and VPS proto-fieldMouse
setup, sync, resync. `gen5/KDERM_DIDERM_APPLICATION.md` documents bonding interactions
per boundary. Cost: $48/mo for complete sovereign diderm envelope.

**Wave 63+ waterFall Phase 4 inversion + K-Derm bonding enforcement** (May 31):
Forgejo-primary push model deployed with proper K-Derm diderm relay chain.
`push_target = "forgejo"` in manifest — gates push to Forgejo only. Diderm relay
chain wired: `pepti-sync-relay.sh` on peptidoglycan mediates metallic→ionic bond;
`ext-github-push.sh` on golgiBody-ext (trans face) ships to GitHub (weak bond).
GitHub SSH write credentials moved exclusively to golgiBody-ext (outer membrane).
`topology.roles` added to manifest declaring per-layer function assignments.
Push mirror API in membrane-shadow (`mirror.push-create/list/sync`), `temporal.sync`
respects `push_target`. Post-receive impulse relay + cascade graphs created.
`EXTERNAL_LEDGER_STANDARD.md` published. Bond-type violation resolved:
proper covalent→metallic→ionic→weak degradation through the diderm envelope.

**Transport evolution roadmap published** (May 31): `gen5/TRANSPORT_EVOLUTION_NANOWIRE_TO_QUORUM.md`
documents the path from SSH-triggered relay (nanowire) to timer-based autonomous sensing
(quorum Phase 1) to songbird mesh relay (Phase 2) to capability-routed quorum (Phase 3).
Current relay chain validated by flockGate (WAN, ~3s propagation) and ironGate (LAN covalent
backbone). biomeGate (async hardware cadence) serves as air-gap validation loop.

**Mountain blurb responses absorbed** (May 27):
- toadStool S279: zero production panic paths, 9,156+ lib tests, handoffs archived
- Songbird W53b: +74 tests (8,070 total), deep debt zero confirmed, `forbid(unsafe_code)` all crates
- biomeOS v3.76: LiveSpore `~/.local/bin` already fixed (eddc3fd2)
- loamSpine W55: BearDog coupling removed, placeholder DIDs replaced, self-knowledge enforced

**Glacial Shift Wave Plan published**: 3-phase roadmap (Waves 53–55+) at
`GLACIAL_SHIFT_WAVE_PLAN.md`. Team handoffs distributed to `handoffs/`:
- Wave 53: Primal mountains — **RESOLVED** (12/13, SouthGate ops carries to W54)
- Wave 54: Deployment + cellMembrane (gate redeploy, VPS Nest, sovereign DNS, K-Derm wire) + **provenance elevation**
- Wave 55+: Springs launch + cross-gate NUCLEUS (proto-nucleate deployment, capability routing)

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
  cleared 15k LOC of dead discovery code. Vault (encrypted creds at rest) deferred
  to Phase 2 (not blocking — in-memory `secrets.*` IPC operational with lazy
  NUCLEUS purpose-key derivation). S4 auth shadow is a cellMembrane observation
  criterion; bearDog auth infra is **complete** (14,940+ tests, zero debt).
- **toadStool**: **S279 deep debt III complete** — zero production panic paths (12 eliminated),
  deprecated legacy capability roundtrip, 9,156+ lib tests. Handoffs archived (S278b).
  **CLEAR** — zero sentinel-blocking items.
- **biomeOS**: **v3.76 — LiveSpore `~/.local/bin` FIXED** (commit eddc3fd2, Wave 49).
  Zero stale patterns. Neural API mesh dispatch ready for cross-gate `capability.call`.
  1 tracked TODO (REST route — enhancement). **CLEAR** — zero sentinel-blocking items.
- **petalTongue**: WASM client-side rendering live. `--family-id` now accepted
  (Wave 49, commit `bb5cdc9`). Showcase pointer updated to central fossilRecord.
  **CLEAR** — no remaining sentinel-blocking items.

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
| **S1** | TLS termination | Caddy+LE :443 (80ms TTFB) | Cloudflare (INACTIVE) | **7-DAY GATE RUNNING** (started 2026-05-31, q15min probe) | p95 < 500ms, 0 TLS failures |
| **S2** | NAT relay | Songbird TURN :3478 | cloudflared (INACTIVE) | **LIVE** (100% 3+ days) | 7-day 100% reachable |
| **S3** | Content serving | NestGate + petalTongue (67ms TTFB) | GitHub Pages (111ms) | **LIVE** | 7-day TTFB parity |
| **S4** | Auth | BearDog BTSP dual-auth | OAuth2/PAM proxy | **SHADOW LIVE on ironGate** (since ~May 14) | 7-day p95 < 50ms |

**Remaining**: S1 gate completes ~June 7. S4 formal 7-day gate blocked on ironGate services restart. DNS NS cutover infra ready (ns1+ns2 live, DNSSEC active), registrar action pending.

### cellMembrane (inner membrane)

| Component | Status |
|-----------|--------|
| VPS (157.230.3.183, DO nyc1) | **OPERATIONAL** |
| Channel 2: Songbird TURN relay | **LIVE** |
| Channel 2b: RustDesk hbbs/hbbr | **LIVE** |
| Channel 3: TLS surface (Caddy + ACME) | **LIVE** |
| Tower composition (BearDog + Songbird + SkunkBat) | **DEPLOYED** |
| Nest expansion (rhizoCrypt + loamSpine + sweetGrass) | **OPERATIONAL** (since May 28) — all 4 services active, ports verified |
| Sovereign shadow functions (membrane-shadow) | **OPERATIONAL** (Wave 62) — Rust crate + temporal/manifest/identity modules |
| Forgejo repos (5 bidirectional + 33 mirrors) | **OPERATIONAL** (Wave 62) — biomeOS/coralReef/sweetGrass/squirrel/wateringHole push-enabled |
| waterFall temporal sync | **OPERATIONAL** (Wave 62) — Rust `temporal.rs`, `cascade-pull.sh --source temporal` |
| Channel 1: Sovereign DNS (knot-dns) | **OPERATIONAL** — ns1 (golgiBody) + ns2 (golgiBody-ext), DNSSEC active, zone transfer confirmed. NS registrar cutover pending. |
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
| **flockGate** | i9-13900K, RTX 3070 Ti, 64GB | Remote covalent (WAN) | **OPERATIONAL** (Wave 63) — WAN relay validated (~3s propagation) | sporePrint | WAN via cellMembrane |
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
| Songbird sled DB corruption (unclean) | neuralSpring | **RESOLVED** Wave 51b — auto-cleanup of orphaned sled DB artifacts on startup (sled removed in Wave 135, artifacts persisted). |
| ~~biomeOS LiveSpore deploys to `~/.local/bin`~~ | re-audit | **RESOLVED** — v3.76 commit eddc3fd2, target → `plasmidBin/primals/` |
| ~~toadStool local wH unarchived~~ | re-audit | **RESOLVED** — S278b: handoffs archived, debris cleaned |
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
