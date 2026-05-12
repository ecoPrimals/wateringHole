# coralReef Handoff: Open Target Acceptance + Trace-as-Default

**From:** hotSpring (Experiment Lab)
**To:** coralReef Team (coral-ember, coral-glowplug, coralctl)
**Date:** 2026-03-24
**Priority:** High — unblocks universal driver experimentation on managed GPUs
**Related:** `CORALREEF_TRACE_INTEGRATION_HANDOFF.md` (trace module spec, prerequisite)
**Architecture:** `hotSpring/specs/UNIVERSAL_DRIVER_REAGENT_ARCHITECTURE.md`

## Summary

Three changes to make GlowPlug/Ember accept **any driver as a reagent** on managed GPUs,
while keeping the protection model intact:

1. Replace `KNOWN_TARGETS` hard rejection with open acceptance + validation
2. Add `Personality::Custom` variant for unknown drivers
3. Invert trace default to on (configurable)

## Phase 1: Open Target Acceptance

### File: `crates/coral-ember/src/swap.rs`

#### Current Code (lines ~283-290)

```rust
const KNOWN_TARGETS: &[&str] = &[
    "vfio", "vfio-pci", "nouveau", "amdgpu", "nvidia", "nvidia_oracle", "xe", "i915",
    "akida-pcie", "unbound",
];
let target_matches = KNOWN_TARGETS.contains(&target) || target.starts_with("nvidia_oracle_");
if !target_matches {
    return Err(format!("swap_device: unknown target driver '{target}'"));
}
```

#### Replace With

```rust
const WELL_KNOWN_TARGETS: &[&str] = &[
    "vfio", "vfio-pci", "nouveau", "amdgpu", "nvidia", "nvidia_oracle", "xe", "i915",
    "akida-pcie", "unbound",
];
let is_well_known = WELL_KNOWN_TARGETS.contains(&target) || target.starts_with("nvidia_oracle_");
if !is_well_known {
    tracing::warn!(
        bdf, target,
        "swap_device: target is not a well-known driver — treating as reagent. \
         GenericLifecycle will be used for conservative defaults."
    );
}

// Validate: must be a valid Linux kernel module name
if target.is_empty()
    || target.len() > 64
    || !target.chars().all(|c| c.is_ascii_alphanumeric() || c == '_' || c == '-')
{
    return Err(format!(
        "swap_device: invalid driver name '{target}' — \
         must be 1-64 chars of [a-zA-Z0-9_-]"
    ));
}
```

#### Rationale

- Protection is **role-based and BDF-based** (lines ~299-307: `is_active_display_gpu`,
  `is_protected`, `managed_bdfs`). The `KNOWN_TARGETS` allowlist was a secondary guard
  that now limits experimentation.
- `GenericLifecycle` (line ~465 of `vendor_lifecycle.rs`) already handles unknown vendors.
- The validation ensures the target string is a valid kernel module name, preventing
  injection or malformed sysfs writes.

### File: `crates/coral-ember/src/swap.rs` — DRM Helper

The `is_drm_driver` helper (used to decide whether to check DRM isolation before bind)
should also handle unknown drivers:

#### Current

```rust
fn is_drm_driver(target: &str) -> bool {
    matches!(target, "nouveau" | "amdgpu" | "nvidia" | "xe" | "i915")
        || target.starts_with("nvidia_oracle")
}
```

#### Replace With

```rust
fn is_drm_driver(target: &str) -> bool {
    // Well-known DRM drivers
    if matches!(target, "nouveau" | "amdgpu" | "nvidia" | "xe" | "i915")
        || target.starts_with("nvidia_oracle")
    {
        return true;
    }
    // Unknown drivers: assume they might create DRM nodes (conservative).
    // DRM isolation check is cheap and safe to run unnecessarily.
    !matches!(target, "vfio" | "vfio-pci" | "akida-pcie" | "unbound")
}
```

This ensures DRM isolation is verified for unknown drivers that might create DRM nodes
on bind. The check is a no-op if isolation is already configured.

## Phase 2: Generic Personality Variant

### File: `crates/coral-glowplug/src/personality.rs`

#### Add Variant to Enum (~line 428)

```rust
pub enum Personality {
    Vfio { group_id: u32 },
    Nouveau { drm_card: Option<String> },
    Nvidia { drm_card: Option<String> },
    NvidiaOracle { drm_card: Option<String>, module_name: String },
    Amdgpu { drm_card: Option<String> },
    Xe { drm_card: Option<String> },
    I915 { drm_card: Option<String> },
    Akida,
    Unbound,
    Custom { driver_name: String, drm_card: Option<String> },
}
```

#### Update `name()` (~line 433)

```rust
pub fn name(&self) -> &str {
    match self {
        // ... existing arms ...
        Self::Custom { driver_name, .. } => driver_name.as_str(),
    }
}
```

Note: this changes `name()` from `const fn` to `fn` because `Custom` returns a runtime
string. If const-ness is needed elsewhere, add a separate `const fn static_name()` that
returns `"custom"` for the `Custom` variant.

#### Update `provides_vfio()` and `supports_hbm2_training()`

```rust
pub const fn provides_vfio(&self) -> bool {
    matches!(self, Self::Vfio { .. })
}

pub const fn supports_hbm2_training(&self) -> bool {
    matches!(
        self,
        Self::Nouveau { .. } | Self::Nvidia { .. } | Self::NvidiaOracle { .. } | Self::Amdgpu { .. }
    )
    // Custom: false by default — unknown drivers don't get HBM2 training assumptions
}
```

#### Update `fmt::Display`

```rust
Self::Custom { driver_name, drm_card } => {
    write!(f, "{driver_name} (reagent)")?;
    if let Some(card) = drm_card {
        write!(f, " [{card}]")?;
    }
    Ok(())
}
```

### File: `crates/coral-glowplug/src/device/swap.rs`

#### Add Fallback Arm in Personality Mapping

In the `match` block that maps target strings to `Personality` variants, add a catch-all:

```rust
other => {
    let drm = self.sysfs.find_drm_card(&self.bdf);
    tracing::info!(
        bdf = %self.bdf, driver = other,
        "unknown driver — using Custom personality"
    );
    self.personality = Personality::Custom {
        driver_name: other.to_string(),
        drm_card: drm,
    };
}
```

### File: `crates/coral-glowplug/src/personality.rs` — Registry

Update `PersonalityRegistry::default_linux()` — the `known` list should still enumerate
well-known targets for discovery/completion, but it no longer gates what can be swapped:

```rust
pub fn default_linux() -> Self {
    Self {
        known: vec![
            "vfio", "vfio-pci", "nouveau", "amdgpu", "nvidia", "nvidia_oracle",
            "xe", "i915", "akida-pcie", "unbound",
        ]
        .into_iter()
        .map(String::from)
        .collect(),
    }
}
```

No change needed here — the registry serves discovery, not restriction.

## Phase 3: Trace-as-Default

### File: `crates/coral-glowplug/src/config.rs`

Add to the `DaemonConfig` struct:

```rust
#[derive(Debug, Clone, Deserialize)]
pub struct DaemonConfig {
    pub socket: String,
    pub log_level: Option<String>,
    pub health_interval_ms: Option<u64>,
    #[serde(default = "default_trace")]
    pub trace_default: bool,
    #[serde(default = "default_trace_dir")]
    pub trace_data_dir: Option<String>,
}

fn default_trace() -> bool { true }
fn default_trace_dir() -> Option<String> {
    Some("/var/lib/coralreef/traces".to_string())
}
```

### File: `crates/coral-glowplug/src/bin/coralctl/main.rs`

Change the `Swap` command:

```rust
Swap {
    bdf: String,
    target: String,
    /// Disable mmiotrace capture for this swap (trace is on by default)
    #[arg(long)]
    no_trace: bool,
},
```

And in the dispatch:

```rust
Command::Swap { bdf, target, no_trace } => {
    let trace = !no_trace; // default: true
    handlers_device::rpc_swap(&cli.socket, &bdf, &target, trace);
}
```

### File: `crates/coral-glowplug/src/socket/handlers.rs`

When dispatching `device.swap`, if the request does not include `trace`, use the config
default:

```rust
"device.swap" => {
    // ... existing target extraction ...
    let enable_trace = params.get("trace")
        .and_then(|v| v.as_bool())
        .unwrap_or(config.daemon.trace_default);
    slot.swap_traced(&target, enable_trace)?;
    // ...
}
```

### File: `crates/coral-ember/src/ipc.rs`

Similarly, Ember should default to `true` when no `trace` param is provided:

```rust
"ember.swap" => {
    let enable_trace = params.get("trace").and_then(|v| v.as_bool()).unwrap_or(true);
    // ...
}
```

### Config Update: `glowplug.toml`

```toml
[daemon]
socket = "/run/coralreef/glowplug.sock"
log_level = "info"
health_interval_ms = 5000
trace_default = true
trace_data_dir = "/var/lib/coralreef/traces"
```

## Test Plan

### Phase 1 Tests

```rust
#[test]
fn swap_accepts_unknown_driver_name() {
    // "custom_research_v1" should not be rejected
    let result = handle_swap_device("0000:99:00.0", "custom_research_v1", &mut map, false);
    // May fail at bind (no such module), but should NOT fail at validation
    assert!(!result.as_ref().is_err_and(|e| e.contains("unknown target")));
}

#[test]
fn swap_rejects_invalid_driver_name() {
    let result = handle_swap_device("0000:99:00.0", "../../../etc/passwd", &mut map, false);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("invalid driver name"));
}

#[test]
fn swap_rejects_empty_driver_name() {
    let result = handle_swap_device("0000:99:00.0", "", &mut map, false);
    assert!(result.is_err());
}
```

### Phase 2 Tests

```rust
#[test]
fn custom_personality_stores_driver_name() {
    let p = Personality::Custom {
        driver_name: "my_research_driver".to_string(),
        drm_card: None,
    };
    assert_eq!(p.name(), "my_research_driver");
    assert!(!p.provides_vfio());
    assert!(!p.supports_hbm2_training());
}

#[test]
fn personality_display_custom() {
    let p = Personality::Custom {
        driver_name: "amdgpu".to_string(),
        drm_card: Some("card2".to_string()),
    };
    assert!(format!("{p}").contains("reagent"));
}
```

### Phase 3 Tests

```rust
#[test]
fn trace_defaults_to_true_when_absent() {
    let params = json!({"bdf": "0000:03:00.0", "target": "nouveau"});
    // trace not specified → should default to config.trace_default (true)
}

#[test]
fn no_trace_flag_disables_trace() {
    let params = json!({"bdf": "0000:03:00.0", "target": "nouveau", "trace": false});
    // explicit false → no trace
}
```

### Integration Test (Manual)

```bash
# Bind a nonsensical driver (will fail at probe, but should NOT fail at validation)
coralctl swap 0000:03:00.0 amdgpu
# Expected: warn "not well-known", attempt bind, probe fails, GPU returns to vfio
# Trace artifacts still captured (mmiotrace of the failed probe attempt)

# Bind a well-known driver with default trace
coralctl swap 0000:03:00.0 nouveau
# Expected: trace ON, full capture, GPU returns to vfio

# Bind with trace disabled
coralctl swap 0000:03:00.0 nouveau --no-trace
# Expected: trace OFF, fast swap, no capture
```

## Dependency

This handoff depends on the **trace integration** handoff
(`CORALREEF_TRACE_INTEGRATION_HANDOFF.md`) being implemented first — specifically the
`trace.rs` module, `MmiotraceSession`, and `VendorLifecycle::trace_filter_ranges()`.

The open target changes (Phase 1-2) can be implemented independently of trace.

## Migration

- Existing `coralctl swap` calls with `--trace` continue to work (flag still accepted,
  just redundant since trace is now default)
- Existing RPC calls with `"trace": true` continue to work
- Existing RPC calls without `"trace"` key now get trace=true instead of false
- No config migration needed (`trace_default` has a serde default of `true`)
