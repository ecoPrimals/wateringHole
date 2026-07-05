# ecoPrimals Ecosystem Blurb — Wave 132g

**Date**: Jul 5, 2026 09:42 EDT | **Wave**: 132g | **From**: eastGate overwatch
**Posture**: **GATEHOUSE ACTIVE** — bearDog 16430d90c: gatehouse mode (:443 TLS + :80 ACME/redirect). Caddy fully replaceable. Sovereign CI triggered. sporeGate cutover FRAGO dispatched.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Wave 132g status**: **Gatehouse/Darkforest architecture shipped.** bearDog IS the sovereign gateway.

**RESOLVED (cumulative)**:
1. ~~bearDog `CryptoProvider` missing~~ → **FIXED** (7e932000f + 136857739 defensive).
2. ~~bearDog `BindMode::Auto`~~ → **FIXED** (7e932000f): Platform-aware detection. grapheneGate unblocked.
3. ~~Bidirectional relay not deployed~~ → **DEPLOYED** on golgi (membrane 0704132). 39/39 parity.
4. ~~bearDog ACME EdDSA rejection~~ → **FIXED** (136857739): ES256 (P-256) signing.
5. ~~Port 80 conflict~~ → **SOLVED** (16430d90c): Http01Solver now dual-purpose (ACME + HTTPS redirect). No Caddy needed.
6. ~~No gatehouse mode~~ → **SHIPPED** (16430d90c): `BEARDOG_GATEHOUSE_MODE=true` activates :443 + :80 unified.

**REMAINING**:
7. **sporeGate: cutover** — stop Caddy, deploy bearDog 16430d90c, activate gatehouse mode. FRAGO dispatched.
8. **ironGate: deploy JupyterHub** → still NOT STARTED. E2E blocker.

**Architecture standard published**: `GATEHOUSE_DARKFOREST_STANDARD.md` — defines gatehouse (known entry), darkforest (invisible mesh), drawbridge (songBird http.proxy crossing point).

---

## flockGate — bearDog / songBird / skunkBat

**Role**: Tower atomic home (songBird, bearDog, skunkBat development)
**Status**: All debt resolved. **Gatehouse mode shipped (16430d90c). No blocking work remaining.**

### RESOLVED (Wave 132f-g)

- **bearDog 7e932000f**: CryptoProvider init + BindMode::Auto platform detection
- **bearDog 136857739**: ES256 signing (Ed25519 → ECDSA P-256), defensive CryptoProvider install, dep promotion
- **bearDog 16430d90c**: Gatehouse mode (`BEARDOG_GATEHOUSE_MODE=true`), HTTP→HTTPS 301 redirect on :80, dual-purpose Http01Solver
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
**Status**: **GATEHOUSE CUTOVER READY.** bearDog 16430d90c on Forgejo, Sovereign CI building. FRAGO dispatched.

### Current State

- **songBird 906fe886**: Deployed, running, `http.proxy` routes LIVE via `SONGBIRD_PROXY_ROUTES`
- **bearDog 16430d90c (on Forgejo, building)**: Gatehouse mode + ES256 + CryptoProvider + BindMode::Auto
- **Caddy**: Still running — **RETIRE after bearDog deploy** (see FRAGO)
- **cellMembrane**: 930 tests, gateway refactored, `relay.config` + `relay.status` commands
- **golgi relay**: ✅ bidirectional relay DEPLOYED + LIVE (39/39 parity, membrane 0704132)

### NEXT: Gatehouse Cutover (FRAGO dispatched)

See `FRAGO_SPOREGATE_GATEHOUSE_CUTOVER_WAVE132G_JUL05_2026.md` for exact steps:
1. Deploy bearDog 16430d90c from Sovereign CI
2. Stop + disable Caddy
3. Start bearDog with `BEARDOG_GATEHOUSE_MODE=true`
4. Validate: ACME cert + HTTP redirect + HTTPS proxy
5. Caddy permanently retired

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
✅ golgi: bidirectional relay DEPLOYED (39/39 parity, membrane 0704132)
✅ eastGate: GATEHOUSE_DARKFOREST_STANDARD.md published

NEXT:
sporeGate: deploy bearDog 16430d90c from Sovereign CI (building now)
    → stop Caddy (permanently)
        → start bearDog BEARDOG_GATEHOUSE_MODE=true
            → ACME cert auto-issues (port 80 FREE)
                → TOWER HTTP FULLY SOVEREIGN ← imminent

ironGate: deploy JupyterHub (parallel, no dependency on above)
    → register jupyter capability
        → E2E: browser → bearDog → songBird → ironGate → JupyterHub
```

---

*Wave 132g — Gatehouse/Darkforest architecture live. Tower atomic IS the castle wall. Caddy retirement imminent. Only operational deployment remains.*
