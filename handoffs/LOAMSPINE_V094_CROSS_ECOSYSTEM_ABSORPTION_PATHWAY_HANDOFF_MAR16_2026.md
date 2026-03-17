<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- ScyBorg Provenance: crafted by human intent, assisted by AI -->

# LoamSpine V0.9.4 — Cross-Ecosystem Absorption & Pathway Learner Handoff

**Primal**: LoamSpine  
**Version**: 0.9.4  
**Date**: March 16, 2026  
**Phase**: Spring Absorption + Pathway Learner + Manifest Discovery

---

## Summary

Following V0.9.3 (tarpc 0.37, DispatchOutcome, OrExit, StreamItem), this session absorbs patterns from across the ecosystem: sweetGrass IPC helpers, healthSpring/wetSpring Pathway Learner metadata, rhizoCrypt manifest discovery, and airSpring multi-format capability parsing.

---

## Changes Made

### 1. IpcPhase Helpers (sweetGrass alignment)

- `is_timeout_likely()`: Returns true for Connect/Read/Write phases
- `is_application_error()`: Returns true for JsonRpcError(_) phases

### 2. OrExit Wired into main.rs

Startup validation evolved from `anyhow::Result` + `?` to zero-panic `or_exit()`:
- `resolved_bind.parse().or_exit("Invalid bind address")`
- `lifecycle.start().await.or_exit("Failed to start lifecycle manager")`

### 3. Pathway Learner Metadata

`capability.list` now includes top-level `operation_dependencies` and `cost_estimates`:

```json
"operation_dependencies": { "entry.append": ["spine.create"], ... },
"cost_estimates": { "entry.append": { "latency_ms": 2, "cpu": "low", "memory_bytes": 8192, "gpu_eligible": false }, ... }
```

Aligns with healthSpring, wetSpring, groundSpring, airSpring, ludoSpring, neuralSpring.

### 4. extract_capabilities()

New function in `capabilities.rs` parsing 4 formats of `capability.list` responses:
1. Flat array: `{ "capabilities": ["a", "b"] }`
2. Object array: `{ "methods": [{ "method": "a", "domain": "x" }] }`
3. Nested domains: `{ "domains": { "spine": ["create", "get"] } }`
4. Combined: all three together

### 5. Manifest Discovery (rhizoCrypt S16)

New `discovery/manifest.rs` module:
- `manifest_dir()` → `$XDG_RUNTIME_DIR/ecoPrimals/`
- `discover_manifests()` → scan `*.json` for `PrimalManifest`
- `find_by_capability()` / `find_by_name()` for targeted lookup

### 6. Proptest

4 property-based tests for error types:
- `ipc_phase_display_never_panics` — IpcPhase Display never panics on any variant
- `ipc_error_helpers_consistent` — method_not_found implies application_error; timeout_likely implies recoverable
- `extract_rpc_error_never_panics` — arbitrary JSON never panics
- `dispatch_outcome_into_result_consistent` — ApplicationError always maps to application_error

### 7. deny.toml Evolution

`wildcards = "warn"` → `"deny"` — matches groundSpring, wetSpring, healthSpring, neuralSpring.

### 8. NeuralAPI IPC Evolution

All `LoamSpineError::Network(format!(...))` in `register_with_neural_api()`, `deregister_from_neural_api()`, and `DiscoveredAttestationProvider::jsonrpc_call()` evolved to structured `LoamSpineError::ipc(IpcPhase::*, ...)` with `extract_rpc_error()`.

---

## Metrics

| Metric | V0.9.3 | V0.9.4 |
|--------|--------|--------|
| Tests | 1,206 | 1,221 |
| Coverage (function) | 91.03% | 90.89% |
| Coverage (line) | 88.91% | 88.74% |
| Clippy warnings | 0 | 0 |
| Source files | 122 | 123 |
| deny.toml wildcards | warn | deny |
| Proptest properties | 0 | 4 |

---

## Ecosystem Alignment

| Pattern | Source | Status |
|---------|--------|--------|
| `is_timeout_likely()` | sweetGrass | **V0.9.4** |
| `is_application_error()` | sweetGrass | **V0.9.4** |
| `operation_dependencies` | healthSpring, wetSpring | **V0.9.4** |
| `cost_estimates` | healthSpring, wetSpring | **V0.9.4** |
| `extract_capabilities()` | wetSpring V125, airSpring v0.8.7 | **V0.9.4** |
| Manifest discovery | rhizoCrypt S16 | **V0.9.4** |
| Proptest for IPC types | rhizoCrypt, sweetGrass, toadstool | **V0.9.4** |
| `deny.toml wildcards=deny` | groundSpring, wetSpring | **V0.9.4** |
| `OrExit` wired | wetSpring V123, rhizoCrypt | **V0.9.4** |

---

## What Remains for V0.9.5+

1. **Wire `StreamItem`** into provenance trio pipeline coordination
2. **Wire `DispatchOutcome`** into JSON-RPC server dispatch path
3. **Storage backend error-path coverage** for line coverage lift
4. **ChaosEngine** integration (rhizoCrypt, beardog patterns)
5. **ValidationHarness** for `loamspine doctor` subcommand
6. **scyBorg license certificate schema** (SCYBORG_PROVENANCE_TRIO_GUIDANCE)
7. **LoamSpineClient trait** matching sweetGrass `anchor()`/`verify()`/`get_anchors()`
