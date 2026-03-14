<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — 90% Coverage, Platform-Agnostic Transport, Doctor Subcommand

**Date**: March 14, 2026 (session 3)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Coverage target achieved + platform-agnostic evolution + UniBin compliance

---

## Summary

Full execution pass on all audit findings from session 2. Every item from the
prioritized action list has been addressed. The codebase has evolved to modern
idiomatic Rust with deep debt solutions, platform-agnostic transport, and
comprehensive test infrastructure.

1. **1022 tests passing** (was 862) — +160 new tests, including wiremock-based
   HTTP client tests and mock adapter capability tests.

2. **90.12% line coverage** (llvm-cov) — crossed the 90% target (was 87.78%).
   Region coverage at 91.84%.

3. **Platform-agnostic transport** — `TransportHint` enum with runtime OS
   detection: Unix socket (Linux/macOS), abstract socket (Android), TCP
   (Windows/fallback). XDG_RUNTIME_DIR respected.

4. **Doctor subcommand** — `rhizocrypt doctor [--comprehensive]` checks DAG
   engine, storage backend, configuration, discovery, and environment.

5. **Zero-copy JSON-RPC handler** — `get_str()`/`get_opt_str()` return `&str`
   instead of `String`, eliminating heap allocations in the hot path.

6. **STORAGE_BACKENDS.md aligned** — spec updated from RocksDB/LMDB (never
   implemented, C deps) to redb/sled (Pure Rust, ecoBin compliant).

7. **Binary integration tests fixed** — `env!("CARGO_BIN_EXE_rhizocrypt")`
   replaces fragile target-dir path construction. All 16 tests pass.

8. **Zero stale TODOs** — grep for TODO/FIXME/HACK/XXX returns zero results
   in production code.

---

## Changes

### Coverage Push (862 → 1022 tests)

| Module | New Tests | Infrastructure |
|--------|-----------|---------------|
| `loamspine_http.rs` | +16 | wiremock mock server |
| `toadstool_http.rs` | +15 | wiremock mock server |
| `nestgate_http.rs` | +12 | wiremock mock server |
| `beardog_http.rs` | +8 | wiremock mock server |
| `handler.rs` | +20 | batch, slice, dehydrate, error paths |
| `store_redb.rs` | +22 | error, edge case, lifecycle, metrics |
| `songbird/tests.rs` | +4 | tarpc mock server |
| `rhizocrypt-service/lib.rs` | +20 | doctor, config, discovery, errors |
| `capabilities/provenance.rs` | +6 | MockProtocolAdapter |
| `constants.rs` | +10 | platform, transport, socket |
| `binary_integration.rs` | +2 | doctor subcommand |

### Platform-Agnostic Transport

- `TransportHint` enum: `UnixSocket(PathBuf)`, `Tcp { host, port }`, `AbstractSocket(String)`
- `socket_dir()`: Linux → XDG_RUNTIME_DIR or /run/ecoPrimals; macOS → /tmp/ecoPrimals; Android/Windows → None
- `socket_path_for_primal(name)`: `{socket_dir}/{name}.sock`
- `preferred_transport(name, port)`: picks best transport for current platform
- All constants backward-compatible; new functions are additive

### Doctor Subcommand

```
rhizoCrypt Doctor v0.13.0-dev
==============================
[✓] DAG engine initialization
[✓] Storage backend (redb)
[✓] Configuration valid (port=0, host=0.0.0.0, env=development)
[!] Discovery service (not configured (standalone mode))
[✓] Environment (development)

Overall: Healthy (standalone mode)
```

### Zero-Copy Handler

Before: `get_str()` → `Result<String>` (heap allocation per field)
After:  `get_str()` → `Result<&str>` (borrow from serde_json::Value)
Impact: Zero allocation in JSON-RPC parameter parsing hot path

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-targets --all-features -- -D warnings` | Clean |
| `cargo doc --no-deps` | Clean (0 warnings) |
| `cargo test --all --all-features` | 1022 pass, 0 fail |
| `cargo llvm-cov --all-features` | 90.12% lines, 91.84% regions |
| `#![forbid(unsafe_code)]` | All 4 crate roots |
| SPDX headers | All `.rs` files |
| Production TODOs | 0 |
| Production unwrap/expect | 0 (all in #[cfg(test)]) |
| Max file size | All under 1000 lines |

---

## Remaining Work

1. **Coverage headroom** — 90.12% achieved; remaining gaps are in:
   - `store_redb.rs` (67%) — DB corruption error paths
   - `toadstool_http.rs` (67%) — some BYOB endpoints untested
   - `songbird/client.rs` (75%) — tarpc transport layer

2. **Spec updates needed** — `INTEGRATION_SPECIFICATION.md` v1 is legacy;
   marked as archived in specs index. V2 is current.

3. **Showcase 06-complete-workflow/** — README references scripts that don't
   exist. Either populate or remove the directory.

4. **llvm-cov in CI** — currently installed locally; CI workflow should
   install `cargo-llvm-cov` and enforce the 90% gate.

---

## Dependencies Added

- `wiremock = "0.6"` (dev-dependency in rhizo-crypt-core) — pure Rust HTTP mock server for testing
- `tempfile = "3.24"` (dev-dependency in rhizocrypt-service) — temporary directories for doctor storage check

---

## Handoff Context

Previous sessions:
- Session 1 (Mar 12): wateringHole standards, UniBin, capability discovery
- Session 2 (Mar 13): Deep debt, 862 tests, cargo-deny, service lib extraction
- Session 3 (Mar 14): This session — 90% coverage, platform-agnostic, doctor

The codebase is in a strong position. All quality gates pass. The next
evolution targets are: CI coverage gate, showcase cleanup, and pushing
toward 95% coverage by testing DB corruption paths with fault injection.
