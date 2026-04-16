# ToadStool S203m: Deep Debt Stub Evolution + Hardcoding Sweep

**Date**: April 16, 2026
**Scope**: Evolve production stubs, centralize hardcoding, harden unsafe docs, audit deps
**Quality Gates**: `cargo fmt` ✅ | `cargo check` ✅ | `cargo clippy --workspace -- -D warnings` ✅ | all tests pass ✅

---

## Summary

Full-dimension deep debt pass: production stubs evolved to real implementations,
sysfs/procfs/env hardcoding centralized to constants, unsafe SAFETY documentation
hardened, external dependency chain audited. 25 files changed, +887/-105 lines.

---

## 1. Production Stubs → Real Implementations

### Edge Discovery (3 modules)

| Module | Before | After |
|--------|--------|-------|
| `runtime/edge/discovery/usb.rs` | Always returned empty Vec | Real sysfs enumeration: `/sys/bus/usb/devices/`, reads `idVendor`/`idProduct`/`manufacturer`/`product` |
| `runtime/edge/discovery/bluetooth.rs` | Adapter check only, empty result | Sysfs BT device enumeration via `/sys/bus/bluetooth/devices/` |
| `runtime/edge/discovery/network.rs` | IPv6 scan: "not yet implemented" | Reads `/proc/net/if_inet6` for link-local addresses, probes with `scope_id` |

All gracefully degrade to empty Vec on non-Linux or permission errors.

### Scheduler Queuing

**Before**: `UniversalJobQueue::add_job` only stored metadata (dependency graph, resource index)
but never pushed jobs into `priority_queues`. `schedule_local_job` logged and returned `Ok(())`.

**After**: `add_job` inserts into per-priority `VecDeque`. `schedule_job` calls `add_job`
before routing. `schedule_local_job` logs post-enqueue telemetry with structured fields
(job_id, priority, target, job_type, local_queue_depth).

## 2. Hardcoding → Constants

### Sysfs/Procfs Paths (8 files)

New `platform_paths` constants:
- `procfs::VERSION` (`/proc/version`)
- `procfs::NET_IF_INET6` (`/proc/net/if_inet6`)
- `sysfs::CLASS_BLUETOOTH`, `BLOCK`, `CLASS_NET`, `CLASS_DMI_ID_PRODUCT_NAME`
- `sysfs::BLOCK_SDA_QUEUE_ROTATIONAL`
- `sysfs::BUS_USB_DEVICES`, `BUS_BLUETOOTH_DEVICES`

Files: `bluetooth.rs`, `detection.rs`, `linux.rs`, `detector.rs`,
`memory.rs`, `storage.rs`, `reporting.rs`, `discovery.rs`

### Environment Variables (5 files)

New `socket_env` constants:
- General: `HOME`
- Identity: `TOADSTOOL_NODE_ID`
- Legacy: `PRIMAL_SOCKET`
- TCP: `TOADSTOOL_TCP_IDLE_TIMEOUT_SECS`
- BTSP: `FAMILY_SEED`
- Cloud detection: `AWS_EXECUTION_ENV`, `ECS_CONTAINER_METADATA_URI`,
  `EC2_INSTANCE_TYPE`, `GCP_PROJECT`, `GOOGLE_CLOUD_PROJECT`,
  `GCLOUD_PROJECT`, `GCE_METADATA_AVAILABLE`, `AZURE_SUBSCRIPTION_ID`,
  `WEBSITE_INSTANCE_ID`, `FUNCTIONS_WORKER_RUNTIME`

Files: `unibin/format.rs`, `unibin/mod.rs`, `tcp.rs`, `jsonrpc_server.rs`, `detector.rs`

## 3. Unsafe SAFETY Documentation

### Blocks (4 sites)
- `contiguous.rs` (lines 44, 60): `NonNull::as_ref`/`as_mut` — SAFETY docs + `debug_assert!` for alignment and `isize` bounds
- `access.rs` (lines ~93, ~117): Same pattern — SAFETY docs + `debug_assert!` for size and alignment

### Send/Sync Impls (6 sites)
- `exclusive_ptr.rs`: `Send`/`Sync` for `ExclusivePtr` — documented invariants (process-wide storage, no TLS)
- `backend.rs`: `Send`/`Sync` for `GpuPtr` — opaque handle semantics, coherence is backend's job
- `threading.rs`: `Send`/`Sync` for `UnifiedBuffer` — field-level Send, RAII single-free, RwLock guards

## 4. Dependency Audit

**`serde_yaml_ng`**: Uses `unsafe-libyaml` which is libyaml transpiled to Rust via c2rust.
**Pure Rust** — no C linker needed. Already ecoBin v3 compliant. No migration needed.

**No C FFI in workspace pins**: `wgpu` has GPU backends (expected/unavoidable).
`tokio`/`rand` use `libc` transitively (normal for async I/O). No `-sys` crates in
workspace dependency pins.

## 5. Root Documentation Updates

- **README.md**: Updated footer to S203m, corrected unsafe counts (40 forbid + 6 deny = 46/46), async-trait 158, edge discovery description, Recently Completed section with S203m/l/j-k, test time consistency (~3m30s)
- **DOCUMENTATION.md**: Updated to S203m with edge/scheduler/hardcoding bullets
- **NEXT_STEPS.md**: Corrected 46/46 crates, scheduler wording
- **DEBT.md**: S203m resolved section added (5 items), scheduler wording corrected

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Edge USB discovery | Empty stub | Real sysfs enumeration |
| Edge BT discovery | Adapter-only stub | Real sysfs device scan |
| Edge IPv6 discovery | "not yet implemented" | procfs-based link-local |
| Scheduler queuing | Metadata-only (no priority queue) | Per-priority VecDeque |
| Raw sysfs/procfs paths | ~50+ scattered | 8 files → constants |
| Raw env var strings | ~50+ scattered | 5 files → constants |
| unsafe SAFETY docs | Minimal | Structured + debug_assert! |

---

## Remaining

- Container `get_metrics()` still returns hardcoded zeros (needs cgroup/Docker stats)
- CLI network configurator `apply_*` methods defer to orchestration layer
- ~40+ more raw sysfs paths remain in deep hardware paths (nvpmu, akida, GPU drivers)
- ~50+ more raw env var call sites across CLI/config modules
- Coverage 83.6% → 90% (hardware-dependent test gaps)
