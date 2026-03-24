# groundSpring V121 — Deep Debt + Ecosystem Absorption Handoff

**Date**: March 23, 2026
**From**: groundSpring team
**To**: All springs, barraCuda, toadStool, biomeOS, ecosystem primals

## Summary

V121 executes deep technical debt resolution and absorbs cross-ecosystem
patterns identified in the V120 audit. Focus areas: smart refactoring (not
arbitrary splits), lint hardening, capability-based evolution, and provenance
trio wiring.

## Changes

### Smart Refactoring
- **`biomeos/mod.rs`** 631 → 232 lines: extracted `storage.rs`, `compute.rs`,
  `registration.rs`, `health.rs`, `routing.rs`, `client_tests.rs`
- **`stats/agreement.rs`** 534 → directory: `coefficient.rs`, `error_metrics.rs`,
  `efficiency.rs`, `willmott.rs`, `hit_rate.rs` with zero public API change

### Ecosystem Absorption
- **`normalize_method()`** — strips `groundspring.`/`barracuda.` legacy prefixes
  (barraCuda v0.3.7 / wetSpring V132 pattern)
- **5-tier socket discovery** — env → XDG family → XDG flat → socket-registry.json
  → temp_dir (biomeOS V266 pattern)
- **`NdjsonSink<W>`** — machine-readable NDJSON validation output (wetSpring V132)
- **`IpcError::is_recoverable()`** — typed recovery classification (wetSpring/healthSpring)
- **Provenance trio `run_lifecycle()`** — session lifecycle pattern (primalSpring V0.3.0)
- **MCP `capability_registry.toml`** — 16 tool definitions (airSpring V0.10)

### Lint Hardening
- Workspace-level `deny` for `clippy::unwrap_used` / `clippy::expect_used`
- All test modules annotated with `#[expect]`
- MSRV 1.85 → 1.87

### Hardcoding → Capability-Based
- `/tmp` → `std::env::temp_dir()` in discovery fallback
- Server-side timeouts env-driven (shared with client)
- `is_enabled()` accepts `"biomeos"` / `"true"` / `"1"`

## Patterns Worth Absorbing

### For barraCuda
- **`normalize_method()` is now ecosystem-standard** — barraCuda should ensure
  its dispatcher also strips legacy prefixes consistently
- **`NdjsonSink`** pattern is useful for validation tools — consider absorbing
  into `barracuda::validation`
- **`IpcError::is_recoverable()`** — typed error classification for IPC clients

### For toadStool
- **5-tier discovery** with socket-registry.json — toadStool's device discovery
  should support the same registry for hardware capability advertisements
- **`capability_registry.toml`** — MCP manifest standard that all primals
  should adopt for Squirrel tool discovery

### For biomeOS
- groundSpring now fully wired for 5-tier discovery; **socket-registry.json**
  writes should be part of biomeOS startup when managing primal sockets
- `normalize_method()` should move to the biomeOS dispatch core so all
  primals inherit legacy prefix handling

### For All Springs
- **Workspace lint `deny` for unwrap/expect** is the new standard. Test
  modules use `#[expect(clippy::unwrap_used)]` with reason strings
- **`NdjsonSink`** for CI consumption — stdout sink for humans, NDJSON
  sink for machines, `NullSink` for benchmarks
- **Provenance trio lifecycle** — `start_session → store → commit → attribute`
  with graceful degradation at each step

## Quality Metrics
- 691 lib tests, 0 failures
- 0 clippy warnings (pedantic + nursery)
- 0 doc warnings
- 0 unsafe code in lib
- 0 unwrap/expect in production code
- 0 TODOs/FIXMEs in library code
- ≥92% library line coverage

## Upstream Issues
- **barraCuda compile without `gpu` feature** still has the `rel_tolerance`
  missing-field error — P0 upstream fix needed
- **wgpu 29** available (MSRV 1.87 matches); coordinated upgrade with
  barraCuda team when ready

## Next
- Dep bumps: `tracing-subscriber` 0.3.23, `tempfile` 3.27.0
- wgpu 28 → 29 (coordinated with barraCuda)
- TensorSession readiness (ludoSpring GpuContext pattern)
- Further file refactoring: `spectral_recon.rs` (625 lines), `drift/mod.rs` (564)
