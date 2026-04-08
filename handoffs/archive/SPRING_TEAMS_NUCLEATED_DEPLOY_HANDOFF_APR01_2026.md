# Spring Teams — Nucleated Deploy Graphs Handoff (April 1, 2026)

**From**: primalSpring coordination (Phase 23g)
**For**: airSpring, groundSpring, healthSpring, hotSpring, neuralSpring, wetSpring
**Reference**: `springs/primalSpring/graphs/spring_deploy/`

---

## What This Is

primalSpring created nucleated deploy graphs for each science spring. These
are proto-compositions: they define the NUCLEUS base plus domain-specific
primals your spring needs. As you validate against these graphs, gaps you
discover flow back upstream to primalSpring and the primal teams.

## The NUCLEUS Base (every spring gets this)

Every nucleated graph starts with the same foundation:

| Node | Primal | Role | Required |
|------|--------|------|----------|
| `biomeos_neural_api` | biomeOS | Orchestration substrate | Yes |
| `beardog_security` | BearDog | Identity, crypto, lineage | Yes |
| `songbird_network` | Songbird | Discovery, mesh, routing | Yes |

These deploy in order: biomeOS first (Phase 0), then BearDog + Songbird
(Phase 1). Your spring primal deploys after the NUCLEUS is healthy.

## Per-Spring Graph Summary

### airSpring (`airspring_deploy.toml`)
- **Domain**: Weather science, ET₀ calculations, atmospheric modeling
- **Extra primals**: barraCuda (GPU math), Squirrel (AI inference)
- **Optional**: Provenance Trio (rhizoCrypt, loamSpine, sweetGrass)
- **Capabilities expected**: `data.weather`, `ecology.experiment`

### groundSpring (`groundspring_deploy.toml`)
- **Domain**: Soil science, geology, Anderson localization
- **Extra primals**: barraCuda (GPU math), toadStool (compute dispatch), NestGate (persistence)
- **Optional**: Provenance Trio
- **Capabilities expected**: `measurement.anderson_validation`, `analysis.run`

### healthSpring (`healthspring_deploy.toml`)
- **Domain**: Biomedical science, clinical models, PK/PD
- **Extra primals**: Squirrel (AI inference), NestGate (patient data persistence)
- **Optional**: Provenance Trio
- **Capabilities expected**: `data.fetch`, `model.inference_route`

### hotSpring (`hotspring_deploy.toml`)
- **Domain**: Physics, lattice QCD, sovereign GPU compute
- **Extra primals**: toadStool (ember compute), coralReef (shader compilation), barraCuda (GPU math), NestGate (result persistence)
- **Optional**: Provenance Trio
- **Capabilities expected**: `physics.lattice_qcd`, `compute.cg_solver`

### neuralSpring (`neuralspring_deploy.toml`)
- **Domain**: Neural networks, ML, evoformer
- **Extra primals**: toadStool (ember compute), coralReef (shader compilation), barraCuda (GPU math), Squirrel (AI), NestGate (model persistence)
- **Optional**: Provenance Trio
- **Capabilities expected**: `science.evoformer_block`, `science.attention_anderson`

### wetSpring (`wetspring_deploy.toml`)
- **Domain**: Biology, ecology, metagenomics, Anderson QS
- **Extra primals**: toadStool (compute dispatch), barraCuda (GPU math), NestGate (sample persistence)
- **Optional**: Provenance Trio
- **Capabilities expected**: `science.anderson`, `community.fastq`

## How to Use Your Graph

### 1. Review your deploy graph
```bash
cat springs/primalSpring/graphs/spring_deploy/<yourspring>_deploy.toml
```

### 2. Validate structurally
Your graph is already structurally validated by primalSpring's graph parser.
All nodes use `by_capability` — no hardcoded primal identities.

### 3. Run your spring against the composition
Start the NUCLEUS primals (via `tools/nucleus_launcher.sh` or biomeOS nucleus),
then start your spring primal. The graph defines what's available.

### 4. Report gaps upstream
When a capability call fails or a primal doesn't behave as expected, file
the gap back to primalSpring. We maintain the gap registry at
`docs/PRIMAL_GAPS.md` and will coordinate with the primal team.

## Patterns to Follow

- **Capability-first**: Your graph nodes should use `by_capability`, not
  primal names. This allows biomeOS to route to the best available provider.
- **Honest scaffolding**: When a primal isn't running, skip the check — never
  fake a pass.
- **Provenance**: If you produce scientific results, wire the Provenance Trio
  (rhizoCrypt for DAG, loamSpine for ledger, sweetGrass for attribution).
- **Health first**: Check `health.liveness` on every primal before calling
  domain methods.

## Reference Documents
- `wateringHole/COMPOSITION_PATTERNS.md` — canonical deploy graph and niche conventions
- `wateringHole/SPOREGARDEN_DEPLOYMENT_STANDARD.md` — BYOB deployment model
- `springs/primalSpring/docs/PRIMAL_GAPS.md` — known primal gaps

---

**primalSpring v0.8.0g**: 403 tests, 67 experiments, 89 deploy graphs, 43/44 (98%) live validation
