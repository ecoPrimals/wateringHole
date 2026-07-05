# ecoPrimals Ecosystem Blurb — Wave 132g

**Date**: Jul 5, 2026 09:31 EDT | **Wave**: 132g | **From**: eastGate overwatch
**Posture**: **ACME READY** — bearDog ES256 signing fix (136857739) pushed to Forgejo. Sovereign CI triggered. ACME gateway code-correct. Remaining scheduling item: port 80 conflict (Caddy holds :80, bearDog HTTP-01 needs it). ironGate JupyterHub still not started.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Wave 132g status**: sporeGate evolved bearDog ACME — ES256 signing fix + defensive CryptoProvider.

**RESOLVED (cumulative)**:
1. ~~bearDog `CryptoProvider` missing~~ → **FIXED** (7e932000f + 136857739 defensive).
2. ~~bearDog `BindMode::Auto`~~ → **FIXED** (7e932000f): Platform-aware detection. grapheneGate unblocked.
3. ~~Bidirectional relay not deployed~~ → **DEPLOYED** on golgi (membrane 0704132). 39/39 parity.
4. ~~bearDog ACME EdDSA rejection~~ → **FIXED** (136857739): ES256 (P-256) signing. Let's Encrypt accepts JWS.
5. ~~rustls-rustcrypto dev-dep only~~ → **FIXED** (136857739): promoted to regular dep in beardog-acme.

**REMAINING**:
6. **Port 80 conflict**: Caddy holds :80, bearDog HTTP-01 solver needs it. **Scheduling decision** — stop Caddy HTTP listener temporarily OR switch to DNS-01 challenge. Not a code fix.
7. **ironGate: deploy JupyterHub** → still NOT STARTED. E2E blocker.

**New evolution absorbed this cascade**:
- bearDog 136857739: ES256 signing (jws.rs + account.rs), defensive CryptoProvider, dep promotion. Pushed to Forgejo, Sovereign CI triggered.
- primalSpring 49e760d: `s_compute_hosting_contract` scenario (116 total, 1080 tests) — validates JupyterHub E2E path, jupyter registry domain, Tower gateway composition.
- golgi: membrane 0704132 deployed, `relay.config` shows both remotes, bidirectional cascade timer.

**Architecture**: sporeGate is public entry (`lab.primals.eco`). Caddy → songBird → mesh → compute backends (LAN: ironGate/strandGate, WAN: flockGate via golgi relay). songBird IS the port solver — no external ports exposed.

---

## flockGate — bearDog / songBird / skunkBat

**Role**: Tower atomic home (songBird, bearDog, skunkBat development)
**Status**: All debt resolved. **No blocking work remaining.**

### RESOLVED (Wave 132f-g)

- **bearDog 7e932000f**: CryptoProvider init + BindMode::Auto platform detection
- **bearDog 136857739**: ES256 signing (Ed25519 → ECDSA P-256), defensive CryptoProvider install, dep promotion
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
**Status**: songBird http.proxy LIVE. **bearDog ES256 fix (136857739) on Forgejo — CI triggered. Port 80 scheduling decision needed.**

### Current State

- **songBird 906fe886**: Deployed, running, `http.proxy` routes LIVE via `SONGBIRD_PROXY_ROUTES`
- **bearDog 136857739 (on Forgejo)**: ES256 signing + defensive CryptoProvider. Sovereign CI triggered.
- **Caddy**: Production TLS (:443) + HTTP (:80). **Holds port 80** that bearDog HTTP-01 solver needs.
- **cellMembrane**: 930 tests, gateway refactored, `relay.config` + `relay.status` commands
- **golgi relay**: ✅ bidirectional relay DEPLOYED + LIVE (39/39 parity, 15min timer, membrane 0704132)

### NEXT: ACME Activation — Port 80 Decision

bearDog ACME code is now correct (ES256, defensive CryptoProvider). The one remaining issue is **port 80**:

**Option A: Temporarily stop Caddy's HTTP listener**
```bash
# In Caddyfile, comment out HTTP→HTTPS redirect
# Or: caddy stop, start bearDog ACME, cert acquired, caddy start
```

**Option B: Switch to DNS-01 challenge (no port 80 needed)**
- Requires `CF_API_TOKEN` on sporeGate (same token needed on golgi anyway)
- bearDog uses Cloudflare DNS API to prove domain ownership
- More robust long-term (no port conflict ever)

**Option C: Shadow cutover** (recommended)
1. Build bearDog 136857739, deploy
2. Stop Caddy entirely (brief downtime ~30s)
3. Start bearDog ACME on :80 + :443
4. Cert issues via HTTP-01
5. If fails → restart Caddy (rollback)
6. If succeeds → bearDog owns both ports, Caddy retired

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
✅ golgi: bidirectional relay DEPLOYED (39/39 parity, membrane 0704132)

NEXT:
sporeGate: build bearDog 136857739 from Sovereign CI
    → deploy to sporeGate
        → PORT 80 DECISION (stop Caddy or DNS-01)
            → ACME cert issuance for lab.primals.eco
                → TOWER HTTP FULLY SOVEREIGN

ironGate: deploy JupyterHub (parallel, no dependency on above)
    → register jupyter capability
        → E2E: browser → bearDog → songBird → ironGate → JupyterHub
```

---

*Wave 132g — ACME code-correct. Remaining items are operational (port scheduling + JupyterHub deploy), not code fixes.*
