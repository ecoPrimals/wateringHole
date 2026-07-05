# ecoPrimals Ecosystem Blurb — Wave 132h

**Date**: Jul 5, 2026 13:23 EDT | **Wave**: 132h | **From**: eastGate overwatch
**Posture**: **E2E LIVE — MESH PEERING** — full HTTP path validated (`lab.primals.eco/hub/api → 200`). Pepti warehouse complete. Remaining: mesh trust + WAN/mobile peering.

---

## What's Done (Wave 132g achievements — fossilized)

```
✅ bearDog gatehouse mode (16430d90c) — :443 TLS + :80 ACME/redirect
✅ songBird drawbridge (40699793) — :7780 HTTP→capability routing, wired into startup
✅ bearDog upstream fix (2ac2bd389) — default → :7780 drawbridge
✅ bearDog Android fix (6ef436864) — StrongBox HSM compiles for aarch64
✅ Caddy retired on sporeGate (permanent)
✅ golgi Caddy proxy updated → sporeGate:7780
✅ ironGate JupyterHub 5.4.5 LIVE on :8000
✅ E2E validated: internet → golgi TLS → sporeGate drawbridge → ironGate JupyterHub → 200
✅ Pepti warehouse LIVE: membrane.primals.eco/depot/ (x86_64 + aarch64, songBird + bearDog)
✅ Bidirectional relay: golgi membrane, 39/39 parity, 15min cascade
✅ All repos at GitHub↔Forgejo parity (zero divergence)
✅ Gatehouse/Darkforest standard published
```

---

## Remaining Work

| # | Item | Gate/Team | Type |
|---|------|-----------|------|
| 1 | Mesh trust: dark-forest mutual auth or LAN trust exception | sporeGate | config |
| 2 | flockGate WAN peering: mesh.init via golgi relay | flockGate | operational |
| 3 | grapheneGate: pull pepti + ADB deploy + mesh.init | eastGate hardware | operational |
| 4 | strandGate: investigate offline (192.168.4.100 unreachable) | sporeGate | hardware/network |
| 5 | bearDog gatehouse on golgi (long-term sovereign TLS) | sporeGate | future |

---

## Per-Gate Dispatch

---

### FOR: sporeGate team

**Context**: You own the gate, LAN topology, membrane layers, Sovereign CI, and pepti warehouse.

**Current state**: E2E LIVE. songBird drawbridge on :7780, JupyterHub returning 200, golgi proxying correctly. Pepti warehouse fully populated.

**Your remaining items**:

1. **Mesh trust configuration** (P1)
   - songBird dark-forest mode requires trust exchange for full mesh registration
   - Options: mutual TLS between mesh peers, pre-shared keys, or LAN trust exception for 10.13.37.0/24
   - Goal: ironGate and strandGate can register capabilities and be discovered via `mesh.peers`

2. **strandGate offline** (P2)
   - 192.168.4.100 unreachable — network or hardware issue
   - Check: Omada switch port, WiFi bridge (if applicable), WireGuard interface
   - Once reachable: `mesh.init` with bootstrap `10.13.37.2:7700`

3. **bearDog gatehouse on golgi** (P3 — future/low priority)
   - DNS `lab.primals.eco` → 157.230.3.183 (golgi)
   - Long-term: move bearDog TLS termination to golgi (it owns the IP)
   - Current golgi Caddy proxy is working — not urgent

**No code work required. All items are operational/configuration.**

---

### FOR: flockGate team

**Context**: You are the WAN validation deployment for inner membrane behaviors. All code debt is resolved. Your gate validates relay, parity, and remote dispatch over WAN latency.

**Current state**: All bearDog/songBird/skunkBat evolution absorbed. No code blockers.

**Your remaining items**:

1. **WAN mesh peering** (P1)
   ```bash
   # Join the mesh via golgi relay:
   socat - UNIX-CONNECT:/run/songbird/songbird.sock <<'EOF'
   {"jsonrpc":"2.0","id":1,"method":"mesh.init","params":{"bootstrap_peers":["10.13.37.1:7700"]}}
   EOF
   ```
   - golgi (10.13.37.1) is the relay between your gate and the LAN mesh
   - After peering: `mesh.peers` should show sporeGate, ironGate, eastGate

2. **Validate WAN relay path** (P2 — after peering)
   - `capability.call` across the golgi relay roundtrip
   - Test: `{"method":"capability.call","params":{"capability":"jupyter","method":"GET","path":"/hub/api"}}`
   - Expected: JupyterHub response routed through relay

3. **Test membrane behaviors over WAN** (P3)
   - `relay.parity` — verify your view of repo states matches golgi's
   - Remote dispatch latency characterization
   - Verify: bidirectional relay still pushes your commits to Forgejo within 15min

**Push protocol reminder**: always push to BOTH remotes:
```bash
git push origin main && git push forgejo main
```

---

### FOR: eastGate hardware team (grapheneGate)

**Context**: You own the Pixel 8a hardware. Binaries come from pepti warehouse — no local cross-compilation needed. bearDog Android fix (6ef436864) has shipped and been built by Sovereign CI.

**Current state**: Pepti warehouse has `aarch64-linux-android` binaries for songBird (21MB) and bearDog ready.

**Your remaining items**:

1. **Pull from pepti warehouse**
   ```bash
   # Via HTTPS:
   wget https://membrane.primals.eco/depot/aarch64-linux-android/songbird
   wget https://membrane.primals.eco/depot/aarch64-linux-android/beardog
   
   # Or via WG overlay:
   scp golgi:/opt/ecoPrimals/depot/aarch64-linux-android/* ./depot/
   ```

2. **ADB deploy**
   ```bash
   adb push depot/songbird /data/local/tmp/songbird
   adb push depot/beardog /data/local/tmp/beardog
   chmod +x /data/local/tmp/songbird /data/local/tmp/beardog
   ```

3. **Start primal suite**
   ```bash
   # songBird first (mesh foundation):
   adb shell "SONGBIRD_PEERS=10.13.37.5:7700 /data/local/tmp/songbird serve &"
   
   # bearDog (IPC + security):
   adb shell "/data/local/tmp/beardog server &"
   ```

4. **Mesh peering**
   ```bash
   # Via USB tether or WiFi — eastGate as bootstrap:
   adb shell "echo '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"mesh.init\",\"params\":{\"bootstrap_peers\":[\"10.13.37.5:7700\"]}}' | socat - UNIX-CONNECT:/data/local/tmp/songbird.sock"
   ```

5. **Validate**
   - BindMode::Auto should detect Android and use abstract sockets
   - `mesh.peers` should show eastGate (and LAN mesh via relay)
   - Test cellular relay fallback if WiFi disconnected

---

## Architecture (Current — Working)

```
INTERNET → Cloudflare → golgi :443 (Caddy TLS)
    → WG 10.13.37.2:7780 → sporeGate songBird drawbridge
        → /hub/* → jupyter capability → ironGate :8000 (JupyterHub 5.4.5) ✅ 200

Build/Deploy:
Forgejo push → sporeGate Sovereign CI → pepti warehouse (golgi depot)
    → x86_64-musl: songbird (23MB), beardog (11MB)
    → aarch64-android: songbird (21MB), beardog (built)

Mesh (current):
    sporeGate ←→ ironGate (LAN, 192.168.4.x, trust pending)
    sporeGate ←→ golgi (WG relay, bidirectional)
    flockGate ←→ golgi (WAN, peering pending)
    grapheneGate ←→ eastGate (mobile, deploy pending)
    strandGate: OFFLINE (unreachable)
```

---

## Repo Status

```
✅ bearDog       6ef436864  (gatehouse + Android fix)
✅ songBird      40699793   (drawbridge wired into orchestrator)
✅ skunkBat      e7eaa5d    (stable)
✅ cellMembrane  c83bcbc    (relay + freshness)
✅ primalSpring  446cdad    (118 scenarios, mesh_convergence_ops)
✅ wateringHole  bceb7c1    (E2E LIVE status)
✅ sporePrint    99bfc9e    (living topology)
✅ petalTongue   0f8da6b    (stable)
```

All at GitHub↔Forgejo parity. Zero divergence.

---

## Critical Path

```
✅ E2E HTTP path LIVE (lab.primals.eco → 200)
✅ Pepti warehouse complete (all arches)
✅ All code shipped + compiled

NEXT:
1. sporeGate: mesh trust config                    ← UNLOCKS capability discovery
2. flockGate: mesh.init via golgi                  ← WAN MESH
3. eastGate: grapheneGate pepti deploy + mesh.init ← MOBILE MESH
4. sporeGate: strandGate offline investigation     ← HARDWARE

After 1+2: WAN mesh operational (capability.call across relay)
After 1+3: Mobile mesh operational (Android + abstract sockets)
```

---

*Wave 132h — E2E validated. Mesh peering phase. Trust, then peer, then full mesh.*
