# ToadStool S175 Deep Debt Evolution Handoff

**Date**: April 21, 2026
**Session**: S175
**From**: ToadStool team
**Status**: All quality gates green

---

## What Changed

### 1. NoopCryptoProvider — Capability-Based Errors

`crates/core/toadstool/src/encryption/provider.rs`

All 5 error-returning methods (`encrypt`, `decrypt`, `generate_key`, `get_key`, `health_check`) now use a single `NOOP_MSG` constant with capability-based guidance:

```
"no crypto provider registered; register a provider via crypto.provider.register capability"
```

Matches the `NoopCloudProvider` pattern established in S174.

### 2. eprintln! → tracing in Library Code

`crates/runtime/universal/src/capabilities.rs` (6 sites)

GPU adapter discovery diagnostics migrated from `eprintln!` to structured `tracing` macros:
- `tracing::warn!` — wgpu discovery timeout, wgpu adapter enumeration panic, no adapter matched selector
- `tracing::info!` with structured fields (`adapter_index`, `adapter_name`, `selector`) — auto/index/name adapter selection

Added `tracing` (workspace dep) to `toadstool-runtime-universal/Cargo.toml`.

### 3. #[allow] → #[expect] Lint Attribute Evolution

13 bare `#[allow]` attributes evolved to `#[expect]` with reasons across 6 files:

| File | Lints Evolved | Notes |
|------|--------------|-------|
| `distributed/universal/detection/gpu.rs` | 4× `dead_code` | Legacy OpenCL stubs (S198 compat) |
| `distributed/cloud/federation/mod.rs` | 1× `unused_imports` | Re-export for downstream use |
| `distributed/network/metrics.rs` | 1× `dead_code` | Field held for future aggregation |
| `management/performance/internal.rs` | 1× `dead_code` + `struct_field_names` | Baseline metrics reserved for model tuning |
| `neuromorphic/akida-setup/pcie.rs` | 2× `dead_code` | PCI scan struct fields |

Preventive `#[allow]` with reasons kept (lints don't currently fire):
- `nvpmu/vfio.rs` — `cast_possible_truncation` + `cast_ptr_alignment` on MMIO accessors
- `nvpmu/power_manager.rs` — `cast_possible_truncation` in `ClockGateConfig::decode`, `cast_precision_loss` on temperature read
- `server/pure_jsonrpc/handler/core/{compute,health,identity}.rs` — 9× `clippy::unused_async` on JSON-RPC handlers

---

## Verification

- `cargo check --workspace` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo test --workspace --lib` — 7,818 pass, 0 failures
- `cargo check --workspace --target armv7-unknown-linux-gnueabihf` — clean

---

## Impact for Other Teams

- **Springs**: No API changes. `NoopCryptoProvider` error messages now guide callers to register a provider via capability, matching ecosystem guidance patterns.
- **primalSpring**: Zero new gaps. All existing quality gates unchanged.
- **biomeOS**: No impact.

---

**License**: AGPL-3.0-or-later
