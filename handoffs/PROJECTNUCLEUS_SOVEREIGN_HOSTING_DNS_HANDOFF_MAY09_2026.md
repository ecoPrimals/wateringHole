# projectNUCLEUS: Sovereign Hosting + DNS Metadata Closure

**Date**: 2026-05-09
**From**: projectNUCLEUS (sporeGarden)
**For**: primalSpring, Songbird team, BearDog team, petalTongue team, NestGate team
**Phase**: 60+ — sovereign intermediate layer

---

## Context

GitHub Pages went down. primals.eco went down with it. A site about sovereign
computing depended entirely on a single external service. We fixed that.

---

## 1. Dual-Hosted primals.eco (Operational)

### What was done

primals.eco now serves from the active gate via Cloudflare tunnel, with GitHub
Pages available as a one-command fallback. The gate builds the same Zola static
site locally and serves it on port 8880.

### Architecture

```
External visitor → Cloudflare edge → tunnel → gate:8880 → Zola static build
                                                         (sporePrint public/)
```

### Components

| Component | File | Purpose |
|-----------|------|---------|
| Zola binary | `/usr/local/bin/zola` (v0.22.1) | Builds sporePrint to static HTML |
| Build/serve script | `deploy/sporeprint_local.sh` | `build` / `serve` / `once` modes |
| Persistent service | `~/.config/systemd/user/sporeprint-local.service` | Serves public/ on 127.0.0.1:8880 |
| Rebuild timer | `~/.config/systemd/user/sporeprint-rebuild.timer` | Pull + build every 15 minutes |
| Tunnel ingress | `~/.cloudflared/config.yml` | `primals.eco → http://127.0.0.1:8880` |
| DNS management | `deploy/sporeprint_dns.sh` | Cloudflare API: `sovereign`/`external`/`status`/`verify` |
| Verification | `deploy/sporeprint_verify.sh` | Dual-origin checks, integrated into `tier_test_all.sh` |
| API token | `~/.cloudflared/cf_api_token` (mode 600) | Cloudflare DNS Edit, scoped to primals.eco |

### DNS switching (one command)

```bash
deploy/sporeprint_dns.sh sovereign    # gate serves primals.eco
deploy/sporeprint_dns.sh external     # GitHub Pages serves primals.eco
deploy/sporeprint_dns.sh status       # show current routing
deploy/sporeprint_dns.sh verify       # check which origin is actually serving
```

### Performance

- Zola build: ~590ms for 90 pages (129 HTML files, 19 MB)
- Response time: 100-130ms through tunnel (Cloudflare ORD edge)
- Rebuild: 15-minute timer, or on-demand via `systemctl --user restart sporeprint-local`

---

## 2. DNS Metadata Leak Closure

### The problem

The gate was using AT&T's ISP resolver (192.168.1.254) for all DNS queries.
This meant AT&T could see every domain the gate resolved — a metadata leak
that the BTSP/Songbird P2P layer is designed to eliminate long-term.

### The fix

`/etc/systemd/resolved.conf` switched to DNS-over-TLS:

- **Primary**: 1.1.1.1 (Cloudflare) via TLS
- **Fallback**: 9.9.9.9 (Quad9) via TLS
- **ISP**: Bypassed entirely
- **DNSSEC**: `allow-downgrade` (validates when available)

### Metadata leak status

| Layer | Leak? | What sees what | Closes when |
|-------|-------|---------------|-------------|
| ISP (AT&T) | **CLOSED** | Sees encrypted TLS traffic to 1.1.1.1, no query content | Done |
| DoT provider (Cloudflare 1.1.1.1) | OPEN | Sees query content (trusted, not sovereign) | H2-20: local recursive resolver (unbound) |
| Cloudflare proxy | OPEN | Sees all HTTP traffic (tunnel terminates at edge) | H2 Step 3b/3c: BearDog TLS + Songbird NAT |
| DNS system itself | OPEN | Domain resolution is publicly observable | H2-19: BTSP direct resolution |

### Sovereignty progression

```
Before:  Gate → AT&T DNS (plaintext) → Cloudflare edge → tunnel → gate
Now:     Gate → Cloudflare DoT (encrypted) → Cloudflare edge → tunnel → gate
Next:    Gate → local unbound → root servers (encrypted) → Cloudflare edge → tunnel → gate
Phase 3: Gate → Songbird mesh → peer resolution → direct P2P (no DNS, no tunnel)
```

---

## 3. Upstream Gaps and Evolution Targets

### For Songbird (NAT traversal — H2-13, H2-14, H2-16)

The Cloudflare tunnel is the current NAT punch-through. Songbird's STUN/TURN
client replaces this entirely. The tunnel works today but Cloudflare sees all
traffic. Songbird NAT traversal closes the last major metadata leak.

**Concrete ask**: Production-ready STUN client that maintains a persistent
hole-punch through consumer NAT (AT&T BGW320 in this case). Fallback chain:
direct → STUN → TURN → cloudflared emergency.

### For BearDog (TLS + ACME — H2-10, H2-11)

BearDog TLS with Let's Encrypt would allow the gate to terminate TLS directly
instead of relying on Cloudflare's edge. Combined with Songbird NAT, this
eliminates Cloudflare from the data path entirely.

**Concrete ask**: X.509 certificate issuance via ACME (Let's Encrypt), SNI-based
routing, auto-renewal. Rate limiting for direct-exposed endpoints.

### For petalTongue (web serving — H2-06)

petalTongue replaces the Python HTTP server and Zola entirely. It would serve
NestGate-backed content with DataBinding for live science visualization.

**Concrete ask**: `--docroot` web mode serving static files from NestGate content
store. Config schema for web mode. Catch-all route handling for static assets.

### For NestGate (content pipeline — H2-05)

NestGate provides the content-addressed storage backend for sporePrint. The
current Zola build produces files that could be `content.put` into NestGate
for petalTongue to serve.

**Concrete ask**: `content.put` method, collection/directory concept, content-type
metadata, blob listing for manifest generation.

### Existing upstream gaps (unchanged)

| ID | What | Owner | Status |
|----|------|-------|--------|
| DF-2 | toadstool `TOADSTOOL_AUTH_MODE` env var mapping | toadStool | Open |
| DF-3 | songbird/squirrel silent on `auth.mode` TCP | Each team | Open |
| U1 | primalSpring `CHECKSUMS` stale | primalSpring | Open |
| U2 | 5 deploy graphs missing `by_capability` | primalSpring | Open |
| U3 | 8 profile graphs missing `bonding_policy` | primalSpring | Open |
| U5 | sweetGrass port 39085 vs 9850 | sweetGrass | Resolved (v0.7.32) |
| JH-11 | Cross-primal token federation | biomeOS/primalSpring | Deferred (Tier 4) |

---

## 4. Patterns Learned

| Pattern | Implementation | Relevance |
|---------|---------------|-----------|
| Pre-primal sovereignty | Zola + Python HTTP + tunnel = functional sovereign hosting without primal stack | Intermediate steps validate the architecture before primal parity |
| DNS-over-TLS as metadata closure | systemd-resolved DoT config | Closes ISP surveillance without primal changes |
| API-driven DNS switching | Cloudflare API token + bash script | One-command origin switching; pattern for any DNS-managed failover |
| Timer-based content sync | systemd timer pulls + builds every 15 min | Content freshness without push infrastructure |
| Dual-origin verification | `sporeprint_verify.sh` checks both origins + tunnel + build | Verification loop catches outages on either side |

---

## 5. What This Proves

- **The site survived a GitHub outage** — the sovereign gate served primals.eco
  while GitHub Pages was down
- **The sovereignty roadmap has a concrete intermediate step** — Zola + tunnel
  is pragmatic, not aspirational
- **DNS metadata leaks are closeable incrementally** — each step reduces the
  attack surface without waiting for the full primal stack
- **Every external outage is a live demo** of why sovereign hosting matters

---

## References

- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — full sovereignty roadmap
- `projectNUCLEUS/specs/TUNNEL_EVOLUTION.md` — tunnel replacement plan
- `projectNUCLEUS/specs/SOVEREIGNTY_VALIDATION_PROTOCOL.md` — calibrate/shadow/cutover
- `projectNUCLEUS/specs/GATE_PORTABILITY.md` — gate-portable architecture
- `projectNUCLEUS/deploy/sporeprint_dns.sh` — DNS switching script
- `projectNUCLEUS/deploy/sporeprint_local.sh` — build/serve script
- `projectNUCLEUS/deploy/sporeprint_verify.sh` — dual-origin verification
