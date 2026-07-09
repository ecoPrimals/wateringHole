# ecoPrimals Ecosystem Blurb — Wave 135a

**Date**: Jul 9, 2026 15:00 EDT | **Wave**: 135a | **From**: eastGate overwatch
**Posture**: **SOVEREIGN — Coordination backend LANDED. nestGate coord domain + petalTongue dashboard + rootPulse-traced ingest pipeline built. live.primals.eco routing configured. Manifest convergence fix shipped.**

---

## Wave 135a Delivery

| Deliverable | Status | Location |
|-------------|--------|----------|
| nestGate `coord.*` JSON-RPC domain (13 methods) | LANDED | `nestgate-rpc/coord_handlers/` |
| nestGate `/coord/*` HTTP routes (10 endpoints) | LANDED | `nestgate-api/handlers/coordination.rs` |
| Coordination types (CoordArtifact, CoordManifest, ArtifactKind) | LANDED | `coord_handlers/types.rs` |
| `coord.ingest` pipeline (rootPulse-ready) | LANDED | `coord_handlers/ingest.rs` |
| petalTongue coordination dashboard sections | LANDED | `web/index.html` + `handlers.rs` |
| petalTongue `/api/coord/*` endpoints (6 routes) | LANDED | `web_mode/mod.rs` |
| `live.primals.eco` Caddy routing | CONFIGURED | `provision-golgi.sh` |
| Manifest fix: `[compositions.nest]` + westGate repos | LANDED | `ecosystem_manifest.toml` |
| Routing handoff for sporeGate/golgi team | DOCUMENTED | `LIVE_PRIMALS_ECO_ROUTING_WAVE135.md` |

---

## Production Architecture

```
primals.eco (LIVE — sovereign, static)
  :443 → bearDog ACME TLS → Caddy :8091 → sporePrint static (Zola)
  :80  → bearDog HTTP-01 + redirect

live.primals.eco (CONFIGURED — pending DNS + Caddy reload)
  :8443 → Caddy TLS → WireGuard → sporeGate petalTongue :9900
    → coordination dashboard (nestGate CAS backend)
    → /api/coord/blurbs, /heads, /waves, /fragos, /topology, /depot

Subdomains (:8443 Caddy)
  membrane.primals.eco → nestGate depot
  git.primals.eco      → Forgejo
  lab.primals.eco      → sporeGate songBird drawbridge

Mesh
  sporeGate ↔ flockGate (WireGuard, 142ms)
  eastGate ↔ golgi ↔ ironGate + southGate (covalent, <1ms)
```

---

## Coordination Backend Architecture

The nestGate coordination backend is a **Nest Atomic + rootPulse composition**.
Coordination artifacts (blurbs, FRAGOs, AARs, wave state, gate heads) flow
through the rootPulse commit pipeline for full provenance tracing:

```
wateringHole (git) → coord.ingest
  → rhizoCrypt (DAG session)
  → bearDog (sign dehydration summary)
  → nestGate CAS (content.put — BLAKE3 hash)
  → loamSpine (session.commit — permanent ledger)
  → sweetGrass (braid.create — attribution)
  → coordination manifest (artifact index)
```

**JSON-RPC methods (coord domain):**

| Method | Description |
|--------|-------------|
| `coord.blurbs.current` | Current wave blurb |
| `coord.blurbs.list` | All blurbs (newest first) |
| `coord.blurbs.get` | Specific blurb by hash or wave |
| `coord.fragos.list` | FRAGOs and AARs |
| `coord.fragos.get` | Specific FRAGO/AAR |
| `coord.waves.current` | Current wave state |
| `coord.waves.history` | Wave history with provenance |
| `coord.heads.get` | Specific gate HEAD state |
| `coord.heads.all` | All gate HEADs |
| `coord.topology` | Mesh topology |
| `coord.depot.status` | Depot staleness + binary inventory |
| `coord.provenance` | rootPulse trail for any artifact |
| `coord.ingest` | Ingest wateringHole artifacts into CAS |

**HTTP routes (REST parallel surface):**

| Route | Description |
|-------|-------------|
| `GET /coord/blurbs` | List + current blurb |
| `GET /coord/blurbs/:wave` | Specific wave blurb |
| `GET /coord/fragos` | FRAGO/AAR list |
| `GET /coord/fragos/:id` | Specific document |
| `GET /coord/waves` | Current wave + history |
| `GET /coord/heads` | All gate HEADs |
| `GET /coord/heads/:gate` | Specific gate |
| `GET /coord/topology` | Mesh topology |
| `GET /coord/depot` | Depot inventory |
| `GET /coord/provenance/:hash` | Provenance trail |

---

## Remaining Wave 135 Goals

### 1. live.primals.eco — Activate

DNS record + Caddy reload needed on golgi. Handoff delivered:
`LIVE_PRIMALS_ECO_ROUTING_WAVE135.md`

**Owner**: sporeGate / golgiBody operations team

### 2. coord.ingest Population

Run initial ingest to populate the coordination CAS with current artifacts.
Can be triggered via `membrane coord.ingest` or direct JSON-RPC.

**Owner**: cellMembrane team (automate via cascade)

### 3. rootPulse Provenance Trio Activation

The ingest pipeline stores artifacts in CAS and updates the manifest. Full
rootPulse provenance (spine_index, braid_id) requires the provenance trio
(rhizoCrypt + loamSpine + sweetGrass) running on sporeGate's NUCLEUS.

When the trio is live, `coord.ingest` calls the `rootpulse_commit` graph:
dehydrate → sign → store → commit → attribute.

**Owner**: sporeGate NUCLEUS composition team

### 4. bearDog Cert Consolidation

Before Aug 13 cert expiry. Options: Host-header routing or DNS-01.

**Owner**: bearDog + sporeGate/golgi team

### 5. capability.call FULL PASS

Retest `capability.call("jupyter")` from flockGate.

**Owner**: flockGate

### 6. strandGate Enrollment

Pending physical access.

---

## Team Dispatches

| Team | Wave 135a Work |
|------|----------------|
| **nestGate** | LANDED: coord domain (13 methods, 10 HTTP routes, CAS-backed manifest, rootPulse-ready ingest). Next: trio activation when NUCLEUS is live. |
| **petalTongue** | LANDED: coordination dashboard (wave status, gate convergence, blurb preview, FRAGO list, depot health). Next: serve via live.primals.eco. |
| **sporeGate/golgi** | ACTION: add `live.primals.eco` DNS A record, reload Caddy. Activate petalTongue web :9900. Run coord.ingest. |
| **cellMembrane** | ACTION: automate coord.ingest via cascade (detect wateringHole changes → ingest). |
| **primalSpring** | LANDED: manifest fix ([compositions.nest] + westGate repos). |
| **bearDog** | Cert consolidation strategy before Aug 13. |
| **flockGate** | capability.call retest pending. |
| **sporePrint** | Content evolution — target: structured data for live.primals.eco. |

---

## Gate Convergence (Wave 135a)

```
✅ eastGate   — Coordination backend + dashboard landed. Overwatch directing.
✅ sporeGate  — Depot 100%. Drawbridge configured. NUCLEUS host target + coord activation pending.
✅ golgiBody  — primals.eco LIVE. live.primals.eco Caddy block configured, DNS pending.
✅ flockGate  — WAN PASS. capability.call retest pending.
✅ ironGate   — 20 repos current.
🔧 strandGate — Enrollment pending (house 2).
```

---

## Manifest Fixes Shipped

- `[compositions.nest]`: Added `loamSpine` to primals (was missing from provenance trio)
- `[gates.westGate]`: Added `rhizoCrypt` to repos (was missing, inconsistent with nest composition)

Both fixes align the manifest with canonical Nest Atomic documentation (7/7).

---

*primals.eco: sovereign. Coordination backend: CAS + rootPulse. Next: activate live.primals.eco, populate coord artifacts, wire provenance trio.*
