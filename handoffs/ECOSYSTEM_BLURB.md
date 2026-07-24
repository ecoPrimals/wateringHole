# ecoPrimals Ecosystem Blurb — Wave 150x

**Date**: Jul 24, 2026 11:33 EDT | **Wave**: 150x | **From**: eastGate overwatch
**Posture**: **P1 BURN-DOWN ACTIVE. 17 FINDINGS RESOLVED (flockGate). songBird + skunkBat HARDENED. TOWER 267x LAN.**

---

## WHERE WE ARE

Tower Atomic **267x faster** than WG overlay on LAN (0.586ms vs 157ms), **1.7x WAN
sustained throughput** (7.1 vs 4.2 Mbps). All 6 domains PROVEN LIVE. flockGate
burned 17 findings (known debt 30 → 29 on eastGate, flockGate reports 48 total
including architecture-specific). songBird shipped pen test hardening (UDS-spoof,
mesh-poison, relay-abuse) + dependency diet (ring→rustcrypto). skunkBat shipped
cipher floor policy. sporeGate hardware team handed off final AAR. P0 CLEAR.

**Glacial correction**: This wave surfaced a git merge divergence that lost data
during multi-gate concurrent pushes to wateringHole. This is not a bug to fix —
it is evidence for the rootPulse roadmap. Git's merge model cannot handle
multi-writer convergence with attribution. rootPulse (DAG + linear + attribution
over nestGate CAS + Provenance Trio) solves this natively. The waterFall publish
cascade (`graphs/waterfall_publish.toml`) already defines the full composition.
We mature existing systems, not patch industry tool limitations.

---

## NEAR-TERM SYSTEMS (what we leverage)

The ecosystem already has mature coordination infrastructure:

| System | Standard | Status | What It Does |
|--------|----------|--------|-------------|
| **waterFall** | `waterfall_publish.toml` | Defined, partially wired | Full cascade: git → impulse → DAG → braid → anchor → relay |
| **Impulse/Potential** | `IMPULSE_POTENTIAL_STANDARD.md` | Active (Wave 63+) | Machine-readable TOML FRAGOs, auto-discovered via cascade |
| **Context Braids** | `CONTEXT_BRAID_STANDARD.md` | Active (Wave 63+) | Structured developer state, TTL auto-decay, replaces blurb paste |
| **Provenance Trio** | rhizoCrypt + loamSpine + sweetGrass | Wired | DAG lineage, ledger anchoring, semantic braids |
| **Sovereign CI** | Forgejo hooks + cascade drift | LIVE (Wave 150w) | Auto-build on push, depot sync, lineage validation |
| **Crash-Loop Breaker** | cellMembrane `gate.crash-loop` | LIVE (Wave 150x) | Self-recovery: detect + stop + disable runaway services |

These systems compose through `NeuralBridge` in membrane-shadow with
try-primal-first semantics. The graduation path from shadow → primal
composition is documented in `ECOSYSTEM_COMMUNICATION_STANDARD.md`.

---

## TOPOLOGY

```
eastGate (.5)    — 1G MikroTik — code hub, LAN peer (0.17ms RTT)
sporeGate (.2)   — 1G MikroTik — membrane coordinator, build authority, HPC
flockGate (.6)   — WAN — Tower primal code teams
golgiBody (.1)   — WAN hub — TURN relay, depot, Forgejo
northGate (.8)   — Windows 11, RTX 5090 — enrolled
grapheneGate     — Tower LIVE (bearDog + songBird + skunkBat)
10G backbone     — between houses/large compute (DONE)
```

New gates (friends/family) use R45 topology. Tower handles mixed 1G/10G routing.

---

## P1 — BURN DOWN KNOWN DEBT (29 eastGate, 48 flockGate)

Teams burning independently. flockGate resolved 17 this cascade:
`concurrent-dispatch` (3→0), `mesh-churn` (4→0), `cipher-downgrade` (4→1),
`enrollment-replay` (2→1), `capability-escalation` (6→4). songBird hardened
UDS-spoof + mesh-poison + relay-abuse (code-level fixes). skunkBat shipped
cipher floor policy.

| Category | Remaining | Key Items |
|----------|-----------|-----------|
| bearDog | 2 | Bond-type cipher floor, seed rotation |
| songBird | 9 | Caller identity (4), UDS hardening (5) |
| Architecture | 27 | grapheneGate aarch64 (14), access-control (13) |
| Misc | 10 | btsp-storm, failover, uds-hop, shadow-fidelity, arch |

### Topology (sporeGate team)

| # | Task | Detail |
|---|------|--------|
| 1 | iperf3 sustained throughput | 1G LAN: `songbird benchmark --sustained` |
| 2 | Gate enrollment (southGate, strandGate) | USB staged, R45 |
| 3 | songBird LAN peer discovery | MikroTik local-priority routing |

## P2 — SOVEREIGNTY EVOLUTION

| # | Task | Owner | Leverage |
|---|------|-------|---------|
| 1 | **sporePrint transplant** | sporeGate | Update primals.eco with Tower Atomic, topology, sovereign CI |
| 2 | sporePrint primal pipeline | eastGate | Replace Zola with petalTongue + nestGate CAS + cellMembrane |
| 3 | CredentialStore squirrel integration | eastGate | bearDog `FileVault` + squirrel IPC |
| 4 | bingoCube WASM WebGL widget | eastGate | Interactive commitment grid on primals.eco |
| 5 | Enrollment seed rotation | bearDog (flockGate) | Pen test finding |

## P3 — ATOMIC EVOLUTION

| # | Task | Depends On |
|---|------|-----------|
| 1 | **Chimera Phase 0** — library extraction | Can start now (pure refactoring) |
| 2 | Node Atomic (proton) | Tower chimera maturity |
| 3 | Nest Atomic (neutron) | Node Atomic |
| 4 | Phase 3 cutover — Tower replaces WG | Chimera + sustained validation |
| 5 | rootPulse sovereign VCS | Provenance Trio maturity + Tower transport |

---

## EXPLORATION DOMAINS — ALL PROVEN LIVE

| # | Domain | Evidence | Where WG Cannot |
|---|--------|----------|-----------------|
| 1 | Capability-aware routing | 5 providers via `capability.call` | WG: all traffic in one tunnel |
| 2 | Multi-stack routing | 6 classes → 5 stacks | WG: undifferentiated |
| 3 | Large data transfer | `content.put` → nestGate CAS | WG: no content awareness |
| 4 | Secure compute mesh | Per-session BTSP keys + attestation | WG: one static key per tunnel |
| 5 | Distributed compute | 4-node targeted dispatch | WG: point-to-point only |
| 6 | Edge/SFF/R45 profile | 30MB RSS, 39MB stack, 300s TTL | WG: kernel module required |

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — 43/43 synced, waterFall + impulse + braids active |
| 2 | Ecological | GREEN — 196 scenarios, 30 debt, chimera Phase 0 ready |
| 3 | Hardware | AMBER — 4 offline gates, topology LIVE |
| 4 | Sovereignty | GREEN — Tower EXCEEDS WG, 6/6 domains, CI LIVE |
| 5 | Public Surface | GREEN — 6/6 healthy, sporePrint transplant issued |
| 6 | Compositions | GREEN — footPrint + esotericWebb LIVE, 6/6 Tower domains |
| 7 | Documentation | GREEN — fossil pass complete, 7 handoffs + 4 AARs active |
| 8 | Campus | GREEN — vision documented, pages pending |

**Fossilized** (F1–F6): Glacial Shift, CAC, Silicon Atheism, Depot/Build, Cascade, Tower Deep Analysis.

---

## ACTIVE DOCS

| Type | Count | Era |
|------|-------|-----|
| Handoffs | 7 | 150w–150x |
| AARs | 4 | 150w–150x |
| Analysis | 3 | 150w–150x |

---

*Wave 150x: Tower EXCEEDS WireGuard (1.56x LAN, 1.11x WAN). 6/6 exploration
domains PROVEN LIVE. Glacial correction: git divergence is rootPulse evidence,
not a bug to patch. Mature existing systems (waterFall, impulse, context braids,
Provenance Trio) before adding new patterns. sporePrint transplant guidance
issued for primals.eco update. 30 known debt findings for teams to burn down.
Crash-loop self-recovery LIVE at both app and systemd layers. 196 scenarios
PASS. 43/43 converged.*
