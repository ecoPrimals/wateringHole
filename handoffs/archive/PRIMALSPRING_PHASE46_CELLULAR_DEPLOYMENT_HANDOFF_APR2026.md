# primalSpring Phase 46 — Cellular Deployment Handoff

## From: primalSpring Phase 46
## For: All spring teams and garden teams
## Date: April 2026

---

## What Happened

primalSpring now produces **deployable cells** for every spring and garden.
A cell is a biomeOS deploy graph: NUCLEUS base + petalTongue `live` mode +
your domain overlay. One command deploys your entire validated composition
as an interactive desktop-like application.

**Key deliverables:**

- 8 cell graphs in `graphs/cells/` (one per spring + esotericWebb)
- `cell_launcher.sh` — unified launcher (`./tools/cell_launcher.sh <spring> start`)
- guidestone **Layer 7** — certifies every cell is deployable
- exp098 — validates all cells structurally + biomeOS dry-run
- petalTongue `live` mode — IPC server + native egui window in one process
- `game.push_scene` drain — ludoSpring scenes route to petalTongue in real time

---

## What This Means for Spring Teams

### Your cell graph is ready

```bash
# Deploy your spring as a live interactive cell
./tools/cell_launcher.sh <yourspring> start

# Or via biomeOS directly
biomeos deploy --graph graphs/cells/<yourspring>_cell.toml
```

This gives you: full NUCLEUS + your domain primal + petalTongue native GUI.
You can push data to `visualization.render.scene` and see it rendered in
real time. User interaction comes back via `interaction.poll`.

### What you need to validate

Your guidestone should now test Layer 7 in addition to Layers 0-6. The
base `primalspring_guidestone` already validates cell structure; your
domain guidestone should validate that your science works through the
live composition pipeline.

### Pattern: science -> scene -> GUI -> feedback

```
Your domain logic ──► visualization.render.scene ──► petalTongue egui window
       ▲                                                       │
       └◄────── interaction.poll ◄────── user input ◄──────────┘
```

This is the same pattern for every domain. Replace `game.*` with your
domain IPC methods.

---

## What This Means for Garden Teams

### Consume cells, don't hand-write graphs

Your deploy graph can now reference a validated cell instead of declaring
every primal node manually. The `esotericwebb_cell.toml` is the reference
garden cell — it composes ludoSpring (game science) + petalTongue live +
the full NUCLEUS.

### Interactive products from validated science

The cell model means your garden product is backed by the same composition
that the spring validated. Science -> product is now a single graph
deployment, not a manual wiring exercise.

---

## Cell Inventory

| Cell | Domain | Graph |
|------|--------|-------|
| hotSpring | QCD physics | `graphs/cells/hotspring_cell.toml` |
| wetSpring | Life science | `graphs/cells/wetspring_cell.toml` |
| neuralSpring | ML inference | `graphs/cells/neuralspring_cell.toml` |
| ludoSpring | Game science | `graphs/cells/ludospring_cell.toml` |
| airSpring | Weather/ecology | `graphs/cells/airspring_cell.toml` |
| groundSpring | Geoscience | `graphs/cells/groundspring_cell.toml` |
| healthSpring | Clinical | `graphs/cells/healthspring_cell.toml` |
| esotericWebb | CRPG (garden) | `graphs/cells/esotericwebb_cell.toml` |

---

## Key References

| Document | Location |
|----------|----------|
| Cell graphs | `springs/primalSpring/graphs/cells/` |
| Cell manifest | `springs/primalSpring/graphs/cells/cells_manifest.toml` |
| Cell launcher | `springs/primalSpring/tools/cell_launcher.sh` |
| exp098 (validation) | `springs/primalSpring/experiments/exp098_cellular_deployment/` |
| guidestone Layer 7 | `springs/primalSpring/ecoPrimal/src/bin/primalspring_guidestone/main.rs` |
| Live GUI pattern | `infra/wateringHole/LIVE_GUI_COMPOSITION_PATTERN.md` |
| Composition guidance | `springs/primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` |
| petalTongue live mode | `primals/petalTongue/src/live_mode.rs` |

---

## YOUR NEXT STEP

1. Pull primalSpring and `infra/wateringHole`
2. Run `./tools/cell_launcher.sh <yourspring> start`
3. Push domain data to `visualization.render.scene`
4. Validate your science works through the live pipeline
5. Update your guidestone to include Layer 7 checks
