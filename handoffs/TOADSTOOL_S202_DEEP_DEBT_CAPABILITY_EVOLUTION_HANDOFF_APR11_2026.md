# ToadStool S202 Handoff — Deep Debt Execution: Capability-Based Evolution

**Date**: April 11, 2026
**Session**: S202
**Author**: toadStool team
**Prior**: S201 (primalSpring gap closure + coverage push)

---

## Summary

Full-spectrum deep debt execution across the toadStool workspace. Five parallel
audit agents covered unsafe code, large files, production mocks, hardcoded values,
external dependencies, and primal-name references. All actionable findings executed.

## Changes Executed

### Hardcoded Literal Evolution
- `self_identity.rs`: `"toadstool"` → `PRIMAL_NAME` constant
- `bear_dog/client.rs`: `"toadstool"` audit service_id → `PRIMAL_NAME`
- `identity.rs`: JSON-RPC `capabilities.list` type field → `PRIMAL_NAME`
- `dispatch/capabilities.rs`: `"coral_reef_available"` → `"shader_compiler_available"`

### Primal-Name Doc Comments → Capability Wording
~15 production doc comments evolved from primal names to capability identifiers:
- `bear_dog/client.rs`, `auth.rs` — "BearDog security service" → "crypto/security capability provider"
- `coordinator/adapter.rs`, `coordinator/mod.rs` — "Songbird" → "coordination"
- `adapters/mod.rs` — "We don't know BearDog, NestGate, or Songbird" → "We don't know specific primals"
- `capabilities/mod.rs` — "BearDog, AWS KMS" → "any provider"
- `services/mod.rs` — legacy primal imports → capability adapter comments
- `infrastructure_templates.rs` — "NestGate" → "storage capability provider"
- `primal_sockets/mod.rs`, `primal_identity.rs`, `primal_discovery_mdns.rs` — all updated
- `doctor/types.rs`, `config_utils/network.rs`, `capability_types.rs`, `services/types.rs`

### Dead Code Removal
- `proxy_to_barracuda` legacy alias removed (was `#[expect(dead_code)]`, zero callers)

### Smart Refactoring
- `jsonrpc_server.rs`: Extracted `dispatch_or_parse_error()` helper — eliminated
  3 duplicated parse→dispatch→error-response patterns (Unix NDJSON, TCP, BTSP)

### Dependency Evolution
- `serialport` in `toadstool-runtime-specialty`: made optional behind `serial-transport` feature
  (C/libudev deps no longer pulled into default builds — ecoBin compliance)

### DEBT.md Hygiene
- `D-ASYNC-DYN-MARKERS` moved from Active Debt → "Known Limitations" (not actionable debt)
- `D-FUZZ-TARGETS` heading refreshed with cross-reference to `D-FUZZ-TARGETS-UNSAFE`

## Audit Findings (for record)

| Dimension | Result |
|-----------|--------|
| **Unsafe code** | 34 blocks, all in hw containment (mmap, ioctl, MMIO, DMA, alloc). All SAFETY-documented. None removable. |
| **Production mocks** | Zero. All Mock* types behind `#[cfg(test)]` or `test-mocks` feature. |
| **Production TODOs** | Zero. No TODO/FIXME/HACK/XXX in any `.rs` file under `crates/`. |
| **Large files** | Most >500-line files are test-only. `jsonrpc_server.rs` was the main prod candidate (now DRY'd). |
| **External deps** | All C/FFI deps feature-gated. Pure Rust stack for crypto, paths, compression. |
| **Deprecated stubs** | CUDA/OpenCL GPU backends intentionally return errors. Embedded placeholders gated behind feature. |

## Active Debt (7 items)

| ID | Summary | Status |
|----|---------|--------|
| D-TARPC-PHASE3-BINARY | Binary framing for Rust-to-Rust peers | Waiting on coordination mesh |
| D-EMBEDDED-PROGRAMMER | ISP/ICSP hardware transport | Waiting on hardware |
| D-EMBEDDED-EMULATOR | Cycle-accurate CPU cores | Waiting on hardware |
| D-COVERAGE-GAP | 83.6% → 90% line coverage | Ongoing |
| D-FUZZ-TARGETS-UNSAFE | GPU buffer access fuzzing | Low priority |
| D-FUZZ-TARGETS | CI, seed corpus, extended campaigns | Low priority |
| D-RUSTIX-DISPLAY-038 | V4L2 ioctl rustix 1.x migration | Blocked on rustix evolution |

## Known Limitations (1 item, not debt)

| ID | Summary |
|----|---------|
| D-ASYNC-DYN-MARKERS | ~55 `#[async_trait]` markers — resolves when Rust stabilizes `async fn` in `dyn Trait` |

## Quality Gates

- `cargo fmt --all -- --check`: PASS
- `cargo clippy --workspace -- -D warnings`: PASS (0 warnings)
- `cargo test --workspace`: PASS (0 failures)
- `cargo check`: PASS

## Files Modified

### Production code
- `crates/core/toadstool/src/self_identity.rs`
- `crates/integration/protocols/src/bear_dog/client.rs`
- `crates/integration/protocols/src/bear_dog/auth.rs`
- `crates/server/src/pure_jsonrpc/handler/core/identity.rs`
- `crates/server/src/pure_jsonrpc/handler/dispatch/capabilities.rs`
- `crates/server/src/pure_jsonrpc/handler/dispatch/tests.rs`
- `crates/cli/src/daemon/jsonrpc_server.rs`
- `crates/cli/src/daemon/nautilus_handlers.rs`
- `crates/cli/src/ecosystem/adapters/mod.rs`
- `crates/cli/src/ecosystem/adapters/coordination/mod.rs`
- `crates/cli/src/ecosystem/adapters/coordination/adapter.rs`
- `crates/cli/src/ecosystem/capabilities/mod.rs`
- `crates/cli/src/ecosystem/services/mod.rs`
- `crates/cli/src/templates/specialized_templates/mod.rs`
- `crates/cli/src/templates/specialized_templates/infrastructure_templates.rs`
- `crates/cli/src/executor/workload/runtime.rs`
- `crates/cli/src/commands/doctor/types.rs`
- `crates/core/common/src/primal_sockets/mod.rs`
- `crates/core/common/src/constants/primal_identity.rs`
- `crates/core/common/src/primal_discovery_mdns.rs`
- `crates/core/common/src/universal_adapter/capability_types.rs`
- `crates/core/config/src/services/types.rs`
- `crates/core/config/src/config_utils/network.rs`
- `crates/runtime/specialty/Cargo.toml`

### Documentation
- `CHANGELOG.md`, `DEBT.md`, `NEXT_STEPS.md`, `DOCUMENTATION.md`
