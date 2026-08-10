# ironGate Wave 157g — Enmesh AAR

**Date**: 2026-08-10 15:42 EDT
**Gate**: ironGate (10.13.37.7)
**Wave**: 157g — ENMESH
**From**: ironGate hardware team
**To**: overwatch (gate-agnostic)

---

## Summary

ironGate absorbed Wave 157g cascade (21 repos, gossip injection code landed across 6 primals). Fixed swarmVine socket discovery on ironGate (capability.call → gossip.status now routes correctly). Cross-gate TCP 7800 verified reachable to westGate + eastGate. songbird-register.sh expanded to cover all 11 active primals. 13/13 alive, 170 caps, 9 registered services.

---

## Execution

### 1. Cascade — 21 repos pulled (Wave 157g)
Major code evolution absorbed:
- **rhizoCrypt**: gossip injection (3 DAG lifecycle events) — `emitter.rs`, `types.rs`, 10 source files
- **loamSpine**: gossip injection (4 spine events: `cas.have`, `braid.head`, `spine.sealed`, `anchor.published`) — `gossip.rs`
- **sweetGrass**: `braid.verify` shipped (method #48, `6357f0f`) — P1 RESOLVED
- **songBird**: `gossip_relay.rs` — MeshRelay scaffolding
- **swarmVine**: 10 files (+227 LOC) — ribocipher, peer discovery evolution
- **skunkBat**: 16 files (+194/-345) — cleanup + hardening
- **cellMembrane**: 14 files — dispatch builder, continued evolution
- **petalTongue**: `gossip_injection.rs` — gossip scaffolding
- **biomeOS**: 20 files (+281/-112) — routing, socket discovery

### 2. swarmVine Socket Discovery Fix (ironGate gate-ops)
**Problem**: swarmVine registered with songBird on startup with 0 capabilities. songBird's first-registration-wins model prevented later capability additions. `capability.call(gossip.status)` failed with "No provider found."

**Fix**: 
1. Expanded `songbird-register.sh` to cover 11 primals (added swarmVine, skunkBat, squirrel, coralReef, barraCuda)
2. Restart sequence: stop swarmVine → restart songBird (clears registry) → run register script (wins with caps) → start swarmVine
3. Result: `capability.call(gossip.status)` → routes to swarmVine → response in <16ms

**Upstream note**: This is a gate-ops workaround. The blurb correctly identifies this as "biomeOS connects wrong socket — config issue." The real fix is for primals to self-register with their capabilities on startup (upstream item for all primals).

### 3. Cross-Gate TCP 7800 Reachability — VERIFIED

| Peer | TCP 7800 | gossip.status | peer_count |
|------|----------|---------------|------------|
| westGate (192.168.4.149) | **REACHABLE** | 5 ingested, 1 peer | Active |
| eastGate (10.13.37.5) | **REACHABLE** | 0 ingested, 0 peers | Fresh |
| sporeGate (10.13.37.1) | **REFUSED** | N/A | swarmVine may not be running |
| ironGate (127.0.0.1) | **LISTENING** | 0 ingested, 0 peers | Healthy |

swarmVine `SWARMVINE_PEERS` updated: `192.168.4.149:7800,10.13.37.5:7800`.

### 4. Gossip Injection Status on ironGate
- **Code landed**: rhizoCrypt (10 files), loamSpine (6 files), petalTongue (1 file)
- **Binaries**: Still depot Wave 157e — gossip injection features NOT in running binaries
- **Action needed**: Next depot rebuild will include gossip injection. Or build from source.

---

## Final State

```
Wave:          157g
Services:      13/13 active
Capabilities:  170 across 9 services
Dispatch:      16ms (capability.call → health.liveness)
TCP 7800:      LISTENING (swarmVine cross-gate gossip)
Mesh peers:    westGate (direct LAN), eastGate (WG) reachable
Gossip peers:  0 (peer discovery cycle pending)
Vine-bat:      OPERATIONAL
```

---

## Open Items (ironGate scope)

1. **Gossip injection binaries**: rhizoCrypt/loamSpine/petalTongue gossip code in source but not in depot binaries. Awaiting next depot rebuild.
2. **swarmVine peer discovery**: TCP 7800 reachable to 2 gates but gossip peers haven't connected yet. Automatic discovery cycles should converge.
3. **songBird registration ordering**: Gate-ops workaround (restart + register script). Upstream fix: primals self-register capabilities on startup.
4. **toadStool**: Still disabled (CLI requires `biome.yaml` manifest). toadStool S375 manifest schema shipped but execution stubbed.
5. **sourDough**: No systemd service template.

---

## ironGate Wave 157g: ENMESHED
