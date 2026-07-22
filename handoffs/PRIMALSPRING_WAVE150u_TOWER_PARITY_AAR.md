# primalSpring AAR — Wave 150u: Tower Atomic Parity Scenario

**Date**: 2026-07-22 | **Gate**: eastGate | **Version**: v0.9.42
**Commit**: `1ab0bfea` | **Status**: STRUCTURAL VALIDATION COMPLETE

---

## What Was Done

primalSpring shipped the **Tower Atomic Parity Benchmark** scenario (item #3a
from the Wave 150u team actions). This validates structural readiness for the
WireGuard → Tower Atomic sovereignty cutover.

### New Scenario: `tower-atomic-parity`

| Property | Value |
|----------|-------|
| Track | Evolution |
| Tier | Rust |
| Checks | 21 (5 phases) |
| Result | ALL PASS |

**Phase breakdown:**

1. **Composition primals** — bearDog BTSP auth + negotiate, songBird relay +
   connect, skunkBat IDS/anomaly, Tower composition tier (5 signals), bootstrap
   signal (two-phase cold-start)
2. **Relay capabilities** — mesh.enroll/init (BTSP-HMAC proof), path finding,
   peer roster, relay publish, BTSP escalation enforcement on relay methods
3. **Benchmark topology** — ≥2 LAN peers with WG addresses, backbone zone peer
   (eastGate/sporeGate), VPS hub (.1) for WAN relay, cross-zone peer (house2)
4. **Parity spec** — latency targets (<5ms LAN, <50ms WAN), throughput targets
   (>800 Mbps LAN, >50 Mbps WAN), tower.health signal for monitoring
5. **Credential store** — secrets.* capability present (CredentialStore shipped
   150u), btsp.server.status for runtime BTSP health

---

## What This Enables

The structural scenario is GREEN. The **actual parity benchmark** requires
Live-tier execution with two active peers running the Tower Atomic stack.

---

## Spin-Up Request for Upstream Teams

### Item #3b: ironGate team — LAN benchmark peer

**What**: Deploy Tower Atomic stack (bearDog + songBird + skunkBat) on ironGate
and run LAN throughput/latency tests against eastGate.

**Requirements**:
- Tower Atomic binaries from depot (all 3 in plasmidBin)
- BTSP-authenticated relay between eastGate (.5) ↔ ironGate (.7)
- iperf3-equivalent throughput test through Tower relay (target: >800 Mbps)
- ping-equivalent latency test through Tower relay (target: <5ms RTT)
- Compare against raw WireGuard baseline on same link
- Report results as `TOWER_LAN_PARITY_RESULTS.md` in wateringHole handoffs

**Topology**:
```
eastGate (10.13.37.5) ←→ Tower Atomic relay ←→ ironGate (10.13.37.7)
                         vs.
eastGate (10.13.37.5) ←→ WireGuard tunnel  ←→ ironGate (10.13.37.7)
```

### Item #3c: golgiBody team — WAN benchmark peer + TURN relay

**What**: Deploy Tower Atomic TURN relay on golgiBody and run WAN
throughput/latency tests between LAN gates and VPS.

**Requirements**:
- Tower Atomic binaries on golgiBody (bearDog + songBird minimum)
- TURN-style relay configuration (songBird mesh.relay listening on VPS)
- iperf3-equivalent throughput test through Tower WAN relay (target: >50 Mbps)
- Latency test eastGate (.5) → golgiBody (.1) → ironGate (.7) (target: <50ms)
- Compare against WG WAN baseline through same path
- Report results as `TOWER_WAN_PARITY_RESULTS.md` in wateringHole handoffs

**Topology**:
```
eastGate (10.13.37.5) ←→ golgiBody TURN (.1) ←→ ironGate (10.13.37.7)
                          vs.
eastGate (10.13.37.5) ←→ golgiBody WG hub (.1) ←→ ironGate (10.13.37.7)
```

---

## primalSpring Live Scenario (pending benchmark results)

Once #3b and #3c report results, primalSpring will ship:
- `s_tower_atomic_parity_live` (Live tier) — actual benchmark execution
- Tolerance constants in `tolerances/` for Tower vs WG parity thresholds
- Updated sovereignty-roadmap scenario with benchmark PASS/FAIL gate

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Scenarios | 174 |
| Lib tests | 1214 (0 fail, 2 ignored) |
| Clippy | 0 (pedantic + nursery) |
| KNOWN_DEBT | 2 (graphenegate-readiness: 1, composition-access-control: 15) |

---

## For Overwatch

- **primalSpring item #3a**: DONE — structural scenario shipped
- **ironGate team (#3b)**: SPIN UP — deploy Tower Atomic, run LAN benchmark
- **golgiBody team (#3c)**: SPIN UP — deploy TURN relay, run WAN benchmark
- **primalSpring (next)**: waiting on benchmark results to ship Live-tier scenario

No blockers. eastGate primalSpring is ready to consume benchmark data as soon
as the peer teams report.
