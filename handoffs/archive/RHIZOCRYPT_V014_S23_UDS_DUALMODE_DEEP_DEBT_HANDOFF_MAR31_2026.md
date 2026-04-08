# rhizoCrypt v0.14.0-dev — Session 23 Handoff

**Date**: March 31, 2026
**Session**: 23
**Focus**: RC-01 fix (UDS + dual-mode TCP), deep debt evolution, `biomeos` path migration

---

## What Changed

### 1. UDS Transport (RC-01 — CRITICAL, now RESOLVED)

- **`--unix [PATH]` CLI flag** added to `rhizocrypt server`
  - Default: `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`
  - Custom: `--unix /custom/path.sock`
- **`UdsJsonRpcServer`** in `jsonrpc/uds.rs`:
  - Stale socket cleanup on startup
  - Parent directory creation
  - Graceful shutdown via `watch::Receiver<bool>`
  - Gated by `#[cfg(unix)]`
- **Newline-delimited JSON-RPC 2.0** wire format (same as socat, biomeOS pipeline)

### 2. Dual-Mode TCP Auto-Detection

- Single TCP JSON-RPC port now accepts **both** raw newline and HTTP POST clients
- Per-connection first-byte peek: `{`/`[` → newline handler, otherwise → Axum router
- Uses `hyper-util` + `tower::Service` for direct Axum integration
- Generic `handle_newline_connection<S>` over `AsyncRead + AsyncWrite`

### 3. `ecoPrimals` → `biomeos` Path Migration

- `safe_env::get_socket_path()` XDG fallback: `ecoPrimals` → `biomeos`
- `discovery::manifest::manifest_dir()`: `ecoPrimals` → `biomeos`
- All docs, test assertions, adapter examples updated
- Uses `constants::BIOMEOS_SOCKET_SUBDIR` (single source of truth)

### 4. Deep Debt Evolution

| Item | Before | After |
|------|--------|-------|
| `OrExit` trait | `std::process::exit(1)` | Returns `Result<T, RhizoCryptError>` |
| `handle_tcp_connection` | `Box<dyn Error>` | `std::io::Result<()>` |
| Discovery coupling | Direct `SongbirdClient` import | Function-scoped import, "discovery adapter" docs |
| Niche docs | Primal names hardcoded | Capability-agnostic |
| Session cleanup | Duplicated in `discard`/`gc_sweep` | Extracted `purge_session_artifacts()` |
| Provider traits | 200+ lines in `integration/mod.rs` | Extracted to `integration/traits.rs` |
| `deny.toml` advisories | 2 stale RUSTSEC ignores | Removed (resolved upstream) |

---

## Unblocked

- **exp094, exp096, exp098**: rhizoCrypt now reachable via UDS
- **exp095**: Needs loamSpine startup fix (LS-03)
- **Provenance trio compositions**: rhizoCrypt UDS socket available for composition graphs
- **+9 validation checks** from ludoSpring
- **IPC Compliance Matrix**: rhizoCrypt now **Conformant** across wire framing, socket path, health, standalone

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-targets --all-features -- -D warnings` | 0 warnings |
| `cargo test --workspace --all-features` | **1,402 tests**, 0 failures |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| SPDX headers | All 129 `.rs` files |
| Max file size | All under 1000 lines |
| Unsafe | Zero (`deny` workspace-wide) |
| Production unwrap/expect | Zero |

---

## New Files

| File | Purpose |
|------|---------|
| `crates/rhizo-crypt-rpc/src/jsonrpc/newline.rs` | Generic newline-delimited JSON-RPC handler |
| `crates/rhizo-crypt-rpc/src/jsonrpc/uds.rs` | Unix domain socket JSON-RPC server |
| `crates/rhizo-crypt-core/src/integration/traits.rs` | Provider traits (extracted from mod.rs) |

---

## Still Blocking

- **exp095** waits on loamSpine LS-03 (startup panic)
- plasmidBin binary submission (not yet in plasmidBin)
- `rustls-rustcrypto` migration (pending upstream stabilization)

---

## Previous Handoff

[RHIZOCRYPT_V014_S22_DEADLOCK_FIX_CONCURRENCY_AUDIT_HANDOFF_MAR24_2026.md](RHIZOCRYPT_V014_S22_DEADLOCK_FIX_CONCURRENCY_AUDIT_HANDOFF_MAR24_2026.md)
