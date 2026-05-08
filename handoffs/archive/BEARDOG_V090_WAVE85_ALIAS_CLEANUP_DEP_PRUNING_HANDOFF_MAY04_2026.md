<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 85 Handoff

**Date**: May 4, 2026
**Branch**: `main`
**Trigger**: Continuous deep debt pass

---

## Summary

Wave 85 addresses naming confusion, unused dependencies, and dep tree bloat.

### 1. Stale Re-Export Aliases Removed

| Alias | Location | Issue | Fix |
|-------|----------|-------|-----|
| `SimplifiedBearDogConfig as UnifiedBearDogConfig` | `beardog_types` crate root | Name collision with the real `unified::UnifiedBearDogConfig` | Export `SimplifiedBearDogConfig` directly |
| `PrimaryUnifiedBearDogConfig` | `canonical::config::mod.rs` | Zero callers | Deleted |
| `WorkingUnifiedConfig` | `canonical::config::mod.rs` | 3 test callers | Migrated to `SimplifiedBearDogConfig` |
| `capability_routing as capability_router` | `beardog_core` lib.rs | 2 import sites | Migrated to `capability_routing` |

Stale comments in `canonical/mod.rs` and `QUICK_START_ZERO_HARDCODING.md` updated.

### 2. Unused `rsa` Removed from `beardog-security`

Zero `rsa::` usage in the crate. `rsa` remains in `beardog-core` and `beardog-tunnel`
where it is actively used for RSA key ops and TLS.

### 3. `x509-parser` Feature-Gated in `beardog-tunnel`

New `tls-x509` feature (default-on) gates `x509-parser` and the `tls.verify_certificate`
handler. Slim builds can disable it to shed the `nom`/`asn1-rs`/`der-parser`/`oid-registry`
transitive dep tree. Both default and `--no-default-features` builds compile cleanly.

---

## CI Results

| Gate | Result |
|------|--------|
| `cargo fmt -- --check` | Clean |
| `cargo clippy --workspace` | 0 warnings |
| `cargo test --workspace --lib` | 12,610 passed, 0 failed |

---

## Downstream Impact

- **primalSpring / all springs**: If you import `beardog_types::UnifiedBearDogConfig` at
  crate root, this was the **SimplifiedBearDogConfig** alias. Use
  `beardog_types::SimplifiedBearDogConfig` or the canonical path
  `beardog_types::canonical::config::SimplifiedBearDogConfig`.
  The real full config struct remains at
  `beardog_types::canonical::config::unified::UnifiedBearDogConfig` (unchanged).
- **`capability_router`**: Use `beardog_core::capability_routing` instead.
- **No wire protocol or IPC method changes.**
