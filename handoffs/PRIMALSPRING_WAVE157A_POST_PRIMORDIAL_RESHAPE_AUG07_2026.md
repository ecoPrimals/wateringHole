# primalSpring — Post-Primordial Reshape (Wave 157a)

**Date**: 2026-08-07
**Gate**: eastGate
**Team**: primalSpring code team
**Wave**: 157a (G67 Stage 2 Neural API Activation)

## Summary

Complete post-primordial reshape of primalSpring: specs modernized to G64-G67,
primordial debt feature-gated, 10 experiments migrated to capability-first
routing, library core evolved to TOML-driven runtime discovery, session-scoped
provenance model adopted, shared experiment utilities extracted.

## Spec Track (Track 1)

| Deliverable | Status |
|-------------|--------|
| `specs/STAGE2_ACTIVATION.md` | NEW — bridges G67 spec to primalSpring validation |
| `specs/NEURAL_API_EVOLUTION.md` | UPDATED — Wave 67 section, N1 done, subGen evidence |
| `specs/COMPOSITION_BROKER.md` | NEW — 704 caps, signal collapse, session provenance |
| `specs/NUCLEUS_LAB_INTEGRATION.md` | NEW — benchScale/agentReagents integration |
| `CONTEXT.md` / `ARCHITECTURE.md` / `README.md` | UPDATED — counts, G67, post-primordial status |

## Code Track (Track 2)

### Primordial Debt Feature-Gated

- `primordial-compat` feature added to `ecoPrimal/Cargo.toml`
- `harness/` module gated behind `#[cfg(feature = "primordial-compat")]`
- `launcher/spawn_*` deprecated functions gated
- `SignalTier` marked `#[deprecated]` with Wave 170 removal target
- Integration tests use `required-features = ["primordial-compat"]`
- Default build is clean post-primordial

### Experiments Migrated to NeuralBridge (10 total)

| Experiment | Migration |
|------------|-----------|
| exp033 | `discover_primal()` → `CompositionContext` |
| exp059 | `socket_env_var()` → `CompositionContext` |
| exp073 | TCP cross-gate → `NeuralBridge` (remote TCP retained for cross-gate) |
| exp074 | TCP health → `CompositionContext::health_check()` |
| exp076 | `tcp_rpc` Pixel → `NeuralBridge::capability_call()` |
| exp077 | Hand-rolled UDS → AI domain via Neural API |
| exp085 | All crypto phases → `NeuralBridge` |
| exp086 | All genetic phases → `NeuralBridge` |
| exp087 | Consolidated to single `NeuralBridge` API |
| exp089 | Live sign/verify → `NeuralBridge` |
| exp090 | Tower LAN probe → `CompositionContext` |
| exp096 | All submodules → `NeuralBridge` via shared `rpc_value()` |

### Library Evolution

| Change | Files |
|--------|-------|
| Crypto HMAC delegates to bearDog RPC | `certification/crypto_bootstrap.rs` |
| `has_tower()` → TOML-derived tier check | `evolution/gate.rs` |
| `from_domain()` → TOML-driven tier resolution | `composition/neural_routing.rs` |
| Tier 1 discovery → capability-first resolution | `composition/context_discovery.rs` |
| `port_entry_for()` → TOML-derived cache | `tolerances/ports.rs` |
| Routing docs → bootstrap vs runtime architecture | `composition/routing.rs` |

### New Experiments

| Experiment | Purpose |
|------------|---------|
| exp116_benchscale_nucleus_lab | benchScale NUCLEUS testing (N2/N4 validation) |
| exp117_compute_trio_routing | Node Atomic compute trio IPC (shader→coralReef→toadStool) |

### Shared Utilities Extracted

- `trio_ops/src/experiment.rs` — `phase_composition_discovery()`, `require_neural_bridge()`, `RemoteGateConfig`, `env_or()`
- `trio_ops/src/census.rs` — TOML-driven port/socket census (deduplicated exp112/113/114)
- Session-scoped provenance model in `trio_ops/src/lib.rs` (4-phase: dehydrate → spine → sign → braid)

## Upstream Gaps for Primal Teams

| Gap | Owner | Description |
|-----|-------|-------------|
| `ipc.resolve({"capability": cap})` | biomeOS | Songbird should support pure capability resolution (currently needs `primal_id` fallback) |
| `crypto.hmac_sha256` RPC | bearDog | Key derivation delegation — primalSpring calls but bearDog may not implement this method yet |
| Session-scoped provenance | rhizoCrypt/loamSpine | `session.commit` method name vs `session` — need canonical method name |
| `braid.create` vs `create_braid` | sweetGrass | Method name standardization needed |
| PathwayLearner wiring | biomeOS | Phase 3/4 gap — ML-driven routing optimization |
| benchScale `lab.create` API | benchScale | exp116 exercises this but API may not be stable |

## Test Results

- 1,263 workspace tests (1,224 lib + 19 trio_ops + 20 doc)
- 197 validation scenarios (14 tracks, 3 tiers)
- 95 experiments (21 tracks)
- 5 pre-existing test failures (ecosystem freshness drift, known debt resolution)
- Zero new regressions

## Next Steps

- N6 validation (full graph execution through Neural API)
- benchScale live testing when server is deployed
- Cross-gate compute trio validation (exp117 → real toadStool/coralReef)
- Downstream spring validation matrix completion
