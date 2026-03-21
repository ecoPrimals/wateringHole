<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# ToadStool S161 — Deep Debt, License Compliance & Coverage Handoff

**Date**: March 21, 2026  
**Session**: S161  
**Primal**: toadStool  
**Type**: Deep debt evolution, SPDX/AGPL alignment, smart module decomposition, coverage gaps, quality gates

## Summary

Session S161 focused on **technical debt reduction** (stubs, hardcoded values, unsafe patterns), **repository hygiene** (duplicate tests, coverage runner completeness), and **license compliance**: workspace `Cargo.toml` and sources aligned to **AGPL-3.0-only** with consistent SPDX identifiers. Targeted **coverage** was added for previously thin areas: `byob_impl` (inline `byob_impl_tests` module tree), `biomeos_integration::agent_backend_evolved`, and hw-learn **`auto_init`** paths via server handler tests. **Quality gates** remain green: `fmt`, `clippy` (0 warnings, pedantic + nursery), `doc`, full workspace tests (0 failures).

## Changes

### Smart refactors — 10 large compilation units → directory modules

Ten previously unwieldy single-file (or near-single-file) units were reorganized into **`mod.rs` + focused submodules** (public API preserved via `mod.rs` re-exports where needed):

1. `crates/cli/src/commands/dispatch/` — `biome`, `ecosystem`, `manifest`, `server`, `universal`, `tests`
2. `crates/cli/src/executor/lifecycle_ops/` — `start`, `stop`, `tests`
3. `crates/cli/src/ecosystem/` — `adapters`, `capabilities`, `discovery`, `integrator_impl`, …
4. `crates/cli/src/daemon/` — `http_server`, `jsonrpc_server`, `nautilus_handlers`, `workload_manager`, …
5. `crates/cli/src/zero_config/` — `core`, `configuration`, `deployment`, `discovery`, `service_discovery`, …
6. `crates/cli/src/templates/` — `basic_templates`, `generator_impl`, `rendering`, `specialized_templates`, …
7. `crates/cli/src/network_config/` — `configurator/`, `types/`
8. `crates/auto_config/src/intelligent/` — `analysis`, `detection`, `generation`, `validation`
9. `crates/auto_config/src/installer/` — `config_manager`, `core`, `integration`, `paths`, `runtimes`, …
10. `crates/auto_config/src/ai_mcp_interface/` — `handlers`, `session`, `types`

### Production stubs evolved

- **`runtime/specialty` embedded emulators** (`embedded/emulator_impls.rs`): placeholder trait impls now return typed **`SystemError::NotSupported`** with stable `feature` + reason strings (no silent success on core operations; `stop` remains a no-op where appropriate).

### Hardcoded values evolved

- **`distributed/src/hosting/recursive.rs`**: child instance URLs and defaults use **environment-aware** config (`TOADSTOOL_API_PORT`, `EnvironmentConfig::from_env()` for bind address) instead of naked literals alone.
- **`integration/protocols/src/config.rs`**: protocol defaults and HTTP helpers use shared **`http_url`** / **`toadstool_common`** patterns; timeouts and pool settings remain explicit `Duration`/`Default` with clear struct boundaries.

### Unsafe code evolved

- **`crates/core/nvpmu/src/vfio.rs`**: VFIO IRQ set and similar packed payloads built with **`to_ne_bytes()`** on integer fields instead of `slice::from_raw_parts` on transient buffers — same wire layout, less UB surface.

### Transport typing

- **`integration/protocols` transport**: routing failures return **`ProtocolError`** variants (e.g. `HttpTransportNotAvailable`, `TRpcTransportNotAvailable`, structured `Transport(...)`) instead of ad-hoc strings only.

### License compliance (AGPL-3.0-only)

- **Root / workspace `Cargo.toml`**: `license = "AGPL-3.0-only"` (workspace package default).
- **SPDX**: headers and crate metadata aligned across the workspace (**1912** tracked `*.rs` files at handoff time; `git ls-files '*.rs' | wc -l`).
- Ecosystem standard: matches **wateringHole** licensing row in `STANDARDS_AND_EXPECTATIONS.md` (AGPL-3.0-only for primals/springs).

### Coverage tests added

- **`byob_impl`**: `crates/core/toadstool/src/byob/byob_impl/byob_impl_tests/` (modular unit tests under `#[cfg(test)]`).
- **`agent_backend`**: `crates/core/toadstool/tests/agent_backend_evolved_coverage_tests.rs` — `AgentBackendEvolved` availability, errors, and serde/capability paths.
- **`auto_init`**: `crates/server/tests/hw_learn_handler_coverage_tests.rs` — `hw_learn_auto_init` / `hw_learn_auto_init_all` JSON-RPC branches.

### Repository cleanup

- Removed duplicate **`crates/cli/tests/adapter_integration_tests_fixed.rs`** (byte-identical to `adapter_integration_tests.rs`).

### Tooling

- **`scripts/run-coverage.sh`**: Tier-1 `CRATES` list extended to match **workspace members** not previously covered: `hw-learn`, `nvpmu`, `toadstool-sysmon`, neuromorphic crates (`akida-driver`, `akida-models`, `akida-reservoir-research`, `akida-setup`, `cross-substrate-validation`, `neurobench-runner`), `toadstool-integration-tests`, `toadstool-examples`. (`toadstool-runtime-edge` remains excluded — `serialport` → libudev.)

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check --workspace` | PASS |
| `cargo fmt --all -- --check` | PASS (0 diffs) |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | PASS (0 warnings; pedantic + nursery) |
| `cargo doc --workspace --all-features --no-deps` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (0 failures) |

## Standards compliance vs `wateringHole/STANDARDS_AND_EXPECTATIONS.md`

| Expectation | S161 status |
|-------------|-------------|
| Rust 2024, toolchain | Met (`edition = "2024"` workspace-wide) |
| Clippy pedantic + nursery, zero warnings | Met (`-D warnings` clean) |
| Unsafe policy | Justified blocks only; VFIO payload construction hardened |
| License AGPL-3.0-only | Met (workspace + SPDX alignment) |
| Documentation | `cargo doc` clean; library `missing_docs` discipline maintained |
| JSON-RPC / capability-first | No breaking IPC contract changes in this session |

## Remaining debt

- **D-COV**: Continue toward **90%** line coverage (wateringHole target); neuromorphic and examples crates add weight to Tier-1 runtime — monitor CI time.
- **Edge runtime**: `toadstool-runtime-edge` still excluded until libudev/serialport story is resolved.

## Cross-primal notes

- No intentional breaking JSON-RPC or capability surface changes; primarily **quality, compliance, and maintainability**.
- Duplicate test file removal reduces confusion and duplicate CI work.

---

*AGPL-3.0-only — ecoPrimals sovereign community property.*
