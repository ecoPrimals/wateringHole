# Songbird v0.2.1 Wave 157 — Deep Debt: Hardcoded Literals, Dead Deps, Doc Cleanup, Debris Removal

**Date**: April 22, 2026  
**From**: Songbird deep debt pass (comprehensive codebase audit)  
**Waves**: 156–157  
**Status**: 7,387 lib tests passed, 0 failures, 22 ignored; Clippy pedantic clean; fmt clean

---

## Wave 156 — BTSP Crypto Discovery + Startup Resilience

- Stage 7 connectivity verification no longer crashes when no crypto provider available (graceful cleartext fallback)
- NDJSON handshake reads have 15s timeout (prevents indefinite blocking)
- Neural API per-chunk read timeout raised 100ms → 5s (BearDog BTSP crypto latency)
- Fixed 2 pre-existing birdsong beacon test failures (7,385 → 7,387 tests, 0 failures)

## Wave 157 — Deep Debt: Hardcoded Literals, Dead Deps, Example Hygiene

### Hardcoded literals → constants (12 files, 10 crates)
- Added `is_loopback_host()`, `LOCALHOST_IPV6`, `DEFAULT_RELAY_PORT`, `HTTPS_STANDARD_PORT`, `DYNAMIC_PORT_RANGE_*`
- Evolved compute adapter, util.rs, NetworkSecurityConfig, discovery, relay, onion, canonical network, iOS, HTTPS to use central constants
- Removed inline `8080`, `3479`, `3478`, `443`, `60000`, `1024`, `8001`–`8005` bare port literals

### Dead workspace deps
- Removed `urlencoding` and `if-addrs` (zero consumers)

### Example hygiene (6 files)
- `Box<dyn Error>` → `anyhow::Result`
- `/tmp/beardog-*.sock` → XDG-based `family_scoped_crypto_socket_path()`

### Doc cleanup
- Fixed stale metrics: file count 1,587 → 1,609, sub-enum count 16 → 33, line count ~430k → ~421k
- Fixed `-sys` claim to "zero first-party -sys crates"
- Fixed REMAINING_WORK structure: moved resolved items (SB-03, BTSP Phase 2 narrative) out of "Active Blockers"
- Fixed CONTRIBUTING lint guidance: `#[expect]` or `#[allow]` with reason
- Reconciled test count across all docs

### Debris removal
- Deleted uncompiled `tests/e2e/`, `tests/chaos/`, `tests/fault/`, `tests/integration/`, `tests/common/`, `tests/helpers/` (~12,400 lines of dead code referencing removed `reqwest` dep)
- Deleted unreferenced root `config/` directory (5 files, superseded by `examples/config/`)
- Fixed broken `SCENARIO_TEMPLATES.md` reference in `local_infrastructure_ci.rs`
- Fixed genesis `--features testing` → `test-mocks` comment

---

## Comprehensive Audit Results (Wave 157)

| Category | Status |
|----------|--------|
| Files >800L | 0 |
| Unsafe code | 0 (`forbid(unsafe_code)` on all 30 crates) |
| `todo!/unimplemented!` | 0 in production |
| Production `panic!` | 0 |
| Production mocks | 0 (all properly gated) |
| `async-trait` | 0 first-party usage |
| `Box<dyn Error>` in production | 0 |
| Legacy patterns (`extern crate`, `try!`) | 0 |
| Hardcoded IPs/ports in production | 0 (all via constants or env) |
| Unused workspace deps | 0 |

### Remaining architectural items (documented, intentional)
- `dyn Stream` — async watch pattern across discovery backends
- `Box<dyn SerialPort>` — external `serialport` crate API
- `Arc<dyn Fn>` — test injection for concurrent env readers
- `unreachable!()` — 2 provably unreachable QUIC VarInt arms (RFC 9000)
