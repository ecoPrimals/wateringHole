<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 97 Handoff

**Date**: May 11, 2026
**Phase**: 10 — Iteration 97
**Theme**: Smart Refactoring + Stub Evolution + Comprehensive Debt Audit

---

## Completed

### Smart File Refactoring (>800L)

| File | Before | After | Strategy |
|------|--------|-------|----------|
| `nv/ioctl/mod.rs` | 929L | 655L + `gem.rs` (299L) | GEM buffer management (alloc, mapping, pushbuf submission) extracted to `nv/ioctl/gem.rs`. Natural domain boundary — GEM ops vs channel management |
| `vfio/channel/mod.rs` | 896L | 594L + `kepler_channel.rs` (305L) | Kepler (GK110/GK210) channel creation extracted to `vfio/channel/kepler_channel.rs`. Architecture-specific — Kepler 2-level page tables vs Volta+ 5-level |

### Stub Evolution

- `IntelDevice::stub()` → `IntelDevice::host_emulated()`: removed "stub" naming from production API. Method now documented as host-memory emulation for testing the vendor-agnostic dispatch pipeline. 8 call sites updated across `src/intel/mod.rs` and `tests/e2e_pipeline.rs`.

### Comprehensive Audit (Zero Debt Confirmed)

| Category | Result |
|----------|--------|
| `Result<_, String>` in production | Zero |
| `.unwrap()` in library code | Zero |
| `eprintln!` in production library | Zero (CLI binaries retain idiomatic usage) |
| `async_trait` / `lazy_static` | Zero direct usage |
| Mocks in production | Zero (`MockWritesMutexPoisoned` is `#[cfg(test)]` gated) |
| `#[expect(dead_code)]` annotations | All 45+ verified valid (DMA lifetime, HW register maps, WIP, generated tables) |
| `deny.toml` enforcement | Active: no `openssl`, `ring`, `cmake`, `bindgen`, `*-sys` (except `linux-raw-sys` via rustix) |
| TODO/FIXME/HACK markers | Zero in committed `.rs` code |
| Commented-out code | Zero |

### Tests

- 4754 passing, 0 failures, 181 ignored (hardware-gated)
- Zero clippy warnings (pedantic + nursery)
- Zero fmt drift

---

## Remaining Debt (from primalSpring audits)

| Item | Priority | Status |
|------|----------|--------|
| Transitive `libc` via tokio/mio | P3 | Upstream — resolves when mio#1735 ships rustix backend. No action from coralReef |
| Coverage ~65% → 90% target | Medium | coral-driver hardware code is the ceiling (~82% non-hardware). Requires GPU hardware CI |
| PTX emitter SM120/Blackwell | Low | WIP in compiler — not blocking compositions |
| UVM hardware validation (RTX 5060) | Low | Dispatch pipeline code-complete, needs on-site hardware |
| Falcon boot FBP=0 resolution | Low | Sovereignty research frontier |
| coral-gpu sovereign path | Low | Replacing wgpu — in progress |
| Compute Trio toadStool absorption | Stadial | coral-ember, coral-glowplug, coral-driver hardware modules → toadStool. coralReef monitors for vestigial removal |

---

## Ecosystem Context

- **Wire Standard L3**: Complete — `capabilities.list` includes `protocol: "jsonrpc-2.0"`, `transport: ["uds", "tcp", "tarpc"]`
- **BTSP Phase 3**: Complete — encrypted frame loop live, `chacha20-poly1305` AEAD, HKDF-SHA256 key derivation
- **JH-0 MethodGate**: Complete — pre-dispatch authorization, `-32001 PERMISSION_DENIED`, bearer token extraction
- **Compute Trio Gate 1**: Satisfied — `shader.compile.capabilities` returns `targets` array; response includes `binary_b64`, `target`, `shader_info` with full metadata
- **primalSpring assessment**: "CLEAN (stadial only)" — no actionable code quality debt

---

## Files Changed

- `crates/coral-driver/src/nv/ioctl/mod.rs` — GEM extraction, re-exports added
- `crates/coral-driver/src/nv/ioctl/gem.rs` — **New**: GEM buffer management submodule (299L)
- `crates/coral-driver/src/vfio/channel/mod.rs` — Kepler extraction
- `crates/coral-driver/src/vfio/channel/kepler_channel.rs` — **New**: Kepler channel creation submodule (305L)
- `crates/coral-driver/src/intel/mod.rs` — `stub()` → `host_emulated()` rename
- `crates/coral-driver/tests/e2e_pipeline.rs` — Call site updates for `host_emulated()`
- `CHANGELOG.md`, `STATUS.md`, `EVOLUTION.md`, `WHATS_NEXT.md` — Updated for Iter 97
