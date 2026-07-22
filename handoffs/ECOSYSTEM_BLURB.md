# ecoPrimals Ecosystem Blurb — Wave 150v

**Date**: Jul 22, 2026 11:40 EDT | **Wave**: 150v | **From**: eastGate overwatch
**Posture**: **TOWER ATOMIC PARITY PIPELINE. 3/3 PRIMALS EVOLVED. GATES READY. TWO BLOCKERS.**

---

## 1. DEPLOYMENT CHAIN

```
User → Cloudflare DNS (*.primals.eco wildcard → golgiBody 157.230.3.183)
  → Caddy on golgiBody (TLS, Host-header routing)
    → WireGuard mesh → target gate → service
```

**Cloudflare**: DNS-only (grey cloud). Wildcard `*.primals.eco`. **DNSSEC 3/3** domains.
**Three-Domain Model**: `primals.eco` (intra) | `primal.eco` (inner) | `nestgate.io` (data)
**Git Relay**: Forgejo → push mirror → GitHub. 43/43 repos mirrored.

### Workspace Layout

| Org | Dir | Count |
|-----|-----|-------|
| ecoPrimals | `primals/` | 15 |
| sporeGarden | `gardens/` | 9 |
| syntheticChemistry | `springs/` | 10 |
| protoKarya | `protists/` | 2 |
| mixed | `infra/` | 7 |

---

## 2. RUNTIME

| Gate | Zone | Services | Status |
|------|------|----------|--------|
| **golgiBody** | VPS | Forgejo, Caddy, RustDesk relay, sporePrint, depot | **LIVE** |
| **sporeGate** | backbone | 13/13 NUCLEUS, footPrint, Tower 3/3, primalSpring | **LIVE** |
| **flockGate** | WAN | esotericWebb V22, Tower 3/3, primalSpring | **LIVE** |
| **grapheneGate** | mobile | Tower (bearDog + songBird + skunkBat) | **LIVE** |
| **eastGate** | backbone | Dev workstation, overwatch | **DEV** |
| **northGate** | house1 | RustDesk + WireGuard (.8) | **ENROLLED** |
| **ironGate** | house2 | 13/13 NUCLEUS, JupyterHub, GPU | **DOWN** (hw) |

**Surfaces**: 6/6 healthy (sporePrint, footPrint, TOPO-VIS, Forgejo, JupyterHub, esotericWebb).

---

## 3. REMAINING WORK — BY TEAM

### P0 — BLOCKERS (unblock Tower Atomic benchmark)

| # | Need | Owner | Detail |
|---|------|-------|--------|
| 1 | **Deploy TURN relay on golgiBody** | songBird (eastGate) + golgiBody ops | `songbird relay` code complete. Needs systemd unit on VPS. Unblocks WAN benchmark. |
| 2 | **Build benchmark harness** | songBird (eastGate) | `songbird benchmark --mode tower-atomic/wireguard --peer <gate>`. JSON output for primalSpring. Any tractable first solution. |

### P1 — Tower Atomic Parity

| # | Need | Owner | Detail |
|---|------|-------|--------|
| 3 | LAN parity benchmark | sporeGate + eastGate | sporeGate (.2) ↔ eastGate (.5), same backbone. **READY NOW** — blocked on #2 (harness). |
| 4 | WAN parity benchmark | sporeGate + flockGate | sporeGate (.2) → golgiBody TURN (.1) → flockGate (.6). Blocked on #1 + #2. |
| 5 | Live-tier scenario | primalSpring (eastGate) | `s_tower_atomic_parity_live` — ships after benchmark results. Structural (21/21) already GREEN. |
| 6 | WAN latency target | primalSpring (eastGate) | WG=68ms on 2-hop. Redefine as "Tower ≤ WG * 1.5x" not absolute <50ms. |

**Parity philosophy**: Initial goal is WireGuard parity — any tractable first solution.
WG has years of dev time on us. We match first, then evolve past. Parity is the floor,
not the ceiling. Targets are relative to WG baseline, not absolute.

### P1 — Sovereignty Pipeline

| # | Need | Owner | Detail |
|---|------|-------|--------|
| 7 | sporePrint primal pipeline | sporePrint (flockGate) | Zola replacement: petalTongue + nestGate CAS + cellMembrane. Lansing Scuffle pages first. |
| 8 | Deploy petalTongue v1.7+ | sporeGate ops | Binary in depot. Activates Webb scene graph + WASM WebGL. |
| 9 | Android Keystore + grapheneGate test | bearDog (southGate) | CredentialStore backend for TEE/StrongBox. bearDog evolved backend (150v). |
| 10 | CredentialStore integration | squirrel (eastGate) | `secrets.*` JSON-RPC. Handoff issued. bearDog shipped trait + FileVault. |

### P1 — Gate Enrollment (Operator)

| # | Need | Owner | Detail |
|---|------|-------|--------|
| 11 | southGate USB enrollment | operator (eastGate) | USB staged, .9 allocated. Plug in and bootstrap. |
| 12 | strandGate enrollment | operator (eastGate) | Dual EPYC 7452, 256GB RAM, RTX 3090. Pending physical access. |

### P2 — Evolution

| # | Need | Owner | Detail |
|---|------|-------|--------|
| 13 | Promote 6 pseudoSpores | lithoSpore (strandGate) | Validation Data Stream v1.0 standard defined. |
| 14 | bingoCube WASM WebGL widget | bingoCube (eastGate) | Unblocked by petalTongue 150r. `render_color_grid_webgl` ready. |
| 15 | footPrint declarative source registry | footPrint (flockGate) | DATA_LAYER_PRIMAL_ABSTRACTION spec committed. |
| 16 | `.unwrap()` clippy audit — remaining primals | all teams | `cargo clippy -- -W clippy::unwrap_used`. 5 primals confirmed 0. |

### P3 / FUTURE

| # | Need | Owner | Detail |
|---|------|-------|--------|
| 17 | pseudoSpore Explorer | esotericWebb (ironGate) | Interactive visualization of pseudoSpore structures. Concept. |
| 18 | rootPulse design | ecosystem | Sovereign VCS over nestGate CAS + Provenance Trio. Forgejo replacement. |
| 19 | sporePrint pipeline design | ecosystem | Full Zola replacement architecture. |
| 20 | SHOW_HN readiness | ecosystem | Rubric, narrative, demo path. |

---

## 4. SOVEREIGNTY EVOLUTION

| Tier | Tool | Primal Path | Status |
|------|------|-------------|--------|
| **REPLACE** | WireGuard | Tower Atomic (bearDog + songBird + skunkBat) | Gates READY. Blockers: TURN relay + harness. |
| **REPLACE** | Zola | petalTongue + nestGate CAS + cellMembrane | WASM WebGL shipped. Pipeline design pending. |
| **LATE-STAGE** | Forgejo | rootPulse (nestGate CAS + Provenance Trio) | Post-rootPulse. |
| **FIREBREAK** | Cloudflare / Caddy / RustDesk / JupyterHub | Outer membrane | Stays. |

---

## 5. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS [TURN relay needed]
  ├─ sporeGate (10.13.37.2) — builder, Tower 3/3 [BENCHMARK PEER]
  ├─ eastGate  (10.13.37.5) — orchestrator, dev [LAN BENCHMARK PEER]
  ├─ flockGate (10.13.37.6) — esotericWebb V22, Tower 3/3 [WAN PEER]
  ├─ ironGate  (10.13.37.7) — compute, GPU [DOWN — hw offline]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Pending: southGate (.9), strandGate (pending)
Offline: westGate, fieldGate, biomeGate
```

**WG IP allocation**: .1=golgi, .2=spore, .5=east, .6=flock, .7=iron, .8=north, .9=south. Available: .3, .4, .10+

---

## 6. WHAT'S DONE (fossilized)

| Achievement | Wave |
|-------------|------|
| Tower primals deep debt (enrollment.verify, crypto bench, bond-type cipher, relay refactor) | 150v |
| Gate AARs GREEN/READY, structural 21/21, WG baselines, cellMembrane unwrap resolved | 150v |
| Cascade convergence, vendor eliminated, credential store, Tower parity spec | 150u |
| Standards reorganized (4 dirs), DNSSEC 3/3, Sovereignty roadmap | 150s-t |
| petalTongue WASM WebGL, nestGate vendor analysis, full dimensional review | 150o-r |
| USB enrollment, workspace reorg, Forgejo-first 43/43, push mirrors | 150j-n |
| Scene unification, NUCLEUS wired, Silicon Atheism P2, CAC 6/6, Glacial Shift 8/8, Depot | ≤150i |

---

## 7. DIMENSIONS

| Dim | Area | Status |
|-----|------|--------|
| 1 Temporal | GREEN | wave.toml current |
| 2 Ecological | GREEN | 0 project TODOs (15/15 primals) |
| 3 Hardware | AMBER | ironGate down, southGate + strandGate pending |
| 4 Sovereignty | GREEN | DNSSEC 3/3, Tower parity pipeline active |
| 5 Surfaces | GREEN | 6/6 healthy |
| 6 Compositions | GREEN | pseudoSpore pipeline maturing |
| 7 Documentation | GREEN | Standards reorganized, handoffs current |
| 8 Campus | GREEN | Lansing Scuffle documented |

**Fossilized**: Glacial Shift (137b), CAC (143b), Silicon Atheism (145a), Depot (150n), Cascade (150k).
**Summary**: 7 GREEN / 1 AMBER (hardware) + 5 fossilized.

---

*Wave 150v: Tower Atomic parity pipeline active. All 3 primals evolved (bearDog enrollment.verify
+ crypto bench, skunkBat bond-type cipher, songBird relay refactor). Gates GREEN/READY. Two
blockers: golgiBody TURN relay (P0), benchmark harness (P1). LAN benchmark sporeGate↔eastGate
READY NOW. Parity first, exceed later. 43/43 converged.*
