# Wave 109 — guideStone Deployment Convergence

**Date**: 2026-06-11
**From**: eastGate overwatch
**FRAGO**: `impulses/active/2026-06-11T07-20_eastGate__wave109-guidestone-deployment-convergence.toml`

---

## Strategic Shift

Deployment works. Cross-topology validation is complete — LAN, WAN, ARM, VPS all proven. grapheneGate 13/13 alive. 5-gate ecosystem live. That was the first solution.

The goal is not deployment. The goal is every NUCLEUS deployment on every gate being **guideStone-grade and functionally identical** — true postPrimordial from VPS, no per-gate special knowledge, no operator memory.

Five guideStone properties applied to deployment:

| Property | Standard |
|----------|----------|
| **Deterministic** | Same depot + same gate profile = identical NUCLEUS state |
| **Reference-Traceable** | Every binary traces to provenance.toml (commit, rustc, timestamp, blake3) |
| **Self-Verifying** | BLAKE3 fail-closed; mismatch = abort |
| **Environment-Agnostic** | musl-static ecoBins, no runtime deps, no local builds |
| **Tolerance-Documented** | Named tolerances for staleness, handshake, convergence, startup |

---

## Five Work Streams

### Stream 1: Standard Primal Startup Contract `[6 primals]`

Every primal converges on: `$PRIMAL server --bind-mode $PRIMAL_BIND_MODE --port $PORT`

No per-primal case blocks in deploy scripts. `PlatformCapabilities::detect()` auto-senses transport (provided by primalSpring ipc crate — primalSpring is not a primal, it provides the infrastructure).

| Primal | Item |
|--------|------|
| bearDog | auto-detect abstract socket from bind mode |
| nestGate | default HTTP in server mode |
| biomeOS | infer `--btsp-optional` from bind mode |
| coralReef | unify `--rpc-bind` with `--port --bind` |
| barraCuda | replace `--no-unix` with bind-mode reading |
| skunkBat | replace `--no-uds` with bind-mode reading |

**guideStone**: P1 (Deterministic), P4 (Environment-Agnostic)

### Stream 2: Build Pipeline + Gate Profiles `[cellMembrane]`

- `membrane plasmid.build` (Rust) replaces `build-primal.sh` — ephemeral staging, provenance, BLAKE3
- Immediate fixes: BUILD-CACHE-01, BUILD-ELF-01, HARVEST-NAME-01
- Gate profiles (GATE-PROFILE-01): topology-aware TOML per gate in `ecosystem_manifest.toml`
- `gate.bootstrap` reads profile; `deploy_pixel.sh` becomes one transport backend

**guideStone**: P1 (Deterministic), P2 (Reference-Traceable)

### Stream 3: Post-Deploy Validation + Orchestration `[3 primals + primalSpring infra]`

- HEALTH-01: standard `{"method":"health"}` → `{status, primal, version, uptime_s}` across all 13
- **rhizoCrypt**: needs JSON-RPC health convergence (currently different protocol)
- **petalTongue**: needs JSON-RPC health convergence (currently different protocol)
- **songBird**: needs standard health or `/health` endpoint (currently HTTP-only)
- 10/13 already respond to JSON-RPC health — formalize the response schema
- LAUNCHER-01 (primalSpring infra): `nucleus_launcher` cross-compiled for aarch64
- Named tolerances: `depot_freshness_max=24h`, `mesh_handshake_timeout=30s`, `health_convergence_window=60s`

**guideStone**: P3 (Self-Verifying), P5 (Tolerance-Documented)

### Stream 4: BTSP End-to-End `[primalSpring + sweetGrass + bearDog]`

- BTSP-E2E-01: validate full handshake (bearDog key → client → sweetGrass/petalTongue)
- Test on grapheneGate TCP-only transport

**guideStone**: P3 (Self-Verifying)

### Stream 5: cellMembrane Cascade + quorumSignal + rootPulse `[cellMembrane]`

Divergence hardening across the four layers (source, depot, binary, process):

| Item | Layer |
|------|-------|
| Dual checksum authority (git + VPS) | depot |
| Post-cascade selective NUCLEUS restart | process |
| Process version match (JSON-RPC, not pgrep) | process |
| deployment.toml emission from gate.bootstrap | binary |
| Agentic divergence resolution | source |
| quorumSignal: 15 atomic signal graphs (Phase 2) | source |
| rootPulse: impulse → full provenance trio | source |
| Freshness mesh: songbird mesh.publish HEADs | source |

**guideStone**: P2 (Reference-Traceable), P3 (Self-Verifying)

---

## Per-Level Guidance

### Primals — Stream 1, 3, 4 convergence

Each primal team: standardize your server startup to the envelope. Remove custom transport flags. Let `PRIMAL_BIND_MODE` and platform detection do the work. See FRAGO `[stream1.items]` for your specific item.

**Routing — which primals have work, which stand by:**

| Primal | Stream 1 (Startup) | Stream 3 (Health) | Stream 4 (BTSP) | Status |
|--------|--------------------|--------------------|------------------|--------|
| bearDog | STARTUP-BD-01 | — | BTSP-E2E-01 | **ACTIVE** |
| nestGate | STARTUP-NG-01 | — | — | **ACTIVE** |
| biomeOS | STARTUP-BM-01 | — | — | **ACTIVE** |
| coralReef | STARTUP-CR-01 | — | — | **ACTIVE** |
| barraCuda | STARTUP-BC-01 | — | — | **ACTIVE** |
| skunkBat | STARTUP-SB-01 | — | — | **ACTIVE** |
| rhizoCrypt | — | HEALTH-RC-01 | — | **ACTIVE** |
| petalTongue | — | HEALTH-PT-01 | — | **ACTIVE** |
| songBird | — | HEALTH-SB-01 | — | **ACTIVE** |
| sweetGrass | — | — | BTSP-E2E-01 | **ACTIVE** |
| toadStool | — | — | — | **STANDBY** |
| squirrel | — | — | — | **STANDBY** |
| loamSpine | — | — | — | **STANDBY** |

> 10 primals ACTIVE, 3 STANDBY. All 13 will eventually formalize HEALTH-01 response schema, but 10/13 already respond — the 3 health items above are convergence gaps.

### primalSpring — Infrastructure (not a primal)

primalSpring provides the evolution spring for primal interactions. It has no NUCLEUS binary — if it still has one, that's not postPrimordial.

- `PlatformCapabilities::detect()` in the ipc crate (consumed by primals)
- HEALTH-01 RFC for standard health endpoint schema
- `nucleus_launcher` cross-compile for aarch64 (LAUNCHER-01)
- BTSP-E2E-01 handshake validation scenario

### Springs — healthSpring independent

healthSpring signal dispatch (`GAP-47-SIGNAL-DISPATCH-LIVE`) remains independent. 15 upstream gaps in healthSpring FRAGO — stable workarounds.

### Gates — flockGate re-test pending

flockGate: VPS songbird restarted (Wave 108). Re-test WAN mesh. File impulse if still failing.

All other gates: operational. grapheneGate 13/13 alive.

### Gardens (cellMembrane) — Streams 2, 5

- `membrane plasmid.build` Rust port (replaces shell pipeline)
- Gate profile TOML in ecosystem_manifest
- Cascade → restart coupling
- deployment.toml emission
- quorumSignal / rootPulse / freshness mesh evolution

---

## Pending

| Item | Owner | Priority |
|------|-------|----------|
| flockGate WAN re-test | flockGate ops | P2 |
| SOURDOUGH-SEGFAULT | sourDough | LOW |
| healthSpring signal dispatch | healthSpring | LOW |
| healthSpring 15 upstream gaps | various | LOW |

---

## Active Documents

| Document | Purpose |
|----------|---------|
| This blurb | Wave 109 per-level guidance |
| `impulses/active/...wave109-guidestone-deployment-convergence.toml` | Main FRAGO — 5 streams |
| `impulses/active/...wave107-healthspring-upstream-gaps.toml` | healthSpring gaps |
| `cellMembrane/AAR_CELLMEMBRANE_WAVE106_DETERMINISTIC_DEPLOYMENT_JUN10_2026.md` | Living deployment standard |

Archived: `archive/wave108/` (grapheneGate AAR + Wave 108 blurb), `archive/wave109/` (wave106 cross-topology FRAGO).

---

**Deployment was the first solution. guideStone convergence is the work.**
