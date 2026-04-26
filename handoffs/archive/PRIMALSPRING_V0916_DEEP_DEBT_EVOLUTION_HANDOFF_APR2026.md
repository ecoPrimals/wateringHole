# primalSpring v0.9.16+ — Deep Debt Evolution Handoff

**Date**: April 2026
**From**: primalSpring v0.9.16 (Phase 44)
**For**: All primal teams + downstream spring teams
**Status**: Stadial gate cleared, deep debt eliminated, ready for downstream absorption

---

## What Changed

### Capability-Based Discovery (zero hardcoded primal names)

All 11 core production modules now reference `primal_names::` constants instead of
inline string literals. The TCP fallback port table in `composition/mod.rs` is
centralized via `tcp_fallback_table()` referencing `tolerances::TCP_FALLBACK_*`
constants. No magic numbers remain in composition discovery logic.

**Pattern for primals to absorb**: If your primal references other primals by name,
centralize those references in a single canonical module (like `primal_names.rs`).
Discovery should be capability-first — call by what you need, not by who provides it.

**Files changed**: `composition/mod.rs`, `niche.rs`, `launcher/biomeos.rs`,
`launcher/spawn.rs`, `launcher/discovery.rs`, `ipc/discover.rs`, `ipc/capability.rs`,
`ipc/neural_bridge.rs`, `tolerances/mod.rs`

### Smart File Refactoring (all production files under 800 LOC)

- `harness/mod.rs`: 874 → 623 LOC (test suite → `harness/tests.rs`)
- `bonding/mod.rs`: 860 → 464 LOC (test suite → `bonding/tests.rs`)
- `composition/mod.rs`: previously extracted in stadial gate (1098 → 688 LOC)

**Pattern**: Extract `#[cfg(test)] mod tests` to `#[cfg(test)] #[path = "tests.rs"] mod tests;`
with a companion file. Tests live next to their module, share `use super::*`,
compile identically.

### Dependency Hygiene

- `blake3`: Confirmed pure Rust SIMD, no C build path in current features
- `exp094`: Unified `serde_json` from standalone `"1"` to `workspace = true`
- `trio_ops`: Version bumped from 0.9.15 → 0.9.16
- All deps confirmed ecoBin compliant (pure Rust, zero C in application layer)

### Incomplete Implementation Evolution

- `handle_bonding_status`: Evolved from placeholder stub ("not yet implemented")
  to proper typed empty response with structured fields
- `generate_harness_nuclear`: Documented as intentional harness-only behavior
  (placeholder proof when BearDog is absent during local tests)

---

## Stadial Compliance Summary

| Metric | Status |
|--------|--------|
| `#![forbid(unsafe_code)]` | Enforced at crate root |
| `#[allow()]` in production | Zero (one justified `#![allow()]` in `experiments/trio_ops`) |
| `dyn` dispatch | 2 justified instances (`ValidationSink`, `Error::source()`) |
| `async-trait` crate | Zero |
| TODO/FIXME/HACK in production | Zero |
| Files > 800 LOC | Zero (max is `composition/mod.rs` at 688) |
| Clippy warnings (pedantic+nursery) | Zero |
| `cargo fmt` drift | Zero |
| Tests | 601 passed, 0 failed |
| Hardcoded primal names in production | Zero (all via `primal_names::` constants) |
| Hardcoded port literals in production | Zero (all via `tolerances::` or env vars) |
| Production mocks | Zero (all isolated to `#[cfg(test)]`) |
| Cross-primal crate imports | Zero (all coordination via IPC) |

---

## What Primals Should Absorb

### 1. Capability-First Discovery Pattern

```rust
// Before: hardcoded primal name
let socket = base_dir.join("biomeos").join("my-socket.sock");

// After: constant from canonical module
let socket = base_dir.join(primal_names::BIOMEOS).join("my-socket.sock");
```

If your primal has a routing table or discovery logic that maps capabilities to
primal names, centralize it. primalSpring's `capability_to_primal()` and
`method_to_capability_domain()` are the ecosystem-wide source of truth.

### 2. TCP Fallback Table Pattern

For cross-gate/LAN/container deployments where UDS isn't available:
- Try UDS discovery first (`connect_by_capability`)
- Fall back to `{PRIMAL}_PORT` env var
- Fall back to centralized constant from `tolerances::`

### 3. Test Extraction Pattern

When a module exceeds 600 LOC with its tests, extract tests to a companion file:

```rust
// In mod.rs — replaces inline #[cfg(test)] mod tests { ... }
#[cfg(test)]
#[path = "tests.rs"]
mod tests;
```

### 4. ROUTED_CAPABILITIES as Const Block

primalSpring's `niche.rs` now uses a `const { }` block to reference `primal_names`
constants in a `&[(&str, &str)]` static slice. This avoids runtime allocation
while keeping primal identity centralized.

---

## What Springs Should Know

### Composition Context

`CompositionContext::from_live_discovery_with_fallback()` now uses the centralized
TCP fallback table. Springs that were manually constructing TCP connections should
migrate to this method for consistent behavior across UDS/TCP/container deployments.

### guideStone Readiness

primalSpring guideStone is **Level 4** — 67/67 live NUCLEUS checks pass,
41/41 bare checks pass, BLAKE3 checksums (P3 self-verifying). All 13 cross-spring
gaps are RESOLVED. Downstream springs with guideStone readiness < 4 should now
have clear paths to Level 5 (primal proof validation).

### plasmidBin Depot

`start_primal.sh` now has explicit case blocks for all 14 primals including
`barracuda`, `coralreef`, and `skunkbat`. Springs deploying via plasmidBin
should use this script for consistent primal startup.

---

## Composition Patterns for NUCLEUS Deployment via neuralAPI

### Deploy Pattern (biomeOS Neural API)

```bash
biomeos deploy --graph graphs/profiles/nucleus_complete.toml --family-id "my-family"
```

biomeOS reads the graph TOML, resolves fragments via `resolve = true`, spawns
primals in topological order, and registers capabilities. Springs connect via
`CompositionContext::from_live_discovery()` and call by capability.

### Validation Pattern (Spring → NUCLEUS)

```rust
let mut ctx = CompositionContext::from_live_discovery_with_fallback();
let mut v = ValidationResult::new("primal-proof");

let alive = validate_liveness(&mut ctx, &["tensor", "security", "storage"], &mut v);
if alive == 0 { std::process::exit(2); }

validate_parity(&mut ctx, "tensor", "tensor.matmul", &expected, tolerance, &mut v);
```

### Three-Tier Validation

- **Tier 1 (LOCAL)**: Spring's local Rust code, always green in CI
- **Tier 2 (IPC-WIRED)**: Live primal calls with `check_skip()` for absent primals
- **Tier 3 (FULL NUCLEUS)**: Proto-nucleate deployed, spring validates externally

---

## Known Remaining Gaps

No open gaps in primalSpring production code. Remaining items are ecosystem-wide:
- HSM hardware validation (exp096 check 15/15 — requires physical HSM)
- benchScale full lab deployment (topology validated, awaiting cross-platform testing)

See `docs/PRIMAL_GAPS.md` for the full resolved gap history.
