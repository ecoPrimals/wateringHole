# ecoPrimals Ecosystem Blurb — Wave 132g

**Date**: Jul 5, 2026 12:50 EDT | **Wave**: 132g | **From**: eastGate overwatch
**Posture**: **FULL MESH READY** — bearDog Android fix shipped (6ef436864). pepti warehouse LIVE. Drawbridge LIVE. Zero code blockers. All gates can now mesh.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Goal**: Get all gates across LAN and WAN fully meshed — capable of routing any capability request to any gate without manual port configuration.

---

## Status: ALL REPOS AT PARITY

```
✅ bearDog       6ef436864  (gatehouse + drawbridge upstream + Android fix)
✅ songBird      16435b36   (drawbridge HTTP listener :7780)
✅ skunkBat      e7eaa5d    (capabilityClient + quarantine)
✅ sweetGrass    bab4657    (stable)
✅ cellMembrane  c83bcbc    (relay + freshness + gateway refactor)
✅ wateringHole  071ec76    (standards + FRAGOs + ownership model)
✅ sporePrint    99bfc9e    (living topology + 254 tests)
✅ primalSpring  cac3eec    (117 scenarios, 1081 tests)
✅ petalTongue   0f8da6b    (deep debt zero)
✅ rhizoCrypt    ef85124    (stable)
✅ toadStool     1ec37498   (stable)
✅ barraCuda     b2618db0   (stable)
✅ coralReef     3078d0b    (stable)
```

Zero divergence. GitHub↔Forgejo bidirectional relay running (golgi membrane 0704132, 15min cascade timer).

**Pepti Warehouse**: LIVE at `membrane.primals.eco/depot/`. songBird x86_64 (23MB) + aarch64 (21MB) available. bearDog x86_64 (11MB) available. bearDog aarch64 building (6ef436864 fix just pushed, CI triggered).

---

## REMAINING: What Blocks Full Mesh

### ~~P0: Deploy Drawbridge~~ DONE

sporeGate deployed songBird drawbridge LIVE on :7780. golgi Caddy updated to proxy to :7780. E2E path works (returns 502 — backend not started yet).

### P1: ironGate JupyterHub

E2E backend. Without this, the drawbridge routes to nothing (returns 502).

```bash
# On ironGate (192.168.4.237 / WG 10.13.37.7):
docker run -d --name jupyterhub \
  --restart unless-stopped \
  -p 127.0.0.1:8000:8000 \
  -v /opt/jupyterhub/data:/data \
  jupyterhub/jupyterhub:latest

# Validate:
curl -s http://localhost:8000/hub/api | jq .version
```

### P2: LAN Mesh Peering (ironGate + strandGate)

Both are on the LAN (192.168.4.x), both have songBird running. Need `mesh.init`:

```bash
# On ironGate and strandGate:
socat - UNIX-CONNECT:/run/songbird/songbird.sock <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"mesh.init","params":{"bootstrap_peers":["10.13.37.2:7700"]}}
EOF
```

This joins them to sporeGate's mesh. Then capability discovery works automatically.

### P3: WAN Mesh Peering (flockGate via golgi relay)

flockGate is remote — needs golgi as relay:

```bash
# On flockGate:
SONGBIRD_PEERS=10.13.37.1:7700 songbird serve
# Or via mesh.init:
{"jsonrpc":"2.0","id":1,"method":"mesh.init","params":{"bootstrap_peers":["10.13.37.1:7700"]}}
```

golgi (10.13.37.1) relays between flockGate and the LAN mesh.

### P4: DNS Resolution

`lab.primals.eco` → 157.230.3.183 (golgi VPS). Current quickest path:
- golgi Caddy proxies `lab.primals.eco` → `10.13.37.2:7780` (sporeGate drawbridge via WG overlay)
- This works NOW — just needs the port update from 7700→7780

Long-term sovereign: bearDog gatehouse on golgi (it's the IP DNS points to).

### P5: grapheneGate (Mobile Mesh)

Android rebuild with BindMode::Auto (landed in 7e932000f). Then `mesh.init` via eastGate bootstrap.

---

## Gate Ownership & Responsibilities

### sporeGate (sporeGate overwatch team)

**Owns**: the gate, LAN topology, membrane layers, Sovereign CI, pepti warehouse

1. **Deploy songBird 16435b36** → start drawbridge on :7780
2. **Deploy bearDog 2ac2bd389** → gatehouse ready (hold for DNS decision)
3. **Update golgi Caddy** → proxy target `10.13.37.2:7780`
4. **Build multi-arch ecobins** → Sovereign CI produces:
   - `x86_64-unknown-linux-gnu` (sporeGate, ironGate, strandGate, eastGate)
   - `aarch64-linux-android` (grapheneGate)
5. **Publish to pepti warehouse** → `/opt/ecoPrimals/depot/` on golgi (accessible via WG overlay)
6. **Validate**: `curl http://lab.primals.eco/hub/api` via golgi → drawbridge → ironGate
7. **LAN mesh topology**: ensure ironGate + strandGate peered via `mesh.init`

### ironGate (sporeGate overwatch team — LAN compute)

1. **Start JupyterHub** (docker, port 8000, localhost only)
2. **mesh.init** → join sporeGate mesh (bootstrap `10.13.37.2:7700`)
3. **Register jupyter capability** via IPC
4. **Pull binaries from pepti warehouse** for upgrades

### flockGate (WAN validation — inner membrane behaviors)

**Role**: WAN deployment target for validating membrane behaviors across non-LAN links.

1. **mesh.init** via golgi relay (`10.13.37.1:7700`)
2. **Validate WAN relay path**: capability.call across golgi relay roundtrip
3. **Test membrane behaviors**: relay.absorb, relay.parity, remote dispatch over WAN latency
4. No code work remaining — all debt resolved

### eastGate (eastGate hardware team)

**Owns**: overwatch coordination, primalSpring, petalTongue, grapheneGate hardware

1. Overwatch: cascade + verify mesh convergence
2. **grapheneGate deploy** from pepti warehouse (see below)
3. Stage pilot dataset to ironGate after JupyterHub lands
4. Continue primalSpring scenario evolution

### grapheneGate (eastGate hardware team — deploys from pepti)

**Owns**: Pixel 8a hardware. **Deploys from ecobins via pepti warehouse, not local builds.**

Deployment flow:
```
sporeGate Sovereign CI (Forgejo push trigger)
    → cross-compile aarch64-linux-android targets
    → publish to pepti warehouse (golgi:/opt/ecoPrimals/depot/android/)
    → eastGate pulls via WG overlay or golgi relay
    → ADB push to grapheneGate

Enables: cross-hardware validation without local cross-compilation
```

Steps:
1. **Pull Android ecobins** from pepti warehouse (golgi depot)
2. **ADB deploy**: `adb push depot/beardog-aarch64 /data/local/tmp/beardog`
3. **Start primal suite** (14 binaries via termux/shell)
4. **mesh.init** with eastGate as bootstrap peer (USB tether or WiFi)
5. **Validate**: abstract socket IPC (BindMode::Auto), cellular relay fallback

### golgi (infrastructure — relay + depot)

1. **Update Caddy**: `lab.primals.eco` proxy → `10.13.37.2:7780`
2. **Pepti warehouse**: serve `/opt/ecoPrimals/depot/` for gate deployments
3. Relay continues (15min timer, 39/39 parity)
4. Future: bearDog gatehouse here (owns DNS IP)

---

## Architecture (Gatehouse/Darkforest + Pepti Warehouse)

```
INTERNET → Cloudflare → golgi :443 (Caddy TLS, temporary)
    → WG overlay → sporeGate :7780 (songBird drawbridge)
        → path routing → capability.call → mesh
            → ironGate :8000 (JupyterHub)
            → strandGate (compute)
            → flockGate via golgi relay (WAN validation)

Build/Deploy (Pepti Layer):
Forgejo push → sporeGate Sovereign CI
    → compile x86_64 + aarch64-android
    → publish → golgi:/opt/ecoPrimals/depot/ (pepti warehouse)
    → gates pull binaries via WG overlay
    → cross-hardware validation (grapheneGate, ironGate, etc.)

Future (once bearDog gatehouse on golgi):
INTERNET → golgi :443 (bearDog TLS) → :7780 (drawbridge) → mesh
```

**Darkforest**: all gates communicate via songBird mesh (UDS, abstract sockets, WG direct-connect). No ports exposed externally. Capabilities, not addresses.

**Pepti Layer**: Sovereign CI builds → depot warehouse → gates deploy. No external package registries. Cross-arch from single CI trigger.

---

## Divergence Status

**ZERO.** All 13+ repos at GitHub↔Forgejo parity. Bidirectional relay on golgi catches any drift within 15 minutes.

Fixed this cascade:
- cellMembrane: cherry-picked `c93344c` (async freshness) onto Forgejo base
- sporePrint: pushed Forgejo state (3 commits) to GitHub

---

## Code Metrics

| Repo | Tests | Status |
|------|-------|--------|
| bearDog | 13,866+ | Gatehouse mode + drawbridge upstream shipped |
| songBird | 8,929+ | Drawbridge HTTP listener shipped |
| cellMembrane | 930 | Gateway refactor + relay + freshness |
| primalSpring | 1,081 | 117 scenarios (gatehouse/darkforest validated) |
| skunkBat | 541 | CapabilityClient + quarantine + metrics |
| sporePrint | 254 | Living topology + coverage sprint |
| petalTongue | 363+ | Deep debt zero |
| toadStool | 9,171+ | Stable |
| biomeOS | 8,351 | Stable |
| barraCuda | 4,619 | Stable |
| coralReef | 3,631 | Stable |
| sweetGrass | 1,658 | Stable |

---

## Critical Path

```
✅ All code shipped (including bearDog Android fix 6ef436864)
✅ All repos at parity
✅ Bidirectional relay live
✅ Pepti warehouse LIVE (membrane.primals.eco/depot/)
✅ Drawbridge LIVE (sporeGate :7780, golgi proxy updated)
✅ Caddy retired on sporeGate

NEXT (operational only):
1. sporeGate CI: rebuild bearDog 6ef436864 for Android  ← PEPTI COMPLETE
2. ironGate: start JupyterHub (docker :8000)            ← 502 → 200
3. ironGate + strandGate: mesh.init                     ← LAN MESH
4. flockGate: mesh.init via golgi                       ← WAN MESH
5. grapheneGate: pull bearDog from pepti + ADB deploy   ← MOBILE MESH

After step 4: LAN + WAN MESHED
After step 5: FULL MESH (all architectures)
```

---

*Wave 132g — Full mesh ready. bearDog Android unblocked. Deploy, peer, validate.*
