# SPDX-License-Identifier: AGPL-3.0-or-later

# ludoSpring V46 — Deep Audit & Composition Handoff

**Date:** April 20, 2026
**From:** ludoSpring
**To:** All primal teams, all spring teams, biomeOS, esotericWebb
**Version:** V46 (791 tests, guideStone readiness 4, plasmidBin v0.10.0)
**Companion:** `LUDOSPRING_V46_THREE_TIER_NUCLEUS_EVOLUTION_HANDOFF_APR20_2026.md`

---

## Executive Summary

ludoSpring V46 is at **guideStone readiness 4** — the first domain spring to
reach NUCLEUS-validated three-tier validation. This deep-audit handoff covers
the complete composition picture: what we use, what works, what's broken, what
we learned, and exactly what each primal/spring team should absorb.

| Metric | Value |
|--------|-------|
| Workspace tests | 791 (0 failures, 0 clippy warnings) |
| Experiments | 100 |
| guideStone checks | 31 bare + 15 IPC + 8 NUCLEUS = **54** (with CHECKSUMS) |
| Primal gaps | 10 (GAP-01–GAP-10) |
| `#[allow]` in app code | 0 |
| `#[expect(reason)]` in app code | 60+ (curated, all with reason strings) |
| TODO/FIXME/HACK in source | 0 |
| Coverage | 90%+ (CI enforced) |

---

## Part 1: Complete Primal Usage Map

### What ludoSpring calls

| Primal | Capability | Methods Used | Where | Status |
|--------|-----------|-------------|-------|--------|
| **barraCuda** | tensor, compute | `activation.fitts`, `activation.hick`, `math.sigmoid`, `math.log2`, `stats.mean`, `stats.variance`, `stats.std_dev`, `noise.perlin2d`, `rng.uniform`, `tensor.create`, `tensor.matmul`, `compute.capabilities`, `compute.dispatch` | guideStone Tier 2, exp084–100 | Working (formula variants GAP-08) |
| **BearDog** | security | `crypto.hash` (BLAKE3) | guideStone Tier 3 | Working (resets without BTSP) |
| **NestGate** | storage | `storage.store`, `storage.retrieve` | guideStone Tier 3, game state persistence | Working |
| **toadStool** | compute | `compute.dispatch.submit`, GPU shader pipeline | 3 game WGSL shaders, raycaster, noise | Working |
| **coralReef** | shader | `shader.compile`, `shader.list` | exp085 shader dispatch chain | Partial (GAP-01) |
| **Songbird** | discovery | `discovery.peers` | Multi-primal topology | HTTP-on-UDS (SKIP) |
| **petalTongue** | visualization | `visualization.render`, scene push | Dashboard, live sessions | HTTP-on-UDS (SKIP) |
| **Squirrel** | ai | `ai.query`, `ai.analyze`, `ai.suggest` | NPC dialogue, narration | Working |
| **biomeOS** | orchestration | `lifecycle.register`, `capability.register`, `health.*` | Deploy graph, Neural API | Working (auto-reg gap) |
| **rhizoCrypt** | provenance | `dag.session.create`, `dag.event.append` | Provenance pipeline | TCP-only (GAP-06) |
| **loamSpine** | provenance | Provenance discovery | — | ~~Startup panic (GAP-07)~~ **RESOLVED** |
| **sweetGrass** | provenance | Provenance attestation | — | Blocked by GAP-06/07 |

### What ludoSpring validates in guideStone

```
Tier 1: LOCAL_CAPABILITIES (31 checks when CHECKSUMS present)
  ├── Determinism:    6 checks (Fitts, Hick, sigmoid, log2, mean, variance)
  ├── Traceability:   7 checks (every golden value finite + sourced)
  ├── Self-Verify:    2 checks (tamper detection) + 12 BLAKE3 (1 manifest + 11 files)
  ├── Environment:    2 checks (no GPU, no network)
  └── Tolerance:      3 checks (ordering, positivity, bare < IPC)

Tier 2: IPC-WIRED (15 checks, skip if primals absent)
  ├── Interaction:    2 checks (Fitts parity, Hick parity)
  ├── Math:           2 checks (sigmoid, log2)
  ├── Statistics:     3 checks (mean, variance, std_dev)
  ├── Procedural:     2 checks (perlin2d, rng.uniform)
  └── Tensor/Compute: 4 checks (create, matmul, capabilities, readiness)

Tier 3: FULL NUCLEUS (8 checks, skip if BearDog/NestGate absent)
  ├── Security:       2 checks (crypto.hash, hash length)
  ├── Storage:        3 checks (store, retrieve, roundtrip)
  └── Pipeline:       3 checks (hash→store→retrieve→verify)
```

---

## Part 2: Composition Patterns — What Works

These patterns are battle-tested across 100 experiments and the guideStone binary.

### Pattern 1: `CompositionContext` as single entry point

```rust
let mut ctx = CompositionContext::from_live_discovery_with_fallback();
```

Discovery tries XDG Unix sockets first, falls back to TCP. Never hardcode
primal names or socket paths. This is the only entry point.

### Pattern 2: Capability-based routing

```rust
let cap = composition::method_to_capability_domain("stats.mean"); // → "tensor"
ctx.call(cap, "stats.mean", params)?;
```

Never route by primal name. If barraCuda is replaced by a faster tensor primal,
the guideStone works unchanged.

### Pattern 3: `extract_any_scalar()` for response envelope tolerance

barraCuda methods return varying envelopes: `{"result": N}`, `{"value": N}`,
bare `N`, `{"data": [N]}`. Our helper tries all shapes.

**Recommendation:** barraCuda standardize on `{"result": N}` for scalars,
`{"result": [...]}` for vectors. This eliminates the helper.

### Pattern 4: Tolerance hierarchy

```
DETERMINISTIC_FLOAT_TOL < BARE_RECOMPUTE_TOL < IPC_ROUND_TRIP_TOL ≤ WGSL_SHADER_TOL
        (0)              (1024 × ε ≈ 2e-13)       (1e-10)              (1e-6)
```

Bare mode uses `BARE_RECOMPUTE_TOL` (FMA reordering, no serialization).
IPC uses `IPC_ROUND_TRIP_TOL` (JSON f64 round-trip). GPU uses `WGSL_SHADER_TOL`
(f32 precision loss). All from `primalspring::tolerances`.

### Pattern 5: `is_skip_error()` for protocol tolerance

```rust
fn is_skip_error(e: &IpcError) -> bool {
    e.is_connection_error() || e.is_protocol_error() || e.is_transport_mismatch()
}
```

Primals that speak HTTP on UDS (Songbird, petalTongue) are classified as
reachable-but-incompatible (SKIP, not FAIL). This prevents false failures
in mixed-protocol deployments.

### Pattern 6: `call_or_skip()` for chained multi-primal validation

When a pipeline step fails (e.g., BearDog unavailable), all downstream steps
skip gracefully rather than producing confusing error messages.

### Pattern 7: BLAKE3 self-verification (Property 3)

```
validation/CHECKSUMS:
  {blake3}  barracuda/src/bin/ludospring_guidestone.rs
  {blake3}  baselines/python/combined_baselines.json
  ...
```

`checksums::verify_manifest(v, "validation/CHECKSUMS")` hashes each file
and compares against the manifest. Tampered files → check failure → exit 1.
Regenerate with `b3sum <files> > validation/CHECKSUMS`.

### Pattern 8: Exit code convention

| Exit | Meaning |
|------|---------|
| 0 | All checks passed — NUCLEUS certified |
| 1 | At least one check failed |
| 2 | No NUCLEUS deployed — bare properties passed |

CI treats exit 2 as "skip" (not failure). `validate_all` meta-runner
understands this convention.

### Pattern 9: Three-tier naming convention

```
bare:*      → Tier 1 (LOCAL_CAPABILITIES)
ipc:*       → Tier 2 (IPC-WIRED)
nucleus:*   → Tier 3 (FULL NUCLEUS)
p3:*        → Property 3 BLAKE3 self-verification
```

Operators can grep guideStone output by tier.

---

## Part 3: Primal Gaps — Action Items per Team

### barraCuda team

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| GAP-02 | Direct Rust import vs IPC | N/A | Library dep retained for Level 2; guideStone uses pure IPC. No action needed. |
| GAP-08 | Fitts/Hick formula variant | HIGH | `activation.fitts` returns 800 (d=256,w=32); Python expects 708.85. Use Shannon formulation: `log₂(2D/W + 1)`, not `log₂(D/W)`. Same for Hick: use `log₂(N)`, not `log₂(N+1)`. |
| — | Response schema inconsistency | HIGH | Standardize: `{"result": N}` for scalars, `{"result": [...]}` for vectors. All springs need `extract_any_scalar()` workaround until this is fixed. |
| — | `noise.perlin3d` lattice invariant | MEDIUM | `perlin3d(0,0,0)` returns -0.11 instead of 0. Gradient noise at integer lattice points must be 0 by definition. |
| — | `math.flow.evaluate` not exposed | LOW | Composable from sigmoid + clamp. Wire as convenience method or document composition recipe. |
| — | `math.engagement.composite` not exposed | LOW | Composable from stats.weighted_mean + tensor ops. Same: wire or document. |

### rhizoCrypt team

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| GAP-06 | TCP-only transport (no UDS) | CRITICAL | Blocks provenance pipeline for all springs. Add `--unix` or `XDG_RUNTIME_DIR` socket support. |

### loamSpine team

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| GAP-07 | Startup panic (`block_on` inside async runtime) | CRITICAL | **RESOLVED** (v0.9.16, April 20 2026): mDNS discovery moved from `spawn_blocking` to isolated `std::thread::spawn` + `tokio::sync::oneshot`. `async-std` no longer sees tokio's thread-local Handle. |

### BearDog team

| Issue | Severity | Action |
|-------|----------|--------|
| Connection reset without BTSP | LOW | Expected behavior. guideStone uses `call_or_skip` to handle gracefully. Document in BTSP spec. |

### Songbird / petalTongue teams

| Issue | Severity | Action |
|-------|----------|--------|
| HTTP framing on UDS | LOW | Handled via `is_protocol_error()` / `is_transport_mismatch()` → SKIP. Consider native JSON-RPC on UDS. |

### biomeOS team

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| — | Running primals not auto-registered with Neural API | HIGH | When biomeOS deploys NUCLEUS, all primal capabilities should auto-register. Currently requires manual `lifecycle.register` + `capability.register`. |
| GAP-10 | `ludospring_guidestone` not in deploy graph | MEDIUM | guideStone should be a deploy graph node. NUCLEUS goes live only after guideStone passes. |
| — | No `game.*` graph node identity | MEDIUM | Discovery resolves tensor/storage but not `game.*` routing to ludoSpring. Add a node or manifest rule. |
| — | Error contract undocumented | LOW | Springs can't distinguish "routed but primal failed" vs "Neural API down". Version error shapes. |

### coralReef team

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| GAP-01 | IPC client not wired in product paths | MEDIUM | Typed client exists; production GPU paths still use `include_str!` + toadStool. Low priority until shader hot-reload is needed. |

### toadStool team

| Issue | Severity | Action |
|-------|----------|--------|
| Naming inconsistency | LOW | Deploy graph uses `toadstool.health` but wire protocol uses `compute.health`. Align. |

### NestGate team

| Issue | Severity | Action |
|-------|----------|--------|
| Unused API surface | LOW | `exists`, `list`, `metadata`, `delete` implemented but not exposed as `game.*` capabilities. Expose or trim. |

### Squirrel team

| Issue | Severity | Action |
|-------|----------|--------|
| Incomplete inference surface | LOW | `InferenceCompleteRequest` etc. defined but no `inference.*` wrappers wired. Expose or document as internal-only. |

---

## Part 4: NUCLEUS Deployment via Neural API from biomeOS

### Current model

```
plasmidBin ecoBin (14 musl-static binaries)
    ↓
biomeOS deploys NUCLEUS graph
    ↓
primalspring_guidestone → certifies composition (67/67)
    ↓
ludospring_guidestone → certifies game science (31+15+8 = 54 checks)
    ↓
NUCLEUS is self-validating
```

### What biomeOS needs to evolve

1. **guideStone as deploy graph node:** Run guideStone first; NUCLEUS goes
   live only if it passes (exit 0).

2. **Auto-capability registration:** When a primal starts, its capabilities
   should auto-register with Neural API. Currently manual.

3. **Health probes include guideStone:** `health.readiness` should reflect
   domain guideStone status, not just process liveness.

4. **`game.*` routing:** Neural API needs a rule mapping `game.*` methods
   to the ludoSpring process. Currently only tensor/storage are routable.

### Neural API patterns that work

- `capability.call` routes to correct primal transparently
- `lifecycle.register` / `capability.register` handshake is clean
- `health.liveness` is fast (<1ms)
- `discovery.peers` (Songbird) works for multi-primal topology

### Neural API patterns that need evolution

- Capability auto-registration on deploy
- Graph-level health aggregation (all nodes healthy → graph healthy)
- guideStone result as a capability: `validation.guidestone.status`

---

## Part 5: What Sibling Springs Should Absorb

### Step-by-step guide

1. **Tier 1 (LOCAL_CAPABILITIES):** Recompute every golden value from
   published formulas. No primals needed. Generate `validation/CHECKSUMS`
   with `b3sum`. This catches constant drift immediately.

2. **Tier 2 (IPC-WIRED):** Use `CompositionContext::from_live_discovery_with_fallback()`
   and `validate_parity` / `validate_parity_vec` for domain IPC.
   Use `check_skip()` when primals are absent.

3. **Tier 3 (FULL NUCLEUS):** Deploy from plasmidBin. Validate cross-atomic
   patterns. Use `call_or_skip` for chained calls. Use `is_skip_error`.

4. **Generate CHECKSUMS:** `b3sum <critical-files> > validation/CHECKSUMS`

5. **Wire CI:** `cargo build --features guidestone`

6. **Update manifest:** `guidestone_readiness` in `downstream_manifest.toml`

7. **Hand back gaps:** `docs/PRIMAL_GAPS.md`

### Key learnings

- **Start with bare mode.** Don't wait for primals. Validate golden values
  locally. This catches formula drift before IPC is involved.

- **Use `validate_parity`, not raw sockets.** The composition API handles
  discovery, routing, and error classification. Raw `UnixStream` calls
  (like V44's `validate_primal_proof`) are for debugging only.

- **Exit 2 is not failure.** Bare mode returning exit 2 is correct. CI
  should not fail on exit 2.

- **Tolerance hierarchy matters.** Bare recomputation tolerance must be
  tighter than IPC tolerance which must be tighter than GPU tolerance.

- **Protocol tolerance prevents false failures.** Primals that speak HTTP
  on UDS are common. Classify as SKIP, not FAIL.

---

## Part 6: Code Quality Audit Results

### Zero counts confirmed

| Check | Count |
|-------|-------|
| TODO/FIXME/HACK in .rs source | 0 |
| `#[allow()]` in application code | 0 |
| Hardcoded primal names | 0 |
| Hardcoded socket paths | 0 |
| `unsafe` blocks | 0 (`#![forbid(unsafe_code)]` everywhere) |
| Clippy warnings (workspace-wide) | 0 |
| Failing tests | 0 |

### `#[allow]` audit

All 33 `#[allow(clippy::unwrap_used, clippy::expect_used)]` occurrences are
on `#[cfg(test)] mod tests` blocks. This is the standard pattern for test
modules — `unwrap`/`expect` are acceptable in tests for panic-on-failure.

Application code uses `#[expect(lint, reason = "...")]` exclusively (60+ sites).
Each has a curated reason string per interstadial standard.

### Debris audit

| Item | Status |
|------|--------|
| `baselines/python/__pycache__/` | In `.gitignore`, not tracked. Local artifact. |
| `barracuda/examples/` | Empty dir, not tracked (git ignores empty dirs). |
| `.bak`, `.old`, `.orig`, `.tmp` files | None found. |
| `.DS_Store` | None found. |
| Stale scripts | None found. |
| Stale handoffs | All superseded handoffs in `wateringHole/handoffs/archive/`. |

---

## Part 7: Readiness Ladder

| Level | Status | Evidence |
|-------|--------|----------|
| 0 — not started | DONE | — |
| 1 — validation exists | DONE | `validate_primal_proof` (V44, raw IPC) |
| 2 — properties documented | DONE | 5 certified properties in binary doc comments |
| 3 — bare guideStone works | DONE | 20 bare checks pass, exit 2 |
| **4 — NUCLEUS guideStone works** | **DONE** | 31 bare + 15 IPC + 8 NUCLEUS = 54 checks |
| 5 — certified | NEXT | Requires all Tier 2 + Tier 3 passing against live NUCLEUS |
| 6 — NUCLEUS deploys in-graph | TARGET | guideStone as deploy graph node |

---

**The water flows downhill. Gaps evaporate uphill. The ecosystem evolves.**
