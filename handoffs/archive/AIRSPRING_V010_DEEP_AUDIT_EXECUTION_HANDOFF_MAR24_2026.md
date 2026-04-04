# airSpring V0.10.0 — Deep Audit Execution (Cross-Primal Handoff)

**From**: airSpring v0.10.0
**Date**: 2026-03-24
**To**: barraCuda, toadStool, coralReef, sibling Springs, wateringHole standards

---

## Summary

Deep audit execution yielded +43 lib tests (943→986), coverage gate now passes
(90.56% ≥ 90%), cargo-deny 0.19 fully compliant, and all CI gates green.

## Key Findings for Ecosystem Teams

### For All Springs: cargo-deny 0.19 Migration

cargo-deny 0.19 introduced breaking changes to `deny.toml`:

1. `[advisories].vulnerability` removed (all vulnerabilities now always error)
2. `[advisories].unmaintained` accepts `"all"|"workspace"|"transitive"|"none"` only
3. SPDX requires full identifiers: `AGPL-3.0-or-later`, not `AGPL-3.0+`
4. `CC0-1.0` needed for `hexf-parse` (via `naga` → `wgpu`) — add to `[licenses].allow`
5. `blake3` transitively brings `cc` — use `{ crate = "cc", wrappers = ["blake3"] }` in bans
6. Path deps need explicit versions to satisfy `wildcards = "deny"`: add `version = "X.Y.Z"` alongside `path = "..."`

### For All Springs: `#[allow()]` vs `#[expect()]` in Shared Test Infra

When `tests/common/mod.rs` is compiled into multiple test binaries, `#[expect(dead_code)]`
fires unfulfilled-lint-expectation errors in binaries that DO use the helper. Use `#[allow()]`
with `reason` for shared test infrastructure. `#[expect()]` remains correct for production
code and single-binary tests.

### For barraCuda: Compile-Time Tolerance Contracts

```rust
const { assert!(GPU_CPU_CROSS.abs_tol <= ET0_REFERENCE.abs_tol) }
```

Rust 2024 `const {}` blocks make tolerance ordering assertions compile-time. Catches drift
at build time, not runtime. Consider for `barracuda::tolerances`.

### For barraCuda: TCP Mock Server Pattern for IPC Testing

```rust
let listener = TcpListener::bind("127.0.0.1:0")?;
let addr = listener.local_addr()?;
let config = ProvenanceConfig { transport_override: Some(Transport::Tcp(addr)) };
```

DI pattern with TCP listener exercises real JSON-RPC round-trips without live biomeOS.
Coverage went from 50→80% on provenance module with 7 tests.

## Current Metrics

| Metric | Value |
|--------|-------|
| Lib tests | 986 |
| Total tests | 1,364 |
| Binaries | 91 |
| Line coverage | 90.56% |
| Tolerances | 58 (5 submodules) |
| Capabilities | 45 |
| barraCuda | 0.3.7 (wgpu 28) |
| cargo-deny | 0.19 clean |
| Unsafe blocks | 0 |
| C dependencies | 0 |

## Supersedes

- `AIRSPRING_V010_DEEP_EVOLUTION_ABSORPTION_HANDOFF_MAR23_2026.md`
- `AIRSPRING_V010_DEEP_AUDIT_BARRACUDA_TOADSTOOL_HANDOFF_MAR23_2026.md`
