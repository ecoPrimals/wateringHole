# Composition Routing Standard

**Authority**: Overwatch + Ecosystem Convention
**Status**: Active (Wave 138a)
**Date**: 2026-07-14
**Prerequisites**: `GATEHOUSE_DARKFOREST_STANDARD.md`, `DIDERM_DOMAIN_ARCHITECTURE.md`

---

## Purpose

This standard defines how live compositions (protoKarya projects and
other deployed products) register with the sovereign routing
infrastructure, ingest external data, and expose capabilities to
the mesh.

Every composition that wants a `*.primals.eco` subdomain or mesh
capability registration MUST follow this standard.

---

## Requirements

### 1. Subdomain Registration

Compositions receive subdomains through the `*.primals.eco` wildcard
DNS. No Cloudflare changes are needed. Only a Caddy server block
on golgi is required.

**Rule**: Add a Caddy block to `provision/provision-golgi.sh` with
the `security_headers` import. The wildcard catch-all block returns
404 for unclaimed subdomains.

```caddy
myproject.primals.eco {
    import security_headers
    reverse_proxy localhost:PORT
}
```

For path-based routing on the root domain:

```caddy
handle /myproject/* {
    reverse_proxy localhost:PORT
}
```

### 2. Drawbridge Capability Registration

Compositions that serve capabilities MUST register them via songBird
drawbridge environment variables:

```bash
SONGBIRD_DRAWBRIDGE_ROUTES=/path=capability_name
SONGBIRD_PROXY_ROUTES=capability_name=http://backend:port
```

This auto-registers the capability in the IPC registry and announces
it to mesh peers. Remote gates can `capability.call("capability_name")`
to reach this composition.

### 3. Data Ingestion via Weak Bonds

External data sources enter through drawbridge weak bonds. This is
the ONLY approved path for external data entering the sovereign
interior.

**Ingestion flow**:

```
External API (USGS, NCBI, ArcGIS, etc.)
  → HTTP/HTTPS fetch (weak bond, zero trust)
    → BLAKE3 hash (integrity verification)
      → NestGate CAS store (content-addressed)
        → Loam Certificate mint (provenance attribution)
          → Available as capability across mesh
```

**Requirements**:
- All fetched data MUST be BLAKE3 hashed before storage
- Source attribution MUST be recorded (sweetGrass braid minimum)
- Data MUST land in NestGate CAS, not local filesystem
- Ingestion SHOULD be idempotent (same data = same hash = no duplicate)

### 4. Domain Trust Levels

| Domain | Trust Level | What Deploys Here |
|--------|------------|-------------------|
| `*.primals.eco` | Outer membrane (untrusted by inner) | Public compositions, shared data, demos |
| `*.primal.eco` | Inner membrane (full trust) | Private compositions, ceremonies, sovereign data |
| `*.nestgate.io` | Content organelle | Federated data gateway, CAS queries |

**Rule**: The same composition code can deploy to both domains. The
domain determines the trust level, which determines what data is
accessible and what provenance is required.

### 5. Composition Manifest

Every composition SHOULD have a manifest file declaring its
capabilities, data sources, and primal dependencies:

```toml
[composition]
name = "footPrint"
org = "protoKarya"
subdomain = "primals.eco/footprint/"
trust_level = "outer"

[capabilities]
exposed = ["gis.render", "gis.layers", "gis.search"]

[data_sources]
usgs = { type = "weak_bond", url = "https://basemap.nationalmap.gov" }
osm = { type = "weak_bond", url = "https://tile.openstreetmap.org" }

[primals]
required = ["nestGate", "songBird", "petalTongue"]
optional = ["bearDog"]
```

### 6. Security Headers

All compositions served through Caddy MUST import the standard
security headers snippet:

```caddy
(security_headers) {
    header {
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        Permissions-Policy "geolocation=(), microphone=(), camera=()"
        -Server
    }
}
```

CSP (Content-Security-Policy) SHOULD be composition-specific to
allow only the external origins the composition needs.

---

## Composition Lifecycle

```
1. DESIGN    — Define capabilities, data sources, primal deps
2. DEVELOP   — Build in protoKarya or relevant org
3. REGISTER  — Add Caddy block + drawbridge routes
4. DEPLOY    — Binary to depot, systemd service, mesh announce
5. VALIDATE  — primalSpring scenario confirms capability.call works
6. OPERATE   — Live on *.primals.eco, data flowing, capabilities exposed
7. FEDERATE  — Other compositions consume via capability.call
```

### Adding a Composition (Checklist)

- [ ] Composition code in appropriate org (protoKarya, sporeGarden, etc.)
- [ ] Caddy block in `provision-golgi.sh` with `security_headers`
- [ ] `SONGBIRD_DRAWBRIDGE_ROUTES` and `SONGBIRD_PROXY_ROUTES` configured
- [ ] Data sources documented with ingestion endpoints
- [ ] NestGate CAS wired for content storage (if applicable)
- [ ] primalSpring validation scenario created
- [ ] Security headers verified (`darkforest --scope outer --target subdomain`)
- [ ] Composition manifest TOML created

---

## Current Compositions (Wave 138a)

| Composition | Subdomain | Status | Capabilities |
|------------|-----------|--------|-------------|
| sporePrint | `primals.eco` | LIVE | `content.serve` |
| footPrint | `primals.eco/footprint/` | LIVE | GIS proxy (10 hosts) |
| TOPO-VIS | `live.primals.eco` | LIVE | `topo.visualize` |
| JupyterHub | `lab.primals.eco` | LIVE | `jupyter` |
| Forgejo | `git.primals.eco` | LIVE | `forge.serve` |
| Nest Atomic | `membrane.primals.eco` | LIVE | Tower + Nest services |
| tideGlass | `tideglass.primals.eco` | PLANNED | GPS reversal screening |
| helixVision | `helix.primals.eco` | PLANNED | Expression analysis |

---

## References

- `GATEHOUSE_DARKFOREST_STANDARD.md` — Bond escalation, drawbridge spec
- `DIDERM_DOMAIN_ARCHITECTURE.md` — Domain trust levels, membrane layers
- `GLOSSARY.md` — Drawbridge, weak bonds, Loam Certificates
- `whitePaper/gen5/foundations/COMPOSITION_ROUTING_PATTERN.md` — Full pattern documentation
- `whitePaper/gen5/foundations/EXTERNAL_SOVEREIGNTY_PATTERN.md` — Collaborator gate routing
- `provision/provision-golgi.sh` — Caddy configuration source of truth

---

## Changelog

| Wave | Change |
|------|--------|
| 138a | Initial: formalized composition routing standard from ad-hoc footPrint and JupyterHub deployments. Wildcard DNS, drawbridge registration, data ingestion via weak bonds, trust levels by domain. |
