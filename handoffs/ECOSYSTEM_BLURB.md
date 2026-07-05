# ecoPrimals Ecosystem Blurb — Wave 132g

**Date**: Jul 5, 2026 10:23 EDT | **Wave**: 132g | **From**: eastGate overwatch
**Posture**: **DRAWBRIDGE SHIPPED** — songBird 16435b36 drawbridge HTTP listener (:7780). bearDog 2ac2bd389 upstream fix. Architecture gap closed. Both on Forgejo, CI triggered.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Wave 132g status**: **Gatehouse/Darkforest architecture complete.** bearDog IS the gateway. songBird IS the drawbridge.

**RESOLVED (cumulative)**:
1. ~~bearDog `CryptoProvider` missing~~ → **FIXED** (7e932000f + 136857739 defensive).
2. ~~bearDog `BindMode::Auto`~~ → **FIXED** (7e932000f): Platform-aware detection. grapheneGate unblocked.
3. ~~Bidirectional relay not deployed~~ → **DEPLOYED** on golgi (membrane 0704132). 39/39 parity.
4. ~~bearDog ACME EdDSA rejection~~ → **FIXED** (136857739): ES256 (P-256) signing.
5. ~~Port 80 conflict~~ → **SOLVED** (16430d90c): Http01Solver now dual-purpose (ACME + HTTPS redirect). No Caddy needed.
6. ~~No gatehouse mode~~ → **SHIPPED** (16430d90c): `BEARDOG_GATEHOUSE_MODE=true` activates :443 + :80 unified.
7. ~~HTTP-to-IPC bridge gap~~ → **SHIPPED** (songBird 16435b36): drawbridge HTTP listener on :7780. Accepts plain HTTP, routes via CapabilityProxyRouter to backends.
8. ~~bearDog upstream default wrong~~ → **FIXED** (2ac2bd389): default upstream 7700→7780 (drawbridge, not federation).

**REMAINING**:
9. **sporeGate: cutover** — deploy bearDog 2ac2bd389 + songBird 16435b36, activate gatehouse + drawbridge. Updated FRAGO below.
10. **DNS**: `lab.primals.eco` points to golgi (157.230.3.183), not sporeGate. Either update DNS or use golgi as front proxy to sporeGate.
11. **ironGate: deploy JupyterHub** → still NOT STARTED. E2E blocker.

**Architecture standard published**: `GATEHOUSE_DARKFOREST_STANDARD.md` — defines gatehouse (known entry), darkforest (invisible mesh), drawbridge (songBird http.proxy crossing point).

---

## flockGate — bearDog / songBird / skunkBat

**Role**: Tower atomic home (songBird, bearDog, skunkBat development)
**Status**: All debt resolved. **Drawbridge + gatehouse upstream fix shipped. No blocking work.**

### RESOLVED (Wave 132f-g)

- **bearDog 7e932000f**: CryptoProvider init + BindMode::Auto platform detection
- **bearDog 136857739**: ES256 signing (Ed25519 → ECDSA P-256), defensive CryptoProvider install, dep promotion
- **bearDog 16430d90c**: Gatehouse mode (`BEARDOG_GATEHOUSE_MODE=true`), HTTP→HTTPS 301 redirect on :80, dual-purpose Http01Solver
- **bearDog 2ac2bd389**: Gateway upstream default → :7780 (drawbridge, not federation :7700)
- **songBird 16435b36**: Drawbridge HTTP listener (`serve_drawbridge`), path→capability routing, `SONGBIRD_DRAWBRIDGE_ROUTES` config
- **skunkBat e7eaa5d**: `CapabilityClient` extraction (DRY ~120 lines), quarantine persistence, nested metrics. 541 tests.

### Ongoing

- WAN peering via golgi relay: `songBird mesh.init` with `bootstrap_peers = ["10.13.37.1:7700"]`
- Continued evolution of Tower atomic as needed

### Ongoing: WAN peering via golgi relay

- `songBird` on flockGate needs `mesh.init` with `bootstrap_peers = ["10.13.37.1:7700"]` (golgi relay)
- Low priority — LAN mesh is operational

### Push Protocol

**IMPORTANT**: Push to BOTH remotes after every commit:
```bash
git push origin main && git push forgejo main
```
flockGate previously pushed only to GitHub, causing divergence. sporeGate pulls from Forgejo for Sovereign CI.

---

## sporeGate — cellMembrane / Sovereign CI / Gateway Deploy

**Role**: Public entry point, builder, gateway host
**Status**: **CUTOVER READY (v2).** Architecture gap solved. New binaries building on Sovereign CI.

### Current State

- **songBird 16435b36 (on Forgejo, building)**: Drawbridge HTTP listener (:7780) — accepts HTTP, routes via CapabilityProxyRouter
- **bearDog 2ac2bd389 (on Forgejo, building)**: Gatehouse mode + upstream default → :7780 (drawbridge)
- **Caddy**: RETIRED (already stopped + disabled by sporeGate team)
- **golgi Caddy**: Currently proxying `lab.primals.eco` → `10.13.37.2:7700` (wrong port — update to :7780)
- **cellMembrane**: 930 tests, gateway refactored, `relay.config` + `relay.status` commands
- **golgi relay**: ✅ bidirectional relay DEPLOYED + LIVE (39/39 parity, membrane 0704132)

### NEXT: Cutover v2 (Updated FRAGO)

**DNS issue identified**: `lab.primals.eco` → 157.230.3.183 (golgi VPS). ACME HTTP-01 needs port 80 on the machine the DNS points to.

**Option A: golgi as front proxy (quick, working now)**
```bash
# On golgi — update Caddy proxy target to drawbridge port
# lab.primals.eco:443 → TLS terminate → proxy 10.13.37.2:7780 (songBird drawbridge on sporeGate)
# golgi holds the cert (existing), songBird drawbridge routes to backends
```

**Option B: Update DNS to sporeGate public IP (sovereign)**
```bash
# Update Cloudflare: lab.primals.eco → sporeGate public IP
# Then bearDog ACME issues cert directly
# Requires CF_API_TOKEN or DNS-01 challenge, OR sporeGate must have a public IP
```

**Option C: golgi runs bearDog gatehouse (DNS stays)**
```bash
# bearDog on golgi for TLS + ACME (it's the IP DNS points to)
# Proxies to sporeGate:7780 via WireGuard overlay (10.13.37.2:7780)
# golgi IS the gatehouse, sporeGate IS the drawbridge
```

### Deployment Steps (once binaries built)

1. Deploy songBird 16435b36 on sporeGate
2. Configure: `SONGBIRD_DRAWBRIDGE_ADDR=127.0.0.1:7780` + `SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter`
3. Deploy bearDog 2ac2bd389 on sporeGate (or golgi per DNS decision)
4. Configure: `BEARDOG_GATEHOUSE_MODE=true` + `BEARDOG_GATEWAY_UPSTREAM=127.0.0.1:7780`
5. Update golgi Caddy: proxy target → `10.13.37.2:7780` (temporary until DNS resolved)
6. Validate: `curl -I http://lab.primals.eco` → 301 (via golgi) or via bearDog directly

### Sovereign CI Note

Pull from **Forgejo** (`git.primals.eco`). Bidirectional relay ensures Forgejo↔GitHub parity (39/39). Use `membrane relay.parity` to verify.

---

## ironGate — GPU Compute / JupyterHub / ABG

**Role**: RTX 5070 GPU compute, JupyterHub host for ABG citizen science
**Status**: songBird running, mesh peered, firewall open. **JupyterHub NOT STARTED (blocker).**

### P1: Deploy JupyterHub

This is the **E2E critical path blocker**. The Caddy route on sporeGate is already configured to proxy to ironGate:8000.

**Steps**:
1. Install Docker (if not present): `curl -fsSL https://get.docker.com | sh`
2. Deploy JupyterHub:
```bash
docker run -d --name jupyterhub \
  --restart unless-stopped \
  -p 127.0.0.1:8000:8000 \
  -v /opt/jupyterhub/data:/data \
  -e JUPYTER_ENABLE_LAB=yes \
  jupyterhub/jupyterhub:latest
```
3. Validate: `curl -s http://localhost:8000/hub/api | jq .version`

### P2: Register `jupyter` capability

After JupyterHub is running:
```bash
socat - UNIX-CONNECT:/run/songbird/songbird.sock <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"primal.announce","params":{"capabilities":["jupyter"],"endpoint":"http://127.0.0.1:8000"}}
EOF
```

### P3: Bioinformatics stack

- salmon, STAR, R/Bioconductor, DESeq2, WGCNA
- Pilot dataset: GSE166686 (RNA-seq, will be staged from eastGate)

### Hardware

- RTX 5070 Ti (16GB VRAM) — GROMACS metadynamics, CUDA workloads
- Connected via House 2 WiFi bridge → Omada → CRS310 → LAN (.237)
- WireGuard: 10.13.37.7
- Firewall: 7700/tcp + 8000/tcp open from 192.168.4.0/22

---

## eastGate — Overwatch / primalSpring / petalTongue

**Role**: Coordination hub, primalSpring validation, petalTongue/sporePrint
**Status**: primalSpring validating Tower + compute contracts. All overwatch items current.

### Completed This Wave

- primalSpring 49e760d: `s_compute_hosting_contract` (116 scenarios, 1080 tests) — validates JupyterHub E2E path, jupyter registry domain (ironGate affinity), Tower composition gateway
- primalSpring 58d4167: `s_beardog_startup_contract`, relay registry, LAN bypass SSOT from TOML
- petalTongue 0f8da6b: deep debt — clippy zero, main.rs extract, deny.toml evolve
- ~~bearDog BindMode::Auto fix~~ → absorbed upstream by flockGate

### Pending

- Stage pilot dataset to ironGate (after JupyterHub)
- Continue cascade + overwatch duties

---

## golgi — VPS / Relay / Forgejo

**Role**: WireGuard hub, Forgejo host, depot, cascade timer, relay chain
**Status**: ✅ Bidirectional relay DEPLOYED + LIVE. 39/39 repos at parity. No more silent divergence.

### Completed

- `relay.absorb()` deployed — detects GitHub-ahead repos, fetches, FF-merges, pushes to Forgejo
- `relay.parity()` deployed — reports divergence direction + commit counts
- Cascade timer evolved from bash to `membrane relay.run` (bidirectional)
- 39/39 repos verified at parity

### Operator Action: CF_API_TOKEN

Provision Cloudflare API token on golgi `tower.env`. One-time action that unlocks agentic DNS management (`dns.update`, `cache.purge`).

---

## grapheneGate — Pixel 8a / Mobile Trust Anchor

**Role**: Portable trust anchor, Tower atomic on Android, cellular relay
**Status**: 14/14 binaries running via ADB. **BindMode::Auto fix landed — ready for Android rebuild.**

### NEXT

- Rebuild bearDog for Android target (7e932000f includes BindMode::Auto platform detection)
- Deploy → abstract socket IPC works automatically via `ANDROID_ROOT` env detection
- `songBird mesh.init` with eastGate as bootstrap peer
- Cellular relay for out-of-LAN mesh access

---

## Code Metrics

| Repo | Tests | Status |
|------|-------|--------|
| cellMembrane | 930 | Evolved (gateway refactor + relay.config + relay.status) |
| primalSpring | 1,080 | Evolved (116 scenarios, compute_hosting_contract) |
| songBird | 8,929+ | LIVE on sporeGate (http.proxy routing) |
| bearDog | 13,866+ | ✅ ACME-ready (136857739: ES256 + CryptoProvider + BindMode) |
| skunkBat | 541 | Evolved (CapabilityClient, quarantine persist, nested metrics) |
| petalTongue | 363+ | Evolved (deep debt, clippy zero) |
| sporePrint | 220 | Evolved (v0.3.1 living topology) |
| barraCuda | 4,619 | Stable |
| coralReef | 3,631 | Stable |
| toadStool | 9,171+ | Stable |
| biomeOS | 8,351 | Stable |
| sweetGrass | 1,658 | Stable |

---

## Critical Path Summary

```
✅ flockGate: bearDog CryptoProvider + BindMode::Auto FIXED (7e932000f)
✅ flockGate: bearDog ES256 signing FIXED (136857739)
✅ flockGate: bearDog GATEHOUSE MODE shipped (16430d90c) — :443 TLS + :80 ACME/redirect
✅ eastGate: songBird DRAWBRIDGE shipped (16435b36) — :7780 HTTP→capability routing
✅ eastGate: bearDog upstream fix (2ac2bd389) — default → :7780 not :7700
✅ golgi: bidirectional relay DEPLOYED (39/39 parity, membrane 0704132)
✅ eastGate: GATEHOUSE_DARKFOREST_STANDARD.md published
✅ sporeGate: Caddy RETIRED (stopped + disabled)

NEXT (all operational — no code fixes remaining):
DNS decision: lab.primals.eco currently → golgi (157.230.3.183)
    Option A: golgi proxies to sporeGate:7780 (fast, working NOW)
    Option B: Update DNS to sporeGate public IP (sovereign)
    Option C: golgi IS the gatehouse (bearDog on golgi)

sporeGate: deploy songBird 16435b36 + bearDog 2ac2bd389
    → configure SONGBIRD_DRAWBRIDGE_ROUTES + BEARDOG_GATEHOUSE_MODE
        → songBird drawbridge + bearDog gateway LIVE
            → TOWER HTTP FULLY SOVEREIGN

ironGate: deploy JupyterHub (parallel, no dependency on above)
    → register jupyter capability via SONGBIRD_PROXY_ROUTES
        → E2E: browser → bearDog → drawbridge → ironGate → JupyterHub
```

---

*Wave 132g — Full Gatehouse/Darkforest stack shipped. Only deployment + DNS remain. No code blockers.*
