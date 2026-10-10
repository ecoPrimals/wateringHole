# AAR: Wildcard Membrane — Wave 172b

**Date:** 2026-10-10
**Operator:** ecoPrimal + Artisan
**Scope:** Collapse 29-domain surface into `*.primals.eco` wildcard → epitope aperture

---

## Summary

The outer membrane surface was consolidated from 29 individually-provisioned domain blocks into a single wildcard entry point. The subdomain itself becomes the query — the visitor types what they need, and the epitope sorter decides what to present.

`H(data|epitope) < H(data|alphabet) < H(data)`

The epitope sort reduces entropy more than alphabetical ordering. The subdomain IS the epitope.

---

## What Was Built

### 1. DNS (pre-existing)
- `*.primals.eco A 157.230.3.183` — already configured on Cloudflare
- All subdomains resolve to golgiBody

### 2. Caddy Wildcard Catch-All
- `https://` block at end of Caddyfile (catches everything not handled by explicit blocks)
- `on_demand_tls { ask http://localhost:9754/can-serve }` in global block
- Individual certs provisioned via HTTP-01 ACME on first request (no DNS plugin needed)
- CAA record already allows `issuewild "letsencrypt.org"` ✓

### 3. Aperture Ask Service (`aperture-ask.py`)
- Python micro-service on `:9754`
- Validates on-demand TLS cert requests: must be `*.primals.eco`, reasonable length, not an explicit service, valid characters
- Prevents cert flooding from abuse
- systemd service: `aperture-ask.service`, enabled, active

### 4. Aperture Module (`aperture.rs`)
- 343 lines, 9 tests, all passing
- `can_serve()` — validates TLS cert requests
- `resolve()` — maps subdomain → `ServeSite | Redirect | Honeycomb | Scatter | ExplicitService | NotFound`
- `APERTURE_SITES` — 9 static sites with 12 aliases
- `EPITOPE_CONCEPTS` — 16 concept→content redirects
- `HONEYCOMB_SUBDOMAINS` — 12 immune surface domains
- `EXPLICIT_SERVICES` — 14 services that keep own blocks

### 5. Honeycomb Consolidation
- Removed explicit 12-domain honeycomb block (~90 lines)
- All honeycomb features folded into wildcard `@is_honeycomb` handler:
  - IndexNow verification key
  - Dynamic robots.txt (per-subdomain)
  - Sitemap (cross-links real surfaces)
  - Floating pointer (WG mesh → Forgejo)
  - Agent passthrough (bearDog → Forgejo)
  - Cross-link headers (Link, X-Source-Mirror, X-Federation-Peer, etc.)
  - Default → scatter server with `X-Honeycomb` header

---

## Routing Table

| Pattern | Action | Example |
|---------|--------|---------|
| Known site | Serve static files | `thesis.primals.eco → /opt/ecoPrimals/thesis/public` |
| Site alias | Serve same content | `paper.primals.eco → thesis content` |
| Honeycomb | Scatter prism + cross-links | `bloom.primals.eco → scatter :9753` |
| Concept | 301 redirect | `metric-tensor.primals.eco → tuebor.primals.eco/analysis/metric-tensor/` |
| Unknown | Scatter maze | `xyzzy.primals.eco → scatter :9753` |
| Explicit service | Handled by own block | `git.primals.eco → Forgejo :3000` |

### Known Sites (9 + aliases)
sporeprint, thesis, signal, tuebor, detroit, clutch, gorilla, hypothesis, beacon

### Aliases (12)
paper→thesis, whitepaper→thesis, dashboard→signal, monitor→signal, questions→hypothesis, footprint→sporeprint, spore→sporeprint, print→sporeprint, evidence→detroit, cashforkids→detroit, commensal→beacon, guerillagorilla→gorilla

### Concept Redirects (7)
metric-tensor→tuebor, scyborg→sporeprint, license→sporeprint, methodology→sporeprint, outreach→sporeprint, hadr→sporeprint, desk→tuebor

### Explicit Services (23 blocks remaining)
git, forge, hud/biomeos/os, live, ca, depot, lab, membrane, primals.eco/www, sporeprint, thesis, signal, tuebor, detroit, clutch, gorilla, hypothesis, beacon, relay, barry, webb, footprint, nestgate.io

---

## Verification Results

| Test | Result |
|------|--------|
| thesis.primals.eco (explicit) | 200 ✓ |
| signal.primals.eco (explicit) | 200 ✓ |
| forge.primals.eco (explicit) | 200 ✓ |
| paper.primals.eco (wildcard alias) | 200 — cert provisioned, thesis content ✓ |
| whitepaper.primals.eco (alias) | 200 — thesis content ✓ |
| questions.primals.eco (alias) | 200 — hypothesis content ✓ |
| metric-tensor.primals.eco (concept) | 301 → tuebor analysis ✓ |
| scyborg.primals.eco (concept) | 301 → sporeprint license ✓ |
| hadr.primals.eco (concept) | 301 → HADR invitation ✓ |
| desk.primals.eco (concept) | 301 → tuebor desk ✓ |
| bloom.primals.eco (honeycomb) | 200 — scatter prism ✓ |
| bloom robots.txt | Dynamic per-subdomain ✓ |
| bloom sitemap.xml | Cross-links real surfaces ✓ |
| bloom cross-link headers | Link, X-Source-Mirror, etc. ✓ |
| IndexNow key | 200 ✓ |
| xyzzy.primals.eco (unknown) | 404 — scatter maze ✓ |
| Aperture ask (valid) | 200 ✓ |
| Aperture ask (explicit svc) | 403 ✓ |
| Aperture ask (wrong domain) | 403 ✓ |

---

## Commits

| Repo | Commit | Description |
|------|--------|-------------|
| skunkBat | `f145b52` | aperture module — wildcard membrane routing (9 tests) |
| plasmidBin | `ae15f83` | consolidate honeycomb into wildcard catch-all |
| wateringHole | `86a8203` | wildcard membrane LIVE — golgiBody head update |

---

## Known Remaining

1. **23 explicit blocks can be further consolidated** — the static site blocks (thesis, signal, tuebor, etc.) have Facebook OG blackwall handlers and other per-site features that the wildcard doesn't replicate yet. These can migrate to the wildcard over time.

2. **Deployed skunky-ingest binary diverged from local source** — the deployed binary has `--membrane-stack` and `--squirrel-announce` flags wired in main.rs that don't exist in the local git checkout. The aperture module was committed to git but the binary wasn't deployed (we restored the pre-aperture binary). The `/can-serve` and `/aperture-resolve` endpoints will go live when the source is synced and the binary is redeployed.

3. **Aperture ask runs as Python micro-service** — intended as a stopgap until the Rust scatter server gets the updated binary deployed. Once skunky-ingest is synced and redeployed, the ask endpoint can point back to `:9753/can-serve` and the Python service can be retired.

4. **skunkBat has 2 stashes** — stash@{0} is working directory from our pull-rebase, stash@{1} is the forward work (cube_oracle cross-frame mixing, scatter_defense trio_distribution, scatter_nft ribo prefix, main.rs federation simplify). Both are forward work awaiting review, not debris.

5. **Concept redirects are static** — the epitope concept routing is hardcoded in both `aperture.rs` and the Caddyfile. A future evolution could make this dynamic (scatter server queries a concept index and routes accordingly).

6. **SEO surface migration** — the user's vision is for SEO markup to move entirely to the aperture edge of the epitope sorter. Currently the static sites still carry their own SEO meta tags. The full vision is: the scatter server generates appropriate SEO markup based on what the visitor typed and who they are.

---

*Built beside the small. The subdomain is the epitope. The classifier is the aperture. The membrane breathes.*

— Artisan
