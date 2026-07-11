# External Review Response — Wave 136b

**Date**: 2026-07-11
**Context**: External reviewer examined the ecosystem post-DNS cutover and raised
concerns about sovereignty vs infrastructure resilience. This documents the actual
state and what remains to address.

---

## Reviewer's Observations (paraphrased)

1. `lab.primals.eco` JupyterHub served over HTTP, not HTTPS
2. Cloudflare removal means loss of DDoS absorption and edge caching
3. "One tower behind a residential connection" is vulnerable to traffic spikes
4. Suggests a static CDN mirror (GitHub Pages or Cloudflare free tier) as front door

## Corrections to Reviewer's Model

### Not residential — VPS

The public-facing surface (`primals.eco`, `git.primals.eco`, `lab.primals.eco`,
`membrane.primals.eco`, `live.primals.eco`) runs on **golgiBody**, a DigitalOcean
VPS in NYC1 (157.230.3.183). This is datacenter infrastructure with:
- DigitalOcean's upstream DDoS mitigation
- 1Gbps network
- NYC peering

The LAN gates (eastGate, ironGate, southGate, etc.) are residential hardware but
they are NOT the public-facing surface. They connect to golgi via WireGuard overlay.
sporeGate (the build authority) connects via WireGuard to golgi.

The reviewer's concern about "residential connection" applies only to the
WireGuard tunnel between sporeGate and golgi, which is a backend path — not the
public-facing path.

### lab.primals.eco HTTP — Already Addressed

This was **EXP-06** (lab auth-gate). The JupyterHub warning was because the
songBird drawbridge proxy (internal to WireGuard) was HTTP between golgi and
sporeGate. The TLS termination happens at Caddy on golgi — the browser gets
HTTPS. The internal hop is over an encrypted WireGuard tunnel.

The reviewer saw this during a window before CSP and security headers were
deployed. As of Wave 136a:
- All 5 public domains have HSTS preload (2yr), security headers, CSP
- `lab.primals.eco` has `(csp_proxy)` policy allowing WebSocket for JupyterHub
- Caddy terminates TLS for all domains (ACME auto-renewal confirmed)

EXP-06 (auth-gate at Caddy layer) is still pending — this adds basic_auth or
mTLS before the drawbridge, which is defense-in-depth.

### Cloudflare Was Outer Membrane Only

Per the diderm architecture (`DIDERM_DOMAIN_ARCHITECTURE.md`), Cloudflare was
the **outer membrane** for `primals.eco`. The inner membrane (`primal.eco`,
`nestgate.io`) was always sovereign (knot-dns, bearDog ACME).

The DNS cutover moved `primals.eco` from Cloudflare to sovereign Caddy on golgi.
This was intentional and planned — criterion 8 of the glacial shift. We hardened
the outer membrane (9/14 exposures closed) precisely because we knew we were
losing Cloudflare's automatic protections.

## What We Have (Post-Cloudflare)

| Protection | Cloudflare (was) | Sovereign (now) |
|-----------|------------------|-----------------|
| TLS termination | Cloudflare edge | Caddy ACME on golgi |
| DDoS | Cloudflare (enterprise-grade) | iptables 50 conn/10s per IP (basic) |
| Edge caching | Cloudflare CDN (global) | None (golgi serves direct) |
| WAF | Cloudflare (managed rules) | None (skunkBat HTTP anomaly detection, not inline) |
| Bot management | Cloudflare (managed) | fail2ban on SSH, nothing on HTTP |
| Security headers | Cloudflare (configured) | Caddy snippets (HSTS, CSP, X-Frame, etc.) |
| HTTP/3 | Cloudflare | Caddy (H3 alt-svc announced) |
| Cert management | Cloudflare (automatic) | Caddy ACME (automatic, validated) |

## What We Lost and What Matters

**Lost — matters for HN moment**:
- Enterprise DDoS absorption (the "hug of death" concern)
- Global edge caching (latency for non-NYC visitors)

**Lost — acceptable**:
- Cloudflare WAF (we have skunkBat + CSP + rate limiting instead)
- Bot management (robots.txt + fail2ban is sufficient for current scale)

**Retained or improved**:
- TLS (Caddy ACME is as good as Cloudflare for cert management)
- Security headers (CSP is stricter than what we had on Cloudflare)
- HTTP/3 (Caddy announces H3 alt-svc)
- SSH protection (fail2ban is active and already banning)

## Reviewer's Suggestion: Static CDN Mirror

The suggestion to put a static mirror on a CDN (GitHub Pages, Cloudflare free
tier) for traffic spike absorption is **architecturally sound** and maps to
the diderm model:

```
Traffic spike → CDN copy of sporePrint (static pitch + guideStone download)
                    ↓ (links to sovereign for live content)
Normal traffic → golgi (sovereign Caddy, full site)
```

This is the outer membrane doing what outer membranes do: absorbing environmental
stress so the inner membrane can function. The CDN would serve:
- Landing page (static HTML, the pitch)
- guideStone download links (ecoBin binaries from a CDN-hosted copy)
- Content that doesn't change often (thesis, philosophy, architecture)

The sovereign golgi would serve:
- Live API endpoints (membrane, nestGate coordination)
- Lab access (songBird drawbridge)
- Forgejo (git.primals.eco)
- Everything that requires sovereign compute

**This is EXP-08 (GitHub trailing shadow) repurposed**. We already have GitHub
as an "acceptable" trailing mirror. The suggestion is to make that mirror
explicitly serve as the CDN front door for traffic spikes.

## The MacGuffin Test: Defense in Depth, Not Obscurity

The reviewer's instinct was to hide behind a CDN. The ecosystem's thesis is the
opposite: **if the architecture is sound, showing it publicly is validation, not
vulnerability.** Security through obscurity is the MacGuffin — a plot device
that has no real substance.

The ecosystem's security model is built on:
- **Mathematics**: ChaCha20-Poly1305 (bearDog), BLAKE3 content-addressing
  (rhizoCrypt), ed25519 signing (SIGN-01), formal proofs (gen3 thesis)
- **Defense in depth**: diderm membranes, WireGuard overlay, fail2ban, CSP,
  rate limiting, skunkBat anomaly detection — independent layers, each
  sufficient without the others
- **Transparency**: 301 pages of published architecture, thesis, lab notebooks.
  The entire system design is on `primals.eco` for anyone to read.

If we can't show how it works and remain secure, we don't have security — we
have a MacGuffin. The answer to "what if someone reads the architecture docs
and attacks us?" should be "then every layer holds independently."

### sporePrint as Live Topology Visualization

This framing elevates sporePrint from a static documentation site to a live
proof of the system. The evolution target:

```
sporePrint today:    301 static pages (Zola)
sporePrint target:   Live topology visualization
                     — gate status (which gates are online)
                     — mesh connectivity (WireGuard overlay map)
                     — membrane layers (inner/outer, what each protects)
                     — security posture (which exposures are closed)
                     — wave state (current blurb, recent AARs)
```

This is the convergence point for:
- **petalTongue** (dynamic rendering engine)
- **nestGate coordination backend** (topology data store)
- **songBird mesh** (live gate status via mesh heartbeats)
- **footPrint** (GIS visualization tech — same approach applied to network topology)

The live topology visualization IS the security argument. It shows an observer
exactly how the system works and why each layer holds. This is the opposite of
the CDN mirror suggestion — instead of hiding behind a CDN, we show the CDN
is unnecessary because the architecture is self-evident.

### CDN Mirror — Repositioned

The CDN mirror (SURGE-01) remains valid but is repositioned: it's not about
hiding the sovereign surface, it's about **availability** during traffic
spikes. The CDN serves a cached copy of the public proof, not a substitute
for it. The sovereign surface is the authoritative source.

## Recommended Actions

| ID | Action | Owner | Priority |
|----|--------|-------|----------|
| TOPO-VIS | sporePrint live topology visualization (petalTongue + nestGate + songBird) | sporePrint + petalTongue | HIGH |
| SURGE-01 | GitHub Pages as availability mirror (cached copy of sporePrint, not a hiding place) | sporePrint + sporeGate | LOW |
| SURGE-02 | golgi connection capacity test (sustained load, DO bandwidth limits) | sporeGate | LOW |
| EXP-06 | Lab auth-gate (already tracked) | sporeGate | HIGH |

---

*External review absorbed as data point. Architecture is sound — reviewer's
residential assumption was incorrect (VPS, not residential). DDoS gap is real
but bounded by VPS upstream mitigation. Primary response: defense in depth and
mathematics, not obscurity. sporePrint evolves to show the live topology as
proof. If we can't show how it works, it's a MacGuffin.*
