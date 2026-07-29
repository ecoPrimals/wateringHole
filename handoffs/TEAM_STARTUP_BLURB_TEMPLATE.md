# Team Startup Blurb — Wave 155i

**From**: eastGate overwatch
**Purpose**: Paste this into any new IDE session on any gate. It bootstraps
the gate through four phases: connectivity → sync → enrollment → code teams.

**Four-phase flow**:
0. **Connectivity**: SSH config for Forgejo (NO WireGuard needed — Forgejo is public)
1. **Sync**: Pull all repos from Forgejo, fix naming divergences, clone missing repos
2. **Enrollment**: WireGuard mesh + Tower Atomic (required for primal IPC, not for code)
3. **Code team**: Paste again with team-specific section for individual primals

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

### Current State (Wave 155i)

**Posture**: ZERO P0s. Composition broker SHIPPED (biomeOS v4.45). Nest Atomic
LIVE on westGate. Deep debt wave complete — 8 primals shipped simultaneous
sweeps. CAS on ZFS verified. RTX 3090 GPU profiled. sporeGate depot refreshed.
**NEXT**: blueGate full atomic stack (Tower → Nest → Node) on Windows.

| Fact | Value |
|------|-------|
| Wave | 155i |
| Primals | 15 (13 active + 2 dormant) |
| Tests | ~63K+ `#[test]` attributes across primals |
| BTSP | 13/13 — all primals ship bearDog ClientHello |
| Signal graphs | 27 (Tower 8, Nest 9, Node 3, Meta 5, Braid 2) |
| Depot | 19 binaries refreshed (16 musl + 3 glibc), BLAKE3 19/19 verified |
| Gates online | 9+ (westGate Nest Atomic LIVE, strandGate Tower+Compute LIVE) |
| Jelly strings | 7/8 resolved (J8 deployed) |
| Forgejo | `ssh://git@git.primals.eco:2222/` — canonical remote (PUBLIC) |
| P0s | **ZERO** — composition broker shipped, glibc fixed, WG DNS fixed |

### Gate-Team Assignments

| Gate | Teams / Primals | Hardware | Status |
|------|-----------------|----------|--------|
| **eastGate** | Overwatch, biomeOS, primalSpring, Tower stack | Code hub, 10G SFP+ | ONLINE |
| **westGate** | petalTongue, squirrel, nestGate, Provenance Trio | Ryzen 7 5700X, 64GB, 2TB NVMe, ZFS 25.4TB | **NEST ATOMIC LIVE** |
| **strandGate** | toadStool, barraCuda, coralReef | Dual EPYC 7452, RTX 3090 (FP64 ~104T) | **TOWER+COMPUTE LIVE** |
| **blueGate** | **NEXT TARGET** — full atomic stack | Windows, house2 | Tower → Nest → Node. Sub-builder. Topo owner H2. |
| **sporeGate** | Build authority, cellMembrane ops | Full NUCLEUS, 9/11 healthy | Depot refreshed |
| **golgiBody** | Depot, Forgejo, enrollment, relay | Sole depot (public VPS) | ONLINE |
| **northGate** | AlphaFold data source (~1TB) | Windows, RTX 5090 | **DAILY DRIVER — DO NOT DEPLOY** |
| **swiftGate** | Second Windows proof | Windows, house2 | After blueGate |

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
│   ├── helixVision      # Structure prediction / biomolecular validation
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
3. Read `infra/wateringHole/ORTHOGONAL_DIMENSIONS_REVIEW.md` — 9 active + 12 fossilized dimensions
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
`infra/wateringHole/handoffs/[GATE_NAME]_OVERWATCH_SYNC_WAVE155i.md`

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
| strandGate | 10.13.37.10 | LIVE (Tower+Compute) |
| westGate | 10.13.37.11 | LIVE (Nest Atomic) |
| blueGate | 10.13.37.12 | **ENROLLING — next target** |
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

**NOTE**: Windows genomeBins (`x86_64-pc-windows-gnu`) require the depot to
have them built. If not yet available, build from source:
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

### westGate: petalTongue

> **petalTongue** — Wave 155i, stable on westGate.
> Version: 1.7.0 | Tests: 6,605 | Status: Stable
> Purpose: Visualization engine — WASM WebGL rendering pipeline.
> Next work: Validate WASM pipeline on westGate. Deploy genomeBin.
> Upstream: bearDog (BTSP), songBird (discovery)

### westGate: squirrel

> **squirrel** — Wave 155i, stable on westGate.
> Version: 0.1.0 | Tests: 763 | Status: Stable
> Purpose: AI assistant with MCP integration.
> Next work: Validate capability registration with biomeOS neuralAPI.
> Upstream: bearDog (BTSP), songBird (discovery), biomeOS (orchestration)

### westGate: Provenance Trio (nestGate + rhizoCrypt + loamSpine + sweetGrass)

> **Provenance Trio** — Wave 155i, **NEST ATOMIC LIVE** on westGate.
> Status: **G3 CLOSED** (sweetGrass v0.8.0 E2E validated). Provenance 6/7 live.
>
> | Primal | Version | Tests | Key Delivery |
> |--------|---------|-------|--------------|
> | nestGate | 0.5.0 | 13,095+ | CAS on ZFS verified (3,119 objects), deep debt complete, zero unsafe, CLI evolved |
> | rhizoCrypt | 0.14.17 | 1,456 | Cross-gate provenance chain, BTSP→DAG bridge |
> | loamSpine | 0.9.16 | 1,285 | Registry drift fixed: certificate.verify/lifecycle/history discoverable |
> | sweetGrass | 0.8.0 | 1,636 | **G3 E2E validated**: LedgerClient, 11 E2E ledger tests, mock loamSpine UDS |
>
> **CAS on ZFS**: 3,119 objects on 25.4TB pool, 1.56× compression. NVMe 316 MB/s write.
> ZFS HDD 25.5 MB/s dsync. ARC 100% hit rate. AlphaFold ~1TB: ~11hr at dsync rate.
> **Provenance 7/7 blocked by**: bearDog `crypto.sign_ed25519` returns health stub.

### strandGate: Compute Trio (toadStool + barraCuda + coralReef)

> **Compute Trio** — Wave 155i, **VALIDATED** on strandGate.
> Hardware: Dual EPYC 7452 (64 cores) + RTX 3090 (24GB VRAM)
>
> | Primal | Version | Tests | Key Delivery |
> |--------|---------|-------|--------------|
> | toadStool | 0.2.0 | 9,193+ | **S346**: security fail-closed, unsafe containment (hw-safe crate), 75 doc warnings fixed |
> | barraCuda | 0.4.0 | 4,957 | **RTX 3090 profiled**: FP64 ~104T, DF64 framing corrected, deep debt sweep |
> | coralReef | 0.2.0 | 3,527 | **Deep debt**: 463 .expect() purged, PTX modernized (-363L net) |
>
> **Glibc depot SHIPPED** by sporeGate (16 musl + 3 glibc, BLAKE3 verified).
> RTX 3090 validated: tensor pipeline, linalg, spectral, shader compilation.
> GPU-resident tensor IDs: ~813× speedup at 512×512 vs JSON serialization.
> Next: Node Atomic profiling, full BTSP validation.

### eastGate: biomeOS (reference — composition broker)

> **biomeOS** — Wave 155i, eastGate. **COMPOSITION BROKER SHIPPED.**
> Version: v4.45 | Tests: 8,564 | Signal graphs: 27
> **Delivered**: riboCipher framing (`[0xEC, 0x01]` prefix), BTSP session
> propagation in signal graph executor, 35 composition broker E2E tests,
> connection pool IO evolution (BufReader), test monolith refactoring.
> Both prior P0s RESOLVED. Zero unsafe, zero TODO/FIXME.
> See `config/signal_tools.toml` for 27 signal graphs.

### eastGate: primalSpring (reference — already running)

> **primalSpring** — Wave 155i, eastGate.
> 197 scenarios, all PASS. Calibrated for 13-gate mesh.
> Active work: Calibrate scenarios for distributed gate topology.
> Track deployment results across westGate, strandGate, and blueGate.

### Any gate: Tower Atomic stack (bearDog + songBird + skunkBat)

> **Tower Atomic** — Wave 155i. Required on every gate before anything else deploys.
> This is the trust foundation. Deploy first, validate, then deploy workloads.
>
> | Primal | Version | Role |
> |--------|---------|------|
> | bearDog | 0.9.0 | Crypto, BTSP auth, FIDO2, beacon genetics |
> | songBird | 0.2.1 | Discovery, mesh, IPC, relay, drawbridge, **ACME HTTP-01 Phase 1** |
> | skunkBat | 0.2.18 | Anomaly detection, protocol audit, ConnectivityAnomaly |
>
> **Deployed LIVE**: westGate, strandGate, grapheneGate, eastGate, sporeGate.
> Validate: `tower.health` should return `{ "status": "healthy" }` from songBird.
> `tower.mesh_status` returns mesh peer count and transport info.
> Fetch genomeBins from `https://depot.primals.eco`.
> **Windows**: Use `x86_64-pc-windows-gnu` target or build from source with `cargo build --release`.

### blueGate: Full Atomic Stack — Tower → Nest → Node (Windows)

> **blueGate** — Wave 155i. **NEXT TARGET.** First full atomic stack on Windows.
> OS: Windows. Peptidoglycan anchor House 2. Sub-builder under sporeGate.
>
> **Three roles**:
> 1. **G1 proof**: Tower Atomic on Windows — first Windows Tower deployment
> 2. **Inner membrane topo owner H2**: DNS, topology services for house2
> 3. **Sub-builder**: Second build node under sporeGate — accelerates depot output
>
> **Deployment sequence**:
> 1. Phase 0+1: Connectivity + sync (this blurb)
> 2. Phase 2: WireGuard enrollment (IP: 10.13.37.12)
> 3. Tower Atomic: bearDog + songBird + skunkBat (build from source if depot lacks Windows bins)
> 4. Nest Atomic: + nestGate + rhizoCrypt + loamSpine + sweetGrass (after Tower stable)
> 5. Node Atomic: + toadStool + barraCuda + coralReef (after Nest stable)
> 6. biomeOS: Full composition broker role — orchestrates all atomics
>
> **biomeOS composition broker**: v4.45 ships riboCipher framing and BTSP session
> propagation. This will be the first gate where biomeOS brokers trust across
> Tower → Nest → Node Atomic composition transitions end-to-end.
>
> **Sub-builder setup**: After Tower stable, enroll as builder under sporeGate.
> Build Windows-native genomeBins (`x86_64-pc-windows-gnu`) for all primals.
> Push to golgiBody depot via `plasmid.push`.
>
> **Report**: File sync report and Tower validation as:
> `infra/wateringHole/handoffs/BLUEGATE_TOWER_ATOMIC_WAVE155i.md`

---

## K-Derm Three-Layer Model (reference)

```
OUTER MEMBRANE — Human access (RustDesk → relay.primals.eco)
PEPTIDOGLYCAN  — LAN/HPC topology fabric (NAT, DNS, switches, cabling)
INNER MEMBRANE — Primal IPC (WireGuard wg0 + songBird :7700 + BTSP)
```

Peptidoglycan anchors: sporeGate (house1) + blueGate (house2).
biomeOS composition broker (v4.45) handles trust propagation across inner membrane.

Forgejo access is OUTSIDE the inner membrane — it's public internet → golgiBody.
You only need inner membrane for primal-to-primal IPC and mesh enrollment.

---

## Glacial Goals (what we're building toward)

| # | Goal | Status |
|---|------|--------|
| G1 | Tower on Windows | **ACTIVE — blueGate target** |
| G7 | Gate enmeshment | **ADVANCING** — westGate+strandGate LIVE, blueGate next |
| G3 | Nest Atomic Phase 0 | **LIVE ON WESTGATE** — blueGate Nest Atomic is NEXT |
| G4 | Nest cross-platform | **ACTIVE** — blueGate (Windows) after Tower stable |
| G10 | Sub-builder mesh | **NEW** — blueGate as sub-builder under sporeGate |
| G6 | bearDog public (crates.io) | READY — final audit |
| G5 | Chimera (single-process Tower) | AFTER G1 |
| G8 | Plasmodium (multi-gate bonding) | AFTER G7 |
| G9 | JOSS publication | AFTER G3+G7 |

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
