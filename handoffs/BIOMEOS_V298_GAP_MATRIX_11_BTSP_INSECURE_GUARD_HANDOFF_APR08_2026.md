# biomeOS v2.98 — GAP-MATRIX-11: BTSP Insecure Guard + Security Posture

**Date**: April 8, 2026
**Scope**: Wire BTSP insecure guard and security posture logging into all biomeOS startup paths
**Gap**: GAP-MATRIX-11 (Medium) — Socket naming alignment implemented but not live-wired
**Tests**: 7,669 passing (0 failures), clippy PASS (0 warnings)

---

## Problem

GAP-MATRIX-11 identified that biomeOS had implemented the BTSP Secure Socket
Architecture code (`btsp_client.rs`) including:

- `validate_insecure_guard()` — refuses startup when both `FAMILY_ID` and `BIOMEOS_INSECURE=1` are set
- `log_security_posture()` — logs production/development/standalone mode
- `is_family_scoped_socket()` — detects `{primal}-{family_id}.sock` patterns
- `security_mode()` — returns `Production` or `Development` based on env

However, **none of these were wired into actual startup paths**. The guard
existed but was never called, meaning biomeOS could silently start with
conflicting security configuration.

---

## Fix

### Startup Guard Integration (4 entry points)

| Entry Point | File | Change |
|-------------|------|--------|
| `biomeos` UniBin | `crates/biomeos/src/main.rs` | Guard + posture after logging init, before dispatch |
| `neural-api-server` | `crates/biomeos-atomic-deploy/src/bin/neural-api-server.rs` | Guard before banner, posture after |
| `NeuralApiServer::serve()` | `crates/biomeos-atomic-deploy/src/neural_api_server/server_lifecycle.rs` | Guard + posture as step 0 before socket bind |
| `tower` binary | `crates/biomeos-core/src/bin/tower.rs` | Guard + posture after logging init |

### Forwarding BTSP Awareness

`crates/biomeos-atomic-deploy/src/neural_router/forwarding.rs`:
- Was: debug log "BTSP-required socket detected" (no context)
- Now: checks `security_mode()` and logs appropriately:
  - Production + BTSP available: debug authenticated
  - Production + no BTSP: warn that handshake not yet wired
  - Development: debug skip

### New Tests (5)

In `crates/biomeos-core/src/btsp_client.rs`:
- `family_scoped_domain_stem_sockets` — domain-stem naming (`security-8ff3b864.sock`)
- `extract_family_from_domain_stem_socket` — domain-stem extraction
- `edge_cases` — empty paths, no-ext, no-suffix
- `security_mode_returns_valid_variant` — smoke test
- `log_security_posture_does_not_panic` — no-panic smoke

---

## What Remains for Full Live Validation

This resolves the "NOT LIVE WIRED" aspect of GAP-MATRIX-11. Full live
validation (Run 6) requires:

1. Start biomeOS with `FAMILY_ID=<real_id>` and verify posture log shows "production"
2. Start biomeOS with `BIOMEOS_INSECURE=1` (no FAMILY_ID) and verify "development" mode
3. Set both `FAMILY_ID` and `BIOMEOS_INSECURE=1` and verify startup is **refused**
4. Verify family-scoped sockets (`primal-{fid}.sock`) trigger BTSP warnings in forwarding
5. Verify non-family sockets (`primal.sock`) do not trigger BTSP warnings

The cryptographic BTSP handshake itself is Phase 2 (depends on BearDog
`btsp.session.create`/`btsp.session.verify` JSON-RPC methods).

---

## Files Changed

- `crates/biomeos/src/main.rs` — guard + posture in `main()`
- `crates/biomeos-atomic-deploy/src/bin/neural-api-server.rs` — guard + posture in `main()`
- `crates/biomeos-atomic-deploy/src/neural_api_server/server_lifecycle.rs` — guard + posture in `serve()`
- `crates/biomeos-core/src/bin/tower.rs` — guard + posture in `main()`
- `crates/biomeos-atomic-deploy/src/neural_router/forwarding.rs` — enhanced BTSP detection
- `crates/biomeos-core/src/btsp_client.rs` — 5 new tests

---

## Verification

```
cargo check --workspace         # PASS
cargo clippy --workspace --all-targets -- -D warnings  # 0 warnings
cargo test --workspace          # 7,669 tests, 0 failures
```
