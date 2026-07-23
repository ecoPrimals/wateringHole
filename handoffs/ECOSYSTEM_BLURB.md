# ecoPrimals Ecosystem Blurb — Wave 150w

**Date**: Jul 23, 2026 10:30 EDT | **Wave**: 150w | **From**: eastGate overwatch
**Posture**: **TOWER 2x WG ON WAN. Shadow deploy blocked on `membrane tower.shadow`.**

---

## LATEST — Gate AARs (Jul 23)

**sporeGate** ran verification benchmarks. **Tower already exceeds WireGuard**:

| Path | Latency (Tower/WG) | Throughput (Tower/WG) | Verdict |
|------|--------------------|-----------------------|---------|
| → eastGate (hub path) | 1.006x | 0.997x | **PARITY** |
| → flockGate (WAN) | 0.993x | **1.98x** | **TOWER EXCEEDS** |

Tower **doubles** WG throughput on WAN with lower jitter (0.42ms vs 0.50ms).

**Operator actions DONE**:
- `MEMBRANE_BUILD_AUTHORITY=1` set on sporeGate (pending restart)
- `golgi-post-receive-ci.sh` deployed to all 43 repos on golgiBody
- 4 benchmark JSON results filed in `benchScale/tower_shadow/`

---

## P0 — BLOCKERS (eastGate code tasks)

Both sporeGate and flockGate report the same blocker:

| # | Blocker | Owner | Detail |
|---|---------|-------|--------|
| 1 | **`membrane tower.shadow` command** | eastGate / cellMembrane | Does not exist. Both gates tried. Needed to enable continuous shadow metrics across mesh. |
| 2 | **songBird mesh enrollment** | eastGate / songBird | flockGate peers are stale (legacy `old-peer`, `iron-gate`, `west-gate`). WG mesh gates not enrolled via `mesh.enroll` BTSP HMAC. |

### `membrane tower.shadow` spec (from gate AARs)

The command must:
1. Configure songBird to duplicate inter-gate RPC on both WG and Tower paths
2. Collect latency/throughput/jitter metrics per gate pair
3. Export to `benchScale/tower_shadow/` in JSON format (per convergence brief)

Until shipped, gates run manual `songbird benchmark` (point-in-time, not continuous).

### songBird mesh enrollment

flockGate's songBird mesh shows 3 legacy peers. Current WG mesh gates
(sporeGate, eastGate, golgiBody) need `mesh.enroll` with BTSP HMAC proofs.
Without this, Tower transport cannot route to the correct peers at transport level.

---

## P1 — Exploration (primalSpring teams)

Tower Atomic already **exceeds** WireGuard on WAN throughput. Six domains to explore:

| # | Domain | Scenario | What to Measure |
|---|--------|----------|-----------------|
| 1 | **Capability-aware routing** | `s_tower_capability_routing` | Per-capability latency/throughput vs single WG tunnel |
| 2 | **Multi-stack routing** | `s_tower_multi_stack` | N songBird on golgiBody, per-purpose tuning |
| 3 | **Large data transfer** | `s_tower_large_data` | 100MB–10GB blobs: throughput, CPU, CAS dedup |
| 4 | **Secure compute mesh** | `s_tower_secure_compute` | bearDog per-session keys vs WG tunnel crypto |
| 5 | **Distributed compute** | `s_tower_compute_mesh` | toadStool cross-gate dispatch + aggregation |
| 6 | **Edge/SFF profile** | `s_tower_edge_profile` | songBird on NUC Celeron: idle CPU, memory |

### Also P1

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 7 | Fix `songbird.sock` (dir, not socket) | songBird | flockGate UDS discovery broken |
| 8 | Direct LAN peering (sporeGate↔eastGate) | operator | Bypass golgiBody hub, unlocks sub-1ms benchmark |
| 9 | Restart songbird-gateway on sporeGate | sporeGate ops | Activate BUILD_AUTHORITY env |
| 10 | iperf3 baseline (sustained throughput) | sporeGate + flockGate | Server-side coordination needed |

---

## P2 — Queued

| # | Task | Owner | Detail |
|---|------|-------|--------|
| 1 | sporePrint primal pipeline | eastGate | Zola replacement |
| 2 | CredentialStore squirrel integration | eastGate | `secrets.*` JSON-RPC |
| 3 | bingoCube WASM WebGL widget | eastGate | Unblocked by petalTongue 150r |
| 4 | Android Keystore + grapheneGate test | bearDog | CredentialStore TEE |
| 5 | Promote 6 pseudoSpores | lithoSpore | Validation Data Stream v1.0 |
| 6 | footPrint declarative source registry | flockGate | DATA_LAYER_PRIMAL_ABSTRACTION |

## P3 / Future

| # | Task | Detail |
|---|------|--------|
| 1 | Phase 3 cutover | Tower replaces WG (pending Phase 2) |
| 2 | rootPulse design | Sovereign VCS |
| 3 | pseudoSpore Explorer | esotericWebb interactive viz |
| 4 | SHOW_HN readiness | Rubric, narrative, demo path |

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
| Sovereign depot pipeline (4 phases + deep debt sweep, 1110 tests) | 150w |
| Benchmark harness shipped, TURN relay LIVE, all blockers cleared | 150v |
| Standards reorg, DNSSEC 3/3, Sovereignty roadmap, cascade 43/43 | 150s-u |
| Scene unification, NUCLEUS, Silicon Atheism P2, CAC 6/6, Glacial 8/8 | ≤150i |

---

## SOVEREIGNTY

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic | **EXCEEDS on WAN (2x throughput). Shadow deploying.** |
| **REPLACE** | Zola | petalTongue + nestGate CAS | Design pending |
| **LATE-STAGE** | Forgejo | rootPulse | Post-rootPulse |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk / JupyterHub | Outer membrane | Stays |

---

## TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, TURN relay, CI hook 43/43
  ├─ sporeGate (10.13.37.2) — build authority, BUILD_AUTHORITY=1 set
  ├─ eastGate  (10.13.37.5) — orchestrator, code hub, Akida NPU
  ├─ flockGate (10.13.37.6) — WAN peer, Tower 7+ days stable
  ├─ ironGate  (10.13.37.7) — compute, GPU [DOWN]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Pending: southGate (.9), strandGate (EPYC, 256GB, 3090)
10G backbone: 4 towers NIC'd, cabling pending
```

---

*Wave 150w: Tower EXCEEDS WireGuard — 2x throughput on WAN, 0.99x latency.
Shadow deploy blocked on `membrane tower.shadow` (eastGate P0). songBird
mesh enrollment needed (stale peers). Sovereign CI deployed 43/43.
primalSpring teams exploring 6 domains to evolve Tower beyond parity.
43/43 converged.*
