# ecoPrimals Ecosystem Blurb — Wave 150b

**Date**: Jul 18, 2026 10:00 EDT | **Wave**: 150b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 2 PRODUCTS LIVE.**

**This wave**: Full orthogonal dimensions review (12 dimensions, Wave 150a).
Dimensional sweep absorbed — 15 teams responded. Demand signal closures
catalogued. Blurb reshaped around live systems, strategic goals, and remaining
primal work. Closed items consolidated. Forward path clarified.

---

## 1. LIVE SYSTEMS — Current State

### footPrint → `primals.eco/footprint/` — **LIVE + FULLY USABLE**

Sovereign GIS home planner on sporeGate. Responsive, accessible, 466 tests,
all coverage thresholds passing. Known locations with descriptions, welcome
overlay, modal system, favicon. Full NUCLEUS composition wired through
songBird drawbridge.

**Remaining wiring** (non-blocking — product is usable without these):

| Wiring | Primal | Priority | What it enables |
|--------|--------|----------|-----------------|
| `PROJECTS_PATH` CAS | nestGate | P1 | Content-addressed project storage (currently filesystem) |
| `WS_PATH` agent bridge | petalTongue | P1 | Real-time AI agent via WebSocket (currently polling) |

### esotericWebb → `primals.eco/webb/` — **V18, LIVE ON GATE**

Cross-evolution CRPG on flockGate:8090. V18 with `demo` subcommand (8-step
guided tour, JSON CI output). 472 tests. 6/9 primals connected. Content
README for authors. Aldric NPC fixed.

**Blocking: ops persistence** — product runs but restarts require manual SSH.

| Ops step | Command | Gate | Status |
|----------|---------|------|--------|
| systemd enable | `systemctl enable --now esotericwebb-server` | flockGate | **PENDING** |
| Caddy route `/webb/` | Add reverse_proxy block → `flockGate:8090` | golgiBody | **PENDING** |

### Other live surfaces

| Surface | URL | Gate | Status |
|---------|-----|------|--------|
| sporePrint (docs) | `primals.eco` | golgiBody | LIVE — 302 pages, pseudoSpore gallery |
| petalTongue TOPO-VIS | `live.primals.eco` | sporeGate | LIVE |
| JupyterHub | `lab.primals.eco` | ironGate | LIVE |

---

## 2. PRIMAL DEMAND SIGNAL — Remaining Work

Items frontloaded by priority. Most Wave 149b P1 items are CLOSED.

### P1 — Inter-Primal Wiring (blocks deeper composition)

| Need | Owner | Consumer | Detail |
|------|-------|----------|--------|
| `PROJECTS_PATH` CAS wiring | nestGate | footPrint | Content-addressed project serving |
| `WS_PATH` agent bridge | petalTongue | footPrint | WebSocket for real-time agent comms |
| `null` params on health | squirrel | esotericWebb | Webb workaround: sends `{}` |
| BTSP → `gate.enroll` | songBird | cellMembrane | Last enrollment automation primitive |

### P2 — Ecosystem Quality + Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| HSM → Android Keystore | bearDog | grapheneGate mobile credential backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 completion |
| Health monitoring trait | ecosystem | Not procfs-hardcoded |
| `primal-transport` crate | ecosystem | Subsystem convergence publication |
| primalSpring CAC scenario | primalSpring | FRAGO issued, not implemented |
| primalSpring `wan-deploy` | primalSpring | 1/5 protoKarya scenarios remaining |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results for promotion |
| Fix groundSpring `bingoCube/nautilus` dep | groundSpring | `cargo test` fails |
| Add `scope.toml` to each spring | spring teams | Self-describing artifact manifest |
| Bash → Rust orchestration | spring teams | 114+ shell scripts across springs |

---

## 3. STRATEGIC GOALS

### NOW (this session / next cascade)

- **Make esotericWebb persistent**: systemd + Caddy on flockGate/golgiBody
- **Route remaining P1 wiring** to nestGate, petalTongue, squirrel, songBird
- **Validate sporePrint root** — confirm primals.eco Zola rebuild current

### NEAR TERM (next 2-4 weeks)

- **Full NUCLEUS composition**: all primals interacting through live products
- **nestGate CAS + petalTongue WS**: complete footPrint's backend composition
- **songBird BTSP**: fully automated mesh enrollment end-to-end
- **pseudoSpore validation**: promote 6 pending spores from PENDING → COMPLETE
- **sporePrint content sweep**: all entity maturity levels current
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090

### FUTURE (quarter horizon)

- **tideGlass composition**: computational chemistry product (Phase 0)
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **Exotic depot architectures**: riscv64, armv7, s390x (validated, not shipping)
- **DNSSEC + inner membrane separation**: sovereign DNS + primal.eco isolation
- **fieldGate recovery**: hardware surgery (dead CMOS)
- **biomeGate recovery**: kernel recovery

---

## 4. DIMENSIONAL SCORECARD (Wave 150a)

| Project | Tests | Clippy | Fmt | Debt | Unsafe | >800L | Prod unwrap |
|---------|-------|--------|-----|------|--------|-------|-------------|
| cellMembrane | 1,092 | 0 | 0 | 0 | 0 | 0 | 0 |
| esotericWebb | 472 | 0 | 0 | 0 | 0 | 0 | 0 |
| footPrint | 466 | 0 | — | 0 | — | 0 | — |
| songBird | 14,322 | swept | swept | 0 | 0 | swept | swept |
| lithoSpore | 227 | 0 | 0 | 0 | 0 | 0 | 0 |
| loamSpine | 1,702 | 0 | 0 | 0 | 0 | 0 | 0 |
| rhizoCrypt | 1,878 | 0 | 0 | 0 | 0 | 0 | 0 |
| nestGate | audit | 0 | 0 | 0 | 0 | audit | audit |
| primalSpring | 1,203 | 82 | 0 | 0 | 0 | 0 | 0 |
| sporePrint | 289 | — | — | 0 | — | 0 | — |

**Ecosystem**: 0 debt markers, 0 unsafe code, 0 mocks in production.

---

## 5. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | 145a |
| Content-Addressed Convergence (6/6) | 143b |
| Glacial Shift (8/8) ALL CLEAR | 137b |
| `gate.enroll` fully automated (7 phases) | 147a |
| lithoSpore ALL CLEAR (USB round-trip, ring dropped) | 150a |
| pseudoSpore pipeline: 7 springs emitted | 150a |
| footPrint LIVE + FULLY USABLE (466 tests, responsive, a11y) | 150a |
| esotericWebb V18 LIVE on flockGate (demo scenario) | 149a |
| E2E Tutorial Standard adopted (both products) | 149a |
| Dimensional review sweep (15 teams responded) | 150a |
| sweetGrass `braid.create/query` CONFIRMED | 150a |
| bearDog crypto JSON-RPC sigs CONFIRMED | 150a |
| GAP-036 + GAP-038 closed ecosystem-wide | 150a |
| songBird drawbridge + /jsonrpc + discovery | 148a |
| Depot operational (59+ binaries, 4 arch) | 142a |

---

## 6. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [LIVE]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [V18, persistence pending]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR]
  └─ northGate (10.13.37.8) — Windows, RTX 5090

Offline: westGate (cold storage), fieldGate (dead CMOS),
         strandGate (pending enrollment), biomeGate (kernel recovery)
```

| Port | Service | Gate | Protocol |
|------|---------|------|----------|
| 8080 | nestGate / petalTongue | sporeGate | HTTP (static + WS) |
| 8090 | footPrint | sporeGate | HTTP (API, behind drawbridge) |
| 8090 | esotericWebb | flockGate | HTTP (direct serve) |

---

## 7. ORTHOGONAL DIMENSIONS SUMMARY (12/12 reviewed)

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | — |
| 2 | Ecological | GREEN | — (dimensional sweep complete) |
| 3 | Hardware | AMBER | 4 gates offline (not blocking) |
| 4 | Sovereignty | GREEN | DNSSEC (P2) |
| 5 | Depot | GREEN | Exotic arch (P3) |
| 6 | Public Surface | AMBER | webb/ route pending, sporePrint root unconfirmed |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric (P3) |
| 8 | Compositions | AMBER | Webb persistence, nestGate CAS, petalTongue WS |
| 9 | Documentation | GREEN | — |
| 10 | Cascade | GREEN | songBird BTSP (P1) |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait, health trait (P2) |

---

*Wave 150b: Full 12-dimension orthogonal review. Blurb reshaped around live
systems and strategic goals. 2 products LIVE (footPrint fully usable, esotericWebb
persistence pending ops). Demand signal condensed — 4 P1 inter-primal wiring
items remain (nestGate CAS, petalTongue WS, squirrel null, songBird BTSP).
15 demand signal items closed in Wave 149b→150a sweep. lithoSpore ALL CLEAR +
7 pseudoSpores emitted. 12 dimensions: 9 GREEN, 3 AMBER (hardware offline gates,
public surface routing, composition wiring). Near-term: full NUCLEUS composition,
projectFOUNDATION design, strandGate enrollment.*
