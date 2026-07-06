# ecoPrimals Ecosystem Blurb — Wave 132h

**Date**: Jul 6, 2026 09:49 EDT | **Wave**: 132h | **From**: eastGate overwatch
**Posture**: **FULL MESH CONVERGENCE** — grapheneGate Tower LIVE. LAUNCHER-01 complete. DH-1 resolved. All primal code shipped.

---

## Ecosystem State

```
LIVE:
  ✅ E2E HTTP: lab.primals.eco → 200 (JupyterHub 5.4.5)
  ✅ LAN mesh: sporeGate↔ironGate (FAMILY_ID trust)
  ✅ WAN mesh: flockGate via golgi relay (2 peers)
  ✅ Mobile: grapheneGate Tower LIVE (bearDog+songBird+skunkBat via ADB)
  ✅ Pepti warehouse: 15/15 binaries per arch (14 primals + nucleus_launcher)
  ✅ Relay: golgi bidirectional, 39/39 parity, 15min timer
  ✅ 13/13 primals STANDBY — zero debt (DH-1 resolved)
  ✅ All repos at GitHub↔Forgejo parity
  ✅ LAUNCHER-01 complete — nucleus_launcher in pepti for aarch64

TOPOLOGY:
  sporeGate ←✅→ ironGate    (LAN direct, 10.13.37.x)
  sporeGate ←✅→ golgi       (WG relay)
  flockGate ←✅→ golgi       (WAN, 2 peers)
  grapheneGate ←✅→ eastGate  (ADB, Tower running)
  strandGate: ALIVE .103     (SSH pending)
```

---

## FOR: Primal Teams (code → pepti → gates)

Push to BOTH remotes: `git push origin main && git push forgejo main`

---

### ALL PRIMALS — STANDBY

**Zero active code work.** All 13 primals at zero debt:

| Invariant | Status |
|-----------|--------|
| Edition 2024 | 13/13 |
| `cargo deny check bans` | 13/13 |
| MethodGate pre-dispatch | 13/13 |
| BTSP Phase 3 | 13/13 |
| `PRIMAL_BIND_MODE=tcp_only` | 13/13 |
| Health standard | 13/13 |
| Stale socket cleanup | 13/13 |
| DH-1 `/tmp` hardcoding | **RESOLVED** (toadStool S328) |
| LAUNCHER-01 aarch64 | **COMPLETE** (3.4MB, in pepti) |

**Recent deliverables (fossilized)**:
- bearDog: gatehouse mode, Android StrongBox HSM fix
- songBird: drawbridge HTTP listener, mesh persistence
- toadStool: DH-1 4th-tier socket resolution
- primalSpring: 123 scenarios, 1096 tests, environment-aware deployment validation

---

### biomeOS team — NEXT EVOLUTION TARGET

**Not blocking critical path.** Future work when mesh stabilizes:

| ID | What | Spec |
|----|------|------|
| CROSS-GATE-EXEC-B | `graph.execute` honors `gate` hint — routes to remote NUCLEUS via `try_relay_dispatch()` | `specs/CROSS_GATE_GRAPH_EXECUTOR.md` |
| CROSS-GATE-EXEC-C | `gate = "any"` — RoutingWeightTable selects optimal gate | Same spec |
| CROSS-GATE-EXEC-D | Fan-out — dispatch same graph to N gates in parallel | Same spec |

This enables HPC mesh workloads (e.g., Tenaillon 2016: 264 genomes across all gates).
The mesh transport is live — biomeOS wires the graph executor to use it.

---

## FOR: Gate Teams (deploy from pepti)

Gate teams consume from `membrane.primals.eco/depot/`. No code changes required.

---

### sporeGate team

**Context**: You own the gate, LAN topology, Sovereign CI, pepti warehouse.

**Current state**: E2E LIVE. grapheneGate Tower deployed. strandGate alive but SSH-inaccessible.

**Your items**:

1. **strandGate enrollment** (P1 — physical access required)
   - Alive at 192.168.4.103 (DHCP shifted from .100)
   - Deploy SSH key → push songBird + bearDog from pepti
   - `mesh.init --bootstrap 10.13.37.2:7700`
   - After: re-enable dark-forest (all LAN peers will have bearDog)

2. **bearDog gatehouse on golgi** (P2 — future)
   - Replace golgi Caddy with bearDog TLS termination
   - Not urgent — current proxy works fine

---

### flockGate team

**Context**: WAN validation. Peering DONE.

**Your items**:

1. **Validate cross-gate dispatch** (P1)
   ```json
   {"method":"capability.call","params":{"capability":"jupyter","method":"GET","path":"/hub/api"}}
   ```
   Expected: JupyterHub response routed via mesh relay

2. **Latency characterization** (P2)
   - Measure cross-gate `capability.call` RTT
   - Verify relay pushes within 15min

---

### eastGate hardware team (grapheneGate)

**Context**: Pixel 8a. Tower composition RUNNING.

**Current state**: bearDog + songBird + skunkBat deployed via ADB. Port forwarding active (9100, 9200, 9140). USB tether provides internet to eastGate.

**Your items**:

1. **Full NUCLEUS deploy** (P1 — now possible with nucleus_launcher)
   ```bash
   wget https://membrane.primals.eco/depot/aarch64-linux-android/nucleus_launcher
   adb push nucleus_launcher /data/local/tmp/ecoprimals/
   adb shell "chmod +x /data/local/tmp/ecoprimals/nucleus_launcher"
   adb shell "/data/local/tmp/ecoprimals/nucleus_launcher start --composition full"
   ```

2. **Mesh validation** (P1)
   - Confirm `mesh.peers` shows sporeGate
   - Test WiFi disconnect → mesh auto-reconnect
   - Validate StrongBox HSM health

3. **Cross-deployment issue**: graphenegate-readiness scenario failures are
   environment-dependent (0 on gates with local depot, 14 on WAN gates without).
   Fixed in primalSpring — test now accepts both values.

---

## Repo Status

```
bearDog       6ef436864  gatehouse + Android fix
songBird      40699793   drawbridge wired into orchestrator
skunkBat      e7eaa5d    stable
toadStool     S328       DH-1 resolved
primalSpring  faaa2cd    123 scenarios, 1096 tests, 0 debt
wateringHole  b1f9bce    LAUNCHER-01 complete, grapheneGate Tower LIVE
sporePrint    99bfc9e    living topology
cellMembrane  0704132    relay + freshness
```

All at GitHub↔Forgejo parity. Zero divergence.

---

## Critical Path

```
✅ All primal code DONE (zero debt, zero P1)
✅ LAUNCHER-01 COMPLETE (nucleus_launcher in pepti)
✅ DH-1 RESOLVED (toadStool S328)
✅ grapheneGate Tower LIVE
✅ LAN + WAN + mobile mesh operational

REMAINING:
1. [GATE] sporeGate: strandGate SSH + deploy       → all LAN enrolled
2. [GATE] sporeGate: re-enable dark-forest          → security posture
3. [GATE] flockGate: validate cross-gate dispatch   → WAN mesh verified
4. [GATE] eastGate: full NUCLEUS via nucleus_launcher → mobile complete
5. [FUTURE] biomeOS: cross-gate graph executor      → HPC fan-out
6. [FUTURE] golgi: bearDog gatehouse                → sovereign TLS
```

---

*Wave 132h — All primal code complete. Gate deploys operational. Ecosystem converging.*
