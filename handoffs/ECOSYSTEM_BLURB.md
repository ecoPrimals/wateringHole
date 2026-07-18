# ecoPrimals Ecosystem Blurb — Wave 150f

**Date**: Jul 18, 2026 11:30 EDT | **Wave**: 150f | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. 6-GATE MESH. 5 SURFACES LIVE.**

**This wave**: Cascade confirmed ALL 5 composition surfaces returning 200 from
WAN. flockGate completed ops: esotericWebb V19.1 LIVE with systemd persistence.
Deployment chain validated end-to-end (Cloudflare → Caddy → WireGuard → service).
lithoSpore shipped `spore-status` dashboard. initioChem wired pseudospore-core.

---

## 1. DEPLOYMENT CHAIN — Validated End-to-End

```
User → Cloudflare DNS (*.primals.eco wildcard → golgiBody VPS)
  → Cloudflare CDN (outer membrane firebreak)
    → Caddy on golgiBody (TLS termination, Host-header routing)
      → reverse_proxy over WireGuard mesh to target gate
        → Local service (footPrint:8090, esotericWebb:8090, etc.)
```

**URL Standard**: `prefix.primals.eco` (subdomain) REQUIRED. Root redirects
to `sporeprint.primals.eco`.

**Three-Domain Model**:
- `primals.eco` — **intra-membrane** (shared ecosystem)
- `primal.eco` — **inner membrane** (personal sovereign)
- `nestgate.io` — **data service point** (CAS, federated APIs)

---

## 2. LIVE SYSTEMS — WAN-Validated (Jul 18 11:00)

| Surface | URL | Code | Latency | Gate |
|---------|-----|------|---------|------|
| footPrint | `footprint.primals.eco` | **200** | 216ms | sporeGate |
| esotericWebb | `webb.primals.eco` | **200** | 235ms | flockGate |
| sporePrint | `sporeprint.primals.eco` | **200** | 524ms | golgiBody |
| TOPO-VIS | `live.primals.eco` | **200** | 357ms | sporeGate |
| Forgejo | `git.primals.eco` | **200** | 203ms | golgiBody |
| JupyterHub | `lab.primals.eco` | **401** | 128ms | ironGate |
| Root redirect | `primals.eco` | **301** | 139ms | golgiBody |

### footPrint → `footprint.primals.eco` — **LIVE**

466 tests, responsive, a11y, ESLint clean. CSP + security headers + SPA
fallback shipped. Caddy routes all traffic to footPrint:8090 (Express
handles static + `/ext` proxy + `/api/*`). `/ws` → petalTongue:8080.

**Remaining verification**: Map tiles (CSP allows tile domains — visual
check needed). CAS consumer wiring (nestGate says COMPLETE, consumer
side unverified).

### esotericWebb → `webb.primals.eco` — **V19.1, LIVE**

HTTP-aware TCP listener (V19.1): detects HTTP framing, extracts JSON-RPC
body, returns HTTP/1.1 200 with CORS. Both raw and HTTP protocols coexist
on port 8090. systemd user unit enabled. 453 tests.

**Known limitations**:
- GET returns 502 (only POST/JSON-RPC works — no browser navigation, P2)
- V19.1 binary not in depot (local build only, P2)
- `loginctl enable-linger` needed for service to survive logout

### sporePrint → `sporeprint.primals.eco` — **LIVE**

302 pages, pseudoSpore gallery for all 7 springs. Root domain redirect
operational.

---

## 3. PRIMAL DEMAND SIGNAL

### P1 — Inter-Primal Wiring (1 item remaining)

| Need | Owner | Status |
|------|-------|--------|
| `WS_PATH` agent bridge | petalTongue | **OPEN** — last remaining P1 |

Previously P1, now resolved:
- ~~nestGate `PROJECTS_PATH` CAS~~ → COMPLETE (Session 114)
- ~~squirrel null params~~ → FIXED (Wave 150b)
- ~~songBird BTSP mesh.enroll~~ → ACTIVE (Wave 150e)

### P2 — Ecosystem Quality

| Need | Owner | Detail |
|------|-------|--------|
| esotericWebb GET handler | esotericWebb | GET → 502 via Caddy (only POST works) |
| esotericWebb depot binary | sporeGate ops | V19.1 local build, not in depot |
| `loginctl enable-linger` | flockGate ops | systemd user unit survives logout |
| `primals.eco` DNSSEC | ops / Cloudflare | Enable via API |
| footPrint CAS consumer verify | footPrint | nestGate says done, consumer unverified |
| `footprint_composition.toml` URL | cellMembrane | Still has old path-based URL |
| cellMembrane `gate.enroll` → `mesh.enroll` | cellMembrane | Call songBird's mesh.enroll |
| HSM → Android Keystore | bearDog | grapheneGate mobile credential backend |
| Credential store trait | bearDog + squirrel | Silicon Atheism Phase 2 |
| Health monitoring trait | ecosystem | Not procfs-hardcoded |
| `primal-transport` crate | ecosystem | Extract transport abstractions |
| primalSpring CAC scenario | primalSpring | FRAGO issued, not implemented |

### P2 — pseudoSpore Pipeline

| Need | Owner | Detail |
|------|-------|--------|
| `validation.json` per spore | 6 spring teams | Module validation results for promotion |
| Fix groundSpring `bingoCube/nautilus` dep | groundSpring | `cargo test` fails |
| Bash → Rust orchestration | spring teams | 114+ shell scripts |

---

## 4. STRATEGIC GOALS

### NOW

- **Verify footPrint tiles** — visual check at `footprint.primals.eco`
- **Verify footPrint CAS** — consumer-side wiring check
- **Enable Cloudflare DNSSEC** for `primals.eco`
- **Push esotericWebb V19.1 to depot**

### NEAR TERM (next 2-4 weeks)

- **petalTongue WS bridge**: last open P1 inter-primal wiring item
- **esotericWebb GET handler**: make `webb.primals.eco/` browser-navigable
- **Full NUCLEUS composition**: all primals interacting through live products
- **pseudoSpore validation**: promote 6 pending spores
- **projectFOUNDATION design**: thread lineage store, nestGate CAS integration
- **strandGate enrollment**: dual EPYC 7452, 256GB RAM, RTX 3090
- **`primal.eco` inner membrane separation**

### FUTURE (quarter horizon)

- **tideGlass composition**: computational chemistry product
- **primal-transport crate**: publish shared transport abstraction
- **SHOW_HN readiness**: rubric, narrative, demo path
- **fieldGate/biomeGate recovery**: hardware surgery / kernel

---

## 5. DIMENSIONAL SCORECARD (Wave 150f)

| Project | Tests | Clippy | Fmt | Debt | Unsafe | >800L | Prod unwrap |
|---------|-------|--------|-----|------|--------|-------|-------------|
| cellMembrane | 1,100 | 0 | 0 | 0 | 0 | 0 | 0 |
| esotericWebb | 453 | 0 | 0 | 0 | 0 | 0 | 0 |
| footPrint | 466 | 0 | — | 0 | — | 0 | — |
| songBird | 14,322 | swept | swept | 0 | 0 | swept | swept |
| lithoSpore | 227+ | 0 | 0 | 0 | 0 | 0 | 0 |
| loamSpine | 1,702 | 0 | 0 | 0 | 0 | 0 | 0 |
| rhizoCrypt | 1,878 | 0 | 0 | 0 | 0 | 0 | 0 |
| nestGate | 1,710 | 0 | 0 | 0 | 0 | 0 | 10 (justified) |
| primalSpring | 1,203 | 0 | 0 | 0 | 0 | 0 | 0 |
| sporePrint | 289 | — | — | 0 | — | 0 | — |

**Ecosystem**: ~23,300+ tests tracked, 0 debt, 0 unsafe, 0 mocks.

---

## 6. COMPLETED MILESTONES

| Milestone | Wave |
|-----------|------|
| **5 composition surfaces LIVE from WAN** | **150f** |
| **Deployment chain validated end-to-end** | **150f** |
| esotericWebb V19.1 LIVE at `webb.primals.eco` (systemd) | 150f |
| lithoSpore `spore-status` dashboard command | 150f |
| initioChem wired pseudospore-core as external consumer | 150f |
| cellMembrane subdomain routing overhaul (5 compositions) | 150e |
| footPrint CSP + SPA fallback for subdomain deployment | 150e |
| songBird `mesh.enroll` ACTIVE (BTSP-verified proof flow) | 150e |
| nestGate dimensional audit ALL CLEAR (1,710 tests) | 150e |
| nestGate `PROJECTS_PATH` CAS complete | 150e |
| squirrel null params fixed | 150b |
| Silicon Atheism Phase 2 (14/14 + lithoSpore) | 145a |
| Content-Addressed Convergence (6/6) | 143b |
| Glacial Shift (8/8) ALL CLEAR | 137b |
| `gate.enroll` fully automated (7 phases) | 147a |
| lithoSpore ALL CLEAR + 7 pseudoSpores emitted | 150a |
| GAP-036 + GAP-038 closed ecosystem-wide | 150a |
| Depot operational (59+ binaries, 4 arch) | 142a |

---

## 7. MESH TOPOLOGY

```
golgiBody (10.13.37.1) — hub, VPS, Caddy TLS, Cloudflare firebreak
  ├─ sporeGate (10.13.37.2) — builder, footPrint:8090 [LIVE]
  ├─ eastGate  (10.13.37.5) — orchestrator, overwatch
  ├─ flockGate (10.13.37.6) — esotericWebb:8090 [V19.1, LIVE]
  ├─ ironGate  (10.13.37.7) — compute, lithoSpore [ALL CLEAR]
  └─ northGate (10.13.37.8) — Windows, RTX 5090 [enrolled]

Offline: westGate (cold storage), fieldGate (dead CMOS),
         strandGate (pending enrollment), biomeGate (kernel recovery)
```

---

## 8. ORTHOGONAL DIMENSIONS SUMMARY

| Dim | Area | Status | Open items |
|-----|------|--------|------------|
| 1 | Temporal | GREEN | — |
| 2 | Ecological | GREEN | — |
| 3 | Hardware | AMBER | 4 gates offline (not blocking) |
| 4 | Sovereignty | AMBER | `primals.eco` DNSSEC (P2) |
| 5 | Depot | GREEN | esotericWebb V19.1 not in depot (P2) |
| 6 | Public Surface | **GREEN** | 5 surfaces LIVE, root redirect working |
| 7 | Glacial Shift | GREEN | SHOW_HN rubric (P3) |
| 8 | Compositions | **GREEN** | Both products externally functional |
| 9 | Documentation | GREEN | Standards current |
| 10 | Cascade | GREEN | — |
| 11 | CAC | GREEN | primalSpring scenario (P2) |
| 12 | Silicon Atheism | GREEN | Credential trait, health trait (P2) |

---

*Wave 150f: 5 composition surfaces WAN-validated LIVE (footPrint 200, webb 200,
sporeprint 200, live 200, git 200). esotericWebb V19.1 shipped HTTP-aware TCP
listener for Caddy compatibility + systemd persistence. Deployment chain proven
end-to-end. lithoSpore shipped spore-status dashboard. initioChem wired
pseudospore-core as first external consumer. Dimensions 6+8 upgraded to GREEN.
Only 1 P1 item remains (petalTongue WS bridge). 10 GREEN / 2 AMBER dimensions.
23,300+ ecosystem tests. Demand signal condensed to P2 quality items.*
