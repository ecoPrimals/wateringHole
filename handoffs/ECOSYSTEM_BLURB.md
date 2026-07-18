# ecoPrimals Ecosystem Blurb — Wave 150e

**Date**: Jul 18, 2026 11:00 EDT | **Wave**: 150e | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. ALL P0 CODE COMPLETE.**

**This wave**: Cascade absorbed evolution from 5 repos. ALL P0 deployment code
is now complete — cellMembrane shipped subdomain routing, footPrint shipped CSP
+ SPA fallback, songBird mesh.enroll is ACTIVE. Only ops deployment on
golgiBody/flockGate remains. 3 of 4 P1 inter-primal wiring items RESOLVED
(nestGate CAS, squirrel null params, songBird BTSP). Demand signal condensed.

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
capabilities, resolves them to URLs, and proxies external "weak bond" APIs
through a domain-validated allowlist. Production: Caddy imports songBird's
`infra/caddy/` snippets for high-volume tile proxying.

**Cloudflare = outer membrane firebreak.** Wildcard `*.primals.eco` → golgiBody.
No DNS changes needed for new subdomains. Target architecture (diderm model).

**URL Standard**: `prefix.primals.eco` (subdomain) REQUIRED. Root domain
redirects to `sporeprint.primals.eco`.

**Three-Domain Model**:
- `primals.eco` — **intra-membrane** (shared ecosystem: compositions, depot, forge, docs)
- `primal.eco` — **inner membrane** (personal sovereign: mesh, ceremonies, private)
- `nestgate.io` — **data service point** (CAS, federated APIs, weak bond data)

---

## 2. LIVE SYSTEMS — Status After Cascade

### footPrint → `footprint.primals.eco` — **CODE COMPLETE, OPS DEPLOYMENT PENDING**

All P0 code issues resolved this cascade:
- cellMembrane: Caddy simplified to 2 routes (catch-all → footPrint:8090,
  `/ws` → petalTongue:8080). CSP headers for tile domains shipped.
- footPrint: CSP + security headers + SPA fallback added to Express server.
- songBird: `footprint-gis-proxy.Caddyfile` updated for subdomain standard.

**Remaining**: Run `membrane caddy.generate` on golgiBody and reload Caddy.
466 tests, responsive, a11y, ESLint clean.

### esotericWebb → `webb.primals.eco` — **V19, CODE COMPLETE, OPS PENDING**

V19 shipped: HTTP transport adapter, canonical URL per subdomain standard.
cellMembrane shipped `WEBB_DOMAIN = "webb.primals.eco"` Caddy vhost.

**Remaining**: `systemctl enable --now esotericwebb-server` on flockGate,
then reload Caddy on golgiBody. 472 tests.

### sporePrint → `sporeprint.primals.eco` — **CODE COMPLETE, OPS PENDING**

cellMembrane shipped `SPOREPRINT_DOMAIN` constant and root redirect.
sporePrint already absorbed subdomain standard (Wave 150d commit).

**Remaining**: Reload Caddy on golgiBody.

### Other live surfaces

| Surface | URL | Gate | Status |
|---------|-----|------|--------|
| TOPO-VIS | `live.primals.eco` | sporeGate | LIVE |
| JupyterHub | `lab.primals.eco` | ironGate | LIVE |
| Forgejo | `git.primals.eco` | golgiBody | LIVE |
| Depot | `depot.primals.eco` | golgiBody | LIVE |

---

## 3. DNSSEC + SOVEREIGNTY STATUS

| Domain | Layer | DNS Authority | DNSSEC | Status |
|--------|-------|--------------|--------|--------|
| `primal.eco` | Inner membrane | knot-dns (sovereign) | **ENABLED** | Fully sovereign |
| `nestgate.io` | Data service point | knot-dns (sovereign) | **ENABLED** | Fully sovereign |
| `primals.eco` | Intra-membrane | Cloudflare (wildcard) | **NOT DONE** | P2 — enable via Cloudflare API |

---

## 4. PRIMAL DEMAND SIGNAL

### OPS — Deployment (code complete, ops action needed)

| Action | Gate | Command / Detail |
|--------|------|-----------------|
| Regenerate Caddyfile | golgiBody | `membrane caddy.generate` — creates vhosts for footprint, webb, sporeprint + root redirect |
| Reload Caddy | golgiBody | `systemctl reload caddy` |
| Enable esotericWebb | flockGate | `systemctl enable --now esotericwebb-server` |

### P1 — Inter-Primal Wiring

| Need | Owner | Status |
|------|-------|--------|
| ~~`PROJECTS_PATH` CAS wiring~~ | nestGate | **COMPLETE** (Session 114). footPrint consumer verification needed. |
| `WS_PATH` agent bridge | petalTongue | Open — WebSocket for real-time agent comms |
| ~~`null` params on health~~ | squirrel | **FIXED** (Wave 150b, commit `325cae96`) |
| ~~BTSP → `gate.enroll`~~ | songBird | **ACTIVE** — `mesh.enroll` with BTSP-verified proof flow. cellMembrane integration P2. |

**Only 1 P1 item remains open**: petalTongue `WS_PATH` agent bridge.

### P2 — Ecosystem Quality + Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| HSM → Android Keystore | bearDog | grapheneGate mobile credential backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 completion |
| Health monitoring trait | ecosystem | Not procfs-hardcoded |
| `primal-transport` crate | ecosystem | Extract transport abstractions (nestGate has candidates) |
| primalSpring CAC scenario | primalSpring | FRAGO issued, not implemented |
| primalSpring `wan-deploy` | primalSpring | 1/5 protoKarya scenarios remaining |
| cellMembrane `gate.enroll` → `mesh.enroll` | cellMembrane | Call songBird's mesh.enroll from enrollment flow |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results for promotion |
| Fix groundSpring `bingoCube/nautilus` dep | groundSpring | `cargo test` fails |
| Add `scope.toml` to each spring | spring teams | Self-describing artifact manifest |
| Bash → Rust orchestration | spring teams | 114+ shell scripts across springs |

---

## 5. STRATEGIC GOALS

### NOW (this session)

- **Deploy Caddy changes on golgiBody** — single ops action makes all 3 products externally live
- **Enable esotericWebb systemd** on flockGate
- **Verify footPrint end-to-end** — consumer-side CAS wiring (nestGate says COMPLETE)
- **Enable Cloudflare DNSSEC** for `primals.eco` (API-supported)

### NEAR TERM (next 2-4 weeks)

- **Full NUCLEUS composition**: all primals interacting through live products
- **petalTongue WS bridge**: last open P1 inter-primal wiring item
- **pseudoSpore validation**: promote 6 pending spores
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090
- **`primal.eco` inner membrane separation**: fully independent identity

### FUTURE (quarter horizon)

- **tideGlass composition**: computational chemistry product (Phase 0)
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **NS cutover for primals.eco**: sovereign DNS (optional — Cloudflare acceptable)
- **fieldGate/biomeGate recovery**: hardware surgery / kernel

---

## 6. DIMENSIONAL SCORECARD (Wave 150e — Updated)

| Project | Tests | Clippy | Fmt | Debt | Unsafe | >800L | Prod unwrap |
|---------|-------|--------|-----|------|--------|-------|-------------|
| cellMembrane | 1,100 | 0 | 0 | 0 | 0 | 0 | 0 |
| esotericWebb | 472 | 0 | 0 | 0 | 0 | 0 | 0 |
| footPrint | 466 | 0 | — | 0 | — | 0 | — |
| songBird | 14,322 | swept | swept | 0 | 0 | swept | swept |
| lithoSpore | 227 | 0 | 0 | 0 | 0 | 0 | 0 |
| loamSpine | 1,702 | 0 | 0 | 0 | 0 | 0 | 0 |
| rhizoCrypt | 1,878 | 0 | 0 | 0 | 0 | 0 | 0 |
| nestGate | 1,710 | 0 | 0 | 0 | 0 | 0 | 10 (justified) |
| primalSpring | 1,203 | 0 | 0 | 0 | 0 | 0 | 0 |
| sporePrint | 289 | — | — | 0 | — | 0 | — |

**Ecosystem totals**: ~23,300+ tests tracked, 0 debt, 0 unsafe, 0 mocks.

---

## 7. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | 145a |
| Content-Addressed Convergence (6/6) | 143b |
| Glacial Shift (8/8) ALL CLEAR | 137b |
| `gate.enroll` fully automated (7 phases) | 147a |
| lithoSpore ALL CLEAR (USB round-trip, ring dropped) | 150a |
| pseudoSpore pipeline: 7 springs emitted | 150a |
| nestGate dimensional audit ALL CLEAR (1,710 tests, 0/0/0/0) | 150e |
| nestGate `PROJECTS_PATH` CAS wiring complete | 150e |
| squirrel null params fixed (esotericWebb P1) | 150b |
| songBird `mesh.enroll` ACTIVE (BTSP-verified proof flow) | 150e |
| cellMembrane subdomain routing overhaul (5 compositions) | 150e |
| footPrint CSP + SPA fallback for subdomain deployment | 150e |
| esotericWebb V19 + subdomain standard adopted | 150e |
| E2E Tutorial Standard adopted (both products) | 149a |
| Dimensional review sweep (15 teams responded) | 150a |
| GAP-036 + GAP-038 closed ecosystem-wide | 150a |
| songBird drawbridge + /jsonrpc + discovery | 148a |
| Depot operational (59+ binaries, 4 arch) | 142a |

---

## 8. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [code complete, Caddy pending]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [V19, systemd + Caddy pending]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Offline: westGate (cold storage), fieldGate (dead CMOS),
         strandGate (pending enrollment), biomeGate (kernel recovery)
```

---

## 9. ORTHOGONAL DIMENSIONS SUMMARY

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | — |
| 2 | Ecological | GREEN | — |
| 3 | Hardware | AMBER | 4 gates offline (not blocking) |
| 4 | Sovereignty | AMBER | `primals.eco` DNSSEC (P2) |
| 5 | Depot | GREEN | Exotic arch (P3) |
| 6 | Public Surface | AMBER | Code complete — ops deployment pending |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric (P3) |
| 8 | Compositions | AMBER | Code complete — Caddy reload + systemd enable pending |
| 9 | Documentation | GREEN | Standards current |
| 10 | Cascade | GREEN | — |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait, health trait (P2) |

---

*Wave 150e: Cascade absorbed 5 repos. ALL P0 routing code COMPLETE —
cellMembrane shipped subdomain routing overhaul (WEBB_DOMAIN, SPOREPRINT_DOMAIN,
footPrint single-upstream, CSP, root redirect). footPrint shipped CSP + SPA
fallback. songBird mesh.enroll ACTIVE. nestGate scored 1,710 tests + confirmed
PROJECTS_PATH CAS complete. squirrel null params fixed. esotericWebb V19 +
subdomain adopted. 3/4 P1 items RESOLVED — only petalTongue WS bridge remains.
Deployment is now a single ops action: Caddy regenerate on golgiBody + systemd
enable on flockGate. Dimensions 6+8 upgraded RED → AMBER (code done, ops pending).
23,300+ tests tracked ecosystem-wide.*
