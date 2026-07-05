# ecoPrimals Ecosystem Blurb — Wave 132g

**Date**: Jul 5, 2026 10:28 EDT | **Wave**: 132g | **From**: eastGate overwatch
**Posture**: **MESH CONVERGENCE** — all code shipped, all repos at parity, zero divergence. Remaining work is operational: deploy binaries, configure mesh peering, start services.

---

## Context (all gates)

You are an agent on a gate in the ecoPrimals ecosystem. The ecosystem is a **sovereign, self-hosted mesh of compute gates** running 13 Rust primals coordinated via WireGuard overlay + Forgejo.

**Goal**: Get all gates across LAN and WAN fully meshed — capable of routing any capability request to any gate without manual port configuration.

---

## Status: ALL REPOS AT PARITY

```
✅ bearDog       2ac2bd389  (gatehouse mode + drawbridge upstream)
✅ songBird      16435b36   (drawbridge HTTP listener :7780)
✅ skunkBat      e7eaa5d    (capabilityClient + quarantine)
✅ sweetGrass    bab4657    (stable)
✅ cellMembrane  c83bcbc    (relay + freshness + gateway refactor)
✅ wateringHole  e2e0523    (standards + FRAGOs + blurb)
✅ sporePrint    99bfc9e    (living topology + 254 tests)
✅ primalSpring  cac3eec    (117 scenarios, 1081 tests)
✅ petalTongue   0f8da6b    (deep debt zero)
✅ rhizoCrypt    ef85124    (stable)
✅ toadStool     1ec37498   (stable)
✅ barraCuda     b2618db0   (stable)
✅ coralReef     3078d0b    (stable)
```

Zero divergence. GitHub↔Forgejo bidirectional relay running (golgi membrane 0704132, 15min cascade timer).

---

## REMAINING: What Blocks Full Mesh

### P0: Deploy Drawbridge (sporeGate)

songBird 16435b36 has the drawbridge HTTP listener but it needs to be **deployed and started** on sporeGate.

```bash
# On sporeGate: rebuild songBird from Sovereign CI output
# Then start with drawbridge config:
SONGBIRD_DRAWBRIDGE_ADDR=127.0.0.1:7780 \
SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter \
SONGBIRD_PROXY_ROUTES=jupyter=http://192.168.4.237:8000 \
songbird serve
```

**Immediate unblock (no DNS change needed)**: Update golgi Caddy:
```
lab.primals.eco → reverse_proxy 10.13.37.2:7780
```
(was :7700, which is wrong — federation not HTTP)

### P1: ironGate JupyterHub

E2E backend. Without this, the drawbridge routes to nothing.

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

## By Gate — What Each Team Does Next

### sporeGate

1. **Deploy songBird 16435b36** → start drawbridge on :7780
2. **Deploy bearDog 2ac2bd389** → gatehouse ready (hold for DNS decision)
3. **Update golgi Caddy** → proxy target `10.13.37.2:7780`
4. **Validate**: `curl http://lab.primals.eco/hub/api` via golgi → drawbridge → ironGate

### ironGate

1. **Start JupyterHub** (docker, port 8000, localhost only)
2. **mesh.init** → join sporeGate mesh (bootstrap `10.13.37.2:7700`)
3. **Register jupyter capability** via IPC

### flockGate

1. **mesh.init** via golgi relay (`10.13.37.1:7700`)
2. No code work remaining — all debt resolved

### eastGate

1. Overwatch: cascade + verify mesh convergence
2. Stage pilot dataset to ironGate after JupyterHub lands
3. Continue primalSpring scenario evolution

### golgi

1. **Update Caddy**: `lab.primals.eco` proxy → `10.13.37.2:7780`
2. Relay continues (15min timer, 39/39 parity)
3. Future: bearDog gatehouse here (owns DNS IP)

### grapheneGate

1. Rebuild bearDog + songBird for `aarch64-linux-android`
2. Deploy via ADB
3. `mesh.init` with eastGate as bootstrap

---

## Architecture (Gatehouse/Darkforest)

```
INTERNET → Cloudflare → golgi :443 (Caddy TLS, temporary)
    → WG overlay → sporeGate :7780 (songBird drawbridge)
        → path routing → capability.call → mesh
            → ironGate :8000 (JupyterHub)
            → strandGate (compute)
            → flockGate via golgi relay

Future (once bearDog gatehouse on golgi):
INTERNET → golgi :443 (bearDog TLS) → :7780 (drawbridge) → mesh
```

**Darkforest**: all gates communicate via songBird mesh (UDS, abstract sockets, WG direct-connect). No ports exposed externally. Capabilities, not addresses.

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
✅ All code shipped
✅ All repos at parity
✅ Bidirectional relay live

NEXT (operational only):
1. sporeGate: deploy songBird drawbridge :7780     ← UNBLOCKS E2E
2. golgi: update Caddy proxy → 10.13.37.2:7780    ← UNBLOCKS HTTP
3. ironGate: start JupyterHub                      ← UNBLOCKS backend
4. ironGate + strandGate: mesh.init                ← LAN MESH
5. flockGate: mesh.init via golgi                  ← WAN MESH
6. grapheneGate: Android rebuild + mesh.init       ← MOBILE MESH

After step 5: ALL GATES MESHED (LAN + WAN)
After step 6: FULL MESH (including mobile)
```

---

*Wave 132g — Zero code blockers. Zero divergence. Deploy and mesh.*
