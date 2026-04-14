# petalTongue v1.6.6 — Deep Debt Sprint 5 Handoff

**Date**: April 11, 2026  
**Scope**: primalSpring PT-04/06/09/12 resolution, deep debt execution, smart refactoring  
**Status**: All 4 primalSpring audit gaps resolved + deep debt execution complete

---

## primalSpring Audit Gaps Resolved (April 11)

### PT-06 (Low): callback_tx push delivery — VERIFIED + IMPROVED

- `UnixSocketServer::new()` wires `callback_tx` via `spawn_push_delivery()`
- Startup log confirms activation: `"📡 PT-06: push delivery activated"`
- `petaltongue ui` UniBin path intentionally skips IPC (documented)

### PT-09 (Low): BTSP Phase 2 handshake — WIRED

- `log_handshake_policy()` now called at `UnixSocketServer::start()`
- Domain symlinks use `btsp::domain_symlink_filename()` for family-scoped naming
- `Drop` impl cleans up correct family-scoped symlink
- Production logs WARN when BearDog handshake not yet enforced

### PT-04 (Low): HTML export — VERIFIED GREEN (5/5 tests)

- `pt04_html_export_product_validation` (unit)
- `test_html_export_e2e_pt04_full_pipeline` (integration)
- `test_html_export_to_stdout` / `test_html_export_to_file` (e2e binary)
- `test_validate_standalone_html_export` (edge cases)

### PT-12 (Low, acceptable): eframe/egui/glow GUI deps — DOCUMENTED

- Feature-gated behind `ui` feature (`default = ["ui"]`)
- PT-12 documentation added to root `Cargo.toml` and `petal-tongue-headless/Cargo.toml`
- Headless path has zero GUI/native display dependencies

---

## Deep Debt Execution

### Dependency Evolution

- **`anyhow` eliminated from ALL production deps** including root binary → `[dev-dependencies]`
- **`ring` confirmed absent** from dep tree (TLS-free `reqwest`, `deny.toml` bans enforced)
- **`cargo deny check`** passes clean (advisories, bans, licenses, sources all ok)

### Self-Knowledge Enforcement

- `BEARDOG`/`SONGBIRD` constants gated behind `#[cfg(feature = "test-fixtures")]`
- Production builds have zero compile-time knowledge of other primal identities
- All other-primal string literals verified test-only (zero production routing by identity)
- `biomeOS` references classified as socket-directory convention (acceptable)

### Smart File Refactoring (9 files, sprint 5)

| File | Before | After (prod) |
|------|--------|--------------|
| `sensory_capabilities/mod.rs` | 723 | **123** |
| `unix_socket_rpc_handlers/mod.rs` | 691 | **216** |
| `audio_sonification.rs` | 799 | **278** |
| `modality/svg.rs` | 707 | **276** |
| `engine.rs` | 792 | **325** |
| `visual_flower.rs` | 723 | **301** |
| `primal_details.rs` | 735 | **348** |
| `neural_graph_client.rs` | 745 | **361** |
| `provenance_trio.rs` | 740 | **362** |

**Total across sprints 4–5**: 20 files refactored. Max production file: 414 lines.

### Bug Fix

- Flaky test `test_resolve_instance_id_error_message_invalid` fixed with `XDG_DATA_HOME` env isolation

### Codebase Health (confirmed clean)

| Dimension | Status |
|-----------|--------|
| Unsafe code | Zero blocks, `forbid(unsafe_code)` on all 21 crates |
| TODO/FIXME/HACK | Zero markers in `.rs` files |
| Production clone density | Minimal (2 necessary ownership clones) |
| Mock isolation | All mocks in `#[cfg(test)]`, sandbox, or feature-gated |
| `format!` waste | Zero literal-only calls |
| `ring` / C deps | Not in dep tree |

---

## Compliance Matrix Delta

| Tier | Before | After | Notes |
|------|--------|-------|-------|
| T3 IPC | A | A | PT-06/09 resolved; BTSP handshake logged |
| T8 Presentation | B | **A** | All `#[allow]` justified; docs updated |

---

## Verification Gates (all green)

```
cargo fmt --check                                          ✅
cargo clippy --workspace --all-targets --all-features -Dw  ✅ (0 warnings)
cargo test --workspace --all-features                      ✅ (0 failures)
cargo deny check                                           ✅ (advisories, bans, licenses, sources ok)
```

---

## Remaining Backlog

- tarpc feature-gating (contained to 4 files; deferred)
- Cross-compilation CI (musl/ARM targets)
- Benchmark regression gates in CI
- cargo-fuzz harness for JSON-RPC parser
- E2E test expansion (62 e2e tests; more scenarios possible)
- 10+ specs in Design/Planning phase
