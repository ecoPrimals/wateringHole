<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 70i Deep Debt Evolution Handoff

**Date**: March 31, 2026  
**Primal**: coralReef  
**Iteration**: 70i  
**Phase**: 10 — Deep Debt Evolution + Safety Audit + Path Agnosticism

---

## What Was Done

### Hardcoded Path Elimination (all crates)

All hardcoded system paths in production code now use env-var overrides with sane defaults:

| Path | Env Var | Default | File |
|------|---------|---------|------|
| Livepatch module name | `$CORALREEF_LIVEPATCH_MODULE` | `livepatch_nvkm_mc_reset` | `coral-ember/src/ipc/handlers_livepatch.rs` |
| Livepatch sysfs path | (derived from module) | `/sys/kernel/livepatch/<module>` | same |
| debugfs tracing root | `$CORALREEF_DEBUGFS_TRACING` | `/sys/kernel/debug/tracing` | `coral-ember/src/trace.rs` |
| TCP bind address | `$CORALREEF_BIND_ADDR` | `127.0.0.1` | `coral-ember/src/lib.rs`, `coral-glowplug/src/config.rs` |

### Safety Documentation Audit

All `unsafe` blocks now have `// SAFETY:` comments — both production and test code:

- `coral-ember/tests/config_and_paths.rs` — ~12 blocks (env save/restore)
- `coral-glowplug/tests/config_env.rs` — 6 blocks (env override)
- `coralreef-core/tests/unix_jsonrpc_default_socket_path_env.rs` — 3 blocks (XDG mutation)

### Unwrap Audit

Full audit: **zero `.unwrap()` in library `src/` code** across all crates. Only in examples, rustdoc blocks, and test code.

### HTTP Host Header Documentation

`primal-rpc-client/src/transport.rs` — documented that `"localhost"` in Unix socket HTTP Host header is HTTP/1.1 protocol compliance, not meaningful hardcoding.

### Large File Refactoring (Iter 70h)

- `device_ops.rs` 1020→791 lines (register handlers → `register_ops.rs`)
- `jit_validation.rs` 1538→613 lines (→ `jit_barracuda.rs` + `jit_shared_memory.rs` + `tests/common/mod.rs`)

### Unsafe Code Evolution (Iter 70h)

- `sovereign.rs` — `unsafe` pointer arithmetic → safe `usize` arithmetic

### IPC Compliance (Iter 70h)

- wateringHole IPC_COMPLIANCE_MATRIX: coralReef → **Conformant (C)** across all dimensions
- PRIMAL_RESPONSIBILITY_MATRIX: Tier 3 actions resolved
- CORALREEF_LEVERAGE_GUIDE: corrected "zero FFI" claim
- ECOBIN_ARCHITECTURE_STANDARD: coralReef added to plasmidBin inventory

### barraCuda Math Validation (Iter 70g)

- Triple-path validated: sigmoid, relu, leaky_relu, elu, hardsigmoid, hardtanh, silu
- Elementwise: add, sub, mul, fma
- Unary: abs, sqrt, sign
- Shared memory: `var<workgroup>` + `workgroupBarrier()`, tree reduction, layer norm, tiled matmul
- Workgroup stress: 256-invocation relu

---

## Audit Results (Clean)

| Dimension | Status |
|-----------|--------|
| `.unwrap()` in library code | 0 |
| `todo!()` / `unimplemented!()` in production | 0 |
| Mocks in production | 0 — all `#[cfg(test)]` isolated |
| Direct `libc` / `-sys` / `cc` / `build.rs` | 0 — transitive only (Cranelift JIT, tokio) |
| Files > 1000 LOC (production) | 0 |
| Clippy warnings (pedantic+nursery) | 0 |
| SPDX headers | 490+ files |

---

## What Remains

### Near-Term (Iter 70j+)

1. **Local scratch memory emulation** — JIT `var<function>` arrays for `for`-loop patterns
2. **MmioRegion safe RAII wrapper** — consolidate 79 `unsafe` sites in `coral-driver`
3. **Coverage push** — ~64% → 90% (19k untestable driver lines excluded)
4. **toadStool E2E pipeline** — dispatch handoff when GPU development stabilizes

### Medium-Term

5. **Cranelift JIT `libc` transitive** — track upstream `cranelift-jit` for pure-Rust mmap (sovereign.rs already uses `rustix` directly)
6. **`#[allow(clippy::*)]` tightening** — remaining `#[allow]` in codegen/lib.rs → narrow or `#[expect]`
7. **dispatch boundary formalization** — coralReef compiles, toadStool dispatches (springs call coralReef directly post-S169)

---

## Validation

```
cargo check --all-features  → clean (0 errors, pre-existing missing_docs only)
cargo test --all-features   → 4232+ passing, 0 failed, ~155 ignored
cargo clippy --all-features -- -D warnings → 0 warnings
```
