<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# biomeOS v2.30 — Provenance Trio Wiring Handoff

**Date**: March 12, 2026
**Primal**: biomeOS
**Version**: v2.30
**Type**: Coordination layer wiring for provenance trio

---

## Summary

Wired the provenance trio (rhizoCrypt + LoamSpine + sweetGrass) into biomeOS's
Neural API coordination layer. Added 3 capability domains, 2 deploy graphs,
and 2 niche templates. All existing tests pass. The trio can now be orchestrated
through `niche.deploy rootpulse` and `niche.deploy provenance-pipeline`.

---

## Changes

### 1. Capability Domains (`capability_domains.rs`)

Added 3 new domains to the fallback resolution table:

| Domain | Provider | Capabilities |
|--------|----------|-------------|
| Ephemeral workspace | `rhizocrypt` | `ephemeral_workspace`, `dag`, `session`, `merkle`, `dehydration`, `slice`, `vertex` |
| Permanent history | `loamspine` | `permanent_storage`, `linear_history`, `spine`, `certificate`, `temporal_anchor`, `commit` |
| Attribution | `sweetgrass` | `attribution`, `braid`, `provenance`, `contribution`, `privacy`, `prov_export` |

Prefix matching works: `dag.create_session` → `rhizocrypt`,
`commit.session` → `loamspine`, `provenance.create_braid` → `sweetgrass`.

### 2. RootPulse Commit Graph (`graphs/rootpulse_commit.toml`)

6-phase sequential graph implementing the RootPulse commit workflow from
`niches/rootpulse/rootpulse-niche.yaml`:

1. **Health checks** — rhizoCrypt + LoamSpine availability
2. **Dehydrate** — `dag.dehydrate` on rhizoCrypt (Merkle root, frontier)
3. **Sign** — `crypto.sign` via BearDog
4. **Store content** — `storage.store` on NestGate
5. **Commit** — `commit.session` on LoamSpine (permanent history)
6. **Attribute** — `provenance.create_braid` on sweetGrass (optional)

### 3. Provenance Pipeline Graph (`graphs/provenance_pipeline.toml`)

Reusable 5-phase graph for any Spring to persist experiment results with
provenance. Parameters: `SESSION_ID`, `EXPERIMENT_ID`, `AGENT_DID`.

Any Spring (wetSpring, airSpring, ludoSpring, etc.) can invoke this pipeline
to get permanent provenance for its experiment results without implementing
its own dehydration flow.

### 4. Niche Templates (`handlers/niche.rs`)

Added 2 templates to `NicheHandler`:

| Template ID | Graph | Category |
|------------|-------|----------|
| `rootpulse` | `rootpulse_commit` | provenance |
| `provenance-pipeline` | `provenance_pipeline` | provenance |

Both templates appear in `niche.list` and can be deployed via `niche.deploy`.

---

## Tests

- `test_capability_to_provider_provenance_trio` — 18 assertions (all pass)
- `test_niche_list_all_templates` — updated to include `rootpulse` and `provenance-pipeline`
- All 10 niche tests pass
- Pre-existing failure `test_primal_start_capability_binary_not_found` is unrelated

---

## What This Enables

### For Springs
Any Spring can now call `niche.deploy provenance-pipeline` with a `SESSION_ID`
and `EXPERIMENT_ID` to get permanent provenance without implementing custom
dehydration logic.

### For RootPulse
The `rootpulse` niche template can now be deployed through biomeOS. The commit
workflow orchestrates the full provenance trio through the Neural API.

### For the Ecosystem
The capability domains allow the Neural API to route `dag.*`, `commit.*`,
`provenance.*` requests to the correct providers. All three primals are now
discoverable through biomeOS's capability resolution.

---

## Remaining Gaps

1. **RootPulse branch/merge/federate graphs** — Only the commit workflow is
   implemented. Branch, merge, and federate workflows from the niche manifest
   need their own graphs.

2. **End-to-end integration test** — The graphs are defined but not tested
   against live primals. Requires Tower + rhizoCrypt + LoamSpine running.

3. **RootPulse CLI wrapper** — The niche manifest describes a `rootpulse` CLI
   that wraps these workflows. Not yet generated.

4. **ContinuousExecutor integration** — For ludoSpring's game engine niche,
   periodic dehydration could be added as a feedback edge in
   `game_engine_tick.toml`.

5. **config/capability_registry.toml** — The TOML config file should be updated
   to match the new domains for production deployments.
