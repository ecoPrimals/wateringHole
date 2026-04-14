# Songbird v0.2.1 — Wave 130: Wire Standard L3, BTSP Handshake, Self-Knowledge Evolution, Deep Debt

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 130  
**Status**: Complete  
**Previous**: Wave 129b (doc accuracy/debris cleanup)

---

## Summary

Comprehensive deep debt evolution closing all primalSpring audit gaps (Wire Standard L3, BTSP Phase 1, socket naming, INSECURE guard, health.liveness) and executing broad self-knowledge cleanup across the codebase: capability-first env var evolution in all 4 universal adapters, production stub evolution (delegation, DB storage, DNS-SD), and port constant consolidation.

## Changes

### Wire Standard L3 (was L2)

| Item | Before | After |
|------|--------|-------|
| `capabilities.list` | `{primal, version, methods}` | `{primal, version, methods, provided_capabilities, consumed_capabilities, protocol, transport}` |
| `health.liveness` | `{"status":"healthy"}` | `{"status":"alive"}` (per CAPABILITY_WIRE_STANDARD.md) |
| Compliance | L2 | L3 |

**Files**: `songbird-universal-ipc/src/introspection/capability_tokens.rs`, `health_payloads.rs`

### BTSP Phase 1 — Handshake Client

| Item | Detail |
|------|--------|
| `BtspClient::handshake()` | Full `ClientHello → ServerHello → ChallengeResponse → HandshakeComplete` via security provider JSON-RPC |
| JSON-RPC methods called | `btsp.session.create`, `btsp.session.verify`, `btsp.negotiate` |
| `BtspSession` struct | `session_id`, `cipher`, `target_socket`, `client_ephemeral_pub`, `server_ephemeral_pub` |
| Reference | BTSP_PROTOCOL_STANDARD.md Phase 27 |

**File**: `songbird-orchestrator/src/btsp_client.rs`

### BIOMEOS_INSECURE Guard

Songbird refuses startup when both `FAMILY_ID` (non-default) and `BIOMEOS_INSECURE=1` are set. Guard fires at the top of `start()` in startup_orchestration.rs. Per PRIMAL_SELF_KNOWLEDGE_STANDARD.md.

**Files**: `songbird-orchestrator/src/env_config.rs`, `startup_orchestration.rs`

### Domain-Based Socket Naming (PRIMAL_SELF_KNOWLEDGE_STANDARD v1.1)

| Item | Before | After |
|------|--------|-------|
| Primary socket | `songbird.sock` | `network.sock` |
| Family-scoped | `songbird-{fid}.sock` | `network-{fid}.sock` |
| Backward compat | — | `create_legacy_socket_symlink()`: `songbird.sock` → `network.sock` |
| CLI `status` | `std::env::temp_dir().join("songbird.sock")` | `BIOMEOS_SOCKET_DIR` / XDG / fallback resolution → `network.sock` |

**Files**: `songbird-orchestrator/src/env_config.rs`, `songbird-cli/src/cli/commands/status.rs`, + 8 test files updated

### Self-Knowledge Evolution — Capability-First Env Vars

All 4 universal adapters now have capability-first env ordering with deprecated primal-name fallbacks:

| Adapter | Priority Order | Deprecated (with `warn!`) |
|---------|---------------|--------------------------|
| Security | `SECURITY_ENDPOINT` > `SECURITY_PROVIDER_ENDPOINT` > `SONGBIRD_SECURITY_ENDPOINT` | `BEARDOG_ENDPOINT` (`#[deprecated]` + runtime warn) |
| Storage | `STORAGE_ENDPOINT` > `STORAGE_PROVIDER_ENDPOINT` > `SONGBIRD_STORAGE_ENDPOINT` | `NESTGATE_ENDPOINT` |
| AI | `AI_ENDPOINT` > `AI_PROVIDER_ENDPOINT` | `SQUIRREL_ENDPOINT` |
| Compute | Already correct | `TOADSTOOL_ENDPOINT` |

### Production Stubs Evolved

| Stub | Evolution |
|------|-----------|
| Delegation (6 methods) | "not yet implemented" → capability-routing guidance errors (consistent with first 3 methods) |
| Registry DB backend | Hardcoded `./data/registry_db_fallback` → URI-derived filesystem delegation (`file:`, `sqlite:` scheme parsing) |
| DNS-SD discovery | Empty `Vec` → biomeos socket directory scanner with TCP sidecar discovery |

### Port Constant Consolidation

- 4 duplicate constants in `songbird-types::constants` deprecated → `defaults::ports`
- 5 downstream files migrated: `songbird-config`, `songbird-discovery`, `songbird-network-federation`, `songbird-remote-deploy`, `songbird-execution-agent`

## Audit Results — Pre-existing Clean

| Category | Status |
|----------|--------|
| Files >800L | 0 (largest 797L `primal_discovery.rs`) |
| Unsafe code | 0 |
| TODO/FIXME/HACK | 0 in production |
| External C deps | Clean on default features |
| Archive/debris | None |

## Validation

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy` (9 modified crates, `-D warnings`) | Clean |
| `cargo check --workspace` | Zero warnings, zero errors |
| `cargo test --workspace` | **13,009 passed, 0 failed** |

## Cross-Cutting Notes

- **primalSpring audit gaps**: All 5 items from the Wave 128-129 downstream audit are resolved (L3, BTSP client, socket naming, INSECURE guard, health.liveness)
- **Self-knowledge violations**: 304+ refs to other primal names remain in production as deprecated env var fallbacks with `tracing::warn!` — these are operational migration shims, not routing violations. Deeper files (primal_discovery, agnostic_config, TLS/crypto socket discovery) already had correct capability-first ordering.
- **BTSP handshake server**: Not in scope — Songbird is a client, not a security provider. Server-side BTSP is BearDog's domain.
- **Port constant deprecation**: Downstream crates that import deprecated `constants::DEFAULT_HTTP_PORT` etc. will see compile-time deprecation warnings guiding to `defaults::ports`.

## Remaining Debt (Songbird)

- Coverage: 72.29% → 90% target (pure-logic module expansion)
- Tor/TLS crypto: blocked on live security provider
- Platform backends: NFC, iOS, WASM
- `ring` elimination: remains via optional `k8s` feature only
