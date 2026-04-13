<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 40: Deep Debt Sweep Handoff

**Date**: April 13, 2026
**Status**: Complete — all quality gates pass
**Triggered by**: Systematic deep debt audit and evolution sprint

---

## 1. Comprehensive Audit Results

| Category | Finding |
|----------|---------|
| **Unsafe code** | Zero. All 28 crates: `#![forbid(unsafe_code)]` |
| **Files > 1000 LOC** | Zero. Largest: `security.rs` at 971 |
| **`todo!()` / `unimplemented!()`** | Zero |
| **TODO/FIXME/HACK** | Zero |
| **Commented-out code** | Zero |
| **Production mocks/stubs** | Audited — all are legitimate architecture (compat shims, explicit `unsupported_operation`, placeholder `SocketAddr` for UDS) |
| **Hardcoded paths** | All centralized in Tier-5 FHS fallbacks with `resolve_*()` wrappers |

---

## 2. Changes Made

### Wildcard Imports Eliminated (3)

| File | Before | After |
|------|--------|-------|
| `pkcs11_discoverer/classification.rs` | `use crate::tunnel::hsm::types::capability::*` + `use crate::universal_hsm_discovery::*` | Explicit: `HsmCapabilities as UniversalHsmCapabilities`, `HsmTier`, `HsmType` |
| `pkcs11_discoverer/discoverer.rs` | `use crate::universal_hsm_discovery::*` | Explicit: `DiscoveredHsm`, `HsmEndpoint`, `HsmType`, `UniversalHsmDiscovery` |
| `pkcs11_discoverer/capability_profiles.rs` | `use crate::tunnel::hsm::types::capability::*` + `use crate::universal_hsm_discovery::*` | Explicit: 11 named types |

iOS Secure Enclave and Android StrongBox wildcards left as-is — modules are conditionally compiled (`#[cfg(target_os)]`) or not included in `mod.rs`.

### Lint Evolution (`#[allow]` → `#[expect]`)

| File | Attribute | Migration |
|------|-----------|-----------|
| `hybrid_intelligence/types/mod.rs` (×3) | `#[allow(deprecated)]` | `#[expect(deprecated, reason = "re-export of deprecated type...")]` |
| `entropy_orchestrator/orchestrator.rs` | `#[allow(unused_mut)]` | `#[expect(unused_mut, reason = "mutated inside #[cfg(feature = \"fido2\")] block")]` |
| `providers/pkcs11.rs` | `#[allow(unused_imports)]` | **Removed entirely** — `debug!` IS used; lint suppression was unnecessary |

Remaining `#[allow(deprecated)]` instances (environment.rs, monitoring_unified, production/mod.rs, trait_impl.rs, type_aliases.rs) have inline comments documenting why `#[expect]` would be **unfulfilled** (rustc does not emit `deprecated` on these specific patterns).

### Dead Cargo Features Removed (5)

| Crate | Feature | Reason |
|-------|---------|--------|
| `beardog-config` | `async` | Zero `#[cfg(feature = "async")]` in source; zero cross-crate references |
| `beardog-genetics` | `camera` | Zero cfg gates (only `microphone` is gated) |
| `beardog-adapters` | `advanced-registry` | Zero cfg gates; zero references |
| `beardog-discovery` | `network-scan` | Zero cfg gates; zero references |
| `beardog-tower-atomic` | `mock-primals` | Zero cfg gates; zero references |

### Dependency Alignment

| Issue | Resolution |
|-------|-----------|
| `mdns-sd` 0.19 in `beardog-capabilities` vs 0.11 everywhere else | Downgraded to 0.11 — eliminates double compilation |
| `thiserror` 1.0 optional dep in `beardog-utils` vs workspace 2.0 | Removed optional dep; `test-utils` feature now empty; test modules use dev-dep `thiserror` 2.0 |

---

## 3. Code Health

| Metric | Value |
|--------|-------|
| Tests | 14,780+ passing, 0 failed |
| Coverage | 90.51% (llvm-cov) |
| Clippy | 0 warnings (pedantic) |
| Format | Clean |
| Docs | 0 warnings |
| Rust Files | 2,150 |
| JSON-RPC Methods | 99 |
| `#[allow(` | 81 (was 86) |
| `#[expect(` | 646 (was 642) |

---

## 4. Remaining Low-Priority Debt

- **`#[allow(deprecated)]` on re-exports/definitions** — 7 instances with documented justification (rustc limitation). Will resolve when deprecated types are fully removed.
- **`#[allow(dead_code)]` in CLI handlers** — ~15 instances with `reason = "..."` for code reserved for future CLI subcommands (key_revoke, key_delegate, etc.).
- **iOS Secure Enclave wildcards** — Module is orphaned (not in `mod.rs`); wildcards are moot. Module itself needs platform integration work.
- **Ionic bond persistence** — NestGate/loamSpine integration (blocked on NestGate).
- **HSM/BTSP Phase 3 signing path** — Stubbed (awaiting hardware fleet).
