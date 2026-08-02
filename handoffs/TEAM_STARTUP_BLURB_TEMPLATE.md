# Team Startup Blurb — Post Wave 155n (Springs+Gardens Phase)

**From**: eastGate overwatch
**Purpose**: Paste this into any new IDE session on any gate. It bootstraps
the gate through four phases: connectivity → sync → enrollment → work.

**Two audiences**:
- **Gate teams**: Phases 0–2 (connectivity, sync, enrollment). Deploy NUCLEUS on hardware.
- **Code teams**: Phases 0–1 (connectivity, sync), then Phase 3 (garden/spring work). Build ON the primals.

**Four-phase flow**:
0. **Connectivity**: SSH config for Forgejo (NO WireGuard needed — Forgejo is public)
1. **Sync**: Pull all repos from Forgejo, fix naming divergences, clone missing repos
2. **Enrollment**: WireGuard mesh + Tower Atomic — **GATE TEAMS ONLY** (required for primal IPC, not for code)
3. **Work**: Garden/spring-specific tasks — **CODE TEAMS ONLY**

---

## PHASE 0: CONNECTIVITY — Forgejo Access

Forgejo (`git.primals.eco`) runs on golgiBody, a **public VPS**. You do NOT
need WireGuard to access it. WireGuard is only needed later for inner membrane
primal IPC. There are two access methods:

### Option A: HTTPS (zero-config, read-only — start here)

All ecoPrimals repos are public. HTTPS clone/pull works immediately with
**no SSH key, no config, no registration**:

```bash
git clone https://git.primals.eco/ecoPrimals/bearDog.git primals/bearDog
```

Use this for initial sync if SSH isn't set up yet. You can repoint to SSH later
when you need push access (only needed for wateringHole handoffs per convergence rule).

### Option B: SSH (read + write — set up when needed)

SSH gives push access for filing handoffs. Port 2222 is open to the internet.

**Step 0b-1: Add host key**

```bash
ssh-keyscan -p 2222 git.primals.eco >> ~/.ssh/known_hosts 2>/dev/null
```

**Step 0b-2: SSH config** — add to `~/.ssh/config` (create if missing):

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

**Step 0b-3: Verify**

```bash
ssh -T git@git.primals.eco
# Should return: "Hi <user>! You've successfully authenticated..."
```

If this fails with "Permission denied", your SSH key isn't registered in Forgejo.
Use HTTPS (Option A) for now — you can pull everything read-only and set up SSH
later when you need push access.

---

## PHASE 1: SYNC — Pull All Repos

### What is ecoPrimals

ecoPrimals is a sovereign, AGPL-3.0 mesh operating system built in pure Rust.
13 primals (autonomous binaries) compose into **atomics**: Tower (security +
discovery + defense), Node (Tower + compute), Nest (Tower + storage +
provenance), and NUCLEUS (all 13). biomeOS orchestrates via a Neural API
with 27 signal graphs and semantic dispatch (`tower.health`, `node.compute`,
`nest.store`, etc.). biomeOS is the **composition broker** — it propagates
BTSP trust and riboCipher framing across atomic boundaries. All binaries
("genomeBins") are served from a single depot on golgiBody
(`https://depot.primals.eco`). Gates are physical machines running Tower
Atomic or higher compositions.

### Current State (Post Wave 155n — Aug 1, 2026)

**Posture**: ZERO P0/P1/P2. Wave 155 POST-THRESHOLD. gen5 THESIS PROVEN ON LIVE DATA.
7 glacial goals COMPLETE. NUCLEUS on 5 gates. Sovereign CI LIVE. 33.79 GB real data ingested.
All 15 primals shipped. Springs+gardens phase: build workloads ON the primals.

| Fact | Value |
|------|-------|
| Wave | 155n (CLOSED) — springs+gardens phase |
| Primals | 15 (13 active + 2 dormant). **All shipped. Substrate is stable.** |
| Tests | **~101K+** across 15 primals |
| biomeOS | **v4.56** — G22 COMPLETE: single-process, dual-protocol (riboCipher + JSON-RPC), 244 caps, 27 signal graphs |
| BTSP | 13/13 — all primals ship bearDog ClientHello |
| Depot | **46 binaries** (16 musl + 15 gnu + 15 windows). BLAKE3 verified. |
| Gates | **5 NUCLEUS** (westGate, strandGate, blueGate, sporeGate, **southGate 22/22 PASS**). G17+G8 PROVEN. |
| Jelly strings | **11/11 resolved** (J12 LIVE E2E SSH, J18 CODE SHIPPED) |
| Sovereign CI | **LIVE** — push-to-deploy for ALL 13 primals. sporeGate build authority. blueGate sub-builder (J12). |
| Provenance | **7/7 COMPLETE** — E2E on Linux + Windows, 8 consecutive passes |
| Forgejo | `ssh://git@git.primals.eco:2222/` — canonical remote (PUBLIC) |
| P0/P1/P2 | **ZERO** |
| Glacial goals | **31 tracked** (7 COMPLETE: G3+G4+G8+G10+G17+G21+G22) |

### Gate-Team Assignments

| Gate | Role | Hardware | Status |
|------|------|----------|--------|
| **eastGate** | Overwatch, code hub | 10G SFP+ | ONLINE |
| **westGate** | Nest Atomic workhorse | Ryzen 7 5700X, 64GB, ZFS raidz1 50.7TB | **NUCLEUS v4.56 G22.** Prov 7/7. AlphaFold ready. |
| **strandGate** | Node Atomic workhorse | Dual EPYC 7452, RTX 3090 | **NUCLEUS v4.55.** Needs v4.56 redeploy. hotSpring target. |
| **sporeGate** | Build authority, depot | Full NUCLEUS, Sovereign CI | **NUCLEUS v4.56 G22.** 46 depot bins. J12 dispatch. |
| **blueGate** | Windows sub-builder | Windows, house2, 10G backbone | **NUCLEUS v4.56.** J12 LIVE E2E. membrane.exe. |
| **ironGate** | GPU compute, esotericWebb host | 14TB HDD, GPU | ONLINE. esotericWebb migration target. |
| **southGate** | **Validation gate — 22/22 PASS** | 5800X3D + RTX 4060 + 128GB + 5TB NVMe | **NUCLEUS PROVEN.** G17+G8. No WG. Own family. 20h stable. |
| **golgiBody** | Depot, Forgejo, enrollment, relay | Sole depot (public VPS) | ONLINE |
| **northGate** | AlphaFold data source (~1TB) | Windows, RTX 5090 | **DAILY DRIVER — DO NOT DEPLOY** |
| **swiftGate** | Second Windows proof | Windows, house2 | After blueGate |

### Active Gardens/Springs (what code teams work on)

| Garden/Spring | Type | What | Gate | Website |
|---------------|------|------|------|---------|
| **hotSpring** | Spring | QCD dynamical programming — GPU lattice simulations, continuous background compute | strandGate (RTX 3090) | primals.eco/hotspring/ |
| **esotericWebb** | Garden | Game engine / creative sandbox on NUCLEUS | ironGate | primals.eco/webb/ |
| **footPrint** | Garden | GIS data visualization, 478 TS tests | any NUCLEUS gate | **LIVE** at primals.eco/footprint/ |
| **sporePrint** | Infra | Public website — triage 334→120 pages, demonstration era | golgi (Caddy) | primals.eco |

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
│   └── rustChip         # Rust tooling
└── infra/          # Infrastructure and documentation (mixed orgs — see mapping)
    ├── wateringHole      # Standards, handoffs, blurbs (ecoPrimals/)
    ├── plasmidBin        # Depot binaries + enrollment scripts (ecoPrimals/)
    ├── fossilRecord      # Archived/completed documentation (ecoPrimals/)
    ├── sporePrint        # SEO / web presence (ecoPrimals/) — empty placeholder on Forgejo
    ├── whitePaper        # Research papers, JOSS publication (ecoPrimals/)
    ├── agentReagents     # Agent tooling (syntheticChemistry/)
    └── benchScale        # Topology benchmarking (syntheticChemistry/)
```

### Windows Prerequisites (blueGate, swiftGate, northGate)

Windows gates need these steps before syncing:

```powershell
# Install Git if not present
winget install Git.Git

# Required: enable long paths (NTFS 260-char limit breaks fossilRecord)
git config --global core.longpaths true

# Required: disable credential manager prompts (blocks non-interactive sessions)
$env:GIT_TERMINAL_PROMPT = 0
$env:GCM_INTERACTIVE = "never"
[Environment]::SetEnvironmentVariable("GIT_TERMINAL_PROMPT", "0", "User")
[Environment]::SetEnvironmentVariable("GCM_INTERACTIVE", "never", "User")

# Recommended: OS-level long path support (requires admin)
# Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
```

### Step 1a: Fix Naming Divergences

Older gate checkouts may have lowercase directory names. Fix them first:

```bash
cd ~/Development/ecoPrimals

# Remove symlinks that point at wrong-case targets (e.g. toadStool → toadstool)
# Must happen BEFORE renames to avoid breaking the symlink target
for d in primals/* gardens/* springs/* infra/*; do
  [ -L "$d" ] && echo "REMOVING SYMLINK: $d → $(readlink $d)" && rm "$d"
done

# Fix case-mismatched primal directories (if they exist)
[ -d primals/beardog ] && [ ! -d primals/bearDog ] && mv primals/beardog primals/bearDog
[ -d primals/nestgate ] && [ ! -d primals/nestGate ] && mv primals/nestgate primals/nestGate
[ -d primals/songbird ] && [ ! -d primals/songBird ] && mv primals/songbird primals/songBird
[ -d primals/toadstool ] && [ ! -d primals/toadStool ] && mv primals/toadstool primals/toadStool

# Remove known duplicates (lowercase when camelCase already exists)
[ -d primals/toadstool ] && [ -d primals/toadStool ] && rm -rf primals/toadstool
[ -d springs/barraCuda ] && rm -rf springs/barraCuda

# Fix branch names (master → main)
for d in primals/* gardens/* springs/* infra/*; do
  [ -d "$d/.git" ] || continue
  (cd "$d" && branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
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

# Detect SSH availability (set once, used by all functions)
if ssh -T git@git.primals.eco 2>&1 | grep -q "successfully authenticated"; then
  FORGEJO_PROTO="ssh"
  echo "SSH authenticated — using SSH URLs"
else
  FORGEJO_PROTO="https"
  echo "SSH not available — using HTTPS (read-only, push needs SSH later)"
fi

forgejo_url() {
  local org="$1" name="$2"
  if [ "$FORGEJO_PROTO" = "ssh" ]; then
    echo "ssh://git@git.primals.eco:2222/${org}/${name}.git"
  else
    echo "https://git.primals.eco/${org}/${name}.git"
  fi
}

repoint_or_reclone() {
  local dir="$1" org="$2" name=$(basename "$1")
  if [ ! -d "$dir/.git" ]; then return; fi
  local current=$(cd "$dir" && git remote get-url origin 2>/dev/null)
  local target=$(forgejo_url "$org" "$name")
  if [ "$current" = "$target" ]; then return; fi

  # Repoint
  (cd "$dir" && git remote set-url origin "$target")
  echo "REPOINTED: $name → $org ($FORGEJO_PROTO)"

  # Test if histories are compatible
  if ! (cd "$dir" && git fetch origin 2>/dev/null && git merge-base --is-ancestor HEAD origin/main 2>/dev/null); then
    echo "  SHALLOW ROOTS: $name — histories incompatible, fresh cloning..."
    local dirty=$(cd "$dir" && git status --porcelain 2>/dev/null | wc -l)
    if [ "$dirty" -gt 0 ]; then
      local stash="${dir}.stash-$(date +%s)"
      echo "  STASHING dirty files → $stash"
      mkdir -p "$stash"
      (cd "$dir" && git diff > "$stash/tracked.patch" 2>/dev/null)
      (cd "$dir" && git status --porcelain | awk '{print $2}' | while read f; do
        [ -f "$f" ] && cp --parents "$f" "$stash/" 2>/dev/null
      done)
    fi
    rm -rf "$dir"
    git clone "$target" "$dir"
    echo "  RECLONED: $name from Forgejo ($FORGEJO_PROTO)"
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
    git clone "$(forgejo_url "$org" "$name")" "$dir"
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
         ludoSpring neuralSpring rustChip; do
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
3. Read `infra/wateringHole/ORTHOGONAL_DIMENSIONS_REVIEW.md` — 10 active + 13 fossilized dimensions
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
`infra/wateringHole/handoffs/[GATE_NAME]_OVERWATCH_SYNC.md`

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
| sporeGate | 10.13.37.2 | LIVE (site router, peptidoglycan anchor H1) |
| eastGate | 10.13.37.5 | LIVE |
| flockGate | 10.13.37.6 | DOWN (dead CMOS / RustDesk lockout) |
| ironGate | 10.13.37.7 | LIVE |
| northGate | 10.13.37.8 | LIVE (daily driver — no deploy) |
| southGate | 10.13.37.9 | **NO WG** (deliberate — validation gate) |
| strandGate | 10.13.37.10 | LIVE (NUCLEUS) |
| westGate | 10.13.37.11 | LIVE (NUCLEUS, ZFS 50.7TB) |
| blueGate | 10.13.37.12 | LIVE (NUCLEUS, Windows, sub-builder) |
| swiftGate | 10.13.37.13 | PENDING KEYGEN |

### Step 2a: WireGuard Setup (HUMAN — requires admin)

**Linux:**

```bash
wg genkey | tee /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey
chmod 600 /etc/wireguard/privatekey

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

sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
ping -c 3 10.13.37.1
```

**Windows (blueGate, swiftGate, northGate):**

Install WireGuard from https://www.wireguard.com/install/. Then in the
WireGuard GUI: Add Tunnel → Create from scratch. Paste this config
(replace `YOUR_IP` and `YOUR_PRIVATE_KEY`):

```ini
[Interface]
Address = YOUR_IP/24
PrivateKey = YOUR_PRIVATE_KEY
ListenPort = 51821

[Peer]
PublicKey = A2fvz3czkqRUuu2mzkSS6IVr/TCQcpsJX9HbDBa1FBc=
Endpoint = 157.230.3.183:51820
AllowedIPs = 10.13.37.0/24
PersistentKeepalive = 25
```

Generate keys from PowerShell (admin):

```powershell
# WireGuard must be installed first
& "C:\Program Files\WireGuard\wg.exe" genkey | Tee-Object -Variable privateKey | & "C:\Program Files\WireGuard\wg.exe" pubkey
# Copy the public key output and send to eastGate overwatch
```

Activate the tunnel in WireGuard GUI. Verify: `ping 10.13.37.1`

**IMPORTANT**: Send your public key to eastGate overwatch so it can be
registered on golgiBody. If your gate is already REGISTERED in the table
above, your peer config may already exist on golgiBody — just bring up the tunnel.

### Step 2b: Set Hostname

**Linux:**
```bash
sudo hostnamectl set-hostname YOUR_GATE_NAME
```

**Windows:**
```powershell
Rename-Computer -NewName YOUR_GATE_NAME -Restart
```

### Step 2c: Deploy Tower Atomic

Tower Atomic (bearDog + songBird + skunkBat) must be deployed before any
workload primals. Fetch genomeBins from the depot.

**Linux:**
```bash
mkdir -p ~/.local/bin
for primal in beardog songbird skunkbat; do
  curl -fsSL "https://depot.primals.eco/primals/$(uname -m)-unknown-linux-musl/${primal}" \
    -o ~/.local/bin/${primal}
  chmod +x ~/.local/bin/${primal}
done
```

**Windows:**

All 14 primal `.exe` binaries are available on the depot (`x86_64-pc-windows-gnu`).
No source build needed — download directly:

```powershell
$depotBase = "https://depot.primals.eco/primals/x86_64-pc-windows-gnu"
$binDir = "$env:USERPROFILE\.local\bin"
New-Item -ItemType Directory -Force -Path $binDir | Out-Null
foreach ($primal in @("beardog", "songbird", "skunkbat")) {
    Invoke-WebRequest -Uri "$depotBase/$primal.exe" -OutFile "$binDir\$primal.exe"
    Write-Host "Downloaded: $primal.exe"
}
# Add to PATH if not already there:
# [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$binDir", "User")
```

If you need to build from source instead (e.g., testing local changes):
```powershell
cd ~/Development/ecoPrimals/primals/bearDog
cargo build --release
# Binary at target/release/beardog.exe
```

### Step 2d: Validate Tower

```bash
# Linux: Start Tower Atomic primals and verify health
# Windows: Run from PowerShell or as Windows Service
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

### CODE TEAM: hotSpring (QCD dynamical programming)

> **hotSpring** — springs/hotSpring. Target gate: **strandGate** (RTX 3090).
> Tests: 627+ | Last evolution: Wave 113 (riboCipher REJECT)
>
> **Purpose**: GPU-resident lattice QCD — run all dynamical options over time
> in background, serve custom computation requests as we understand the physics.
> HMC, pseudofermion, metadynamics, free energy surfaces.
>
> **Primals used**: barraCuda (tensor), toadStool (dispatch), coralReef (shaders),
> sweetGrass (provenance DAG), biomeOS (orchestration), songBird (IPC).
>
> **Catch-up needed**: biomeOS evolved from v4.45 → v4.56 (G22 single-process,
> unified namespace, dual-protocol). hotSpring's `primal_bridge.rs` and
> `composition.rs` need updating for v4.56 capability changes. The
> `by_domain()` migration (GAP-HS-002) is already done.
>
> **Website surface**: primals.eco/hotspring/ — live QCD visualizations
> rendered by petalTongue from strandGate GPU output.
>
> **Open gaps**: GAP-HS-001 (squirrel round-trip), GAP-HS-005 (ionic GPU lease).

### CODE TEAM: esotericWebb (game engine / creative)

> **esotericWebb** — gardens/esotericWebb. Target gate: **ironGate** (migrated from flockGate DOWN).
> Tests: 472 | Version: V22 | Last evolution: Wave 150o
>
> **Purpose**: Interactive game engine / creative sandbox running on NUCLEUS.
> Scene binding, NPC dialogue, WebGL rendering via petalTongue IPC.
>
> **Primals used**: petalTongue (rendering), squirrel (NPC AI), songBird (IPC),
> biomeOS (composition).
>
> **Open gaps**: GAP-002 (petalTongue CRPG scene type — resolved on Webb side,
> awaiting petalTongue v1.7+ deploy), GAP-003 (squirrel NPC dialogue constraint enforcement).
>
> **Website surface**: primals.eco/webb/ — interactive demo.

### CODE TEAM: sporePrint (website triage)

> **sporePrint** — infra/sporePrint. Deploys to golgi via Forgejo auto-publish hook.
> See `SPOREPRINT_BLURB.md` for full task breakdown.
>
> **Purpose**: Transition from conceptual credibility surface to live demonstration.
> 334 pages → ~120-150 in main nav. Move stale content to /foundation/ and /backstory/.
> Add live evidence dashboards. New main nav: Lab | Science | Architecture | Products | Get Started.

### GATE TEAM: Any new gate (Tower → NUCLEUS deployment)

> **All primals are in depot.** 46 binaries across 3 platforms.
> biomeOS v4.56 (G22 COMPLETE). Tower Atomic LIVE on 6 gates.
>
> **Deployment sequence**:
> 1. Phase 0+1: Connectivity + sync (this blurb)
> 2. Phase 2: WireGuard enrollment (get IP from eastGate overwatch)
> 3. Fetch genomeBins from `https://depot.primals.eco`
> 4. Tower Atomic: bearDog + songBird + skunkBat (trust foundation)
> 5. Nest Atomic: + nestGate + rhizoCrypt + loamSpine + sweetGrass
> 6. Node Atomic: + toadStool + barraCuda + coralReef
> 7. biomeOS: Full NUCLEUS — orchestrates all 13 primals
>
> **Validate**: `tower.health` → `{ "status": "healthy" }`.
> `composition.status` → 13/13 services, socket count, capabilities.
> **Windows**: Use `x86_64-pc-windows-gnu` binaries from depot.
>
> **Report**: File sync report and validation as:
> `infra/wateringHole/handoffs/[GATE_NAME]_DEPLOYMENT_AAR.md`

### GATE TEAM: southGate (validation gate — special)

> **southGate** — VALIDATION GATE. Deliberately **NO WireGuard**.
> HW: 5800X3D + RTX 4060 + 128GB + 5TB NVMe.
>
> **Purpose**: Prove that a gate on a different LAN can deploy NUCLEUS from the
> public depot without inheriting /etc/environment or WireGuard configs.
> Validates J18 portability, G8 bonding, G17 reconstitution.
>
> **Deployment**: Use `https://depot.primals.eco` only. Own genetic lineage.
> No mesh shortcuts. If NUCLEUS launches clean, the system is portable.

### GATE TEAM: strandGate (v4.56 redeploy)

> **strandGate** — NUCLEUS v4.55. Needs v4.56 redeploy (20-minute operation).
> HW: Dual EPYC 7452, RTX 3090.
>
> **Purpose**: Node Atomic workhorse. hotSpring's target gate for GPU compute.
> After v4.56 redeploy, ready for continuous QCD lattice simulations.
>
> **Steps**: Pull biomeOS v4.56 from depot. Restart membrane-biomeos.service.
> Validate: 12/12 HEALTHY, G22 dual-protocol, socket stability.

---

## K-Derm Three-Layer Model (reference)

```
OUTER MEMBRANE — Human access (RustDesk → relay.primals.eco)
PEPTIDOGLYCAN  — LAN/HPC topology fabric (NAT, DNS, switches, cabling)
INNER MEMBRANE — Primal IPC (WireGuard wg0 + songBird :7700 + BTSP)
```

Peptidoglycan anchors: sporeGate (house1) + blueGate (house2).
biomeOS v4.56 (G22 COMPLETE) handles orchestration + trust propagation across inner membrane.

Forgejo access is OUTSIDE the inner membrane — it's public internet → golgiBody.
You only need inner membrane for primal-to-primal IPC and mesh enrollment.

---

## Glacial Goals (what we're building toward)

| # | Goal | Status |
|---|------|--------|
| G3 | Provenance Trio 7/7 | **COMPLETE** |
| G4 | NUCLEUS on multiple gates | **COMPLETE** (×4) |
| G21 | biomeOS-cellMembrane coevolution | **COMPLETE** |
| G22 | biomeOS API convergence (whitePaper milestone) | **COMPLETE** |
| G18 | squirrel → biomeOS agent orchestration | **ACTIVE** |
| G19 | petalTongue + Node Atomics live rendering | **ACTIVE** |
| G20 | esotericWebb game engine on NUCLEUS | **ACTIVE** |
| G8 | Plasmodium (multi-gate bonding) | VALIDATING (southGate) |
| G17 | Portability — reconstitute from cold | VALIDATING (southGate) |
| G11 | Any chip + drive = mesh gate | steamGate NEXT |
| G24 | Sovereign Identity Garden | CONCEPT (gate-first, phone later) |
| G23 | nestGate CAS-layer fractional replication | NEW |

28 glacial goals tracked total. See `ORTHOGONAL_DIMENSIONS_REVIEW.md` for full list.

---

## Appendix: Answers to Common Gate Questions

**Q: Do I need WireGuard to pull repos?**
No. Forgejo is on a public VPS. HTTPS works with zero config:
`git clone https://git.primals.eco/ecoPrimals/bearDog.git`. SSH (port 2222)
works too once your key is registered. WireGuard is only for inner membrane
(primal IPC, `10.13.37.x` overlay).

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
