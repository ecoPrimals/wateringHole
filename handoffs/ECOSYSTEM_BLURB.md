# ecoPrimals Ecosystem Blurb — Wave 150d

**Date**: Jul 18, 2026 10:20 EDT | **Wave**: 150d | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. DEPLOYMENT CHAIN TRACED.**

**This wave**: Deep investigation of deployment chain. Subdomain standard
formalized (`prefix.primals.eco`). songBird's role as inner membrane port
solver documented. Cloudflare outer membrane firebreak pattern confirmed.
DNSSEC status clarified. Routing fixes specified with exact architectural
context. Standards updated.

---

## 1. DEPLOYMENT CHAIN — How Traffic Reaches Services

```
User → Cloudflare DNS (*.primals.eco wildcard → golgiBody VPS)
  → Cloudflare CDN (outer membrane firebreak — absorbs hostile traffic)
    → Caddy on golgiBody (TLS termination, Host-header routing)
      → reverse_proxy over WireGuard mesh to target gate
        → songBird drawbridge :7780 (capability → port resolution)
          → Local service (footPrint:8090, esotericWebb:8090, etc.)
```

**songBird = inner membrane port solver.** Drawbridge maps paths to
capabilities (`SONGBIRD_DRAWBRIDGE_ROUTES`), resolves capabilities to URLs
(`SONGBIRD_PROXY_ROUTES`), and proxies external "weak bond" APIs through a
domain-validated allowlist. Production optimization: Caddy handles external
HTTPS proxying directly via songBird's `infra/caddy/` snippets.

**Cloudflare = outer membrane firebreak.** Wildcard `*.primals.eco` resolves
to golgiBody. No DNS changes needed for new subdomains — only a Caddy block.
Cloudflare absorbs DDoS and bot traffic. This is the **target architecture**
(diderm model), not transitional.

**URL Standard**: `prefix.primals.eco` (subdomain) is REQUIRED for all
compositions. Path-based routing (`primals.eco/path/`) is prohibited.
Root domain (`primals.eco`) redirects to `sporeprint.primals.eco`.

**Three-Domain Model**:
- `primals.eco` — **intra-membrane** (shared ecosystem: compositions, depot, forge, docs)
- `primal.eco` — **inner membrane** (personal sovereign: mesh, ceremonies, private compositions)
- `nestgate.io` — **data service point** (CAS, federated APIs, weak bond data ingestion)

---

## 2. LIVE SYSTEMS — Actual State (Operator-Verified Jul 18)

### footPrint → `footprint.primals.eco` — **DEPLOYED, NOT EXTERNALLY FUNCTIONAL**

**Observed**: UI shell loads but map tiles gray/blank, geocoder non-functional.

| Issue | Fix | Owner |
|-------|-----|-------|
| Caddy routes `/api/*` but proxy is at `/ext` | Route ALL `footprint.primals.eco` → footPrint:8090 (let Express handle everything) | cellMembrane |
| Catch-all → petalTongue:8080 | Change catch-all upstream to footPrint:8090 | cellMembrane |
| Map tiles blank (CSP or Esri) | Add CSP `img-src` for `*.arcgisonline.com`, `*.tile.openstreetmap.org` | cellMembrane |
| songBird Caddy snippets not imported | Import `footprint-gis-proxy.Caddyfile` for production tile proxying | sporeGate ops |

**Simplest fix**: Replace the three sub-routes with a single `reverse_proxy sporeGate:8090`. footPrint's Express server already handles static files, `/ext` proxy, `/api/*`, and would only need petalTongue for `/ws`.

### esotericWebb → `webb.primals.eco` — **404, CADDY MISSING**

**Observed**: `primals.eco/webb/` returns sporePrint 404.

| Issue | Fix | Owner |
|-------|-----|-------|
| No Caddy vhost for `webb.primals.eco` | Add `webb.primals.eco { reverse_proxy 10.13.37.6:8090 }` to golgiBody | sporeGate ops |
| cellMembrane uses path-based (`/webb/`) | Change `ESOTERICWEBB_PATH` to `WEBB_DOMAIN = "webb.primals.eco"` | cellMembrane |
| No systemd persistence | `systemctl enable --now esotericwebb-server` on flockGate | sporeGate ops |

### Verified live surfaces

| Surface | URL | Gate | Status |
|---------|-----|------|--------|
| sporePrint | `sporeprint.primals.eco` | golgiBody | NEEDS MIGRATION (currently on root `primals.eco`) |
| TOPO-VIS | `live.primals.eco` | sporeGate | LIVE |
| JupyterHub | `lab.primals.eco` | ironGate | LIVE |
| Forgejo | `git.primals.eco` | golgiBody | LIVE |
| Depot | `depot.primals.eco` | golgiBody | LIVE |

---

## 3. DNSSEC + SOVEREIGNTY STATUS

| Domain | Layer | DNS Authority | DNSSEC | Status |
|--------|-------|--------------|--------|--------|
| `primal.eco` | Inner membrane | knot-dns (sovereign) | **ENABLED** | Fully sovereign |
| `nestgate.io` | Content organelle | knot-dns (sovereign) | **ENABLED** | Fully sovereign |
| `primals.eco` | Outer membrane | Cloudflare (wildcard) | **NOT DONE** | P2 — enable via Cloudflare or NS cutover |

**NS architecture**: Porkbun registrar. `primal.eco` + `nestgate.io` point to
`ns1.primals.eco` / `ns2.primals.eco` (sovereign knot-dns on golgiBody).
`primals.eco` points to Cloudflare nameservers. knot-dns runs with DNSSEC
enabled on VPS; the `primals.eco` NS cutover to sovereign is pending registrar
action but NOT required (outer membrane MAY use Cloudflare per diderm model).

**DNSSEC options for `primals.eco`**:
1. Enable DNSSEC through Cloudflare (quick — API-supported) — preserves CDN/DDoS
2. Cutover NS to sovereign knot-dns — full sovereignty but loses Cloudflare protection
3. Recommended: option 1 first (outer membrane MAY use commercial per diderm standard)

---

## 4. PRIMAL DEMAND SIGNAL

### P0 — Deployment Broken (blocks external users)

| Need | Owner | Detail |
|------|-------|--------|
| Fix footPrint Caddy routing | cellMembrane | Route all `footprint.primals.eco` → sporeGate:8090. Add CSP for tile domains. Import songBird Caddy GIS snippets. |
| Create `webb.primals.eco` Caddy vhost | cellMembrane + ops | Subdomain standard. `reverse_proxy 10.13.37.6:8090` on golgiBody. |
| Change cellMembrane esotericWebb constant | cellMembrane | `ESOTERICWEBB_PATH → WEBB_DOMAIN = "webb.primals.eco"` (subdomain standard) |
| Enable esotericWebb systemd | sporeGate ops | `systemctl enable --now esotericwebb-server` on flockGate |
| Migrate sporePrint to `sporeprint.primals.eco` | cellMembrane + ops | Add `SPOREPRINT_DOMAIN` constant, Caddy vhost, root redirect |

### P1 — Inter-Primal Wiring

| Need | Owner | Consumer | Detail |
|------|-------|----------|--------|
| `PROJECTS_PATH` CAS wiring | nestGate | footPrint | Content-addressed project serving |
| `WS_PATH` agent bridge | petalTongue | footPrint | WebSocket for real-time agent comms |
| `null` params on health | squirrel | esotericWebb | Webb workaround: sends `{}` |
| BTSP → `gate.enroll` | songBird | cellMembrane | Last enrollment automation primitive |

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

- **Fix deployment chain**: footPrint Caddy routing + CSP + songBird snippets
- **Create `webb.primals.eco`**: Caddy vhost + systemd persistence
- **Migrate sporePrint** to `sporeprint.primals.eco`, root domain redirect
- **Evolve cellMembrane**: subdomain constants for all compositions
- **Enable Cloudflare DNSSEC** for `primals.eco` (API-supported)

### NEAR TERM (next 2-4 weeks)

- **Full NUCLEUS composition**: all primals interacting through live products
- **nestGate CAS + petalTongue WS**: complete footPrint's backend composition
- **songBird BTSP**: fully automated mesh enrollment end-to-end
- **pseudoSpore validation**: promote 6 pending spores from PENDING → COMPLETE
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090
- **`primal.eco` inner membrane separation**: fully independent identity

### FUTURE (quarter horizon)

- **tideGlass composition**: computational chemistry product (Phase 0)
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **Exotic depot architectures**: riscv64, armv7, s390x (validated, not shipping)
- **NS cutover for primals.eco**: sovereign DNS if Cloudflare exits (optional)
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
| primalSpring | 1,203 | **0** | 0 | 0 | 0 | 0 | 0 |
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
| footPrint code complete (466 tests, responsive, a11y) — routing P0 | 150c |
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
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [routing broken]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [Caddy missing]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Offline: westGate (cold storage), fieldGate (dead CMOS),
         strandGate (pending enrollment), biomeGate (kernel recovery)
```

| Port | Service | Gate | Protocol |
|------|---------|------|----------|
| 8080 | nestGate / petalTongue | sporeGate | HTTP (static + WS) |
| 8090 | footPrint | sporeGate | HTTP (API, behind drawbridge) |
| 8090 | esotericWebb | flockGate | HTTP (direct serve) |

---

## 8. ORTHOGONAL DIMENSIONS SUMMARY (12/12 reviewed)

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | — |
| 2 | Ecological | GREEN | — |
| 3 | Hardware | AMBER | 4 gates offline (not blocking) |
| 4 | Sovereignty | AMBER | `primals.eco` DNSSEC not enabled |
| 5 | Depot | GREEN | Exotic arch (P3) |
| 6 | Public Surface | **RED** | footPrint routing broken, webb Caddy missing |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric (P3) |
| 8 | Compositions | **RED** | Neither product externally functional |
| 9 | Documentation | GREEN | Standards updated (routing, CSP) |
| 10 | Cascade | GREEN | songBird BTSP (P1) |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait, health trait (P2) |

---

*Wave 150d: Three-domain model refined. `primals.eco` = intra-membrane (shared
ecosystem), `primal.eco` = inner membrane (personal sovereign), `nestgate.io` =
data service point. Root domain redirects to `sporeprint.primals.eco`.
All compositions use `prefix.primals.eco` subdomains. Deployment chain traced
end-to-end: Cloudflare → Caddy → songBird drawbridge → service. songBird =
inner membrane port solver. Cloudflare = outer firebreak (target architecture).
DNSSEC: sovereign domains enabled, `primals.eco` P2. Both products deployed
but not externally functional — 5 P0 routing/ops items issued. Standards
updated: DIDERM_DOMAIN_ARCHITECTURE, COMPOSITION_ROUTING_STANDARD.*
