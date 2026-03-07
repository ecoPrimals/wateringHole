# Cross-Primal IPC Rewire — `shader.compile.*` Contract Migration

**Date**: March 7, 2026
**From**: coralReef, toadStool, barraCuda
**To**: All primals consuming `shader.compile.*`

---

## Summary

coralReef Phase 10 Iteration 6 migrated its JSON-RPC method names from
`compiler.*` to `shader.compile.*` per wateringHole `SEMANTIC_METHOD_NAMING_STANDARD`.
This handoff documents the cross-primal rewire that aligns toadStool and
barraCuda with the new contract.

## Method Name Migration

| Old (pre-Iteration 6) | New (wateringHole standard) | Purpose |
|------------------------|-----------------------------|---------|
| `compiler.health` | `shader.compile.status` | Health/readiness probe |
| `compiler.compile` | `shader.compile.spirv` | SPIR-V → native binary |
| `compiler.compile_wgsl` | `shader.compile.wgsl` | WGSL → native binary |
| `compiler.supported_archs` | `shader.compile.capabilities` | Supported GPU architectures |

## Repositories Updated

### coralReef (`ecoPrimals/coralReef`)
- Already on `shader.compile.*` since Iteration 6
- JSON-RPC: `jsonrpsee` `#[method(name = "shader.compile.*")]`
- tarpc: `ShaderCompileTarpc` trait with `spirv()`, `wgsl()`, `status()`, `capabilities()`
- Differentiated error codes: `-32001` InvalidInput, `-32002` NotImplemented, `-32003` UnsupportedArch

### toadStool (`ecoPrimals/phase1/toadStool`)
- `crates/server/src/coral_reef_client.rs`:
  - `health()`: `compiler.health` → `shader.compile.status`
  - `compile_wgsl()`: `compiler.compile_wgsl` → `shader.compile.wgsl`
  - `compile_spirv()`: `compiler.compile` → `shader.compile.spirv`
- Handler (`shader.compile.*` external methods) unchanged — already correct
- Doc comments updated to reference new method names

### barraCuda (`ecoPrimals/barraCuda`)
- `crates/barracuda/src/device/coral_compiler.rs`:
  - `compile_spirv()`: already on `shader.compile.spirv`
  - `compile_wgsl_direct()`: already on `shader.compile.wgsl`
  - `health()`: already on `shader.compile.status`
  - `probe_jsonrpc()`: already on `shader.compile.status`, legacy `compiler.health` fallback removed
  - `spawn_coral_compile()` doc comment updated
- Module-level IPC contract doc already correct

## Data Flow (Post-Rewire)

```
Spring WGSL shader
       │
barraCuda (spawn_coral_compile)
       │ shader.compile.wgsl / shader.compile.spirv
       ▼
toadStool (shader.compile.* handler)
       │ shader.compile.wgsl / shader.compile.spirv
       ▼
coralReef (JSON-RPC server)
       │ WGSL → naga → SSA IR → optimize → legalize → RA → encode
       ▼
Native GPU binary (SM70-SM89, GFX1030)
```

## Verification

- toadStool: `cargo check --workspace` passes
- barraCuda: `cargo check --workspace` passes
- coralReef: 856 tests, zero warnings, zero failures
- All three repos use `shader.compile.*` exclusively — zero `compiler.*` IPC references remain

## Breaking Change Note

Pre-Iteration 6 coralReef instances (if any exist) will not respond to
`shader.compile.*` method names. The legacy `compiler.*` fallback in barraCuda's
`probe_jsonrpc()` has been removed. All deployments should use coralReef
Iteration 6+ (`967876f` or later).

---

*Contract aligned. Three primals, one namespace. `shader.compile.*` is the standard.*
