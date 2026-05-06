<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 92: Wire Standard L3 + Deep Debt Pass

**Date**: May 6, 2026
**From**: coralReef team
**To**: primalSpring, all downstream springs

---

## Summary

Wire Standard L3 alignment (`capabilities.list` gets `protocol` + `transport` fields). Deep debt pass: `coral_probe.rs` typed errors (zero `Result<_, String>` remaining anywhere in production), all hardcoded kernel device paths now env-overridable. Cross-cutting BufReader/TCP audits verified.

## Wire Standard L3

`CapabilityListResponse` now includes:

```json
{
  "primal": "coralreef-core",
  "version": "0.1.0",
  "protocol": "jsonrpc-2.0",
  "transport": ["uds", "tcp", "tarpc"],
  "methods": ["shader.compile.spirv", "..."],
  "capabilities": ["health", "identity", "shader"]
}
```

- `protocol` field: always `"jsonrpc-2.0"` (our primary wire protocol)
- `transport` field: `["uds", "tcp", "tarpc"]` on Unix; `["tcp", "tarpc"]` on non-Unix
- Backward compatible: existing consumers ignore unknown fields via serde defaults

## Cross-Cutting Audit Results

| Item | Status | Detail |
|------|--------|--------|
| BufReader post-negotiate | Correct | BufReader passed through to `process_encrypted_frames` — buffered bytes consumed correctly by async reader |
| Whitespace-tolerant TCP | Not needed | BTSP marker classification (`{` = JSON, other = marker) correct for all ecosystem clients |
| Port 9730 | Confirmed | Operational on ironGate, primalSpring has `TCP_FALLBACK_CORALREEF_PORT = 9730` |

## Test Results

- 4,686 passing, 0 failures, 177 ignored (hardware-gated)
- Zero clippy warnings (`clippy::pedantic` + `clippy::nursery`)
- Test `capability_list_wire_standard_l2` → renamed to `capability_list_wire_standard_l3` with L3 assertions

## Deep Debt — Typed Errors

`coral_probe.rs` (the fork-isolated GPU diagnostic binary):
- All `Result<_, String>` → `ProbeError` enum with `thiserror`
- Variants: `ResourceOpen`, `Mmap`, `Timeout`, `BatchTimeout`, `ChildFailed`, `BatchChildFailed`, `Fork`, `HexParse`
- Zero `Result<_, String>` remaining in any production code (binary or library)

## Deep Debt — Env-Overridable Device Paths

All hardcoded kernel device paths now have `OnceLock`-based env var overrides:

| Path | Env Override | Default |
|------|-------------|---------|
| coral-kmod device | `CORALREEF_CORAL_RM_PATH` | `/dev/coral-rm` |
| NVIDIA control | `CORALREEF_NV_CTL_PATH` | `/dev/nvidiactl` |
| NVIDIA UVM | `CORALREEF_NV_UVM_PATH` | `/dev/nvidia-uvm` |
| GPU device prefix | `CORALREEF_NV_GPU_PATH_PREFIX` | `/dev/nvidia` |
| DRM render prefix | `CORALREEF_DRI_RENDER_PREFIX` | `/dev/dri/renderD` |
| kmod sysfs | `CORALREEF_KMOD_SYSFS_PATH` | `/sys/module/coral_kmod` |

Enables container testing and non-standard deployments without recompilation.

## Downstream Impact

- No breaking changes (additive fields only on capabilities.list)
- primalSpring and composition tooling can now read L3 envelope from coralReef
- Discovery escalation hierarchy: coralReef discoverable at tiers 3-5 (UDS/registry/TCP); tier-1 Songbird registration deferred

## primalSpring Phase 59 Gap Resolution

| Item | Status |
|------|--------|
| Wire Standard L3 on `capabilities.list` | **RESOLVED** (this iteration) |
| BufReader post-negotiate correctness | **VERIFIED** (no action needed) |
| Whitespace-tolerant TCP detection | **ASSESSED** — not applicable |
| `Result<_, String>` in production code | **RESOLVED** — zero remaining |
| Hardcoded paths without env override | **RESOLVED** — all device paths env-overridable |
