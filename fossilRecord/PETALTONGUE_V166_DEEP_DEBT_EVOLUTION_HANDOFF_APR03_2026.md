# petalTongue v1.6.6 — Deep Debt Evolution & Capability Compliance Handoff

**Date**: April 3, 2026
**Primal**: petalTongue (visualization)
**Version**: 1.6.6
**Scope**: Deep debt elimination, capability-based discovery compliance, smart refactoring, zero-copy evolution

---

## Summary

Multi-pass evolution sprint addressing all gaps identified in the primalSpring downstream audit. petalTongue is now fully capability-based discovery compliant per `CAPABILITY_BASED_DISCOVERY_STANDARD.md` v1.2 — zero primal-named modules, zero primal-specific env vars in production routing, zero hardcoded cross-primal identity coupling.

### Audit Gap Resolution

| Audit Item | Status |
|------------|--------|
| PT-04: `ExportFormat::Html` headless graph render | **CLOSED** — `visualization.render.graph` now supports `format: "html"` |
| PT-06: `callback_tx` push wiring | **CLOSED** — GUI broadcast → push delivery thread fully wired |
| ~20 files with primal names | **CLOSED** — All primal-named modules renamed to capability-based |
| 24 env-var refs | **CLOSED** — No primal-specific env vars remain in production routing |

---

## Capability-Based Discovery Compliance

### Module Renames (primal identity → capability domain)

| Before | After | Rationale |
|--------|-------|-----------|
| `squirrel_adapter.rs` / `SquirrelAdapter` | `ai_adapter.rs` / `AiAdapter` | AI interaction adapter — capability, not primal |
| `toadstool.rs` | `discovered_display.rs` | Capability-discovered display backend |
| `toadstool_v2.rs` | `discovered_display_v2.rs` | Capability-discovered display V2 (tarpc) |
| `pub mod toadstool_compute` | `pub mod gpu_compute` | GPU compute provider — capability, not primal |

### Identity Coupling Eliminated

- Removed 13 unused primal name constants from `primal_names` (kept only `PETALTONGUE` + `BIOMEOS`)
- Remaining primal name references are exclusively in doc comments explaining ecosystem architecture (acceptable per standard)
- Feature flag `ui-toadstool` renamed to `discovered-display`

---

## Zero-Copy & Performance Evolution

| Area | Change | Impact |
|------|--------|--------|
| `SpringDataAdapter::adapt()` | `&Value` → owned `Value` | Eliminates 4 deep JSON clones on hot path |
| `adapt_game_scene` / `adapt_soundscape` | `.get().cloned()` → `.remove()` | Move instead of clone for scene/definition fields |
| Audio RPC handler | `definition.clone()` → `as_object_mut().remove()` | Zero-copy definition extraction |
| IPC error path | `ref err` + `.clone()` → `err` (move) | Move ownership into error variant |
| `Box<dyn Error>` in discovery | → typed `Integration(String)` + `Upstream(String)` variants | Eliminates heap-allocated trait objects |
| Retry policy | `Box<dyn Error>` bound → `Into<DiscoveryError>` | Type-safe error propagation, no boxing |

---

## Smart Refactoring

Three large files decomposed by domain, not arbitrary split:

### `dns_parser.rs` (759 → directory module)

| File | Lines | Domain |
|------|-------|--------|
| `dns_parser/mod.rs` | 12 | Barrel re-exports |
| `dns_parser/header.rs` | 97 | DNS header flags, opcodes, response codes |
| `dns_parser/name.rs` | 133 | Label compression, name encoding/decoding |
| `dns_parser/record.rs` | 546 | SRV, TXT, A, AAAA, ResourceRecord parsing |

### `spring_adapter.rs` (728 → directory module)

| File | Lines | Domain |
|------|-------|--------|
| `spring_adapter/mod.rs` | 195 | Facade: detect_format, adapt, simple formats |
| `spring_adapter/game_channel.rs` | 146 | ludoSpring GameChannelType + 7 variant mapping |
| `spring_adapter/eco_timeseries.rs` | 59 | ecoPrimals/time-series/v1 envelope |
| `spring_adapter/helpers.rs` | 22 | Array/string extraction utilities |
| `spring_adapter/tests.rs` | 348 | All unit tests |

### `unix_socket_rpc_handlers/mod.rs` (769 → 691 + 87)

| File | Lines | Domain |
|------|-------|--------|
| `mod.rs` | 691 | Struct, constructors, helpers, submodule declarations |
| `dispatch.rs` | 87 | `handle_request` method routing |

---

## Dead Code & Feature Flag Cleanup

| Item | Action |
|------|--------|
| `audio_playback.rs` (orphaned, not in module tree) | Deleted |
| `audio_providers/` (5 files, deprecated) | Deleted (previous pass) |
| Feature `ecoprimal` (empty, no cfg refs) | Removed |
| Feature `framebuffer-direct` (no cfg refs) | Removed |
| Feature `ui-toadstool` | Renamed to `discovered-display` |
| `unreachable!` in `biomeos_ui_manager.rs` | → `tracing::error!` + graceful return |
| 13 unused primal name constants | Removed |

---

## Dependency Evolution

| Change | Rationale |
|--------|-----------|
| `crossterm` 0.28 → 0.29 in `petal-tongue-ui` | Aligns with `petal-tongue-tui` + `ratatui 0.30`, eliminates duplicate version |
| `ratatui` 0.28 → 0.30 (previous pass) | Resolves `foldhash` dual-version from `lru` |
| `examples/benches` `#[allow]` → `#[expect]` with reasons | Modern idiomatic Rust lint evolution |
| `cargo deny check` | Clean: advisories ok, bans ok, licenses ok, sources ok |

### ecoBin Compliance Confirmed

- Zero `ring`, `openssl`, `native-tls`, `aws-lc-rs` in dependency graph
- `reqwest` runs TLS-free (`default-features = false`)
- Crypto via RustCrypto stack (`aes-gcm`, `sha1`)
- `blake3` with `default-features = false` (pure Rust)
- `deny.toml` guards enforce banned C crypto/TLS crates

---

## Documentation Cleanup

| File | Changes |
|------|---------|
| `START_HERE.md` | Updated module inventory: `constants/`, `dns_parser/`, capability count, `ai_adapter` reference |
| `*.rs` comments | Removed 15+ stale `NEW:` / `EVOLUTION:` / `REMOVED:` migration labels |
| Feature docs | Updated `ui-toadstool` → `discovered-display` in backend module docs |
| Doc references | Fixed "Toadstool backend" → "discovered display backend" in eframe docs |
| Example docs | Updated `framebuffer-direct` feature reference |

---

## Verification

| Check | Result |
|-------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | PASS |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | PASS |
| `cargo test --workspace` | ALL PASS (0 failures) |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| SPDX headers | All `.rs` files |
| File sizes | All under 1,000 lines |
| `unsafe` blocks | Zero |
| `todo!()` / `unimplemented!()` | Zero in production |
| `unreachable!()` in production | Zero (replaced with graceful error) |

---

## Remaining Documented Debt (Accepted)

These items are intentional staging or upstream-blocked, not violations:

| Item | Status | Notes |
|------|--------|-------|
| `missing_docs` suppressed in discovery + UI crates | `#![expect(missing_docs)]` | Incremental doc coverage — not a compliance issue |
| `ProviderCache` (`cache.rs`) | `#[cfg(test)]` only | Complete, well-tested, ready for integration when needed |
| Audio socket/direct backends | Stub (`is_available = false`) | Graceful degradation by design; PipeWire/ALSA protocol not implemented |
| `base64` 0.21 vs 0.22 duplicate | Upstream `ron`/`egui` | Resolves when egui upgrades |
| `winnow` duplicate | Upstream `toml`/`winit` | Resolves with ecosystem alignment |
| Haptic / VR modalities | `ModalityStatus::Unavailable` | Spec'd but not yet implemented |

---

## IPC Compliance Matrix Update

petalTongue capability-based discovery status should be updated from **P (Partial)** to **C (Conformant)**:

- Zero primal-specific env vars in production routing
- Zero primal-named modules/types for generic roles
- Zero hardcoded primal names in discovery or routing code
- `discover_primal_socket()` uses generic mechanism (identity-based fallback tier, per standard)
- All remaining primal name references are in doc comments (acceptable per checklist)
