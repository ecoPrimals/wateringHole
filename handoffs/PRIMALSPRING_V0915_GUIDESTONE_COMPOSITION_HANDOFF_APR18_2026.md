# primalSpring v0.9.15 — guideStone Composition Certification Handoff

**Date**: April 18, 2026
**From**: primalSpring v0.9.15 (Phase 43+)
**For**: All downstream springs (hotSpring, healthSpring, neuralSpring, wetSpring, ludoSpring, airSpring, groundSpring)
**License**: AGPL-3.0-or-later

---

## What Changed

primalSpring now has its own **guideStone binary** (`primalspring_guidestone`) that validates NUCLEUS composition correctness across 6 layers. This is the **base certification layer** — domain guideStones inherit it and only validate their own science on top.

### New Artifacts

| Artifact | Location | What It Does |
|----------|----------|--------------|
| `primalspring_guidestone` binary | `ecoPrimal/src/bin/primalspring_guidestone/main.rs` | 6-layer NUCLEUS composition certification |
| guideStone Composition Standard | `wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` | Ecosystem-wide standard for self-validating deployables |
| Layered certification docs | `wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` | "Layered Certification: Base + Domain" section |
| Composition API (public) | `ecoPrimal/src/composition/mod.rs` | `capability_to_primal()`, `method_to_capability_domain()`, `validate_liveness()` |

### The 6 Certification Layers

| Layer | What It Validates | Requires Primals? |
|-------|------------------|------------------|
| **0 — Bare Properties** | Deploy graph parsing, fragment resolution, manifest consistency, bonding types | No |
| **1 — Discovery** | All primals discoverable via capability-based scan | Yes |
| **2 — Atomic Health** | Tower, Node, Nest `health.liveness` response | Yes |
| **3 — Capability Parity** | `stats.mean`, `tensor.matmul`, storage roundtrip, shader capabilities | Yes |
| **4 — Cross-Atomic Pipeline** | Tower hash → Nest store → retrieve → verify | Yes |
| **5 — Bonding Model** | `BondType` well-formedness, cipher policy ordering, trust hierarchy | No |
| **6 — BTSP + Crypto** | `crypto.hash` determinism, BTSP policy, Ed25519 sign/verify roundtrip | Yes |

### Exit Codes

- `0` — all layers passed (NUCLEUS certified)
- `1` — one or more layers failed
- `2` — bare-only mode (no primals discovered, structural checks only)

---

## What You Should Do

### If your spring is at guideStone Level 0 (airSpring, groundSpring)

1. **Pull primalSpring** and review the guideStone standard: `wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md`
2. **Read your manifest entry**: `graphs/downstream/downstream_manifest.toml`
3. **Start with a validation window**: Build a simple IPC client that calls your `validation_capabilities` against a running NUCLEUS and compares results against your Python baselines
4. Use `primalspring::composition::{CompositionContext, validate_parity, validate_liveness}` as your API

### If your spring is at guideStone Level 1 (healthSpring, neuralSpring, wetSpring, ludoSpring)

1. **You already have the validation binary.** Now evolve it toward a guideStone:
2. **Document the 5 properties** for your domain science (deterministic output, reference-traceable, self-verifying, environment-agnostic, tolerance-documented)
3. **Add bare guideStone mode**: Properties 1–5 must hold without any primals running
4. **Package as a deployable binary**: Name it `<spring>_guidestone`
5. **Use the pre-flight**: Run `primalspring_guidestone` first — if it passes, discovery/health/crypto are already certified

### If your spring is at guideStone Level 5 (hotSpring)

1. **You're the reference.** hotSpring-guideStone-v0.7.0 is the certified pattern.
2. **Use the pre-flight**: `primalspring_guidestone` before your domain checks avoids redundant validation
3. **Hand back patterns**: Any patterns you discover that should be universal, hand back to primalSpring

---

## Composition API You Should Use

### Discovery + Liveness

```rust
use primalspring::composition::{CompositionContext, validate_liveness};
use primalspring::validation::ValidationResult;

let mut ctx = CompositionContext::from_live_discovery_with_fallback();
let mut v = ValidationResult::new("myspring guideStone");

let alive = validate_liveness(&mut ctx, &mut v, &["tensor", "security", "compute"]);
if alive == 0 {
    eprintln!("No NUCLEUS primals. Deploy from plasmidBin and rerun.");
    std::process::exit(2);
}
```

### Scalar Parity

```rust
use primalspring::composition::validate_parity;
use primalspring::tolerances;

validate_parity(
    &mut ctx, &mut v,
    "sample_mean",
    "tensor",           // capability domain → resolves to barraCuda
    "stats.mean",       // JSON-RPC method
    serde_json::json!({"data": [1.0, 2.0, 3.0, 4.0, 5.0]}),
    "result",           // key in JSON-RPC response
    3.0,                // expected (from Python baseline)
    tolerances::IPC_ROUND_TRIP_TOL,
);
```

### Method Routing

```rust
use primalspring::composition::{capability_to_primal, method_to_capability_domain};

let domain = method_to_capability_domain("stats.mean");    // → "tensor"
let primal = capability_to_primal(domain);                  // → "barracuda"
```

---

## guideStone Readiness Tracker

| Spring | Level | What's Done | Next Step |
|--------|-------|-------------|-----------|
| **primalSpring** v0.9.15 | **1** | `primalspring_guidestone` binary, 6-layer certification | Live NUCLEUS testing, Properties 2–3 |
| **hotSpring** v0.6.32 | **5** | guideStone-v0.7.0: all 5 properties certified | aarch64 CI |
| **healthSpring** V53 | **1** | exp122 IPC parity, `math_dispatch.rs` | Property 4 (patient data), 9/11 methods library-only |
| **neuralSpring** V133 | **1** | `IpcMathClient` (9 methods), 7 caps | 18 barraCuda surface gaps |
| **wetSpring** V145 | **1** | Exp403 (5 primals over IPC), 22 caps | guideStone packaging |
| **ludoSpring** V44 | **1** | `validate_primal_proof`, four-layer | guideStone packaging |
| **airSpring** v0.10.0 | **0** | 90.56% coverage, no IPC | Build IPC client |
| **groundSpring** V124 | **0** | 92% coverage, no IPC | Build IPC client |

---

## Key References

| Document | Location |
|----------|----------|
| guideStone Composition Standard | `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` |
| Composition Guidance | `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` |
| Downstream Manifest | `primalSpring/graphs/downstream/downstream_manifest.toml` |
| Proto-Nucleate Template | `primalSpring/graphs/downstream/proto_nucleate_template.toml` |
| Ecosystem Leverage Guide | `primalSpring/wateringHole/PRIMALSPRING_ECOSYSTEM_LEVERAGE_GUIDE.md` |
| Primal Gaps Registry | `primalSpring/docs/PRIMAL_GAPS.md` |
| Stadial Gate | `primalSpring/wateringHole/STADIAL_PARITY_GATE_APR16_2026.md` |
| Graph Consolidation Handoff | `primalSpring/wateringHole/GRAPH_CONSOLIDATION_AND_NUCLEUS_DEPLOYMENT_HANDOFF_APR16_2026.md` |

---

## Gaps for Primals (Upstream Evolution Needed)

These gaps were discovered during composition validation and guideStone certification.
They require primal team evolution, not spring-side fixes.

| Gap | Primal | Impact | Severity |
|-----|--------|--------|----------|
| `crypto.sign_contract` (ionic bond negotiation) | BearDog | Cross-tower compositions can't negotiate ionic bonds via IPC | Medium |
| BTSP Phase 3 encrypted channel runtime | All | Post-handshake encrypted communication not exercised in live deployment | Medium |
| `compute.dispatch` standardization | toadStool | Springs doing GPU compute can't route generically | Medium |
| Squirrel provider registration protocol | Squirrel | Springs adding Squirrel to compositions can't register as providers | Low |
| `storage.fetch_external` (cross-spring data) | NestGate | Cross-spring data pipelines need external fetch | Low |
| 18 barraCuda IPC surface gaps (eigh, Pearson, chi-squared, etc.) | barraCuda | neuralSpring blocked on full self-validation | High |
| loamSpine provenance chain API for guideStone receipts | loamSpine | guideStone DAG signing can't trace computation provenance | Low |

---

## The End Goal

Pull to a clean machine. Deploy NUCLEUS from `plasmidBin` ecobins.
`primalspring_guidestone` certifies the composition is sound.
Domain guideStone certifies the science is faithful.
The NUCLEUS is self-validating. The spring steps aside.

```
Python baseline (peer-reviewed)
    → Rust validation (spring binary, the "Rust proof")  ← DONE
        → Primal composition (IPC to NUCLEUS)             ← Level 5
            → guideStone deploys in-graph                 ← Level 6
                → NUCLEUS self-validates and serves        ← TARGET
```

*This handoff supersedes: `PRIMALSPRING_PHASE43_FINAL_HANDOFF_APR15_2026.md`,
`PRIMALSPRING_V0914_PHASE43_HANDOFF_APR14_2026.md` for composition and
guideStone-related content.*
