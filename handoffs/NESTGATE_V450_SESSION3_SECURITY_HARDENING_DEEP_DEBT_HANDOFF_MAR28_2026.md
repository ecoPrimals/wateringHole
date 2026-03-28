# NESTGATE v4.5.0-dev — Session 3: Security Hardening & Deep Debt Evolution

**Date**: March 28, 2026
**From**: NestGate team
**To**: All primals (especially BearDog security, primalSpring composition)
**Supersedes**: `NESTGATE_V410_COMPREHENSIVE_AUDIT_EVOLUTION_HANDOFF_MAR27_2026.md` (additive)

---

## Quick Metrics

```
Build:              13/13 crates (0 errors, including --all-features)
Musl static:        WORKING (4.7MB, x86_64-unknown-linux-musl)
Clippy:             ZERO production warnings (pedantic+nursery)
Format:             CLEAN
Docs:               CLEAN (0 warnings)
Tests:              12,383 passing, 0 failures (469 ignored)
Coverage:           ~72% line (target: 90%)
Files > 1000 lines: 0 (largest: 927)
#[allow] crate:     26 in nestgate-api (was 30), 1 in nestgate-core
Unsafe blocks:      1 production (AVX2 SIMD, feature-gated)
```

---

## What Changed (Session 3)

### 1. Security Hardening — admin/admin eliminated

**Impact**: BearDog, primalSpring, any caller using local auth

- Hardcoded `admin/admin` credentials **removed** from `HybridAuthenticationManager`
- Local password auth now requires `NESTGATE_LOCAL_AUTH_HASH` env var (argon2 hash)
- Without the env var, password auth returns a clear error directing to security primal
- `call_security_primal()`: evolved from 50ms sleep stub to **real Unix socket IPC**
  - Sends JSON-RPC `auth.authenticate` to security primal endpoint
  - Proper error handling for unreachable/rejected
- `validate_token_signature()`: evolved from `return true` to **HMAC-SHA256 verification**
  - Tokens are now `payload.hex-signature` format
- `create_workspace_secret()`: evolved from `secret_{id}_{uuid}` to HMAC-SHA256 key derivation with OS entropy
- `create_token()`: now produces cryptographically signed HMAC tokens

**Action for BearDog**: If callers were relying on admin/admin for testing, they need to either:
1. Set `NESTGATE_LOCAL_AUTH_HASH` with an argon2 hash, or
2. Use the security primal's `auth.authenticate` endpoint

### 2. Monitoring Metrics — Real System Data

- `get_metrics()`: all placeholder values replaced with real `linux_proc`:
  - CPU from `/proc/stat`, memory from `/proc/meminfo`
  - Network bytes from `/proc/net/dev`
  - Uptime from `/proc/uptime`, load average from `/proc/loadavg`
- Non-Linux: falls back to zero (not fake data)
- MCP `ProtocolHandler`: health returns real uptime (was `Duration::from_secs(0)`)

### 3. Clippy #[allow] Reduction (30→26)

Removed 4 crate-level suppressions by fixing underlying code:
- `significant_drop_in_scrutinee`: fixed RwLock guard lifetime in circuit breaker
- `manual_strip`: fixed 2 instances in bandwidth parser → `strip_suffix()`
- `or_fun_call`: no instances remained
- `branches_sharing_code`: fixed 3 instances (workspace crud, metrics collector)

### 4. Storage Handler Tests (+13 tests)

`storage_handlers.rs` (432 lines, previously 0 tests) now has 13 tests covering:
- `resolve_family_id`: param override, state fallback, missing error, priority
- Handler validation: store/retrieve/exists/delete/list require params
- Integration: round-trip store+retrieve, list after store, nested key paths

### 5. Debris Cleanup

- Removed empty `relative/` directory
- Removed empty `nestgate.lcov` (0 bytes)
- Deleted `clustering_summary.txt` (stale refactoring note)
- Deleted `basic_tests_append.txt` (orphaned test draft)
- Fixed misplaced `#[deprecated]` inside `Debug::fmt` (syntactically invalid)
- Fixed ZFS dev stub tests expecting hardcoded pool names
- Cleaned stale "placeholder" / "in a real implementation" comments in evolved code

---

## Remaining Known Debt

### Coverage Gap (~72% → 90% target)
Top untested files by ROI:
1. `sse.rs` (648 lines, 0 tests)
2. `event_coordination.rs` (557 lines, 0 tests)
3. `unified_api_config/handlers.rs` (921 lines, 0 tests)
4. `unified_api_config/handler_types.rs` (672 lines, 0 tests)
5. `rest/rpc/manager.rs` (582 lines, 0 tests)

### Stubs Still Present
- `monitoring.rs`: ZFS metrics history and alerts still partially synthetic
- `connection_pool/factory.rs`: `create_database_pool` returns "not implemented"
- MCP `handler.rs`: orchestrator routing returns empty success
- MCP `handler.rs`: federation join / service registration not implemented standalone

### #[allow] Suppressions (26 remaining)
All 26 are still needed — mostly pedantic doc/style lints (`missing_errors_doc`,
`doc_markdown`, `cast_precision_loss`, etc.) that require extensive doc work to resolve.

### Scripts/Tools (archive candidates)
- `tools/auto_document_*.py` (4 files) — one-off doc generation
- `tools/analyze_sleep_usage.py` — one-off analysis
- `tools/unwrap_audit*.sh` (2 files) — superseded by workspace lint `unwrap_used = "warn"`

---

## Cross-Primal Notes

### For BearDog
- NestGate's `call_security_primal()` now sends real JSON-RPC `auth.authenticate`
  over Unix socket. BearDog should ensure its socket endpoint handles this method.
- Expected request: `{"jsonrpc":"2.0","id":1,"method":"auth.authenticate","params":{"username":"...","auth_method":"..."}}`
- Expected response: `{"result":{"token":"...","roles":["..."]}}`

### For primalSpring
- All 4 composition issues from exp066/068 remain resolved
- `family_id` defaults from socket name (no regression)
- Nested key paths work, list/store paths aligned
- Musl static build still working (4.7MB)

### For Songbird
- NestGate's security socket discovery follows XDG standard
  (`XDG_RUNTIME_DIR` → `/run/user/{uid}` → `/tmp`)
- `NESTGATE_SECURITY_SLUG` env var available for non-beardog security providers
