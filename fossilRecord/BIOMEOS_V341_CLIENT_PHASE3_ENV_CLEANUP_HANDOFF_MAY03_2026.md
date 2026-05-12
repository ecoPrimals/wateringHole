# biomeOS v3.41 — Client-Side Phase 3 + Hardcoded Env Var Elimination

**Date**: May 3, 2026
**From**: biomeOS team
**To**: All downstream consumers (primalSpring, springs, deployment tooling)

---

## Summary

Two major evolutions:

1. **Client-side BTSP Phase 3** — biomeOS now negotiates encrypted channels as a
   *client* when calling primals outbound. Previously, only server-side Phase 3 was
   wired (v3.40). Now both directions support ChaCha20-Poly1305 encrypted framing
   with graceful plaintext fallback.

2. **Hardcoded primal-name env vars eliminated** — All environment variable names
   that embedded specific primal identities (`BEARDOG_*`, `SONGBIRD_*`) have been
   replaced with capability-based names (`FAMILY_ID`, `SECURITY_ENDPOINT`,
   `DISCOVERY_ENDPOINT`, etc.).

---

## Client-Side Phase 3 Details

### New modules

| Module | Crate | Purpose |
|--------|-------|---------|
| `btsp_crypto.rs` | `biomeos-core` | Shared crypto primitives (previously duplicated in `btsp_negotiate.rs`) |
| `btsp_client_phase3.rs` | `biomeos-core` | Client-side Phase 3 negotiation: `perform_client_handshake_phase3()` |

### Flow

```
jsonrpc_unix_btsp / call_primal_rpc
  → perform_client_handshake_phase3()
    → Phase 2 handshake (existing)
    → send ChallengeResponse with preferred_cipher: "chacha20-poly1305"
    → retain shared_secret as handshake_key
    → send btsp.negotiate RPC
    → derive SessionKeys via HKDF-SHA256
    → return ClientPhase3Outcome::Encrypted { keys, stream }
      OR ClientPhase3Outcome::Plaintext { stream }
  → send_encrypted_jsonrpc() or send_jsonrpc_line() accordingly
```

### Affected paths

- `atomic_transport.rs` — `jsonrpc_unix_btsp` now Phase 3 aware
- `node_handlers.rs` — `call_primal_rpc` uses Phase 3 with fallback
- `capability_translation/mod.rs` — implicitly via `AtomicClient::call_btsp()`
- `neural_router/forwarding.rs` — implicitly via `AtomicClient::call_btsp()`

### Backward compatibility

Fully backward compatible. If a primal does not support `btsp.negotiate` or returns
`cipher: "null"`, biomeOS falls back to plaintext JSON-RPC over the authenticated
Phase 2 channel. No breakage for primals without Phase 3.

---

## Environment Variable Migration

### Breaking changes (deployment config)

| Old | New | Used by |
|-----|-----|---------|
| `BEARDOG_FAMILY_ID` | `FAMILY_ID` | Tower/spore config |
| `BEARDOG_FAMILY_SEED` | `FAMILY_SEED` | Family credentials |
| `BEARDOG_FAMILY_SEED_FILE` | `FAMILY_SEED_FILE` | Spore tower.toml |
| `BEARDOG_NODE_ID` | `NODE_ID` | Tower/spore config |
| `BEARDOG_ENDPOINT` | `SECURITY_ENDPOINT` | Observability, metrics |
| `SONGBIRD_ENDPOINT` | `DISCOVERY_ENDPOINT` | Discovery bootstrap, metrics |
| `BEARDOG_PORT` | `SECURITY_PORT` | Port resolution |
| `SONGBIRD_PORT` | `DISCOVERY_PORT` | Port resolution |

### Action required

If your deployment scripts or environment files reference any of the "Old" env var
names above, update them to the "New" names. biomeOS no longer reads the old names.

The `DISCOVERY_ENDPOINT` env var is now the sole mechanism for explicit discovery
provider endpoint configuration.

---

## Test Results

- **7,866 tests** (0 failures, fully concurrent)
- `cargo check` clean
- `cargo clippy --workspace -- -D warnings` zero warnings
- `cargo fmt --check` clean
- All production files < 800 LOC

---

## Files Changed

### New files
- `crates/biomeos-core/src/btsp_crypto.rs` (229 LOC)
- `crates/biomeos-core/src/btsp_client_phase3.rs` (222 LOC)

### Modified files (13)
- `crates/biomeos-core/src/lib.rs`
- `crates/biomeos-core/src/btsp_client.rs`
- `crates/biomeos-core/src/atomic_client/atomic_transport.rs`
- `crates/biomeos-core/src/family_credentials.rs`
- `crates/biomeos-core/src/discovery_bootstrap.rs`
- `crates/biomeos-core/src/observability/mod.rs`
- `crates/biomeos-core/src/tower_config.rs`
- `crates/biomeos-types/src/constants/env_vars.rs`
- `crates/biomeos-types/src/constants/network.rs`
- `crates/biomeos-types/src/constants/mod.rs`
- `crates/biomeos-atomic-deploy/src/deployment_graph.rs`
- `crates/biomeos-atomic-deploy/src/neural_api_server/btsp_negotiate.rs`
- `crates/biomeos-atomic-deploy/src/executor/node_handlers.rs`
- `crates/biomeos-spore/src/spore/config.rs`
- `crates/biomeos-spore/src/verify.rs`
- `crates/biomeos-spore/src/seed.rs`
