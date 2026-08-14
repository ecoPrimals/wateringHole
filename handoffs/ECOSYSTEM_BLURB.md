# ecoPrimals Ecosystem Blurb — Wave 157k Interstadial (Post-Stabilization)

**Date**: Aug 14, 2026 07:33 | **Wave**: 157k | **From**: sporeGate (foreman)
**Posture**: 11 gates ONLINE (biomeGate DOWN). **0/0/0.** Systemd registry convergence COMPLETE — cascade no longer spawns orphan processes. All 15 primal services stable under single-authority systemd management. Songbird consolidated to `songbird-gateway.service`. CAS replication to ironGate WIRED. Build pipeline fully autonomous.

---

## What Changed (sporeGate ops — Aug 14 07:14–07:33)

### Systemd Registry Convergence (STABILITY FIX)

Root cause of overnight process accumulation discovered and fixed:

```
BEFORE:  registry.rs mapped "beardog" → "beardog-membrane.service" (WRONG)
         nucleus_restart → systemctl restart beardog-membrane.service → FAIL
         → fallback: raw process spawn → ORPHAN ACCUMULATION

NOW:     registry.rs mapped "beardog" → "membrane-beardog.service" (CORRECT)
         nucleus_restart → systemctl restart membrane-beardog.service → OK
         → no orphans, clean convergence
```

All 13 primal entries corrected. songbird: `songbird-relay.service` → `songbird-gateway.service`. petaltongue: `petaltongue-membrane.service` → `membrane-petaltongue.service`.

### Songbird Service Consolidation

Two competing systemd units (`songbird-gateway.service` + `membrane-songbird.service`) resolved. `membrane-songbird` disabled. Gateway is authoritative (drawbridge, proxy, mesh-init, Restart=always). Drop-in added for FAMILY_ID/FAMILY_SEED/ECOPRIMALS_ROOT compatibility.

### CAS Replication Wiring

`replicate_to_cas_nodes()` added to `depot_sync.rs` — after local CAS archival, replicates to ironGate `/mnt/nestgate/cas`. Dedup-aware (checks remote before transfer).

### Process Cleanup

- Killed accumulated orphans from previous cascade cycles
- Restarted all 15 primal systemd services to clean state
- Removed stale sockets
- `pop-upgrade.service` remains masked

---

## Remaining Stadial Work

| # | Item | Owner | Status |
|---|------|-------|--------|
| ~~1~~ | ~~Enmesh blueGate Windows builder into cascade~~ | ~~sporeGate~~ | **CLOSED** |
| 2 | graftGate SSH key enrollment + builder.serve | physical | BLOCKED — M4 Mac Mini |
| 3 | southGate SSH key enrollment | overwatch | Port open, key not authorized |
| 4 | biomeGate SSH recovery | physical | GPU lab DOWN, eventual |
| 5 | westGate CAS enrollment | sporeGate | 50.7TB cold CAS target |
| 6 | Graduate CAS archival from SSH to TCP relay | sporeGate | Use builder.serve pattern |
| 7 | Graduate depot push from SSH to TCP relay | sporeGate | Use builder.serve pattern |

---

## Active Code Teams (4 tracks, rest dormant)

| Team | Track | Status |
|------|-------|--------|
| **eastGate — biomeOS** | `deploy.result` gossip via swarmVine | Last orchestration gap |
| **eastGate — primalSpring** | Wire `FleetDeployHealth` into `nucleus_launcher` CLI | Integration once biomeOS Phase 1 lands |
| **sporeGate — cellMembrane** | `native_braid.py` → Rust (1,259 LOC) | westGate/wateringHole scope |
| **westGate — nestGate** | nestgate.io Phase 3: `/cas/{hash}` via `content.locate` | Endpoint plumbing |

---

## Depot Status

| Target | Status | Notes |
|--------|--------|-------|
| `x86_64-unknown-linux-musl` | **15/15 CURRENT** | Pushed to 5 gates |
| `aarch64-unknown-linux-musl` | **15/15 REBUILT** | ironGate sub-builder, CAS replicated |
| `aarch64-apple-darwin` | **5/15 refreshed** | graftGate, blocked on SSH for remaining 10 |
| `x86_64-pc-windows-gnu` | **STALE** | blueGate builder RUNNING — needs cascade trigger |

---

## Code Team Ownership (Canonical)

| Gate | Code Teams | Role |
|------|-----------|------|
| eastGate | biomeOS, squirrel, projectNUCLEUS, primalSpring + overwatch | Orchestration + sovereignty |
| ironGate | bearDog, songBird, skunkBat, swarmVine, bingoCube, petalTongue, esotericWebb, footPrint, tideGlass + springs | Primal workhorse, 14TB NFT braid + CAS |
| strandGate | toadStool, barraCuda, coralReef, hotSpring, rustChip, helixVision, initioChem | Compute trio + batch HPC + science |
| westGate | rhizoCrypt, loamSpine, sweetGrass, nestGate, wetSpring, projectFOUNDATION | Provenance trio + data CAS (50.7TB) |
| sporeGate | cellMembrane, lithoSpore, plasmidBin ops | Topology + depot + cascade |
| graftGate | sourDough | Darwin builder (FULL NUCLEUS) |
| southGate | neuralSpring | Validation canary |
| blueGate | — | Windows builder (ENMESHED) |
| biomeGate | — | DOWN (GPU lab) |

---

## Architecture Reference

**NUCLEUS** = Tower + Nest + Node + biomeOS + petalTongue + squirrel + cellMembrane

| Atomic | Primals | Role |
|--------|---------|------|
| **Tower** | bearDog + songBird + skunkBat + swarmVine | Shared electron cloud: crypto, routing, defense, gossip |
| **Nest** | Tower + nestGate + rhizoCrypt + loamSpine + sweetGrass | Data identity: CAS + DAG + spine + braids |
| **Node** | Tower + toadStool + barraCuda + coralReef | Compute: dispatch + GPU + shaders |

---

## CONVERGENCE RULE

> **Systemd registry convergence COMPLETE.** Cascade no longer spawns orphan processes.
> All 13 primal systemd_unit entries match deployed unit names. songbird consolidated
> to `songbird-gateway.service` (single authority). Build pipeline stable and autonomous.
> Next: graduate CAS archival + depot push from SSH to TCP relay (builder.serve pattern).

---

*Wave 157k interstadial post-stabilization. 0/0/0. Systemd registry convergence DONE — cascade orphan leak FIXED. 15 primal services stable. songbird consolidated. CAS replication to ironGate wired. builder.serve template for SSH graduation. Next: CAS/depot TCP relay, deploy.result gossip, nestgate.io Phase 3.*
