# coralReef: Warm Handoff Daemon Wiring + Polish — Handoff Mar 30 2026

## Summary

All GPU lifecycle control operations (livepatch management, BAR0 register access,
FECS state monitoring, orchestrated warm handoff) have been moved from shell scripts
and local `coralctl` CLI logic into the `coral-ember` and `coral-glowplug` daemon
layer as first-class JSON-RPC operations. This makes GPU lifecycle programmable by
any primal or project that can speak JSON-RPC over a Unix socket.

## What Changed

### New RPC Methods

| RPC | Crate | Handler |
|-----|-------|---------|
| `ember.livepatch.status` | coral-ember | `handlers_livepatch::status` |
| `ember.livepatch.enable` | coral-ember | `handlers_livepatch::enable` |
| `ember.livepatch.disable` | coral-ember | `handlers_livepatch::disable` |
| `ember.mmio.read` | coral-ember | `handlers_device::mmio_read` |
| `ember.fecs.state` | coral-ember | `handlers_device::fecs_state` |
| `device.warm_handoff` | coral-glowplug | `device_ops::handle_warm_handoff` |

### EmberClient Methods (coral-glowplug → coral-ember)

`mmio_read`, `fecs_state`, `livepatch_status`, `livepatch_enable`, `livepatch_disable`

### Health Loop Enhancement

`DeviceSlot::enrich_fecs_via_ember()` — active-health devices get live FECS register
data from ember (mmap-based) instead of the broken `File::seek+read` path.

### coralctl Simplification

`warm-fecs` and `warm-fecs-nvidia` commands are now thin wrappers over
`device.warm_handoff` RPC. Local BAR0 read and sysfs write helpers deleted.

## Code Quality / Polish (Same Session)

1. **Bar0Access DRY** — `open_resource` and `open_resource_readonly` now share a
   `mmap_file(file, path, prot)` helper. 40+ lines of duplication removed.

2. **FECS Register Constants** — Canonical `pub const FECS_CPUCTL`, `FECS_SCTL`,
   `FECS_PC`, `FECS_MB0`, `FECS_MB1`, `FECS_EXCI` added to `coral-driver::nv::bar0`.
   Replaces magic numbers in `handlers_device.rs`.

3. **Hex Parsing Consolidated** — `coral_driver::parse_hex_u32` and `parse_hex_u64`
   are the single source of truth. Three duplicate implementations (ember, glowplug,
   coralctl) now delegate.

4. **enrich_fecs_via_ember Simplified** — Uses `"halted"`/`"stopped"` booleans from
   the JSON response directly instead of re-parsing hex and recalculating bitfields.

5. **Livepatch Idempotency** — `enable`/`disable` handlers log whether the operation
   was a no-op, return `"was_noop"` in the JSON response.

6. **Warm Handoff Trace Flag** — `device.warm_handoff` now accepts `"trace": true`
   for mmiotrace capture during the swap.

## Test Coverage

16 new tests added (808 total across coral-driver/ember/glowplug):
- coral-driver: `parse_hex_u32/u64`, Bar0 readonly, FECS offset alignment/range
- coral-ember: livepatch handler (disable noop, patched funcs mock, transition polling)
- coral-glowplug: EmberClient mock server round-trips (mmio_read, fecs_state,
  livepatch_status, RPC error propagation), request/response format verification

## Files Changed

### coral-driver
- `src/lib.rs` — `parse_hex_u32`, `parse_hex_u64` + tests
- `src/nv/bar0.rs` — FECS constants, `mmap_file` helper, `open_resource_readonly`
  simplified, tests for readonly + offsets

### coral-ember
- `src/ipc/handlers_device.rs` — `mmio_read`, `fecs_state` RPCs, uses shared constants
- `src/ipc/handlers_livepatch.rs` — **new file** — `status`, `enable`, `disable` RPCs
- `src/ipc.rs` — dispatch entries for new RPCs
- `src/ipc/tests.rs` — tests for mmio/fecs/livepatch/parse_hex

### coral-glowplug
- `src/ember.rs` — `mmio_read`, `fecs_state`, `livepatch_*` client methods, mock tests
- `src/socket/handlers/device_ops.rs` — `device.warm_handoff` handler + trace flag
- `src/device/health.rs` — `enrich_fecs_via_ember` simplified
- `src/bin/coralctl/handlers_device/mod.rs` — thin wrappers over warm_handoff RPC

## For Other Primals

Any primal that needs GPU state can now:
```bash
# Query FECS firmware state
echo '{"jsonrpc":"2.0","method":"ember.fecs.state","params":{"bdf":"0000:03:00.0"},"id":1}' | socat - UNIX:/run/coralreef/ember.sock

# Read arbitrary BAR0 register
echo '{"jsonrpc":"2.0","method":"ember.mmio.read","params":{"bdf":"0000:03:00.0","offset":"0x409100"},"id":1}' | socat - UNIX:/run/coralreef/ember.sock

# Full warm handoff cycle
echo '{"jsonrpc":"2.0","method":"device.warm_handoff","params":{"bdf":"0000:03:00.0","driver":"nouveau","poll_fecs":true},"id":1}' | socat - UNIX:/run/coralreef/glowplug.sock
```

## Relevant Experiments

- **Exp 125**: Livepatch breakthrough — kernel livepatch NOP (4 functions)
- **Exp 127**: Warm FECS dispatch attack — firmware preserved but HALT not resumable
- **Exp 128**: Puzzle box matrix — parallel K80 + Titan V solution tracks

## Next Steps (For GPU Cracking Team)

1. Run K80 hardware tests (Exp 128 Track A) — validate full recipe replay + FECS boot
2. Run Titan V timing attack via `device.warm_handoff` with `poll_fecs: true`
3. Integrate STOP_CTXSW into the warm handoff sequence
4. Capture nvidia RM's FECS init sequence via UVM tracing
