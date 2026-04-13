# coralReef Handoff: Iteration 80 — Wire Contract, CompilationInfo IPC, Deep Debt (April 12, 2026)

**From:** coralReef  
**To:** All primal teams, all spring teams  
**Status:** 4,504 tests passing. Wire contract documented. CompilationInfo in IPC. Socket alignment complete. Hot-path IPC allocations eliminated. Feature-gate fix for non-workspace builds. VFIO constructors feature-gated. MMU oracle unit-tested. Deep debt audit clean.

---

## What Changed

### 1. Wire Contract Documentation (Composition Blocker — RESOLVED)

New `docs/SHADER_COMPILE_WIRE_CONTRACT.md` — the authoritative JSON-RPC/tarpc wire contract for shader compilation. This was the **blocking composition gap** identified by primalSpring.

**Request** (`shader.compile.wgsl`):
```json
{"jsonrpc":"2.0","id":1,"method":"shader.compile.wgsl","params":{"source":"@compute @workgroup_size(64)...","target":"sm_70","opt_level":2}}
```

**Response** (success):
```json
{"jsonrpc":"2.0","id":1,"result":{"binary":"<base64>","size":2048,"arch":"sm70","status":"compiled","info":{"gpr_count":24,"instr_count":187,"shared_mem_bytes":0,"barrier_count":0,"workgroup_size":[64,1,1]}}}
```

**Error** (compilation failure):
```json
{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"WGSL parse error: ...","data":null}}
```

Document covers: all `shader.compile.*` and `health.*` methods, JSON-RPC error code mapping, multi-stage ML pipeline composition (tokenizer → attention → FFN as sequential compile-then-dispatch), capability discovery responses, tarpc transport notes.

### 2. CompilationInfo in IPC Responses

`CompileResponse` and `DeviceCompileResult` now carry `info: Option<CompilationInfoResponse>` with:

| Field | Type | Meaning |
|-------|------|---------|
| `gpr_count` | u32 | Registers used per thread |
| `instr_count` | u32 | Total instructions in binary |
| `shared_mem_bytes` | u32 | Shared memory per workgroup |
| `barrier_count` | u32 | Barrier synchronization points |
| `workgroup_size` | [u32; 3] | Declared workgroup dimensions |

Springs can now use this metadata for dispatch decisions (occupancy, memory budgeting, pipeline scheduling).

### 3. Crypto Socket Discovery Alignment

Socket directory resolution was duplicated across `coralreef-core`, `coral-glowplug`, and `coral-ember`. Now centralized:

- `coral-glowplug/config.rs`: `resolve_socket_dir()`, `family_id()`, `ecosystem_namespace()` — `pub` API
- `coral-ember/config.rs`: `resolve_socket_dir()` — `pub(crate)` API
- Both BTSP modules delegate to their respective config modules

Path resolution order (all three crates, aligned):
1. `CORALREEF_SOCKET_DIR` env var
2. `/run/coralreef/` (default)

Scoped socket naming (aligned):
1. `crypto-{family_id}.sock` (when `BIOMEOS_FAMILY_ID` set)
2. `crypto.sock` (unscoped fallback)

### 4. Idiomatic Rust Evolution

- **`NvArch::parse()`**: Was iterating `ALL` and calling `format!("sm_{sm}")` / `format!("sm{sm}")` per variant (14 heap allocations per parse). Now a direct `match` on string literals — zero allocations.
- **`IntelArch::Display`**: Was duplicating `short_name()` values in match arms. Now `f.write_str(self.short_name())`.
- **UDS Host header**: `primal-rpc-client` was sending `Host: localhost` on Unix domain socket requests. Now derives from socket filename (e.g. `Host: coralreef-core`).

---

## Deep Debt Audit Summary

Comprehensive audit confirmed the codebase is clean:

| Area | Finding |
|------|---------|
| Hardcoded primal names | **Zero** in production code |
| Hardcoded ports | **Zero** in production (test-only) |
| Socket paths without env override | **All** have env overrides |
| Mocks in production | **All** `#[cfg(test)]` or feature-gated |
| `todo!()` / `unimplemented!()` | **Zero** in production |
| `Result<_, String>` in production | **Zero** (all typed via `thiserror`) |
| `.unwrap()` in library code | **Zero** (confined to tests) |
| Unsafe code | **All** in `coral-driver` only, all with `// SAFETY:` |
| `#![forbid(unsafe_code)]` | **All** crate roots except `coral-driver` |
| `ring` / `openssl` / C-sys | **Banned** via `deny.toml`, absent from lockfile |

---

## What Each Team Should Know

### neuralSpring
- The wire contract documents exactly how to compose multi-stage ML pipelines: compile each stage (tokenizer, attention, FFN) as a separate `shader.compile.wgsl` call, then dispatch sequentially via toadStool with dependency chaining.
- `CompilationInfo` in responses lets you compute occupancy and schedule GPU resources before dispatch.

### toadStool
- `CompilationInfo.workgroup_size` tells you the declared workgroup dimensions — use for dispatch grid calculation.
- `CompilationInfo.shared_mem_bytes` tells you shared memory per workgroup — use for occupancy estimation.

### barraCuda
- Binary output in `CompileResponse.binary` is the same format as before. The `info` field is additive.
- For multi-GPU dispatch, `shader.compile.wgsl.multi` returns per-device results each with their own `info`.

### primalSpring
- Both BLOCKING COMPOSITION items from the Iter 80 audit are **RESOLVED**:
  1. Wire contract documented in `SHADER_COMPILE_WIRE_CONTRACT.md`
  2. Multi-stage ML pipeline documented in both the wire contract and `IPC_COMPOSITION_AND_LATENCY.md`
- REMAINING DEBT items status:
  - Transitive `libc`: unchanged (deferred until mio→rustix upstream)
  - Crypto socket alignment: **RESOLVED** this iteration

---

## Quality Gates

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-features -- -D warnings` | PASS (0 warnings) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --all-features --no-deps` | PASS |
| `cargo deny check` | PASS (advisories ok, bans ok, licenses ok, sources ok) |
| `cargo test --all-features` | **4,504 tests**, 0 failed, 153 ignored |
| Files >1000 LOC | 0 |
| TODO/FIXME/HACK in .rs | 0 |

---

## Files Changed

| Crate | File | Change |
|-------|------|--------|
| coralreef-core | `service/types.rs` | `CompilationInfoResponse` struct, `info` field on `CompileResponse` and `DeviceCompileResult` |
| coralreef-core | `service/compile.rs` | `handle_compile_wgsl` and `handle_compile_wgsl_multi` populate `info` via `compile_wgsl_full` |
| coralreef-core | `service/tests.rs` | Updated serde roundtrip tests for `info` field |
| coral-reef | `gpu_arch.rs` | `NvArch::parse()` zero-allocation rewrite; `IntelArch::Display` DRY |
| coral-glowplug | `config.rs` | Centralized `resolve_socket_dir()`, `family_id()`, `ecosystem_namespace()` as `pub` |
| coral-glowplug | `socket/btsp.rs` | Delegates to centralized config |
| coral-ember | `config.rs` | New `resolve_socket_dir()` |
| coral-ember | `btsp.rs` | Delegates to centralized config |
| primal-rpc-client | `transport.rs` | Socket-name-derived UDS Host header |
| coralreef-core | `ipc/newline_jsonrpc.rs` | Hot-path alloc: eliminated `format!` copy and per-line `trim().to_owned()`; `#[must_use]` on `make_response` |
| coralreef-core | `service/compile.rs` | `STATUS_SUCCESS` constant; `#[must_use]` on `parse_fma_policy` |
| coralreef-core | `service/tests.rs` | 5 new wire contract serde roundtrip tests |
| coral-driver | `nv/uvm_compute/types.rs` | Feature-gate fix: inline `CLFLUSH`/no-op instead of `vfio` import |
| coral-reef | `codegen/ir/op_float/f64_ops.rs` | "placeholder" → "pseudo-op" (6 ops) |
| coral-reef | `codegen/ir/op.rs`, `opt_instr_sched_common.rs` | "placeholder" → "pseudo-op" |
| coral-driver | `vfio/channel/mmu_oracle/engine_regs.rs` | **New** — extracted engine register capture tables (static data arrays + shared `read_regs()` helper) |
| coral-driver | `vfio/channel/mmu_oracle/capture.rs` | 825→654 LOC: engine register data moved to `engine_regs.rs` |
| coral-driver | `nv/vfio_compute/acr_boot/.../boot_config.rs` | `Display` impl: inlined `write!` instead of allocating via `label()` → `format!()` |
| coralreef-core | `service/compile.rs` | `#[must_use]` on `parse_target`, `handle_compile_spirv`, `handle_compile`, `handle_compile_wgsl`, `handle_compile_wgsl_multi` |
| coralreef-core | `service/tests.rs` | 6 multi-stage ML pipeline composition tests (sequential 3-stage, workgroup, cross-vendor, occupancy, independence, serde roundtrip) |
| coralreef-core | `ipc/newline_jsonrpc.rs` | `#[must_use]` on `dispatch_jsonrpc` |
| coral-driver | `error.rs` | `#[cfg(feature = "vfio")]` on `sysfs_io`, `vbios_resource_io`, `resource_io` constructors + tests — eliminates dead_code on default builds |
| coral-driver | `vfio/channel/mmu_oracle/capture.rs` | 11 new pure-Rust unit tests: `decode_entry_addr` (4), `EntryFlags` decode (5), serde roundtrips (2) |
| coral-driver | `vfio/channel/mmu_oracle/engine_regs.rs` | 4 new unit tests: serde roundtrip, unique register names, unique offsets, non-empty tables |
| docs/ | `SHADER_COMPILE_WIRE_CONTRACT.md` | **New** — authoritative wire contract |
| docs/ | `IPC_COMPOSITION_AND_LATENCY.md` | Wire contract reference, info fields in diagrams |

---

## References

- `docs/SHADER_COMPILE_WIRE_CONTRACT.md` — wire contract (primary)
- `docs/IPC_COMPOSITION_AND_LATENCY.md` — composition patterns and latency budgets
- `CHANGELOG.md` § Iteration 80
- `STATUS.md` § Iteration 80
