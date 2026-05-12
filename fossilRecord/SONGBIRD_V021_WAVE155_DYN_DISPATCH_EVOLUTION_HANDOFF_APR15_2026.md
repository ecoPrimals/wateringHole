# Songbird v0.2.1 — Wave 154–155 Handoff

**Date**: April 15, 2026
**From**: Songbird deep debt pass (Waves 154–155)
**Scope**: Mock isolation, dead deps, lint hygiene, `dyn` dispatch evolution

---

## Wave 154 — Mock Isolation, Dead Deps, Lint Hygiene

### Changes
- **Feature-gated production stubs**: `StubAllow`, `StubDeny`, `StubPassthrough`, `StubMockEncrypted` in `songbird-lineage-relay` now behind `#[cfg(any(test, feature = "test-mocks"))]` — zero mocks in production binary
- **Removed dead deps**: `regex` from `songbird-types` (zero usage) and `songbird-cli` (orphaned consumer)
- **Deleted debris**: `security_audit.rs` — orphaned, never compiled, ~50 syntax errors
- **Removed alias**: `LegacySecurityTlsCryptoClient` deprecated alias (defined but never referenced)
- **Fixed deprecated usage**: test assertion migrated from `constants::DEFAULT_HTTP_PORT` → `defaults::ports::DEFAULT_HTTP_PORT`
- **Lint hygiene**: blanket `#![cfg_attr(test, allow(...))]` in `universal-ipc` and `lineage-relay` given reason strings

## Wave 155 — `dyn` Dispatch Evolution

### 6 production `dyn` sites eliminated

| Crate | Before | After |
|-------|--------|-------|
| `songbird-http-client` | `&mut dyn Iterator` | `impl Iterator` (monomorphized) |
| `songbird-orchestrator` | `Box<dyn Error + Send + Sync>` | Concrete `MetricsError` |
| `songbird-universal` (transport) | `Pin<Box<dyn Future>>` (3 helpers) | Inline `async` match (production); boxed recursion test-only |
| `songbird-universal` (discovery) | `impl Fn → Pin<Box<dyn Future>>` | Generic `F: Fn → Fut` |
| `songbird-registry` (plugin) | `Box<dyn ComposablePlugin>` | `RegisteredPlugin` struct |
| `songbird-registry` (traits) | `&dyn Composable` | `&impl Composable` |

### Remaining `dyn` (architectural, kept)
- `Pin<Box<dyn Stream<Item = ServiceEvent> + Send>>` — standard async watch stream; all backends return `stream::empty()`; will evolve to enum when real streams ship
- `Box<dyn SerialPort>` — external `serialport` crate API
- `Arc<dyn Fn(&str) → Result<String, VarError>>` — intentional test env injection

---

## Verification

| Check | Result |
|-------|--------|
| `cargo check --workspace` | Clean |
| `cargo clippy --workspace -- -D warnings` | Zero warnings |
| `cargo fmt --all --check` | Clean |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace --lib` | **7,385 passed**, 2 failed (pre-existing env-dependent birdsong beacon), 22 ignored |

## Next Targets

- `serde_yaml` → TOML-only (5+ call sites in config/discovery)
- `bincode` 1.x (RUSTSEC-2025-0141) — transitive via tarpc
- Coverage expansion (72.29% → 90%)
- BTSP Phase 3 (cipher negotiation + encrypted framing)
