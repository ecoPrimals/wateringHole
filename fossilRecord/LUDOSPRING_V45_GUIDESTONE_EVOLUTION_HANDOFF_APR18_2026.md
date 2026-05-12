# SPDX-License-Identifier: AGPL-3.0-or-later

# ludoSpring V45 — guideStone Evolution Handoff

**Date:** April 18, 2026
**From:** ludoSpring
**To:** All primal teams, all spring teams, biomeOS, esotericWebb
**Version:** V45 (790+ tests, guideStone readiness 3, plasmidBin v0.10.0)

---

## Executive Summary

ludoSpring V45 is the first domain spring to reach **guideStone readiness 3**
(bare mode passes). The `ludospring_guidestone` binary validates 5 certified
properties without any live primals (15 structural checks), and validates
15 domain science checks across 13 barraCuda IPC methods when a NUCLEUS is
deployed. This handoff documents everything learned about the composition
patterns, primal gaps, and deployment model — for primal teams to evolve and
sibling springs to follow the same path.

```
Python baseline (peer-reviewed)
    → Rust validation (spring binary)         ← Level 2 DONE
        → IPC composition (ludoSpring socket)  ← Level 3 DONE
            → Primal proof (raw IPC)           ← Level 4 (V44)
                → guideStone (composition API) ← Level 5 readiness 3 (V45)
                    → NUCLEUS deploys in-graph ← Level 6 TARGET
```

---

## Part 1: What ludoSpring Proved

### Three-layer guideStone architecture

| Layer | What it does | Checks | Primals needed |
|-------|-------------|--------|----------------|
| **0 — Bare Properties** | Validates 5 certified properties from first principles | 15 | None |
| **1 — Discovery** | Finds NUCLEUS primals via `CompositionContext` | 2 | tensor, compute |
| **2 — Domain Science** | Validates game science via capability-routed IPC | 15 | barraCuda minimum |

### Layer 0 breakdown (bare — always passes)

| Property | Checks | Method |
|----------|--------|--------|
| Deterministic Output | 6 | Recompute Fitts, Hick, sigmoid, log₂, mean, variance from published formulas |
| Reference-Traceable | 7 | Every golden constant is finite and sourced to a named paper |
| Self-Verifying | 2 | Tampered golden values (+1.0, +0.001) detected by tolerance guard |
| Environment-Agnostic | 2 | No GPU feature, no network calls in bare mode |
| Tolerance-Documented | 3 | `DETERMINISTIC_FLOAT < IPC_ROUND_TRIP ≤ WGSL_SHADER`, `BARE_RECOMPUTE < IPC_ROUND_TRIP` |

### Layer 2 breakdown (domain science — requires NUCLEUS)

| Method | Capability | Validation | Golden Value |
|--------|-----------|------------|--------------|
| `activation.fitts` | tensor | Parity | 708.848 (Fitts 1954, MacKenzie 1992) |
| `activation.hick` | tensor | Parity | 650.0 (Hick 1952) |
| `math.sigmoid` | tensor | Parity | 0.6225 |
| `math.log2` | tensor | Parity | 3.0 (exact) |
| `stats.mean` | tensor | Parity | 3.0 (exact) |
| `stats.variance` | tensor | Parity | 4.0 |
| `stats.std_dev` | tensor | Existence | — |
| `noise.perlin2d` | tensor | Parity | 0.0 (origin invariant) |
| `rng.uniform` | tensor | Existence | — |
| `tensor.create` | tensor | Existence | — |
| `tensor.matmul` | tensor | Vector parity | `[3,7,2,5]` (I×A = A) |
| `compute.capabilities` | compute | Existence | — |
| `health.readiness` | security | Existence | — |

---

## Part 2: Composition Patterns That Work

These patterns are validated by 100 experiments (790+ tests) and the guideStone
binary. Sibling springs should adopt them directly.

### Pattern 1: `CompositionContext` for all IPC

```rust
let mut ctx = CompositionContext::from_live_discovery_with_fallback();
let alive = validate_liveness(&mut ctx, &mut v, &["tensor", "compute"]);
if alive == 0 { std::process::exit(v.exit_code_skip_aware()); }
```

Discovery tries XDG Unix sockets first, falls back to TCP. No hardcoded
primal names or socket paths. `from_live_discovery_with_fallback()` is the
only entry point springs should use.

### Pattern 2: Capability-based routing

```rust
let cap = composition::method_to_capability_domain("stats.mean"); // → "tensor"
let primal = composition::capability_to_primal("tensor"); // → "barracuda"
ctx.call(cap, "stats.mean", params)?;
```

Never route by primal name. Route by capability domain. This decouples the
guideStone from the specific primal providing the service — if barraCuda is
replaced by a faster tensor primal, the guideStone works unchanged.

### Pattern 3: Flexible scalar extraction

barraCuda methods return varying JSON envelopes (`{"result": N}`, `{"value": N}`,
bare `N`, `{"data": [N]}`). Our `extract_any_scalar()` helper tries all shapes.

**Recommendation to barraCuda:** Standardize on `{"result": N}` for all scalar
returns. This would eliminate the helper entirely.

### Pattern 4: Exit code convention

| Exit | Meaning |
|------|---------|
| 0 | All checks passed — NUCLEUS certified |
| 1 | At least one check failed |
| 2 | No NUCLEUS deployed — bare properties passed |

`validate_all` meta-runner understands exit 2 as "skip" (not failure). This
lets CI pass even without live primals.

### Pattern 5: Tolerance hierarchy

```
DETERMINISTIC_FLOAT_TOL < BARE_RECOMPUTE_TOL < IPC_ROUND_TRIP_TOL ≤ WGSL_SHADER_TOL
        (0)              (1024 × ε ≈ 2e-13)       (1e-10)              (1e-6)
```

Bare mode uses `BARE_RECOMPUTE_TOL` (covers FMA reordering, no serialization).
IPC mode uses `IPC_ROUND_TRIP_TOL` (covers JSON f64 round-trip). GPU mode uses
`WGSL_SHADER_TOL` (covers f32 precision loss). All from `primalspring::tolerances`.

### Pattern 6: `validate_parity_vec` for multi-element results

```rust
composition::validate_parity_vec(
    &mut ctx, &mut v,
    "tensor_matmul_identity", "tensor", "tensor.matmul",
    json!({"a": [[1,0],[0,1]], "b": [[3,7],[2,5]], ...}),
    "result", &[3.0, 7.0, 2.0, 5.0], tol,
);
```

Use `validate_parity` for scalars, `validate_parity_vec` for arrays.

---

## Part 3: Primal Gaps and Evolution Requests

### For barraCuda

| Issue | Severity | Impact | Recommendation |
|-------|----------|--------|----------------|
| Response schema inconsistency | HIGH | All springs need `extract_any_scalar()` workaround | Standardize: `{"result": N}` for scalars, `{"result": [...]}` for vectors |
| `activation.fitts` formula variant | HIGH | Returns 800 for (d=256,w=32); Python expects 708.85 | Use Shannon formulation: `log₂(2D/W + 1)`, not `log₂(D/W)` |
| `activation.hick` formula variant | HIGH | Returns 675.49 for (n=8); Python expects 650 | Use `log₂(N)`, not `log₂(N+1)` for consistency with Hick (1952) |
| `noise.perlin3d` lattice invariant | MEDIUM | `perlin3d(0,0,0)` returns -0.11 instead of 0 | Gradient noise at integer lattice points must be 0 by definition |
| `math.flow.evaluate` not exposed | LOW | Composable from sigmoid + clamp | Wire as convenience method or document composition recipe |
| `math.engagement.composite` not exposed | LOW | Composable from stats.weighted_mean + tensor ops | Same: wire or document |

### For rhizoCrypt

| Issue | Severity | Impact |
|-------|----------|--------|
| TCP-only transport (no UDS) | CRITICAL | Blocks 4 composition experiments (exp094, 095, 096, 098) |

UDS is the standard ecosystem transport. rhizoCrypt is the last primal without
it. Adding `--unix` or `XDG_RUNTIME_DIR` socket support would unblock ~9 checks.

### For loamSpine

| Issue | Severity | Impact |
|-------|----------|--------|
| Startup panic (`block_on` inside async runtime) | CRITICAL | Blocks exp095 |

`infant_discovery.rs:233` nests `block_on` in an existing Tokio runtime.
Fix: use `spawn_blocking` or restructure discovery to be async-native.

### For biomeOS

| Issue | Severity | Impact |
|-------|----------|--------|
| Running primals not auto-registered with Neural API | HIGH | -14 checks (exp087, 088) |
| `ludospring_guidestone` not in deploy graph | MEDIUM | Can't self-validate as part of NUCLEUS |

When biomeOS deploys a NUCLEUS graph, all primals should auto-register their
capabilities. Currently, only manually-registered capabilities are routable.

### For toadStool / coralReef

| Issue | Severity | Impact |
|-------|----------|--------|
| Inter-primal discovery gap | MEDIUM | toadStool can't find coralReef even when socket exists |

toadStool reports "coralReef not available" despite active coralReef socket.
Likely a discovery protocol mismatch — toadStool may not be probing the right
capability strings.

---

## Part 4: Composition Score

### Experiment composition results (95/141)

| Track | Experiments | Pass | Total | Key finding |
|-------|------------|------|-------|-------------|
| Gap Discovery (T26) | exp084-088 | 34 | 51 | barraCuda math works; Neural API registration gap |
| Science via Composition (T27) | exp089-093 | 38 | 43 | 3 experiments fully pass; Fitts/Hick formula mismatch |
| NUCLEUS Game Engine (T28) | exp094-098 | 23 | 42 | Population dynamics fully pass; rhizoCrypt UDS blocks rest |
| Composition Validation (T29) | exp099 | 13 | 13 | **Rust == IPC parity confirmed** |

**Projected with all primal fixes: ~143/154 (92.9%)**

### guideStone readiness ladder

| Level | Status | Evidence |
|-------|--------|----------|
| 0 — not started | DONE | — |
| 1 — validation exists | DONE | `validate_primal_proof` (V44, raw IPC) |
| 2 — properties documented | DONE | 5 certified properties in binary doc comments |
| **3 — bare guideStone works** | **DONE** | 15 bare checks pass without primals, exit 2 |
| 4 — NUCLEUS guideStone works | NEXT | Requires live barraCuda to validate Layer 2 |
| 5 — certified | TARGET | Requires all Layer 2 checks passing against live NUCLEUS |

---

## Part 5: What Sibling Springs Should Do

### Step-by-step guide (ludoSpring as template)

1. **Add `primalspring` as optional path dep:**
   ```toml
   primalspring = { path = "../../primalSpring/ecoPrimal", optional = true }
   [features]
   guidestone = ["dep:primalspring"]
   ```

2. **Create `{spring}_guidestone.rs`:**
   - Layer 0: Bare properties — recompute every golden value, verify
     tolerances, check traceability, prove self-verification
   - Layer 1: Discovery via `CompositionContext::from_live_discovery_with_fallback()`
   - Layer 2: Domain science via `validate_parity`, `validate_parity_vec`,
     `check_method_exists`

3. **Wire into `validate_all` meta-runner** with `skip_on_exit_2: true`

4. **Update CI:** `cargo build --features guidestone`

5. **Update downstream manifest:**
   - `guidestone_readiness` = current level
   - `validation_capabilities` = list of IPC methods your guideStone validates

6. **Hand back gaps:** Document primal gaps in `docs/PRIMAL_GAPS.md` and
   handoff to `wateringHole/handoffs/`

### Key learnings for springs

- **Start with bare mode.** Don't wait for live primals. Validate your golden
  values locally first — this catches constant drift and formula errors before
  any IPC is involved.

- **Use `validate_parity`, not raw socket calls.** The composition API handles
  discovery, capability routing, and error classification. Raw `UnixStream`
  calls (like V44's `validate_primal_proof`) are useful for debugging but
  should not be the guideStone's primary path.

- **`extract_any_scalar` is a workaround.** The canonical path is
  `validate_parity(ctx, v, name, cap, method, params, "result", expected, tol)`.
  When barraCuda standardizes response schemas, the helper becomes unnecessary.

- **Exit 2 is not failure.** Bare mode returning exit 2 is correct — it means
  the guideStone validated everything it could without live primals. CI should
  not fail on exit 2.

---

## Part 6: NUCLEUS Deployment via Neural API from biomeOS

### Current model

```
plasmidBin ecoBin → biomeOS deploys → NUCLEUS graph runs
    ↓
primalspring_guidestone → certifies composition is sound
    ↓
ludospring_guidestone → certifies domain science is faithful
    ↓
NUCLEUS is self-validating
```

### What biomeOS needs to evolve

1. **guideStone as deploy graph node:** The guideStone binary should be a node
   in the NUCLEUS deploy graph. When the graph starts, the guideStone runs first,
   and the NUCLEUS only goes live if it passes.

2. **Auto-capability registration:** When a primal starts via biomeOS, its
   capabilities should auto-register with the Neural API. Currently springs
   must explicitly call `lifecycle.register` + `capability.register`.

3. **Health probes include guideStone:** `health.readiness` should reflect
   whether the domain guideStone has passed (not just whether the process is up).

### Neural API patterns that work

- `capability.call` routes to the correct primal transparently
- `lifecycle.register` / `capability.register` handshake is clean
- `health.liveness` is fast (<1ms) and reliable
- Discovery via Songbird `discovery.peers` works for multi-primal topologies

### Neural API patterns that need evolution

- Capability auto-registration (see §3 biomeOS gap)
- Graph-level health aggregation (all nodes healthy → graph healthy)
- guideStone result as a capability itself (`validation.guidestone.status`)

---

## Part 7: Files Changed Across All Repos

### ludoSpring

| File | Change |
|------|--------|
| `barracuda/src/bin/ludospring_guidestone.rs` | Three-layer architecture: bare (15) + discovery (2) + domain (15) |
| `barracuda/src/bin/validate_all.rs` | Includes `ludospring_guidestone` |
| `barracuda/Cargo.toml` | `guidestone` feature, `primalspring` dep |
| `.github/workflows/ci.yml` | `cargo build --features guidestone` |
| `README.md` | V45 readiness 3 |
| `CHANGELOG.md` | V45 readiness 3 entry |
| `CONTEXT.md` | V45 readiness 3 |
| `docs/PRIMAL_GAPS.md` | GAP-02 readiness 3, expanded IPC list |
| `whitePaper/baseCamp/README.md` | Readiness 3, date fix |
| `experiments/README.md` | Readiness 3, date fix |
| `wateringHole/README.md` | V45 active, V43/V44 archived |
| `wateringHole/handoffs/LUDOSPRING_V45_GUIDESTONE_HANDOFF_APR18_2026.md` | Readiness 3 throughout |
| `wateringHole/handoffs/archive/` | V43, V44 handoffs archived |

### primalSpring

| File | Change |
|------|--------|
| `graphs/downstream/downstream_manifest.toml` | `guidestone_readiness = 3`, +`stats.variance`, +`compute.capabilities` |
| `wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` | Readiness 3, 15 bare + 15 IPC |

### infra/wateringHole

| File | Change |
|------|--------|
| `PRIMAL_REGISTRY.md` | ludoSpring readiness 3, 15 bare + 15 IPC |
| `ECOSYSTEM_EVOLUTION_CYCLE.md` | ludoSpring readiness 3 |
| `handoffs/LUDOSPRING_V45_GUIDESTONE_EVOLUTION_HANDOFF_APR18_2026.md` | **This document** |

---

## Score Summary

| Metric | Value |
|--------|-------|
| Tests | 790+ |
| Experiments | 100 |
| Validators | 7 (3 core + composition + primal_proof + guidestone + meta-runner) |
| guideStone readiness | **3** (bare passes, NUCLEUS ready) |
| Bare checks | 15 (5 certified properties) |
| Domain IPC checks | 15 (13 barraCuda methods) |
| Composition score | 95/141 (67.4%) — projected 143/154 (92.9%) with primal fixes |
| Primal gaps | 10 (GAP-01–GAP-10) |
| Clippy | 0 warnings |
| Coverage | 90%+ |

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
