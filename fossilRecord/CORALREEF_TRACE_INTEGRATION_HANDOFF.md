# coralReef Handoff: Native Trace Integration + nvidia_oracle Target

**From:** hotSpring (Experiment Lab)
**To:** coralReef Team (coral-ember, coral-glowplug, coralctl)
**Date:** 2026-03-24
**Priority:** High — unblocks Exp 082 multi-backend oracle campaign

## Summary

Ember already runs as root with `CAP_SYS_ADMIN` and orchestrates all driver swaps. mmiotrace capture should be a **built-in capability** of the swap lifecycle, not an external script requiring pkexec. Every swap with `--trace` becomes a permanent learning record for the ACR boot solver.

Additionally, `nvidia_oracle` (a renamed nvidia.ko) should be a known driver target, enabling multi-version driver coexistence without touching the protected display GPU.

## Architecture

```
coralctl swap 0000:03:00.0 nouveau --trace
  |
  v
GlowPlug: device.swap {bdf, target, trace: true}
  |
  v
Ember: ember.swap {bdf, target, trace: true}
  |
  v
handle_swap_device(bdf, target, held, enable_trace=true)
  |
  +-- Step 4: MmiotraceSession::enable()     <-- NEW
  +-- Step 5: bind_native(bdf, target, lifecycle)
  +-- Step 6: session.capture(bdf, target, data_dir, filter_ranges)  <-- NEW
  |
  v
Trace saved to /var/lib/coralreef/traces/<driver>_<bdf>_<timestamp>/
```

## Phase 1: New Module — `crates/coral-ember/src/trace.rs`

### Public API

```rust
pub struct MmiotraceSession { started_at: Instant }

impl MmiotraceSession {
    pub fn enable() -> Result<Self, String>;
    pub fn capture(self, bdf: &str, driver: &str, data_dir: &Path,
                   filter_ranges: &[RegisterRange]) -> Result<TraceCapture, String>;
    pub fn abort(self);
}

pub struct RegisterRange {
    pub name: &'static str,
    pub start: u32,  // BAR0 offset range start
    pub end: u32,    // BAR0 offset range end
}

pub fn nvidia_falcon_ranges() -> Vec<RegisterRange>;
pub fn default_data_dir() -> PathBuf;  // $CORALREEF_TRACE_DIR or /var/lib/coralreef/traces
pub fn list_traces(data_dir: &Path) -> Vec<PathBuf>;
pub fn is_mmiotrace_active() -> bool;
```

### Implementation Details

- `enable()`: Mounts debugfs if needed, writes `mmiotrace` to `/sys/kernel/debug/tracing/current_tracer`, sets `tracing_on=1`. Refuses if another tracer is active.
- `capture()`: Stops tracing, reads `/sys/kernel/debug/tracing/trace`, saves raw + filtered outputs. Resets tracer to `nop`. Also captures warm BAR0 via `resource0` read.
- Filter: mmiotrace write lines start with `W <width> <timestamp> <address> <value>`. Parse 4th token as hex address, check if it falls in any RegisterRange.
- Output per capture:
  - `mmiotrace_raw.txt` — full trace
  - `mmiotrace_writes.txt` — write-only operations
  - `mmiotrace_<range_name>.txt` — per-range filtered writes
  - `bar0_warm.bin` — BAR0 snapshot while driver is bound
  - `manifest.json` — metadata (driver, bdf, timestamp, write counts, kernel version)

### NVIDIA Falcon Ranges

| Name | Start | End |
|------|-------|-----|
| SEC2 | 0x087000 | 0x087FFF |
| FECS | 0x409000 | 0x409FFF |
| GPCCS | 0x41A000 | 0x41AFFF |
| PMU | 0x10A000 | 0x10AFFF |
| PFB | 0x100000 | 0x100FFF |
| PCLOCK | 0x130000 | 0x13FFFF |

## Phase 2: VendorLifecycle Trait Extension

### `vendor_lifecycle.rs` — New Method

```rust
pub trait VendorLifecycle: Send + Sync + fmt::Debug {
    // ... existing methods ...

    /// BAR0 register ranges for mmiotrace filtering.
    /// Default: empty (no per-range filtering, still captures all writes).
    fn trace_filter_ranges(&self) -> Vec<RegisterRange> {
        Vec::new()
    }
}
```

### NvidiaLifecycle — Override

```rust
impl VendorLifecycle for NvidiaLifecycle {
    // ... existing methods unchanged ...

    fn trace_filter_ranges(&self) -> Vec<RegisterRange> {
        crate::trace::nvidia_falcon_ranges()
    }
}
```

## Phase 3: Wire Trace into `handle_swap_device`

### `swap.rs` — New Signature

```rust
pub fn handle_swap_device(
    bdf: &str,
    target: &str,
    held: &mut HashMap<String, HeldDevice>,
    enable_trace: bool,  // <-- NEW PARAMETER
) -> Result<String, String> {
```

### Insertion Points

Between existing Step 3 (unbind) and Step 4 (bind):

```rust
// Step 4: enable mmiotrace if requested
let trace_session = if enable_trace && target != "vfio" && target != "vfio-pci" && target != "unbound" {
    match trace::MmiotraceSession::enable() {
        Ok(session) => Some(session),
        Err(e) => {
            tracing::warn!(bdf, target, error = %e, "mmiotrace enable failed — proceeding without trace");
            None
        }
    }
} else {
    None
};

// Step 5: bind to target driver (existing logic)
let bind_result = match target { ... };

// Step 6: capture trace after bind
if let Some(session) = trace_session {
    match &bind_result {
        Ok(_) => {
            let filter_ranges = lifecycle.trace_filter_ranges();
            let data_dir = trace::default_data_dir();
            match session.capture(bdf, target, &data_dir, &filter_ranges) {
                Ok(cap) => tracing::info!(...),
                Err(e) => tracing::warn!(...),
            }
        }
        Err(_) => session.abort(),
    }
}
```

## Phase 4: IPC Propagation

### `ipc.rs` — `ember.swap` Handler

Extract optional `trace` param from request:

```rust
"ember.swap" => {
    // ... existing bdf/target extraction ...
    let enable_trace = params.get("trace").and_then(|v| v.as_bool()).unwrap_or(false);
    // ...
    match swap::handle_swap_device(bdf, target, &mut map, enable_trace) { ... }
}
```

### `ember.rs` (GlowPlug EmberClient)

Add `swap_device_traced` method:

```rust
pub fn swap_device_traced(&self, bdf: &str, target: &str, trace: bool) -> Result<String, EmberError> {
    // Same as swap_device but includes "trace": true in params
}
```

Keep existing `swap_device` as `self.swap_device_traced(bdf, target, false)`.

### `device/swap.rs` (GlowPlug DeviceSlot)

Add `swap_traced(&mut self, target: &str, trace: bool)`:

```rust
pub fn swap_traced(&mut self, target: &str, trace: bool) -> Result<(), DeviceError> {
    // Same as swap() but calls client.swap_device_traced(bdf, target, trace)
}
```

### `socket/handlers.rs` — `device.swap` Dispatch

Extract optional `trace` param:

```rust
"device.swap" => {
    // ... existing ...
    let enable_trace = params.get("trace").and_then(|v| v.as_bool()).unwrap_or(false);
    slot.swap_traced(&target, enable_trace)?;
    // ...
}
```

## Phase 5: coralctl CLI

### `main.rs` — Swap Command

```rust
Swap {
    bdf: String,
    target: String,
    #[arg(long)]
    trace: bool,  // <-- NEW FLAG
},
TraceStatus,  // <-- NEW SUBCOMMAND
TraceList,    // <-- NEW SUBCOMMAND
```

### `handlers_device.rs`

```rust
pub fn rpc_swap(socket: &str, bdf: &str, target: &str, trace: bool) {
    let mut params = json!({"bdf": bdf, "target": target});
    if trace { params["trace"] = json!(true); }
    // ... existing logic ...
}

pub fn rpc_trace_status(socket: &str) { ... }
pub fn rpc_trace_list() { ... }
```

Note: `coral-glowplug` will need `coral-ember` as a dependency for `coral_ember::trace::{list_traces, default_data_dir, is_mmiotrace_active}` used in the trace-list/trace-status commands.

## Phase 6: nvidia_oracle Driver Target

### KNOWN_TARGETS — `swap.rs`

```rust
const KNOWN_TARGETS: &[&str] = &[
    "vfio", "vfio-pci", "nouveau", "amdgpu", "nvidia",
    "nvidia_oracle",
    "xe", "i915", "akida-pcie", "unbound",
];
// Also accept nvidia_oracle_* variants (versioned):
let target_matches = KNOWN_TARGETS.contains(&target) || target.starts_with("nvidia_oracle_");
```

### NvidiaOracleLifecycle — `vendor_lifecycle.rs`

```rust
pub struct NvidiaOracleLifecycle {
    pub device_id: u16,
    pub module_name: String,
}

impl VendorLifecycle for NvidiaOracleLifecycle {
    fn description(&self) -> &str { "NVIDIA Oracle (renamed module for driver coexistence)" }
    fn prepare_for_unbind(&self, bdf, _) -> Result<(), String> { pin_power + clear reset_method }
    fn rebind_strategy(&self, _) -> RebindStrategy { SimpleBind }
    fn settle_secs(&self, target) -> u64 { if "nouveau" { 10 } else { 8 } }
    fn stabilize_after_bind(&self, bdf, _) { pin_power + clear reset_method }
    fn verify_health(&self, bdf, _) -> Result<(), String> { check not D3cold }
    fn trace_filter_ranges(&self) -> Vec<RegisterRange> { nvidia_falcon_ranges() }
}
```

Add `detect_lifecycle_for_target(bdf, target)` that returns `NvidiaOracleLifecycle` for `nvidia_oracle*` targets, falls back to `detect_lifecycle(bdf)` otherwise.

### Personality — `personality.rs`

```rust
// Enum variant:
NvidiaOracle { drm_card: Option<String>, module_name: String },

// Registry:
known: vec![..., "nvidia_oracle", ...],

// create():
"nvidia_oracle" => Some(Box::new(NvidiaOraclePersonality { ... })),

// GpuPersonality trait:
pub struct NvidiaOraclePersonality { drm_card_path: Option<String>, module_name: String }
```

### DeviceSlot::swap — `device/swap.rs`

```rust
t if t.starts_with("nvidia_oracle") => {
    let drm = self.sysfs.find_drm_card(&self.bdf);
    self.personality = Personality::NvidiaOracle { drm_card: drm, module_name: t.to_string() };
}
```

## Build Script

The oracle module build script lives in `hotSpring/scripts/build_nvidia_oracle.sh`. It patches two `#define`s in the open kernel source and builds a renamed `.ko`:

1. `MODULE_BASE_NAME "nvidia"` → `"nvidia_oracle"` in `common/inc/nv-linux.h`
2. `NV_MAJOR_DEVICE_NUMBER 195` → `0` (dynamic) in `common/inc/nv-chardev-numbers.h`

The proprietary blob (`nv-kernel.o_binary`) does NOT hardcode "nvidia" as a string, so the rename propagates cleanly through the PCI driver name, procfs paths, and device nodes.

## Test Plan

1. `cargo test -p coral-ember` — existing tests pass with `enable_trace: false`
2. `cargo test -p coral-glowplug` — existing dispatch tests pass with no `trace` param
3. Manual: `coralctl swap 0000:03:00.0 nouveau --trace` captures mmiotrace
4. Manual: `coralctl trace-list` shows the captured trace
5. Manual: `coralctl swap 0000:03:00.0 nvidia_oracle --trace` (after building the module)

## Cross-Reference Findings (Bonus)

From GV100 header analysis (hotSpring Exp 082):

- **PTE `>> 4` encoding**: Confirmed correct for 4K-aligned addresses
- **SYS_MEM_COH_TARGET inconsistency**: `attempt_sysmem_acr_boot` uses `2`, `attempt_acr_chain` uses `3` at the `0x668` bind_inst register. Verify against Nouveau and reconcile.
- **Fault buffer register names**: `GET/PUT/SIZE` are swapped in `registers.rs` vs `dev_fb.h` (`0xE2C/0xE30/0xE34`)
