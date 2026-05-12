# ludoSpring V42 — Composition Evolution Handoff

**Date:** April 11, 2026
**From:** ludoSpring
**To:** primalSpring, barraCuda, toadStool, coralReef, Squirrel, petalTongue, biomeOS, NestGate, rhizoCrypt, loamSpine, sweetGrass, all springs
**Status:** CI-green, 781 tests, 100 experiments, 10 documented gaps (GAP-09 RESOLVED), ecoBin v0.9.0
**Supersedes:** V41 Composition Evolution Patterns (Apr 11, 2026)

---

## Executive Summary

ludoSpring V42 completes the evolution from **validation spring** to **composition spring**. Python validated Rust. Now Rust and Python are validation targets for ecoPrimal NUCLEUS composition patterns. The key V42 advances:

1. **`lifecycle.composition` is live** — biomeOS and peers can probe ludoSpring's proto-nucleate health via JSON-RPC at runtime
2. **Capability-first discovery** — composition probing resolves by `discover_by_capability()` before falling back to name-based tiered discovery
3. **`nest_atomic` declared** — fragments now reflect the full atomic surface ludoSpring wires (tower + node + nest + meta)
4. **Provenance unified** — all 88 experiment files, test headers, and `BaselineProvenance` structs aligned to single commit `19e402c0` matching `combined_baselines.json`
5. **ecoBin banned-crate enforcement** — `deny.toml` denies 8 C dependencies per ecoBin v3.0

## What Changed in V42

| Change | Impact | Module |
|--------|--------|--------|
| `lifecycle.composition` JSON-RPC handler | Runtime composition visible to biomeOS/peers | `ipc/handlers/lifecycle.rs` |
| Capability-first `probe_dependency()` | `by_capability(dep.capability)` → name fallback | `ipc/composition.rs` |
| `nest_atomic` in fragments | Accurate atomic surface declaration | `ipc/composition.rs`, `capability_registry.toml` |
| Provenance unified to `19e402c0` | Single-source traceability across 88 files | All experiments, `validation.rs` |
| ecoBin banned-crate list in `deny.toml` | Enforced: openssl-sys, ring, aws-lc-sys, native-tls, zstd-sys, lz4-sys, libsqlite3-sys, cryptoki-sys | `deny.toml` |
| fog_of_war.wgsl README reconciled | Shader docs match implementation (distance mask, not Bresenham) | `barracuda/shaders/game/README.md` |
| exp045 doc link fixed | Zero rustdoc warnings | `experiments/exp045` |
| GAP-09 → RESOLVED | `nest_atomic` declared; trio `required: false` | `docs/PRIMAL_GAPS.md` |

**Test delta:** 780 → 781 (+1 `lifecycle_composition_returns_report`). Zero clippy. Zero fmt diffs. `cargo deny check` passes.

## For primalSpring — Composition Feedback

### Patterns ludoSpring Validates

ludoSpring now exercises the full composition evolution ladder from `SPRING_COMPOSITION_PATTERNS.md`:

| Pattern | § | Status | Notes |
|---------|---|--------|-------|
| Method normalization | §1 | DONE | Iterative prefix strip; tested with double-prefixed biomeOS calls |
| Capability registration | §2 | DONE | 27 capabilities + semantic mappings + cost estimates + operation dependencies |
| Tiered discovery | §3 | DONE | 6-tier chain; **V42: composition probing now by_capability first** |
| Two-tier dispatch | §4 | DONE | Three-tier in practice (lifecycle / infra / science) |
| Graph validation | §5 | DONE | **V42: `lifecycle.composition` handler externally callable** |
| Niche identity | §11 | DONE | 11 `NicheDependency` entries with capability domains |

### Gaps Handed Back

- **GAP-03** (fragment metadata): `nest_atomic` now declared in ludoSpring. Proto-nucleate graph at `primalSpring/graphs/downstream/ludospring_proto_nucleate.toml` should update `fragments` to match.
- **GAP-05** (trio not in proto-nucleate): ludoSpring wires trio with `required: false`. Proto-nucleate graph should add optional trio nodes.
- **GAP-10** (`game.*` identity): No graph node advertises the `game` capability domain. biomeOS needs a routing rule or ludoSpring needs a graph node declaring `game.*` as its provider set.
- **Deployment matrix**: `deployment_matrix.toml` cell `ludospring-ipc-surface` is still marked as a blocker for storytelling topologies. ludoSpring now exposes 27 `game.*` methods + `lifecycle.composition` — this surface may be sufficient.

### Proto-nucleate Alignment

ludoSpring's niche now declares **`tower_atomic`, `node_atomic`, `nest_atomic`, `meta_tier`** — matching a near-full NUCLEUS composition minus `nucleus` (full assembly). Proto-nucleate graph should evolve to match.

## For barraCuda

### Active Consumption (v0.3.11)

| Primitive | ludoSpring module | Usage |
|-----------|-------------------|-------|
| `activations::sigmoid` | `interaction::flow` | `DifficultyCurve` |
| `stats::dot` | `metrics::engagement` | Weighted engagement composite |
| `rng::lcg_step`, `state_to_f64` | `procedural::bsp` | Deterministic BSP generation |
| `device::WgpuDevice` | `game/engine/gpu_context.rs` | GPU context (behind `gpu` feature) |
| `session::TensorSession` | `game/engine/gpu_context.rs` | Scaffolded, zero product call sites |

### GAP-08 (Fitts/Hick formula mismatch)

IPC-exposed Fitts/Hick formulas still produce different values than ludoSpring's validated implementations. 4 composition checks fail. ludoSpring uses MacKenzie (1992) parameters; barraCuda IPC surface may use different constants.

### Absorption Candidates

| Module | Priority | What barraCuda gets |
|--------|----------|---------------------|
| `procedural::noise` (Perlin 2D/3D + fBm) | P1 | GPU-ready noise; ludoSpring copy is validation reference |
| `capability_domains.rs` | P1 | Structured Domain/Method introspection pattern |
| `validation/` (`ValidationHarness<S>`) | P1 | Composable validation with `ValidationSink` trait |
| `procedural::wfc` | P2 | Wave Function Collapse (GPU-parallel candidate) |
| `procedural::bsp` | P2 | BSP spatial partitioning |
| `ipc/toadstool.rs` | P0 | Typed toadStool client — first typed contract for compute dispatch |

### TensorSession (GAP-04)

`GpuContext::tensor_session()` exists but has zero product call sites. barraCuda should clarify the f32 vs f64 `TensorSession` story so ludoSpring can wire at least one Tier A op (sigmoid or dot) through `TensorSession` for end-to-end validation.

## For toadStool

- GPU dispatch handlers (`game.gpu.*`) delegate to toadStool via `compute.submit` / `compute.dispatch.submit`
- 5 WGSL shaders in `barracuda/shaders/game/` — 3 game-specific (fog, lighting, pathfind), 2 inherited (perlin_2d, dda_raycast)
- Shader tier mapping documented in `specs/BARRACUDA_REQUIREMENTS.md`

## For coralReef (GAP-01)

Typed client exists (`ipc/coralreef.rs` — `shader.compile`, `shader.list`). Product GPU path still uses embedded WGSL + toadStool dispatch, not coralReef compile. Wiring coralReef on the product path requires coralReef maturity for WGSL→native compilation.

## For rhizoCrypt (GAP-06 — CRITICAL)

TCP-only transport blocks 9 composition checks. ludoSpring's proto-nucleate declares `transport = "uds_only"`. All trio IPC stubs gracefully degrade. When UDS lands, ludoSpring will automatically light up provenance.

## For loamSpine (GAP-07 — CRITICAL)

Startup panic (runtime nesting) blocks 6 composition checks. ludoSpring's `ipc/provenance/loamspine.rs` is wired and tested for degradation. Ready to activate when the panic is resolved.

## For Squirrel

Typed inference wire types ready: `InferenceCompleteRequest`, `InferenceEmbedRequest`/`Response`, `InferenceModelsRequest`, `ModelInfo`. ludoSpring gains `inference.complete`, `inference.embed`, `inference.models` automatically when neuralSpring evolves WGSL shader ML. No code changes needed — Squirrel discovers neuralSpring as provider.

## For biomeOS

- `lifecycle.composition` → returns `CompositionReport` with per-dependency liveness, fragment metadata, and composition completeness
- `health.liveness` / `health.readiness` for Kubernetes-style probes
- `capability.list` with cost estimates and operation dependencies for scheduling
- Neural API registration via `lifecycle.register` on startup (graceful standalone fallback)
- `lifecycle.composition` enables biomeOS to verify graph health without running science workloads

## For All Springs — V42 Composition Template

The composition evolution ladder is now fully exercised by ludoSpring:

```
1. Read proto-nucleate → know your primals and atomics
2. Wire typed IPC clients → graceful degradation for each primal
3. Add NicheDependency table → 11 entries with capability domains
4. Add normalize_method() → handle biomeOS/peer-prefixed calls
5. Add three-tier dispatch → lifecycle/infra/science separation
6. Add IpcErrorPhase → retry/recovery/method-not-found classification
7. Add tiered discovery → 6-tier resolution with structured DiscoveryResult
8. Add CompositionReport → runtime composition health (NEW: externally callable)
9. Add lifecycle.composition handler → biomeOS can probe your composition
10. Probe by_capability first → name fallback for legacy primals
11. Declare accurate fragments → nest_atomic when you wire Nest surface
12. Unify provenance → single commit, single date, single SHA across all artifacts
13. Enforce ecoBin bans → deny.toml banned-crate list
14. Validate: Python → Rust → IPC → NUCLEUS → composition report → deployment
```

## Verification

```sh
cargo fmt --all -- --check              # PASS
cargo clippy --workspace --all-features # 0 warnings
cargo test --workspace --all-features   # 781 passed, 0 failed
cargo deny check                        # advisories ok, bans ok, licenses ok, sources ok
python3 baselines/python/check_drift.py # No baseline drift
```

---

**License:** AGPL-3.0-or-later
