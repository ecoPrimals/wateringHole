# petalTongue v1.6.6 — BTSP + Deep Debt Sprint 4 Handoff

**Date**: April 9, 2026  
**Scope**: PT-04, PT-06, PT-08, PT-09, deep debt execution  
**Status**: All 4 primalSpring audit gaps resolved + 6 waves of debt execution

---

## Gaps Resolved (primalSpring audit)

### PT-08 (HIGH): BTSP Phase 1 — DONE

- `validate_insecure_guard()` in `petal-tongue-ipc/src/btsp.rs`
- `FAMILY_ID` + `BIOMEOS_INSECURE=1` → FATAL, refuses to start
- Family-scoped socket: `petaltongue-{family_id}.sock` in production posture
- Domain symlink: `visualization-{family_id}.sock` per Self-Knowledge Standard
- Guard called in `src/main.rs` before any subcommand
- 14 unit tests covering all posture permutations

### PT-09 (MEDIUM): BTSP Phase 2 Handshake Stub — DONE

- `HandshakePolicy::Open` (dev) / `PendingBearDog { family_id }` (production)
- `log_handshake_policy()` at `UnixSocketServer::start()` — warns when production FAMILY_ID
  is set but BearDog enforcement not yet active
- Ready for BearDog `btsp.session.create` / `btsp.session.verify` integration

### PT-04: HTML Export Product Validation — DONE

- `pt04_html_export_product_validation` end-to-end test
- Full pipeline: SVG → wrap_svg_in_html → validate → write → read-back → structural check
- Tests: DOCTYPE, html/head/body/style tags, charset, viewport meta, SVG embedding, round-trip

### PT-06: callback_tx Push Delivery — DONE (verified, not a gap)

- Push delivery IS wired in all JSON-RPC paths via `UnixSocketServer::new()`
- Server mode and UI binary both get `callback_tx` at startup
- Modes without IPC (web/tui/headless/ui) documented as intentionally push-free

---

## Deep Debt Execution (6 waves)

### Wave 1: Standards Compliance
- **`anyhow` eliminated** from 6 production crate deps → dev-deps or removed
- **`#[allow(` → `#[expect(`**: 9 of 11 migrated with reasons; 2 `dead_code` remain (correct)

### Wave 2: Clone/Allocation Density
- `property_panel.rs`: clone_from, in-place get_mut (no per-frame clones)
- `engine.rs`: Arc::clone replaces self.clone(); single name string built once
- `structure.rs`: `impl Into<String>` for static suggestions
- `modality.rs`: returns `&'static str` instead of allocating

### Wave 3: Smart File Refactoring
- 11 files split (tests extracted to siblings)
- Max file: 799 lines (down from 790 pre-split)
- Files: builders, data_binding, basic_charts, interaction, tarpc_types,
  property_panel, main, live_data, unix_socket_server, chart_renderer, describe

### Wave 4: Audio Backend Evolution
- `audio-socket` and `audio-direct` features (opt-in, not default)
- Stubs return typed AudioError variants
- Module docs describe implementation requirements

### Wave 5: Sandbox Cleanup
- mock-biomeos: capability_names constants, discover_primal_socket, .expect()

### Wave 6: Documentation
- CHANGELOG, README, ENV_VARS, START_HERE updated
- BTSP env vars documented (BIOMEOS_INSECURE, FAMILY_ID precedence)

---

## Compliance Matrix Delta

| Tier | Before | After | Notes |
|------|--------|-------|-------|
| T1 Build | A | A | No change |
| T2 UniBin | B | B | aarch64 musl still pending |
| T3 IPC | B | **A** | BTSP Phase 1 socket scoping + domain symlink |
| T4 Discovery | C | C | 982 refs still high (constants-based, not routing) |
| T8 Presentation | C | **B** | CONTEXT.md exists; 3 #[allow(] down from 32 |
| T9 Deploy | C | C | musl aarch64 still pending |

---

## Wire Standard Compliance

- **L2/L3**: PASS (was already fine per audit)
- **BTSP Phase 1**: PASS (this sprint)
- **BTSP Phase 2**: STUB (handshake policy logged; BearDog integration pending)

---

## Remaining Backlog

- Cross-compilation CI (musl aarch64 target)
- Benchmark regression gates in CI
- cargo-fuzz harness for JSON-RPC parser
- E2E test expansion (201 lines thin)
- 10+ specs in Design/Planning phase
- Discovery ref count reduction (982 → lower; constants-based evolution)

---

## Verification Gates (all green)

```
cargo fmt --check                                          ✅
cargo clippy --workspace --all-targets --all-features -D warnings  ✅
cargo test --workspace --all-features                      ✅ (0 failures)
cargo doc --workspace --no-deps                            ✅
cargo deny check                                           ✅
```
