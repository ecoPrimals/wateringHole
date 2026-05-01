# petalTongue v1.6.6 — primalSpring Phase 56 Audit Response

**Date**: May 1, 2026
**Scope**: PG-48/GAP-12 resolution, deny.toml hardening, quality gate verification, doc refresh
**Tests**: 6,191+ passing (98 suites), 0 failures, 0 Clippy warnings, 0 fmt violations

---

## Context

primalSpring Phase 56 audit (April 30, 2026) identified the following petalTongue
gaps en route to BTSP Phase 3 readiness:

- **PG-48**: musl binary panics on `live` mode (winit event loop threading)
- **GAP-12**: Dashboard param schema docs (`session_id` + `bindings` required for
  `visualization.render.dashboard`)

Additionally, the permanent interstadial quality gate requires: `cargo deny check bans`
passes, `async-trait` eliminated, edition 2024 enforced.

---

## 1. PG-48: musl Binary Panic (Already Resolved)

**Status**: Confirmed resolved — no code changes needed.

The fix was already in place across three call sites:
- `src/ui_mode.rs`: `native_options_with_any_thread()` applies `with_any_thread(true)`
  for both X11 and Wayland on Linux
- `src/live_mode.rs`: Uses `native_options_with_any_thread()` from `ui_mode`
- `crates/petal-tongue-ui/src/backend/eframe.rs`: Independent `with_any_thread(true)` call

Workspace `Cargo.toml` explicitly selects `x11` + `wayland` eframe features and
lists `winit` as a direct dependency for platform extension traits.

primalSpring's own Explorer guide had already marked this "ADDRESSED".

---

## 2. GAP-12: Dashboard Param Schema Documentation

**Problem**: Consumers (primalSpring, healthSpring, springs) calling
`visualization.render.dashboard` needed wire-level JSON-RPC schema documentation
showing required and optional fields.

**Fix**: Added comprehensive module-level rustdoc to
`crates/petal-tongue-ipc/src/visualization_handler/types/dashboard.rs`:

- Full JSON-RPC request example with `session_id`, `title`, `bindings` array
  (including `TimeSeries` and `Gauge` examples)
- Required fields table: `session_id` (string), `title` (string), `bindings` (DataBinding[])
- Optional fields table with defaults: `domain` (null), `modality` ("svg"), `max_columns` (3)
- DataBinding variant listing (all 11 channel types)
- Full JSON-RPC response example
- Error codes table (-32602 for invalid params)

---

## 3. deny.toml: async-trait Regression Guard

**Problem**: Interstadial quality gate requires `async-trait` eliminated.
petalTongue had zero direct usage but no `deny.toml` ban to prevent regression.

**Fix**: Added `async-trait` to the `[bans] deny` list with wrappers for transitive
deps we cannot control: `axum`, `axum-core`, `opentelemetry_sdk`.

`cargo deny check bans` now passes clean.

---

## 4. Quality Gate Verification

| Check | Result |
|-------|--------|
| `cargo clippy --all-targets --all-features -- -D warnings` | 0 warnings |
| `cargo fmt --all -- --check` | 0 violations |
| `cargo deny check bans` | bans ok |
| `cargo test --all-features --workspace` | 6,191 passed, 0 failed |
| `cargo doc --no-deps` | 0 warnings |
| Edition | 2024 (`[workspace.package]`, `rust-version = "1.87"`) |
| `async-trait` direct usage | None (zero in `.rs` or `Cargo.toml`) |
| BTSP Phase 2 | Operational (20+ handshake tests, typed errors, provider delegation) |

---

## 5. BTSP Phase 3 Readiness Assessment

Phase 3 (encrypted channel) is deferred ecosystem-wide per primalSpring guidance:
"We'll provide a reference implementation via sourDough scaffold once BearDog
lands the client-side negotiation."

petalTongue's Phase 2 foundation is ready to absorb:
- `BtspHandshakeError` typed errors (thiserror enum)
- `btsp::server` with `exchange_hello`, `verify_challenge`, `perform_server_handshake`
- `btsp::json_line` with relay functions
- `btsp::client::provider_call` for BearDog delegation
- Framing protocol (`read_frame`/`write_frame`) for length-prefixed messages
- `BtspHandshakeConfig::from_env()` with 5-path provider socket discovery

When sourDough scaffold provides cipher negotiation, the integration points are:
1. Post-handshake `ReadHalf`/`WriteHalf` wrapping in `btsp::server`
2. Cipher suite selection in `btsp::client::provider_call` → `btsp.negotiate`
3. Key exchange via existing `exchange_hello` flow

---

## 6. Doc Refresh

- `README.md`: Test count 6,054→6,191+, BTSP Phase 1→Phase 2, deny.toml notes
- `wateringHole/petaltongue/README.md`: Test count 5,952→6,191+, 16→18 crates, date
  April 26→May 1, added BTSP/zero-copy/deny evolution items
- `wateringHole/petaltongue/PETALTONGUE_NEEDS_FROM_ECOSYSTEM.md`: Version v1.6.7→v1.6.6
  (matches workspace), date April 17→May 1
- `wateringHole/PRIMAL_REGISTRY.md`: petalTongue row updated (18 crates, 6,191+ tests,
  ~90% coverage, BTSP Phase 2, deny bans clean, async-trait banned)

---

## Remaining (Not petalTongue Debt)

| Primal | Gap | Status |
|--------|-----|--------|
| rhizoCrypt | PG-45: UDS no JSON-RPC response | Upstream |
| toadStool | PG-46: Slow initial socket response | Upstream |
| barraCuda | PG-47: `stats.entropy` not found | Upstream |

---

**Maintainer**: ecoPrimals / petalTongue
**License**: AGPL-3.0-or-later
