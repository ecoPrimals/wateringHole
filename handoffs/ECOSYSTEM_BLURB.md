# ecoPrimals Ecosystem Blurb — Wave 162 Mesh Wake (Oct 5, 2026)

**Date**: Oct 5, 2026 10:15 | **Wave**: 162 | **From**: overwatch (eastGate)
**Posture**: **MESH WAKE.** eastGate + golgiBody + sporeGate ONLINE. northGate ALIVE (WG). songbird federation: sporeGate ↔ golgiBody OK, eastGate local OK, cross-gate protocol mismatch (sporeGate sends legacy riboCipher). **sporePrint DOWN** (Zola build permission — P1 fix). detroit + gorilla + live + nestgate.io + footprint + lab all serving. **Windows 16/16 compile** (depot rebuild pending). **8 architecture families.** sporeGate ran lead Waves 159–161: observatory, receptor, signal depth, DAG orthogonalization, golgiBody fossilization (65%→49% disk), pen test, Wayback seeding. House 2 gates all OFFLINE — physical power-on needed.

---

## What Changed (Waves 159–162 — Sep 28 – Oct 5)

### sporeGate Lead Session (Waves 159–162)

sporeGate ran autonomously for a week while eastGate was focused on custody/racketeering work:

| Wave | What sporeGate Shipped |
|------|----------------------|
| 159 | cascade.notify gossip event, gate.pull --mesh path |
| 160 | DAG orthogonalization, ownership cycle fix, event-driven relay, GitHub mirror |
| 160.5 | **LuxR receptor** — Caddy log analytics without surveillance (quorum sensing model) |
| 161 | Observatory page on sporePrint, receptor snapshot pipeline, dual signal log |
| 161b | Evidence depot symlinks, skunkBat anomaly detection signal feed |
| 162 | Signal depth + correlation metadata, behavioral classification, visitor classification |

### New Capabilities Built by sporeGate

- **Observatory** (`/observatory/` on sporePrint) — live receptor data visualization. No cookies, no tracking pixels, pure server-side log analysis. 5 visitor classes: human, search bot, AI bot, social bot, other bot.
- **Signal Log** (`/var/log/membrane/signal.jsonl`) — dual LuxI (outbound publish events) + LuxR (inbound receptor snapshots) for skunkBat anomaly detection.
- **Behavioral Classification** — probe path detection, velocity checks, UA fingerprinting. Extracted to `cellmembrane-types` for `skunky-ingest`.
- **golgiBody Fossilization** — 65% → 49% disk. Removed stale plasmidBin targets, venvs, source repos. Runtime-only remains.
- **Pen Test** — 13 vuln scanner probes rejected (403). Security headers verified. Server header hidden.
- **Wayback Machine** — 14/15 key detroit pages archived.
- **Reddit Repeater Drafts** — 6 subreddit posts drafted (r/Detroit, r/CharterSchools, r/DataHoarder, etc.)

### Key Finding: Domain A Overloaded

golgiBody hosts both the live sites AND Forgejo on one VPS — single failure domain kills the 2 most important surfaces. **Recommendation**: migrate Forgejo to LAN (sporeGate or blueGate). golgiBody becomes thin relay only.

### Deployment Failure Taxonomy (AAR)

13 failures cataloged across fossilization session, 4 pattern classes identified:
1. **Resource exhaustion** — unbounded operations on bounded hosts
2. **Dependency chain breakage** — cleanup destroying runtime dependencies
3. **State outliving context** — stale PIDs, routes, binaries, worktrees
4. **Protocol mismatch** — riboCipher version skew between nodes

8 resilience abstractions proposed. Key insight: "The organism's biggest weakness is that components assume their environment hasn't changed since they last checked."

---

## Gate Status (Wave 162)

| Gate | WG IP | Status | Last Handshake | Notes |
|------|-------|--------|----------------|-------|
| **eastGate** | .5 | ✅ ONLINE | seconds | 10G SFP+, overwatch, songbird :7700 OK |
| **golgiBody** | .1 | ✅ ONLINE (HUB) | — | VPS relay, 11 peers configured |
| **sporeGate** | .2 | ✅ ONLINE | seconds | Inner membrane, songbird federated to golgi |
| **northGate** | .8 | ✅ ALIVE | 40 sec | Windows 11, RTX 5090 |
| **biomeGate** | .3 | ⏸️ stale | 52 days | House 1 — needs power |
| **graftGate** | .13 | ⏸️ stale | 49 days | House 1 — needs power |
| **flockGate** | .6 | ⏸️ stale | 68 days | Remote (WAN only) |
| **ironGate** | .7 | ⏸️ stale | 49 days | House 2 — needs power |
| **strandGate** | .10 | ⏸️ stale | 44 days | House 2 — needs power |
| **blueGate** | .12 | ⏸️ stale | 49 days | House 2 — needs power |
| **southGate** | .9 | ❌ NEVER | — | House 2 — needs power + WG config |
| **westGate** | .11 | ❌ NEVER | — | House 2 — needs power + WG config |

---

## Live Sites (Oct 5)

| Site | Status | URLs | Notes |
|------|--------|------|-------|
| **detroit.primals.eco** | ✅ 200 | 127+ | Evidence pipeline LIVE. Pen tested. Wayback seeded. |
| **gorilla.primals.eco** | ✅ 200 | 20 | Methodology — fEAR, preSCENT, STRIDe, amicusContra |
| **live.primals.eco** | ✅ 200 | — | Via sporeGate :8190 |
| **nestgate.io** | ✅ 200 | — | Via sporeGate :8190 |
| **footprint.primals.eco** | ✅ 200 | — | Rerouted to sporeGate :8090 (was dead ironGate) |
| **lab.primals.eco** | ✅ 401 | — | Auth required |
| **sporeprint.primals.eco** | ❌ 404 | 403 | **DOWN — Zola build permission error. P1 fix needed.** |

---

## Teams — Wave 162

| Role | Authority | What They Do |
|------|-----------|-------------|
| **Code** | eastGate (overwatch) | All 16 primals. Architecture. Cross-compile. |
| **Ops** | sporeGate | Cascade, depot, builds, sites, receptor, observatory. |
| **Relay** | golgiBody (cloud) | Forgejo, Caddy, depot, WG hub. Thin relay target. |
| **Content** | publicRecord team | detroit + guerillaGorilla. OSINT. Evidence pipeline. |
| **Validators** | Gate teams (on rewake) | Pull, build, validate, report. |

---

## Active Tracks — Wave 162

| # | Track | Owner | Status |
|---|-------|-------|--------|
| 1 | **sporePrint build fix** | golgiBody / sporeGate | ❌ P1 — Zola permission error, site DOWN |
| 2 | **eastGate songbird federation** | eastGate | ✅ Running — protocol mismatch with sporeGate (legacy riboCipher) |
| 3 | **House 2 power wake** | physical | ⏸️ westGate → ironGate → strandGate → blueGate |
| 4 | **northGate primal bootstrap** | sporeGate + northGate | 🔄 WG alive, depot pull pending |
| 5 | **Windows depot rebuild** | sporeGate | ⏸️ 16/16 compile, needs cargo build + sync |
| 6 | **cellMembrane signal depth** | sporeGate | 🔄 Wave 162 — multi-file receptor, outreach events, session detection |
| 7 | **Forgejo → LAN migration** | sporeGate | ⏸️ Biggest redundancy win (splits domain A) |
| 8 | **detroit content evolution** | publicRecord team | 🔄 OSINT, FOIA, dynasty expansion |
| 9 | **House 1 power** | physical | ⏸️ biomeGate + graftGate |
| 10 | **arXiv Rung 1** | eastGate | ⏸️ Needs strandGate |

---

## CONVERGENCE RULE

> **Mesh Wake.** eastGate + golgiBody + sporeGate ONLINE. northGate WG ALIVE.
> sporeGate ran lead Waves 159–162: observatory, receptor, signal depth, golgi fossilization.
> sporePrint DOWN (P1 — Zola build permission). detroit + gorilla + 4 more sites serving.
> Windows 16/16 compile. Depot rebuild pending.
> 13 deployment failures cataloged, 4 pattern classes, 8 resilience abstractions.
> House 2 gates need physical power-on. Wake order: westGate → ironGate → strandGate → blueGate.
> eastGate songbird running, cross-gate federation needs sporeGate binary update.
> October: mesh wake, sporePrint fix, House 2 power, Forgejo LAN migration.
> *"Beside the small. Against unaccountable power. For the record."*

---

**See also**: [`HARDWARE.md`](../HARDWARE.md) | [`MESH_WAKE_WAVE161_EASTGATE_OVERWATCH.md`](MESH_WAKE_WAVE161_EASTGATE_OVERWATCH.md)

*Wave 162 mesh wake. 3 gates + golgiBody + northGate ALIVE. sporeGate ran lead (observatory, receptor, signal depth, fossilization, pen test). sporePrint DOWN (P1). detroit serving, pen tested, Wayback seeded. 16/16 Windows compile. House 2 needs power. Wake order: westGate → ironGate → strandGate → blueGate.*
