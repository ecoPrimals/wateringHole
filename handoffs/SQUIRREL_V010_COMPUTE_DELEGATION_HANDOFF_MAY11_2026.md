<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — Compute Delegation Wired (Composition Parity)

**Date**: May 11, 2026
**Session**: BC
**Audit Source**: primalSpring stadial audit (May 11, 2026) — "squirrel — MEDIUM (compute delegation not wired)"

## Problem

`auto_detect_compute_provider()` detected `COMPUTE_ENDPOINT` presence but called
`create_compute_from_type("capability")` which fell through to a dead error path.
In composition, squirrel's compute needs hit a dead end — it could never delegate
to toadStool even when the compute primal was available.

## Resolution

### `RemoteComputeProvider` — JSON-RPC IPC delegation

Created `RemoteComputeProvider` in `crates/main/src/compute_client/provider_trait.rs`
that implements the full `ComputeProvider` trait via JSON-RPC 2.0 IPC:

- **Transport**: Unix socket (`unix://...`) or TCP (`host:port` / `http://host:port`)
- **Protocol**: Newline-delimited JSON-RPC 2.0 (same framing as all ecoPrimals IPC)
- **Method mapping**:
  - `execute_workload` → `compute.execute` (translates `WorkloadExecutionSpec` to toadStool's
    `JsonWorkloadSubmission` wire format with base64-encoded payload)
  - `get_workload_status` → `compute.status`
  - `cancel_workload` → `compute.cancel`
  - `list_workloads` → `compute.list`
  - `get_capabilities` → `compute.capabilities`
  - `health_check` → `health.check`

### `ComputeBackend::Remote` variant

Added to the enum dispatch pattern, maintaining zero `dyn` usage.

### `auto_detect_compute_provider()` detection chain

Updated to properly resolve endpoints and create the remote provider:

1. `COMPUTE_PROVIDER_TYPE` env → explicit type selection ("local", "remote", "toadstool")
2. `COMPUTE_SERVICE_ENDPOINT` / `COMPUTE_ENDPOINT` / `TOADSTOOL_ENDPOINT` → creates
   `RemoteComputeProvider` with resolved endpoint
3. No env set → falls back to `LocalProcessProvider` (development only)

### Test coverage

6 new tests:
- `auto_detect_with_compute_endpoint_creates_remote`
- `auto_detect_with_toadstool_endpoint_creates_remote`
- `auto_detect_explicit_remote_type_needs_endpoint`
- `remote_provider_metadata_includes_endpoint`
- `remote_provider_health_check_fails_on_unreachable`
- `auto_detect_no_env_falls_back_to_local`

### Quality Gate Results

| Metric | Result |
|--------|--------|
| `cargo fmt --all` | PASS |
| `cargo clippy -p squirrel` | ZERO warnings |
| `cargo test --workspace` | 7,209 pass / 0 fail |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

## Composition Impact

Squirrel can now participate in Nest/NUCLEUS compositions that require compute
delegation. When toadStool is in the composition and advertises its endpoint via
`COMPUTE_ENDPOINT` (or socket registry), squirrel's compute path routes through
IPC instead of hitting the local dev stub error.

## Wire Format Reference

Squirrel → toadStool `compute.execute` JSON-RPC:

```json
{
  "jsonrpc": "2.0",
  "id": "<uuid>",
  "method": "compute.execute",
  "params": {
    "workload_id": "<uuid>",
    "workload_type": "generic",
    "data": "<base64(json{image,command,environment})>",
    "metadata": { ... },
    "priority": "Normal",
    "requirements": {
      "cpu_cores": 4,
      "memory_bytes": 8589934592,
      "timeout_secs": 3600
    }
  }
}
```
