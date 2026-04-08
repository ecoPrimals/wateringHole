# NestGate v4.7.0 — primalSpring T1–T9 Audit Resolution

**Date**: April 4, 2026
**Commit**: (see nestgate main)
**Tests**: 12,095 passing, 0 failures, 468 ignored
**Clippy**: CLEAN (`-D warnings`)
**fmt**: CLEAN

---

## Audit Findings Resolved

### T1 Build (B → A)
- Fixed `migration.rs` fmt deviation (long line from `discovery_default_host()` call)
- Fixed `nestgate-api/README.md` license inconsistency (`-or-later` → `-only` per `LICENSING.md`)

### T2 UniBin (D → B)
- `server` alias for `daemon` subcommand: **already existed**
- `--port` now functional in socket-only mode: env vars `NESTGATE_API_PORT` / `NESTGATE_HTTP_PORT` / `NESTGATE_PORT` activate TCP JSON-RPC alongside Unix socket
- Added `env_port_if_set` / `env_port_if_set_source` — returns `None` when no env var set (prevents unintended TCP activation from compiled-in defaults)
- Updated `Daemon` `--port` doc to accurately reflect socket-only vs HTTP mode behavior

### T3 IPC (C → B)
- TCP JSON-RPC now activatable via env vars in socket-only mode (see T2)
- Broadened capability symlink policy: `storage.sock` symlink now created for any dedicated runtime directory, not just `biomeos/` parents
- Excluded from `/tmp` and `/var/tmp` (global namespace collision risk)
- Old `socket_parent_is_biomeos_standard_dir` deprecated, new `socket_parent_eligible_for_capability_symlink` is the entry point

### T4 Discovery (C → B+)
- Removed 12 primal-name references from docs/comments across 8 files
- **Remaining**: 48 total (47 in deprecated `services_config.rs` compat surface + 1 test denylist guard)
- `biomeos` refs are ecosystem protocol names (socket directory standard), not primal coupling
- All active production routing is capability-based

### T9 Deploy (D → C)
- aarch64-unknown-linux-musl rustup target installed
- Cross-compilation instructions added to `START_HERE.md`
- `.cargo/config.toml` already had correct linker/rustflags for musl static builds
- **Blocked**: actual binary build requires `gcc-aarch64-linux-gnu` (CI/deploy environment dependency)

---

## Code Changes

### nestgate-bin
- `commands/env.rs`: Added `env_port_if_set_source` + `env_port_if_set`
- `commands/service.rs`: Socket-only daemon branch now merges env port before `tcp_jsonrpc_listen_addr`
- `cli/mod.rs`: Re-exports `env_port_if_set`
- `cli/subcommands.rs`: Updated `--port` doc for accuracy
- `cli/tests.rs`: 4 new `env_port_if_set` tests (all concurrent via `MapEnv`)

### nestgate-rpc
- `socket_config.rs`: `socket_parent_eligible_for_capability_symlink` replaces `socket_parent_is_biomeos_standard_dir` (old deprecated)
- `socket_config_tests.rs`: 11 tests updated for broadened symlink policy

### Documentation/comments (8 files)
- Replaced specific primal names with generic capability terms in module docs and code comments

---

## Remaining Audit Debt

| Tier | Grade | Notes |
|------|-------|-------|
| T1   | A     | Clean |
| T2   | B     | Full link requires TCP integration test with actual client |
| T3   | B     | TCP+symlink wired; TCP integration test pending |
| T4   | B+    | 47 deprecated compat refs — removal is a breaking change |
| T9   | C     | Binary build needs CI with `gcc-aarch64-linux-gnu` |
