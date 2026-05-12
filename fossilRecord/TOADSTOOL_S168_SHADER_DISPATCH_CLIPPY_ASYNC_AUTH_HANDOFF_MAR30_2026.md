# ToadStool S168 — Sovereign Shader Pipeline + Clippy Zero-Warning + Async Auth

**Date**: March 30, 2026
**From**: toadStool team
**Session**: S168
**Refs**: ludoSpring V35 Part 4, coralReef Iter 70

---

## Summary

S168 closes the ludoSpring V35 / coralReef Iter 70 E2E sovereign shader pipeline gap and resolves full workspace clippy compliance, async auth evolution, and coverage expansion.

---

## 1. `shader.dispatch` JSON-RPC Method (ludoSpring V35 Gap Closure)

### What

Implemented `shader.dispatch` — the dispatch half of the sovereign shader pipeline. This closes the compile→dispatch→readback E2E gap identified by ludoSpring V35 (Part 4) and coralReef Iter 70.

### Pipeline (now complete)

```
coralReef (shader.compile.wgsl) → toadStool (shader.dispatch) → GPU (VFIO/DRM) → consumer (readback)
```

### API Surface

```json
{
  "jsonrpc": "2.0",
  "method": "shader.dispatch",
  "params": {
    "binary": "<base64 string OR JSON u8 array>",
    "workgroup_size": [256, 1, 1],
    "buffers": [{"size": 1024, "usage": "storage"}],
    "bdf": "0000:01:00.0",
    "dispatch_mode": "vfio",
    "readback": true,
    "timeout_ms": 5000
  },
  "id": 1
}
```

Also accepts coralReef's `CompileResponse` shape for zero-friction pipeline chaining:

```json
{
  "compile_result": { "binary": [...], "arch": "sm89", "target_device": 0 },
  "workgroup_size": [256, 1, 1],
  "buffers": [...]
}
```

### Binary Encoding

- **base64 string** (preferred, compact for JSON-RPC transport)
- **JSON array of u8** (backward-compatible with `compute.dispatch.submit`)
- Auto-detected based on JSON type (string vs array)

### Implementation

- New file: `crates/server/src/pure_jsonrpc/handler/dispatch/shader_dispatch.rs`
- Method on `DispatchHandler` (preferred over `ShaderHandler` to avoid circular references)
- Delegates to coralReef's `compute.dispatch.execute` for actual GPU submission
- Thermal safety check via `check_thermal_for_bdf_pub()`
- Job tracking reuses `compute.dispatch.{status,result}` infrastructure
- Registered in:
  - Literal router (`"shader.dispatch"` arm)
  - `dispatch_by_impl_name` (`"shader_dispatch"` arm)
  - Semantic method registry (`shader.dispatch` → `shader_dispatch`)
  - Songbird capability registration (`"shader.dispatch"` in capabilities array)
  - `dispatch_capabilities` method list

### Tests (18 new)

16 unit tests + 2 handler-level routing/discoverability tests covering: missing params, missing binary, empty binary (array + base64), invalid base64, wrong type, base64 acceptance, u8 array acceptance, `compile_result` shape, readback default/override, VFIO without coralReef, dispatch count increment, job trackability, handler routing, semantic registry discoverability.

---

## 2. Full Workspace Clippy Zero-Warning

`cargo clippy --workspace --all-targets -- -D warnings` now passes with 0 warnings. ~120+ warnings fixed across 20+ crates:
- `redundant_clone` (63), `default_constructed_unit_structs` (18), `float_cmp` (8), `needless_collect` (8), `derive_partial_eq_without_eq` (5), `manual_mul_add` (5), `string_lit_as_bytes` (3), `needless_pass_by_value` (2), plus misc

---

## 3. Async-First Auth Backend

`BearDogBackend::sign_payload()` and `public_key()` evolved from synchronous (per-call `std::thread::scope` + `tokio::runtime::Builder::new_current_thread()` + `block_on`) to native `async fn`. Eliminates per-call thread spawn and runtime construction overhead. `AuthBackend` trait, `AuthenticationManager`, and all call sites updated.

---

## 4. Server Connection Zero-Copy

Raw JSON-RPC path in `pure_jsonrpc/connection.rs` evolved from `to_vec()` (copy) to `Cow::Borrowed` (zero-copy) for both Unix and TCP handlers.

---

## 5. Coverage Expansion Round 2

11 specialty runtime files from 0% → covered: `error.rs`, `types/configs/management.rs`, `types/emulation.rs`, `embedded/dos.rs`, `cross_compilation.rs`, `mainframe/{ibm,vax,as400}.rs`, `emulator_impls.rs`, `programmer_impls.rs`.

---

## Impact on Other Primals

| Primal | Impact |
|--------|--------|
| **coralReef** | E2E pipeline now testable: `shader.compile.wgsl` → `shader.dispatch` → readback. ludoSpring V35 P2 gap resolved. |
| **barraCuda** | Can chain compiled binaries through toadStool dispatch without manual binary re-encoding. |
| **ludoSpring** | exp085 primal composition chain now completable end-to-end. |
| **All primals** | No breaking changes. New method is additive. |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | 0 diffs |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 warnings |
| `cargo check --workspace` | Clean |
| `cargo test --workspace --lib` | All passing, 0 failures |

---

## Files Changed

- `crates/server/src/pure_jsonrpc/handler/dispatch/shader_dispatch.rs` — **NEW**: `shader_dispatch` method
- `crates/server/src/pure_jsonrpc/handler/dispatch/mod.rs` — register `shader_dispatch` module
- `crates/server/src/pure_jsonrpc/handler/dispatch/capabilities.rs` — add `shader.dispatch` to methods list
- `crates/server/src/pure_jsonrpc/handler/dispatch/tests.rs` — 16 new shader dispatch tests
- `crates/server/src/pure_jsonrpc/handler/mod.rs` — wire `shader.dispatch` route + 2 handler-level tests
- `crates/core/toadstool/src/semantic_methods.rs` — register `shader.dispatch` → `shader_dispatch` mapping
- `crates/core/toadstool/src/ipc_helpers/connection.rs` — add `shader.dispatch` to Songbird capabilities
- `DEBT.md`, `NEXT_STEPS.md`, `README.md`, `DOCUMENTATION.md`, `CHANGELOG.md` — S168 updates
- ~30 additional files for clippy fixes, async auth evolution, zero-copy, and coverage expansion
