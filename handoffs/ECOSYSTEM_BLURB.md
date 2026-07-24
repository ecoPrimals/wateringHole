# ecoPrimals Ecosystem Blurb — Wave 150x

**Date**: Jul 24, 2026 09:37 EDT | **Wave**: 150x | **From**: eastGate overwatch
**Posture**: **SYSTEMD HARDENING SHIPPED. `Restart=always` ELIMINATED ECOSYSTEM-WIDE. CRASH-LOOP ROOT CAUSE CLOSED.**

---

## WHERE WE ARE

Tower Atomic Phase 1 PASS (WG parity proven). Phase 2 shadow ACTIVE on 3 gates.
All 4 teams converged on crash-loop divergence. cellMembrane now ships the
**systemd-level fix**: every unit changed from `Restart=always` to `Restart=on-failure`
with `StartLimitBurst=10` / `StartLimitIntervalSec=120`. The 29,081-restart
pattern is now impossible at the unit level, not just detected by crash-loop breaker.

bearDog AAR: security hardening documented (13,937 tests). eastGate AAR:
**Tower 1.56x WG throughput on LAN** (6.49 vs 4.16 Gbps), LAN path 500x
faster than WG overlay (0.15ms ICMP vs 78ms WG overlay). Shadow timer active.

Dimensional review (150x): **8 GREEN / 1 AMBER (hardware — offline gates)**.
Fossil pass: 27 stale docs archived. P0 CLEAR. Known debt: 30 findings.

---

## TOPOLOGY (LIVE — already operational)

```
eastGate (.5)    — R45 → MikroTik — code hub, LAN peer (0.17ms to sporeGate)
sporeGate (.2)   — R45 → MikroTik — intra-membrane coordinator, HPC interface, build authority
flockGate (.6)   — WAN peer — Tower primal code teams
golgiBody (.1)   — WAN hub — TURN relay, depot, CI hooks, Forgejo
northGate (.8)   — Windows 11, RTX 5090 — enrolled
grapheneGate     — Tower LIVE (bearDog + songBird + skunkBat)
```

**Backbone**: 10G between houses/large compute (DONE). 1G MikroTik for LAN gates (DONE).
New gates (friends/family) use R45 topology — Tower must leverage mixed 1G/10G routing.
Sustained throughput testing can run NOW on 1G LAN (sporeGate ↔ eastGate).

---

## P0 — CLEAR

No outstanding P0 items.

## P1 — REMAINING

### Tower Hardening (30 known debt findings)

All 9 shipped tasks from the convergence cascade are DONE. The 30 remaining
findings are distributed across 10 stress/pen scenarios — teams evolve
independently against them. No single blocker.

### Topology (sporeGate team)

| # | Task | Detail |
|---|------|--------|
| 1 | iperf3 sustained throughput | 1G LAN: `songbird benchmark --sustained` (sporeGate ↔ eastGate) |
| 2 | Gate enrollment (southGate, strandGate) | USB staged, R45 topology |
| 3 | Fix biomeos-beacon service unit | Point to depot binary or disable |
| 4 | songBird LAN peer discovery | Leverage MikroTik topology for local-priority routing |

### Exploration (6 domains)

| # | Domain | Status |
|---|--------|--------|
| 1 | Capability-aware routing | **PROVEN LIVE** |
| 2 | Multi-stack routing (golgiBody multiple Tower stacks) | Structural GREEN |
| 3 | Large data transfer (prep notice → route via Tower) | Structural GREEN |
| 4 | Secure compute mesh | Structural GREEN |
| 5 | Distributed compute | Structural GREEN |
| 6 | Edge/SFF/R45 profile (friends + family gates) | Structural GREEN |

## P2 — Queued

| # | Task | Owner |
|---|------|-------|
| 1 | sporePrint primal pipeline (replace Zola) | eastGate |
| 2 | CredentialStore squirrel integration | eastGate |
| 3 | bingoCube WASM WebGL widget | eastGate |
| 4 | Android Keystore + grapheneGate | bearDog (flockGate) |
| 5 | Promote 6 pseudoSpores | lithoSpore |
| 6 | Enrollment seed rotation | bearDog (flockGate) |

## P3 / Future

| # | Task |
|---|------|
| 1 | **biomeOS chimera** — Phase 0 library extraction (pure refactoring, can start now) |
| 2 | Node Atomic (proton) — depends on Tower chimera maturity |
| 3 | Nest Atomic (neutron) — depends on Node Atomic |
| 4 | Phase 3 cutover — Tower replaces WG on all gates |
| 5 | rootPulse sovereign VCS |
| 6 | pseudoSpore Explorer |

---

## DIMENSIONAL SCORECARD (Wave 150x)

| # | Dimension | Status | Key Finding |
|---|-----------|--------|-------------|
| 1 | Temporal | GREEN | 43/43 synced, blurb current, GLOSSARY needs refresh |
| 2 | Ecological | GREEN | 196 scenarios PASS, 30 known debt, all primals compile |
| 3 | Hardware/Topology | AMBER | 10G+1G LIVE, shadow on 3 gates, 4 offline gates pending |
| 4 | Sovereignty | GREEN | DNSSEC 3/3, sovereign CI, crash-loop breaker, Tower P1 PASS |
| 5 | Public Surface | GREEN | 6/6 healthy, pen test surface mapped |
| 6 | Compositions | GREEN | footPrint + esotericWebb LIVE, petalTongue WASM shipped |
| 7 | Documentation | GREEN | 27 docs fossilized, 6 active handoffs, 6 active AARs |
| 8 | Campus | GREEN | Vision documented, pages pending |
| 9 | Tower Deep Analysis | GREEN | Honest data, chimera design, 4-team convergence |

**Fossilized** (F1–F5): Glacial Shift, CAC, Silicon Atheism, Depot/Build, Cascade — all stable.

---

## WHAT'S DONE (fossilized)

| Wave | Achievement |
|------|-------------|
| 150w | Tower Atomic PHASE 1 PASS, shadow ACTIVE 3 gates, LAN peering 0.17ms |
| 150w | Sovereign depot pipeline DELIVERED (4 phases) |
| 150x | Service crash-loop divergence found + stopped (29,081 restarts) |
| 150x | Tower deep analysis: 3 docs, 14 new scenarios (196 total), chimera design |
| 150x | ALL 4 TEAMS CONVERGED: 1,838 lines, P1 Tower Hardening 9/9 SHIPPED |
| 150x | Dimensional review: 8G/1A, 5 fossilized dimensions stable |
| 150x | Fossil pass: 27 docs → fossilRecord, 6 handoffs + 6 AARs remain active |
| 150x | **systemd hardening**: `Restart=always` → `on-failure` + StartLimitBurst ALL units |
| 150x | **nestgate nosocket unit**: `membrane-nucleus-nosocket@.service` for evolved CLI |
| 150x | **bearDog AAR**: security hardening documented (13,937 tests, 0 failures) |

---

*Wave 150x: cellMembrane eliminated `Restart=always` from ALL systemd units (12 files).
Every unit now uses `Restart=on-failure` + `StartLimitBurst=10` + `StartLimitIntervalSec=120`.
New `membrane-nucleus-nosocket@.service` for nestgate's evolved CLI. bearDog pushed
AAR documenting enrollment replay protection + UDS connection cap (13,937 tests).
Crash-loop root cause is now closed at both application (breaker) and systemd (limits) layers.
P0 CLEAR. 30 known debt. 196 scenarios PASS. 43/43 converged.*
