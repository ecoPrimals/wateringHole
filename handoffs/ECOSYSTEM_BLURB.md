# ecoPrimals Ecosystem Blurb — Wave 157k Post-Pandemic Evolution

**Date**: Aug 12, 2026 | **Wave**: 157k | **From**: overwatch (eastGate)
**Posture**: **INNER MEMBRANE LIVE.** 11 gates ONLINE (biomeGate DOWN). 0/0/0.

---

## Code Team Ownership — Rationalized (Canonical)

| Gate | Code Teams | Role |
|------|-----------|------|
| eastGate | biomeOS, squirrel, projectNUCLEUS, primalSpring, blueFish + overwatch infra | Orchestration + sovereignty |
| ironGate | bearDog, songBird, skunkBat, swarmVine, bingoCube, petalTongue, esotericWebb, footPrint, tideGlass + 4 parked springs | Primal workhorse, 14TB NFT braid, primary Linux builder |
| strandGate | toadStool, barraCuda, coralReef, hotSpring, rustChip, helixVision, initioChem | Compute trio + batch HPC + science |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, wetSpring, projectFOUNDATION | Provenance trio + data CAS (50.7TB ZFS) |
| sporeGate | cellMembrane, lithoSpore, plasmidBin ops | Topology + depot + cascade + pseudoSpore |
| graftGate | sourDough | Darwin builder (15/15, enmeshed) |
| southGate | neuralSpring | Validation canary |
| blueGate | (builds all 13, no code teams) | Windows builder |
| biomeGate | — | DOWN — SSH recovery pending |

---

## Operational Blockers (5)

| # | Item | Owner |
|---|------|-------|
| 1 | blueGate depot pull — .210:7700 timed out | blueGate |
| 2 | eastGate NUCLEUS restart + hostname fix | eastGate |
| 3 | songBird --node-id flag (reports binary name) | songBird team (ironGate) |
| 4 | ~~southGate LAN IP .149 vs .148~~ **FIXED** — dnsmasq + TOPOLOGY_MAP corrected | ~~sporeGate topology~~ CLOSED |
| 5 | biomeGate SSH recovery | biomeGate (eventual) |

---

## Solo Enablers (unchanged)

- **sporeGate**: NanoWire Tier 2 retirement → autonomous cascade
- **westGate**: CAS federation + native_braid.py → Rust (145/s → 16K/s)
- **strandGate**: arXiv Rung 1 campaign (22/45), pseudoSpore pipeline

---

## Gate Directives

1. Pull latest depot (15/15 current at sporeGate — **DEPOT REBUILT Aug 12**). Redeploy NUCLEUS binaries to match rationalized ownership.
2. Verify gossip — after redeploy, confirm primals are gossiping. 9/16 live. Watch for swarmVine subscription failures or silent drops.
3. Code teams: You now know your home gate. No code moves needed — Forgejo is canonical, all gates clone from there. This is about who owns what for coordination, blurbs, and agent spin-up.

---

## Gossip Watch

As primals redeploy on new home gates, gossip topology may shift. The 6-gate mesh and 9/16 primal injection should hold. Watch for:
- Subscription re-registration after binary restart
- cascade.notify delivery across gate boundaries (VERIFIED: sporeGate → 3 peers)
- Any bidirectional federation drops (southGate was 342/1,216 — baseline)

---

## sporeGate Ops Actions (Wave 157k)

- [x] southGate LAN IP fixed: `.149` → `.148` (dnsmasq, TOPOLOGY_MAP, AAR)
- [x] Depot cascade: 15/18 synced, 13/13 current
- [x] cascade.notify gossip injection verified: Accepted, TTL 8, 3 peers propagating
- [x] Gossip state: tower=4, data=1, compute=0, peers=3, ingested=2,806
- [x] nestgate.io Phase 2 live: /depot/ (4 arch), /provenance/ (BLAKE3 prefix match)
- [x] swarmVine + membrane rebuilt from current HEADs, deployed to depot
- [x] `membrane-cascade.service` fixed: was using stale `/opt/membrane/membrane` → now uses install depot path
- [x] Fleet binary push: eastGate (Jun 4→Aug 12), ironGate (Aug 8→Aug 12), strandGate (Aug 8→Aug 12), golgiBody synced
- [x] Orphan cleanup: eastGate `songbird.depot-jul9` + `primalspring_primal` removed
- [x] Provenance gap fixed: swarmVine + membrane added to `provenance.toml`
- [x] 15/15 binaries consistent across infra depot, install depot, /usr/local/bin (BLAKE3 verified)

---

## westGate Ortho Sweep Response (Wave 157k)

**Status**: ALL CLEAR. 44/44 repos cascaded. biomeOS rebuilt + redeployed. songBird `content.locate` mesh scope wired.

### Cascade

- [x] 44/44 repos pulled from Forgejo — all at HEAD
- [x] Key upstream absorbed: biomeOS spawn leak (`6df4220e`), songBird deep-debt + `content.locate` (`5bc2d3988`), nestGate `content.exists` fix (`4f6dbb045`), swarmVine evolution (5 commits), cellMembrane binary lineage
- [x] biomeOS rebuilt from source (`56286c0a` + Nest Atomic), tests pass, deployed

### Live State

```
nest.health:          healthy=true pipeline=true domains=6/6 alive=14
gossip.status:        peers=5 ingested=1544 tower=10
mesh.peers:           4/4 online (eastGate, ironGate, strandGate, sporeGate)
composition.self_test: ok=true primals=23 v4.57.0
braid.list:           100 braids via riboCipher → sweetGrass
```

### Solo Enabler Progress: CAS Federation

**content.locate mesh scope — WIRED** (`a5dbe79b2` pushed to songBird):
- Iterates reachable mesh peers via BeaconMesh
- Sends `capability.call content.exists` to each peer's HTTP endpoint
- Returns verified locations for peers confirming content
- Peers sorted by path priority (LAN first)
- 48/48 dispatch tests pass

This closes the missing piece for nestgate.io Phase 3 (`/cas/{hash}`) — petalTongue can now call `content.locate` with `scope: "all"` to find content across gates before serving.

### Remaining on westGate Solo Enablers

| Item | Status | Next |
|------|--------|------|
| CAS federation (`content.locate`) | **mesh scope WIRED** | Wire into petalTongue `/cas/{hash}` route |
| `native_braid.py` → Rust | Replacement path documented | Build `membrane content.braid` CLI + `data_braid_ingress.toml` graph |
| sweetGrass announcement persistence | Known gap | biomeOS auto-announce at startup or persist announcements |
| Inter-gate `content.get` E2E test | Ready to attempt | songBird probes + nestGate content.fetch in place |
