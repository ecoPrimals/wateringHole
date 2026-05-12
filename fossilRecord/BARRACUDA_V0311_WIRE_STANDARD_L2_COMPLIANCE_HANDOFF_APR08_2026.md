# barraCuda v0.3.11 — Wire Standard L2 Compliance Handoff

**Date**: April 8, 2026
**Sprint**: 33
**From**: barraCuda team
**To**: primalSpring, biomeOS, downstream primals
**Context**: primalSpring downstream audit flagged barraCuda as "no active gaps — future L3 dependency". Wire Standard L2 compliance was pending GPU compute method stabilization. Methods are now stable (31 methods, all quality gates green). This handoff documents L2 adoption.

---

## What Changed

### Wire Standard L2 — capabilities.list Envelope

`capabilities.list` now returns the standard `{primal, version, methods}` envelope per `CAPABILITY_WIRE_STANDARD.md` v1.0:

```json
{
  "primal": "barracuda",
  "version": "0.3.11",
  "methods": ["identity.get", "primal.info", "primal.capabilities", "health.liveness", ...],
  "provided_capabilities": [
    {"type": "compute", "methods": ["dispatch"], "version": "0.3.11", "description": "GPU compute shader dispatch"},
    {"type": "tensor", "methods": ["create", "matmul", "add", "scale", "clamp", "reduce", "sigmoid"], "version": "0.3.11", "description": "GPU tensor operations"},
    {"type": "fhe", "methods": ["ntt", "pointwise_mul"], "version": "0.3.11", "description": "Fully homomorphic encryption primitives"},
    ...
  ],
  "consumed_capabilities": ["shader.compile.cpu", "shader.validate", "compute.dispatch"],
  "protocol": "jsonrpc-2.0",
  "transport": ["uds", "tcp"],
  "provides": [...],
  "domains": [...],
  "hardware": {"gpu_available": true, "f64_shaders": true, "spirv_passthrough": false}
}
```

`provided_capabilities` groups are derived from the dispatch table via `discovery::provided_capability_groups()` — zero hardcoded domain catalog.

### Wire Standard L2 — identity.get

New `identity.get` method returns lightweight primal identity for biomeOS observability:

```json
{"primal": "barracuda", "version": "0.3.11", "domain": "compute", "license": "AGPL-3.0-or-later"}
```

Wired in both JSON-RPC dispatch and tarpc `BarraCudaService`.

### Method Count

30 → 31 methods (added `identity.get`). Full method list in `REGISTERED_METHODS` constant.

---

## Wire Standard Compliance Checklist

### Level 1 (Routable) — COMPLETE
- [x] `capabilities.list` responds to JSON-RPC probe over UDS
- [x] Response parseable by biomeOS
- [x] `health.liveness` responds with `{status: "alive"}`

### Level 2 (Standard) — COMPLETE
- [x] result contains `primal` field (canonical name: `barracuda`)
- [x] result contains `version` field (SemVer: `0.3.11`)
- [x] result contains `methods` flat string array (31 methods)
- [x] Every entry in `methods` is callable (verified by `test_all_dispatch_routes_exist`)
- [x] Method names follow `domain.operation` dotted convention
- [x] `identity.get` implemented and returns `{primal, version, domain, license}`
- [x] `health.liveness`, `health.check`, `health.readiness` all implemented

### Level 3 (Composable) — PARTIAL
- [x] `provided_capabilities` grouping present with type + methods per group
- [x] `consumed_capabilities` lists cross-primal dependencies
- [ ] `cost_estimates` for high-cost methods (future)
- [ ] `operation_dependencies` for methods with prerequisites (future)

---

## Files Changed

| File | Change |
|------|--------|
| `crates/barracuda-core/src/ipc/methods/primal.rs` | L2 envelope in `capabilities()`, new `identity()` handler |
| `crates/barracuda-core/src/ipc/methods/mod.rs` | `identity.get` in REGISTERED_METHODS + dispatch routing |
| `crates/barracuda-core/src/discovery.rs` | `provided_capability_groups()` + `domain_description()` |
| `crates/barracuda-core/src/rpc_types.rs` | `IdentityInfo` struct |
| `crates/barracuda-core/src/rpc.rs` | tarpc `identity_get` trait method + implementation |
| `crates/barracuda-core/src/ipc/methods_tests.rs` | 13 new L2 compliance tests |

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (pedantic + nursery) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | PASS |
| `cargo nextest run --workspace` | 4,187 pass / 0 fail / 14 skip |

---

## Future Work

- **Wire Standard L3**: `cost_estimates` and `operation_dependencies` when ecosystem composition patterns are stabilized by primalSpring
- **Erasure coding primitive**: GPU-accelerated GF(2^8) erasure code for L3 covalent mesh backup pattern (dependency from primalSpring GAP-MATRIX)

---

**License**: AGPL-3.0-or-later
