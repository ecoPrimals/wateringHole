# ironGate Local Overwatch — Code Team Blurb

**Date**: 2026-08-04 15:45 EDT (Session 10 — G18 Dispatch LIVE)
**Gate**: ironGate (10.13.37.7) — PRIMARY DOWNSTREAM HOST
**Wave**: 156d
**Audience**: esotericWebb code team + footPrint code team (parallel IDE sessions)
**From**: ironGate hardware team (local overwatch)

---

## SUBSTRATE STATE — What You're Building On

ironGate is running **full NUCLEUS v4.57+** with G18 signal dispatch LIVE.
Squirrel rebuilt from source and redeployed with `signal.dispatch` + `signal.plan`.
7 cross-primal providers registered. RTX 5070 stable at 42°C.

```
biomeOS:        v4.57.0 (nucleus attach SHIPPED)
CELL:           esotericwebb_cell ATTACHED (exp006: 19/22 PASS, 0 fail)
SQUIRREL:       REBUILT — signal.dispatch + signal.plan LIVE
PROVIDERS:      7 registered (rhizoCrypt, bearDog, nestGate, petalTongue,
                sweetGrass, loamSpine, toadStool)
NUCLEUS:        v4.57 Neural API on /run/user/1000/membrane/
SOCKETS:        2 membrane + 27 legacy (migration in progress)
GPU:            RTX 5070 / 12 GB / CUDA 12.8 / 42°C
RAM:            94 GB DDR5 (81 GB available)
CPU:            i9-14900K (24c/32t)
Disk:           3.3 TB available of 3.6 TB NVMe
Rust:           1.96.0
Node.js:        22.23.2
```

### What Changed Since Session 9

- **Squirrel rebuilt from source** — `signal.dispatch` + `signal.plan` now operational
- **7 providers registered** — cross-primal dispatch validated
- **Cross-primal dispatch proven** — squirrel → rhizoCrypt (DAG), squirrel → bearDog (crypto)
- **SO_PEERCRED, content.query, K-derm** — all confirmed SHIPPED and operational

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

### Your Priority

**Phase 1 DONE, Phase 3 (G18) infrastructure DONE.** Next steps:
1. Test `signal_plan` integration in exp006 or a new experiment
2. Wire provenance (DAG) into session lifecycle via `signal.dispatch`
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

### Your Priority

**Phase 2 DEPLOYED, G18 infrastructure READY.** Next steps:
1. Wire a squirrel → agent bridge connector (WebSocket client in squirrel or adapter)
2. Test `content.query` dispatch for GPS dataset discovery
3. Wire SO_PEERCRED (now SHIPPED in rhizoCrypt G63) for authenticated CAS writes
4. Remaining: golgi Caddy routing for public HTTPS (`footprint.primals.eco`)

### Remaining Blockers

| Blocker | What | Owner | Status |
|---------|------|-------|--------|
| ~~BTSP local-trust~~ | ~~SO_PEERCRED for CAS write~~ | — | **CLEARED** (rhizoCrypt G63) |
| ~~G18 dispatch~~ | ~~Signal dispatch infra~~ | — | **CLEARED** (Session 10) |
| Caddy routing | DNS + reverse proxy for `footprint.primals.eco` | sporeGate | **PENDING** — only remaining P1 |
| Squirrel→bridge connector | WebSocket client from squirrel to footPrint | footPrint team | **NEW** — next code task |

---

## KEY DATES

| When | What |
|------|------|
| Session 8 (today) | FIRST CELL BOOT — esotericWebb attached to NUCLEUS |
| Session 9 (today) | Depot sync validated, 6/8 blockers cleared |
| Session 10 (now) | G18 signal dispatch LIVE — 7 providers, cross-primal dispatch |
| Next | Code teams wire signal.plan + agent bridge |
