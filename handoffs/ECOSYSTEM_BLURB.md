# ecoPrimals Ecosystem Blurb — Wave 150x

**Date**: Jul 24, 2026 20:45 EDT | **Wave**: 150x | **From**: eastGate overwatch
**Posture**: **KNOWN DEBT 30→10. songBird CallerContext + UDS hardening resolved 7 pen scenarios. 653 shadow samples. blake3 delegation LIVE.**

---

## WHERE WE ARE

Tower 267x LAN, 1.7x WAN. 6/6 domains PROVEN LIVE. **Known debt collapsed
from 30 to 10 findings** — songBird's CallerContext + UDS hardening resolved
`capability-escalation` (4→1), `uds-spoof` (5→1), and bearDog's cipher floor
resolved pen findings. primalSpring pushed 10 hours of continuous shadow data
(653 JSON samples across 6 gates). songBird wired blake3 delegation to
bearDog via `crypto.hash.blake3` — crypto composition advancing. P0 CLEAR.

---

## CODE TEAMS (flockGate — primal source evolution)

### bearDog — crypto primal

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | ~~Bond-type cipher floor enforcement~~ | DONE | BTSP negotiation rejects below floor |
| 2 | ~~`crypto.hash.blake3` capability~~ | DONE | songBird can now delegate blake3 via UDS |
| 3 | ~~Deep debt sweep~~ | DONE | Hardcoding eliminated, capability-based config |
| 4 | Enrollment seed rotation | P2 | Queued |
| 5 | Android Keystore + grapheneGate validation | P2 | Code complete, awaiting hardware |

bearDog is the ecosystem crypto provider. All primals route crypto through
bearDog UDS (`crypto.*` capabilities). Hot-path crypto stays local until
chimera extracts shared library.

### songBird — transport/routing primal

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | **Crypto delegation to bearDog** | P1 | blake3 delegation LIVE (`dark_forest_beacon`), 4 crates feature-gated |
| 2 | ~~Caller identity verification~~ | DONE | `CallerContext` wired into IPC connection + method gate |
| 3 | ~~UDS hardening~~ | DONE | Socket permissions, peer cred verification |
| 4 | ~~Pen test hardening~~ | DONE | UDS-spoof, mesh-poison, relay-abuse |
| 5 | ~~Dependency diet~~ | DONE | ring→rustcrypto, chrono eliminated, rand→fastrand, 83 files |
| 6 | ~~Legacy env deprecation~~ | DONE | Name-based endpoints marked for removal |

`CRYPTO_COMPOSITION.md` classifies 19 seams: 5 hot-path (chimera), 6 delegating
(bearDog UDS), 5 test-only, 3 already delegating.

### skunkBat — defense/protocol primal

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | Cipher floor policy | DONE | `SKUNKBAT_CIPHER_FLOOR` env, typed BindMode errors |
| 2 | Deep debt sweep | DONE | `unreachable!()` eliminated, BTSP dedup |
| 3 | Spawn-rate anomaly detection | DONE | Shipped 150x |

skunkBat is clean. No open P1. Future work: chimera integration.

---

## DEPLOYMENT / OPS (sporeGate — build, deploy, hardware, topology)

### cellMembrane — membrane coordinator

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | systemd hardening | DONE | `Restart=always` eliminated ecosystem-wide |
| 2 | Crash-loop breaker | DONE | `gate.crash-loop` + auto-scan in cascade |
| 3 | Sovereign CI pipeline | DONE | Forgejo hooks → build → depot → lineage |
| 4 | `membrane-nucleus-nosocket@.service` | DONE | nestgate evolved CLI support |
| 5 | ~~Deep debt sweep~~ | DONE | LAN registry, test extraction, safe casts, +960/-861 |

### Topology / Hardware

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | iperf3 sustained throughput | P1 | **BLOCKED** — needs eastGate iperf3 server or SSH access |
| 2 | Gate enrollment (southGate) | P1 | USB staged, needs physical cabling |
| 3 | Gate enrollment (strandGate) | P1 | USB staged, needs physical cabling + WG IP allocation |
| 4 | songBird LAN peer discovery | P1 | MikroTik local-priority routing |
| 5 | Fix biomeos-beacon unit (eastGate) | P1 | Disable phantom unit (11,161 restarts) |
| 6 | SSH access sporeGate→eastGate | P1 | No key auth configured |
| 7 | Manifest: eastGate LAN IP | P1 | Correct `192.168.4.5` → `192.168.4.244` |

### sporePrint — public face

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | Transplant to primals.eco | P2 | Guidance issued (`SPOREPRINT_WAVE150x_TRANSPLANT_GUIDANCE.md`) |

---

## OVERWATCH (eastGate — code hub, integration, scenarios)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | primalSpring scenario debt burn-down | P1 | **10 known debt** (196 scenarios, all PASS) |
| 2 | Unblock sporeGate (iperf3 server, SSH key, biomeos-beacon) | P1 | Ops tasks from sporeGate AAR |
| 3 | sporePrint primal pipeline (Zola → petalTongue + nestGate CAS) | P2 | Design phase |
| 4 | CredentialStore squirrel integration | P2 | bearDog `FileVault` + squirrel IPC |
| 5 | bingoCube WASM WebGL widget | P2 | Interactive commitment on primals.eco |
| 6 | Chimera Phase 0 — library extraction | P3 | After bearDog UDS composition validated |

---

## ATOMIC EVOLUTION (all teams)

| # | Task | Depends On |
|---|------|-----------|
| 1 | **Composition validation** — bearDog UDS crypto works for all cold-path | Code teams (P1) |
| 2 | **Chimera Phase 0** — shared library extraction | Composition validated |
| 3 | Node Atomic (proton) | Tower chimera maturity |
| 4 | Nest Atomic (neutron) | Node Atomic |
| 5 | Phase 3 cutover — Tower replaces WG | Chimera + sustained validation |
| 6 | rootPulse sovereign VCS | Provenance Trio maturity + Tower transport |

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
| 1 | Temporal/Coordination | GREEN — 43/43 synced |
| 2 | Ecological | GREEN — 196 scenarios, **10 debt** |
| 3 | Hardware | AMBER — 4 offline gates |
| 4 | Sovereignty | GREEN — Tower EXCEEDS WG, 6/6, CI LIVE |
| 5 | Public Surface | GREEN — 6/6 healthy |
| 6 | Compositions | GREEN — crypto composition migrating |
| 7 | Documentation | GREEN — fossil pass complete |
| 8 | Campus | GREEN — vision documented |

**Fossilized** (F1–F6): Glacial Shift, CAC, Silicon Atheism, Depot/Build, Cascade, Tower Deep Analysis.

---

*Wave 150x: Known debt 30→10. songBird CallerContext + UDS hardening resolved
7 pen scenarios. bearDog cipher floor + blake3 capability LIVE. songBird blake3
delegation wired. 653 shadow samples across 6 gates (10 hours continuous).
cellMembrane LAN registry + test extraction. Composition advancing. 196
scenarios PASS. 43/43 converged.*
