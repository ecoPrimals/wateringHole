# biomeOS v3.42 — Coordinator Transport + Graph Schema + Final Env Var Sweep

**Date**: May 4, 2026
**Version**: 3.42
**From**: biomeOS
**Status**: PRODUCTION READY — 7,866 tests (0 failures), clippy PASS, fmt PASS

---

## Changes

### 1. Coordinator Transport Migration (primalSpring Phase 58 — HIGH priority)

5 coordinator call sites migrated from `AtomicClient::call()` (plaintext) to
`AtomicClient::call_btsp()` (BTSP Phase 3 capable):

- `discovery_init.rs` — `derive_coordination_key` crypto operations
- `capability_handlers/health.rs` — `call_primal_health` probes
- `health_check.rs` — `rpc_ping` lifecycle health pings
- `neural_router/discovery_primal.rs` — `quick_health_check` and `check_endpoint_health`

All security-critical and health-related outbound calls now attempt encrypted
framing on Unix socket endpoints.

### 2. Graph Schema Alignment PG-39 (primalSpring Phase 58 — LOW priority)

- **`neural_to_deployment` fix**: The `capability` field was being set to
  `"capability_call"` (the operation name) instead of the actual capability
  string. Fixed to extract the real capability from `operation.params["capability"]`.
- **`security_model` passthrough**: `convert_deployment_node` now reads and
  passes through the `security_model` field from primalSpring graph definitions
  into the node's config map.

### 3. Final BEARDOG_NODE_ID Elimination

Eliminated all 15 remaining `BEARDOG_NODE_ID` references across the codebase:

**Production code:**
- `tower_orchestration.rs` — removed 2 `BEARDOG_NODE_ID` fallbacks; `NODE_ID` is sole env var
- `nucleus.rs` — removed redundant `.env("BEARDOG_NODE_ID", ...)` from spawner
- `verification.rs` — node-id extraction reads `NODE_ID` instead of `BEARDOG_NODE_ID`
- `lib.rs` — comment "NestGate-integrated" → "storage-provider integrated"

**Test data (7 files):**
- `tower_config.rs`, `spore_tests.rs`, `nucleus_tests2.rs`, `engine_tests.rs`,
  `e2e_verify_refresh.rs`, `unit_verification_simple.rs`, `unit_refresh_tests.rs`

### 4. Dependency Analysis

52 unique external dependencies — all pure Rust ecosystem standard:
- **Crypto**: RustCrypto (chacha20poly1305, hkdf, sha2, ed25519-dalek) — zero openssl/ring
- **System**: rustix (safe syscalls) — no direct libc usage
- **Async**: tokio ecosystem
- **Web**: axum + tower stack
- **No C-wrapper crates** to evolve

---

## Codebase Health

| Metric | Value |
|--------|-------|
| Tests | 7,866 (0 failures, fully concurrent) |
| Files >800 LOC | 0 (largest: 798) |
| Unsafe | 0 |
| TODO/FIXME | 0 |
| Production mocks | 0 |
| Hardcoded primal names/env vars | 0 |
| External C deps | 0 |
| Clippy | PASS (pedantic+nursery, -D warnings) |
| Format | PASS |

---

## primalSpring Phase 58 Audit — Fully Resolved

Both audit items are now addressed:
1. **Phase 3 transport encryption (HIGH)** — coordinator calls migrated to `call_btsp`
2. **Graph schema alignment PG-39 (LOW)** — capability extraction fixed, `security_model` supported
