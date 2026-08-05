# ecoPrimals Ecosystem Blurb — Signal Dispatch + Federation Era

**Date**: Aug 5, 2026 AM | **Wave**: 156d | **From**: eastGate overwatch
**Posture**: **P0/P1/P2: ZERO. ALL 6 NUCLEUS GATES v4.57+. G18 SIGNAL DISPATCH LIVE (ironGate, 9 providers). ironGate NUCLEUS storage LIVE (12.7 TB CAS, songBird federation to westGate configured). Convoy provenance at 145/s (460x total improvement). 16⁴ DUAL-GPU DATA COMPLETE (cross-vendor parity: 6 ppm at β=6.2, +0.01% vs published at β=6.0). tideGlass 214 tests, 17 IPC methods. Reviewer rubric shipped (42 items). ~135K+ tests, 13/13 GREEN. nestgate.io NEURAL API WIRED (20 primals, capability maps live).**

---

## GATE FLEET STATUS — POST-SYNC

| Gate | NUCLEUS | Depot | Status |
|------|---------|-------|--------|
| **sporeGate** | **14/14 v4.57+** | **BUILD AUTHORITY — FRESH** | Sovereign CI. 52/52 harvest complete. LAN-first Tower (4 local, 1ms). nestgate.io Neural API wired (20 primals). |
| **ironGate** | **10/10 v4.57+** | **CURRENT** | G18 DISPATCH LIVE (9 providers). NUCLEUS storage 12.7 TB CAS. songBird federation to westGate. 708 tests. |
| **westGate** | **14/14 v4.57** | **SOURCE-BUILT** | GPS data converted. Convergence sweep complete. `nucleus attach` ready. Convoy at 145/s (452 GB CAS). |
| **strandGate** | **v4.57+ (restart deferred)** | **CURRENT** | GPU at 100% QCD production. 16⁴ dual-GPU data COMPLETE. |
| **blueGate** | **14/14 v4.57+** | **CURRENT** | Depot sync done. UniBin CLI migration documented. |
| **southGate** | **13/13 v4.57+** | **CURRENT** | Re-validated after 97h uptime. Tower 0.15ms avg, 19 Gbps. |
| **biomeGate** | Source-built compute | — | GPU lab. Not full NUCLEUS. |
| **golgi** | Thin relay | **Caddy CLEANED** | 14 routes. footprint.primals.eco LIVE. Deprecated directives removed. |
| **northGate** | — | — | Daily driver. Skip. |
| **grapheneGate** | Tower | — | Mobile. Skip. |
| **eastGate** | — | — | Overwatch. Skip. |

---

## WHAT SPOREGATE EXECUTED THIS SESSION

| Item | Before | After |
|------|--------|-------|
| **nestgate.io Neural API bridge** | Dashboard "Loading..." for all dynamic sections. petalTongue couldn't find Neural API socket. | **20 primals discovered. Capability maps live.** Symlinked `neural-api-e8b62b6e.sock` to biomeOS discovery path. Persisted in systemd drop-in. |
| **webb.primals.eco 502 investigation** | Blurb reported 502. | GET returns 200 (serves HTML). HEAD returns 502 — esotericWebb HTTP handler bug, not routing. No golgi action needed. |
| **golgi Caddy cleanup** | Deprecated `basicauth` directive. Unnecessary `header_up X-Forwarded-For/Proto` (Caddy does this by default). | Migrated to `basic_auth`. Removed redundant headers. Formatted. Clean reload. |
| **petalTongue service** | Missing `DISCOVERY_SOCKET` and `FAMILY_ID` env vars. Heartbeat failing (attempt 40+, backoff 1920s). | Added `DISCOVERY_SOCKET=/run/membrane/biomeos-api-e8b62b6e.sock` and `FAMILY_ID=e8b62b6e` to systemd user unit. Neural API bridge functional. |

---

## LIVE SITE ASSESSMENT — UPDATED

| Site | URL | Status | Detail |
|------|-----|--------|--------|
| **sporePrint** | `sporeprint.primals.eco` | **LIVE, 200** | Zola static site. Science content. |
| **footPrint** | `footprint.primals.eco` | **LIVE, 200** | CAS works. Map empty — needs squirrel + petal WebSocket wiring (ironGate team). |
| **nestgate.io** | `nestgate.io` | **LIVE, 200 — NEURAL API WIRED** | Dashboard shows 20 primals, capability maps, topology. Gate mesh still shows "Not Found" (WG conf query needed). |
| **esotericWebb** | `webb.primals.eco` | **GET 200 / HEAD 502** | HEAD bug in esotericWebb HTTP handler. GET works. Upstream fix needed. |

---

## K-DERM THREE-DOMAIN TOPOLOGY — FULLY OPERATIONAL

| Layer | Domain | DNS | Status |
|-------|--------|-----|--------|
| **Outer** | `primals.eco` | Cloudflare (wildcard) | **LIVE** — 14 Caddy routes, cleaned. |
| **Peptidoglycan** | `nestgate.io` | Sovereign Knot DNS + DNSSEC | **LIVE** — branded, Neural API wired (20 primals). |
| **Inner** | `primal.eco` | Sovereign Knot DNS (zero public) | **LIVE** — dnsmasq deployed, all 11 gates resolving. |

---

## NEXT PHASE: DATA FLOW ACTIVATION + PETAL VIS

The infrastructure is deployed. Data flows need to be turned on.

### Gate Team Assignments (from overwatch)

**westGate team**: tideGlass cell boot → federation unblock → convoy convergence
**ironGate team**: footPrint→squirrel wiring → tideGlass PetalTongueClient → petalTongue scene passthrough
**strandGate team**: arXiv Rung 1 rubric (42 items, 12 MUST-fix)
**eastGate overwatch**: RustScript extraction (`@protokarya/rustscript`) → petalTongue TypeScript SDK

### Remaining sporeGate Work

| Item | Status | Detail |
|------|--------|--------|
| nestgate.io gate mesh | **PARTIAL** | Neural API wired. Gate table/WG overlay still "Not Found" — needs mesh.peers query from petalTongue web mode or SSR pre-render. |
| nestgate.io discovery registration | **DEFERRED** | biomeos-api socket returns EOF on JSON-RPC. BTSP handshake may be required. Non-blocking (standalone mode works). |
| Webb HEAD 502 | **UPSTREAM** | esotericWebb HTTP handler bug. Not golgi routing. |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| Gates online | **11** |
| Depot | **v4.57+ SYNCED — ALL 6 NUCLEUS GATES.** 52 builds. |
| Data NAS | **westGate** (3.21 TB / 153 datasets / **452 GB CAS**, convoy 145/s) |
| ironGate storage | **12.7 TB CAS LIVE** |
| Primal tests | **~135,000+** |
| Signal dispatch | **G18 LIVE** — ironGate, 9 providers |
| Convoy provenance | **145/s** (460x total improvement) |
| arXiv Rung 1 | **16⁴ DATA COMPLETE** — +0.01% at β=6.0, 6 ppm cross-vendor |
| K-derm | **3/3 FULLY OPERATIONAL** |
| nestgate.io | **20 primals discovered, capability maps live** |
| Caddy | **14 routes, cleaned (no deprecated directives)** |

---

*Wave 156d — Signal Dispatch + Federation Era. G18 LIVE on ironGate (9 providers). nestgate.io Neural API WIRED (20 primals discovered, capability maps live on dashboard). golgi Caddy CLEANED (deprecated basicauth→basic_auth, redundant headers removed). petalTongue user service wired to Neural API discovery socket + FAMILY_ID. All 6 NUCLEUS gates v4.57+. ~135K+ tests, 13/13 GREEN.*
