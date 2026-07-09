# Evolution AAR: DNS Cutover → Divergence Catalog

**Date**: 2026-07-09 (Wave 134k)
**Scope**: Complete DNS/TLS cutover retrospective — what worked, what broke,
every patch becomes a divergence for fractal/isomorphic evolution

---

## What Worked

### 1. Caddy as Host-routing TLS front door

Caddy on :443 handles all domains with zero configuration drama — ACME, HTTP/2,
HTTP/3 alt-svc, Host-based routing, file serving, reverse proxy. Every gate
deployment that needs a public TLS surface should use this pattern.

**Fractal pattern**: `Caddy :443 → Host routing → backend dispatch`

### 2. WireGuard backhaul mesh

The `golgi → sporeGate → ironGate` path works. Caddy reverse-proxies
`lab.primals.eco` through WireGuard to songBird's drawbridge on sporeGate,
which capability-routes to JupyterHub on ironGate. Three hops, fully sovereign.

**Fractal pattern**: `Public TLS → WireGuard → songBird capability routing → backend`

### 3. Thin Forgejo relay (shallow repos)

golgi disk went from 69% to 34% with depth=1 bare repos. Pushes work. Monthly
re-shallowing timer keeps it thin. Full history lives on sporeGate.

**Fractal pattern**: `Edge gate = shallow relay, compute gate = full history`

### 4. pepti depot + sovereign CI

All 15 primals cross-compiled for x86_64 + aarch64, checksummed, depot-synced
to golgi. Binary deployment is `rsync` from depot.

**Fractal pattern**: `sporeGate builds → depot → rsync to edge gates`

### 5. bearDog ACME capability

bearDog successfully obtained a Let's Encrypt certificate with multi-domain
SANs. The ACME client works. The CSR SAN fix was absorbed into the codebase.

**Fractal pattern**: `bearDog ACME = sovereign cert issuance per gate`

---

## What Broke — Each Patch Is a Divergence

Every item below was a runtime patch. Each one is now a divergence between
the current operational state and what the infra/topology should be for
fractal and isomorphic deployments.

### DIV-DNS-01: bearDog has no Host routing

**What broke**: bearDog on :443 proxied all traffic to a single upstream.
`git.primals.eco`, `membrane.primals.eco`, `lab.primals.eco` all got the
sporePrint homepage.

**Patch**: Restored Caddy on :443.

**Divergence**: bearDog's gatehouse mode is single-upstream TCP proxy. For
isomorphic deployments, each gate needs to handle N domains on :443 — either
bearDog learns SNI/Host dispatch, or every gate ships Caddy as the TLS front.

**Evolution path**:
- **Option A (bearDog evolves)**: Add `BEARDOG_GATEWAY_ROUTES` config —
  SNI-based dispatch to multiple upstreams. Requires TLS termination +
  HTTP parsing in bearDog.
- **Option B (Caddy canonical)**: Accept Caddy as the sovereign TLS layer.
  bearDog provides crypto identity + BTSP + ACME capability, Caddy does
  the HTTP routing. This is where we are today.
- **Recommended**: Option B now, Option A as a long-term bearDog milestone.
  Caddy is battle-tested and gives us HTTP/2, HTTP/3, automatic ACME, and
  Host routing. bearDog should focus on capabilities Caddy can't do (BTSP,
  primal identity, mesh auth).

**Isomorphic requirement**: Every gate's `provision-*.sh` must include Caddy
with Host-routing Caddyfile as the TLS surface pattern.

### DIV-DNS-02: HTTP/2 / ALPN regression

**What broke**: bearDog's raw TCP proxy doesn't negotiate ALPN. Browsers
fell back to HTTP/1.1.

**Patch**: Caddy on :443 restored HTTP/2 + HTTP/3 alt-svc.

**Divergence**: If bearDog ever takes TLS front-door duty, it must implement
ALPN negotiation (h2, http/1.1) during TLS handshake.

**Evolution path**: bearDog's `rustls` already supports ALPN — surface it
through the gatehouse config. Low priority while Caddy handles TLS.

### DIV-DNS-03: petalTongue assumed to be sporePrint file server

**What broke**: The cutover plan pointed bearDog upstream at petalTongue
(:8090), assuming it served the Zola static site. It serves a Gate Mesh
dashboard instead.

**Patch**: Added Caddy :8091 for static file serving.

**Divergence**: petalTongue's role was ambiguous. In the isomorphic topology,
petalTongue is a **visualization primal** — it renders ecosystem dashboards,
not static sites. The static site build pipeline (Zola) is a separate concern.

**Evolution path**:
- **Zola as sovereignty tool**: Zola is now installed on sporeGate (v0.22.1).
  sporePrint builds locally. This means sporeGate can build + deploy the
  static site without depending on golgi's Zola installation.
- **petalTongue as dynamic overlay**: petalTongue serves `/api/gates`,
  `/api/health`, `/api/metrics` on top of the Zola baseline. It's an
  enhancement, not a replacement.
- **Build pipeline**: `sovereign-ci` should include `zola build` as a cascade
  step, triggered by sporePrint commits.

### DIV-DNS-04: Subdomain port displacement (:8443)

**What broke**: Moving Caddy to :8443 broke all existing subdomain links.
External users, bookmarks, search engines — all expect :443.

**Patch**: Caddy restored to :443, :8443 eliminated.

**Divergence**: Port displacement is never acceptable for public-facing
services. The isomorphic topology must guarantee :443 for all TLS services
via Host-based routing.

**Evolution path**: Enforced in provisioning — `provision-*.sh` must never
move public-facing services off standard ports.

### DIV-DNS-05: CSR SAN missing in bearDog ACME

**What broke**: bearDog's `build_csr()` only set CN, not SAN extensions.
Multi-domain ACME orders require SANs.

**Patch**: Fixed `issuance.rs` to include `SubjectAltName` for all domains.

**Divergence**: This fix is in the codebase (`beardog-acme/src/client/issuance.rs`)
but needs a test. The ACME test suite should include multi-domain CSR
validation.

**Evolution path**: Add `#[test] fn csr_includes_all_sans()` to beardog-acme.
Every primal that generates X.509 artifacts should validate SAN completeness.

### DIV-DNS-06: Caddy cert renewal blocked by bearDog

**What broke**: When bearDog owned :80, Caddy couldn't renew its own LE
certs via HTTP-01. The existing certs expire Aug 13.

**Patch**: Caddy back on :443/:80 — it renews its own certs now. Problem
eliminated.

**Divergence**: This was a consequence of DIV-DNS-01. In any dual-TLS-server
topology, cert renewal ownership must be explicit. Either one server owns
all ACME, or they use different challenge types (HTTP-01 vs DNS-01).

**Evolution path**: If bearDog ever takes :443 again, it must either:
- Handle ACME for ALL domains on that IP, or
- Support DNS-01 challenges so Caddy can renew independently

### DIV-DNS-07: Stale content references (Cloudflare Tunnel)

**What broke**: `compute-access.md` still described Cloudflare Tunnel
architecture. The contact page was missing from the source tree.

**Patch**: Rewrote compute-access.md for songBird drawbridge. Created
contact.md.

**Divergence**: Content drift from infrastructure changes. The Zola site
describes an architecture that evolves independently of the content.

**Evolution path**: `spore-validate` should include a content-infra drift
check — scan markdown for known-stale patterns (e.g., "Cloudflare Tunnel",
"Cloudflare Access") and flag them. This is a natural extension of the
existing validation pipeline.

### DIV-DNS-08: Zola version skew (golgi 0.19.2 vs sporeGate 0.22.1)

**Discovery**: golgi runs Zola 0.19.2, sporeGate now has 0.22.1. The site
builds on both, but template features and performance differ.

**Divergence**: Tool version skew across gates.

**Evolution path**: Zola becomes a pepti-managed binary. Each gate pulls
Zola from the depot at a pinned version. `checksums.toml` includes `zola`
alongside the primals.

---

## Sovereignty Layer Status

The sovereignty goal: every tool in the build/deploy/serve pipeline is either
a primal or a depot-managed binary. No external package managers, no cloud
services, no vendor lock-in.

| Tool | Status | Gate(s) | Path to Sovereignty |
|------|--------|---------|---------------------|
| **Caddy** | Deployed | golgi | Add to pepti depot (static binary) |
| **Zola** | Installed | sporeGate (0.22.1), golgi (0.19.2) | Add to pepti depot, pin version |
| **Forgejo** | Deployed | golgi | Already managed via provision script |
| **Rust/Cargo** | Installed | sporeGate | Build tool, stays on compute gate |
| **cross** | Installed | sporeGate | Cross-compile tool, stays on compute gate |
| **WireGuard** | Deployed | golgi, sporeGate, ironGate, flockGate | Kernel module + wg-quick |
| **rsync** | System | all | Standard tool, no action needed |
| **bearDog** | Depot binary | all | Already in pepti depot |
| **songBird** | Depot binary | golgi, sporeGate | Already in pepti depot |
| **membrane** | Depot binary | all | Already in pepti depot |
| **JupyterHub** | pip install | ironGate | Stays as Python tool on compute gate |
| **RustDesk** | Binary | golgi | Add to pepti depot |

### New sovereignty additions this wave:

1. **Zola v0.22.1** — installed on sporeGate at `/usr/local/bin/zola`. Can
   build sporePrint locally (239 pages, 15s). Next: add to pepti depot as
   `zola` binary for both x86_64 and aarch64.

2. **Caddy** — should be depot-managed. Currently installed ad-hoc on golgi.
   The static binary is ideal for pepti — no runtime dependencies.

---

## Isomorphic Deployment Checklist

For any new gate to be isomorphic with golgi, it needs:

```
Gate Provisioning Isomorphism:
  ☑ Caddy :443 with Host-routing Caddyfile
  ☑ WireGuard backhaul to mesh
  ☑ songBird for capability routing + federation
  ☑ bearDog for crypto identity + BTSP
  ☑ Forgejo shallow relay (if edge gate)
  ☑ UFW with standard ports only (:443, :80, :2222, :51820)
  ☑ pepti depot binaries for all services
  ☐ Zola for sporePrint build (sovereignty layer)
  ☐ sovereign-ci cascade trigger
  ☐ automatic cert management (Caddy ACME)
```

### Fractal Pattern: The "golgi Template"

Every edge gate deployment should be derivable from `provision-golgi.sh` by
changing:
- Gate name and WireGuard keys
- Domain names in Caddyfile
- Upstream IPs for reverse proxy targets
- Forgejo repo list (or skip Forgejo for non-forge gates)

The script structure — install tools → configure services → write systemd
units → enable firewall → enable services — is the fractal template.

---

## Divergence Summary Table

| ID | Severity | Patch Applied | Evolution Target |
|----|----------|---------------|------------------|
| DIV-DNS-01 | CRITICAL | Caddy restored :443 | bearDog SNI dispatch or Caddy canonical |
| DIV-DNS-02 | HIGH | Caddy HTTP/2 | bearDog ALPN if/when it takes TLS |
| DIV-DNS-03 | HIGH | Caddy :8091 static | Zola sovereignty + petalTongue overlay |
| DIV-DNS-04 | HIGH | Standard ports restored | Provisioning rule: never displace ports |
| DIV-DNS-05 | MEDIUM | CSR SAN fix | Add ACME test coverage |
| DIV-DNS-06 | MEDIUM | Caddy owns ACME | Single ACME owner per IP |
| DIV-DNS-07 | LOW | Content rewritten | spore-validate content drift checks |
| DIV-DNS-08 | LOW | Zola installed both | Zola in pepti depot, pinned version |

---

## Architecture — Current Production (Post-134k)

```
Internet
  │
  └── golgi (157.230.3.183) — thin edge relay
      │
      ├── Caddy :443 (ACME, HTTP/2, Host routing)
      │   ├── primals.eco      → file_server (Zola static)
      │   ├── www.primals.eco  → 301 → primals.eco
      │   ├── membrane.*       → depot + health + nestgate
      │   ├── git.*            → Forgejo :3000
      │   └── lab.*            → WireGuard → sporeGate songBird :7780
      │
      ├── Caddy :80 (ACME HTTP-01 + HTTPS redirect)
      │
      ├── bearDog (standby, port 9999)
      │   └── ACME cert ready for primals.eco + www
      │
      ├── Forgejo :3000 / :2222 (shallow bare repos)
      │
      ├── songBird (mesh federation + TURN relay)
      │
      └── WireGuard :51820 → sporeGate (10.13.37.2)

sporeGate (10.13.37.2) — sovereign compute
  │
  ├── Full git mirrors (/opt/forgejo-mirror/)
  ├── pepti depot (/opt/ecoPrimals/depot/)
  ├── Rust/Cargo/cross (build toolchain)
  ├── Zola v0.22.1 (sporePrint builder) ← NEW
  ├── songBird (drawbridge + capability routing)
  ├── sovereign-ci (build + deploy cascade)
  │
  └── WireGuard → ironGate (10.13.37.7), flockGate (10.13.37.3)
```

---

## Next Steps

1. **Add Zola to pepti depot** — download musl binaries for both arches,
   checksum, add to `checksums.toml`. Pin at v0.22.1.
2. **Add Caddy to pepti depot** — same pattern. Pin version.
3. **Wire `zola build` into sovereign-ci** — cascade step triggered by
   sporePrint commits. Build on sporeGate, rsync `public/` to golgi.
4. **bearDog ACME tests** — multi-domain CSR validation test.
5. **spore-validate content drift** — scan for stale infra references.
6. **Upgrade golgi Zola** — 0.19.2 → 0.22.1 from pepti depot.
7. **Provision template** — extract `provision-golgi.sh` into a
   parameterized template for fractal gate deployment.
