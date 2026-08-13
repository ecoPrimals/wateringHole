# ecoPrimals Ecosystem Blurb — Wave 157k Interstadial (Post-Enmeshment)

**Date**: Aug 13, 2026 09:04 | **Wave**: 157k | **From**: sporeGate (foreman)
**Posture**: 11 gates ONLINE (biomeGate DOWN). **0/0/0.** Stadial item #1 CLOSED: blueGate + ironGate enmeshed into cascade via Tower Atomic TCP dispatch. **SSH deprecated for sub-builder dispatch (R-SUB in NanoWire checklist confirmed RETIRED).** CAS replication to ironGate 12TB WIRED. Gate hygiene composition-native. Build pipeline fully autonomous for musl + aarch64 targets. Windows target ready for first autonomous rebuild.

---

## What Changed (sporeGate ops — Aug 13 07:43–09:00)

### Sub-Builder Enmeshment (Stadial #1 CLOSED)

The foreman cascade can now auto-dispatch cross-architecture builds to ironGate and blueGate without SSH:

```
BEFORE:  sporeGate --SSH--> ironGate/blueGate "membrane plasmid.harvest ..."
NOW:     sporeGate --call_tcp(riboCipher)--> builder.serve :9800 → JSON-RPC plasmid.harvest
```

**Changes:**
- `SubBuilderEntry` gains `builder_host` / `builder_port` — direct TCP when mesh relay unavailable
- `resolve_builder_endpoint()` prefers TCP over MeshRelay (bridge until relay registration universal)
- `builder.serve` handles riboCipher `[0xEC, 0x01]` signal prefix (compatible with `call_tcp` framing)
- ironGate: `membrane-builder.service` (systemd, enabled, `:9800`, UFW opened for LAN)
- blueGate: rebuilt from `e8d4ffa`, WMI-detached process, scheduled task for reboot persistence
- Both verified end-to-end: `health` + `plasmid.staleness` via riboCipher-framed TCP from sporeGate

**Commits:**
- `e8d4ffa` cellMembrane — enmesh: TCP fallback + riboCipher signal handling
- `f8406bac6` wateringHole — manifest: builder_host/port for TCP dispatch

### SSH Deprecation Cross-Solve

This enmeshment **retires SSH for all sub-builder dispatch** (NanoWire checklist item R-SUB). The same TCP JSON-RPC pattern can now graduate the remaining SSH uses:

| SSH Use | Current | Tower Atomic Replacement | Status |
|---------|---------|--------------------------|--------|
| Sub-builder dispatch | `ssh gate "membrane plasmid.harvest"` | `call_tcp(builder_host:9800, plasmid.harvest)` | **RETIRED** |
| CAS archival | `ssh::scp_from(golgi, old_binary)` | `call_tcp` + binary relay RPC or HTTPS GET | Next |
| Depot push | `ssh::scp_to(golgi, new_binary)` | `call_tcp` + binary relay RPC or HTTPS PUT | Next |
| Gate pull/check | `ssh gate "membrane temporal.cascade"` | `cascade.notify` gossip (already live) | Parallel |
| Service ops | `ssh gate "systemctl ..."` | `service.*` capability RPC | Future |

The `builder.serve` pattern (TCP listener + riboCipher framing + JSON-RPC dispatch) is the template for all remaining SSH retirements. Each gate that runs `builder.serve` can be extended with additional capabilities (`depot.push`, `depot.pull`, `service.status`) on the same port.

---

## Remaining Stadial Work

| # | Item | Owner | Status |
|---|------|-------|--------|
| ~~1~~ | ~~Enmesh blueGate Windows builder into cascade~~ | ~~sporeGate~~ | **CLOSED.** TCP dispatch live, riboCipher compatible. |
| 2 | graftGate SSH key enrollment + builder.serve | physical | BLOCKED — M4 Mac Mini, physical access needed |
| 3 | southGate SSH key enrollment | overwatch | Port open, key not authorized |
| 4 | biomeGate SSH recovery | physical | GPU lab DOWN, eventual |
| 5 | westGate CAS enrollment | sporeGate | LAN IP not in topology — 50.7TB cold CAS target |
| 6 | **Graduate CAS archival from SSH to TCP relay** | sporeGate | NEW — use builder.serve pattern for `depot.cas_push` capability |
| 7 | **Graduate depot push from SSH to TCP relay** | sporeGate | NEW — use builder.serve pattern for `depot.receive` capability |

---

## Active Code Teams — ALL STADIAL TRACKS CLOSED

| Team | Track | Status |
|------|-------|--------|
| ~~**eastGate — biomeOS**~~ | ~~`deploy.result` gossip~~ | **DONE** (`f80e5f2a`). Dormant. |
| ~~**eastGate — primalSpring**~~ | ~~Wire `FleetDeployHealth`~~ | **DONE** (`d15ab028`, v0.9.50). Dormant. |
| ~~**sporeGate — cellMembrane**~~ | ~~`native_braid.py` → Rust~~ | **RETIRED** by westGate (`membrane content.braid`). |
| ~~**westGate — nestGate**~~ | ~~nestgate.io Phase 3~~ | **LIVE.** `/cas/{hash}` + provenance routes. |
| **strandGate — barraCuda** | Silicon saturation gaps (GPU-resident CG, async probe) | Science-track, not stadial. 6 gaps exposed. |

All primal code teams are **dormant**. Remaining work is infrastructure ops + science campaigns.

---

## Downstream Patterns (After Stadial Closes)

| Track | Description | Owner |
|-------|-------------|-------|
| **SSH → Tower Atomic graduation** | Extend `builder.serve` to handle `depot.*`, `service.*`, `gate.*` capabilities. Each graduated capability removes one SSH call site from the NanoWire checklist. | sporeGate |
| **nestgate.io Phase 3** | `/cas/{hash}` via `content.locate` mesh query. Data Braids card. | westGate + golgiBody |
| **arXiv submission** | Murillo/Chuna QCD preprint 41/42. Wire live site + reviewer send. | strandGate |
| **Science pipeline E2E (G71)** | GPU data → pseudoSpore → NFT → reviewer. | strandGate → ironGate → sporePrint |
| **tideGlass cell boot** | Cell 2026 GPS rebuild on westGate. CAS federation now live. | westGate |
| **sporePrint refresh (G14)** | pseudoSpore LIVE. QCD page + science artifacts. | ironGate |

---

## Depot Status

| Target | Status | Notes |
|--------|--------|-------|
| `x86_64-unknown-linux-musl` | **15/15 CURRENT** | Pushed to 5 gates |
| `aarch64-unknown-linux-musl` | **15/15 REBUILT** | ironGate sub-builder, CAS replicated |
| `aarch64-apple-darwin` | **5/15 refreshed** | graftGate, blocked on SSH for remaining 10 |
| `x86_64-pc-windows-gnu` | **STALE → READY** | blueGate builder enmeshed — first autonomous rebuild on next cascade |

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

> **Stadial #1 CLOSED.** Sub-builder dispatch is Tower Atomic TCP — SSH RETIRED for this path.
> The `builder.serve` pattern (TCP + riboCipher + JSON-RPC) is the template for graduating
> ALL remaining SSH uses. Each capability added to `builder.serve` removes one SSH call site.
> Overwatch: notify blueGate their builder is enmeshed and Windows depot will auto-rebuild
> on next cascade. graftGate needs SSH key enrollment for Darwin builder.serve deployment.

---

*Wave 157k interstadial CONFIRMED. 0/0/0. ALL stadial code tracks CLOSED. Enmeshment DONE. deploy.result Phases 1+2 DONE. nestgate.io Phase 3 LIVE. native_braid.py RETIRED. strandGate silicon saturation shipped. Remaining: physical access + SSH graduation. Downstream: arXiv, science E2E.*

---

## westGate — Wave 157k Solo Enabler Drop (Aug 13 2026)

**nestgate.io Phase 3 LIVE**: `/cas/{hash}` + `/cas/{hash}/provenance` routes on petalTongue peptidoglycan surface. Resolution order: local nestGate `content.exists` → `content.get`, then songBird `content.locate` mesh federation (scope: "all"), then 404 with federation status. Provenance routes query sweetGrass `braid.get` with riboCipher framing. Proper HTTP codes (200/404/502/504), Content-Type from CAS metadata, X-Content-Hash/X-Content-Source headers.

**sweetGrass announcement persistence FIXED**: `auto_announce_from_translations()` cross-references discovered primal sockets with TOML translation registry. Runs at startup (step 5a) and every background discovery sweep (30s). sweetGrass `braid.verify`, `braid.create` etc. are now routable immediately on biomeOS boot without manual `primal.announce`.

**native_braid.py RETIRED**: `membrane content.braid` is the Rust-native replacement. Routes through biomeOS Neural API (NeuralBridge) instead of direct primal sockets. Pipeline: `content.ingest → dag.session.create → dag.event.append_batch → dag.dehydration.trigger → spine.create → session.commit → crypto.sign → braid.create`. Supports `--only`/`--skip`/`--dry-run`/`--incremental`. Graph composition equivalent: `data_braid_ingress.toml` (invoke via `membrane deploy.graph`).

**0 active Python/Bash orchestration** in the westGate pipeline. All glue replaced.
