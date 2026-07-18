# ecoPrimals Ecosystem Blurb — Wave 149a

**Date**: Jul 18, 2026 08:40 EDT | **Wave**: 149a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 2 PRODUCTS LIVE. E2E STANDARD ADOPTED.**

**This cascade**: Both product teams responded to the E2E Tutorial Standard.
footPrint shipped known locations + picker UI + URL hash deep-linking (275 tests,
`5f449df`). esotericWebb shipped V18 — `esotericwebb demo` subcommand with YAML-driven
guided tour (8 steps, 6/9 primals exercised, JSON output for CI). songBird fixed
mutex poison cascade in persistence tests. sporePrint added `live` maturity level
(green badge, 302 pages, 79 entities). primalSpring KNOWN_DEBT calibrated to 1.
4 handoffs fossilized.

---

## Upstream Primal Demand Signal

Accumulated needs from all downstream consumers. Each primal team: address
your rows. This section grows as gardens evolve — that's the point.

### esotericWebb team (OPS — 2 remaining)

| Need | Consumer(s) | Priority | Detail |
|------|-------------|----------|--------|
| systemd persistence on flockGate | sporeGate ops | P1 | cellMembrane unit FIXED (`33aa33a`). Deploy: `systemctl enable --now esotericwebb-server`. |
| Caddy route `/webb/` on golgiBody | sporeGate ops | P1 | Caddy config FIXED. Route `/webb/` → `flockGate:8090`. |

### songBird (3 CLOSED, 1 open)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| ~~`PROXY_PATH` drawbridge~~ | footPrint | — | **CLOSED** |
| ~~`/jsonrpc` endpoint~~ | esotericWebb | — | **CLOSED** |
| ~~Discovery schemas~~ | esotericWebb | — | **CLOSED** |
| BTSP → cellMembrane `gate.enroll` | enrollment | P1 | Pending |

### squirrel

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Accept `null` params on health | esotericWebb | P1 | Open |

### nestGate

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `PROJECTS_PATH` CAS wiring | footPrint | P1 | Open |

### petalTongue

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| `WS_PATH` agent bridge | footPrint | P1 | Open |

### bearDog

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Confirm crypto JSON-RPC sigs | esotericWebb | P1 | Open |
| HSM → Android Keystore | grapheneGate | P2 | Open |

### sweetGrass

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| Confirm `braid.create/query` | esotericWebb | P1 | Open |

### biomeOS

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| GAP-017: neural-api resurrection | esotericWebb | P2 | Open |
| GAP-018: executors not exposed | esotericWebb | P2 | Open |

### ALL primals (ecosystem convention)

| Need | Consumer(s) | Priority | Status |
|------|-------------|----------|--------|
| GAP-036: Socket naming convention | esotericWebb | P2 | Open |
| GAP-038: Stale UDS socket cleanup | esotericWebb | P2 | Open |

---

## Path to Live — Downstream Projects

### footPrint → `primals.eco/footprint/` — **LIVE + E2E TUTORIAL SHIPPED**

Full path wired. Known locations picker + URL hash deep-linking shipped.
5 locations: MSU Campus, Downtown EL, Red Cedar River, Meridian Twp, Haslett Ag.
**Next**: nestGate CAS wiring (P1), petalTongue WS bridge (P1).

### esotericWebb → `primals.eco/webb/` — **V18, LIVE ON GATE, E2E DEMO SHIPPED**

V18, 472 tests, 6/9 primals connected, flockGate:8090. `esotericwebb demo`
subcommand ships 8-step guided tour with verification. Deploy artifacts FIXED.

| Step | Status | Owner |
|------|--------|-------|
| 1-6. Binary, Caddy unit, songBird, composition, Forgejo | **ALL DONE** | — |
| 7. systemd enable on flockGate | **PENDING** | sporeGate ops |
| 8. Caddy route on golgiBody | **PENDING** | sporeGate ops |
| 9. E2E demo scenario | **SHIPPED** (V18, `18b8169`) | esotericWebb |

### lithoSpore → CLI tool — **PIPELINE PROVEN, DEEP DEBT CLEAR**

| Step | Status |
|------|--------|
| 1-5. Platform trait, pack/unpack, initioChem, deep debt | **ALL DONE** (222 tests) |
| 6. USB round-trip validation | NOT STARTED |

### projectFOUNDATION → TBD (NOT STARTED)

---

## Ecosystem Test Health

| Project | Tests | Clippy | Debt |
|---------|-------|--------|------|
| cellMembrane | 1,100 | 0 | 0 |
| esotericWebb | 472 | 0 | 0 |
| songBird | full pass | 0 | 0 |
| footPrint | 275 | clean | 0 |
| lithoSpore | 222 | 0 | 0 |
| sporePrint | 289 | 0 | 0 |
| primalSpring | 1,203 | 0 | 1 |

---

## Completed Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | **COMPLETE** |
| Content-Addressed Convergence (6/6) | **COMPLETE** |
| Glacial Shift (8/8) | **ALL CLEAR** |
| `gate.enroll` fully automated (7 phases) | **SHIPPED** |
| lithoSpore pack/unpack + initioChem | **SHIPPED** |
| **footPrint LIVE** | **LIVE** — sovereign mesh + known locations E2E |
| **esotericWebb LIVE on flockGate** | **V18** — 6/9 primals, demo scenario shipped |
| **E2E Tutorial Standard adopted** | **SHIPPED** — both products compliant |
| songBird drawbridge + /jsonrpc + discovery | **SHIPPED** |
| sporePrint `live` maturity level | **SHIPPED** — green badge, 302 pages |
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
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [pipeline proven]
  └─ northGate (10.13.37.8) — Windows, RTX 5090
```

---

*Wave 149a: E2E Tutorial Standard fully adopted — both live products compliant.
footPrint shipped known locations + picker + hash deep-linking (5f449df, 275 tests).
esotericWebb shipped V18 with `demo` subcommand — 8-step guided tour, JSON CI output,
exercises 6/9 primals (18b8169). songBird fixed mutex poison cascade (f0025ee6).
sporePrint added `live` maturity level (351c6cd). primalSpring KNOWN_DEBT → 1.
4 handoffs fossilized. Remaining: ops persistence (systemd + Caddy) for esotericWebb,
then primal-level demand signal items (nestGate CAS, petalTongue WS, squirrel null,
bearDog sigs, sweetGrass braids).*
