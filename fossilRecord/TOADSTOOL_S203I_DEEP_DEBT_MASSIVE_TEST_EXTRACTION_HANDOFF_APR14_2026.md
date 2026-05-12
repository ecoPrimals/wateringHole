# ToadStool S203i — Deep Debt: Massive Test Extraction + Hardcoding Evolution

**Date**: April 14, 2026
**Session**: S203i
**Scope**: 52 production files across 22 crates

## Summary

S203i is a massive test extraction sprint, moving ~10,000+ lines of inline
`#[cfg(test)] mod tests { ... }` blocks from production files into dedicated
companion `*_tests.rs` files. This reduces production file sizes, improves
navigability, and makes test coverage tracking cleaner.

Additionally, hardcoded primal-specific references in dispatch error metadata
were evolved to capability-neutral guidance.

## Test Extraction (52 files)

Pattern used throughout: `#[cfg(test)] #[path = "{name}_tests.rs"] mod tests;`

### Crates affected (22 total)
- `core/config` (runtime_defaults, validation/mod, profiler, substrate, discovery_integration)
- `core/common` (modern_utils, capability_provider/mod, unix_jsonrpc_client, primal_discovery, primal_discovery_mdns, error_codes)
- `core/toadstool` (workload/ai_ml, security/mod, security_hardening/mod, performance_hardening/mod, ipc/client, encryption/types, biomeos_integration/storage_backend_evolved, deployment_layer/detector, universal/types, universal/pipeline_graph, workload/selector)
- `core/nvpmu` (init)
- `core/sysmon` (pcie_topology)
- `toadstool-core` (silicon)
- `server` (errors, handler/mod, handler/dispatch/pipeline, handler/core/wire_l3, unibin/execution)
- `cli` (ecosystem/adapters/universal, ecosystem/adapters/storage)
- `auto_config` (lib, ai_mcp_interface/mod, hardware/cpu)
- `distributed` (coordination/capability_client, security_provider/unix_socket_provider, security_provider/tcp_provider)
- `integration/protocols` (config)
- `integration/security` (discovery)
- `management/performance` (implementation/selection)
- `runtime/container` (lib)
- `runtime/orchestration` (orchestrator, resource_orchestrator)
- `runtime/specialty` (cross_compilation, mainframe/ibm, mainframe/vax, embedded/toolchains)
- `runtime/display` (pcie_transport, ipc/server, drm/buffer)
- `runtime/secure_enclave` (audit)
- `runtime/gpu` (unified_memory/types)
- `security/sandbox` (types)
- `neuromorphic/akida-driver` (loading)
- `ml/burn-inference` (handled via existing extraction)

### Metrics
- Production files >500 lines: **38 → 25** (remaining are pure production code)
- Largest remaining production file: 678 lines (edge/arduino.rs — hardware driver)
- All quality gates pass: clippy 0 new warnings, all tests green

## Hardcoding Evolution

1. **`discovery_defaults.rs`**: Literal `"localhost"` in `FallbackEndpoints::fallback_endpoint()`
   replaced with `DEFAULT_HOSTNAME` constant from `toadstool_common::constants::network`
2. **`dispatch/submit.rs`**: `CORALREEF_URL` reference in error metadata replaced with
   capability-neutral guidance
3. **`dispatch/shader_dispatch.rs`**: `CORALREEF_URL / CORALREEF_SOCKET` reference replaced
   with capability-neutral guidance

## Quality Gates
- `cargo check --workspace --all-targets`: Clean
- `cargo clippy --workspace --all-targets`: 0 new warnings (1 pre-existing doc warning in config crate)
- `cargo test -p toadstool-server --lib`: 646 tests, 0 failures
- All affected crate tests: 0 failures

## Remaining Polish
- Coverage 83.6% → 90% target (D-COVERAGE-GAP)
- `async-trait` modernization (~320 instances — Rust language constraint)
- V4L2 ioctl cleanup
- Fuzz seed corpus + extended campaigns
