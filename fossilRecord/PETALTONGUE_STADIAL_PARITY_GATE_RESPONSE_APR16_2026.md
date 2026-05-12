# petalTongue — Stadial Parity Gate Response

**Date**: April 16, 2026
**Version**: 1.6.6
**Responding to**: `STADIAL_PARITY_GATE_APR16_2026.md`
**Status**: **INTERSTADIAL-READY** — all gate criteria satisfied

---

## Gate Criteria Resolution

### 1. async-trait + dyn Dispatch Elimination — CLEAR

| Metric | Value |
|--------|-------|
| `async-trait` in Cargo.toml | **0** (removed in Sprint 8) |
| `#[async_trait]` attributes | **0** (47→0 in Sprint 8) |
| `Box<dyn CustomTrait>` / `Arc<dyn CustomTrait>` | **0** (all replaced with enum dispatch) |
| `Pin<Box<dyn Future>>` | **0** (all converted to native async) |
| Custom `dyn` trait objects | **0** |

**Remaining `dyn` (irreducible, gate-compliant):**

| Usage | Count | Why irreducible |
|-------|-------|-----------------|
| `Box<dyn Fn(...)>` | 2 | Rust requires `dyn` for type-erased closures |
| `&dyn std::error::Error` | 2 | Standard library trait interface |
| `Box<dyn std::error::Error + Send + Sync>` | 2 | Axum/hyper handler error boundary |
| Doc comments / lint annotations | 17 | Not code — references to replaced patterns |
| **Total** | **23** | 6 production, all non-trait-object |

### 2. Lockfile Ghost Debt — RESOLVED (ring is phantom)

**`ring` in Cargo.lock**: Present but **never compiled**.

Dependency chain:
```
reqwest (optional: hyper-rustls) → rustls → rustls-webpki → ring
```

Evidence:
- `cargo tree -i ring` → "nothing to print"
- `cargo tree -i hyper-rustls` → "nothing to print"
- `cargo tree -i rustls` → "nothing to print"
- The entire chain is an optional dependency of reqwest (TLS backend)
- petalTongue configures reqwest with `default-features = false`, no TLS features

**Why it can't be removed from Cargo.lock**: Cargo's resolver includes optional
dependency resolutions in the lockfile for version stability. This is Cargo behavior,
not a dependency choice. The lockfile entry does not represent compiled code.

**reqwest**: Upgraded from 0.12 → 0.13. Production dependency (not dev-only).
Used for local ecosystem HTTP/SSE communication (biomeOS API, discovery, entropy).
Configured with: `default-features = false, features = ["json", "charset", "http2", "stream"]`.
No TLS, no ring, no aws-lc-rs in the compiled binary.

### 3. Edition 2024 + deny.toml — CLEAR

- Edition: `2024`
- Rust version: `1.87`
- `deny.toml`: Present and enforced
- `cargo deny check bans`: Passes

### 4. No "Managed" Exceptions — CLEAR

No exceptions claimed. All custom trait `dyn` dispatch eliminated.
Remaining `dyn` is idiomatic Rust (closures, std::error::Error) — not custom trait objects.

---

## Additional Fixes in This Pass

1. **reqwest 0.12 → 0.13**: Zero-breakage upgrade, all tests pass
2. **Integration test cfg fix**: `#[cfg(test)]` → `#[cfg(any(test, feature = "test-fixtures"))]`
   for `HangHealthCheckProvider` / `FailingHealthCheckProvider` so chaos integration
   tests compile correctly
3. **CLI duplicate import fix**: Removed duplicate imports in `petal-tongue-cli/handlers/tests.rs`
4. **Doctest fix**: Added `VisualizationDataProvider` trait import to discovery crate doctest

---

## Note for primalSpring

The `ring` lockfile stanza is a Cargo resolver artifact. It cannot be eliminated
without removing `reqwest` entirely (replacing with raw `hyper` client calls — possible
but significant refactor across 6 crates). The lockfile entry has **zero effect on
the compiled binary** — confirmed via `cargo tree` with all targets, all features,
dev/build/normal edges.

If the gate requires literal lockfile cleanliness (zero `ring` stanzas regardless of
compilation), the path forward is: replace `reqwest` with direct `hyper`+`hyper-util`
client. This is doable but lower priority than getting the three `async-trait` primals
(sweetGrass, BearDog, toadStool) through the gate.

---

**License**: AGPL-3.0-or-later
