# ecoPrimals Ecosystem Blurb — Wave 132h

**Date**: Jul 6, 2026 09:07 EDT | **Wave**: 132h | **From**: eastGate overwatch
**Posture**: **LAN+WAN MESHED** — E2E live, all code shipped. Remaining: 1 CI build + gate deploys.

---

## Ecosystem State

```
LIVE:
  ✅ E2E HTTP: lab.primals.eco → 200 (JupyterHub 5.4.5)
  ✅ LAN mesh: sporeGate↔ironGate (FAMILY_ID trust)
  ✅ WAN mesh: flockGate via golgi relay (2 peers)
  ✅ Pepti warehouse: membrane.primals.eco/depot/ (x86_64 + aarch64)
  ✅ Relay: golgi bidirectional, 39/39 parity, 15min timer
  ✅ 13/13 primals STANDBY — zero P1 debt
  ✅ All repos at GitHub↔Forgejo parity

TOPOLOGY:
  sporeGate ←✅→ ironGate    (LAN direct, 10.13.37.x)
  sporeGate ←✅→ golgi       (WG relay)
  flockGate ←✅→ golgi       (WAN, 2 peers)
  strandGate: ALIVE .103     (SSH pending)
  grapheneGate: DEPLOY READY (binaries in pepti)
```

---

## FOR: Primal Teams (code → pepti → gates)

Primal code ships first. Gate teams deploy from pepti warehouse.
Push to BOTH remotes: `git push origin main && git push forgejo main`

---

### toadStool team

**One remaining debt item.**

| ID | What | Priority | Status |
|----|------|----------|--------|
| DH-1 | `/tmp` hardcoding — `temp_dir()` fallback still lands in `/tmp` when no env set | P2 | 4/5 primals resolved, toadStool remaining |

**What to fix**: When `BIOMEOS_SOCKET_DIR` and `XDG_RUNTIME_DIR` are both unset, the 3-tier resolution falls through to `std::env::temp_dir()` which returns `/tmp`. This breaks `ProtectSystem=strict` on systemd VPS units.

**Fix approach**: Add a 4th tier that uses a hardcoded `/run/membrane/` path when running as a systemd service (detect via `INVOCATION_ID` env), or require one of the env vars to be set (fail-closed).

**Impact**: Non-blocking for mobile (Android uses `/data/local/tmp` anyway). Blocks full systemd hardening on VPS (12 services still without `ProtectSystem=strict`).

---

### songBird team

**No active work required.** All shipped.

Current HEAD: `40699793` (drawbridge wired into orchestrator startup)

Recent deliverables absorbed by gates:
- Drawbridge HTTP listener (:7780) — Gatehouse→Darkforest crossing
- Mesh persistence (peers.toml, auto-reconnect)
- Federation port auto-promote to `0.0.0.0`
- FAMILY_ID auto-register (dark-forest disabled for LAN)

**Glacial** (no timeline pressure): `federation.enabled` config formalization.

---

### bearDog team

**No active work required.** All shipped.

Current HEAD: `6ef436864` (StrongBox HSM Android fix)

Recent deliverables absorbed by gates:
- Gatehouse mode (:443 TLS + :80 ACME/redirect)
- Gateway upstream → drawbridge :7780
- Android StrongBox HSM (10 compile errors resolved for aarch64)
- `BindMode::Auto` platform detection (ANDROID_ROOT env + cfg)
- `rustls_rustcrypto::provider().install_default()` in main()

---

### biomeOS team

**No active work required for current critical path.** Next evolution target (post-mesh):

| ID | What | Priority | Status |
|----|------|----------|--------|
| CROSS-GATE-EXEC-B | `graph.execute` honors `gate` hint — delegates to `try_relay_dispatch()` for remote gates | P3 | Spec done (Wave 60). Enables HPC fan-out across mesh. |

This is the next major capability evolution: cross-gate graph execution. The mesh transport is live — biomeOS needs to wire `graph.execute` to use it. See `specs/CROSS_GATE_GRAPH_EXECUTOR.md` in wateringHole.

---

### primalSpring team

**One CI/build task.**

| ID | What | Priority | Status |
|----|------|----------|--------|
| LAUNCHER-01 | `nucleus_launcher` cross-compile for aarch64-linux-android | P2 | `.cargo/config.toml` has `cargo cross-aarch64` alias ready. Need CI pipeline addition. |

**What's needed**: Add `nucleus_launcher` to the Sovereign CI aarch64 build targets (alongside songBird/bearDog). The cross-compile config already exists:

```toml
# .cargo/config.toml (already in repo)
[target.aarch64-unknown-linux-musl]
linker = "aarch64-linux-gnu-gcc"
rustflags = ["-C", "target-feature=+crt-static"]

[alias]
cross-aarch64 = "build --release --target aarch64-unknown-linux-musl --bin nucleus_launcher"
```

**Impact**: Unblocks full 14-primal orchestration on grapheneGate via single command.
**Workaround**: Gate teams can deploy songBird + bearDog individually (works today).

---

### All other primals (skunkBat, coralReef, nestGate, rhizoCrypt, loamSpine, sweetGrass, squirrel, barraCuda, petalTongue)

**STANDBY. No action required.**

All at zero debt. 13/13 passing primalSpring gate on all invariants:
- Edition 2024, `cargo deny check bans`, `forbid(unsafe_code)`
- MethodGate 13/13, BTSP Phase 3 13/13, plasmidBin musl-static 13/13
- `PRIMAL_BIND_MODE=tcp_only` adopted 13/13
- Health standard converged, stale socket cleanup absorbed

---

## FOR: Gate Teams (deploy from pepti)

Gate teams consume binaries from `membrane.primals.eco/depot/` and handle operational deployment. No code changes required.

---

### sporeGate team

**Context**: You own the gate, LAN topology, membrane layers, Sovereign CI, and pepti warehouse.

**Current state**: E2E LIVE. Mesh operational. strandGate found alive at .103 but SSH-inaccessible.

**Your items**:

1. **strandGate enrollment** (P1 — physical access required)
   - Alive at 192.168.4.103 (DHCP shifted from .100), 30ms latency (WiFi)
   - Deploy SSH key → push songBird + bearDog from pepti
   - Then: `mesh.init --bootstrap 10.13.37.2:7700`
   - After: re-enable dark-forest (all LAN peers will have bearDog)

2. **LAUNCHER-01 CI addition** (P2 — after primalSpring ships the alias)
   - Add `nucleus_launcher` aarch64 target to Sovereign CI pipeline
   - Publish to pepti: `/opt/ecoPrimals/depot/aarch64-linux-android/nucleus_launcher`

3. **bearDog gatehouse on golgi** (P3 — future)
   - Replace golgi Caddy with bearDog direct TLS termination
   - Not urgent — current proxy works

---

### flockGate team

**Context**: WAN validation deployment. Peering DONE.

**Current state**: PEERED. 2 reachable peers via golgi relay.

**Your items**:

1. **Validate cross-gate dispatch** (P1)
   ```json
   {"method":"capability.call","params":{"capability":"jupyter","method":"GET","path":"/hub/api"}}
   ```
   Expected: JupyterHub response routed through sporeGate→golgi→you

2. **Latency characterization** (P2)
   - `relay.parity` — confirm repo state matches golgi
   - Measure cross-gate `capability.call` RTT
   - Verify bidirectional relay pushes within 15min

---

### eastGate hardware team (grapheneGate)

**Context**: Pixel 8a mobile deployment. Binaries in pepti warehouse.

**Your items**:

1. **Pull + deploy** (P1)
   ```bash
   wget https://membrane.primals.eco/depot/aarch64-linux-android/songbird
   wget https://membrane.primals.eco/depot/aarch64-linux-android/beardog
   adb push songbird /data/local/tmp/ecoprimals/
   adb push beardog /data/local/tmp/ecoprimals/
   adb shell "chmod +x /data/local/tmp/ecoprimals/*"
   ```

2. **Start + peer** (P1)
   ```bash
   adb shell "cd /data/local/tmp/ecoprimals && \
     PRIMAL_BIND_MODE=tcp_only \
     SONGBIRD_PEERS=10.13.37.2:7700 \
     ./songbird server --bind 0.0.0.0 --port 7700 &"
   adb shell "cd /data/local/tmp/ecoprimals && \
     PRIMAL_BIND_MODE=tcp_only \
     ./beardog server --port 9500 &"
   # Mesh join:
   adb shell 'echo "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"mesh.init\",\"params\":{\"bootstrap_peers\":[\"10.13.37.2:7700\"]}}" | nc 127.0.0.1 7700'
   ```

3. **Validate** (P2)
   - `mesh.peers` → should show sporeGate (10.13.37.2)
   - StrongBox HSM initializes (hardware-backed crypto)
   - WiFi disconnect/reconnect → mesh auto-recovers

**After this**: FULL MESH (LAN + WAN + mobile)

---

## Repo Status

```
bearDog       6ef436864  gatehouse + Android fix
songBird      40699793   drawbridge wired into orchestrator
skunkBat      e7eaa5d    stable
primalSpring  66ebdb7    122 scenarios, 1095 tests, 0 debt
wateringHole  2cf8336    LAN+WAN MESHED posture
sporePrint    99bfc9e    living topology
cellMembrane  0704132    relay + freshness
petalTongue   0f8da6b    stable
```

All at GitHub↔Forgejo parity. Zero divergence.

---

## Critical Path

```
1. [PRIMAL] toadStool: DH-1 /tmp fix           → systemd hardening
2. [PRIMAL] primalSpring: LAUNCHER-01 aarch64   → pepti warehouse
3. [GATE]   sporeGate: strandGate SSH + deploy  → LAN complete
4. [GATE]   eastGate: grapheneGate ADB deploy   → FULL MESH
5. [GATE]   sporeGate: re-enable dark-forest    → security posture
6. [FUTURE] biomeOS: cross-gate graph executor  → HPC fan-out
```

---

*Wave 132h — Primal code complete. Gate deploys next. Zero P1 blockers.*
