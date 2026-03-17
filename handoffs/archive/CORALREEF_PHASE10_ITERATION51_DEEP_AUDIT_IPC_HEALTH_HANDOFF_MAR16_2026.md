# coralReef — Phase 10 Iteration 51: Deep Audit Compliance + IPC Health + Doc Hygiene

**Date**: March 16, 2026  
**Phase**: 10 — Iteration 51  
**Primal**: coralReef (sovereign Rust GPU compiler)

---

## Summary

Full wateringHole compliance audit execution: IPC health methods (`health.check`, `health.liveness`, `health.readiness`) implemented across all three transports (JSON-RPC, tarpc, Unix socket), socket path standard aligned to `$XDG_RUNTIME_DIR/biomeos/<primal>-<family_id>.sock`, config self-knowledge via `PRIMAL_NAME`/`PRIMAL_VERSION`/`family_id()`, zero-copy transport evolution, `coral-gpu` smart refactor (977→65 LOC lib.rs), unsafe impl documentation, clippy pedantic cleanup, and all root docs updated. 2157 tests, 0 failures.

## What Changed

### CI Quality Gates — All PASS

| Check | Status |
|-------|--------|
| `cargo fmt --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-targets -- -D warnings` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS (1 non-blocking doc warning in coral-gpu) |
| `cargo test --workspace` | PASS (2157 tests, 0 failures) |
| `cargo deny check` | PASS (advisories ok, bans ok, licenses ok, sources ok) |
| `cargo llvm-cov` | 57.28% region / 57.71% line / 67.98% function |

### wateringHole IPC Compliance

- **`health.check`**: Returns primal status, version, uptime — JSON-RPC, tarpc, Unix socket
- **`health.liveness`**: Returns alive boolean — JSON-RPC, tarpc, Unix socket
- **`health.readiness`**: Returns ready boolean with capabilities list — JSON-RPC, tarpc, Unix socket
- **Socket path standard**: `ECOSYSTEM_NAMESPACE` changed from `"ecoPrimals"` to `"biomeos"` per wateringHole `PRIMAL_IPC_PROTOCOL`
- **`primal_socket_name()`**: Generates `<primal>-<family_id>.sock` where family_id reads `$BIOMEOS_FAMILY_ID` (default: `"default"`)
- **Semantic method naming**: All 8 IPC methods follow `{domain}.{operation}[.{variant}]` pattern per wateringHole `SEMANTIC_METHOD_NAMING_STANDARD`

### Config Self-Knowledge

- `PRIMAL_NAME`: `env!("CARGO_PKG_NAME")` — compile-time self-knowledge
- `PRIMAL_VERSION`: `env!("CARGO_PKG_VERSION")` — compile-time version
- `family_id()`: Reads `$BIOMEOS_FAMILY_ID` environment variable (defaults to `"default"`)
- `#[must_use]` on all config functions

### Zero-Copy Transport Evolution

- `primal-rpc-client` transport: `Bytes::copy_from_slice(&buf[body_start..])` → `buf.drain(..body_start); Bytes::from(buf)` — true zero-copy by taking ownership of remaining buffer

### Smart Refactoring

| Original | LOC | Refactored Into |
|----------|-----|-----------------|
| `coral-gpu/src/lib.rs` | 977 | `lib.rs` (65) + `kernel.rs`, `context.rs`, `fma.rs`, `pcie.rs`, `driver.rs`, `hash.rs` |

### Safety Documentation

- `unsafe impl Send/Sync for DmaBuffer` — documented: dedicated allocation, borrow rules, freed on Drop, container_fd thread-safe
- `unsafe impl Send/Sync for MappedBar` — documented: MMIO-mapped, volatile + atomic, lifetime tied to struct
- `unsafe impl Send/Sync for NvUvmComputeDevice` — documented: ownership, pushbuffer serialization, thread-safe fds
- `unsafe impl Send/Sync for Bar0Access` — documented: mmap'd BAR0, volatile aligned reads, OwnedFd lifetime

### Clippy Pedantic Fixes

- `items_after_statements` in primal-rpc-client tests
- `case_sensitive_file_extension_comparison` → `Path::extension()`
- `redundant_closure_for_method_calls` → method references
- `map_unwrap_or` → `is_some_and()`
- `useless_format` → string literals
- `assertions_on_constants` → `const {}` blocks
- Unused imports, doc backticks

### genomeBin Manifest

- `pie_verified = true` for coralreef
- `ecobin_grade = "A++"` (up from `A+`)

### E2E IPC Test

New `e2e_ipc.rs` test (gated behind `e2e` feature):
- Starts JSON-RPC and tarpc servers
- Tests all 8 semantic methods via both transports
- Verifies JSON-RPC 2.0 response format (jsonrpc, id, result fields)

## Coverage Analysis

| Metric | Before (Iter 50) | After (Iter 51) |
|--------|-------------------|-----------------|
| Tests passing | 1992 | 2157 |
| Region coverage | 57.10% | 57.28% |
| Line coverage | 57.54% | 57.71% |
| Function coverage | 67.80% | 67.98% |

Remaining coverage gap concentrated in:
- `coral-driver` VFIO/hardware code (requires exclusive GPU access)
- `coral-reef` compiler codegen (SM-specific instruction encoding paths)
- `amd-isa-gen` tool (27.57% — table generator, not runtime code)

## Markers Audit

| Category | Count | Location |
|----------|-------|----------|
| TODO | 6 | All in `amd_metal.rs` (AMD VFIO metal stubs — planned future work) |
| EVOLUTION | 9 (Rust) + 2 (config) | Documented future optimizations (co-issue, dual-issue, PrmtSel, etc.) |
| FIXME / HACK / XXX | 0 | Clean |
| `todo!()` / `unimplemented!()` | 0 | Clean |

## Inter-Primal Notes

### For toadStool
- All health IPC methods now available for ecosystem health monitoring
- Socket path follows `$XDG_RUNTIME_DIR/biomeos/coralreef-<family_id>.sock`
- coral-glowplug systemd daemon remains production-ready

### For barraCuda
- `compile_wgsl_full()` and `dispatch_precompiled()` APIs stable
- Health endpoints can be used for pre-dispatch readiness checks
- FMA capability reporting via `health.readiness` capabilities list

### For hotSpring
- `$HOTSPRING_DATA_DIR` still drives VBIOS and test data paths
- `$BIOMEOS_FAMILY_ID` enables multi-instance deployment

### For biomeos
- coralReef now fully compliant with `PRIMAL_IPC_PROTOCOL` socket path convention
- All 8 semantic methods follow `SEMANTIC_METHOD_NAMING_STANDARD`
- `genomeBin/manifest.toml` updated with `pie_verified = true`

## Blockers / Known Issues

1. **VFIO tests require `systemctl stop coral-glowplug`** — daemon holds both VFIO groups
2. **Texture compute prologue**: not yet implemented — blocks texture coverage
3. **SM50 ICE**: Integer division via float rounding panics on SM50 encoder
4. **f16 support**: `enable f16;` not wired through naga parser
5. **Coverage 57.71% → 90%**: Major gap in compiler codegen paths and hardware-gated code

## Files Modified (Key)

- `crates/coralreef-core/src/config.rs` — ECOSYSTEM_NAMESPACE, PRIMAL_NAME/VERSION, family_id(), primal_socket_name()
- `crates/coralreef-core/src/ipc/mod.rs` — #[must_use], updated socket naming
- `crates/coralreef-core/src/ipc/unix_jsonrpc.rs` — biomeos namespace, health dispatch handlers
- `crates/coralreef-core/src/ipc/jsonrpc.rs` — health.check/liveness/readiness methods
- `crates/coralreef-core/src/ipc/tarpc_transport.rs` — health methods on tarpc trait
- `crates/coralreef-core/src/service/mod.rs` — handle_health_check/liveness/readiness
- `crates/coralreef-core/src/service/types.rs` — HealthCheckResponse, LivenessResponse, ReadinessResponse
- `crates/coralreef-core/tests/e2e_ipc.rs` — NEW: E2E IPC test
- `crates/coral-gpu/src/lib.rs` — smart refactor → 6 submodules
- `crates/coral-driver/src/vfio/dma.rs` — SAFETY comments
- `crates/coral-driver/src/vfio/device.rs` — SAFETY comments
- `crates/coral-driver/src/nv/uvm_compute.rs` — SAFETY comments
- `crates/coral-driver/src/nv/bar0.rs` — SAFETY comments
- `crates/primal-rpc-client/src/transport.rs` — zero-copy evolution
- `crates/primal-rpc-client/src/tests.rs` — clippy fix
- `wateringHole/genomeBin/manifest.toml` — pie_verified, ecobin_grade

---

**Next session**: Coverage expansion (main.rs, nak-ir-proc, IPC transports, codegen passes), AMD metal stubs toward real implementations, VFIO hardware validation
