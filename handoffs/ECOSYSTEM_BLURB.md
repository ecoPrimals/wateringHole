# ecoPrimals Ecosystem Blurb — Wave 150a

**Date**: Jul 18, 2026 09:55 EDT | **Wave**: 150a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 2 PRODUCTS LIVE. DIMENSIONAL SWEEP COMPLETE.**

**This cascade**: Massive team response to dimensional review. 15 repos pulled,
6 handoffs absorbed and fossilized. Key closures:
- **sweetGrass**: `braid.create/query` CONFIRMED (P1 closed)
- **bearDog**: crypto JSON-RPC sigs CONFIRMED (P1 closed)
- **footPrint**: responsive design, accessibility, ESLint zero, 466 tests, favicon,
  modals, welcome overlay, picker descriptions — ALL shipped (P1+P2+P3 closed)
- **esotericWebb**: aldric NPC fixed, cargo fmt, content README added (P1 closed)
- **songBird**: prod unwrap elimination, file splits, clippy sweep (177 files, P1 closed)
- **lithoSpore**: clippy clean, USB round-trip DONE, ring dropped, pseudoSpore
  emission from all 7 springs (P1+P2 closed, ALL CLEAR)
- **primalSpring**: fmt 54→0, unwrap 4→0, clippy 456→82 (P2 closed)
- **cellMembrane**: fmt 62→0 (P2 closed)
- **rhizoCrypt**: deprecation purge, dead code removal, arch splits, GAP-036+038
  CLOSED, 1,878 tests, 93.83% coverage
- **loamSpine**: dimensional self-audit ALL PASS, 1,702 tests
- **nestGate**: dimensional audit, fmt 133 files, GAP-038 socket liveness
- **biomeOS**: GAP-017/018/036/038 ALL RESOLVED
- **barraCuda, coralReef, skunkBat, toadStool**: dimensional cleanups

---

## Upstream Primal Demand Signal

Items remaining after this wave. Most P1 items from Wave 149b are now CLOSED.

### esotericWebb (OPS — 2 remaining)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| systemd persistence on flockGate | sporeGate ops | P1 | cellMembrane unit FIXED. Deploy: `systemctl enable --now esotericwebb-server`. |
| Caddy route `/webb/` on golgiBody | sporeGate ops | P1 | Route `/webb/` → `flockGate:8090`. |

### songBird (1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | Pending |

### squirrel (1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Accept `null` params on health | esotericWebb | P1 | Open (Webb works around with `{}`) |

### nestGate (1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | footPrint | P1 | Open |

### petalTongue (1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | footPrint | P1 | Open |

### bearDog (1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| HSM → Android Keystore | grapheneGate | P2 | Open |

### Spring teams (pseudoSpore follow-up)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| Populate `validation.json` per spore | lithoSpore pipeline | P2 | 6 PENDING spores need module validation results |
| Fix groundSpring `bingoCube/nautilus` dep | lithoSpore | P2 | `cargo test` fails on missing path dependency |
| Add `scope.toml` to each spring | lithoSpore convention | P2 | Self-describing artifact manifest |

---

## Demand Signal Closures (Wave 149b→150a)

| Item | Team | Status |
|------|------|--------|
| ~~sweetGrass `braid.create/query`~~ | sweetGrass | **CONFIRMED** — 107 braid tests |
| ~~bearDog crypto JSON-RPC sigs~~ | bearDog | **CONFIRMED** — stable since 142a |
| ~~footPrint responsive/a11y/ESLint~~ | footPrint | **ALL SHIPPED** — 466 tests |
| ~~footPrint coverage below thresholds~~ | footPrint | **CLOSED** — all thresholds passing |
| ~~footPrint favicon + modals + welcome~~ | footPrint | **SHIPPED** |
| ~~esotericWebb aldric NPC bug~~ | esotericWebb | **FIXED** — `c4c35dc` |
| ~~esotericWebb cargo fmt~~ | esotericWebb | **DONE** |
| ~~songBird 556 clippy + 81 unwrap + oversized~~ | songBird | **SWEPT** — 177 files |
| ~~cellMembrane cargo fmt~~ | cellMembrane | **DONE** — 62 files |
| ~~primalSpring fmt + unwrap + clippy~~ | primalSpring | **DONE** — 54→0, 4→0, 456→82 |
| ~~lithoSpore 308 clippy~~ | lithoSpore | **CLEAN** — 0 warnings |
| ~~lithoSpore USB round-trip~~ | lithoSpore | **DONE** — 6-step deploy-test |
| ~~biomeOS GAP-017/018~~ | biomeOS | **RESOLVED** |
| ~~GAP-036 socket naming~~ | sweetGrass, rhizoCrypt, loamSpine, biomeOS, nestGate | **CLOSED** ecosystem-wide |
| ~~GAP-038 stale UDS cleanup~~ | sweetGrass, rhizoCrypt, loamSpine, biomeOS, nestGate | **CLOSED** ecosystem-wide |
| ~~sporePrint esotericWebb.md metadata~~ | sporePrint | Pending confirmation |

---

## Dimensional Scorecard (Wave 150a — Post-Sweep)

| Project | Clippy | Fmt | Debt | Unsafe | >800L | Tests | Prod unwrap |
|---------|--------|-----|------|--------|-------|-------|-------------|
| cellMembrane | 0 | **0** | 0 | 0 | 0 | 1,092 | 0 |
| esotericWebb | 0 | **0** | 0 | 0 | 0 | 472 | 0 |
| footPrint | **0** | — | 0 | — | 0 | **466** | — |
| songBird | swept | swept | 0 | 0 | swept | 14,322 | **swept** |
| lithoSpore | **0** | 0 | 0 | 0 | 0 | **227** | 0 |
| loamSpine | 0 | 0 | 0 | 0 | 0 | **1,702** | 0 |
| rhizoCrypt | 0 | 0 | 0 | 0 | 0 | **1,878** | 0 |
| nestGate | audit | **0** | 0 | 0 | audit | audit | audit |
| sporePrint | — | — | 0 | — | 0 | 289 | — |
| primalSpring | **82** | **0** | 0 | 0 | 0 | 1,203 | **0** |
| biomeOS | gaps resolved | — | 0 | 0 | — | — | — |

---

## Path to Live — Downstream Projects

### footPrint → `primals.eco/footprint/` — **LIVE + FULLY USABLE**

Responsive design, accessibility, welcome overlay, known locations with descriptions,
favicon, modal system — all shipped. 466 tests, all coverage thresholds passing.
**Next**: nestGate CAS wiring (P1), petalTongue WS bridge (P1).

### esotericWebb → `primals.eco/webb/` — **V18, LIVE ON GATE, PERSISTENCE PENDING**

Aldric NPC fixed. Content README added. Demo scenario fully validated.

| Step | Status | Owner |
|------|--------|-------|
| 1-6. Binary, Caddy unit, songBird, composition, Forgejo | **ALL DONE** | — |
| 7. systemd enable on flockGate | **PENDING** | sporeGate ops |
| 8. Caddy route on golgiBody | **PENDING** | sporeGate ops |
| 9. E2E demo scenario | **SHIPPED + FIXED** (V18) | — |

### lithoSpore → CLI tool — **ALL CLEAR**

All 7 steps complete + ring dropped + clippy clean. USB round-trip validated.
pseudoSpore emission from all 7 springs shipped. 227 tests, 0 everything.

### pseudoSpore Pipeline — **7 SPRINGS EMITTED**

| Spring | Artifact | Status |
|--------|----------|--------|
| hotSpring | CompChem-GuideStone v1.6.1 | COMPLETE |
| groundSpring | LTEE-Measurement v1.0.0 | PENDING validation |
| airSpring | Agricultural-Meteorology v1.0.0 | PENDING validation |
| healthSpring | Clinical-PKPD v1.0.0 | PENDING validation |
| neuralSpring | ML-Surrogates v1.0.0 | PENDING validation |
| wetSpring | Life-Science-Analytics v1.0.0 | PENDING validation |
| ludoSpring | Game-Science v1.0.0 | PENDING validation |

### projectFOUNDATION → TBD (NOT STARTED)

---

## Completed Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** |
| **lithoSpore ALL CLEAR** | **DONE** — USB round-trip, ring dropped, 227 tests |
| **pseudoSpore pipeline: 7 springs emitted** | **SHIPPED** |
| **footPrint LIVE + FULLY USABLE** | **LIVE** — responsive, a11y, 466 tests |
| **esotericWebb V18 LIVE on flockGate** | **LIVE** — demo fixed, persistence pending |
| **E2E Tutorial Standard adopted** | **SHIPPED** — both products compliant |
| **Dimensional review sweep** | **COMPLETE** — 15 teams responded |
| **sweetGrass braids CONFIRMED** | **CLOSED** — braid.create/query stable |
| **bearDog crypto sigs CONFIRMED** | **CLOSED** — Ed25519 + HMAC stable |
| **GAP-036 + GAP-038 ecosystem-wide** | **CLOSED** — socket naming + stale cleanup |
| songBird drawbridge + /jsonrpc + discovery | **SHIPPED** |
| sporePrint `live` maturity level | **SHIPPED** — 302 pages |
| Depot (59+ binaries, 4 arch) | **OPERATIONAL** |

---

## Canonical Port Map

| Port | Service | Gate | Protocol |
|------|---------|------|----------|
| 8080 | nestGate / petalTongue | sporeGate | HTTP (static + WS) |
| 8090 | footPrint | sporeGate | HTTP (API, behind drawbridge) |
| 8090 | esotericWebb | flockGate | HTTP (direct serve) |

---

## 6-Gate Mesh (LIVE)

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [LIVE]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [V18, persistence pending]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

*Wave 150a: Massive dimensional sweep response. 15 repos absorbed, 6 handoffs
fossilized. sweetGrass braids + bearDog crypto sigs CONFIRMED (2 P1 closures).
footPrint shipped responsive + a11y + ESLint zero + 466 tests + full UX polish.
esotericWebb aldric NPC fixed. songBird swept 177 files. lithoSpore ALL CLEAR +
pseudoSpore emission from all 7 springs. GAP-036 + GAP-038 closed ecosystem-wide
(sweetGrass, rhizoCrypt, loamSpine, biomeOS, nestGate). primalSpring fmt+unwrap
clean. rhizoCrypt: 1,878 tests, 93.83% coverage. loamSpine: 1,702 tests, all
dimensions PASS. Remaining: ops persistence for esotericWebb, nestGate CAS,
petalTongue WS, squirrel null, songBird BTSP.*
