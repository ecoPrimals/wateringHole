<!--
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# wetSpring V143 — Deploy Graph Canonical Migration + Composition Validation Tier

| Field | Value |
|-------|-------|
| **Spring** | wetSpring |
| **Version** | V143 |
| **Date** | 2026-04-11 |
| **barraCuda** | 0.3.11 |
| **Wire Standard** | L2 + L3 compliant |
| **Proto-nucleate** | 141/141 (Exp400 D01–D07) |
| **Status** | All quality gates green |

---

## Summary

wetSpring V143 migrates all 7 deploy graphs from legacy `[[graph.node]]` to
primalSpring canonical `[[graph.nodes]]` schema (NA-016), adds bonding policy
and fragments metadata, aligns capability strings to proto-nucleate canonical
form, and extends composition validation with 44 new programmatic checks.

This completes the third validation tier:
1. **Python validates Rust** — 58 scripts → 1,950 tests, 5,800+ checks
2. **Rust validates NUCLEUS composition** — 141/141 proto-nucleate, 21 domains
3. **Composition self-validates** — deploy graphs cross-checked against
   proto-nucleate via D07 metadata compliance (schema, fragments, bonding,
   ownership, canonical capability strings)

---

## What Changed (for primal/spring teams)

### 1. Deploy Graph Schema Migration: `[[graph.node]]` → `[[graph.nodes]]`

All 7 wetSpring deploy graphs now use the canonical plural schema. This
aligns with primalSpring NA-016 and all proto-nucleate graphs.

**Action for springs:** Migrate your deploy graphs to `[[graph.nodes]]`.
primalSpring's parser accepts both via `[workspace.package]` but canonical
is plural. biomeOS should parse `[[graph.nodes]]` as primary.

### 2. Deploy Graph Metadata Enrichment

Every graph now carries full `[graph.metadata]`:

```toml
[graph.metadata]
pattern_version = "2026-04-11"
schema = "canonical"
witness_wire = "WireWitnessRef"
encoding_standard = "wateringHole/ATTESTATION_ENCODING_STANDARD.md"
composition_model = "nucleated"
science_domain = "life_science_chemistry"
owner = "wetSpring"
fragments = ["tower_atomic", "node_atomic", "nest_atomic", "meta_tier"]
```

**Action for springs:** Add `composition_model`, `owner`, `fragments` to
your deploy graph metadata. biomeOS can use this for composition analysis.

### 3. Bonding Policy Declaration

Full-NUCLEUS graphs (`wetspring_deploy.toml`, `wetspring_science_nucleus.toml`)
now declare `[graph.bonding_policy]`:

```toml
[graph.bonding_policy]
bond_type = "Metallic"
trust_model = "InternalNucleus"
tower_internal = "covalent"
tower_to_node = "metallic"
tower_to_nest = "metallic"
encryption_tiers.tower = "full"
encryption_tiers.node = "delegated"
encryption_tiers.nest = "delegated"
encryption_tiers.meta = "delegated"
```

**Action for springs with full-NUCLEUS graphs:** Declare bonding policy.
Per `NUCLEUS_SPRING_ALIGNMENT.md`, cross-atomic compositions must declare
bond type, trust model, and encryption tiers per atomic boundary.

### 4. Capability String Alignment

Deploy graph capability strings now match proto-nucleate canonical form:

| Old (deploy) | New (proto-nucleate canonical) |
|-------------|-------------------------------|
| `storage.put`, `storage.get` | `storage.store`, `storage.retrieve` |
| `provenance.session`, `provenance.vertex` | `dag.session.create`, `dag.event.append` |
| `attribution.braid`, `attribution.calculate` | `braid.create`, `braid.commit` |
| `compute.dispatch`, `compute.performance_surface` | `compute.dispatch.submit`, `compute.execute` |
| `visualization.render`, `visualization.render.dashboard` | `render.dashboard`, `tui.push` |

**Action for biomeOS/primals:** If you parse deploy graph capability strings,
use the canonical form. The proto-nucleate is the source of truth.

### 5. Node Atomic Completeness

Full-NUCLEUS graphs now include `coralreef` and `barracuda` as graph nodes
(previously only `toadstool` represented Node Atomic compute). This matches
the proto-nucleate's vision of all three compute primals as discrete nodes.

### 6. Composition Validation D07

Exp400 now has 7 domains (was 6), 141 checks (was 97):

| Domain | Checks | New in V143 |
|--------|--------|-------------|
| D01: Niche self-knowledge | 17 | — |
| D02: Capability surface | 25 | — |
| D03: Proto-nucleate coverage | 20 | — |
| D04: Deploy graph structure | 21 | — |
| D05: Composition model | 8 | — |
| D06: Bonding & atomic alignment | 6 | — |
| **D07: Deploy graph metadata** | **44** | **NEW** |

D07 checks per graph: `composition_model`, `owner`, `fragments`,
`[[graph.nodes]]` canonical schema. Full-NUCLEUS graphs additionally:
`bonding_policy`, `witness_wire`, all 4 fragment declarations
(`tower_atomic`, `node_atomic`, `nest_atomic`, `meta_tier`), `coralreef`
node, `barracuda` node.

---

## Binary Naming Note for primalSpring

The proto-nucleate (`wetspring_lifescience_proto_nucleate.toml`) declares
`binary = "wetspring_primal"`. The actual binary in `Cargo.toml` is
`wetspring` (pointing to `wetspring_server.rs`). All deploy graphs now use
`binary = "wetspring"`. Recommend aligning the proto-nucleate to `wetspring`.

---

## Quality Gates

| Check | Status |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -D warnings` | 0 warnings |
| `cargo test --workspace` | 1,950 passed, 0 failed |
| Wire Standard | L2 + L3 |
| Proto-nucleate | 141/141 (Exp400 D01–D07) |
| `forbid(unsafe_code)` | Enforced |
| `#[allow()]` | 0 in production |
| Deploy graph schema | `[[graph.nodes]]` canonical |
| Deploy graph metadata | All 7 graphs complete |
| Bonding policy | Declared on full-NUCLEUS graphs |

---

## Open Primal Gaps (unchanged from V142)

| # | Gap | Blocked By |
|---|-----|------------|
| PG-02 | Provenance trio endpoints | Trio IPC readiness |
| PG-03 | Name-based discovery | Songbird `capability.resolve` |
| PG-04 | NestGate storage | NestGate IPC readiness |
| PG-05 | toadStool compute IPC | NUCLEUS deployment |
| PG-06 | Ionic bond protocol | primalSpring Track 4 |

---

*This handoff is maintained by wetSpring and archived in
`infra/wateringHole/handoffs/`. Previous: V142 (Wire Standard), V139
(composition validation), V138 (primal composition patterns).*
