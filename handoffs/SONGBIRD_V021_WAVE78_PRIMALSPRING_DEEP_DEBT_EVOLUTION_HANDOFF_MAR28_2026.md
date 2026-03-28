# SONGBIRD v0.2.1 — Wave 78: primalSpring Deep Debt Evolution Handoff

**Date**: March 28, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Session**: 21 (Wave 78)  
**Coverage**: 67.55% (up from 67.45%)  
**Tests**: 10,836 passed, 0 failed, 269 ignored

---

## primalSpring Phase 17 — All 3 Concrete Issues Resolved

1. **BIRDSONG BEACON `capabilities` FIELD** — Added `#[serde(default)]` to `GenerateBeaconRequest::capabilities` in `birdsong_handler.rs`. Callers who omit `capabilities` no longer get a serde "missing field" error. Downstream code already handles empty vec safely.

2. **MESH FLOW DOCUMENTED IN README** — Added "Sovereign Beacon Mesh" section to `README.md` with the validated call sequence (`mesh.init` → `mesh.announce` → `mesh.peers` → `mesh.status`) and link to `specs/SOVEREIGN_BEACON_MESH_SPECIFICATION.md`.

3. **BEARDOG DISCOVERY ERROR MESSAGES** — `discover_beardog_socket` in `birdsong_handler.rs` now collects all tried paths (BEARDOG_SOCKET env, XDG_RUNTIME_DIR, well-known fallback) and includes them in the error message for cross-gate diagnostic clarity.

---

## Coverage Expansion (+149 tests net)

| Module | Change | Focus |
|--------|--------|-------|
| `sovereignty/adapter.rs` | +15 tests | route_request, execute_request, create_routing_decision, compliance edges |
| `src/lib.rs` | +9 tests | REPL edge cases, error debug, CLI parsing edges |
| `security.rs` | Smart refactored 1209→950+263 lines | Protocol detection, discovery fallback, trait tests |
| `container.rs` | 3→18 tests | K8s detection, capability inference, environment resilience |
| `storage.rs` | +10 tests | Protocol detection, trait implementation |

---

## Hardcoding Evolution

- **Storage detection**: `songbird-compute-bridge` evolved from hardcoded `storage_gb: Some(100)` to actual `df`-based detection + `COMPUTE_STORAGE_GB` env override
- **HTTP discovery**: `songbird-cli/discovery.rs` stub replaced with real TCP-based HTTP/1.0 probe
- **Port centralization**: Remaining hardcoded external ports wrapped in `SafeEnv::get_port`
- **TorService**: `onion_address()` evolved from `"placeholder.onion"` → `Option<&str>` (None until BearDog descriptor published)
- **Genesis ceremony**: `mock_lineage` → `synthetic_lineage` with error-level degradation logging

## Idiomatic Rust Improvements

- `Box<dyn Error>` → `anyhow::Result` with `bail!` (compute-bridge registration)
- `SystemTime::duration_since(...).expect(...)` → `.unwrap_or_default()` (TLS clock-skew safe)
- `Box<dyn Error>` → typed `DiscoveryError` with `?` propagation (mDNS discovery)
- Inline format args cleanup

## Cleanup

- Moved `ecoPrimals/` (51MB, ~1023 files of session/archive fossil) from inside songbird to parent `ecoPrimals/archive/songbird-sessions-fossil-mar28-2026/`
- Moved `docs/DEEP_DEBT_SOLUTIONS.md` to fossil (historical reference)
- Updated README.md, CONTEXT.md, REMAINING_WORK.md with current metrics

---

## Remaining Coverage Gaps (Structural)

The gap between 67.55% and the 90% target is in areas requiring dedicated infrastructure:

| Category | Coverage | Blocker |
|----------|----------|---------|
| Bluetooth (USB/UART/BLE) | 0-45% | Requires hardware |
| CLI rendering/templates | 0-30% | Terminal/stdout capture needed |
| HTTP-calling methods | ~63% | Mock HTTP server infrastructure needed |
| Binary entry points | ~35% | main.rs delegation (structural) |

**Next steps for coverage**: Build a lightweight mock HTTP server test harness (similar to `mockito` pattern but in-process) to unlock the HTTP-calling paths in unified_adapter, discovery, and federation modules.

---

## Quality Gate Status

| Check | Status |
|-------|--------|
| `cargo fmt --check` | ✅ Clean |
| `cargo clippy --all-features --all-targets -D warnings` | ✅ Zero warnings (pedantic + nursery) |
| `cargo test --all` | ✅ 10,836 passed, 0 failed |
| `cargo doc --workspace --no-deps` | ✅ Clean |
| `overflow-checks` | ✅ Enabled in release builds |
| `#![forbid(unsafe_code)]` | ✅ All 30 crates |
| Production unwrap/panic/todo | ✅ Zero |
| Files >1000 lines | ✅ Zero |
