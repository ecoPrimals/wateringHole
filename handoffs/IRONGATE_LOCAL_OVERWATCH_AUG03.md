# ironGate Local Overwatch — Code Team Blurb

**Date**: 2026-08-05 08:30 EDT (Session 12 — NUCLEUS Storage LIVE)
**Gate**: ironGate (10.13.37.7) — PRIMARY DOWNSTREAM HOST
**Wave**: 156d
**Audience**: esotericWebb code team + footPrint code team (parallel IDE sessions)
**From**: ironGate hardware team (local overwatch)

---

## SUBSTRATE STATE — What You're Building On

ironGate is running **full NUCLEUS v4.57+** with **live CAS on 12.7 TB ext4**.
nestGate v0.5.0 running with BLAKE3 content-addressed storage.
9 cross-primal providers registered. songBird federation to westGate configured.

```
biomeOS:        v4.57.0 (nucleus attach SHIPPED)
CELL:           esotericwebb_cell ATTACHED (exp006: 19/22 PASS, 0 fail)
SQUIRREL:       signal.dispatch + signal.plan LIVE
NESTGATE:       v0.5.0 — CAS on 12.7 TB ext4 (sdc1), family 9b32f3a8
PROVIDERS:      9 registered (rhizoCrypt, bearDog, nestGate, nestGate-tcp,
                petalTongue, sweetGrass, loamSpine, toadStool, songBird)
SONGBIRD:       v0.2.1 — federation ENABLED, 1 peer (westGate LAN)
NUCLEUS:        v4.57 Neural API on /run/user/1000/membrane/
SOCKETS:        4 membrane + 29 biomeos
GPU:            RTX 5070 / 12 GB / CUDA 12.8
RAM:            94 GB DDR5 (81 GB available)
CPU:            i9-14900K (24c/32t)
Disk (NVMe):    3.3 TB available of 3.6 TB
Disk (CAS):     12 TB available of 12.7 TB ext4 (/mnt/nestgate)
Rust:           1.96.0
Node.js:        22.23.2
```

### What Changed Since Session 10

- **12.7 TB CAS disk mounted** — `/dev/sdc1` at `/mnt/nestgate`, fstab persistent
- **nestGate v0.5.0 running** — UDS + TCP (SO_PEERCRED local-trust on port 8080)
- **CAS write/read roundtrip proven** — BLAKE3 content.put → content.get
- **footPrint CAS E2E validated** — `createNeuralApiClient()` → TCP:8080 → nestGate
- **esotericWebb nest.store decomposition validated** — content.put + dag.event.append
- **songBird federation configured** — westGate reachable on LAN, federation enabled
- **9 providers** — nestGate (UDS + TCP) and songBird added to squirrel
- **Cell graphs updated** — both include `verify_nestgate` preflight
- **biomeos doctor** — 4/4 healthy including nestGate

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
- **Live composition**: exp006 19/22 PASS, 0 fail, 3 skip (socket migration)
- **G19**: petalTongue scene push FIRING on ironGate

### NEW: G18 Signal Dispatch Is Available

Your `PrimalBridge` already has `signal_plan()` (line 196 in `domains.rs`). It
calls `signal.plan` on the squirrel socket. **This is now live on ironGate.**

**What you can do now:**

1. **Wire `signal_plan` into the enrichment pipeline** — have squirrel decompose
   player intent into atomic session actions:

   ```rust
   let tools = vec![
       ToolDef {
           name: "session.act".into(),
           description: "Perform a player action".into(),
           parameters: serde_json::json!({"type":"object","properties":{"kind":{"type":"string"},"id":{"type":"string"}}}),
       },
   ];
   let plan = bridge.signal_plan("Player wants to explore the forest", &tools)?;
   ```

2. **Use `signal.dispatch` for cross-primal orchestration** — dispatch to any
   registered provider through squirrel:
   - `dag.session.create` → rhizoCrypt (provenance)
   - `crypto.hash` → bearDog (content hashing)
   - `braid.create` → sweetGrass (attribution)
   - `cert.mint` → loamSpine (certificates)

3. **LLM provider needed for AI features** — `ai.query`, `ai.narrate`,
   `signal.plan` all need an `AI_PROVIDER_SOCKETS` config pointing to an LLM.
   Without one, these degrade gracefully. To activate:
   ```bash
   export AI_PROVIDER_SOCKETS="http://localhost:11434"  # e.g. Ollama
   ```

### NEW: Live CAS Is Available

nestGate is running with 12.7 TB backing. Your `nest_store` signal (line 652 in
`domains.rs`) now has a **real CAS** behind it. Session provenance gets real persistence.

**What's changed for you:**

1. **`nest_store` fires to live CAS** — content.put stores BLAKE3-addressed blobs
   on the 12.7 TB disk. No more in-memory only.
2. **DAG provenance tracks content hashes** — `dag.event.append` with `DataCreate`
   links to CAS hashes, creating a full provenance chain.
3. **TCP local-trust (port 8080)** bypasses BTSP — same-gate services don't need
   bearDog auth. UDS still requires BTSP for cross-gate calls.

### Your Priority

**Phase 1 DONE, G18 DONE, CAS LIVE.** Next steps:
1. Test `nest_store` with real session data (session provenance → CAS → DAG)
2. Wire `signal_plan` into enrichment pipeline
3. Explore LLM provider setup for live AI narration
4. Continue game content iteration

---

## footPrint CODE TEAM

### Your Working Directory

```
gardens/footPrint/
├── src/             # TypeScript source (Vite frontend + Express server)
│   ├── agent/       # Agent bridge (server-bridge.ts, protocol.ts)
│   ├── rustscript/  # Rust safety primitives
│   ├── core/        # Store, renderer, solver, constraints
│   └── server.ts    # Express server + WebSocket bridge + agent API
├── projects/        # GeoJSON project data
├── deploy/          # systemd unit + Caddy snippet + README
└── specs/           # Specifications
```

### Current State

- **Tests**: **708 PASS** (53 test files, vitest 4.1.10, 1.04s)
- **Server**: LIVE on :3002 (`status: ok, version: 2.0.0`, uptime: 2h+)
- **Agent bridge**: WebSocket at `/ws/bridge` — READY, `agentConnected: false`
- **HEAD**: `a498566`

### NEW: Squirrel Dispatch Infrastructure Is Ready

The squirrel G18 dispatch is live on ironGate. Your agent bridge protocol
(JSON-RPC 2.0 over WebSocket) is already defined in `src/agent/protocol.ts`.

**What you need to wire:**

1. **Connect squirrel to the agent bridge** — squirrel needs a WebSocket client
   that connects to `ws://localhost:3002/ws/bridge` and can issue `project.command`
   requests:

   ```typescript
   // From squirrel's perspective (or a footPrint agent adapter):
   const ws = new WebSocket('ws://localhost:3002/ws/bridge');
   ws.send(JSON.stringify({
     jsonrpc: '2.0',
     method: 'project.command',
     params: { payload: { action: 'add-entity', kind: 'point', ... } },
     id: 1,
   }));
   ```

2. **Signal dispatch path** — footPrint can use squirrel's `signal.dispatch`
   for cross-primal calls via UDS:

   ```bash
   echo '{"jsonrpc":"2.0","method":"signal.dispatch","params":{"signal":"content.query","params":{"query":"GPS NF1"}},"id":1}' | \
     socat - UNIX-CONNECT:/run/user/1000/biomeos/squirrel.sock
   ```

3. **Available providers via squirrel**:
   - `content.query` → nestGate (GPS metadata search)
   - `crypto.hash` → bearDog (BLAKE3 hashing)
   - `dag.event.append` → rhizoCrypt (provenance)
   - `compute.submit` → toadStool (GPU compute)

### NEW: Live CAS Is Available

nestGate is running on `TCP localhost:8080` with SO_PEERCRED local-trust. Your
`createNeuralApiClient()` defaults to this — **zero config, it just works.**

**Proven E2E**: `contentPut({family:'9b32f3a8', content_base64:...})` → stored → 
`contentGet({hash:..., family:'9b32f3a8'})` → retrieved. Data on 12.7 TB disk.

**westGate federation**: songBird configured, LAN reachable. When westGate
exposes its nestGate TCP, `content.replicate.pull` will pull GPS datasets.

### Your Priority

**Phase 2 DEPLOYED, CAS LIVE, federation CONFIGURED.** Next steps:
1. Wire CAS persistence into project save/load (content.put for GeoJSON)
2. Wire a squirrel → agent bridge connector (WebSocket client)
3. Test `content.query` dispatch for GPS dataset discovery from westGate
4. Remaining: golgi Caddy routing for public HTTPS (`footprint.primals.eco`)

### Remaining Blockers

| Blocker | What | Owner | Status |
|---------|------|-------|--------|
| ~~BTSP local-trust~~ | ~~SO_PEERCRED for CAS write~~ | — | **CLEARED** (rhizoCrypt G63) |
| ~~G18 dispatch~~ | ~~Signal dispatch infra~~ | — | **CLEARED** (Session 10) |
| ~~CAS not running~~ | ~~nestGate not started~~ | — | **CLEARED** (Session 12) |
| Caddy routing | DNS + reverse proxy for `footprint.primals.eco` | sporeGate | **PENDING** |
| westGate federation | nestGate TCP + content capability | westGate hw | **BLOCKED** |
| Squirrel→bridge connector | WebSocket client from squirrel to footPrint | footPrint team | Next code task |

---

## KEY DATES

| When | What |
|------|------|
| Session 8 | FIRST CELL BOOT — esotericWebb attached to NUCLEUS |
| Session 9 | Depot sync validated, 6/8 blockers cleared |
| Session 10 | G18 signal dispatch LIVE — 7 providers, cross-primal dispatch |
| Session 12 (now) | **NUCLEUS STORAGE LIVE** — 12.7 TB CAS, federation configured |
| Next | Code teams wire CAS persistence + signal.plan |
