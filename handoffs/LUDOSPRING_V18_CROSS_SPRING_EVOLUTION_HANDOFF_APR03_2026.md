# ludoSpring V18 Cross-Spring Evolution Handoff

**Date:** April 3, 2026
**From:** ludoSpring V18 (game science, primal composition)
**To:** All sibling springs (wetSpring, healthSpring, neuralSpring, groundSpring, airSpring, hotSpring)
**Type:** Methodology handoff — patterns for adoption, not code for import

---

## Executive Summary

ludoSpring V15-V18 evolved from science validation to primal composition validation.
This handoff documents patterns, methodology, and per-spring action items that
sibling springs can absorb independently. No shared crates — only shared knowledge.

---

## 1. What ludoSpring Built (Reference, Not Dependency)

### 1.1 Typed Deploy Graph Parsing

`DeployGraph`, `GraphNode`, `topological_waves()` — typed Rust structs that parse
BYOB deploy graph TOML (`[[graph.node]]` schema) without importing primalSpring
or biomeOS. Any spring can independently implement the same parsing from
`wateringHole/BYOB_DEPLOY_GRAPH_SCHEMA.md`.

**Pattern to absorb:** If your spring wants to validate primal compositions,
implement your own `DeployGraph` parser from the BYOB schema spec. Do not import
ludoSpring's implementation.

### 1.2 Composition Recipe

`deploy::recipe::validate_composition()` codifies:

```
Parse graph -> Validate structure -> Topological waves -> Discover by capability
-> Walk waves (health probe) -> Run domain science -> Report
```

Returns a `CompositionReport` with per-node health, capability satisfaction,
and readiness summary. This is the bridge between deploy graphs and domain
science validation.

**Pattern to absorb:** Adapt the recipe to your domain. Replace "game science"
with "field genomics" or "PK/PD modeling" or "spectral analysis". The recipe
structure is domain-agnostic.

### 1.3 ValidationHarness Skip Semantics

ludoSpring experiments use `ValidationHarness` with three exit codes:
- Exit 0: all checks pass
- Exit 1: any check fails
- Exit 2: all non-skipped checks pass (some skipped due to missing primals)

Skip semantics enable composition experiments to run meaningfully even when
some primals are not available. The experiment reports what it can validate
and skips what it cannot.

**Pattern to absorb:** If your spring already uses `ValidationResult`, consider
adding skip semantics for IPC-dependent checks so experiments degrade gracefully.

### 1.4 Session Lifecycle IPC

Four JSON-RPC methods for session-aware composition:
- `game.begin_session` / `game.complete_session`
- `game.session_state` / `game.tick_health`

**Pattern to absorb:** Define your own session lifecycle methods using the
same naming convention (`{domain}.begin_session`, `{domain}.complete_session`).
The lifecycle pattern (initialize → run → finalize with aggregate metrics) is
universal.

### 1.5 Proto Sketch Creation

ludoSpring created 9 proto deploy graph sketches for esotericWebb. Each sketch:
- References the validating experiment
- Marks which gaps it addresses
- Suggests adaptations for the absorbing product

**Pattern to absorb:** When your spring validates a composition that a garden
could use, create a proto sketch in `graphs/sketches/`. This is how springs
feed gardens without code coupling.

---

## 2. Per-Spring Action Items

### 2.1 wetSpring

| Action | Priority | Evidence |
|--------|----------|---------|
| Absorb field sample provenance pattern (exp062) | P1 | 39/39 checks, 6 fraud types, DAG isomorphism with extraction shooter |
| Consider proto sketch for helixVision (field genomics garden) | P2 | Same pattern ludoSpring used for esotericWebb |
| Evaluate deploy graph typing for 16S/metagenomics pipeline validation | P2 | If wetSpring wants to validate multi-primal bio pipelines |

**What ludoSpring proved for wetSpring:** The `SampleCertificate` and `SampleDag`
patterns from exp062 map directly to field genomics architecture. Fraud detectors
become the QC pipeline. The same `GenericFraudDetector` (exp065) that catches
game item duplication catches sample tampering with >80% structural similarity.

### 2.2 healthSpring

| Action | Priority | Evidence |
|--------|----------|---------|
| Absorb consent-gated medical access pattern (exp063) | P1 | 35/35 checks, 5 fraud types, DID-based patient records |
| Adapt cross-domain fraud unification (exp065) | P2 | Same fraud detectors work for medical access violations |
| Consider proto sketch for patient records garden | P2 | ZK access proofs, consent certificates |

**What ludoSpring proved for healthSpring:** Patient-owned medical records via
DID-based loamSpine certificates. Consent certificates as scoped lending.
Every access is a DAG vertex. BearDog selective disclosure proofs.

### 2.3 neuralSpring

| Action | Priority | Evidence |
|--------|----------|---------|
| Evaluate attributed AI narration pattern (exp075) | P1 | Squirrel + sweetGrass braids + rhizoCrypt context |
| Consider Squirrel constraint enforcement for AI models | P2 | NPC personality certs constrain AI output — same pattern for ML model guardrails |

**What ludoSpring proved for neuralSpring:** AI-generated text can carry provable
attribution through sweetGrass braids. The constraint pattern (loamSpine cert
limits what Squirrel can generate) applies to any AI model guardrail scenario.

### 2.4 groundSpring

| Action | Priority | Evidence |
|--------|----------|---------|
| Evaluate live science dashboard pattern (exp076) | P2 | petalTongue + rhizoCrypt metric provenance |
| Consider uncertainty provenance via rhizoCrypt DAGs | P2 | Every uncertainty estimate traceable to a specific computation |

**What ludoSpring proved for groundSpring:** Real-time metrics dashboards where
every data point traces to a specific computation in a specific DAG vertex.
Uncertainty provenance becomes structural, not documentary.

### 2.5 airSpring

| Action | Priority | Evidence |
|--------|----------|---------|
| Evaluate hardware dispatch pattern (exp077) | P2 | toadStool caps + barraCuda compute + local parity |
| Consider deploy graph typing for multi-field GPU pipeline | P2 | airSpring already has deploy graphs with `[graph.metadata]` |

**What ludoSpring proved for airSpring:** Hardware-aware compute dispatch where
the composition queries real silicon capabilities before routing workloads.
airSpring already has deploy graphs — the typed parsing and recipe pattern
would complement existing infrastructure.

### 2.6 hotSpring

| Action | Priority | Evidence |
|--------|----------|---------|
| Evaluate sovereign render pipeline pattern (exp077) | P2 | toadStool + coralReef + barraCuda composition |
| Consider proto sketch for physics simulation gardens | P3 | Same pattern: validate composition, create sketch for consumers |

**What ludoSpring proved for hotSpring:** Hardware-aware GPU pipeline composition
where toadStool discovers capabilities, coralReef compiles shaders, and barraCuda
routes compute — all orchestrated via deploy graph.

---

## 3. Gap Discovery Methodology

### 3.1 How to Surface Gaps

Every composition experiment that encounters a missing capability, a startup
failure, or a protocol mismatch is documenting an evolution gap. ludoSpring's
methodology:

1. Write the deploy graph declaring what you need
2. Write the experiment composing those capabilities
3. Run the experiment — passes become validated patterns, failures become gaps
4. Document gaps in a spec (who owns it, priority, evidence, resolution)
5. Create handoffs for the owning teams

### 3.2 The Ecosystem Evolution Map

`ludoSpring/specs/ECOSYSTEM_EVOLUTION_MAP.md` is the authoritative gap analysis.
Each gap has an owner, priority, evidence experiment, and resolution path.
Sibling springs should create similar maps if they discover composition gaps.

---

## 4. What NOT to Do

- **Do NOT import ludoSpring crates** — implement patterns independently
- **Do NOT copy ludoSpring code** — re-derive from wateringHole standards
- **Do NOT wait for ludoSpring** — evolve on your own timeline
- **Do NOT submit PRs to ludoSpring** — hand off via wateringHole if you
  discover something ludoSpring should know

---

## 5. Cross-References

| Resource | Location |
|----------|----------|
| BYOB deploy graph schema | `wateringHole/BYOB_DEPLOY_GRAPH_SCHEMA.md` |
| Ecosystem evolution map | `ludoSpring/specs/ECOSYSTEM_EVOLUTION_MAP.md` |
| Primal leverage map | `ludoSpring/specs/PRIMAL_LEVERAGE_MAP.md` |
| Upstream primal handoff | `wateringHole/handoffs/LUDOSPRING_V18_UPSTREAM_EVOLUTION_HANDOFF_APR03_2026.md` |
| Downstream garden handoff | `wateringHole/handoffs/LUDOSPRING_V18_DOWNSTREAM_EVOLUTION_HANDOFF_APR03_2026.md` |
| Proto sketches for Webb | `ludoSpring/graphs/sketches/` |
| gen3 Paper 26 (methodology) | `infra/whitePaper/gen3/baseCamp/26_primal_composition_as_scientific_methodology.md` |
| gen4 deploy graph paper | `infra/whitePaper/gen4/architecture/DEPLOY_GRAPH_COMPOSITION.md` |

---

## License

AGPL-3.0-or-later
