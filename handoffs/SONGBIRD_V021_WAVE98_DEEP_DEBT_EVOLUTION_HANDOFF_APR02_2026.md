# Songbird v0.2.1-wave98: Deep Debt Evolution

**Date**: 2026-04-02
**Commit**: `11744c514`
**Builds on**: Wave 97 (capability-based discovery compliance)

## Summary

Systematic deep debt resolution across 6 categories: hardcoded path portability,
large file smart refactoring, production stub evolution, test triage, and primal
name constant alignment.

## Changes

### 1. Hardcoded `/tmp` → `std::env::temp_dir()` (portability + security)

All production socket fallback paths now use `std::env::temp_dir()` instead of
literal `/tmp/`, making Songbird portable across `TMPDIR` configurations and
multi-user environments.

- `songbird-types/defaults/paths`: public constants → functions returning `PathBuf`
- Orchestrator, http-client, tls, crypto-provider, nfc, lineage-relay all migrated
- **API change**: downstream code importing `BEARDOG_SOCKET_LEGACY` etc. must switch
  to `security_socket_default_path()` and similar functions

### 2. Smart File Refactoring (4 files)

| File | Before | After | Extracted |
|------|--------|-------|-----------|
| `punch_handler.rs` | 844L | ~482L | types, port_pattern, coordinate, tests |
| `http_deploy.rs` | 838L | ~410L | types, capabilities, chunked |
| `config/constants.rs` | 816L | ~146L | 10 domain modules |
| `adapters/compute.rs` | 814L | ~460L | metrics, adapter |

### 3. Production Stub Evolution

- `security_setup.rs`: already fail-closed — removed misleading "placeholder"
- `cli/types.rs`: documented actual env-based behavior
- `app/core.rs`: Windows IPC documented as known platform limitation
- `network/binding.rs`: interface query documented as known limitation
- `sovereignty/adapter.rs`: evolved from placeholder to real discovery delegation
  with federation capabilities and network effects

### 4. Test Triage

- **22 tests un-ignored**, all pass:
  - 19 orchestrator comprehensive tests (env-driven security setup)
  - 3 TLS E2E tests (handshake flow)
- Bare `#[ignore]` annotations given explicit reason strings
- ~159 ignored tests remain (valid: live service, hardware, blocked on API)

### 5. Primal Name Alignment

- `universal-ipc` platform maps (unix, windows, android, ios) use `BIOMEOS_DIR`
  constant instead of `"biomeos"` string literals

## Metrics

- **54 files changed**, 3,079 insertions, 2,613 deletions
- **12,154 tests pass**, 0 failures, 0 clippy warnings
- **~402,500** total Rust lines across 30 crates
- Zero `unsafe` blocks (workspace `unsafe_code = "forbid"`)
- Zero production `todo!()` or `unimplemented!()`
