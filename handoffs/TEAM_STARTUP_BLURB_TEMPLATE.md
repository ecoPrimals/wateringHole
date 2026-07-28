# Team Startup Blurb — Wave 155f

**From**: eastGate overwatch
**Purpose**: Paste this into any new IDE session on any gate. It bootstraps
the gate through four phases: connectivity → sync → enrollment → code teams.

**Four-phase flow**:
0. **Connectivity**: SSH config for Forgejo (NO WireGuard needed — Forgejo is public)
1. **Sync**: Pull all repos from Forgejo, fix naming divergences, clone missing repos
2. **Enrollment**: WireGuard mesh + Tower Atomic (required for primal IPC, not for code)
3. **Code team**: Paste again with team-specific section for individual primals

---

## PHASE 0: CONNECTIVITY — Forgejo SSH Setup

Forgejo (`git.primals.eco`) runs on golgiBody, a **public VPS**. Port 2222 is
open to the internet. You do NOT need WireGuard to pull repos. WireGuard is
only needed later for inner membrane primal IPC.

### Step 0a: Add Forgejo Host Key

```bash
ssh-keyscan -p 2222 git.primals.eco >> ~/.ssh/known_hosts 2>/dev/null
```

### Step 0b: SSH Config

Add to `~/.ssh/config` (create if missing):

```
Host forgejo git.primals.eco
    HostName git.primals.eco
    Port 2222
    User git
    IdentityFile ~/.ssh/id_ed25519_ecoPrimal
```

If you don't have `id_ed25519_ecoPrimal`, generate one:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_ecoPrimal -C "$(hostname)@primals.eco"
```

Then register the public key in Forgejo: `https://git.primals.eco` → Settings →
SSH/GPG Keys → Add Key. Or ask eastGate overwatch to register it as a deploy key.

### Step 0c: Verify

```bash
ssh -T git@git.primals.eco
# Should return: "Hi <user>! You've successfully authenticated..."
```

If this fails with "Permission denied", your SSH key isn't registered in Forgejo.
Ask eastGate overwatch to add it, or register at `https://git.primals.eco`.

---

## PHASE 1: SYNC — Pull All Repos

### What is ecoPrimals

ecoPrimals is a sovereign, AGPL-3.0 mesh operating system built in pure Rust.
13 primals (autonomous binaries) compose into **atomics**: Tower (security +
discovery + defense), Node (Tower + compute), Nest (Tower + storage +
provenance), and NUCLEUS (all 13). biomeOS orchestrates via a Neural API
with 26 signal graphs and semantic dispatch (`tower.health`, `node.compute`,
`nest.store`, etc.). All binaries ("genomeBins") are served from a single
depot on golgiBody (`https://depot.primals.eco`). Gates are physical machines
running Tower Atomic or higher compositions.

### Current State (Wave 155f)

**Posture**: Gate workload distribution. Teams deploying to dedicated gates.
Tower Atomic hardening first — Nest Atomic after Tower is stable.

| Fact | Value |
|------|-------|
| Wave | 155f |
| Primals | 15 (13 active + 2 dormant) |
| Tests | ~56K `#[test]` attributes across primals |
| BTSP | 13/13 — all primals ship bearDog ClientHello |
| Signal graphs | 26 (Tower 8, Nest 8, Node 3, Meta 5, Braid 2) |
| Depot | 39 genomeBins (13 primals × 3 targets) on golgiBody |
| Gates online | 7 (northGate + ironGate RustDesk degraded) |
| Jelly strings | 6/7 deployment automation items resolved |
| Forgejo | `ssh://git@git.primals.eco:2222/` — canonical remote (PUBLIC) |

### Gate-Team Assignments

| Gate | Teams / Primals | Hardware |
|------|-----------------|----------|
| **eastGate** | Overwatch, biomeOS, primalSpring, Tower stack, cellMembrane | Code hub, 10G SFP+ |
| **westGate** | petalTongue, squirrel, nestGate, rhizoCrypt, loamSpine, sweetGrass | 5x14TB HDD, Nest testbed |
| **strandGate** | toadStool, barraCuda, coralReef | Dual EPYC, RTX 3090 |
| **sporeGate** | Build authority, deployment foreman | Full NUCLEUS |
| **golgiBody** | Depot, Forgejo, enrollment, relay | Sole depot (public VPS) |

### Workspace Structure

The workspace is at `~/Development/ecoPrimals/` with this layout:

```
ecoPrimals/
├── primals/        # 15 autonomous Rust binaries (Forgejo org: ecoPrimals/)
│   ├── bearDog          # Trust foundation — crypto, BTSP, FIDO2, beacon
│   ├── songBird         # Discovery — mesh, IPC, relay, drawbridge
│   ├── skunkBat         # Defense — anomaly detection, protocol audit
│   ├── nestGate         # Content-addressed storage — CAS, provenance
│   ├── rhizoCrypt       # Lineage DAG — content identity, federation
│   ├── loamSpine        # Certificate ledger — lifecycle, verification
│   ├── sweetGrass       # Attribution braids — provenance chains
│   ├── toadStool        # Compute dispatch — GPU, wgpu, hardware learning
│   ├── barraCuda        # Tensor math — linear algebra, GPU compute
│   ├── coralReef        # Shader compilation — WGSL, SPIR-V
│   ├── biomeOS          # Orchestrator — Neural API, signal graphs, NUCLEUS
│   ├── squirrel         # AI assistant — MCP, ML
│   ├── petalTongue      # Visualization — WASM, WebGL, rendering
│   ├── sourDough        # (dormant)
│   └── bingoCube        # (dormant)
├── gardens/        # Products and integration layers (Forgejo org: sporeGarden/)
│   ├── cellMembrane     # Deployment fabric — gate config, harvest, push
│   ├── esotericWebb     # Interactive ecosystem visualization
│   ├── lithoSpore       # USB portability / pseudoSpore packaging
│   ├── projectFOUNDATION # Knowledge foundation layer
│   ├── projectNUCLEUS   # Full NUCLEUS product
│   ├── helixVision      # Helix vision system
│   ├── initioChem       # Computational chemistry
│   ├── metalForge       # Metal fabrication
│   └── blueFish         # (placeholder)
├── springs/        # Science and domain applications (Forgejo org: syntheticChemistry/)
│   ├── primalSpring     # Scenario validation + benchmarks
│   ├── hotSpring        # Compute dispatch
│   ├── wetSpring        # Biodiversity + spectral analysis
│   ├── airSpring        # Air quality / atmospheric
│   ├── groundSpring     # Geological
│   ├── healthSpring     # Health data
│   ├── ludoSpring       # Game/simulation
│   ├── neuralSpring     # Neural/NPU
│   ├── coralForge       # Coral ecology
│   └── rustChip         # Rust tooling
└── infra/          # Infrastructure and documentation (mixed orgs — see mapping)
    ├── wateringHole      # Standards, handoffs, blurbs (ecoPrimals/)
    ├── plasmidBin        # Depot binaries + enrollment scripts (ecoPrimals/)
    ├── fossilRecord      # Archived/completed documentation (ecoPrimals/)
    ├── sporePrint        # SEO / web presence (ecoPrimals/)
    ├── whitePaper        # Research papers, JOSS publication (ecoPrimals/)
    ├── agentReagents     # Agent tooling (syntheticChemistry/)
    └── benchScale        # Topology benchmarking (syntheticChemistry/)
```

### Step 1a: Fix Naming Divergences

Older gate checkouts may have lowercase directory names. Fix them first:

```bash
cd ~/Development/ecoPrimals

# Fix case-mismatched primal directories (if they exist)
[ -d primals/beardog ] && [ ! -d primals/bearDog ] && mv primals/beardog primals/bearDog
[ -d primals/nestgate ] && [ ! -d primals/nestGate ] && mv primals/nestgate primals/nestGate
[ -d primals/songbird ] && [ ! -d primals/songBird ] && mv primals/songbird primals/songBird

# Remove known duplicates (if they exist)
[ -d primals/toadstool ] && [ -d primals/toadStool ] && rm -rf primals/toadstool
[ -d springs/barraCuda ] && rm -rf springs/barraCuda

# Fix branch names (master → main)
for d in primals/* gardens/* springs/* infra/*; do
  (cd "$d" 2>/dev/null && branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
   [ "$branch" = "master" ] && git branch -m master main 2>/dev/null && echo "$(basename $d): master → main")
done
```

### Step 1b: Repoint Remotes from GitHub to Forgejo

Older gates may still point at GitHub. This script repoints all remotes to
Forgejo using the correct org mapping.

**WARNING — Shallow Roots**: GitHub-origin repos often have **incompatible
commit histories** with Forgejo and cannot fast-forward. If `git pull` fails
after repointing, you must **fresh clone** from Forgejo (back up the old
directory first if it has local changes). strandGate hit this on 7/7 GitHub
repos — all required fresh clones. westGate (31 GitHub repos) will likely
need the same treatment. The script below handles this automatically:

```bash
cd ~/Development/ecoPrimals

repoint_or_reclone() {
  local dir="$1" org="$2" name=$(basename "$1")
  if [ ! -d "$dir/.git" ]; then return; fi
  local current=$(cd "$dir" && git remote get-url origin 2>/dev/null)
  local target="ssh://git@git.primals.eco:2222/${org}/${name}.git"
  if [ "$current" = "$target" ]; then return; fi

  # Repoint
  (cd "$dir" && git remote set-url origin "$target")
  echo "REPOINTED: $name → $org"

  # Test if histories are compatible
  if ! (cd "$dir" && git fetch origin 2>/dev/null && git merge-base --is-ancestor HEAD origin/main 2>/dev/null); then
    echo "  SHALLOW ROOTS: $name — histories incompatible, fresh cloning..."
    local stash=""
    local dirty=$(cd "$dir" && git status --porcelain 2>/dev/null | wc -l)
    if [ "$dirty" -gt 0 ]; then
      stash="${dir}.stash-$(date +%s)"
      echo "  STASHING dirty files → $stash"
      mkdir -p "$stash"
      (cd "$dir" && git diff > "$stash/tracked.patch" 2>/dev/null)
      (cd "$dir" && git status --porcelain | awk '{print $2}' | while read f; do
        [ -f "$f" ] && cp --parents "$f" "$stash/" 2>/dev/null
      done)
    fi
    rm -rf "$dir"
    git clone "$target" "$dir"
    echo "  RECLONED: $name from Forgejo"
  fi
}

# primals → ecoPrimals org
for d in primals/*; do repoint_or_reclone "$d" "ecoPrimals"; done

# gardens → sporeGarden org
for d in gardens/*; do repoint_or_reclone "$d" "sporeGarden"; done

# springs → syntheticChemistry org
for d in springs/*; do repoint_or_reclone "$d" "syntheticChemistry"; done

# infra — mixed orgs
for d in wateringHole plasmidBin fossilRecord sporePrint whitePaper; do
  repoint_or_reclone "infra/$d" "ecoPrimals"
done
for d in agentReagents benchScale; do
  repoint_or_reclone "infra/$d" "syntheticChemistry"
done
```

### Step 1c: Clone Missing Repos

Check for missing repos and clone them:

```bash
cd ~/Development/ecoPrimals

clone_if_missing() {
  local dir="$1" org="$2" name="$3"
  if [ ! -d "$dir" ]; then
    echo "CLONING: $name → $dir"
    git clone "ssh://git@git.primals.eco:2222/${org}/${name}.git" "$dir"
  fi
}

# Primals (all should exist)
for p in bearDog songBird skunkBat nestGate rhizoCrypt loamSpine sweetGrass \
         toadStool barraCuda coralReef biomeOS squirrel petalTongue sourDough bingoCube; do
  clone_if_missing "primals/$p" "ecoPrimals" "$p"
done

# Gardens
for g in cellMembrane esotericWebb lithoSpore projectFOUNDATION projectNUCLEUS \
         helixVision initioChem metalForge blueFish; do
  clone_if_missing "gardens/$g" "sporeGarden" "$g"
done

# Springs
for s in primalSpring hotSpring wetSpring airSpring groundSpring healthSpring \
         ludoSpring neuralSpring coralForge rustChip; do
  clone_if_missing "springs/$s" "syntheticChemistry" "$s"
done

# Infra
clone_if_missing "infra/wateringHole" "ecoPrimals" "wateringHole"
clone_if_missing "infra/plasmidBin" "ecoPrimals" "plasmidBin"
clone_if_missing "infra/fossilRecord" "ecoPrimals" "fossilRecord"
clone_if_missing "infra/sporePrint" "ecoPrimals" "sporePrint"
clone_if_missing "infra/whitePaper" "ecoPrimals" "whitePaper"
clone_if_missing "infra/agentReagents" "syntheticChemistry" "agentReagents"
clone_if_missing "infra/benchScale" "syntheticChemistry" "benchScale"
```

### Step 1d: Pull Everything

```bash
cd ~/Development/ecoPrimals
for d in primals/* gardens/* springs/* infra/*; do
  name=$(basename "$d")
  echo "=== $name ==="
  (cd "$d" && git fetch origin 2>/dev/null && git pull --rebase origin main 2>/dev/null) || echo "SKIP: $name"
done
```

### Step 1e: Review State

After sync completes:

1. Read `infra/wateringHole/handoffs/ECOSYSTEM_BLURB.md` — universal handoff
2. Read `infra/wateringHole/wave.toml` — current wave and posture
3. Read `infra/wateringHole/ORTHOGONAL_DIMENSIONS_REVIEW.md` — 11 active + 10 fossilized dimensions
4. Check for remaining dirty repos:
```bash
for d in primals/* gardens/* springs/* infra/*; do
  name=$(basename "$d")
  dirty=$(cd "$d" 2>/dev/null && git status --porcelain 2>/dev/null | wc -l)
  [ "$dirty" -gt 0 ] && echo "$name: $dirty dirty files"
done
```

### Step 1f: Report Divergences

File your sync report as:
`infra/wateringHole/handoffs/[GATE_NAME]_OVERWATCH_SYNC_WAVE155f.md`

Report:
- Repos that failed to pull (merge conflicts, auth errors)
- Uncommitted local changes (stash or discard — ask eastGate if unsure)
- Missing repos that failed to clone
- Any extra directories not in the canonical layout (safe to keep, just report)

---

## PHASE 2: ENROLLMENT — WireGuard + Tower Atomic

**This phase requires human action and is NOT needed for code review work.**
Skip this if you're only doing code team audit/review. Enrollment is needed
when the gate will run primals (Tower Atomic or higher).

### WireGuard Mesh IP Assignments

| Gate | WG IP | Status |
|------|-------|--------|
| golgiBody | 10.13.37.1 | LIVE (hub) |
| sporeGate | 10.13.37.2 | LIVE (site router) |
| eastGate | 10.13.37.5 | LIVE |
| flockGate | 10.13.37.6 | LIVE (WAN) |
| ironGate | 10.13.37.7 | LIVE |
| southGate | 10.13.37.9 | REGISTERED |
| strandGate | 10.13.37.10 | REGISTERED |
| westGate | 10.13.37.11 | REGISTERED |
| blueGate | 10.13.37.12 | PENDING KEYGEN |
| swiftGate | 10.13.37.13 | PENDING KEYGEN |

### Step 2a: WireGuard Setup (HUMAN — requires sudo)

```bash
# Generate keypair
wg genkey | tee /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey
chmod 600 /etc/wireguard/privatekey

# Create wg0.conf (replace YOUR_IP with your gate's IP from table above)
cat > /etc/wireguard/wg0.conf << 'WGEOF'
[Interface]
Address = YOUR_IP/24
PrivateKey = CONTENTS_OF_/etc/wireguard/privatekey
ListenPort = 51821

[Peer]
# golgiBody (hub)
PublicKey = A2fvz3czkqRUuu2mzkSS6IVr/TCQcpsJX9HbDBa1FBc=
Endpoint = 157.230.3.183:51820
AllowedIPs = 10.13.37.0/24
PersistentKeepalive = 25
WGEOF

# Bring up
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0

# Verify
ping -c 3 10.13.37.1
```

**IMPORTANT**: Send your public key to eastGate overwatch so it can be
registered on golgiBody. If your gate is already REGISTERED in the table
above, your peer config may already exist on golgiBody — just bring up wg0.

### Step 2b: Set Hostname

```bash
sudo hostnamectl set-hostname YOUR_GATE_NAME
```

### Step 2c: Deploy Tower Atomic

Tower Atomic (bearDog + songBird + skunkBat) must be deployed before any
workload primals. Fetch genomeBins from the depot:

```bash
mkdir -p ~/.local/bin
for primal in beardog songbird skunkbat; do
  curl -fsSL "https://depot.primals.eco/primals/$(uname -m)-unknown-linux-musl/${primal}" \
    -o ~/.local/bin/${primal}
  chmod +x ~/.local/bin/${primal}
done
```

### Step 2d: Validate Tower

```bash
# Start Tower Atomic primals and verify health
# (exact startup depends on composition — see cellMembrane docs)
# Expected: tower.health returns { "status": "healthy" }
# Expected: tower.mesh_status returns peer count and transport info
```

---

## PHASE 3: CODE TEAM SPIN-UP

After overwatch has synced the gate (Phase 0+1 complete), paste this blurb
again with the team-specific section below for the primal(s) you're working on.

**Phase 2 (enrollment) is NOT required for code team work.** Code teams can
audit, review, build, and test locally without being on the mesh. Enrollment
is only needed when deploying primals to run as services.

### Audit Dimensions (all teams)

> Review `specs/` and the codebase/docs at root, and docs at parent
> `ecoPrimals/infra/wateringHole/` for inter-primal standards. Start with
> `wateringHole/STANDARDS_AND_EXPECTATIONS.md`, then `ECOSYSTEM_BLURB.md`.
>
> **Code Quality**
> - Linting: `cargo clippy --all-targets -- -W clippy::pedantic -W clippy::nursery` (0 warnings)
> - Formatting: `cargo fmt --check` (clean)
> - Doc checks: `cargo doc --no-deps` (0 warnings, all public items documented)
> - Idiomatic Rust: no `unwrap()` in non-test code — use `anyhow`/`thiserror`
> - File size: 800 lines max per file — split if over
> - Lean dependencies, clean module graph, no circular deps
>
> **Architecture Compliance**
> - JSON-RPC + tarpc: all IPC is JSON-RPC wire + tarpc service trait
> - genomeBin compliant: single-binary per `ECOBIN_ARCHITECTURE_STANDARD.md`
> - Semantic method naming per `SEMANTIC_METHOD_NAMING_STANDARD.md`
> - Platform-native transport: songBird universal-ipc (UDS/named pipes/TCP)
> - BTSP: must ship bearDog ClientHello for authenticated IPC
> - biomeOS neuralAPI: capabilities discoverable via `capability.call`
>
> **Test Coverage**
> - Target: 90% line coverage via `cargo llvm-cov` (report actual)
> - Required tiers: unit, integration, E2E scenario (via primalSpring)
>
> **Debt & Gaps**
> - Find all `todo!()`, `FIXME`, `HACK`, `TODO` markers
> - Hardcoded ports/names/constants → extract to config
> - Dead code, unused imports, stale feature flags
>
> **Sovereignty**
> - AGPL-3.0 / scyBorg triple-license
> - No telemetry, no cloud lock-in, pure Rust crypto
> - All genomeBins from `https://depot.primals.eco`
>
> **What have we not completed?** Report all gaps, mocks standing in for real
> integrations, TODOs, deep debt, and upstream blockers. Prioritize as P0/P1/P2.

### Key Standards (in `infra/wateringHole/`)

| Standard | Path |
|----------|------|
| Architecture | `fossilRecord/wave150s_standards/ECOBIN_ARCHITECTURE_STANDARD.md` |
| Method naming | `protocols/SEMANTIC_METHOD_NAMING_STANDARD.md` |
| Licensing | `foundations/LICENSING_AND_COPYLEFT.md` |
| Expectations | `STANDARDS_AND_EXPECTATIONS.md` |
| Pure Rust crypto | `fossilRecord/wave150s_standards/PURE_RUST_CRYPTO_PURITY_STANDARD.md` |
| Ecosystem posture | `handoffs/ECOSYSTEM_BLURB.md` |

### Convergence Rule

> **eastGate owns the codebase.** Gate teams are deployment validators
> and workload runners. Follow this workflow:
>
> 1. **DO NOT** push code changes from your gate (except wateringHole handoffs).
> 2. **Minimal edits only**: config tweaks, environment-specific settings.
> 3. **Report back**: File findings as handoffs in `infra/wateringHole/handoffs/`.
> 4. **Pull from Forgejo regularly** to stay converged.
> 5. Bugs: document in handoff with file, line, proposed fix — eastGate ships it.
>
> Handoff push access: your gate's SSH key must be registered in Forgejo with
> write access to `ecoPrimals/wateringHole`. Ask eastGate overwatch to set this up.

---

## Team-Specific Contexts (paste the relevant one)

### westGate: petalTongue

> **petalTongue** — Wave 155f, deploying to westGate.
> Version: 1.7.0 | Tests: 5,812 | Status: Stable
> Purpose: Visualization engine — WASM WebGL rendering pipeline.
> BTSP ClientHello: SHIPPED.
> Next work: Validate genomeBin deployment cycle on westGate. Confirm WASM
> pipeline runs correctly on westGate hardware. Report any platform divergences.
> Upstream: bearDog (BTSP), songBird (discovery)

### westGate: squirrel

> **squirrel** — Wave 155f, deploying to westGate.
> Version: 0.1.0 | Status: Stable
> Purpose: AI assistant with MCP integration.
> Next work: Deploy to westGate. Validate startup, capability registration
> with biomeOS neuralAPI. Report deployment divergences.
> Upstream: bearDog (BTSP), songBird (discovery), biomeOS (orchestration)

### westGate: Provenance Trio (nestGate + rhizoCrypt + loamSpine + sweetGrass)

> **Provenance Trio** — Wave 155f, deploying to westGate.
> Status: G3 CONVERGING — foundation shipped, IPC wiring deferred until Tower stable.
>
> | Primal | Version | Tests | Key Delivery |
> |--------|---------|-------|--------------|
> | nestGate | 0.5.0 | 13,236 | BTSP peer wiring, NTFS CAS safety |
> | rhizoCrypt | 0.14.17 | 1,456 | Cross-gate provenance chain, BTSP→DAG bridge |
> | loamSpine | 0.9.16 | 1,702 | Entry extraction, certificate.history RPC, delegated minting |
> | sweetGrass | 0.7.64 | 1,676 | CertificateRef on braids, cross-gate attribution, G3 READY |
>
> **Storage Tiering on westGate**: nestGate's CAS should be validated against
> the real hardware — 5x14TB HDD (cold), plus SSD/NVMe if available.
> Profile read/write latencies per tier. This data feeds Nest Atomic design.
>
> **Deferred G3 work** (after Tower stable): Wire IPC callers between primals —
> rhizoCrypt calls loamSpine.certificate.verify, sweetGrass links CertificateRef
> to loamSpine certificates, loamSpine validates MintingAuthority.
> See `aars/PROVENANCE_TRIO_G3_CONVERGENCE_155b_AAR.md` for convergence gaps.

### strandGate: Compute Trio (toadStool + barraCuda + coralReef)

> **Compute Trio** — Wave 155f, deploying to strandGate.
> Hardware: Dual EPYC 7452 (64 cores) + RTX 3090 (24GB VRAM)
>
> | Primal | Version | Tests | Key Delivery |
> |--------|---------|-------|--------------|
> | toadStool | 0.2.0 | 17,614+ | S343 wgpu cross-platform GPU pipeline |
> | barraCuda | 0.4.0 | 3,080 | BTSP client, tensor math, transport refactor |
> | coralReef | 0.2.0 | 2,896 | WGSL → SPIR-V, IPC merge resolution |
>
> Next work: Deploy all three. Validate `node.discover_hardware` signal graph —
> toadStool should discover the RTX 3090 via wgpu. Run `node.compute` and
> `node.dispatch` on real GPU workloads. Profile dispatch latency, shader
> compile times, tensor throughput. Report via handoff.
>
> See `handoffs/TOADSTOOL_S342_CROSS_PLATFORM_GPU_JUL27_2026.md` for GPU context.

### eastGate: biomeOS (reference — already running)

> **biomeOS** — Wave 155f, eastGate overwatch hub.
> Version: 0.1.0 | Tests: 8,522+ | Signal graphs: 26
> Active work: Live `tower.health` signal graph validation as teams deploy
> to gates. Monitor capability registration from deploying primals.
> See `config/capability_registry.toml` for the 19 atomic-tier translations.

### eastGate: primalSpring (reference — already running)

> **primalSpring** — Wave 155f, eastGate.
> 197 scenarios, all PASS. Calibrated for 13-gate mesh.
> Active work: Calibrate scenarios for distributed gate topology.
> Track deployment results from westGate and strandGate.

### Any gate: Tower Atomic stack (bearDog + songBird + skunkBat)

> **Tower Atomic** — required on every gate before anything else deploys.
> This is the trust foundation. Deploy first, validate, then deploy workloads.
>
> | Primal | Version | Role |
> |--------|---------|------|
> | bearDog | 0.9.0 | Crypto, BTSP auth, FIDO2, beacon genetics |
> | songBird | 0.2.1 | Discovery, mesh, IPC, relay, drawbridge |
> | skunkBat | 0.2.18 | Anomaly detection, protocol audit, ConnectivityAnomaly |
>
> Validate: `tower.health` should return `{ "status": "healthy" }` from songBird.
> `tower.mesh_status` returns mesh peer count and transport info.
> Fetch genomeBins from `https://depot.primals.eco`.

---

## K-Derm Three-Layer Model (reference)

```
OUTER MEMBRANE — Human access (RustDesk → relay.primals.eco)
PEPTIDOGLYCAN  — LAN/HPC topology fabric (NAT, DNS, switches, cabling)
INNER MEMBRANE — Primal IPC (WireGuard wg0 + songBird :7700 + BTSP)
```

northGate + ironGate have degraded outer membrane (RustDesk issues).
Peptidoglycan anchors: sporeGate (house1) + blueGate (house2).

Forgejo access is OUTSIDE the inner membrane — it's public internet → golgiBody.
You only need inner membrane for primal-to-primal IPC and mesh enrollment.

---

## Glacial Goals (what we're building toward)

| # | Goal | Status |
|---|------|--------|
| G1 | Tower on Windows | FRONTLOADED |
| G7 | Gate enmeshment | FRONTLOADED — workload distribution validates pipeline |
| G6 | bearDog public (crates.io) | READY — final audit |
| G3 | Nest Atomic Phase 0 | AFTER TOWER STABLE — westGate testbed |
| G5 | Chimera (single-process Tower) | AFTER G1 |
| G8 | Plasmodium (multi-gate bonding) | AFTER G7 |
| G9 | JOSS publication | AFTER G3+G7 |

---

## Appendix: Answers to Common Gate Questions

**Q: Do I need WireGuard to pull repos?**
No. Forgejo is on a public VPS. SSH to `git.primals.eco:2222` works from anywhere.
WireGuard is only for inner membrane (primal IPC, `10.13.37.x` overlay).

**Q: My repos point at GitHub (`github-ecoPrimal`). What do I do?**
Run Step 1b above. All canonical remotes are now on Forgejo. GitHub mirrors
exist but are not authoritative.

**Q: I have lowercase directory names (beardog, nestgate, songbird).**
Run Step 1a above. CamelCase is canonical.

**Q: I have a `springs/barraCuda` directory.**
It's a duplicate — barraCuda lives in `primals/`. Remove `springs/barraCuda`.

**Q: I have `primals/toadstool` AND `primals/toadStool`.**
Remove `primals/toadstool` (lowercase). Keep `primals/toadStool` (camelCase).

**Q: Some repos are on `master` branch, not `main`.**
Run Step 1a above — it renames `master` → `main`.

**Q: I have extra directories like `archive/`, `sort-after/`, or `springs/` duplicates.**
These are local artifacts from older waves. Safe to keep for reference, but
they're not part of the canonical layout and won't sync.

**Q: `gardens/projectFOUNDATION` is a symlink to `gardens/foundation`?**
That's fine. Some gates have both names pointing at the same repo. The
Forgejo name is `sporeGarden/projectFOUNDATION`. Keep the symlink.

**Q: `git pull` fails with "shallow roots" or "unrelated histories" after repointing?**
The GitHub and Forgejo copies diverged. Back up any dirty files, delete
the directory, and fresh clone from Forgejo. The Step 1b script handles
this automatically.

**Q: What SSH key should I use?**
`~/.ssh/id_ed25519_ecoPrimal` is the ecosystem key. If you have a gate-specific
key, that works too — just register it in Forgejo. Deploy keys (read-only) are
fine for gates that only pull.

**Q: What if barraCuda has local precision.rs / tests.rs changes?**
Stash them: `cd primals/barraCuda && git stash`. If they're intentional local
work, describe them in your sync report handoff. eastGate decides whether
to integrate.
