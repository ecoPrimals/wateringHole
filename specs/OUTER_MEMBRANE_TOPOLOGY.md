# Outer Membrane Topology — Full External Surface Specification

**Date**: Aug 17, 2026 | **Wave**: 157k | **Owner**: overwatch + sporeGate (sporePrint)
**Status**: LIVE reference. Update this file when any external surface configuration changes.

---

## Architecture

The external surface follows the Three-Domain K-Derm Model. All public traffic terminates
at **golgiBody Caddy** (`157.230.3.183:443`), which routes per-hostname to either local
file serving or WireGuard-meshed gates.

```
Internet
    │
    ├─ primals.eco ─────── OUTER MEMBRANE (Cloudflare DNS → golgiBody Caddy)
    │     sporePrint static site, depot, git, lab, relay, enrollment
    │
    ├─ nestgate.io ─────── PEPTIDOGLYCAN (Sovereign Knot DNS → golgiBody Caddy)
    │     petalTongue live data/trust surface (CAS, provenance, federation)
    │
    └─ primal.eco ──────── INNER MEMBRANE (Sovereign Knot DNS, SEALED)
          0 public A records. WireGuard mesh only.
```

---

## DNS Layer

### Registrar + Nameserver Ownership

| Domain | Registrar | DNS Provider | Nameservers |
|--------|-----------|--------------|-------------|
| **primals.eco** | Porkbun | **Cloudflare** | `albertus.ns.cloudflare.com`, `serena.ns.cloudflare.com` |
| **nestgate.io** | Porkbun | **Sovereign Knot DNS** | `ns1.primals.eco`, `ns2.primals.eco` |
| **primal.eco** | Porkbun | **Sovereign Knot DNS** | `ns1.primals.eco`, `ns2.primals.eco` |

### Sovereign DNS Infrastructure

| Server | IP | Role |
|--------|-----|------|
| `ns1.primals.eco` | `157.230.3.183` | golgiBody — Knot master |
| `ns2.primals.eco` | `137.184.197.151` | golgiBody-ext — Knot slave |

- Auto DNSSEC (ECDSA P-256), AXFR/IXFR zone transfers
- CAA records: `issue "letsencrypt.org"` + `issuewild "letsencrypt.org"`
- DNSSEC for primals.eco verified: DS 2371/13/2 chain (Porkbun → .eco TLD → Cloudflare KSK)

### Cloudflare DNS Records (primals.eco)

| Type | Name | Target | Notes |
|------|------|--------|-------|
| A | `primals.eco` | `157.230.3.183` | Root domain |
| CNAME | `sporeprint` | `primals.eco` | Main website |
| CNAME | `lab` | `primals.eco` | JupyterHub |
| CNAME | `relay` | `primals.eco` | RustDesk bootstrap |
| CNAME | `ca` | `primals.eco` | step-ca SSH CA |
| CNAME | `depot` | `primals.eco` | Binary depot |
| A | `git` | `157.230.3.183` | Forgejo |
| Wildcard | `*.primals.eco` | → golgiBody | Caddy is routing authority |

**Not in repo**: Cloudflare zone is managed via dashboard. No API automation exists.

---

## TLS + Caddy Routing

All public TLS terminates at golgiBody Caddy. Let's Encrypt certificates via ACME.

**Version-controlled Caddyfile**: `infra/plasmidBin/membrane/Caddyfile`
**Live Caddyfile**: `/etc/membrane/Caddyfile` on golgiBody
**Known drift**: `live.primals.eco` port `:9900` in VC → `:8190` on live server (Aug 12 fix)

### Full Routing Map

| Hostname | DNS Source | Caddy Action | Backend Target | Gate | Service |
|----------|-----------|-------------|----------------|------|---------|
| `primals.eco` | CF A | 301 → `sporeprint.primals.eco` (except `/enroll*`) | — | golgi | Redirect |
| `primals.eco/enroll*` | CF A | `reverse_proxy 127.0.0.1:7780` | local | golgi | Enrollment portal |
| `www.primals.eco` | CF CNAME | 301 → `sporeprint.primals.eco` | — | golgi | Redirect |
| **`sporeprint.primals.eco`** | CF CNAME | `file_server /opt/ecoPrimals/sporePrint/public` | local | golgi | **Zola static site** |
| `footprint.primals.eco` | CF wildcard | `reverse_proxy 10.13.37.2:8090` | WG→sporeGate | sporeGate | footPrint GIS |
| `webb.primals.eco` | CF wildcard | `reverse_proxy 10.13.37.7:8090` | WG→ironGate | ironGate | esotericWebb CRPG |
| `live.primals.eco` | CF wildcard | `reverse_proxy 10.13.37.2:8190` | WG→sporeGate | sporeGate | petalTongue topo-viz |
| `lab.primals.eco` | CF CNAME | `reverse_proxy 10.13.37.2:7780` + basicauth | WG→sporeGate | sporeGate | JupyterHub gateway |
| `membrane.primals.eco` | CF wildcard | Mixed: `/depot/*`, `/hooks/*`, health | local | golgi | Depot hooks, status |
| `depot.primals.eco` | CF CNAME | `file_server /opt/ecoPrimals/depot/` | local | golgi | Binary depot browser |
| `git.primals.eco` | CF A | `reverse_proxy localhost:3000` | local | golgi | **Forgejo** |
| `ca.primals.eco` | CF CNAME | `reverse_proxy localhost:9443` (TLS skip) | local | golgi | **step-ca SSH CA** |
| `relay.primals.eco` | CF CNAME | `file_server` + basicauth | local | golgi | RustDesk info page |
| **`nestgate.io`** | Knot A | `reverse_proxy 10.13.37.2:8190` | WG→sporeGate | sporeGate | **petalTongue peptidoglycan** |
| `www.nestgate.io` | Knot A | 301 → `nestgate.io` | — | golgi | Redirect |

### Security Headers (all vhosts)

- HSTS: `max-age=63072000; includeSubDomains; preload`
- X-Content-Type-Options: `nosniff`
- X-Frame-Options: `DENY`
- CSP: per-vhost (sporePrint allows inline styles for Zola)
- Access log: JSON to `/var/log/caddy/access.log` (50 MiB rotation)

---

## sporePrint Deploy Pipeline

### Current Flow (Sovereign-Primary)

```
Developer push → Forgejo (git.primals.eco)
    │
    ├─ post-receive hook: 50-zola-publish
    │     git reset --hard → zola build --force
    │     output → /opt/ecoPrimals/sporePrint/public
    │     Caddy serves immediately (no restart needed)
    │
    ├─ sovereign-ci-trigger → sporeGate (WG mesh)
    │     builds primals, syncs depot (NOT Zola)
    │
    └─ golgiBody-ext: 15-min timer pull
         └─ GitHub Pages trailing shadow (CI: deploy.yml)
```

### Known Issues

| Issue | Detail | Priority |
|-------|--------|----------|
| **SP-DIV-04** | `temporal.cascade` rebuilds primals but doesn't push Zola output to golgi | P1 |
| **Dual checkout** | `/opt/ecoPrimals/sporePrint/` vs `/opt/ecoPrimals/infra/sporePrint/` — path confusion | P1 |
| **Content stale** | sporePrint reflects ~Wave 155m; 60+ waves of evolution not published | P1 |
| **Zola version** | 0.22.1 pinned — check compatibility if site fails to build | P2 |

### Target Pipeline (Phase B — Not Live)

CAS-backed serving: NestGate `content.get` → Caddy reverse_proxy, with Zola output stored
in CAS rather than filesystem. Designed in `specs/BUILD_DEPLOY_PIPELINE.md`.

---

## Google Search Console

### Current State (from screenshots Aug 17)

- **Property**: `sporeprint.primals.eco` (URL-prefix)
- **Sitemap**: `/sitemap.xml` submitted Jul 26, last read Aug 13, **Status: Success**, 401 discovered pages
- **Indexing**: "Processing data" — not yet showing indexed/not-indexed breakdown
- **Coverage**: "Processing data, please check again in a day"

### What Exists

| Component | Status | Location |
|-----------|--------|----------|
| `robots.txt` | Deployed (`Allow: /`, sitemap pointer) | `infra/sporePrint/static/robots.txt` |
| `sitemap.xml` | Generated by Zola (401 pages) | Auto-built at `sporeprint.primals.eco/sitemap.xml` |
| `llms.txt` (4 variants) | Deployed (AI discovery) | `infra/sporePrint/static/llms*.txt` |
| `identity.json` (Schema.org) | Deployed | `infra/sporePrint/static/identity.json` |
| google-site-verification | **NOT FOUND** — may be verified via DNS TXT record | — |
| GSC service account | **DEPLOYED** on golgi | `/opt/ecoPrimals/credentials/gsc-service-account.json` |
| GSC project | `ecoprimals-seo` | Service account: `sporeprint-seo@ecoprimals-seo.iam.gserviceaccount.com` |

### API Capability (Available, NOT Implemented)

The Google Search Console API provides full agentic management:

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `sitemaps.submit` | `PUT /webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` | Submit/resubmit sitemap |
| `sitemaps.get` | `GET /webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` | Check sitemap status |
| `sitemaps.list` | `GET /webmasters/v3/sites/{siteUrl}/sitemaps` | List all submitted sitemaps |
| `searchanalytics.query` | `POST /webmasters/v3/sites/{siteUrl}/searchAnalytics/query` | Query search performance |
| `urlInspection.index.inspect` | `POST /v1/urlInspection/index:inspect` | Inspect specific URL indexing |

**Auth**: OAuth 2.0 with `https://www.googleapis.com/auth/webmasters` scope.
**Credentials**: Service account at `/opt/ecoPrimals/credentials/gsc-service-account.json` on golgi.

### Planned `membrane seo.*` Commands (Spec Only — No Rust Implementation)

| Command | Purpose |
|---------|---------|
| `membrane seo.submit-sitemap` | Submit/resubmit sitemap to GSC |
| `membrane seo.status` | Query indexing coverage stats |
| `membrane seo.request-index` | Request indexing for specific URLs |
| `membrane seo.coverage` | Check indexed vs not-indexed breakdown |

**Owner**: sporeGate (cellMembrane) — credentials deployed, API confirmed available.

---

## The Google Problem

### What's Likely Broken

The screenshots show GSC is *working* — sitemap was successfully read on Aug 13, 401 pages discovered. But:

1. **"Processing data"** on the coverage report is normal for new properties or properties that were recently re-verified. GSC can take 2-7 days to process.

2. **The real issue is the property scope**: GSC shows `sporeprint.primals.eco` as the property. But `primals.eco` (root domain) redirects to `sporeprint.primals.eco`. If Google is crawling `primals.eco` and being redirected, it may see the content under `sporeprint.primals.eco` but attribute it differently.

3. **Recommendation**: Verify `primals.eco` as a **Domain property** (`sc-domain:primals.eco`) in addition to the URL-prefix property for `sporeprint.primals.eco`. Domain properties capture all subdomains. This requires a DNS TXT record verification.

4. **Wildcard routing**: If unrecognized subdomains (e.g., `random.primals.eco`) reach Caddy without a matching server block, Caddy's default behavior varies. Ensure unknown subdomains return 404 or redirect to sporePrint, not serve content under different canonical URLs.

---

## sporePrint → NUCLEUS Live Surface (Concept Evolution)

### Phase 0: Fix the Static Site (NOW)
- Triage Zola build on golgi (post-receive hook, dual checkout path, Zola 0.22.1 compat)
- Get primals.eco serving current content
- Verify Google can crawl it

### Phase 1: Live Data Endpoints
- petalTongue routes for gate status, test counts, depot versions
- Same pattern as nestgate.io Phase 2+3
- Caddy proxies new routes to sporeGate petalTongue `:8190`

### Phase 2: cellMembrane Data Pipeline
- Validation counts, spring results, provenance chain stats → petalTongue
- strandGate QCD data (45 configs, plaquette values) served live
- CAS links for references and datasets

### Phase 3: Semantic Layer
- Structured data for translate.js (Validation Class V)
- Machine-readable science data, validation results, references
- JSON-LD enrichment beyond current `identity.json`

### Phase 4: Google SEO Automation
- Implement `membrane seo.*` commands using GSC API
- Automated sitemap resubmission on content change
- Coverage monitoring and indexing status alerts
- Run via sporeGate as agentic SEO management

---

## Cloudflare Configuration (Not in Repo)

Cloudflare manages DNS for `primals.eco` via their dashboard. No API token or Terraform
config exists in the codebase. To automate Cloudflare DNS, the sporeGate team would need
to create a Cloudflare API token and implement `membrane dns.*` commands.

**Critical**: Any DNS changes for `primals.eco` (adding/removing subdomains, TXT records
for domain verification) currently require manual dashboard access.

---

## File Index

| Purpose | Path |
|---------|------|
| Three-domain spec | `wateringHole/specs/THREE_DOMAIN_TOPOLOGY_SPEC.md` |
| This file | `wateringHole/specs/OUTER_MEMBRANE_TOPOLOGY.md` |
| Caddy config (VC) | `plasmidBin/membrane/Caddyfile` |
| sporePrint config | `sporePrint/config.toml` |
| sporePrint deploy spec | `sporePrint/specs/BUILD_DEPLOY_PIPELINE.md` |
| robots.txt | `sporePrint/static/robots.txt` |
| llms.txt | `sporePrint/static/llms.txt` |
| identity.json | `sporePrint/static/identity.json` |
| GitHub shadow CI | `sporePrint/.github/workflows/deploy.yml` |
| Inner DNS (dnsmasq) | `plasmidBin/membrane/primal-eco.dnsmasq.conf` |
| DNS action log | `wateringHole/fossilRecord/.../KDERM_DNS_ACTIONS.md` |
| SEO agentification spec | `wateringHole/fossilRecord/.../CELLMEMBRANE_WAVE151c_SEO_AGENTIFICATION.md` |

---

*Outer membrane topology — Wave 157k. Porkbun → Cloudflare (primals.eco) + Sovereign Knot
(nestgate.io, primal.eco sealed). golgiBody Caddy terminates all TLS. 14 subdomains/routes
mapped. GSC API available, credentials deployed, automation not implemented. sporePrint
evolving from static Zola to NUCLEUS-served live surface. QCD data, provenance chains, and
gate status to be served live via petalTongue + cellMembrane pipeline.*
