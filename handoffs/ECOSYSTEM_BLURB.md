# ecoPrimals Ecosystem Blurb — Wave 150v

**Date**: Jul 23, 2026 07:15 EDT | **Wave**: 150v | **From**: eastGate overwatch
**Posture**: **EXECUTE PARITY BENCHMARKS. ALL BLOCKERS RESOLVED.**

---

## MISSION: Tower Atomic Parity Benchmark

Tower Atomic (bearDog + songBird + skunkBat) replaces WireGuard for mesh transport.
All infrastructure is LIVE. The `songbird benchmark` CLI harness is SHIPPED.
**Execute LAN + WAN parity benchmarks and report results.**

### What's Ready

| Component | Status | Detail |
|-----------|--------|--------|
| Tower primals (3/3) | **LIVE** on sporeGate, flockGate, grapheneGate | bearDog, songBird, skunkBat |
| TURN relay | **LIVE** on golgiBody:3478 | Since Jul 12, `songbird-relay.service` |
| Benchmark harness | **SHIPPED** | `songbird benchmark` — setup/latency/throughput, JSON+text, p50/p95/p99 |
| Structural scenario | **GREEN** | 21/21 checks pass (`s_tower_atomic_parity`) |
| WG baselines | **MEASURED** | sporeGate→golgi 38ms, flockGate→golgi 31ms, end-to-end 68ms |

### Parity Philosophy

Initial goal is **WireGuard parity** — any tractable first solution.
WG has years of dev time on us. Match first, exceed later.
Targets are **relative to WG baseline**, not absolute thresholds.

---

## TEAM ASSIGNMENTS

### sporeGate — Benchmark Driver (LAN + WAN)

> **primalSpring** on sporeGate — Wave 150v, parity execution.
>
> You drive both benchmarks. The harness and relay are LIVE.
>
> **LAN benchmark** (sporeGate ↔ eastGate, same backbone):
> ```
> songbird benchmark --mode tower-atomic --peer 10.13.37.5:7700 --probes 100 --duration 30s --output json > /tmp/lan_tower.json
> songbird benchmark --mode wireguard   --peer 10.13.37.5:7700 --probes 100 --duration 30s --output json > /tmp/lan_wg.json
> ```
>
> **WAN benchmark** (sporeGate → golgiBody TURN → flockGate):
> ```
> songbird benchmark --mode tower-atomic --peer 10.13.37.6:7700 --probes 100 --duration 30s --output json > /tmp/wan_tower.json
> songbird benchmark --mode wireguard   --peer 10.13.37.6:7700 --probes 100 --duration 30s --output json > /tmp/wan_wg.json
> ```
>
> **Topology**:
> ```
> LAN: sporeGate (.2) ←→ eastGate (.5)     [same backbone switch]
> WAN: sporeGate (.2) ←→ golgiBody TURN (.1) ←→ flockGate (.6)
> ```
>
> **Deliverables**:
> 1. Run all 4 benchmark commands above
> 2. Capture JSON output for primalSpring consumption
> 3. Compare Tower vs WG: latency (p50/p95/p99), throughput (Mbps), setup time (ms)
> 4. File AAR to `infra/wateringHole/aars/` with results and analysis
> 5. Push AAR + JSON reports upstream
>
> **Parity targets** (relative to WG baseline):
>
> | Metric | WG Baseline | Tower Target |
> |--------|-------------|--------------|
> | RTT (LAN) | ~1ms | ≤ WG * 1.5x |
> | RTT (WAN, 2-hop) | ~68ms | ≤ WG * 1.5x |
> | Throughput | TBD | ≥ WG * 0.8x |
> | Setup time | ~50ms | ≤ 500ms |
>
> **CONVERGENCE RULE**: Do NOT evolve primal code. Run benchmarks,
> report results, file AAR. Code evolution happens on eastGate only.
>
> **Read first**:
> - `primals/songBird/infra/wateringHole/TOWER_ATOMIC_CONVERGENCE.md`
> - `primals/songBird/deployment/relay/README.md`
> - `primals/songBird/infra/wateringHole/HANDOFF.md`

---

### eastGate — Orchestrator + LAN Peer

> **primalSpring** on eastGate — Wave 150v, orchestration + code evolution.
>
> **Role 1: LAN benchmark peer**
> - Serve as the far endpoint for sporeGate's LAN benchmark
> - Ensure Tower primals are running: bearDog (`security.sock`),
>   songBird (`:7780` drawbridge), skunkBat (via BTSP dispatch)
> - Accept incoming benchmark probes from sporeGate (.2)
>
> **Role 2: Code evolution hub**
> - All code changes happen here, nowhere else
> - Integrate benchmark results from sporeGate + flockGate AARs
> - Ship `s_tower_atomic_parity_live` scenario once results arrive
> - Calibrate WAN latency targets based on actual measurements
>   (WG=68ms 2-hop — redefine as "Tower ≤ WG * 1.5x")
>
> **Role 3: Remaining evolution queue**
>
> | # | Item | Priority |
> |---|------|----------|
> | 1 | Integrate parity benchmark results → live scenario | **P1** |
> | 2 | sporePrint primal pipeline (Zola replacement design) | P1 |
> | 3 | CredentialStore squirrel integration (`secrets.*` JSON-RPC) | P1 |
> | 4 | bingoCube WASM WebGL widget (petalTongue unblocked) | P2 |
> | 5 | `.unwrap()` clippy audit — remaining primals | P2 |
> | 6 | rootPulse design (sovereign VCS, long-term) | P3 |
>
> **CONVERGENCE RULE**: eastGate is the sole code evolver.
> Gate teams file AARs → eastGate integrates and pushes.

---

### flockGate — WAN Benchmark Peer

> **primalSpring** on flockGate — Wave 150v, WAN peer.
>
> You serve as the far endpoint for the WAN parity benchmark.
> sporeGate drives, you respond.
>
> **What to do**:
> 1. Verify Tower primals running (bearDog, songBird, skunkBat)
>    ```
>    # Check services
>    systemctl status beardog songbird skunkbat
>    # Or check sockets
>    ls /run/user/$(id -u)/biomeos/security.sock
>    ```
> 2. Accept incoming benchmark probes from sporeGate (.2) via
>    golgiBody TURN relay (.1)
> 3. Confirm esotericWebb V22 still healthy (webb.primals.eco)
>    — should not conflict, different ports
> 4. Optionally run reverse benchmarks from flockGate side for
>    bidirectional comparison
>
> **Topology**:
> ```
> WAN benchmark path:
>   sporeGate (.2) ←→ golgiBody TURN (:3478) ←→ flockGate (.6) ← YOU
>                     vs.
>   sporeGate (.2) ←→ golgiBody WG hub (.1) ←→ flockGate (.6)
> ```
>
> **Deliverables**:
> 1. Confirm WAN peer ready (Tower responding to probes)
> 2. File short AAR confirming participation + any anomalies
> 3. Push AAR upstream
>
> **CONVERGENCE RULE**: Do NOT evolve primal code. Serve as peer,
> report findings, file AAR. Code evolution happens on eastGate only.

---

## CONTEXT (for reference)

### Deployment Chain
```
User → Cloudflare DNS (*.primals.eco → golgiBody 157.230.3.183)
  → Caddy (TLS, Host-header routing) → WireGuard mesh → gate → service
```

### Mesh Topology
```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, TURN relay LIVE (:3478)
  ├─ sporeGate (10.13.37.2) — builder, Tower 3/3 [BENCHMARK DRIVER]
  ├─ eastGate  (10.13.37.5) — orchestrator, dev  [LAN PEER + CODE HUB]
  ├─ flockGate (10.13.37.6) — esotericWebb V22   [WAN PEER]
  ├─ ironGate  (10.13.37.7) — compute, GPU       [DOWN — hw offline]
  └─ northGate (10.13.37.8) — Windows, RTX 5090  [enrolled]
```

### Sovereignty Evolution

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic | **BENCHMARKING NOW** |
| **REPLACE** | Zola | petalTongue + nestGate CAS + cellMembrane | Pipeline design pending |
| **LATE-STAGE** | Forgejo | rootPulse | Post-rootPulse |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk / JupyterHub | Outer membrane stays |

### What's Done (fossilized)

| Achievement | Wave |
|-------------|------|
| Benchmark harness shipped, TURN relay LIVE, all blockers resolved | 150v |
| Tower primals deep debt, gate AARs GREEN, structural 21/21, WG baselines | 150v |
| Standards reorg, DNSSEC 3/3, Sovereignty roadmap, cascade 43/43 | 150s-u |
| WASM WebGL, vendor analysis, USB enrollment, workspace reorg | ≤150r |
| Scene unification, NUCLEUS, Silicon Atheism P2, CAC 6/6, Glacial 8/8 | ≤150i |

---

*Wave 150v: ALL BLOCKERS RESOLVED. Three primalSpring teams executing Tower Atomic parity
benchmarks. sporeGate drives (LAN + WAN), eastGate serves as LAN peer and code hub,
flockGate serves as WAN peer. Results determine if Tower Atomic matches WireGuard.
Parity first, exceed later. 43/43 converged.*
