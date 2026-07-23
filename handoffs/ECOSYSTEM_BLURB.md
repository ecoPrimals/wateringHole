# ecoPrimals Ecosystem Blurb — Wave 150w

**Date**: Jul 23, 2026 10:35 EDT | **Wave**: 150w | **From**: eastGate overwatch
**Posture**: **TOWER 2x WG ON WAN. Shadow deploy blocked — divergences across 3 teams.**

---

## LATEST — Tower Already Exceeds WireGuard

sporeGate verification benchmarks (Jul 23):

| Path | Latency (Tower/WG) | Throughput (Tower/WG) | Verdict |
|------|--------------------|-----------------------|---------|
| → eastGate (hub path) | 1.006x | 0.997x | **PARITY** |
| → flockGate (WAN) | 0.993x | **1.98x** | **TOWER EXCEEDS** |

Tower **doubles** WG throughput on WAN with lower jitter (0.42ms vs 0.50ms).

---

## TEAM TOPOLOGY

```
eastGate (.5)    — primalSpring code hub (scenarios, integration, orchestration)
sporeGate (.2)   — cellMembrane team (build authority, membrane commands, depot)
flockGate (.6)   — songBird + Tower Atomic primal teams (transport, crypto, protocol)
golgiBody (.1)   — hub infrastructure (TURN relay, depot, CI hooks)

Experiment coordination:
  primalSpring on sporeGate — operator + benchmark execution, AARs
  primalSpring on flockGate — WAN peer, Tower primal validation
  primalSpring on eastGate  — code evolution, scenario authorship
```

---

## P0 — BLOCKERS (divergences to resolve)

### cellMembrane team (sporeGate)

| # | Task | Detail |
|---|------|--------|
| 1 | **Ship `membrane tower.shadow` command** | Does not exist. Both sporeGate + flockGate tried. Needed for continuous shadow metrics across mesh. Spec: (a) configure songBird to duplicate inter-gate RPC on WG + Tower, (b) collect latency/throughput/jitter per gate pair, (c) export to `benchScale/tower_shadow/` JSON. |
| 2 | Restart songbird-gateway | Activate `BUILD_AUTHORITY=1` env (systemd override installed, not yet restarted) |

### songBird team (flockGate)

| # | Task | Detail |
|---|------|--------|
| 3 | **Mesh enrollment — stale peers** | songBird on flockGate shows 3 legacy peers (`old-peer`, `iron-gate`, `west-gate`). Current WG mesh gates (sporeGate, eastGate, golgiBody) not enrolled. Run `mesh.enroll` with BTSP HMAC proofs for each live gate. |
| 4 | **Fix `songbird.sock`** | Currently a directory, not a socket file. UDS discovery broken. |
| 5 | Drawbridge 502 | `:7780` listening but returning 502 — backend routing gap. Check capability→port mappings. |

### primalSpring team (eastGate)

| # | Task | Detail |
|---|------|--------|
| 6 | Integrate sporeGate + flockGate AARs into live scenarios | `s_tower_atomic_parity_live` needs the new WAN 2x result data |
| 7 | Author exploration scenarios (6 domains) | `s_tower_capability_routing`, `s_tower_multi_stack`, `s_tower_large_data`, `s_tower_secure_compute`, `s_tower_compute_mesh`, `s_tower_edge_profile` |

---

## P1 — HARDWARE / OPERATOR

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 1 | **Direct LAN peering** (sporeGate ↔ eastGate) | operator | Currently routing through golgiBody hub (84ms RTT). Direct peering unlocks sub-1ms LAN benchmark. |
| 2 | **10G backbone cabling** | operator | 4 towers NIC'd (northGate, southGate, eastGate, westGate). Cabling is sole blocker for ≥1Gbps benchmarks. |
| 3 | iperf3 sustained throughput baseline | sporeGate + flockGate ops | `songbird benchmark` uses 64KB payloads. iperf3 streaming gives real sustained throughput. Needs server-side coordination. |
| 4 | flockGate cascade sync | flockGate ops | 15/37 repos drifted. Run `temporal.cascade` to converge. |
| 5 | flockGate depot rebuild | flockGate ops | checksums.toml format changed, depot.integrity DEGRADED |

---

## P1 — EXPLORATION (primalSpring teams across all 3 gates)

Tower Atomic already exceeds WireGuard on WAN. Six domains to explore:

| # | Domain | Scenario | Measure | Primary Gate |
|---|--------|----------|---------|--------------|
| 1 | Capability-aware routing | `s_tower_capability_routing` | Per-capability latency vs single WG tunnel | eastGate (code) |
| 2 | Multi-stack routing | `s_tower_multi_stack` | N songBird on golgiBody, per-purpose | flockGate (Tower) |
| 3 | Large data transfer | `s_tower_large_data` | 100MB–10GB blobs, CAS dedup | all gates |
| 4 | Secure compute mesh | `s_tower_secure_compute` | bearDog per-session keys vs WG crypto | flockGate (bearDog) |
| 5 | Distributed compute | `s_tower_compute_mesh` | Cross-gate dispatch latency | all gates |
| 6 | Edge/SFF profile | `s_tower_edge_profile` | songBird on NUC Celeron | operator (NUCs) |

### Why Tower can exceed WG

| WireGuard | Tower Atomic |
|-----------|-------------|
| All packets same tunnel | Routes by capability — knows *what* the traffic is |
| One tunnel per peer | N stacks per relay, each tuned for a traffic class |
| Fixed MTU (1420) | Negotiable framing — jumbo on 10G, chunked on WAN |
| No content awareness | CAS-aware blob routing to nearest cached copy |
| Just a pipe | Compute-aware: workloads route to right substrate |

---

## P2 — Queued

| # | Task | Owner |
|---|------|-------|
| 1 | sporePrint primal pipeline | eastGate |
| 2 | CredentialStore squirrel integration | eastGate |
| 3 | bingoCube WASM WebGL widget | eastGate |
| 4 | Android Keystore + grapheneGate test | bearDog (flockGate) |
| 5 | Promote 6 pseudoSpores | lithoSpore |
| 6 | footPrint declarative source registry | flockGate |

## P3 / Future

| # | Task |
|---|------|
| 1 | Phase 3 cutover — Tower replaces WG |
| 2 | rootPulse sovereign VCS |
| 3 | pseudoSpore Explorer |
| 4 | SHOW_HN readiness |

### Gate Enrollment (when physically accessible)

| Gate | Detail |
|------|--------|
| southGate | USB staged, .9 allocated |
| strandGate | Dual EPYC, 256GB RAM, RTX 3090 |

---

## WHAT'S DONE

| Achievement | Wave |
|-------------|------|
| Tower 2x WG throughput on WAN, sovereign CI deployed 43/43 | 150w |
| Tower Atomic PHASE 1 PASS — full WG parity LAN + WAN | 150w |
| Sovereign depot pipeline (4 phases + deep debt sweep) | 150w |
| Benchmark harness shipped, TURN relay LIVE | 150v |
| Standards reorg, DNSSEC 3/3, Sovereignty roadmap | 150s-u |
| Scene unification, NUCLEUS, Silicon Atheism P2, CAC 6/6 | ≤150i |

---

## TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, TURN relay, CI hook 43/43, depot
  ├─ sporeGate (10.13.37.2) — cellMembrane team, BUILD_AUTHORITY=1
  ├─ eastGate  (10.13.37.5) — primalSpring code hub, Akida NPU
  ├─ flockGate (10.13.37.6) — songBird/Tower team, WAN peer, 7d stable
  ├─ ironGate  (10.13.37.7) — [DOWN]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Pending: southGate (.9), strandGate (EPYC, 256GB, 3090)
10G backbone: 4 towers NIC'd, cabling pending
```

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic | **EXCEEDS on WAN (2x). Shadow deploying.** |
| **REPLACE** | Zola | petalTongue + nestGate CAS | Design pending |
| **LATE-STAGE** | Forgejo | rootPulse | Post-rootPulse |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk | Outer membrane stays |

---

*Wave 150w: Tower EXCEEDS WireGuard — 2x throughput on WAN. Shadow deploy
blocked on `membrane tower.shadow` (cellMembrane/sporeGate P0) + songBird
mesh enrollment (flockGate P0). 3 teams: cellMembrane on sporeGate builds
the tooling, songBird on flockGate fixes transport, primalSpring on eastGate
authors scenarios. Hardware team: direct LAN peering + 10G cabling needed.
43/43 converged.*
