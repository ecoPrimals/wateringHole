# Gate Setup, Sync, and Resync Standard

**Authority**: wateringHole consensus (Wave 63)
**Applies to**: Physical gates (LAN/WAN), VPS proto-fieldMouse deployments
**Prerequisites**: ecosystem_manifest.toml, K_DERM_TOPOLOGY_STANDARD.md

---

## Gate Types

### Physical Gates (Cytoplasm)

Desktop/server hardware running full NUCLEUS. Connected via LAN or WAN.
Bond type to inner membrane: **covalent**.

| Gate | Hardware | Location | Springs |
|------|----------|----------|---------|
| eastGate | Primary dev | LAN | Full ecosystem |
| ironGate | Server | LAN | Core primals + health/ludo |
| southGate | Dev | LAN | Core primals + wet/neural |
| biomeGate | Dev | LAN | Core primals + hot |
| strandGate | ABG science | LAN | Science suite + genomics |
| flockGate | WAN shadow | WAN | sporePrint + full validation |

### VPS Proto-FieldMouse Deployments (Periplasm)

DigitalOcean droplets running specialized membrane roles. The diderm envelope
consists of three nodes with distinct K-Derm layer assignments.

| Node | K-Derm Layer | Bond | Role | GitHub SSH |
|------|-------------|------|------|------------|
| golgiBody | Inner membrane (cis) | Covalent/Metallic | Forgejo sovereign store, NUCLEUS, DNS | None (revoked) |
| peptidoglycan | Peptidoglycan | Metallic | Sync relay, impulse cascade, builds | None (revoked) |
| golgiBody-ext | Outer membrane (trans) | Ionic/Weak | GitHub push, sporePrint hosting | **Yes** (ships extracellularly) |

Only the outer membrane (trans face) holds GitHub SSH write credentials.
The diderm relay chain propagates pushes with proper bond degradation:
`gate → inner (covalent) → peptidoglycan (metallic) → outer (ionic) → GitHub (weak)`.
See `hooks/forgejo/README.md` for the relay chain scripts.

---

## Prerequisites (complete BEFORE starting)

- [ ] **SSH key generated** on the new gate (`ssh-keygen -t ed25519`)
- [ ] **SSH key registered on Forgejo** (primary): `curl -X POST https://git.primals.eco/api/v1/user/keys -H "Authorization: token <TOKEN>" -H "Content-Type: application/json" -d '{"title":"<gate>","key":"<pubkey>"}'`
  - To register keys without a pre-existing token, have an existing gate admin add your SSH public key via the Forgejo web UI: **Admin Panel -> User Accounts -> Keys -> Add Key**, or request eastGate to register via the `membrane` CLI.
- [ ] **Verify Forgejo connectivity**: `ssh -p 2222 git@git.primals.eco` should print `Hi <user>!`
- [ ] **Gate profile exists** in `ecosystem_manifest.toml` under `[gates.<name>]`

GitHub SSH key registration is **not needed** for gates — gates push only to Forgejo.
The K-Derm relay chain handles GitHub propagation automatically via golgiBody-ext.
If you need read access to GitHub for cold-start (Forgejo unreachable), register
a read-only deploy key: `gh ssh-key add ~/.ssh/id_ed25519.pub --title "<gate>"`

---

## Pre-Bootstrap Cleanup

If this gate previously had repos cloned at non-standard paths, remove them:

```bash
# Known stale layouts from pre-standard workspace
rm -rf ~/Development/ecoPrimals/songbird    # superseded by primals/songBird/
rm -rf ~/Development/ecoPrimals/toadstool   # superseded by primals/toadStool/
```

---

## Known Large Repos (shallow clone recommended for WAN)

These repos have large histories and will timeout or saturate bandwidth on full WAN clone.
Use `--shallow` flag or `git clone --depth 1` for these:

| Repo | Approx Size | Notes |
|------|-------------|-------|
| bearDog | 413K LOC, 2226 files | Largest in ecosystem |
| songBird | Large history | Federation protocol |
| toadStool | Large history | Identity system |
| petalTongue | Large | NLP/taxonomy |
| hotSpring | 127K LOC, 2562 files | Thermodynamics spring |
| sporePrint | Large | Zola site + pseudoSpores |
| rustChip | Large | Embedded systems |

To unshallow later: `git fetch --unshallow`

---

## Gate Setup — Physical

### Step 1: Workspace Layout

```bash
mkdir -p ~/Development/ecoPrimals
cd ~/Development/ecoPrimals

echo "<gate-name>" > .gate
export GATE_NAME=$(cat .gate)
```

### Step 2: Clone wateringHole

wateringHole is always the first clone. It contains the ecosystem manifest,
cascade-pull, and all standards.

> **Note**: Forgejo paths are case-sensitive. Use exact casing from
> ecosystem_manifest.toml (e.g., `ecoPrimals/wateringHole`, not
> `ecoprimals/wateringhole`). Mismatched casing fails silently.

```bash
mkdir -p infra
git clone ssh://git@git.primals.eco:2222/ecoPrimals/wateringHole.git infra/wateringHole
```

If golgiBody Forgejo is unreachable, fall back to GitHub:
```bash
git clone git@github.com:ecoPrimals/wateringHole.git infra/wateringHole
```

### Step 3: Cascade Pull

cascade-pull reads the gate profile from ecosystem_manifest.toml and clones
only the repos this gate needs.

```bash
cd infra/wateringHole

# Full clone (LAN or fast connection)
./scripts/cascade-pull.sh --gate $GATE_NAME --clone-missing --source temporal

# WAN gate (shallow clone for large repos)
./scripts/cascade-pull.sh --gate $GATE_NAME --clone-missing --shallow --source temporal
```

**Fallback** — If Forgejo is unreachable (key not registered yet):
```bash
# Clone from GitHub only (uses SSH URLs when SSH agent is active)
./scripts/cascade-pull.sh --gate $GATE_NAME --clone-missing --shallow --source origin
```

This will:
- Read `[gates.<name>]` from ecosystem_manifest.toml for the repo list
- Create workspace directories (primals/, springs/, gardens/, infra/) if missing
- Clone missing repos into the standard layout
- Auto-shallow known large repos (bearDog, songBird, etc.) even without `--shallow`
- Set up both `origin` (GitHub) and `forgejo` remotes
- Run temporal sync to pull from the leading remote
- Pre-flight check Forgejo connectivity before per-repo fetches

### Step 4: Dev Platform

```bash
# Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Verify
rustc --version
cargo --version

# Zola (for sporePrint and other static site builds)
# Option A: pre-built binary (recommended)
# Download from https://www.getzola.org/documentation/getting-started/installation/
# Option B: build from source (slower)
cargo install zola
```

### Step 5: Membrane Binary (Optional)

If the gate needs VPS control or advanced temporal sync:

```bash
cd gardens/cellMembrane/crates/membrane-shadow
cargo build --release
sudo cp target/release/membrane /usr/local/bin/
```

### Step 6: NUCLEUS Deploy (Optional)

For gates running primal services:

```bash
# From plasmidBin
cd infra/plasmidBin
./deploy_gate.sh --composition tower    # Tower first
./deploy_gate.sh --composition node     # Then Node
./deploy_gate.sh --composition nest     # Then Nest
./deploy_gate.sh --composition full     # Full NUCLEUS
```

---

## Gate Setup — VPS Proto-FieldMouse

VPS nodes are provisioned via `doctl` and bootstrapped with a role-specific
configuration. They are NOT full gates — they are membrane layer nodes.

### Provisioning

```bash
doctl compute droplet create <name> \
  --image debian-12-x64 \
  --size <size-slug> \
  --region nyc1 \
  --ssh-keys <key-id> \
  --tag-names membrane,<role>
```

### Bootstrap (common to all VPS nodes)

```bash
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq git curl build-essential pkg-config libssl-dev unzip jq ufw

mkdir -p /opt/ecoPrimals
echo "<node-name>" > /opt/ecoPrimals/.gate

ssh-keygen -t ed25519 -f /root/.ssh/id_ed25519 -N "" -C "<node-name>@vps"
# Register pubkey on GitHub (gh ssh-key add) and Forgejo (API POST /user/keys)
```

### Role-Specific Bootstrap

**Inner membrane (golgiBody)**:
- Forgejo, Caddy TLS for git.primals.eco, knot-dns
- NUCLEUS primal services via UDS
- UFW: SSH + 2222 (Forgejo SSH) + 443 (Caddy)
- Workspace: wateringHole only (Forgejo serves all repo data)

**Peptidoglycan**:
- Rust, Zola, build-essential
- Full 39-repo workspace (--depth 1 for bloated repos)
- Both origin + forgejo remotes on every repo
- membrane binary built and installed
- UFW: SSH only (no public services)

**Outer membrane (golgiBody-ext)** — trans/shipping face:
- Caddy, Zola for sporePrint hosting
- wateringHole clone + `ext-github-push.sh` for GitHub publication
- GitHub SSH write credentials (only node with extracellular write access)
- UFW: SSH + HTTP + HTTPS

---

## Sync — cascade-pull

### Daily Sync

```bash
cd ~/Development/ecoPrimals/infra/wateringHole
./scripts/cascade-pull.sh --source temporal
```

`--source temporal` uses the membrane binary (if available) to:
1. Fetch all remotes (origin, forgejo) — pull from any source
2. Compare commit timestamps across remotes
3. Pull from the temporally leading remote
4. Push to the designated target (default: `forgejo` — VPS mediator model)
5. Report divergences

**Push Target**: The manifest `push_target = "forgejo"` means gates push
only to Forgejo. The VPS push mirror auto-propagates to GitHub as the
external linear ledger. Gates no longer need to worry about GitHub access.

### Automated Sync (systemd timer)

```bash
# Install systemd units
sudo cp systemd/cascade-pull.service /etc/systemd/system/
sudo cp systemd/cascade-pull.timer /etc/systemd/system/

# Configure
sudo systemctl edit cascade-pull.service
# Set Environment: ECOPRIMALS_ROOT, CASCADE_GATE, CASCADE_PARALLEL

sudo systemctl enable --now cascade-pull.timer
```

### Manual Sync Modes

```bash
# Pull from Forgejo only (inner membrane)
./scripts/cascade-pull.sh --source forgejo

# Pull from GitHub only (extracellular)
./scripts/cascade-pull.sh --source origin

# Dry run (show what would happen)
./scripts/cascade-pull.sh --source temporal --dry-run

# Check freshness without pulling
./scripts/cascade-pull.sh --check
```

---

## Resync — Recovery from Divergence

### Soft Resync (ff-only failed)

When temporal sync reports divergence (non-fast-forward), investigate:

```bash
cd <repo-path>
git log --oneline origin/main..forgejo/main  # Commits on Forgejo not on GitHub
git log --oneline forgejo/main..origin/main  # Commits on GitHub not on Forgejo
```

Resolution options:
1. **Rebase**: `git rebase origin/main` (if your work is on top)
2. **Merge**: `git merge origin/main` (creates merge commit)
3. **Force-align**: `git reset --hard <leading-remote>/main` (loses local work)

### Hard Resync (corrupted state)

When a gate's workspace is in an unrecoverable state:

```bash
# Remove the repo entirely
rm -rf <repo-path>

# Re-clone via cascade-pull
cd ~/Development/ecoPrimals/infra/wateringHole
./scripts/cascade-pull.sh --gate $GATE_NAME --clone-missing --source temporal
```

### VPS Resync

For peptidoglycan (structural layer):
```bash
# On peptidoglycan
cd /opt/ecoPrimals/infra/wateringHole
./scripts/cascade-pull.sh --gate peptidoglycan --source temporal
```

For golgiBody-ext (outer membrane / trans face):
```bash
# Sync wateringHole for relay scripts
cd /opt/ecoPrimals/infra/wateringHole
git pull --ff-only forgejo main

# Re-pull and rebuild sporePrint
cd /opt/ecoPrimals/infra/sporePrint
git pull origin main
zola build
sudo systemctl restart caddy
```

---

## Multi-Vendor VPS Plans

The diderm model is designed for vendor portability:

### Current: DigitalOcean nyc1

All three nodes in the same datacenter for <1ms inter-node latency.
Cost: ~$48/mo total.

### Planned: Multi-vendor redundancy

| Vendor | Role | Rationale |
|--------|------|-----------|
| DigitalOcean | Inner membrane (golgiBody) | Established, Forgejo data lives here |
| Hetzner | Peptidoglycan mirror | Cost-effective builds, EU jurisdiction |
| Vultr | Outer membrane backup | Geographic redundancy |

The inner membrane is the hardest to move (Forgejo data). Peptidoglycan and
outer membrane are stateless and can be reprovisioned from scratch.

### WAN Mesh Sovereign Barrier

The ultimate goal: if enough physical gates have WAN connectivity, the VPS
becomes optional. Gates form a covalent mesh via Songbird TURN relay:

```
Gate A (WAN) ←─[covalent]──→ Gate B (WAN)
     ↕                              ↕
Gate C (LAN) ←─[covalent]──→ Gate D (LAN)
```

In this model:
- Forgejo can run on any gate with stable uptime (replaces golgiBody inner)
- Temporal sync happens peer-to-peer (replaces peptidoglycan)
- sporePrint can be served from any gate with public IP (replaces golgiBody-ext)
- VPS becomes a bootstrap convenience, not a requirement

This is the **sovereign barrier**: the point where the ecosystem no longer
depends on any external provider for core operations. VPS nodes transition
from "metallic fleet" to "weak extracellular" — a nice-to-have, not essential.

---

## SSH Key Management

### Gate Key Registration

Every gate needs its SSH key registered on **Forgejo only** (inner membrane):
`curl -X POST https://git.primals.eco/api/v1/user/keys -H "Authorization: token <TOKEN>" ...`

GitHub SSH write access lives exclusively on golgiBody-ext (outer/trans membrane).
Gates do not need GitHub keys — the K-Derm relay chain handles propagation.

With the Forgejo-primary model, only Forgejo SSH access is required. GitHub
is populated by the VPS push mirror. GitHub keys are only needed if a gate
wants direct read access for cold-start when Forgejo is unreachable.

### Registered Keys (Wave 63)

| Key Name | Registered On |
|----------|---------------|
| irongate | GitHub, Forgejo |
| eastGate | Forgejo |
| southGate | Forgejo |
| flockGate | Forgejo |
| golgiBody (inner) | Forgejo (owns it) |
| peptidoglycan | Forgejo |
| golgiBody-ext (outer) | Forgejo, **GitHub** (trans face ships extracellularly) |
