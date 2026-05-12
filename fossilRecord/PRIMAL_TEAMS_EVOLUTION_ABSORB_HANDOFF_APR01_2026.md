# Primal Teams — Evolution & Absorption Handoff (April 1, 2026)

**From**: primalSpring coordination (Phase 23g — Primal Rewiring + Gap Cleanup)
**For**: biomeOS, BearDog, Songbird, NestGate, petalTongue, Squirrel, toadStool, sweetGrass, loamSpine, rhizoCrypt
**Reference**: `springs/primalSpring/docs/PRIMAL_GAPS.md`

---

## Context

primalSpring completed a full primal audit cycle, reviewing all 10 primals
and rewiring its internals to match your latest APIs. This handoff documents
what we learned, what we absorbed, and what remains for each primal team.

## Per-Primal Status

### biomeOS

**What we absorbed**: v2.81 `topology.rescan` method, `graph.execute` as the
canonical graph deployment target (was `graph.deploy`), `capability.discover`
socket resolution, Phase 0 substrate health in all deploy graphs.

**What works**: Neural API routing, capability domains, graph listing, health
probing — all validated through 7 composition subsystems.

**Open items**:
- `capability.call` does not implement gate-aware routing (`gate` param ignored)
- `api`/`nucleus` modes still force Unix sockets — no TCP fallback for mobile
- Consider exposing `topology.rescan` result format documentation

### BearDog

**What we absorbed**: v0.9.0+ crypto delegation model. NestGate and Songbird
now delegate cryptographic operations to BearDog via IPC rather than carrying
their own crypto dependencies.

**What works**: Ed25519, Blake3, BirdSong beacon, secrets, genetic identity —
all routed through biomeOS capability.call or direct socket.

**Open items**:
- Still no `--listen <addr>` TCP-only mode for mobile deployment
- Gate-aware federation routing needed for multi-gate crypto ops

### Songbird

**What we absorbed**: Wave 91 concurrent test harness, ring removal, BearDog
crypto delegation, Dark Forest / birdsong env vars in BirdSongConfig.

**What works**: Health, mesh.init, mesh.announce, TCP server mode.

**Remaining gaps**:
- **SB-02** (Low): `mesh.peers` — would help composition monitoring
- **SB-03** (Low): `mesh.topology` — useful for network visualization

### NestGate

**What we absorbed**: ring/aws-lc-rs elimination (NG-04 resolved), nestgate-security
zero crypto deps via BearDog delegation (NG-05 resolved), `family_id` parameter
requirement on `storage.list`.

**What works**: `storage.store`, `storage.retrieve`, `storage.list` (with `family_id`),
health probing. C5 (Persistence) now 5/5 PASS.

**Remaining gaps**:
- **NG-01** (Medium): `storage.list` returns empty without clear filter semantics — the
  only medium-severity gap remaining across all primals
- **NG-02** (Low): No `storage.query` for structured/filtered queries
- **NG-03** (Low): No pagination on list operations

### petalTongue

**What we absorbed**: `RenderingAwareness` auto-init in `UnixSocketServer` (PT-05
resolved), periodic discovery refresh in server mode (PT-07 resolved), zero-copy
IPC, blake3 integration.

**What works**: `visualization.render.dashboard`, `interaction.subscribe`,
`interaction.poll`, `interaction.apply`. C1 (Render) and C6 (Proprioception) both PASS.

**Remaining gaps**:
- **PT-04** (Low): `visualization.render.scene` not yet implemented
- **PT-06** (Low): No `visualization.export` endpoint

### Squirrel

**What we absorbed**: alpha.27 `LOCAL_AI_ENDPOINT` wired into AiRouter (SQ-02
resolved). `ai.query` and `ai.list_providers` now work when a local model
backend (Ollama) is running.

**What works**: Health probing, `ai.list_providers`, `ai.query` (when Ollama is
available). C2 (Narration) 3/4 PASS — the single failure is environmental (no
Ollama), not a code gap.

**Remaining gaps**:
- **SQ-03** (Low): No `ai.list_models` for model inventory — nice for tooling

### toadStool

**What we absorbed**: S171 `ember.*` methods for hardware lifecycle management,
`shader.compile` domain reclaimed by coralReef since S169, zero-copy ember
watchdog patterns.

**What works**: `compute.dispatch.grid_shader`, `ember.list`, `ember.status`,
health probing. Used in Tower and Node compositions.

**Remaining gaps**: None tracked — toadStool is clean.

### sweetGrass / loamSpine / rhizoCrypt (Provenance Trio)

**What we absorbed**: sweetGrass v0.7.27 (attribution), loamSpine (ledger),
rhizoCrypt (DAG). All three are wired into primalSpring's `ipc::provenance`
module and included in the Provenance Trio overlay in all nucleated deploy graphs.

**What works**: Structural validation, launch profiles, deploy graph nodes.
`provenance.commit`, `provenance.verify`, `provenance.attribute` wired.

**Remaining gaps**: Live multi-node provenance E2E (awaiting all three running
concurrently in a composition).

## What primalSpring Contributes Back

1. **Nucleated deploy graphs** — 6 science spring proto-compositions in `graphs/spring_deploy/`
2. **Composition patterns** — `wateringHole/COMPOSITION_PATTERNS.md`
3. **Gap registry** — `docs/PRIMAL_GAPS.md` (primal-scoped, severity-rated)
4. **Validation tooling** — `tools/validate_compositions.py` (C1-C7 live validation)
5. **Method constants** — `ecoPrimal/src/ipc/methods.rs` as canonical method catalog
6. **Discovery patterns** — 6-tier socket discovery in `ecoPrimal/src/ipc/discover.rs`

## Evolution Recommendations

### For All Primals
- Ensure `health.liveness` returns within 50ms — primalSpring's composition
  validator uses this as the first probe for every primal
- Document your socket binding pattern (family-suffixed vs plain name) so
  discovery logic can be tuned
- Expose `capabilities.list` if you don't already — biomeOS routes based on it

### Architecture Hierarchy Reminder
```
primals (upstream)
  └─→ primalSpring (coordination)
        └─→ springs (downstream tributaries)
              └─→ gardens (product layer)
```

Primals own their APIs. primalSpring validates compositions. Springs consume
patterns. As springs validate, they expose gaps that flow back upstream.

---

**primalSpring v0.8.0g**: 403 tests, 67 experiments, 89 deploy graphs, 43/44 (98%) live validation
