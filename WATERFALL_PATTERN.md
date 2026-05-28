# WaterFall Pattern — Sovereign Gate Sync

**Pattern class**: firstLast coordination (biomeOS neuralAPI)
**Lineage**: Parallels **RootPulse** — both are distributed coordination patterns.
RootPulse coordinates primals for single-repo version control within a
cytoplasm; WaterFall coordinates membranes for multi-repo ecosystem sync
across envelope layers.

**Status**: Phase 1–2 implemented (manifest + script evolved, remotes configured).
Phases 3–5 are operational and require multi-day validation windows.

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
forgejo_host = "ironGate"
default_source = "github"   # flip to "forgejo" at inversion (Phase 4)
default_branch = "main"

[repos.primalSpring]
# ... existing fields ...
forgejo_repo = "syntheticChemistry/primalSpring"
```

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

### Phase 4: Inversion

1. Flip `[sync].default_source = "forgejo"` in manifest
2. `cascade-pull` now pulls from Forgejo by default
3. Optionally rename remotes:
   ```bash
   git remote rename origin github
   git remote rename forgejo origin
   ```
4. Invert server-side mirror direction:
   - Forgejo post-receive hooks push to GitHub
   - `forgejo_sync.sh` becomes `github_push_mirror.sh`
5. GitHub becomes a trailing read-only mirror (extracellular)

### Rollback

If Forgejo becomes unavailable during shadow period or after inversion:
```bash
cascade-pull --source github    # explicit fallback
```

## Phase 5: Multi-Biome / Multi-Membrane

Once gates pull from Forgejo and push back to it, WaterFall becomes a
full biomeOS coordination pattern:

- **Gate specialization**: Different biomes pull different repo subsets
  via `--gate` profiles in the manifest (ironGate = dev, southGate =
  production, biomeGate = experimental)
- **VPS cascade profile**: cellMembrane gets its own cascade-pull profile
  (periplasm-local repos only)
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

- **Wave 60** (2026-05-28): Phase 1–2 implemented. Manifest v2.0.0 with
  `[sync]` section and `forgejo_repo` fields. `cascade-pull.sh` evolved
  with `--source` and `--ensure-remotes`. All eastGate repos configured
  with `forgejo` remote. Validation extended to check WaterFall fields.
