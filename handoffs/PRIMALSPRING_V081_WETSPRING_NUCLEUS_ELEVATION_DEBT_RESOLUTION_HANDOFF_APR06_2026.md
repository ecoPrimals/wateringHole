<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# primalSpring v0.8.1 — wetSpring NUCLEUS Elevation + Debt Resolution

**Date:** April 6, 2026
**From:** primalSpring → wetSpring, biomeOS, wateringHole, plasmidBin
**Previous:** `WETSPRING_PRIMALSPRING_ABSORPTION_V2_HANDOFF_APR06_2026.md`
**Previous:** `BIOMEOS_V290_NEURAL_API_SEMANTIC_ROUTING_PROVENANCE_TRIO_HANDOFF_APR06_2026.md`

---

## Context

wetSpring deployed the first full NUCLEUS science pipeline
(`wetspring_science_nucleus.toml`) and identified 6 ecosystem debt items
blocking live end-to-end operation. biomeOS v2.90 resolved the Neural API
routing gap (DEBT-03). This handoff resolves the primalSpring-owned items
and documents what is handed up to primal teams.

primalSpring is **upstream** of springs (defines proto graphs and
coordination patterns) and **downstream** of primals (validates their
compositions work via plasmidBin deployments). Springs expose evolution
gaps; primalSpring refines and solves them or hands up to primal teams.

---

## What Was Resolved

### DEBT-02: Canonical Capability Registry (HIGH — RESOLVED)

**Problem:** `niche::CAPABILITIES` was a flat list of 47 methods with no
distinction between what primalSpring locally serves and what it knows about
but routes to other primals. This caused over-advertisement — biomeOS could
route calls to primalSpring that it can't actually handle.

**Solution:** Split into three layers:

- **`LOCAL_CAPABILITIES`** (30 methods): Methods this binary actually handles
  in `dispatch_request`. Callers get a real response. Registered with biomeOS
  as `served_locally: true`.

- **`ROUTED_CAPABILITIES`** (24 methods with provider annotations): Methods
  primalSpring coordinates but routes to other primals via Neural API semantic
  routing. Each entry names the canonical provider (`songbird`, `biomeos`,
  `squirrel`, `petaltongue`). Registered as `served_locally: false` with
  `canonical_provider` hint.

- **`all_capabilities()`**: Backward-compatible combined accessor.

**`capabilities.list` response** now returns structured output:

```json
{
  "local_capabilities": ["coordination.validate_composition", ...],
  "routed_capabilities": [{"method": "ai.query", "provider": "squirrel"}, ...],
  "capabilities": [...combined flat list...],
  "semantic_mappings": {...},
  "operation_dependencies": {...},
  "cost_estimates": {...}
}
```

**`identity.get`** now reports only `LOCAL_CAPABILITIES` — honest about what
this process serves.

**`capability_registry.toml`** updated with 4 new entries (`graph.waves`,
`graph.capabilities`, `bonding.propose`, `bonding.status`) and all provider
annotations consistent with `ROUTED_CAPABILITIES`.

**Tests:** 3 new tests (`local_and_routed_are_disjoint`,
`routed_capabilities_have_providers`, `routed_capabilities_are_not_empty`)
plus updated existing tests. All 438 pass, 0 fail.

**For wetSpring:** Your deploy graph can now validate capability names against
this registry. The `graph_validate` module's capability domain checks can
consume the `provider` field to verify routing paths.

### DEBT-03: Neural API Method Routing (HIGH — RESOLVED by biomeOS v2.90)

biomeOS v2.90 implements universal semantic routing fallback. Any
`domain.operation` method auto-routes through `capability.call`. 32 new
provenance trio translations. 9 composition health aliases. Springs need
no code changes.

**Verified:** primalSpring's `NeuralBridge::capability_call()` path is
compatible. Direct `domain.operation` calls also work via semantic fallback.

### DEBT-06: Ionic Contract Negotiation Protocol (LOW — PARTIALLY RESOLVED)

**Problem:** Rich type system existed (`IonicProposal`, `ContractState` FSM,
`IonicContract`, `ProvenanceSeal`) but no RPC handlers were wired.

**Solution:** Added two new methods to `dispatch_request`:

- **`bonding.propose`**: Deserializes and validates an `IonicProposal`,
  returns structured validation result. Rejects invalid trust models,
  empty capabilities, empty identity.

- **`bonding.status`**: Queries contract status by ID. Currently returns
  `not_found` (contract store not yet implemented).

**What remains (handed up to BearDog):** Runtime contract store needs
BearDog crypto signatures for the propose→accept handshake. The types
and validation are ready; the crypto binding is the blocker.

### Bug Fix: `probe_capability` Tier 2 Discovery

**Problem:** When capability-based discovery found a socket via
capability-named socket tier (e.g. `security.sock`) but `resolved_primal`
was `None`, the handler called `probe_primal("unknown")` which re-runs
discovery for a primal named "unknown" — always fails.

**Solution:** Added `coordination::probe_primal_at_socket()` that probes
a known socket directly without the discovery step. `handle_probe_capability`
now branches: if both socket and primal name are known, uses `probe_primal`;
if only socket is known, uses `probe_primal_at_socket`.

### Code Quality

- `cargo fmt` — all formatting drift fixed
- `cargo clippy` — zero warnings (pedantic + nursery)
- `cargo doc` — zero warnings
- `cargo deny check` — all clean
- All files under 1000 LOC
- Zero unsafe, zero `#[allow()]` in production code

---

## What Was Already Ready (No Changes Needed)

### DEBT-01: Bonding Policy Rust Types (MEDIUM)

**Status:** Types exist and are production-quality in `bonding/mod.rs`:
`BondType` (5 variants), `TrustModel` (4 variants), `BondingConstraint`
(glob-based capability allow/deny, bandwidth, concurrency), `BondingPolicy`
with validation, JSON round-trip, and factory methods. All `Serialize +
Deserialize`.

**Action for wateringHole:** Extract to a shared crate (`biomeos-types` or
`ecoPrimals-contracts`) so wetSpring's `bonding_metadata.json` validates
against these types. primalSpring's types are the reference implementation.

### DEBT-04: Structured Experiment Harness (LOW)

**Status:** `ValidationResult` with `run()`, `check_bool()`, `check_skip()`,
`check_relative()`, `check_abs_or_rel()`, `check_or_skip()`,
`with_provenance()`, pluggable sinks (stdout, NDJSON, null), `section()`,
exit codes (0/1/2) is the de facto ecosystem standard.

**Decision:** Current pattern works. Adding an `Experiment` trait with
`run()` / `verify()` / `report()` is additive — will implement when
wetSpring concretely needs it for registry integration.

---

## What Is Handed Up

### To plasmidBin: DEBT-05 Binary Name Verification (MEDIUM)

primalSpring uses short binary names (`beardog`, `songbird`, `nestgate`,
`toadstool`, etc.) per `primal_names.rs`. wetSpring's deploy graph now
matches. But nobody has verified these match `plasmidBin/primals/` output.

**Request:** plasmidBin team publishes a manifest of canonical binary names.
primalSpring will add a verification experiment.

### To BearDog: Ionic Crypto Handshake

The ionic negotiation protocol is typed and validated
(`bonding.propose` works). The runtime contract store needs BearDog crypto
signatures for the propose→accept→seal handshake.

**Request:** BearDog team exposes `crypto.sign_contract` and
`crypto.verify_contract` via JSON-RPC. primalSpring will wire the
full negotiation flow once available.

### To wateringHole: Shared Type Crate

`BondType`, `TrustModel`, `BondingConstraint`, `BondingPolicy`,
`IonicProposal`, `ContractState`, `IonicContract`, `ProvenanceSeal` —
all ready for extraction into an ecosystem-shared crate. Decision on
crate naming and packaging is a wateringHole governance choice.

---

## Quality Gates

```bash
cargo test --workspace          # 438 passed, 0 failed, 42 ignored
cargo clippy --workspace --all-targets  # 0 warnings
cargo fmt --check               # 0 diffs
cargo doc --workspace --no-deps # 0 warnings
cargo deny check                # all clean
```

## Files Changed

| File | Change |
|------|--------|
| `ecoPrimal/src/niche.rs` | Split CAPABILITIES → LOCAL_CAPABILITIES + ROUTED_CAPABILITIES + all_capabilities(); updated registration logic; 7 new/updated tests |
| `ecoPrimal/src/coordination/mod.rs` | Added `probe_primal_at_socket()` for Tier 2 capability discovery |
| `ecoPrimal/src/bin/primalspring_primal/main.rs` | Honest capabilities.list/identity.get; fixed probe_capability; added bonding.propose/bonding.status handlers |
| `config/capability_registry.toml` | Added graph.waves, graph.capabilities, bonding.propose, bonding.status entries |
| `ecoPrimal/src/bonding/ionic.rs` | Formatting only (cargo fmt) |
| `experiments/exp020_rootpulse_commit/src/main.rs` | Import order (cargo fmt) |

---

*© 2025–2026 ecoPrimals — AGPL-3.0-or-later / CC-BY-SA-4.0 / ORC*
