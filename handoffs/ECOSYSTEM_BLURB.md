# ecoPrimals Ecosystem Blurb — Wave 150w

**Date**: Jul 23, 2026 10:00 EDT | **Wave**: 150w | **From**: eastGate overwatch
**Posture**: **PHASE 2 — SHADOW DEPLOY ALL LIVE TOPO. EXPLORE + EXCEED.**

---

## P0 — Shadow Deploy (all live gates)

Tower Atomic PHASE 1 PASS (Jul 23). Deploy shadow mode across all live topology.
Tower runs alongside WireGuard — WG carries production, Tower carries mirrored
traffic with continuous metrics. Both stacks active simultaneously.

| Gate | IP | Role | Shadow Action |
|------|----|------|---------------|
| golgiBody | .1 | Hub, TURN relay | Deploy multi-stack routing (RPC + blob + relay profiles) |
| sporeGate | .2 | Build authority | Shadow enable, benchmark driver |
| eastGate | .5 | Code hub | Shadow enable, LAN peer to sporeGate |
| flockGate | .6 | WAN peer | Shadow enable, WAN metrics collection |

**Operator steps per gate**:
1. `membrane tower.shadow --enable` — activates Tower transport on songBird mesh port
2. Verify shadow metrics landing in `benchScale/tower_shadow/`
3. Confirm WG production traffic unaffected

### P0 — Operator Deploy (remaining)

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 1 | Deploy `golgi-post-receive-ci.sh` to golgiBody | operator | `scp` hook to each primal repo's `hooks/post-receive.d/30-sovereign-ci` |
| 2 | Set `MEMBRANE_BUILD_AUTHORITY=1` on sporeGate | operator | systemd unit override or `membrane.env` |

---

## P1 — Exploration (primalSpring teams evolve Tower Atomic)

Tower Atomic is a *specialized* capability-routed mesh. WireGuard is a
general-purpose kernel VPN. The specialization opens 6 domains where Tower
can exceed WireGuard over time.

| # | Domain | Scenario | What to Measure | Springs |
|---|--------|----------|-----------------|---------|
| 1 | **Capability-aware routing** | `s_tower_capability_routing` | Per-capability latency/throughput vs single WG tunnel | all |
| 2 | **Multi-stack routing** | `s_tower_multi_stack` | N songBird instances on golgiBody, per-purpose tuning | songBird |
| 3 | **Large data transfer** | `s_tower_large_data` | 100MB–10GB blobs: throughput, CPU, CAS dedup benefit | wetSpring, hotSpring, neuralSpring |
| 4 | **Secure compute mesh** | `s_tower_secure_compute` | bearDog per-session keys vs WG tunnel crypto | bearDog, all |
| 5 | **Distributed compute** | `s_tower_compute_mesh` | toadStool cross-gate dispatch latency + aggregation | hotSpring, groundSpring |
| 6 | **Edge/SFF profile** | `s_tower_edge_profile` | songBird on NUC Celeron: idle CPU, memory, relay throughput | lithoSpore |

### Why Tower can exceed WG

| WireGuard | Tower Atomic |
|-----------|-------------|
| All packets same tunnel | Routes by capability — knows *what* the traffic is |
| One tunnel per peer | N stacks per relay, each tuned for a traffic class |
| Fixed MTU (1420) | Negotiable framing — jumbo on 10G, chunked on WAN |
| No content awareness | CAS-aware blob routing to nearest cached copy |
| Tunnel-level encryption | Per-capability crypto policy (PostPrimordial = strong) |
| Just a pipe | Compute-aware: workloads route to right substrate |
| Same overhead on Celeron as EPYC | Tunable: minimal relay profile for edge hardware |

### Hardware targets for exploration

| Workload | Path | Hardware |
|----------|------|----------|
| Large bioinformatics data | strandGate (EPYC, 256GB) ↔ eastGate | 10G backbone (when cabled) |
| HBM2 compiler artifacts | biomeGate (Threadripper, Titan V) ↔ gates | 1G / 10G |
| Multi-GPU compute | strandGate (3090+6950XT) ↔ biomeGate (Titan V) | Cross-gate GPU dispatch |
| NPU coordination | eastGate ↔ strandGate ↔ biomeGate (3× Akida) | Neuromorphic mesh |
| Edge relay | NUC Celerons + NucBox M6 | Minimal Tower profile |
| WAN science | flockGate ↔ golgiBody TURN ↔ LAN gates | Multi-hop relay |

---

## P2 — Queued

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 1 | sporePrint primal pipeline | eastGate | Zola replacement: petalTongue + nestGate CAS + cellMembrane |
| 2 | CredentialStore squirrel integration | eastGate | `secrets.*` JSON-RPC, bearDog `FileVault` backend |
| 3 | bingoCube WASM WebGL widget | eastGate | Unblocked by petalTongue 150r |
| 4 | Android Keystore + grapheneGate test | bearDog | CredentialStore TEE/StrongBox backend |
| 5 | Promote 6 pseudoSpores | lithoSpore | Validation Data Stream v1.0 |
| 6 | footPrint declarative source registry | flockGate | DATA_LAYER_PRIMAL_ABSTRACTION spec |

## P3 / Future

| # | Task | Detail |
|---|------|--------|
| 1 | **Phase 3 cutover** | Tower replaces WG for inter-gate traffic (pending Phase 2) |
| 2 | rootPulse design | Sovereign VCS over nestGate CAS + Provenance Trio |
| 3 | pseudoSpore Explorer | esotericWebb interactive visualization |
| 4 | SHOW_HN readiness | Rubric, narrative, demo path |

### Gate Enrollment (operator, when physically accessible)

| # | Gate | Detail |
|---|------|--------|
| 1 | southGate | USB staged, .9 allocated |
| 2 | strandGate | Dual EPYC, 256GB RAM, RTX 3090. Pending physical access |

---

## WHAT'S DONE

| Achievement | Wave |
|-------------|------|
| Tower Atomic PHASE 1 PASS — full WG parity on LAN + WAN | 150w |
| Sovereign depot pipeline (4 phases + deep debt sweep, 1110 tests) | 150w |
| Benchmark harness shipped, TURN relay LIVE, all blockers cleared | 150v |
| Tower primals deep debt, gate AARs GREEN, structural 21/21 | 150v |
| Standards reorg, DNSSEC 3/3, Sovereignty roadmap, cascade 43/43 | 150s-u |
| WASM WebGL, vendor analysis, USB enrollment, workspace reorg | ≤150r |
| Scene unification, NUCLEUS, Silicon Atheism P2, CAC 6/6, Glacial 8/8 | ≤150i |

---

## SOVEREIGNTY

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic | **PHASE 1 PASS — shadow deploying, exploring exceeding** |
| **REPLACE** | Zola | petalTongue + nestGate CAS | Design pending |
| **LATE-STAGE** | Forgejo | rootPulse | Post-rootPulse |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk / JupyterHub | Outer membrane | Stays |

---

## TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, TURN relay, multi-stack target
  ├─ sporeGate (10.13.37.2) — build authority, Tower 3/3, shadow driver
  ├─ eastGate  (10.13.37.5) — orchestrator, code hub, Akida NPU
  ├─ flockGate (10.13.37.6) — WAN peer, esotericWebb V22
  ├─ ironGate  (10.13.37.7) — compute, GPU [DOWN]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Pending: southGate (.9), strandGate (EPYC, 256GB, 3090)
10G backbone: 4 towers NIC'd, cabling pending (sole blocker for ≥1Gbps bench)
```

---

*Wave 150w: TOWER ATOMIC PHASE 1 PASS. Shadow deploying across all live topo.
primalSpring teams exploring 6 domains where Tower Atomic exceeds WireGuard:
capability routing, multi-stack relay, large data, secure compute, distributed
compute mesh, edge profiles. First tractable solution achieved — now evolve.
43/43 converged.*
