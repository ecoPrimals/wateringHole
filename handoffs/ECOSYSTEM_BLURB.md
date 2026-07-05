# ecoPrimals Ecosystem Blurb — Wave 132f

**Date**: Jul 5, 2026 08:14 EDT | **Wave**: 132f | **From**: eastGate overwatch
**Posture**: **DEBT RESOLUTION** — Tower HTTP integration exposed blockers. songBird http.proxy LIVE, bearDog ACME panics, relay needs deploy.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. This is the single source of truth for all teams. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Wave 132 shipped**: 3-gate LAN mesh LIVE (eastGate ↔ sporeGate ↔ ironGate), cross-gate `capability.call` validated, songBird `http.proxy` deployed on sporeGate, petalTongue living topology wired, sporePrint v0.3.1. primalSpring: 114 scenarios / 1078 tests.

**Architecture**: sporeGate is public entry (`lab.primals.eco`). Caddy → songBird → mesh → compute backends (LAN: ironGate/strandGate, WAN: flockGate via golgi relay). songBird IS the port solver — no external ports exposed.

---

## flockGate — bearDog / songBird / skunkBat

**Role**: Tower atomic home (songBird, bearDog, skunkBat development)
**Status**: Code-complete on Tower HTTP. **2 P1 debt items found during deploy.**

### P1 DEBT: bearDog `CryptoProvider` missing at startup

**Problem**: `beardog-cli/src/main.rs` never calls `rustls_rustcrypto::provider().install_default()`. When sporeGate deployed bearDog (ff18b17f5) and attempted ACME gateway startup, it panics at:

```
beardog-acme/src/rustls_provider.rs:30
  "rustls CryptoProvider not installed — binary must call
   rustls_rustcrypto::provider().install_default() at startup"
```

Both `serve_https_gateway()` and `build_http_client()` call `assert_installed()` which triggers this panic in production (`#[cfg(not(test))]` path).

**Fix**: Add one line near the top of `main()` in `crates/beardog-cli/src/main.rs`, before any ACME or TLS operations:

```rust
#[tokio::main]
async fn main() -> Result<(), BearDogError> {
    let _ = rustls_rustcrypto::provider().install_default();
    
    let cli = Cli::parse();
    // ...
```

**Acceptance**: `beardog server --gateway` no longer panics. ACME cert issuance succeeds on sporeGate :443.

### P1 DEBT: bearDog `BindMode::Auto` not merged

**Problem**: `BindMode::Auto` always evaluates to `false` — never auto-detects abstract sockets on Android/grapheneGate. A local fix exists on eastGate but was never pushed upstream.

**Fix**: In `crates/beardog-cli/src/handlers/server/mod.rs`, replace the flat boolean:

```rust
let use_abstract =
    args.bind_mode == crate::BindMode::Abstract || args.r#abstract;
```

With platform-aware detection:

```rust
let use_abstract = match args.bind_mode {
    crate::BindMode::Abstract => true,
    crate::BindMode::Auto => {
        if args.r#abstract {
            true
        } else {
            cfg!(target_os = "android") || {
                std::env::var("ANDROID_ROOT").is_ok()
                    || std::env::var("ANDROID_DATA").is_ok()
            }
        }
    }
    _ => args.r#abstract,
};
```

**Acceptance**: `beardog server --bind-mode auto` correctly uses abstract sockets on grapheneGate (Pixel 8a).

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
**Status**: songBird http.proxy LIVE. bearDog deployed but ACME blocked. Awaiting flockGate fix.

### Current State

- **songBird 906fe886**: Deployed, running, `http.proxy` routes configured via `SONGBIRD_PROXY_ROUTES`
- **bearDog ff18b17f5**: Deployed but ACME gateway panics (see flockGate P1 above)
- **Caddy**: Remains production TLS terminator until bearDog ACME works
- **cellMembrane**: 926 tests, bidirectional relay code merged (fce96e2)

### P2: Deploy bidirectional relay to golgi

The `relay.absorb()` + `relay.parity()` code (commit fce96e2) is merged but not deployed to golgi. The 15min cascade timer on golgi needs the updated `membrane` binary to run reverse-sync (GitHub → Forgejo).

**Steps**:
1. Build `membrane` binary from cellMembrane HEAD (8cb7784)
2. Push to golgi: `/usr/local/bin/membrane`
3. Restart cascade-pull.timer
4. Validate: `membrane relay.parity` shows all repos at parity

### P2: bearDog ACME activation (after flockGate fix)

Once flockGate pushes the CryptoProvider fix:
1. Rebuild bearDog on Sovereign CI (triggered by Forgejo push)
2. Deploy new binary to sporeGate
3. `beardog server --gateway` on :443
4. Validate ACME cert issuance for `lab.primals.eco`
5. Begin 7-day shadow period (Caddy + bearDog in parallel)
6. Retire Caddy after shadow passes

### Sovereign CI Note

Pull from **Forgejo** (`git.primals.eco`). All gate teams must push to Forgejo for CI to trigger. If you see stale code, run `membrane relay.parity` to check.

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
**Status**: All local work shipped. Monitoring + cascade.

### Completed This Wave

- primalSpring: 114 scenarios, 1078 tests, `s_tower_http_gateway` scenario validates Tower contract
- petalTongue: DataService → mesh.peers wired, `/api/mesh-peers` endpoint, 363 tests
- sporePrint: v0.3.1 living topology page
- bearDog BindMode::Auto fix (local, needs push to flockGate)

### Pending

- Push `BindMode::Auto` fix to bearDog origin+forgejo (or hand to flockGate to absorb)
- Stage pilot dataset to ironGate (after JupyterHub)
- Continue cascade + overwatch duties

---

## golgi — VPS / Relay / Forgejo

**Role**: WireGuard hub, Forgejo host, depot, cascade timer, relay chain
**Status**: Running. Relay is unidirectional (Forgejo → GitHub only). **Needs bidirectional upgrade.**

### P2: Deploy updated membrane binary

cellMembrane fce96e2 adds `relay.absorb()` — detects when GitHub is ahead of Forgejo and pulls changes back. Currently golgi's relay only pushes outward.

**After deploy**: the 15min cascade timer will automatically fix any GitHub↔Forgejo drift.

### Operator Action: CF_API_TOKEN

Provision Cloudflare API token on golgi `tower.env`. One-time action that unlocks agentic DNS management (`dns.update`, `cache.purge`).

---

## grapheneGate — Pixel 8a / Mobile Trust Anchor

**Role**: Portable trust anchor, Tower atomic on Android, cellular relay
**Status**: 14/14 binaries running via ADB. **Blocked on bearDog `BindMode::Auto`.**

### Pending

- bearDog `BindMode::Auto` fix lands → rebuild for Android target → abstract socket IPC works
- `songBird mesh.init` with eastGate as bootstrap peer
- Cellular relay for out-of-LAN mesh access

---

## Code Metrics

| Repo | Tests | Status |
|------|-------|--------|
| cellMembrane | 926 | Evolved (bidirectional relay) |
| primalSpring | 1,078 | Evolved (114 scenarios) |
| songBird | 8,929+ | LIVE on sporeGate |
| bearDog | 13,866+ | **DEBT** (2 P1 fixes needed) |
| skunkBat | 539 | Evolved (security.advisory) |
| petalTongue | 363 | Evolved (mesh.peers wired) |
| sporePrint | 220 | Evolved (v0.3.1 living topology) |
| barraCuda | 4,619 | Stable |
| coralReef | 3,631 | Stable |
| toadStool | 9,171+ | Stable |
| biomeOS | 8,351 | Stable |
| sweetGrass | 1,658 | Stable |

---

## Critical Path Summary

```
flockGate: fix bearDog CryptoProvider + BindMode::Auto
    → push to origin + forgejo
        → sporeGate: Sovereign CI rebuilds bearDog
            → sporeGate: deploy → ACME gateway :443 works
                → 7-day shadow → Caddy retirement
                    → TOWER HTTP FULLY SOVEREIGN

ironGate: deploy JupyterHub (parallel, no dependency on above)
    → register jupyter capability
        → E2E: browser → bearDog → songBird → ironGate → JupyterHub
```

---

*Wave 132f — debt exposed, fixes scoped, paths clear. Each gate has exactly what it needs.*
