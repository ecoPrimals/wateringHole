# petalTongue v1.6.6 — Evolution Sprint 2 Handoff

**Date**: April 6, 2026
**Primal**: petalTongue (visualization)
**Version**: 1.6.6
**Scope**: primalSpring audit remediation, smart refactoring, zero-copy evolution, doc cleanup

---

## Summary

Two-phase evolution sprint completing the primalSpring downstream audit and
continuing deep debt elimination. All audit items resolved, all files under
1000 lines, all verification passing.

---

## Phase 1: primalSpring Audit Remediation

| Audit Item | Resolution |
|------------|-----------|
| `test_a_record_parse` failure | Fixed PII scrub regression: test fixture `[192, 168, 1, 100]` → `[192, 0, 2, 100]` |
| `health.readiness` missing `version`/`primal` | Added per `DEPLOYMENT_VALIDATION_STANDARD.md` v1.0 |
| `health.check` missing `primal` | Added `"primal": "petaltongue"` field |
| No `rust-version` | Added `rust-version = "1.87"` to `[workspace.package]` |
| No `CONTEXT.md` | Created per ecosystem pattern (17 primals/springs now have one) |
| No `[workspace.lints.rust]` | Added `unsafe_code = "forbid"` workspace-wide |
| `#[allow(clippy::unwrap_used)]` widespread | Migrated 33 to `#[expect]` with reasons; removed 6 where unused |
| No capability-domain symlink | Server creates `visualization.sock` → `petaltongue.sock` on start; cleans up on Drop |

---

## Phase 2: Deep Debt Evolution

### Capability-Based Naming (Final)

| Before | After |
|--------|-------|
| `DisplayCapabilities::toadstool()` | `DisplayCapabilities::network_display()` |
| `"squirrel-ui-adapter"` subscriber ID | `"ai-interaction-adapter"` |

Zero remaining primal-name violations in production code. All remaining primal
names are in doc comments (ecosystem context), test fixtures, or logging.

### Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `graph_manager.rs` | 806 lines | `graph_manager/mod.rs` (314) + `tests.rs` (462) |
| `headless_integration_tests.rs` | 834 lines | 5 themed test files (data_flow, panel, scenario, viewport, frame) |

Combined with prior sprint: `dns_parser/`, `spring_adapter/`, `constants/`,
`unix_socket_rpc_handlers/dispatch.rs` — all large files domain-decomposed.

### Zero-Copy RPC Evolution

| Handler | Change | Impact |
|---------|--------|--------|
| `visualization.render` | Shape check before consuming; no `req.params.clone()` | Eliminates full JSON clone on every render call |
| `visualization.render.scene` | `as_object_mut().remove("scene")` | Move instead of clone for scene graphs |
| `capabilities.sensory.negotiate` | `remove("input")` / `remove("output")` | Zero-copy deserialization of capability sets |
| `ui_config` / `thresholds` extraction | `as_object_mut().remove()` | Move instead of clone for config objects |

### Documentation Cleanup

| Area | Changes |
|------|---------|
| `START_HERE.md` | Updated date, `graph_engine/` path, MSRV reference |
| `CHANGELOG.md` | Added [Unreleased] entries for all evolution work |
| `ENV_VARS.md` | Updated date |
| Logging | "Toadstool WASM" → "Network display"; "Toadstool backend" → "Discovered display" |
| Stale comments | Removed `REMOVED:` migration note, fixed broken `docs/` paths |

---

## Verification

| Check | Result |
|-------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | PASS |
| `cargo test --workspace` | ALL PASS (0 failures) |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` | PASS |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| File sizes | All under 1,000 lines (largest: `primitive.rs` at 816) |
| `unsafe` blocks | Zero |
| Primal-name violations | Zero in production routing |

---

## Remaining Documented Debt (Accepted)

| Item | Status | Notes |
|------|--------|-------|
| Audio socket/direct backends | Stub (`is_available = false`) | Graceful degradation by design |
| `ProviderCache` (`cache.rs`) | Complete, test-only | Ready for integration when needed |
| `base64` 0.21 vs 0.22 duplicate | Upstream `ron`/`egui` | Resolves when egui upgrades |
| `winnow` duplicate | Upstream `toml`/`winit` | Resolves with ecosystem alignment |
| Haptic / VR modalities | `ModalityStatus::Unavailable` | Spec'd but not yet implemented |
| `missing_docs` suppressed in discovery + UI | `#![expect(missing_docs)]` | Incremental doc coverage |
