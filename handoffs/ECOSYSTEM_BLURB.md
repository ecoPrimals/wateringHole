# ecoPrimals Ecosystem Blurb — Wave 132f

**Date**: Jul 5, 2026 09:03 EDT | **Wave**: 132f | **From**: eastGate overwatch
**Posture**: **INTEGRATION READY** — Both P1 bearDog fixes merged (7e932000f). Bidirectional relay deployed + live on golgi (39/39 parity). sporeGate needs to rebuild bearDog and activate ACME gateway. ironGate JupyterHub remains parallel blocker.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Wave 132f status**: All P1 debt **RESOLVED** by gate teams within 1 hour of dispatch.

**RESOLVED this cycle**:
1. ~~bearDog `CryptoProvider` missing~~ → **FIXED** (7e932000f): flockGate added `install_default()` to `main()`.
2. ~~bearDog `BindMode::Auto`~~ → **FIXED** (7e932000f): Platform-aware detection. grapheneGate unblocked.
3. ~~Bidirectional relay not deployed~~ → **DEPLOYED** on golgi. 39/39 repos at parity.

**REMAINING**:
4. **sporeGate: rebuild bearDog** (7e932000f on Forgejo) → deploy → activate ACME :443.
5. **ironGate: deploy JupyterHub** → still NOT STARTED. E2E blocker.

**New evolution absorbed**:
- skunkBat e7eaa5d: `CapabilityClient` extraction, quarantine persistence, nested metrics. 541 tests.
- primalSpring 58d4167: `s_beardog_startup_contract` scenario (115 total), relay registry. 1079 tests.
- cellMembrane 0704132: gateway config.rs extracted, `relay.config` + `relay.status` commands. 930 tests.
- petalTongue 0f8da6b: deep debt — clippy zero, main.rs extract, deny.toml evolve.

**Architecture**: sporeGate is public entry (`lab.primals.eco`). Caddy → songBird → mesh → compute backends (LAN: ironGate/strandGate, WAN: flockGate via golgi relay). songBird IS the port solver — no external ports exposed.

---

## flockGate — bearDog / songBird / skunkBat

**Role**: Tower atomic home (songBird, bearDog, skunkBat development)
**Status**: All P1 debt RESOLVED. skunkBat evolved. **No blocking work.**

### RESOLVED (Wave 132f)

- **bearDog 7e932000f**: CryptoProvider init + BindMode::Auto — both P1 fixes landed, pushed to both remotes.
- **skunkBat e7eaa5d**: `CapabilityClient` extraction (DRY ~120 lines), quarantine persistence (`quarantine.json`), nested `SecurityMetrics`. 541 tests.

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
**Status**: songBird http.proxy LIVE. **bearDog P1 fix on Forgejo — ready to rebuild + activate ACME.**

### Current State

- **songBird 906fe886**: Deployed, running, `http.proxy` routes LIVE via `SONGBIRD_PROXY_ROUTES`
- **bearDog ff18b17f5 (stale)**: Deployed but panics on ACME. **7e932000f now on Forgejo** — fix is ready.
- **Caddy**: Remains production TLS terminator until new bearDog deployed
- **cellMembrane**: 930 tests, gateway refactored, `relay.config` + `relay.status` commands
- **golgi relay**: ✅ bidirectional relay DEPLOYED + LIVE (39/39 parity, 15min timer)

### NEXT: Rebuild + Deploy bearDog 7e932000f → ACME Activation

bearDog P1 fix is on Forgejo (7e932000f). Sovereign CI should trigger (or manually kick):
1. Build bearDog from Forgejo HEAD (7e932000f) — includes CryptoProvider + BindMode::Auto
2. Deploy new binary: `/usr/local/bin/beardog`
3. `beardog server --gateway` on :443
4. Validate ACME cert issuance for `lab.primals.eco`
5. Begin 7-day shadow period (Caddy + bearDog :443 in parallel)
6. Retire Caddy after shadow passes

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
**Status**: All work shipped. primalSpring validating Tower contracts. Overwatch monitoring.

### Completed This Wave

- primalSpring 58d4167: `s_beardog_startup_contract` (115 scenarios, 1079 tests) — validates CryptoProvider init, BindMode::Auto, TLS ownership, Tower startup ordering
- primalSpring: relay registry added (`[relay]` domain → cellMembrane methods), LAN bypass SSOT (TOML-derived zones)
- petalTongue 0f8da6b: deep debt — clippy zero warnings, main.rs extract, deny.toml evolve
- sporePrint: v0.3.1 living topology page
- ~~bearDog BindMode::Auto fix~~ → absorbed by flockGate (7e932000f)

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
| primalSpring | 1,079 | Evolved (115 scenarios, s_beardog_startup_contract) |
| songBird | 8,929+ | LIVE on sporeGate (http.proxy routing) |
| bearDog | 13,866+ | ✅ P1 FIXED (7e932000f) — ready for rebuild |
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
✅ golgi: bidirectional relay DEPLOYED (39/39 parity)

NEXT:
sporeGate: Sovereign CI rebuild bearDog 7e932000f
    → deploy to sporeGate
        → ACME gateway :443 activates
            → 7-day shadow → Caddy retirement
                → TOWER HTTP FULLY SOVEREIGN

ironGate: deploy JupyterHub (parallel, no dependency on above)
    → register jupyter capability
        → E2E: browser → bearDog → songBird → ironGate → JupyterHub
```

---

*Wave 132f — P1 debt resolved. Integration path: sporeGate rebuilds bearDog, ironGate deploys JupyterHub. Both can proceed independently.*
