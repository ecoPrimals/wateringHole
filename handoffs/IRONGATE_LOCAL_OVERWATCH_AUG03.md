# ironGate Local Overwatch — Code Team Blurb

**Date**: 2026-08-04 14:34 EDT (Session 9 — Depot Sync Validated)
**Gate**: ironGate (10.13.37.7) — PRIMARY DOWNSTREAM HOST
**Wave**: 156d
**Audience**: esotericWebb code team + footPrint code team (parallel IDE sessions)
**From**: ironGate hardware team (local overwatch)

---

## SUBSTRATE STATE — What You're Building On

ironGate is running **full NUCLEUS v4.57+** with Neural API on `/run/user/1000/membrane/`.
All depot-synced binaries deployed (52 builds). RTX 5070 (12 GB VRAM, CUDA 12.8) stable.
**Both workloads are LIVE** — esotericWebb cell attached, footPrint server on :3002.

```
biomeOS:        v4.57.0 (nucleus attach SHIPPED)
CELL:           esotericwebb_cell ATTACHED (exp006: 19/22 PASS, 0 fail)
NUCLEUS:        v4.57 Neural API on /run/user/1000/membrane/
SOCKETS:        2 membrane + 27 legacy (migration in progress)
GRAPHS:         45 found in Graphs Directory
GPU:            RTX 5070 / 12 GB / CUDA 12.8 / 42°C
RAM:            94 GB DDR5
CPU:            i9-14900K (24c/32t)
Disk:           3.4 TB available of 3.6 TB NVMe
Rust:           1.96.0
Node.js:        22.23.2
```

### Blockers Cleared Since Session 8

- **SO_PEERCRED SHIPPED** (rhizoCrypt G63) — CAS local-trust is real
- **content.query SHIPPED** (nestGate) — query metadata from CAS
- **nestgate.io wired** — content backend operational, branded
- **K-derm 3/3** — dnsmasq deployed, all 11 gates resolving

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

- **Version**: V31b (V30d→V31b absorbed Aug 4)
- **HEAD**: `5902a6f` — capability parity + cell graph alignment for biomeOS v4.57
- **Tests**: 465 lib pass
- **Clippy**: clean
- **Live composition**: exp006 19/22 PASS, 0 fail, 3 skip (socket migration)
- **G19 MILESTONE**: petalTongue scene push FIRING on ironGate
- **V31b**: capability parity, cell graph alignment, AAR for first cell boot

### Your Priority

**Phase 1: CELL BOOT COMPLETE.** The cell is live. Explore:
1. squirrel G18 signal dispatch (real consumer wiring)
2. batch provenance (V30 feature) testing against CAS with SO_PEERCRED
3. content.query integration (now shipped in nestGate)
4. Game content iteration — run exp006 after changes to validate

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

- **Tests**: **708 PASS** (53 test files, vitest 4.1.10, 1.04s)
- **Server**: LIVE on :3002 (`status: ok, version: 2.0.0`)
- **HEAD**: `a498566` — manifest-driven sources, riboCipher UDS transport
- **Node.js**: v22.23.2
- **Deps**: 347 packages

### Dev Server

```bash
cd gardens/footPrint
PORT=3002 npm run dev
# Frontend: http://localhost:5173/footprint/
# API: http://localhost:3002
# WebSocket: ws://localhost:3002/ws/bridge
# Health: http://localhost:3002/api/health
```

### Phase 2 Deploy — DONE

| File | Purpose | Status |
|------|---------|--------|
| `deploy/footprint.service` | systemd unit (PORT=3002) | DEPLOYED |
| `deploy/caddy-footprint-api.snippet` | Caddy reverse proxy | READY (needs golgi Caddy update) |

### Your Priority

**Phase 2: DEPLOYED.** Server live, CAS E2E verified, agent bridge running.
Now available:
1. **SO_PEERCRED** is SHIPPED (rhizoCrypt G63) — wire authenticated CAS writes
2. **content.query** is SHIPPED (nestGate) — wire metadata search for GPS datasets
3. **GPS data** is CONVERTED (11 JSON, 103 MB on westGate) — ready for viz integration
4. Remaining: golgi Caddy routing for public HTTPS (`footprint.primals.eco`)

### Remaining Blockers

| Blocker | What | Owner | Status |
|---------|------|-------|--------|
| ~~BTSP local-trust~~ | ~~SO_PEERCRED for CAS write~~ | ~~bearDog/nestGate~~ | **CLEARED** (rhizoCrypt G63) |
| Caddy routing | DNS + reverse proxy for `footprint.primals.eco` | sporeGate | **PENDING** — only remaining P1 |

---

## KEY DATES

| When | What |
|------|------|
| Session 8 (today) | FIRST CELL BOOT — esotericWebb attached to NUCLEUS |
| Session 9 (now) | Depot sync validated, 6/8 blockers cleared |
| Next | squirrel G18 dispatch + golgi Caddy routing |
