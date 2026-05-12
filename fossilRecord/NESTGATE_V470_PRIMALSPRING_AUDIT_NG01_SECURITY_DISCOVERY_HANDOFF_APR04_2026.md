# NestGate v4.7.0 — primalSpring Audit Resolution: NG-01, Security, Discovery

**Date**: April 4, 2026
**Scope**: Resolve NG-01 metadata backend wiring, advance security delegation, complete discovery compliance
**Verification**: Clippy CLEAN, fmt PASS, 12,088 tests (0 failures, ~468 ignored)

---

## primalSpring Audit Response

### NG-01: Metadata Backend Wiring — RESOLVED

**Problem**: `FileMetadataBackend` and `MetadataBackend` trait existed and were used by `SemanticRouter`, but the production Unix IPC handler (`legacy_ecosystem_rpc_handler`) did not expose `metadata.*` routes.

**Fix**:
- Created `metadata_handlers.rs` in `unix_socket_server/` with `metadata.store`, `metadata.retrieve`, `metadata.search` handlers
- Added `Arc<dyn MetadataBackend>` to `StorageState` — `FileMetadataBackend` with `InMemoryMetadataBackend` fallback
- Wired routes into `handle_request` dispatch table
- 3 new tests covering store/retrieve, search by capability, and missing-name validation

`metadata.*` is now available on both the SemanticRouter path AND the legacy Unix IPC path.

### NG-03: data.* Stubs — CONFIRMED RESOLVED (no action)

Already honest delegation stubs with discovery guidance in both routers. Tests verify `NotImplemented` with `discovery.query` + `NESTGATE_CAPABILITY_DATA` hints.

### nestgate-mcp — CONFIRMED SHED (no action)

No directory on disk, not in workspace members, no imports. Only historical references in CHANGELOG.

### nestgate-security Crypto Delegation — ADVANCED

**What was done**:
- Added `CertUtils::calculate_fingerprint_delegated()` — async method routing SHA-256 through `CryptoDelegate::hash()` (`crypto.hash` IPC to BearDog)
- Local `calculate_fingerprint()` retained for backward compat with docs pointing to delegated path

**Current delegation coverage**:
| Operation | Delegated? |
|-----------|-----------|
| encrypt/decrypt | Yes (CryptoDelegate) |
| sign/verify | Yes |
| hash | Yes (+ fingerprint_delegated) |
| JWT sign/verify | Yes |
| HMAC sign/verify | Yes |
| password verify | Yes |
| random bytes | Yes |
| cert fingerprint | Yes (async delegated path) |
| cert parse/validity | Local (x509-parser — parse only, no crypto verification) |
| token creation | Local UUID (no crypto) |

**Remaining**: `sha2` dep stays for sync fallback path; `x509-parser` for cert parsing (non-crypto); AuthTokenManager UUID tokens.

### Discovery Compliance — COMPLETE

All primal-named methods in `ServicesConfig` now carry consistent `#[deprecated(since = "0.12.0")]`:
- Getters: `get_songbird_url`, `get_toadstool_url`, `get_beardog_url`, `get_squirrel_url`, `get_biomeos_url`
- Builders: `with_songbird_url`, `with_toadstool_url`, `with_beardog_url`, `with_squirrel_url`, `with_biomeos_url`
- All point to `get_capability_url()` / `with_capability()` alternatives
- `with_biomeos_url` was missing `#[deprecated]` — fixed

**Ref counts**: 130 production-path refs in 24 files; dominated by `BIOMEOS_SOCKET_DIR` (protocol-level), deprecated getters, and docs. Zero primal-specific env vars. No hardcoded routing logic.

## Files Changed

### Created
- `nestgate-rpc/src/rpc/unix_socket_server/metadata_handlers.rs`

### Modified
- `nestgate-rpc/src/rpc/unix_socket_server/mod.rs` — MetadataBackend in StorageState, metadata.* routes
- `nestgate-rpc/src/rpc/unix_socket_server/storage_handlers.rs` — test state init
- `nestgate-rpc/src/rpc/unix_socket_server/session_handlers.rs` — test state init
- `nestgate-rpc/src/rpc/unix_socket_server/template_handlers.rs` — test state init
- `nestgate-security/src/cert/utils.rs` — calculate_fingerprint_delegated
- `nestgate-config/src/config/external/services_config.rs` — consistent #[deprecated]

---

*Last Updated: April 4, 2026*
