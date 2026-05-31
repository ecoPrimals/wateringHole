# WaterFall Pattern — Sovereign Gate Sync

**Pattern class**: firstLast coordination (biomeOS neuralAPI)
**Lineage**: Parallels **RootPulse** — both are distributed coordination patterns.
RootPulse coordinates primals for single-repo version control within a
cytoplasm; WaterFall coordinates membranes for multi-repo ecosystem sync
across envelope layers.

**Status**: Phase 1–4 implemented. Phase 4 inversion LIVE (Wave 63+).
Gates push to Forgejo only; VPS push mirrors propagate to GitHub as external linear ledger.
Phase 5 specified (gate specialization + covalent routing).

## K-Derm Topology

The diderm cell envelope model from `cellMembrane` provides the
architectural framing. Each layer maps to an ecosystem component:

| K-Derm Layer        | Ecosystem Component                        | Role in WaterFall                                |
|---------------------|--------------------------------------------|--------------------------------------------------|
| **Cytoplasm**       | Gate NUCLEUS workspace                     | Local evolution — repos evolve independently     |
| **Plasma membrane** | Gate firewall + SSH keys                   | Covalent boundary — SSH auth to periplasm        |
| **Periplasm**       | Forgejo on VPS — golgiBody (`git.primals.eco`) | WaterFall mediator — distributes pulls, receives pushes |
| **Outer membrane**  | VPS channels (Caddy, sporePrint, TURN)     | Service surface — lab.primals.eco, membrane.primals.eco |
| **Extracellular**   | GitHub                                     | Trailing mirror — outer-world CI and discovery   |

The **peptidoglycan layer** (Caddy TLS surface + static lab) sits between
the outer membrane and periplasm, providing structural rigidity — this is
now live at `lab.primals.eco`.

## Flow

```
                    ┌──────────────────────────────────┐
                    │        Extracellular (GitHub)     │
                    │     trailing push mirror from FJ  │
                    └──────────────┬───────────────────┘
                                   │ post-receive hook
                    ┌──────────────┴───────────────────┐
                    │  Outer Membrane (VPS channels)    │
                    │  lab.primals.eco, sporePrint       │
                    └──────────────┬───────────────────┘
                                   │ webhook
                    ┌──────────────┴───────────────────┐
                    │   Periplasm (Forgejo)             │
                    │   git.primals.eco                 │
                    │   38 repos, waterfall source      │
                    └───┬───────┬───────┬──────────────┘
                        │       │       │
          ┌─────────────┘       │       └──────────────┐
          ▼                     ▼                      ▼
    ┌───────────┐       ┌───────────┐          ┌───────────┐
    │ eastGate  │       │ southGate │          │ biomeGate │
    │ cytoplasm │       │ cytoplasm │          │ cytoplasm │
    └───────────┘       └───────────┘          └───────────┘

    ─── waterfall down: cascade-pull --source forgejo ───▶
    ◀── evolution up:   git push forgejo ────────────────
```

### Waterfall Down (pull)

Gates invoke `cascade-pull.sh --source forgejo` (or `auto`). The script:

1. Reads `ecosystem_manifest.toml` `[sync]` for Forgejo SSH URL
2. For each repo, selects the `forgejo` remote (falls back to `origin` if missing)
3. Executes `git pull --ff-only <remote>` concurrently across repos
4. Updates `freshness.toml` via `--publish-freshness`

### Evolution Up (push)

Individual repos push to Forgejo after local development:

```bash
git push forgejo main
```

Forgejo post-receive hooks then:
- Push to GitHub as a trailing mirror (extracellular)
- Trigger sporePrint webhook refresh (outer membrane)

## Configuration

### ecosystem_manifest.toml

```toml
[sync]
forgejo_base_url = "https://git.primals.eco"
forgejo_ssh = "ssh://git@git.primals.eco:2222"
forgejo_host = "golgiBody"
default_source = "temporal"
default_branch = "main"
push_to_followers = true
push_target = "forgejo"       # Phase 4 inversion: gates push to Forgejo only

[repos.primalSpring]
# ... existing fields ...
forgejo_repo = "syntheticChemistry/primalSpring"
```

**`push_target`**: Controls where temporal sync pushes. `"forgejo"` means gates
push only to the Forgejo remote. The VPS push mirror auto-propagates to GitHub.
Set to `"all"` for legacy dual-push behavior.

### Gate-level override

```bash
# ~/.config/cascade-pull.env (or environment variable)
CASCADE_SYNC_SOURCE=forgejo
```

### cascade-pull.sh flags

| Flag                | Description                                    |
|---------------------|------------------------------------------------|
| `--source github`   | Pull from `origin` (GitHub) — current default  |
| `--source forgejo`  | Pull from `forgejo` remote (periplasm)         |
| `--source auto`     | Try `forgejo`, fall back to `origin`           |
| `--ensure-remotes`  | Add/update `forgejo` remote to all repos       |

## Inversion Protocol (Phase 3–4)

The inversion flips Forgejo from trailing mirror to primary source.

### Phase 3: Shadow Period (dual-source validation)

1. Run `cascade-pull --source forgejo --check` alongside normal pulls
2. Compare HEADs from both remotes for parity
3. Track parity for 7+ days (matching membrane telemetry cutover gate)
4. Extend `s_ecosystem_freshness` or add `s_ecosystem_forgejo_parity`
   to validate in CI

### Phase 4: Inversion — LIVE (Wave 63+)

1. `[sync].push_target = "forgejo"` in manifest — gates push to Forgejo only
2. `[sync].default_source = "temporal"` — pull from whichever remote leads
3. VPS push mirrors created via `membrane mirror.push-create` per repo
4. Forgejo `sync_on_commit = true` — every push auto-mirrors to GitHub
5. GitHub becomes the external linear ledger (analogous to loamSpine → BTC/ETH)
6. Forgejo post-receive webhook fires impulse cascade via `impulse-relay-hook.sh`

**Implementation files**:
- `hooks/forgejo/setup-push-mirrors.sh` — one-time push mirror provisioning
- `hooks/forgejo/impulse-relay-hook.sh` — post-receive impulse cascade
- `graphs/waterfall_publish.toml` — full cascade graph specification

**K-Derm bonding debt**: Push mirror currently fires from golgiBody-inner
directly to GitHub, crossing covalent→weak without intermediate bond degradation.
Target flow when membrane inner/outer separation completes:
inner (covalent) → peptidoglycan (metallic) → golgiBody-ext (ionic) → GitHub (weak).
GitHub SSH keys migrate from inner to outer (trans face) at that point.

### Rollback

If Forgejo becomes unavailable during shadow period or after inversion:
```bash
cascade-pull --source github    # explicit fallback
```

## Phase 5: Multi-Biome / Multi-Membrane — Gate Specialization

Once gates pull from Forgejo and push back to it, WaterFall becomes a
full biomeOS coordination pattern with covalent routing.

### Gate-Spring Ownership

Each gate owns specific science domains and pulls only what it needs.
The canonical SSOT is `GATE_SPRING_OWNERSHIP.md`.

| Gate | Domain | Springs | Sync Profile |
|------|--------|---------|-------------|
| **eastGate** | Coordination hub | primalSpring, airSpring, groundSpring | Full superset (38 repos) |
| **ironGate** | Clinical, game science | healthSpring, ludoSpring | Core + health/ludo + esotericWebb |
| **southGate** | Biology, ML inference | wetSpring, neuralSpring | Core + wet/neural |
| **biomeGate** | GPU compute | hotSpring | Core + hotSpring |
| **strandGate** | ABG science, genomics | hotSpring, wetSpring | Core + ABG gardens + lithoSpore |
| **golgiBody** | Periplasmic relay | — | NUCLEUS primals + deployment infra |

### Gate Auto-Detection

`cascade-pull.sh --gate auto` resolves the current gate identity:

1. `GATE_NAME` environment variable (explicit override)
2. Hostname detection (`hostname -s` mapped to gate name)
3. Falls back to pulling all repos if unresolved

This makes per-gate sync the default operational mode. Gates pull only
their assigned repos, reducing bandwidth and avoiding conflicts in
repos they don't own.

### Cross-Gate Compute Routing

hotSpring operates on both strandGate (ABG science validation) and
biomeGate (GPU-accelerated physics). The science evolves on strandGate;
heavy compute dispatches to biomeGate via Songbird mesh. This is the
first cross-gate covalent bond — work flows between gates through the
periplasm rather than through manual coordination.

### Covalent Evolution Path

```
Ad-hoc routing (Wave 55-59)
    Handoff blurbs coordinate gate work manually.
    ↓
Documented ownership (Wave 60) — THIS PHASE
    GATE_SPRING_OWNERSHIP.md + manifest [gates.*] profiles.
    cascade-pull --gate auto syncs per-gate repos.
    ↓
Songbird mesh discovery (Wave 62+)
    Gates advertise capabilities via Songbird primitives.
    Cross-gate dispatch replaces manual blurbs.
    ↓
toadStool covalent dispatch (Wave 63+)
    Compute jobs route to best-fit gate hardware.
    hotSpring GPU work auto-dispatches to biomeGate.
    ↓
biomeOS graph.execute (Wave 65+)
    WaterFall becomes a TOML-defined neuralAPI pattern.
    Routing via biomeOS engine instead of shell scripts.
    Parallels RootPulse coordination of primals.
```

### Infrastructure Patterns

- **VPS cascade profile**: golgiBody gets its own cascade-pull profile
  (periplasm-local NUCLEUS repos only — no springs)
- **New gate bootstrap**: Clone from Forgejo, install cascade-pull timer,
  done — K-Derm endosymbiosis (Phase 1 weak → Phase 4 covalent)
- **Nested diderm**: A lab's outer membrane is the campus periplasm;
  WaterFall flows through each envelope independently
- **neuralAPI elevation**: WaterFall becomes a TOML-defined neuralAPI
  pattern in biomeOS, routing via the biomeOS engine instead of shell
  scripts — just as RootPulse coordinates rhizoCrypt + loamSpine +
  NestGate + sweetGrass

## Key Files

| File | Role |
|------|------|
| `infra/wateringHole/ecosystem_manifest.toml` | Repo catalog + `[sync]` config |
| `infra/wateringHole/cascade-pull.sh` | WaterFall orchestrator |
| `infra/wateringHole/freshness.toml` | Wave state snapshot |
| `gardens/projectNUCLEUS/deploy/forgejo_mirror.sh` | Forgejo repo provisioning |
| `springs/primalSpring/ecoPrimal/.../s_ecosystem_freshness.rs` | Manifest + sync validation |

## History

- **Wave 63+** (2026-05-31): Phase 4 inversion LIVE. `push_target = "forgejo"`
  in manifest. Push mirror API added to membrane-shadow (`mirror.push-create`,
  `mirror.push-list`, `mirror.push-sync`). Temporal sync respects designated
  push target. Post-receive impulse relay hook and cascade graphs created.
  GitHub becomes external linear ledger; gates push to Forgejo only.
- **Wave 60** (2026-05-28): Phase 1–2 implemented. Manifest v2.0.0 with
  `[sync]` section and `forgejo_repo` fields. `cascade-pull.sh` evolved
  with `--source` and `--ensure-remotes`. All eastGate repos configured
  with `forgejo` remote. Validation extended to check WaterFall fields.
