# ironGate Local Overwatch — Code Team Blurb

**Date**: 2026-08-04 09:15 EDT
**Gate**: ironGate (10.13.37.7) — PRIMARY DOWNSTREAM HOST
**Wave**: 155v/156d
**Audience**: esotericWebb code team + footPrint code team (parallel IDE sessions)
**From**: ironGate hardware team (local overwatch)

---

## SUBSTRATE STATE — What You're Building On

ironGate is running **full NUCLEUS** with 26/27 IPC sockets healthy. All 13
primals are deployed and responding. The RTX 5070 (12 GB VRAM, CUDA 12.8) is
available for petalTongue rendering and toadStool/coralReef compute dispatch.

```
NUCLEUS HEALTH: 26/27 HEALTHY (1 missing: network.sock — non-blocking)
GRAPHS DIR:     READY (newly functional this wave)
GPU:            RTX 5070 / 12 GB / CUDA 12.8 / 60°C idle
RAM:            94 GB DDR5 (82 GB available)
CPU:            i9-14900K (24c/32t)
Disk:           3.4 TB available of 3.6 TB NVMe
Rust:           1.96.0
Node.js:        22.23.2
```

### Primal Sockets Available (for IPC)

All sockets in `/run/user/1000/biomeos/`:

| Domain | Socket | Status |
|--------|--------|--------|
| ai | `ai.sock` / `squirrel.sock` | HEALTHY |
| crypto | `beardog.sock` / `btsp.sock` / `crypto.sock` / `ed25519.sock` / `x25519.sock` | HEALTHY |
| dag | `dag.sock` / `rhizocrypt.sock` | HEALTHY |
| ledger | `ledger.sock` / `loamspine.sock` | HEALTHY |
| math | `math.sock` / `barracuda.sock` | HEALTHY |
| permanence | `permanence.sock` / `neural-api-default.sock` | HEALTHY |
| provenance | `provenance.sock` / `sweetgrass.sock` | HEALTHY |
| security | `security.sock` / `skunkbat.sock` | HEALTHY |
| shader | `shader.sock` / `coralreef-core-default.sock` | HEALTHY |

### Neural API Routing

biomeOS Neural API is live on `neural-api-default.sock`. Your code should use
`capability.call` to route through biomeOS instead of connecting to individual
primal sockets. This follows the canonical pattern from the three-domain topology
spec: consumers talk to Neural API, not individual primals. Both esotericWebb's
`PrimalBridge::discover()` and footPrint's riboCipher transport do this automatically.

---

## esotericWebb CODE TEAM

### Your Working Directory

```
gardens/esotericWebb/
├── webb/src/         # Core library: IPC bridge, session, narrative, content, state
├── experiments/      # 6 experiments (exp001-exp006)
├── content/          # Game content YAML (worlds, NPCs, scenes)
├── graphs/           # Cell graphs (esotericwebb_cell.toml)
├── deploy/           # esotericwebb.toml + launch_interactive.sh
├── config/           # Runtime config
└── specs/            # Standards and gap tracking
```

### Current State

- **Version**: V30 (V26→V27→V28→V29→V30 absorbed Aug 4)
- **Tests**: 482 pass (463 lib + 18 integration + 1 doc)
- **Clippy**: 0 warnings (pedantic + nursery)
- **Live composition**: exp006 PROVEN — 22 pass, 0 fail, 0 skip
- **G19 MILESTONE**: petalTongue scene push FIRING on ironGate
- **HEAD**: `8d4181b` (V30)

### V30 Evolution

- **V27-V28**: petalTongue integration — live site, grammar, WebGL, animation
- **V29**: deep debt refactor + docs refresh
- **V30**: cell graph validation + batch provenance readiness
- **V30b**: typed LocationDef, canonical name constants, `#[allow]→#[expect]`

### What exp006 Shows (V30)

```
Discovery: 8/9 primals direct + all 9 via Neural API
Session:   "The Weaver's Parlor" loaded, 12 actions available
Actions:   examine + navigate work, state advances, knowledge tracked
Enrichment: FIRING — scene pushed to petalTongue on both examine and navigate
```

### Open Gaps

| Gap | What | Priority |
|-----|------|----------|
| **GAP-002** | petalTongue CRPG scene type — resolved on Webb side, awaiting petalTongue v1.7+ | Low |
| **GAP-003** | squirrel NPC dialogue constraint enforcement | Medium |
| **Cell attach** | `biomeos deploy --mode attach` for formal cell boot (executor→cell schema) | P1 upstream |

### Deploy Infrastructure

- `graphs/esotericwebb_cell.toml` — cell composition graph (13 capabilities, 3 liveness gates)
- `deploy/esotericwebb.toml` — composition fragment
- `deploy/launch_interactive.sh` — NUCLEUS + petalTongue live mode
- biomeOS Graphs Directory: **READY** (newly functional)

### Your Priority

**Phase 1: First live cell boot.** Cell graph is structurally validated. All primal
sockets are live. esotericwebb.sock is healthy. The gap is `biomeos deploy --mode attach`
cell-schema parsing (upstream biomeOS team). Run `exp006` to validate your changes
against the live NUCLEUS.

---

## footPrint CODE TEAM

### Your Working Directory

```
gardens/footPrint/
├── src/             # TypeScript source (Vite frontend + Express server)
│   ├── rustscript/  # Rust safety primitives (Option, Result, Vec, Cow, RefCell, Channel)
│   ├── core/        # Store, renderer, solver, constraints
│   ├── types/       # Shape, source, snap types
│   └── server.ts    # Express server + WebSocket bridge + agent API
├── projects/        # GeoJSON project data (Lansing Scuffle, etc.)
├── deploy/          # systemd unit + Caddy snippet + README
├── specs/           # Specifications
└── vitest.config.ts # Test config
```

### Current State

- **Tests**: **628 PASS** (43 test files, vitest 4.1.10, 1.17s)
- **Stack**: TypeScript / Vite / Leaflet (frontend) + Express/tsx (server)
- **HEAD**: `badea22` — manifest-driven sources, riboCipher UDS transport
- **Node.js**: v22.23.2
- **Deps**: 347 packages

### Recent Evolution (3 commits absorbed)

- `5bec3e5`: riboCipher UDS transport + ironGate Phase 2 deploy config (port 3002)
- `01e1adc`: manifest-driven source registration, coverage, centralization
- `badea22`: root docs + specs updated to manifest-driven state

### Dev Server

```bash
cd gardens/footPrint
PORT=3002 npm run dev
# Frontend: http://localhost:5173/footprint/
# API: http://localhost:3002
# WebSocket: ws://localhost:3002/ws/bridge
# Health: http://localhost:3002/api/health
```

### Phase 2 Deploy Infrastructure (READY)

| File | Purpose |
|------|---------|
| `deploy/footprint.service` | systemd unit (PORT=3002) |
| `deploy/caddy-footprint-api.snippet` | Caddy reverse proxy for TLS termination |
| `deploy/README.md` | Deploy instructions + port allocation |

### Phase 2 Deploy Plan

1. Wire nestGate CAS for project persistence (replacing Express CRUD)
2. Wire songBird drawbridge for external GIS sources (USGS, FEMA, OSM, Esri)
3. Configure Caddy: `footprint.primals.eco` → `:5173` (frontend) + `:3002` (API)
4. BTSP local-trust (SO_PEERCRED) for authenticated CAS write

### Remaining Blockers

| Blocker | What | Owner |
|---------|------|-------|
| BTSP local-trust | SO_PEERCRED for CAS write authentication | bearDog / nestGate |
| Caddy routing | DNS + reverse proxy for `footprint.primals.eco` | sporeGate |

---

## CONVERGENCE RULE (applies to both teams)

> **eastGate owns the codebase.** Code teams on ironGate are consumers and validators.
>
> 1. **DO NOT** push code changes to Forgejo (except wateringHole handoffs)
> 2. **Minimal edits only**: config tweaks, environment-specific settings
> 3. **Report back**: File findings as handoffs in `infra/wateringHole/handoffs/`
> 4. **Pull from Forgejo regularly** to stay converged
> 5. **Bugs**: Document in handoff with file, line, proposed fix — eastGate ships it

### Push access

ironGate has Forgejo SSH push access for `ecoPrimals/wateringHole` only (handoffs).
For code changes, document in a handoff and eastGate will integrate.

---

## HARDWARE TEAM STATUS

- NUCLEUS: 26/27 HEALTHY, Graphs Directory newly READY
- GPU: RTX 5070, 60°C idle, 5% util, 524 MiB VRAM
- Network: WireGuard live (golgi 38ms, sporeGate 77ms, eastGate 78ms)
- Port allocation: 3000 reserved, 3001 petalTongue, 3002 footPrint
- All 13/13 primals GREEN (barraCuda was YELLOW, now GREEN)
- Three-domain topology spec absorbed (primals.eco / nestgate.io / primal.eco)

If you need a primal restarted, a socket investigated, or GPU access configured,
ping the hardware team (this IDE session or wateringHole handoff).

---

*ironGate local overwatch. Wave 155v/156d. NUCLEUS 26/27 HEALTHY. 13/13 GREEN. GPU ready.
esotericWebb V30: cell graph validation + batch prov, exp006 22/22 PASS.
footPrint: 628 tests, Phase 2 DEPLOY READY, port 3002 validated.*
