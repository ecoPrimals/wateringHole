# ludoSpring V41 — Composition Evolution Patterns Handoff

**Date:** April 11, 2026
**From:** ludoSpring
**To:** primalSpring, barraCuda, toadStool, coralReef, Squirrel, petalTongue, biomeOS, NestGate, rhizoCrypt, loamSpine, sweetGrass, all springs
**Status:** CI-green, 779 tests, 100 experiments, 10 documented gaps, 9 composition patterns absorbed

---

## Executive Summary

ludoSpring V41 absorbs 9 hardened composition patterns from primalSpring, plasmidBin, and `SPRING_COMPOSITION_PATTERNS.md`. This completes the evolution from **validation spring** (Python→Rust) to **composition spring** (Python→Rust→IPC→NUCLEUS). The patterns are tested, documented, and ready for ecosystem-wide adoption.

**Key narrative:** Python was our validation target for Rust. Now both Python and Rust are validation targets for ecoPrimal NUCLEUS composition patterns. The golden chain traces a single computation (Fitts cost, Flow sigmoid, engagement dot product) from the published paper's formula through Python baseline → Rust library → IPC serialization → NUCLEUS primal graph → runtime composition validation.

## What Changed in V41

### Composition Patterns Absorbed

| # | Pattern | Source | Location | Tests Added |
|---|---------|--------|----------|-------------|
| 1 | `IpcErrorPhase` + `PhasedIpcError` | primalSpring `ecoPrimal/src/ipc/error.rs` | `ipc/envelope.rs` | 5 |
| 2 | `is_retriable()` / `is_recoverable()` / `is_method_not_found()` | primalSpring `PhasedIpcError` | `ipc/envelope.rs` | (included in #1) |
| 3 | Method normalization (`normalize_method`) | `SPRING_COMPOSITION_PATTERNS` §1 | `ipc/envelope.rs` + `ipc/handlers/mod.rs` | 6 |
| 4 | Three-tier dispatch (lifecycle → infra → science) | `SPRING_COMPOSITION_PATTERNS` §4 | `ipc/handlers/mod.rs` | 2 |
| 5 | Tiered discovery (`DiscoveryTier`, `DiscoveryResult`) | `SPRING_COMPOSITION_PATTERNS` §3 | `ipc/discovery/mod.rs` | 4 |
| 6 | `NicheDependency` table (11 primals) | `SPRING_COMPOSITION_PATTERNS` §11 | `niche.rs` | 2 |
| 7 | Typed inference wire types (`inference.*`) | neuralSpring | `ipc/squirrel.rs` | 0 (types only) |
| 8 | `CompositionReport` + live validation | `SPRING_COMPOSITION_PATTERNS` §5 | `ipc/composition.rs` (new) | 3 |
| 9 | `--port` CLI flag | plasmidBin startup contract | `bin/ludospring.rs` | 0 (CLI) |

**Test delta:** 733 → 779 (+46 tests). Zero clippy warnings. Zero regressions.

### Architecture Changes

**Before V41:** Flat dispatch (one `match` with 40+ arms), bare `Option<PrimalEndpoint>` discovery, no error phase tracking, no dependency table.

**After V41:**
- Dispatch is three-tiered: `dispatch_lifecycle()` → `dispatch_infrastructure()` → `dispatch_science()`, with method normalization before matching
- Discovery returns `DiscoveryResult::Found { endpoint, tier }` or `DiscoveryResult::NotFound { target, searched }` — 6-tier priority chain
- IPC errors carry phase context via `PhasedIpcError` with `is_retriable()` enabling smart retry
- `NicheDependency` table declares all 11 proto-nucleate primals with roles, required flags, and capability domains
- `CompositionReport` probes all dependencies at runtime and reports live/absent counts

## For All Springs — Composition Evolution Template

ludoSpring is now the **reference implementation** for how a spring absorbs composition patterns. The progression is:

```
1. Read proto-nucleate graph → know your primals
2. Wire typed IPC clients → graceful degradation for each
3. Add NicheDependency table → self-documenting composition
4. Add normalize_method() → handle biomeOS/peer-prefixed calls
5. Add three-tier dispatch → lifecycle/infra/science separation
6. Add IpcErrorPhase → retry/recovery classification
7. Add tiered discovery → structured NotFound diagnostics
8. Add CompositionReport → runtime composition health
9. Validate: Python → Rust → IPC → NUCLEUS → composition report
```

**Every spring should follow this progression.** The patterns are small (~15–50 lines each), tested, and backwards-compatible.

## For primalSpring — Patterns to Absorb Ecosystem-Wide

### 1. `normalize_method()` — MUST for all springs

```rust
fn normalize_method(method: &str) -> Cow<'_, str> {
    let prefixes = ["myspring.", "barracuda.", "biomeos."];
    let mut m = method;
    loop {
        let before = m;
        for p in prefixes { if let Some(s) = m.strip_prefix(p) { m = s; } }
        if m == before { break; }
    }
    if m == method { Cow::Borrowed(method) } else { Cow::Owned(m.to_owned()) }
}
```

biomeOS routing can double-prefix method names. Without normalization, `biomeos.ludospring.game.evaluate_flow` returns -32601. With it, the method resolves correctly.

### 2. `IpcErrorPhase` — SHOULD for all IPC clients

Enables smart retry: connect failures are retriable, parse failures are not, method-not-found means fallback to a different endpoint. This is critical for composition resilience.

### 3. `NicheDependency` table — SHOULD for all springs

Self-documenting alternative to reading TOML graphs at runtime. The table mirrors the proto-nucleate and makes dependency auditing trivial:

```rust
pub const DEPENDENCIES: &[NicheDependency] = &[
    NicheDependency { name: "toadstool", role: "compute", required: true, capability: "compute" },
    // ...
];
```

### 4. `CompositionReport` — SHOULD for all springs

Runtime validation that the deployment matches the proto-nucleate. Springs that implement this can answer `lifecycle.composition` requests from biomeOS and provide actionable diagnostics.

### 5. Three-tier dispatch — SHOULD for all springs

Separating lifecycle/infra/science makes auditing clear: lifecycle methods are always available, infrastructure handles routing, science is the domain. `Option<HandlerResult>` chaining is clean and extensible.

## For barraCuda Team

### Current state (unchanged from V40)
- v0.3.11 consumed, CPU-only default
- 13 WGSL shaders ready for tier-A absorption (sigmoid, relu, softmax, dot, reduce, lcg, scale, abs + 5 game-domain)
- GAP-04 (TensorSession) and GAP-08 (Fitts/Hick formula mismatch) still open

### New: ludoSpring validates barraCuda composition patterns
The `CompositionReport` now probes barraCuda as a niche dependency (`required: true, capability: "tensor"`). When barraCuda ships an IPC server, ludoSpring will validate it automatically.

## For biomeOS / Neural API Team

### Method normalization is live
ludoSpring now handles prefixed calls from biomeOS routing. Other springs should follow. The ecosystem convention is: dispatch normalizes, callers can use any prefix.

### `CompositionReport` for `lifecycle.composition`
Proposed new IPC method: `lifecycle.composition` returns a JSON report of dependency health. ludoSpring implements `ipc/composition.rs` as a reference. biomeOS can query this to build a live composition dashboard.

### GAP-10 (game.* identity) — still open
ludoSpring registers as `game.*` provider but the proto-nucleate graph has no `game` node. biomeOS deployment tooling needs to handle the spring-as-deployer pattern.

## For Provenance Trio (rhizoCrypt, loamSpine, sweetGrass)

### nest_atomic decision documented (GAP-09)
ludoSpring does NOT add `nest_atomic` to fragments. The stubs are aspirational — they gracefully degrade and will activate when:
1. rhizoCrypt ships UDS transport (GAP-06)
2. loamSpine resolves startup panic (GAP-07)
3. primalSpring adds a Nest overlay graph

`NicheDependency` table marks trio primals as `required: false`, which is accurate: ludoSpring's core science works without them.

## For Squirrel / neuralSpring Team

### Typed inference wire types added
`ipc/squirrel.rs` now defines `InferenceCompleteRequest`, `InferenceEmbedRequest`, `InferenceEmbedResponse`, `InferenceModelsRequest`, `ModelInfo`. These are ready for when neuralSpring's `inference.*` surface stabilizes. No capability routing changes needed — Squirrel handles provider discovery.

## For toadStool Team

GPU dispatch via `toadstool::dispatch_submit()` is stable. `NicheDependency` declares toadStool as `required: true, capability: "compute"`. The `CompositionReport` will automatically validate toadStool availability when deployed.

## For coralReef Team

GAP-01 (coralReef IPC not wired in production paths) unchanged. The typed client works; migration from embedded WGSL to sovereign compilation is pending.

## Primal Gap Matrix (10 gaps — unchanged)

| Gap | Primal | Severity | Status |
|-----|--------|----------|--------|
| GAP-01 | coralReef | MEDIUM | PARTIAL — client exists, engine not wired |
| GAP-02 | barraCuda | MEDIUM | OPEN — direct Rust imports, not IPC |
| GAP-03 | NestGate | LOW | OPEN — fragment metadata |
| GAP-04 | barraCuda | MEDIUM | OPEN — TensorSession unused in product |
| GAP-05 | Trio | LOW | OPEN — trio not in proto-nucleate |
| GAP-06 | rhizoCrypt | CRITICAL | OPEN — TCP-only, no UDS |
| GAP-07 | loamSpine | CRITICAL | OPEN — startup panic |
| GAP-08 | barraCuda | HIGH | OPEN — Fitts/Hick formula mismatch |
| GAP-09 | Nest | LOW | DOCUMENTED — aspirational stubs |
| GAP-10 | biomeOS | HIGH | OPEN — game.* graph identity |

## Composition Maturity Assessment (V41)

| Dimension | V40 | V41 | Notes |
|-----------|-----|-----|-------|
| Python baselines | 10/10 | 10/10 | All models have provenance, no drift |
| Rust validation | 9/10 | 9/10 | 779 tests, all tolerances named |
| IPC composition | 8/10 | **9/10** | +error phases, +method normalization, +three-tier dispatch |
| NUCLEUS deployment | 7/10 | **8/10** | +CompositionReport, +NicheDependency, +tiered discovery |
| GPU evolution | 6/10 | 6/10 | 16 WGSL shaders, TensorSession still unused in product |
| Ecosystem alignment | 8/10 | **9/10** | All 9 SPRING_COMPOSITION_PATTERNS absorbed |

**Overall: 8.5/10 — composition-validated, deployment-ready for Node + Meta.**

---

**Next Steps:**
1. Other springs absorb the same 9 patterns (template: ludoSpring `ipc/envelope.rs`, `handlers/mod.rs`, `discovery/mod.rs`, `niche.rs`, `composition.rs`)
2. primalSpring considers making `normalize_method`, `IpcErrorPhase`, and `NicheDependency` shared types in ecoPrimal
3. biomeOS adds `lifecycle.composition` to the standard probe set
4. barraCuda absorbs tier-A shaders and resolves Fitts/Hick formula mismatch (GAP-08)
5. rhizoCrypt ships UDS transport (GAP-06) → unblocks nest_atomic overlay
6. loamSpine resolves startup panic (GAP-07) → unblocks provenance pipeline

---

**License:** AGPL-3.0-or-later
