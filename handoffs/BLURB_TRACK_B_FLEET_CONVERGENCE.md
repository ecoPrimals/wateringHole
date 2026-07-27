# Track B: Fleet Convergence — 5-Gate Enrollment + NUCLEUS Validation

**Wave**: 155a | **Owner**: eastGate overwatch
**Parallel with**: Track A (Evolution)

---

## GOAL

Get the 5 returning gates fully enrolled and converged via the autonomous
enrollment system. Solve remaining divergences. Validate the entire
postPrimordial deployment pipeline end-to-end using benchScale and agentReagents
to provision a NUCLEUS fleet. **All binaries from golgiBody** — zero USB,
zero manual transfer.

This track tests the membrane and the postPrimordial deployment system we built.

---

## PHASE 1: COMPLETE ENROLLMENT (5 gates → meshed)

The gates are online via RustDesk. The enrollment system is code-complete on golgiBody.

### Enrollment Execution

Each gate runs `gate-enroll.sh` — one command, zero operator intervention:

```bash
./infra/plasmidBin/enroll/gate-enroll.sh \
  --hub primals.eco \
  --gate <gate_name> \
  --token <GATE_ENROLLMENT_TOKEN> \
  --compose full
```

### Gate-by-Gate Status

| # | Gate | Current State | Enrollment Action | Post-Enrollment |
|---|------|---------------|-------------------|-----------------|
| 1 | southGate | WG keyed, repos at Wave ~114 | `--token` retroactive enrollment | Fast-forward repos from Forgejo |
| 2 | strandGate | WG keyed, repos at Wave ~114 | `--token` retroactive enrollment | Fast-forward repos from Forgejo |
| 3 | westGate | WG keyed, mixed-wave repos | `--token` retroactive enrollment | **Divergence resolution** (see below) |
| 4 | blueGate | Fresh, no WG keys | `--token` full enrollment | Clone all 43+ repos from Forgejo |
| 5 | swiftGate | Fresh, no WG keys | `--token` full enrollment | Clone all 43+ repos from Forgejo |

### Enrollment Prerequisites on golgiBody

| Prerequisite | How to Verify |
|-------------|---------------|
| songBird running with `mesh.gate_enroll` | `curl -s http://localhost:7780/enroll -d '{"jsonrpc":"2.0","method":"mesh.gate_enroll","params":{},"id":1}'` — should return error about missing params, not connection refused |
| Drawbridge route configured | `SONGBIRD_DRAWBRIDGE_ROUTES` includes `/enroll=mesh!public` |
| `GATE_ENROLLMENT_TOKEN` set | Environment variable on golgiBody songBird process |
| `FORGEJO_API_TOKEN` set | Service account token for SSH key registration |
| `FAMILY_SEED` or `BEARDOG_FAMILY_SEED` set | For encrypted seed delivery |
| WireGuard `wg0` active | `wg show wg0` shows existing peers |
| bearDog UDS available | `/run/membrane/beardog.sock` for crypto.encrypt |

### Enrollment Success Criteria

Per gate, enrollment is complete when:
1. Gate has mesh IP in .20-.254 range
2. `ping 10.13.37.1` succeeds from gate (hub reachable over WG)
3. `ssh -T git@forgejo` succeeds (Forgejo SSH key registered)
4. Family seed stored at `~/.config/ecoPrimals/family_seed.enc`
5. Gate appears in `wg show wg0` peers on golgiBody

---

## PHASE 2: CONVERGENCE — REPOS FROM GOLGI

After enrollment, each gate fetches all repos from Forgejo over the WG mesh.
Binaries come from golgiBody depot (plasmidBin), not USB.

### Standard Convergence (south, strand, blue, swift)

```bash
# Clone or fast-forward all repos
ECO_ROOT=/home/$USER/Development/ecoPrimals
mkdir -p "$ECO_ROOT"/{primals,springs,infra,gardens}

for org in ecoPrimals sporeGarden; do
  # List repos from Forgejo API
  repos=$(curl -s "http://10.13.37.1:3000/api/v1/orgs/$org/repos?limit=50" | jq -r '.[].name')
  for repo in $repos; do
    target="$ECO_ROOT/$(classify_repo $repo)"
    git clone "ssh://git@10.13.37.1:2222/$org/$repo.git" "$target/$repo" 2>/dev/null \
      || (cd "$target/$repo" && git fetch origin && git merge --ff-only origin/main)
  done
done

# Build all primals from source
for primal in "$ECO_ROOT"/primals/*/; do
  (cd "$primal" && cargo build --release 2>&1 | tail -1)
done

# Validate
cd "$ECO_ROOT/springs/primalSpring" && cargo test --release
```

### westGate Divergence Resolution

westGate has mixed-wave repos from partial GitHub pulls before SSH was revoked.
Some repos may have diverged commits that don't exist on Forgejo.

```bash
# For each repo on westGate:
cd "$repo"
git fetch origin  # origin = Forgejo

# Check for divergence
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
BASE=$(git merge-base HEAD origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "OK: $repo is current"
elif [ "$LOCAL" = "$BASE" ]; then
  git merge --ff-only origin/main
  echo "FAST-FORWARD: $repo updated"
else
  echo "DIVERGED: $repo — manual review needed"
  git log --oneline HEAD...origin/main
fi
```

Expected: most repos will fast-forward cleanly. Any diverged repos should
be inspected for local-only commits (likely stale GitHub-sourced), then
reset to Forgejo HEAD: `git reset --hard origin/main`.

### Binary Deployment from golgiBody

All gates should pull binaries from golgiBody's depot, not build locally
(source build is validation, depot is deployment):

```bash
# On each gate, after enrollment:
scp -o ProxyJump=none -P 22 \
  "golgi:/opt/plasmidBin/primals/x86_64-unknown-linux-musl/*" \
  /opt/ecoPrimals/primals/

# Or via plasmidBin fetch:
cd infra/plasmidBin && ./fetch.sh pull
```

---

## PHASE 3: NUCLEUS VALIDATION — benchScale + agentReagents

With gates enrolled and converged, validate the full NUCLEUS composition
using the existing test infrastructure.

### Level 1: Docker Composition Test (minutes)

Fast iteration — validates 13-primal composition health:

```bash
cd infra/benchScale

# Create 3-node NUCLEUS lab
cargo run -- create nucleus-test topologies/ecoprimals-nucleus-3node.yaml

# Deploy primals from golgiBody depot
./scripts/deploy-ecoprimals.sh --lab nucleus-test --plasmidbin ../plasmidBin

# Run primalSpring validation
./scripts/run-tests.sh
```

**Proves**: All 13 primals compose correctly, cross-gate health, NAT degradation handling.

### Level 2: WaterFall Cascade Test (enrollment-adjacent)

Tests the Forgejo-first cascade-pull that gates use after enrollment:

```bash
# Create 4-gate + Forgejo topology
cargo run -- create wf-test topologies/ecoprimals-waterfall-gate-sync.yaml

# Deploy and validate cascade
./scripts/deploy-waterfall.sh --lab wf-test
```

**Proves**: Forgejo sync parity, cascade-pull gate profiles, temporal cascade health.

### Level 3: VPS Depot Fleet Test

6-gate fleet simulation — closest to the real 5-gate enrollment scenario:

```bash
# Create fleet lab
cargo run -- create fleet-test topologies/ecoprimals-vps-depot-deploy.yaml

# Deploy with 8-phase validation
./scripts/deploy-vps-depot.sh --lab fleet-test
```

**Proves**: Multi-gate depot deployment, federation peering, version parity across fleet.

### Level 4: Libvirt OS-Fidelity Mesh (production mirror)

Full systemd, real UDS sockets, `gate.bootstrap`, `membrane` CLI — highest fidelity:

```bash
# Build gate images (agentReagents)
cd infra/agentReagents
cargo run --bin agent-reagents -- build templates/gates/gate-nucleus-full.yaml
cargo run --bin agent-reagents -- build templates/gates/gate-nuc-canary.yaml

# Create libvirt mesh (benchScale)
cd ../benchScale
cargo run --features libvirt -- create mesh-test topologies/irongate-nucleus-mesh.yaml --backend libvirt

# Validate mesh health
./scripts/validate-mesh.sh --topology irongate-nucleus-mesh
```

**Proves**: Real systemd units, UDS-first binding, SongBird 3-way federation,
BearDog crypto spine, `temporal.cascade --dry-run` (zero version skew),
canary resource constraints, `gate.bootstrap` flow.

### Level 5: Physical Gate Validation

After levels 1-4 pass in simulation, run the actual 5-gate enrollment:

```bash
# On each enrolling gate (via RustDesk session):
./gate-enroll.sh --hub primals.eco --gate strandGate --token <token> --compose full
# ... wait for enrollment ...
# Clone repos, build, validate
```

---

## PHASE 4: ENMESHMENT — GATES AS COMPUTE

Once enrolled and validated, each gate serves its role:

| Gate | Mesh IP | Role | Deployments |
|------|---------|------|-------------|
| strandGate | .20-.254 | Heavy bioinformatics compute | primalSpring + wetSpring + neuralSpring, NF pipeline candidate |
| westGate | .20-.254 | Cold storage archive | NestGate CAS backend (76TB ZFS), ecosystem archive |
| blueGate | .20-.254 | General compute | Profile during enrollment, assign based on capacity |
| swiftGate | .20-.254 | General compute | Profile during enrollment, assign based on capacity |
| southGate | .20-.254 | Full NUCLEUS (house2) | Second sovereign site, full 13-primal deployment |

### Ongoing Update Path

Once meshed, gates stay current via golgiBody:

1. `wateringHole/wave.toml` announces new waves
2. `membrane temporal.cascade --check` detects staleness
3. `git fetch origin && git merge --ff-only origin/main` pulls updates
4. Depot binaries refresh via `plasmidBin/fetch.sh pull`
5. New systems coming online on golgiBody are visible to all meshed gates

---

## SUCCESS CRITERIA — TRACK B COMPLETE WHEN:

- [ ] All 5 gates enrolled (mesh IP, WG peer, Forgejo SSH, family seed)
- [ ] All 5 gates converged (43+ repos at Forgejo HEAD)
- [ ] westGate divergence resolved (all repos match Forgejo)
- [ ] benchScale Level 1 (Docker NUCLEUS) PASS
- [ ] benchScale Level 2 (WaterFall cascade) PASS
- [ ] benchScale Level 3 (VPS depot fleet) PASS
- [ ] benchScale Level 4 (libvirt OS-fidelity mesh) PASS
- [ ] At least 1 physical gate validates end-to-end enrollment
- [ ] All bins sourced from golgiBody depot (zero USB)
- [ ] Published heads for all 5 gates in `wateringHole/heads/`

---

*Track B focuses on fleet operations and validation. Track A (evolution)
handles capability evolution towards Nest Atomic and bearDog public flip.*
