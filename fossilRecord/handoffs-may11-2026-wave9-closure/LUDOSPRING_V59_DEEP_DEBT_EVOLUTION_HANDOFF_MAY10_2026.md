# ludoSpring V59 — Deep Debt Resolution & Evolution Patterns Handoff

**Date:** May 10, 2026
**Spring:** ludoSpring V59.1
**Audience:** primalSpring, all springs, barraCuda, biomeOS, primal teams
**Quality:** 815+ tests, zero clippy, zero bare `#[allow]`, zero TODO/FIXME, zero unsafe

---

## Executive Summary

ludoSpring completed its post-interstadial deep debt resolution: Tier 4 IPC-first rewiring,
`crate::math` dual-path dispatch, python_parity refactoring, biomeOS v3.51 absorption,
skunkBat wiring, and all upstream blocker closures. This handoff documents **patterns
learned**, **remaining evolution targets**, and **guidance for ecosystem adoption**.

---

## Part 1: Patterns for Ecosystem Adoption

### 1.1 Tier 4 Dual-Path Math Module

The `crate::math` pattern lets a spring compile without barraCuda library linkage while
maintaining identical numerical behavior. When `local` feature is enabled, functions delegate
to barraCuda. When disabled, pure-Rust inline fallbacks provide the same result.

**Key lesson:** The inline fallback must use the **exact same constants and bit-extraction**
as barraCuda's implementation. ludoSpring initially used Knuth MMIX LCG constants for the
fallback while barraCuda used a different increment — this caused a parity failure caught
by the `tier4_math_parity` validation scenario. Always inspect the upstream source.

**Cargo.toml pattern:**

```toml
[features]
default = ["ipc", "local"]
local = ["dep:barracuda"]
ipc = ["dep:clap", ...]

[dependencies]
barracuda = { path = "...", optional = true }
```

**Code pattern:**

```rust
pub fn sigmoid(x: f64) -> f64 {
    #[cfg(feature = "local")]
    { barracuda::activations::sigmoid(x) }
    #[cfg(not(feature = "local"))]
    { 1.0 / (1.0 + (-x).exp()) }
}
```

### 1.2 biomeOS v3.51 Integration

Two new endpoints absorbed:

- **`composition.status`** → `{ active_users, primal_health, resource_pressure }`
  Wire into health/monitoring paths. Non-fatal if biomeOS unavailable.

- **`method.register`** → Dynamic registration of spring-specific methods at startup.
  Eliminates manual biomeOS config for spring capabilities.

Both use `NeuralBridge::call_raw(method, &params)` for generic JSON-RPC forwarding.
Any spring with an existing `NeuralBridge` or `IpcClient` can add this in one function.

### 1.3 skunkBat Deploy Graph Wiring

Add a `skunkbat` node to deploy graphs with `by_capability = "defense"` and
`required = false`. Forwards audit events to rhizoCrypt DAG + sweetGrass braid.
When JH-5 Phase 3 ships, cross-primal audit trails are automatic.

```toml
[[nodes]]
id = "skunkbat"
depends_on = ["beardog", "songbird"]
by_capability = "defense"
required = false
capabilities = ["baseline.observe", "baseline.anomaly", "security.audit_log"]
```

### 1.4 Large Test File Refactoring Pattern

ludoSpring's `python_parity.rs` (872 lines) was split into a directory-based test module:

```
tests/python_parity/
├── main.rs           # mod declarations + workspace #![allow]
├── interaction.rs    # Fitts, Hick, Steering, Doom
├── noise.rs          # Perlin 2D/3D, fBm
├── procedural.rs     # GOMS, L-systems, turtle, BSP
└── metrics.rs        # Four Keys, Flow, DDA
```

The pattern: `tests/foo.rs` → `tests/foo/main.rs` + submodules. Cargo discovers the
test binary from the directory name matching the original file name. No `[[test]]` config
needed. Each submodule is focused, searchable, and under 250 lines.

### 1.5 Bare `#[allow]` Elimination

Every `#[allow(...)]` in the codebase now includes `reason = "..."`. In test modules,
the pattern is:

```rust
#![allow(
    clippy::unwrap_used,
    clippy::expect_used,
    reason = "test assertions use unwrap/expect for clarity"
)]
```

For production code, prefer `#[expect(..., reason = "...")]` which fails if the lint
no longer fires (guarantees the suppression is still needed).

---

## Part 2: Composition Parity Status

| Metric | Value |
|--------|-------|
| Composition checks | 130/141 (92.2%) |
| Fully PASS experiments | 9 |
| `game.*` methods canonical | 28 (ecosystem total 413) |
| Capabilities across primals | 30 across 11 |
| Validation scenarios | 6 (absorbed into UniBin) |
| guideStone | L4 (54/54 checks, v1.2.0) |

### Remaining 11 Failing Checks

| Check | Owner | Severity | Notes |
|-------|-------|----------|-------|
| PG-47: perlin3d lattice + stats.entropy | **barraCuda** | Low | 5 checks blocked |
| PG-48: petalTongue threading | **petalTongue** | Low | 3 checks blocked |
| Squirrel inference routing | **Squirrel** | Low | 1 check (inference.complete live) |
| Content ownership edge cases | **ludoSpring** | Low | 2 checks (E2E provenance replay) |

---

## Part 3: Remaining Evolution Targets

| Target | Priority | Blocker | Notes |
|--------|----------|---------|-------|
| guideStone L5 → L6 (NUCLEUS deployment validation) | Medium | Live plasmidBin environment | Tier 4 rewiring is prerequisite — done |
| Re-validate exp084-098 against updated plasmidBin | Medium | plasmidBin refresh | 46 experiments pending live validation |
| GPU benchmark suite (Kokkos/Galaxy-style) | Low | barraCuda GPU path maturity | When GPU dispatch via toadStool stabilizes |
| Paper absorption (Bartle 1996, MDA 2004, Schell 2008) | Low | None | Design validation experiments for game design theory |
| Dataset integration (Steam telemetry, BGG metrics) | Low | Cross-domain tooling | When data pipelines stabilize |
| projectNUCLEUS workload spec | Low | None | Create `workloads/ludospring/` TOML |
| Python baselines → notebook form | Low | None | Functional parity exists in scripts |

---

## Part 4: Notes for Primal Teams

### For primalSpring

- **Canonical registry:** 413 methods (28 `game.*`). ludoSpring cross-sync test validates
  bidirectionally. Pattern available for all springs.
- **Tier 4 reference:** ludoSpring is the first spring with optional barraCuda. The
  `crate::math` dual-path pattern is the proposed ecosystem standard.
- **GAP-12 closed:** 18 → 28 `game.*` methods. All 28 match niche.rs SSOT.

### For barraCuda

- **`optional = true`:** ludoSpring no longer forces library linkage.
- **LCG parity issue documented:** Springs implementing inline fallbacks must match
  barraCuda's exact `rng::lcg_step` constants (multiplier=6364136223846793005,
  increment=1) and `state_to_f64` bit extraction (`>> 33`, divided by `u32::MAX`).
  Consider exposing these constants as `pub const` for cross-crate use.
- **PG-47 open:** `stats::perlin3d` + `stats::entropy` — 5 ludoSpring checks blocked.
- **CPU parity benchmarks:** `baselines/python/bench_cpu_parity.py` covers Perlin,
  fBm, raycaster, Fitts. Results: Rust is 15-50x faster on all benchmarks.

### For biomeOS

- **v3.51 absorption complete:** `composition.status` + `method.register` wired.
- **28 methods ready** for dynamic registration via `method.register` on startup.
- **Cell graph:** `ludospring_cell.toml` with skunkBat node for audit logging.

### For rhizoCrypt

- **GAP-06 confirmed RESOLVED** — full provenance pipeline operational via UDS.
- **Deploy graphs updated** to depend on rhizoCrypt via skunkBat forwarding chain.

### For sibling springs

- **Tier 4 rewiring pattern** is documented and tested — adopt for IPC-first builds.
- **`crate::math` module** provides the reference implementation for dual-path dispatch.
- **python_parity directory split** pattern for large test files.
- **biomeOS v3.51 integration** is one function call per endpoint.
- **Deploy graph skunkBat wiring** is copy-paste from ludoSpring templates.

---

## Quality Gate

```
cargo build                                              ✓ (default: ipc + local)
cargo build --no-default-features --features ipc         ✓ (IPC-only sovereign)
cargo fmt --check                                        ✓ (zero diffs)
cargo clippy --workspace --all-targets                   ✓ (zero warnings)
cargo test --workspace --lib --tests                     ✓ (815+ tests, 0 failures)
```
