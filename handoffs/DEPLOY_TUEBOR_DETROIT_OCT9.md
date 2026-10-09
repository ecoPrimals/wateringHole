# Deploy: tuebor + detroit + Fleet DNS — Oct 9

**Priority:** HIGH — site rebuild + fleet DNS records
**Date:** October 9, 2026 09:05 AM

---

## What Needs to Happen

Pull latest and rebuild both Zola sites on golgiBody.

### tuebor (barry.primals.eco)

```bash
cd /srv/tuebor && git pull origin main && zola build
```

**3 new pages + 4 modified:**

| New Page | Path | What It Is |
|----------|------|-----------|
| How To Build an OS | `/analysis/how-to-build-an-os/` | Dykema dark money architecture — kernel/scheduler/process table. Bipartisan bus. SDJ phone = Dykema phone. |
| Infrastructure Grid | `/analysis/infrastructure-grid/` | Fluorescent tag map — 11 nodes where entity infra touches individual privacy. FOIAworks + LakeNet + GoDaddy + M365 + SDJ + ONF + RFFW. |

| Modified Page | What Changed |
|---------------|-------------|
| `_index.md` (homepage) | New "Infrastructure Studies" section added to Analysis |
| `analysis/_index.md` | Reorganized — Infrastructure Studies + Pattern Analysis sections |
| `evidence/foiaworks-infrastructure.md` | Added Related Pages cross-links (grid, OS, LakeNet) |
| `analysis/lakenet-signal-trace.md` | Added Related Pages cross-links (grid, OS, FOIAworks) |

### detroit (detroit.primals.eco)

```bash
cd /srv/detroit && git pull origin main && zola build
```

**1 new page:**

| New Page | Path | What It Is |
|----------|------|-----------|
| How To Build an OS | `/analysis/how-to-build-an-os/` | Detroit-framed version — SDJ → PCA → 3% math. Same data, school extraction framing. |

**Note:** detroit origin (Forgejo) is unreachable — pull from GitHub remote:
```bash
cd /srv/detroit && git pull github main && zola build
```

---

## Verify After Build

```bash
curl -s https://barry.primals.eco/analysis/how-to-build-an-os/ | head -20
curl -s https://barry.primals.eco/analysis/infrastructure-grid/ | head -20
curl -s https://detroit.primals.eco/analysis/how-to-build-an-os/ | head -20
```

Should return page-specific HTML, not the homepage.

---

## Context

This session produced an unsupervised OSINT pass that found:
- Renae Moore = Dykema staff on 5 dark money boards
- SDJ phone (517-374-9100) = Dykema Lansing office
- Knox = former Ethics Board running dark money
- Wilk = Chatfield + Snyder + Duggan + Barrett
- RFFW LLC = $1M money laundering complaint (same Wilk/Moore)

All written up as publishable analysis. Cross-linked across every existing evidence page. The tuebor site is now a self-contained reference — point anyone to it and the whole grid lights up.

---

## Fleet DNS — Cloudflare Records to Add

All 4 new bodies are live. Add A records in Cloudflare → primals.eco → DNS:

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| A | `golgi-de` | `2.28.141.35` | DNS only (grey) | Auto |
| A | `golgi-jp` | `207.182.107.135` | DNS only (grey) | Auto |
| A | `golgi-us` | `40.160.96.29` | DNS only (grey) | Auto |
| A | `golgi-in` | `172.232.85.202` | DNS only (grey) | Auto |

This creates:
- `golgi-de.primals.eco` → Hetzner Falkenstein
- `golgi-jp.primals.eco` → Vultr Tokyo
- `golgi-us.primals.eco` → OVH Virginia
- `golgi-in.primals.eco` → Linode Mumbai

Grey cloud (DNS only) so Caddy gets raw traffic for TLS + fleet fingerprinting.

## Fleet IP Registry (COMPLETE)

| Body | Provider | IP | Region | Jurisdiction |
|------|----------|-----|--------|-------------|
| golgiBody | DigitalOcean | 157.230.3.183 | NYC, US | US federal |
| golgiHetzner | Hetzner | 2.28.141.35 | Falkenstein, DE | German StGB §202a + GDPR |
| golgiVultr | Vultr | 207.182.107.135 | Tokyo, JP | Japan APPI |
| golgiOVH | OVH | 40.160.96.29 | Virginia, US | US federal |
| golgiLinode | Linode | 172.232.85.202 | Mumbai, IN | India IT Act |

## Provision Order (after DNS propagates)

SSH from sporeGate to each new body, run the provision script:

```bash
# Verify SSH access
ssh root@2.28.141.35 hostname        # golgiHetzner
ssh root@207.182.107.135 hostname     # golgiVultr
ssh root@40.160.96.29 hostname        # golgiOVH
ssh root@172.232.85.202 hostname      # golgiLinode

# Then provision each (Caddy + skunky-ingest + honeycomb)
# Use the provision-golgi script from wateringHole/provision/
```
