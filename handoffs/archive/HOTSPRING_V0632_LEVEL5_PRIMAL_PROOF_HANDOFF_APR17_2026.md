# hotSpring v0.6.32 — Level 5 Primal Proof Handoff

**Date:** April 17, 2026
**From:** hotSpring
**To:** primalSpring auditors, barraCuda team, sibling springs
**License:** AGPL-3.0-or-later

---

## Summary

hotSpring has implemented the Level 5 "primal proof" infrastructure: a Tier 3
validation harness (`validate_primal_proof`) that calls NUCLEUS primals directly
over IPC and compares results against Python/Rust baselines. This completes the
three-tier validation arc.

**Validation Ladder Position:** Level 2-3 (Rust proof) is solid with 63/63
suites. Level 5 (primal proof) harness is written, standalone mode verified
(exit 2). Full IPC validation requires deployed plasmidBin ecobins.

---

## What Changed

### 1. downstream_manifest.toml — Fixed validation_capabilities

**Before:** Listed hotSpring's own `LOCAL_CAPABILITIES` (`physics.lattice_qcd`,
`physics.nuclear_eos`, etc.) — methods the spring *serves*, not methods it needs
to *call*.

**After:** Lists actual primal IPC methods the spring's science exercises:

```toml
validation_capabilities = [
    "tensor.matmul",        # barraCuda — SU(3) gauge field matrix operations
    "tensor.create",        # barraCuda — tensor allocation
    "tensor.add",           # barraCuda — field arithmetic
    "tensor.scale",         # barraCuda — scalar-field multiplication
    "stats.mean",           # barraCuda — observable averaging
    "stats.std_dev",        # barraCuda — statistical error
    "compute.dispatch",     # barraCuda/toadStool — GPU shader execution
    "crypto.hash",          # BearDog — blake3 provenance witnesses
    "tolerances.get",       # barraCuda — tolerance retrieval
    "validate.gpu_stack",   # barraCuda — GPU capability validation
]
```

**Action for primalSpring:** Verify other springs follow this pattern. The
`validation_capabilities` field should list primal IPC methods consumed during
the Level 5 proof, not the spring's own served methods.

### 2. validate_primal_proof Binary

New Tier 3 harness with 9 probes exercising all 10 manifest capabilities:

| Probe | IPC Method | Primal | Baseline |
|-------|-----------|--------|----------|
| Parameter construction | `tensor.create` + `tensor.scale` | barraCuda | Rust local |
| SU(3) matrix multiply | `tensor.matmul` | barraCuda | Identity parity < 1e-15 |
| Field arithmetic | `tensor.add` | barraCuda | Element-wise parity < 1e-15 |
| Observable averaging | `stats.mean` + `stats.std_dev` | barraCuda | Python baseline (plaquette) |
| GPU dispatch | `compute.dispatch` | toadStool/barraCuda | Result present |
| Provenance witness | `crypto.hash` | BearDog | Valid blake3 hex |
| Tolerance retrieval | `tolerances.get` | barraCuda | Result present |
| GPU stack validation | `validate.gpu_stack` | barraCuda | Result present |
| End-to-end SEMF | `stats.mean` (for term sum) | barraCuda | `COMPOSITION_SEMF_PARITY_REL` (1e-10) |

Exit codes: 0 = all PASS, 1 = at least one FAIL, 2 = all SKIP (no NUCLEUS).

### 3. IPC Mapping Document

`docs/PRIMAL_PROOF_IPC_MAPPING.md` maps every domain science path (SEMF,
lattice QCD, HMC, CG, gradient flow, MD, observables, provenance) to specific
primal JSON-RPC methods with parameters, expected values, and tolerances.

This is the design document for Level 5/6 evolution — when barraCuda IPC
replaces in-process library calls for production science.

### 4. Capability Domain Routing Fix

`validate_nucleus_node` and `validate_nucleus_composition` were routing
hotSpring's own physics methods through the "compute" capability domain
(`call_by_capability("compute", "physics.nuclear_eos", ...)`), which could
accidentally resolve to toadStool instead of hotSpring. Fixed to use "physics"
domain.

**Action for sibling springs:** Check that `call_by_capability` uses the correct
domain for the target primal. `"compute"` → toadStool, `"physics"` → hotSpring,
`"math"` → barraCuda, `"crypto"` → BearDog.

### 5. Stadial Compliance

| Item | Before | After |
|------|--------|-------|
| `ValidationSink::Ndjson` | `Box<dyn Write + Send>` | `Vec<u8>` (zero dyn) |
| bin/ `#[allow]` (6 sites) | `#[allow(clippy::float_cmp)]` | `#[expect(clippy::float_cmp, reason)]` |
| bin/ `unsafe_code` (2 files) | `#![allow(unsafe_code)]` | `#![expect(unsafe_code, reason)]` / `cfg_attr` |
| metalForge/forge | no `rust-version` | `rust-version = "1.87"` |
| harvest-ecobin.sh | minimal metadata | full schema matching committed `metadata.toml` |

---

## Architecture: Deploy Graph vs Proto-Nucleate

hotSpring maintains two distinct graph types — documented in `graphs/README.md`:

| Property | Proto-Nucleate | Deploy Graph |
|----------|---------------|--------------|
| Location | primalSpring/graphs/downstream/ | hotSpring/graphs/ |
| Spring binary as node | No | Yes (order = 10) |
| Purpose | Level 5 primal proof | Level 2-3 integration |
| Consumed by | validate_primal_proof | biomeOS deploy |

The proto-nucleate defines *which* primals compose (the target). The deploy
graph defines *how* to deploy them (including the spring's own server).

---

## Gaps Handed Back to primalSpring

### For barraCuda team:
- The 10 `validation_capabilities` in the manifest need to be exercised against
  the actual barraCuda ecobin. The harness is ready; what's needed is a deployed
  NUCLEUS with barraCuda alive on UDS.
- `tolerances.get` and `validate.gpu_stack` may not exist as methods on the
  barraCuda primal yet. These would be useful for cross-spring tolerance
  synchronization and GPU health reporting.

### For primalSpring:
- **Downstream manifest pattern:** Verify all springs' `validation_capabilities`
  list primal IPC methods (consumed), not local methods (served).
- **Capability domain routing:** The `capability_domain_for_required_primal()`
  mapping in `composition.rs` should be canonical. Current: beardog→"crypto",
  barracuda→"math", toadstool→"compute", coralreef→"shader".
- **Tier 3 harness pattern:** `validate_primal_proof` is the template for
  sibling springs. Key pattern: discover → call by capability → compare vs
  baseline → exit 0/1/2.

### For biomeOS team:
- The `register_with_target()` pattern in `niche.rs` sends `lifecycle.register`
  + `capability.register` for each domain. Confirm biomeOS processes the
  `semantic_mappings`, `operation_dependencies`, and `cost_estimates` payloads.
- Neural API socket discovery via `resolve_neural_api_socket()` uses convention
  `neural-api-{family_id}.sock`. Confirm this matches biomeOS naming.

---

## Composition Patterns for NUCLEUS Deployment via neuralAPI

### Deployment Flow

```
biomeos deploy --graph graphs/hotspring_qcd_deploy.toml
  → biomeOS reads deploy graph
  → Spawns primals in dependency order (beardog → songbird → ... → hotspring_primal)
  → Each primal registers via lifecycle.register
  → biomeOS routes capability.call through neuralAPI semantic layer
  → validate_primal_proof exercises the composition externally
```

### Pattern: Spring as External Validator

Springs are NOT nodes in the proto-nucleate (Level 5) graph. They validate
*against* the composition, not *inside* it. The spring's own server binary
appears in the deploy graph (Level 2-3) for integration testing. The distinction:

- **Level 2-3:** Spring server dispatches science in-process via library calls.
  The `validate_nucleus_*` binaries test this routing.
- **Level 5:** A separate harness calls primals directly over IPC. The
  `validate_primal_proof` binary tests this.
- **Level 6:** NUCLEUS deployed from plasmidBin ecobins on a clean machine.
  Spring validates externally (same harness, different environment).

### OnceLock for Family ID

hotSpring replaced `unsafe { std::env::set_var("FAMILY_ID", ...) }` with
`niche::set_family_id()` using `std::sync::OnceLock`. This is Edition 2024
compliant and eliminates the last `unsafe` in application code. Pattern
recommended for all springs that need runtime-configurable family IDs.

---

## Files Changed

### hotSpring repository
- `barracuda/src/bin/validate_primal_proof.rs` — NEW
- `docs/PRIMAL_PROOF_IPC_MAPPING.md` — NEW
- `barracuda/Cargo.toml` — new `[[bin]]` entry
- `barracuda/src/bin/validate_all.rs` — suite count 62→63
- `barracuda/src/validation/composition.rs` — `Vec<u8>` replaces `Box<dyn Write>`
- `barracuda/src/bin/validate_nucleus_node.rs` — domain routing fix
- `barracuda/src/bin/validate_nucleus_composition.rs` — domain routing fix
- `barracuda/src/bin/validate_npu_beyond_sdk.rs` — `#[expect]` migration
- `barracuda/src/bin/validate_npu_pipeline.rs` — `#[expect]` migration
- `barracuda/src/bin/bench_kokkos_complexity.rs` — `#[expect]` migration
- `barracuda/src/bin/validate_5060_dual_use.rs` — `#[expect(unsafe_code)]`
- `barracuda/src/bin/exp070_register_dump.rs` — `cfg_attr` + `#[expect(unsafe_code)]`
- `metalForge/forge/Cargo.toml` — added `rust-version = "1.87"`
- `graphs/README.md` — deploy graph vs proto-nucleate documentation
- `scripts/harvest-ecobin.sh` — full metadata schema generation

### primalSpring repository
- `graphs/downstream/downstream_manifest.toml` — hotspring `validation_capabilities` corrected

### infra/wateringHole
- This handoff document

---

## Next Steps

1. **Deploy NUCLEUS from plasmidBin** and run `validate_primal_proof` against live primals
2. **barraCuda team:** Confirm `tensor.*`, `stats.*`, `tolerances.get`, `validate.gpu_stack` methods work as documented in `PRIMAL_PROOF_IPC_MAPPING.md`
3. **Sibling springs:** Adopt the `validate_primal_proof` pattern — the three-tier harness template is reusable
4. **primalSpring:** Audit all springs' `validation_capabilities` for the same bug (listing own methods instead of consumed primal methods)
