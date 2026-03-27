# wetSpring V132 → barraCuda / toadStool Absorption Handoff

**Date:** 2026-03-23
**From:** wetSpring V132
**To:** barraCuda team, toadStool team
**License:** AGPL-3.0-or-later
**Companion:** WETSPRING_V132_DEEP_EVOLUTION_CROSS_ECOSYSTEM_ABSORPTION_HANDOFF_MAR23_2026.md

---

## Executive Summary

wetSpring V132 completed the **`GpuDriverProfile` → `DeviceCapabilities`** migration,
aligned **`normalize_method()`** with barraCuda **v0.3.7**, added **`performance_surface.report()`**
as a stub for toadStool integration, used **`DeviceCapabilities::latency_model()`** for
dispatch thresholds, and wired **StreamItem NDJSON** for downstream **loamSpine** /
**rhizoCrypt** style consumers. This document lists upstream asks, contributions back,
and API stability notes for barraCuda/toadStool planning.

---

## What wetSpring V132 Did

- Migrated from deprecated **`GpuDriverProfile`** to **`DeviceCapabilities`** (wetSpring
  is ready for barraCuda to remove deprecated types once no other consumers remain).
- Implemented **`normalize_method()`** on the wetSpring side (matches barraCuda v0.3.7).
- Added **`performance_surface.report()`** stub, ready for a toadStool endpoint.
- Added **`DeviceCapabilities::latency_model()`** usage for dispatch thresholds.
- Wired **StreamItem NDJSON** protocol (ready for **loamSpine** / **rhizoCrypt** integration).

---

## What wetSpring Needs from barraCuda

| Priority | Ask | Notes |
|----------|-----|--------|
| GPU path | **`BatchReconcileGpu`** primitive | `reconciliation_gpu` is currently CPU passthrough |
| Spectral | **DF64 GEMM** | Consumer-GPU spectral cosine workloads |
| Substrate | **`BandwidthTier`** in **metalForge** substrate model | Cross-stack bandwidth modeling |
| Dispatch | **`ComputeDispatch` → new BGL model** | Migration path and guidance |

---

## What wetSpring Can Contribute Back

1. **PROVENANCE_REGISTRY pattern** — **58** baseline scripts with SHA-256 hashes.
2. **ValidationSink pattern** — CI pipeline integration without forking validators.
3. **Workspace lint infrastructure pattern** — first spring with workspace-level lints.
4. **`IpcError::is_recoverable()`** + **retry policy** — operational resilience for IPC clients.

---

## API Stability Notes

- **wetSpring no longer uses `GpuDriverProfile`** — safe to remove upstream if no
  other consumers remain.
- **wetSpring uses `DeviceCapabilities`:** `.from_device()`, `.fp64_strategy()`,
  `.precision_routing()`, `.needs_exp_f64_workaround()`, `.needs_log_f64_workaround()`,
  `.latency_model()`, `.backend`, `.device_type`, `.device_name`, `.f64_shaders`.
- **wetSpring dispatches via `normalize_method()`** — RPC may send bare or prefixed
  method names; both normalize to a single dispatch path.
