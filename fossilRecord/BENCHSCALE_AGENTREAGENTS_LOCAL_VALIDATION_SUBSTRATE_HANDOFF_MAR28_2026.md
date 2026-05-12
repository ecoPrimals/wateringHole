# benchScale + agentReagents — Local Validation Substrate Handoff

**Date**: March 28, 2026
**From**: primalSpring (local multi-node validation infrastructure)
**To**: All primal teams + infra maintainers
**Scope**: benchScale and agentReagents are now functional ecoPrimals validation tools. This documents what works, what each primal team needs to fix, and how the ecosystem deployment pipeline has evolved.

---

## Context

benchScale (pure Rust lab substrate) and agentReagents (infrastructure artifact supply chain) were originally built for a separate but related project under the syntheticChemistry org. They have been onboarded into `ecoPrimals/infra/` and wired into the primalSpring validation pipeline.

The goal: **every primal composition should be testable locally in Docker containers before deploying to real gates.** This round of integration produced the first working end-to-end pipeline and exposed concrete debt in every primal's deployment surface.

## What Now Works

### One-Command Local Validation

```bash
cd springs/primalSpring
scripts/validate_local_lab.sh
```

This creates a Docker lab, deploys all primal binaries from plasmidBin, starts them with correct per-binary CLI commands, waits for health, runs cross-gate experiments, reports results, and tears down. ~30 seconds wall time.

### Pre-Deploy Gate Validation

```bash
cd infra/plasmidBin
./deploy_gate.sh user@gate --local-validate --composition tower
```

Runs the benchScale pipeline before SSH-pushing to a real gate. Catches composition failures locally.

### Live Test Results (March 28, 2026)

| Primal | Node | Alive | TCP Health | Protocol |
|--------|------|-------|------------|----------|
| beardog | tower | Yes | LIVE | TCP JSON-RPC (9100) |
| songbird | tower | Yes | LIVE | HTTP /health (9200) |
| biomeos | tower | No | Zombie | `neural-api` needs graph init |
| groundspring | spring | Yes | UDS only | Unix socket |
| healthspring_primal | spring | Yes | UDS only | Unix socket |
| neuralspring | spring | Yes | UDS only | Unix socket |
| wetspring | spring | Yes | UDS only | Unix socket |
| ludospring | spring | Yes | UDS only | Unix socket |

**7 of 8 primals alive in Docker. 2 experiments pass (exp074 cross-gate health, exp073 LAN covalent mesh).**

---

## Exposed Primal Gaps — Action Items for Teams

### Every primal has a different CLI contract

This is the single biggest deployment friction. The deploy script had to special-case every binary:

| Binary | Subcommand | Listen flag | --family-id |
|--------|-----------|-------------|-------------|
| beardog | `server` | `--listen 0.0.0.0:PORT` | Yes |
| songbird | `server` | `--port PORT` | No (env only) |
| nestgate | `daemon` | N/A (UDS only) | No (env `NESTGATE_FAMILY_ID`) |
| toadstool | (none) | `--port PORT` | No (env `TOADSTOOL_FAMILY_ID`) |
| biomeos | `neural-api` | N/A | No (env `FAMILY_ID`) |
| neuralspring | `serve` | N/A (UDS) | No |
| healthspring_primal | `serve` | N/A (UDS) | No |
| groundspring | `server` | N/A (UDS) | No |
| wetspring | `server` | N/A (UDS) | No |
| ludospring | `server` | N/A (UDS) | No |

**Recommendation**: Align on a common convention. Either:
- All primals accept `server --listen ADDR --family-id ID` (UniBin standard), or
- All primals accept `LISTEN_ADDR` and `FAMILY_ID` as env vars consistently

### Songbird speaks HTTP, not TCP JSON-RPC

Songbird's `--port` binds an HTTP server (for discovery/federation), not a raw TCP JSON-RPC endpoint like BearDog. The experiment code had to add a dual-protocol health probe.

**Songbird team**: Consider adding a JSON-RPC endpoint alongside the HTTP server, or document that cross-gate JSON-RPC to Songbird must go through the Unix socket (which means it's local-only).

### biomeos crashes without a graph/biome.yaml

`biomeos neural-api` exits immediately if no biome.yaml or graphs are provided. In a Docker lab, the binary is deployed but has no orchestration context.

**biomeOS team**: Consider a `--standalone` or `--health-only` mode for validation scenarios where biomeos should start and respond to health probes without requiring a full graph.

### Spring primals are UDS-only

All spring primals (groundspring, healthspring_primal, neuralspring, wetspring, ludospring) listen exclusively on Unix domain sockets. They cannot be health-checked from outside their container over TCP.

**Spring teams**: Not necessarily a bug — springs are designed for local IPC. But for cross-node validation, either:
- Add optional `--listen ADDR` for TCP binding, or
- Accept that springs are validated by in-container probes only

### NestGate and ToadStool not in Tower topology

The tower-2node topology only deploys beardog + songbird + biomeos on the tower node. NestGate, ToadStool, and Squirrel require the nucleus-3node topology, which hasn't been live-tested yet.

### Cross-arch benchScale gap

`deploy-ecoprimals.sh` does not check `primals/aarch64/` paths. On an ARM host, binaries won't be found. `bootstrap_gate.sh` has a path mismatch where `fetch.sh` puts aarch64 binaries in `primals/aarch64/` but bootstrap looks for flat `primals/`.

---

## How benchScale Models Deployment Conditions

### 5 Network Presets (tc-based)

| Preset | Scenario | Latency | Loss | Bandwidth | Jitter |
|--------|----------|---------|------|-----------|--------|
| basement_lan | Same-rack HPC | 0.5ms | 0% | 10 Gbps | 0.1ms |
| home_lan | Home WiFi/ethernet | 2ms | 0.01% | 1 Gbps | 1ms |
| friend_wan | Cross-city friend gate | 50ms | 0.5% | 100 Mbps | 10ms |
| mobile_cell | Pixel on LTE/5G | 100ms | 2% | 10 Mbps | 30ms |
| satellite | Starlink/geo | 600ms | 5% | 5 Mbps | 50ms |

### 3 ecoPrimals Topologies

| Topology | Nodes | Composition | Presets Used |
|----------|-------|-------------|--------------|
| tower-2node | 2 | Tower + springs | home_lan |
| nucleus-3node | 3 | Full NUCLEUS + springs + mobile | basement, home, mobile |
| wan-federation | 3 | Same nodes, WAN stress | friend, mobile, satellite |

### Gap: tc rules not applied yet

Docker containers lack `iproute2`, so the network presets are defined and parsed but degradation isn't enforced. Fixable by using a custom Docker image or installing iproute2 at container creation.

---

## Bonding Model Coverage

| Bond Type | Deploy Graphs | Live Tested | Crypto Flow |
|-----------|---------------|-------------|-------------|
| **Covalent** | 5 multi-node graphs | Yes (beardog + songbird in Docker) | BearDog BTSP + shared family seed |
| **Ionic** | Mentioned in data_federation comments | No | Cross-family contract (specified, not implemented) |
| **Metallic** | Taxonomy only | No | Fleet-scale shared compute (roadmap) |
| **Weak** | Taxonomy only | No | Opportunistic peer (roadmap) |
| **OrganoMetalSalt** | Taxonomy only | No | Multi-modal (roadmap) |

Only covalent bonds are deployable. For ionic/metallic to work, we need:
1. Deploy graphs that set non-covalent bond types
2. Primals (especially Songbird + BearDog) that negotiate trust differently per bond type
3. Experiments that validate cross-family interactions

---

## What benchScale + agentReagents Contribute Going Forward

### benchScale (pure Rust + shell)
- Repeatable multi-node Docker/LXD/QEMU labs from YAML topologies
- Network condition simulation (tc-based, 5 presets)
- Binary deployment and health checking
- Wired into primalSpring `validate_local_lab.sh` and plasmidBin `deploy_gate.sh --local-validate`

### agentReagents (artifact supply chain)
- Cloud-init configs for VM provisioning (`ecoprimals-node.yaml`)
- Artifact storage for ISOs, base images, debs (git-tracked manifests, git-ignored binaries)
- VM-tier validation when Docker isn't sufficient (libvirt/QEMU path)

### What they don't do
- They don't implement crypto — that's BearDog
- They don't implement networking — that's Songbird
- They don't validate primal internals — they validate **compositions** and **deployment surfaces**
- They expose gaps; primal teams fix gaps

---

## Repository Locations

| Tool | Path | Org |
|------|------|-----|
| benchScale | `ecoPrimals/infra/benchScale` | syntheticChemistry (origin), ecoPrimals (integration) |
| agentReagents | `ecoPrimals/infra/agentReagents` | syntheticChemistry (origin), ecoPrimals (integration) |
| plasmidBin | `ecoPrimals/infra/plasmidBin` | ecoPrimals |
| primalSpring | `ecoPrimals/springs/primalSpring` | ecoPrimals |

---

## Next Evolution Cycles

1. **Live-test nucleus-3node topology** — NestGate + ToadStool + Squirrel in Docker
2. **Enforce tc network conditions** — custom Docker image with iproute2
3. **Cross-arch benchScale** — aarch64 binary resolution in deploy-ecoprimals.sh
4. **biomeos standalone mode** — health-only start without graph
5. **Ionic bond deploy graph** — first cross-family validation experiment
6. **Sprint primal CLI alignment** — common `server --listen --family-id` or env convention
