<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V49 — Primal & Spring Evolution Handoff

**Date**: 2026-04-10
**From**: healthSpring (spring team)
**To**: All primal teams, all spring teams, biomeOS, primalSpring

---

## Context: Three-Tier Validation

healthSpring now validates at three tiers:

1. **Python → Rust**: 54 Python baselines validate 83 Rust experiments (Tier 0-1)
2. **Rust CPU → GPU**: 6 WGSL shaders validated against CPU fallbacks (Tier 2-3)
3. **Direct Rust → NUCLEUS composition**: 6 composition experiments validate that
   IPC dispatch, proto-nucleate aliases, and wire protocol round-trips reproduce
   identical results to direct Rust calls (Tier 4)

The third tier is new in V48-49. It means: Python was the validation target for
Rust, and now Rust+Python are both validation targets for the ecoPrimal NUCLEUS
composition patterns themselves. The science is validated; now the *composition*
is validated.

---

## For barraCuda Team

### Absorb: `TensorSession` API

healthSpring retains 6 local WGSL shaders (`shaders/health/*.wgsl`) solely because
the `execute_fused_local` path uses single-encoder fusion that cannot mix barraCuda
encoders. Once `TensorSession` provides dependent multi-operation pipeline fusion,
healthSpring can remove all local shaders and consume `barracuda::ops` exclusively.

**Action**: Expose `TensorSession` as a public API. healthSpring will be the first
consumer and validation target.

### Absorb: `uncertainty::std_dev` is already delegated

V49 delegates `uncertainty::std_dev` to `barracuda::stats::correlation::std_dev`.
No further absorption needed for this function.

### Current pin: v0.3.11 (`7f6649f`)

healthSpring CI gates on this rev. When barraCuda releases a new version, update
the pin comment in `ecoPrimal/Cargo.toml` and the CI check in `.github/workflows/ci.yml`.

---

## For toadStool Team

### Composition pattern: `compute.offload` → `compute.dispatch.submit`

healthSpring routes GPU work through `compute.offload` which maps to toadStool's
`compute.dispatch.submit`. The dispatch matrix experiment (exp069) validates all
6 GPU ops through this path.

### Capability vocabulary alignment

healthSpring uses `compute.offload` and `compute.shader_compile`; toadStool
advertises `compute.execute`, `compute.submit`, `compute.gpu.dispatch`. The
semantic overlap should be standardized. Proposed: toadStool accepts both
naming conventions or aliases are agreed at the primalSpring level.

---

## For BearDog Team

### Ionic bond enforcement needed

healthSpring's proto-nucleate declares a dual-tower HIPAA enclave with ionic
bridge between Tower A (patient data) and Tower B (analytics). No primal currently
implements `crypto.ionic_bond` or `crypto.verify_family` for per-family key
management. healthSpring has IPC stubs ready; once BearDog evolves these
capabilities, wiring is straightforward.

**Action**: Evolve `crypto.ionic_bond`, `crypto.verify_family`, per-family key
management. healthSpring will validate as first consumer.

---

## For NestGate Team

### Egress fence needed

The ionic bridge security model requires NestGate to enforce egress fences:
time-series egress policy, family-scoped encryption at rest, de-identified
aggregates only crossing the bridge.

**Action**: Evolve `storage.egress_fence`. healthSpring will validate.

---

## For Songbird Team

### Discovery method name alignment

healthSpring calls `net.discovery.find_by_capability` on Songbird. The proto-nucleate
lists `discovery.find_primals` and `discovery.announce`. These don't match.

**Action**: Standardize on `discovery.*` per semantic naming convention. healthSpring's
`tower_atomic.rs` will update once the canonical names are agreed.

---

## For Squirrel / neuralSpring Team

### Inference capability discovery

healthSpring discovers inference providers by scanning `model.*` then `inference.*`
capability prefixes. The proto-nucleate assigns Squirrel `ai.complete`, `ai.models`,
`inference.*` capabilities.

healthSpring V49 supports both `model.*` and `inference.*` as discovery and routing
namespaces. The canonical namespace should be decided at the primalSpring level.

### Deploy graph inclusion blocked

healthSpring cannot include Squirrel in its deploy graphs until Squirrel reaches
ecoBin compliance and publishes stable `inference.*` capabilities. Once ready,
healthSpring will add an optional Squirrel node.

---

## For biomeOS Team

### Deploy graph format

healthSpring ships two deploy graphs:
- `healthspring_niche_deploy.toml` — `[[graph.node]]` format (primalSpring structural)
- `healthspring_biomeos_deploy.toml` — `[[nodes]]` format (biomeOS NeuralExecutor)

Both now carry NUCLEUS fragment metadata (`fragments`, `particle_profile`,
`proto_nucleate`) and bonding policy (`[graph.bonding]`). biomeOS should parse
these keys for composition health and security enforcement.

### neuralAPI Pathway Learner

healthSpring's `capability.list` response includes `operation_dependencies` and
`cost_estimates` for the Pathway Learner to optimize execution graphs. The
healthSpring primal serves 62 science + 22 infrastructure capabilities.

---

## For All Spring Teams

### Composition validation pattern

healthSpring's Tier 4 composition validation is a reusable pattern for any spring
transitioning from "validated science" to "validated primal composition":

1. **exp112-113**: Dispatch parity — `dispatch_science(method, params)` matches
   direct Rust function calls to machine epsilon
2. **exp114**: Capability surface completeness — every registered method dispatches
3. **exp115**: Proto-nucleate alignment — socket conventions, PRIMAL_NAME/DOMAIN
4. **exp116**: Provenance lifecycle — data session begin/record/complete round-trip
5. **exp117**: Wire protocol round-trip — JSON-RPC serialization fidelity

Any spring can adopt this pattern by replicating the experiment structure and
adapting the method names to their science domain.

### Proto-nucleate alias pattern

healthSpring implements `resolve_proto_alias()` which maps high-level `health.*`
capabilities from the proto-nucleate graph to canonical `science.*` methods.
This allows biomeOS to route by proto-nucleate vocabulary while the spring
maintains its own domain-specific method namespace.

### ecoBin harvest

healthSpring's 2.5 MB static-PIE binary is harvested to `infra/plasmidBin/healthspring/`.
Any spring producing a primal binary should follow the same pattern:
`cargo build --release --target x86_64-unknown-linux-musl` → strip → copy to plasmidBin.

---

## For primalSpring Team

### Proto-nucleate gaps resolved

Gap §1 (capability namespace) is now fixed — healthSpring implements option (a):
`health.*` aliases alongside `science.*`. Confirm this approach or propose option (b)
(revise proto-nucleate to `science.*` vocabulary).

### Remaining gaps

| Gap | Blocked on | Action |
|-----|-----------|--------|
| Ionic bridge | BearDog + NestGate evolution | Wire when capabilities exist |
| Discovery naming | Songbird alignment | Update once canonical names agreed |
| Inference namespace | Squirrel alignment | Both `model.*` and `inference.*` supported |
| Squirrel in deploy | Squirrel ecoBin compliance | Add optional node when ready |

### Deploy graph fragment metadata

Both healthSpring deploy graphs now declare `fragments = ["tower_atomic", "nest_atomic"]`
and a full `[graph.bonding]` section. primalSpring should validate these keys in
graph structural tests.
