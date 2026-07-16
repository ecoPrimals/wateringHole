# cellMembrane Wave 143b Deep Debt

**Date**: Jul 16, 2026 | **Wave**: 143b | **From**: eastGate cellMembrane team
**Commit**: `e1b056e` | **Tests**: 1,073 | **Clippy**: 0 warnings

---

## Delivered

### CSPRNG → `getrandom` (Security Evolution)

The non-Unix CSPRNG fallback (BLAKE3-derived from pid+timestamp, with cyclic
byte repetition for >32 byte buffers) was a known weak point with an explicit
TODO comment. Replaced with `getrandom` crate — single code path, OS-native
RNG on all platforms. Eliminates the `#[cfg(unix)]`/`#[cfg(not(unix))]` split
in `gate/nucleus.rs`.

### Service Filter → Registry-Derived

`DEFAULT_SERVICE_FILTER` (hand-maintained grep regex) replaced by
`MembraneService::build_service_filter()` which generates the filter
from the service registry + `INFRA_SERVICE_FILTER_EXTRAS` (forgejo,
fail2ban). New primals added to the registry automatically appear in
the filter. Tests verify every registry entry is covered.

### GLACIAL_SHIFT_TRACKER Trimmed (554→77 lines)

Full wave-by-wave history (Waves 50–142b) archived to
`infra/fossilRecord/cellMembrane/GLACIAL_SHIFT_TRACKER_FULL_HISTORY_wave142b.md`.
Active tracker now contains only: current status, last 2 wave entries,
stadial criteria, sovereignty table, and Dark Forest compliance.

---

## CAC Status Update (L3 + L6)

The blurb marks L3 (Heads TreeParity) and L6 (Cascade tree-parity policy)
as "FRAGO issued" but both are **SOLVED** by Wave 142b:

- **L3**: `freshness.rs::publish_gate_heads()` uses `git_rev_parse_tree()`
  (tree hashes, not commit SHAs) since Wave 142b.
- **L6**: `sync_engine.rs::try_local_tree_parity()` checks tree parity
  before impulse/policy dispatch. `try_pull_converge()` checks tree parity
  after rebase conflict.

Blurb CAC table should update L3 and L6 to SOLVED.

---

## Remaining cellMembrane Deep Debt (P3)

| Item | Priority | Notes |
|------|----------|-------|
| `build_err` → `impl Into<String>` | P3 | 4 call sites with `ShadowError::Build(format!(...))` |
| Cytoplasm static IP table → manifest-only | P3 | Requires topology migration |
| Named Pipe transport implementation | P3 | Windows parity — stub exists |
| ribocipher nuclear tier | P3 | Deferred until per-peer lineage keys |
