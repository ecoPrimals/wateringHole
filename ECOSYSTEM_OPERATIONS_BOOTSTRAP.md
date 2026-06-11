<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Ecosystem Operations Bootstrap

**Purpose**: Durable operational context for any fresh instance (AI or human) working on any part of the ecoPrimals project. This document is state-safe — if all conversation memory is lost, this plus the repo's own docs gets you operational.

**Last Updated**: 2026-06-11 (Wave 109)

---

## 1. Infrastructure Topology

### The K-Derm Diderm Model

The ecosystem is physically deployed across a three-node VPS envelope (DigitalOcean NYC1) plus local development gates:

```
┌─────────────────────────────────────────────────────────────────────┐
│  INNER MEMBRANE (golgiBody)         157.230.3.183                   │
│  SSH alias: golgi                                                    │
│  Role: Sovereign periplasm — Forgejo, NUCLEUS primals, Knot DNS     │
│  Services: forgejo, 13x nucleus-primals, knot-dns, caddy, songbird  │
│  Binary depot: /opt/ecoPrimals/infra/plasmidBin/                    │
├─────────────────────────────────────────────────────────────────────┤
│  PEPTIDOGLYCAN (peptidoglycan)      157.230.209.218                 │
│  SSH alias: pepti (ProxyJump via golgi)                             │
│  Role: Structural layer — build hub, workspace, temporal sync       │
│  Services: workspace, builds, temporal-sync                          │
├─────────────────────────────────────────────────────────────────────┤
│  OUTER MEMBRANE (golgiBody-ext)     137.184.197.151                 │
│  SSH alias: golgi-ext (ProxyJump via golgi)                         │
│  Role: Public-facing — Caddy TLS, sporePrint, WAN depot, TURN      │
│  Serves: membrane.primals.eco, lab.primals.eco, git.primals.eco     │
│  WAN depot: https://membrane.primals.eco/depot/                     │
└─────────────────────────────────────────────────────────────────────┘
```

### SSH Configuration

All SSH access is via `~/.ssh/config` host aliases:

```
Host golgi         → 157.230.3.183 (root, direct)
Host golgi-ext     → 137.184.197.151 (root, ProxyCommand via golgi)
Host pepti         → 157.230.209.218 (root, ProxyCommand via golgi)
```

**To connect**: `ssh golgi`, `ssh pepti`, `ssh golgi-ext`

### Forgejo (Sovereign Git)

- **URL**: `https://git.primals.eco` (web) / `ssh://git@git.primals.eco:2222/` (SSH clone)
- **Host**: runs on golgiBody (inner membrane)
- **API**: `https://git.primals.eco/api/v1/` (token from `~/.config/forgejo/token`)
- **Orgs**: `ecoPrimals` (shared infra), `sporeGarden` (private repos)

### Songbird Mesh

- **Federation port**: 7700 (golgiBody)
- **Mesh peer address**: `157.230.3.183:7700`
- **Local gates** federate to VPS mesh peer for WAN connectivity
- **Env override**: `MEMBRANE_VPS_PEER`

---

## 2. Local Workspace Layout

Every gate (development machine) has the same workspace structure:

```
~/Development/ecoPrimals/
├── primals/          # 15 primal repos (bearDog, songBird, biomeOS, etc.)
├── springs/          # 8 spring repos (hotSpring, neuralSpring, etc.)
│   └── primalSpring/ # Infrastructure spring (not a primal)
├── gardens/          # 5 garden repos (cellMembrane, lithoSpore, etc.)
├── infra/            # Shared infrastructure
│   ├── wateringHole/ # Ecosystem guidance, handoffs, impulses, standards
│   ├── plasmidBin/   # Binary depot (checksums.toml, provenance.toml, primals/)
│   ├── sporePrint/   # Public-facing project (website, docs)
│   ├── whitePaper/   # Scientific whitepaper
│   ├── benchScale/   # Benchmarking tools
│   └── agentReagents/ # AI agent tools
├── fossilRecord/     # Archived history
└── sort-after/       # Unsorted staging
```

### Key Files

| File | Purpose |
|------|---------|
| `infra/wateringHole/ecosystem_manifest.toml` | Source of truth: repos, gates, topology, sync config |
| `infra/wateringHole/freshness.toml` | Live HEAD commits for all repos (published by cascade) |
| `infra/plasmidBin/checksums.toml` | BLAKE3 hashes for all deployed binaries |
| `infra/plasmidBin/provenance.toml` | Build traceability (commit, rustc, timestamp) |
| `infra/plasmidBin/sources.toml` | Source registry for all primal repos |
| `gardens/cellMembrane/membrane.toml` | K-Derm layer config, SSH aliases, channels |

---

## 3. The Cascade System

### What It Does

The cascade is how code flows from development to production. It's a manifest-driven parallel sync system that keeps all repos coherent across git remotes and gates.

### How to Run It

```bash
# From any gate — pull all repos from VPS (Forgejo is authority):
membrane temporal.cascade

# Quick cascade with options:
membrane temporal.cascade --check          # dry-run: show what's stale
membrane temporal.cascade --with-harvest   # sync + rebuild drifted primals
membrane temporal.cascade --clone-missing  # clone repos not yet on this gate

# Single-repo sync:
membrane temporal.sync path/to/repo

# Push freshness state after sync:
# (cascade does this automatically)
```

### Flow

```
Forgejo (golgi:2222)  ←→  Local Gate  →  GitHub (origin)
         ↕                                      ↕
    VPS workspace                         Public mirror
    (depot authority)                    (outer membrane)
```

The cascade:
1. Reads `ecosystem_manifest.toml` to discover all repos for this gate
2. Pulls from Forgejo (SSH, port 2222) — the sovereign authority
3. Pushes to GitHub (origin) — the outer membrane mirror
4. Publishes `freshness.toml` with HEAD commits
5. Optionally harvests (builds) primals with upstream changes

### Remote Naming Convention

Every repo has two remotes:
- `forgejo` → `ssh://git@git.primals.eco:2222/{org}/{repo}.git`
- `origin` → `https://github.com/{org}/{repo}.git`

### Resolving Conflicts

```bash
# If ff-only fails on wateringHole (common — multiple teams push):
cd infra/wateringHole
git pull --rebase origin main    # or forgejo main
git push forgejo main && git push origin main

# If cascade reports divergence:
membrane temporal.cascade --check   # see which repos diverged
# Then manually resolve per-repo
```

---

## 4. Building and Deploying Primals

### Build Pipeline

```bash
# Build a single primal (guideStone-grade):
membrane plasmid.build beardog --target x86_64-unknown-linux-musl

# Build all changed primals:
membrane plasmid.harvest

# Build for Android (grapheneGate):
membrane plasmid.harvest --target aarch64-linux-android

# Check NDK readiness:
membrane plasmid.ndk.check

# Dry-run (show what would build):
membrane plasmid.build songbird --dry-run
```

### Deploy to VPS

```bash
# Push built binaries to golgiBody (atomic replace + restart):
membrane plasmid.refresh

# Full zero-touch pipeline (harvest + refresh + health check):
membrane plasmid.pipeline

# Sync inner→outer depot (BLAKE3 diff):
membrane plasmid.depot_sync
```

### Deploy to New Gate

```bash
# One-command gate enrollment:
membrane gate.bootstrap eastGate --dry-run   # preview
membrane gate.bootstrap eastGate             # execute

# For mobile NUCs:
membrane gate.bootstrap mobileGolgi --mobile

# Check gate health after deploy:
membrane gate.status

# Read a gate's expected configuration:
membrane gate.profile eastGate
```

### Binary Depot Structure

```
plasmidBin/
├── checksums.toml        # BLAKE3 hashes per target
├── provenance.toml       # Build metadata (commit, rustc, timestamp)
├── sources.toml          # Source registry (repo URLs, binary names)
└── primals/
    ├── x86_64-unknown-linux-musl/    # VPS + desktop gates
    │   ├── beardog
    │   ├── songbird
    │   └── ... (13 binaries)
    └── aarch64-unknown-linux-musl/   # grapheneGate + ARM NUCs
        └── ... (13 binaries)
```

---

## 5. Configuration Resolution

### membrane.toml

Located at `gardens/cellMembrane/membrane.toml` or `/etc/membrane/membrane.toml`:

```toml
[membrane.layers.inner]
host = "golgiBody"
ssh_alias = "golgi"
ip = "157.230.3.183"

[membrane.layers.peptidoglycan]
host = "peptidoglycan"
ip = "157.230.209.218"

[membrane.layers.outer]
host = "golgiBody-ext"
ip = "137.184.197.151"
```

### Environment Variables (key ones)

| Variable | Default | Purpose |
|----------|---------|---------|
| `MEMBRANE_SSH_HOST` | `golgi` | SSH alias for inner membrane |
| `PEPTI_SSH_HOST` | `pepti` | SSH alias for peptidoglycan |
| `GOLGI_EXT_HOST` | `golgi-ext` | SSH alias for outer membrane |
| `FORGEJO_SSH_HOST` | `git.primals.eco:2222` | Forgejo clone endpoint |
| `ECOPRIMALS_ROOT` | `~/Development/ecoPrimals` | Local workspace root |
| `VPS_ECOPRIMALS_ROOT` | `/opt/ecoPrimals` | VPS workspace root |
| `MEMBRANE_VPS_PEER` | `157.230.3.183:7700` | Songbird federation peer |
| `WAN_DEPOT_URL` | `https://membrane.primals.eco/depot` | Public binary depot |
| `MEMBRANE_INSTALL_BASE` | `/opt/membrane` | Binary install base |
| `ANDROID_NDK_HOME` | — | NDK root for Android cross-compile |

### Priority Order

1. Environment variables (highest)
2. `membrane.toml` in workspace
3. Compiled defaults (lowest)

---

## 6. AI Interaction Patterns

### Starting a Session

When an AI instance connects to any part of this project:

1. **Read this document** for infrastructure context
2. **Read the repo's own README** for domain-specific context
3. **Cascade**: `git pull --ff-only forgejo main` on relevant repos
4. **Check wateringHole** for active impulses (FRAGOs) and handoffs

### Common Operations

```bash
# "Cascade from VPS and review" means:
cd /path/to/repo && git pull --ff-only forgejo main
cd /path/to/wateringHole && git pull --ff-only forgejo main
# + git pull --ff-only origin main (resolve if diverged)
# Then review what changed (git log, active impulses)

# "Push via cascade" means:
git add -A && git commit -m "message"
git push forgejo main && git push origin main

# "Check VPS state" means:
membrane gate.health         # 13-primal sweep via SSH
membrane gate.status         # local gate health
ssh golgi 'pgrep -la server' # raw process list
```

### Handoff Conventions

When finishing work that other teams need:
1. Create a handoff in `wateringHole/handoffs/`: `{PRIMAL}_{VERSION}_{TOPIC}_{DATE}.md`
2. Update the active FRAGO if applicable
3. Push both wateringHole remotes
4. If blocking other work, create an impulse in `impulses/active/`

### Error Recovery

| Situation | Action |
|-----------|--------|
| `ff-only` fails | `git pull --rebase origin main` then retry push |
| Freshness conflict | `git checkout --theirs freshness.toml && git add && git commit` |
| SSH timeout to golgi | Check if VPS is up: `ping 157.230.3.183` |
| pepti unreachable | pepti routes through golgi: fix golgi first |
| Build fails (NDK) | `membrane plasmid.ndk.check` — verify toolchain |
| Stale depot | `membrane plasmid.harvest --force` then `plasmid.depot_sync` |

---

## 7. Gate Profiles

Gates are declared in `ecosystem_manifest.toml` under `[gates.*]`:

| Gate | Arch | Mobility | Transport | Composition | Role |
|------|------|----------|-----------|-------------|------|
| eastGate | x86_64-musl | fixed | LAN | full | Primary dev + build host |
| ironGate | x86_64-musl | fixed | LAN | full | Secondary dev gate |
| southGate | x86_64-musl | fixed | LAN | full | Science/ABG gate |
| strandGate | x86_64-musl | fixed | LAN | full | CompChem + genomics |
| grapheneGate | aarch64-musl | mobile | adb | full | Pixel 8a trust anchor |
| flockGate | x86_64-musl | fixed | WAN | full | WAN shadow (sporePrint) |
| golgiBody | x86_64-musl | fixed | local | full | VPS inner membrane |
| peptidoglycan | x86_64-musl | fixed | local | builds | VPS structural layer |
| golgiBody-ext | x86_64-musl | fixed | local | relay | VPS outer membrane |

---

## 8. Primal Composition

### The 13 NUCLEUS Primals

| Primal | Binary | Domain | IPC Port (default) |
|--------|--------|--------|-------------------|
| bearDog | `beardog` | Cryptography | UDS |
| songBird | `songbird` | Networking | 7700 (federation) |
| nestGate | `nestgate` | Storage | UDS |
| toadStool | `toadstool` | Hardware | UDS |
| barraCuda | `barracuda` | Math/GPU | UDS |
| coralReef | `coralreef` | Shader compile | UDS |
| squirrel | `squirrel` | AI coordination | UDS |
| biomeOS | `biomeos` | Orchestration | UDS |
| rhizoCrypt | `rhizocrypt` | Provenance | UDS |
| loamSpine | `loamspine` | Persistent store | UDS |
| sweetGrass | `sweetgrass` | Data provenance | UDS |
| petalTongue | `petaltongue` | UI/CLI | UDS |
| skunkBat | `skunkbat` | Telemetry | UDS |

### Standard Startup Envelope (Wave 109)

```bash
$PRIMAL server --bind-mode $PRIMAL_BIND_MODE --port $PORT
```

- `PRIMAL_BIND_MODE`: `uds_only` | `tcp_only` | `dual` | `fallback`
- UDS sockets at: `/run/membrane/{primal}.sock` or `$XDG_RUNTIME_DIR/biomeos/{primal}.sock`

### Standard Health Endpoint (HEALTH-01)

```json
→ {"jsonrpc":"2.0","method":"health","params":{},"id":1}
← {"jsonrpc":"2.0","result":{"status":"ok","primal":"beardog","version":"0.9.1","uptime_s":42},"id":1}
```

---

## 9. Wave System

### What Waves Are

Waves are numbered iterations of ecosystem-wide coordination. Each wave has:
- A **blurb** (high-level guidance from overwatch)
- A **FRAGO** (Fragmentary Order — machine-readable TOML in `impulses/active/`)
- **Handoffs** (per-team deliverables in `handoffs/`)

### Current Wave: 109 — guideStone Deployment Convergence

5 work streams: Standard startup contract, Build pipeline + gate profiles, Post-deploy validation, BTSP E2E, cellMembrane cascade hardening.

### Wave Lifecycle

```
Blurb issued → FRAGO filed → Teams execute → Handoffs filed →
FRAGO updated → Blurb archived → Next wave
```

### Active FRAGOs

Check: `ls infra/wateringHole/impulses/active/`

---

## 10. Development Workflow (for AI agents)

### Before Starting Work

1. Cascade: `git pull --ff-only forgejo main` (all relevant repos)
2. Read active impulses in `wateringHole/impulses/active/`
3. Check freshness: `cat infra/wateringHole/freshness.toml | grep {repo}`
4. Identify which stream/wave item you're working on

### During Work

- Commit early, push often (both remotes)
- Zero clippy warnings, zero `unwrap()`, zero `#[allow()]`
- All files under 1000 LOC
- Update FRAGOs as items complete

### After Work

1. Push to both remotes: `git push forgejo main && git push origin main`
2. If completing a wave item: update the active FRAGO
3. If handing off: create handoff doc in wateringHole
4. If blocking others: file impulse

### Testing

```bash
cargo clippy --workspace --all-targets  # zero warnings
cargo fmt --all -- --check              # formatted
cargo test --workspace                  # all pass
```

---

## 11. Critical Operational Knowledge

### VPS Process Management

```bash
# On golgiBody — primals run as systemd services:
ssh golgi 'systemctl list-units | grep membrane'

# Restart a primal:
ssh golgi 'systemctl restart membrane-nucleus@beardog'

# Check logs:
ssh golgi 'journalctl -u membrane-nucleus@songbird --since "5 min ago"'

# Start songbird federation manually:
ssh golgi 'cd /opt/ecoPrimals/primals/songBird && nohup ./target/release/songbird server --federation --port 7700 &'
```

### Forgejo Administration

```bash
# On golgiBody:
ssh golgi '/opt/forgejo/forgejo admin user list'
ssh golgi '/opt/forgejo/forgejo admin repo list'

# API (from anywhere with token):
curl -H "Authorization: token $(cat ~/.config/forgejo/token)" \
  https://git.primals.eco/api/v1/repos/search?q=bearDog
```

### Caddy (TLS/Reverse Proxy)

```bash
# On golgiBody-ext:
ssh golgi-ext 'systemctl status caddy'
ssh golgi-ext 'cat /etc/caddy/Caddyfile'

# WAN depot is served from:
# /opt/ecoPrimals/infra/plasmidBin/ → https://membrane.primals.eco/depot/
```

### plasmidBin Depot Sync

```bash
# Inner → outer membrane binary flow:
membrane plasmid.depot_sync

# This compares BLAKE3 hashes between golgi:/opt/ecoPrimals/infra/plasmidBin/
# and golgi-ext:/opt/ecoPrimals/infra/plasmidBin/, copies changed binaries,
# and updates checksums on the outer membrane.
```

---

## 12. guideStone Properties (deployment standard)

Every deployment artifact must satisfy:

| # | Property | Verification |
|---|----------|-------------|
| P1 | **Deterministic** | Same depot + gate profile = identical state |
| P2 | **Reference-Traceable** | `provenance.toml` has commit + rustc + timestamp + blake3 |
| P3 | **Self-Verifying** | BLAKE3 mismatch = abort (fail closed) |
| P4 | **Environment-Agnostic** | musl-static, no runtime deps |
| P5 | **Tolerance-Documented** | Named tolerances in deployment.toml |

---

## 13. Quick Reference Commands

```bash
# Cascade from VPS:
cd ~/Development/ecoPrimals/gardens/cellMembrane && git pull --ff-only forgejo main
cd ~/Development/ecoPrimals/infra/wateringHole && git pull --ff-only forgejo main

# Build + deploy cycle:
membrane plasmid.build beardog
membrane plasmid.refresh
membrane gate.status

# Check ecosystem state:
membrane gate.health
membrane plasmid.status

# Gate profile:
membrane gate.profile eastGate

# Full cascade:
membrane temporal.cascade --with-harvest
```

---

## 14. History & Context for Humans

### Project Genesis

ecoPrimals is a sovereign computing ecosystem — 13 Rust primals that compose into NUCLEUS deployments. The goal is reproducible scientific computation without vendor lock-in: pure Rust, zero C dependencies, WGSL GPU compute, content-addressed storage, cryptographic provenance.

### Evolution Timeline

- **Waves 1-40**: Individual primal development, Python→Rust ports in springs
- **Waves 40-60**: NUCLEUS composition, deployment scripts, sovereignty graduation
- **Waves 60-80**: K-Derm diderm topology, VPS deployment, 5-gate mesh
- **Waves 80-106**: Cross-topology validation, grapheneGate 13/13, WAN deployment
- **Waves 106-108**: Deterministic deployment (6 invariants), NDK cross-compile, full rebuild
- **Wave 109**: guideStone convergence — making all deployments identical and self-verifying

### The Bio-Inspired Architecture

- **Primals** = organisms (autonomous, self-contained)
- **Springs** = validation niches (scientific domain proofs)
- **Gardens** = membrane layers (cellMembrane = infrastructure coordination)
- **Gates** = deployment endpoints (eastGate, grapheneGate, etc.)
- **K-Derm** = cell membrane topology (inner/peptidoglycan/outer)
- **NUCLEUS** = atomic composition (Tower + Node + Nest = 9 core)
- **Impulses** = coordination signals (FRAGOs, handoffs)
- **Cascade** = temporal sync flow (Forgejo → gates → GitHub)

### The White Paper

`infra/whitePaper/gen5/` contains the current generation scientific white paper. It documents the ecosystem architecture, sovereignty model, and scientific validation approach for external audiences.

---

*This document is the state-safe bootstrap. If you lose all context, read this first.*
