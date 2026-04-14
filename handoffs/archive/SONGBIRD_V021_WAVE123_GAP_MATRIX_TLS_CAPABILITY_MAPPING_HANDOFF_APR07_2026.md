# Songbird v0.2.1 — Wave 123: GAP-MATRIX-03 TLS Compat + Capability Method Mapping

**Date**: April 7, 2026
**Primal**: songBird
**Previous**: Wave 122 (archived)
**Upstream**: primalSpring v0.9.3 Live Validation GAP-MATRIX

---

## Summary

Resolves two primalSpring audit items from the live validation matrix:
- **GAP-MATRIX-03** (Low): TLS 1.3 handshake failures against CDN-fronted hosts
- **Capability method gap** (Low): Capability tokens returning "unknown method" when called

## GAP-MATRIX-03: TLS 1.3 Compatibility

### Root Cause

The ClientHello already advertised all three TLS 1.3 cipher suites (0x1301, 0x1302, 0x1303). The failure against httpbin.org (Cloudflare) was caused by:

1. **Empty legacy session ID** — `msg.push(0)` sent zero-length session ID. RFC 8446 Appendix D.4 requires 32 random bytes for middlebox compatibility. Some CDN/WAF stacks reject empty session IDs.

2. **Incomplete signature algorithms** — Missing RSA-PSS variants (`rsa_pss_rsae_sha384`, `rsa_pss_rsae_sha512`, `rsa_pss_pss_*`) required by Cloudflare cert chain validation.

### Fix

**All 4 extension strategies** (Minimal, Standard, Modern, MaxCompatibility) updated:

- **Session ID**: 32-byte legacy session ID now included in ClientHello (both `handshake_refactored` and `handshake_v2` code paths)
- **Minimal sig algs**: 3 → 6 algorithms (added `rsa_pss_rsae_sha384`, `rsa_pss_rsae_sha512`, `rsa_pkcs1_sha384`)
- **Standard sig algs**: 9 → 14 algorithms (added all 6 RSA-PSS variants: `rsa_pss_rsae_sha384`, `rsa_pss_rsae_sha512`, `rsa_pss_pss_sha256`, `rsa_pss_pss_sha384`, `rsa_pss_pss_sha512`, moved PKCS1 to end per preference order)
- **MaxCompatibility cert sig algs**: 5 → 8 algorithms (full PSS family in `signature_algorithms_cert` extension)

### Files Changed

- `crates/songbird-http-client/src/tls/handshake_refactored/handshake_flow.rs` — 32-byte session ID + test update
- `crates/songbird-http-client/src/tls/handshake_refactored/extensions.rs` — expanded sig algs across Minimal/Standard/MaxCompat
- `crates/songbird-http-client/src/tls/handshake_v2/client_hello.rs` — 32-byte session ID

## Capability Method Gap

### Root Cause

`capabilities.list` returns 14 NEST capability tokens (e.g., `network.discovery`, `ipc.jsonrpc`). These tokens were advertisement-only — not registered in `JsonRpcMethod::from_wire_str`. Calling them as method names returned "unknown JSON-RPC method".

### Fix

**Two-pronged approach:**

1. **Normalization aliases** in `normalize_json_rpc_method_name()` — capability tokens now map to their primary callable method:
   - `network.discovery` → `discovery.peers`
   - `network.federation` → `songbird.federation.peers`
   - `network.relay` → `relay.status`
   - `network.stun` → `stun.status`
   - `network.igd` → `igd.status`
   - `network.tls` → `http.request`
   - `network.tor` → `tor.status`
   - `network.onion` → `onion.status`
   - `ipc.jsonrpc` / `ipc.tarpc` → `rpc.methods`
   - `network.quic` / `crypto.delegate` / `nfc.genesis` / `bluetooth.pair` → `health.readiness`

2. **New `capabilities.methods` endpoint** — returns full mapping of each token to all its callable methods (not just the primary one). Example response:
   ```json
   {
     "network.discovery": ["discovery.peers", "discovery.announce", "discovery.list_peers"],
     "network.stun": ["stun.serve", "stun.stop", "stun.status", "stun.get_public_address", "stun.bind"],
     ...
   }
   ```

### Files Changed

- `crates/songbird-types/src/json_rpc_method/mod.rs` — normalization aliases for 14 tokens
- `crates/songbird-types/src/json_rpc_method/domain_methods.rs` — `CapabilitiesMethod::Methods` variant
- `crates/songbird-universal-ipc/src/introspection/capability_tokens.rs` — `CAPABILITY_METHOD_MAP` + `capabilities_methods()`
- `crates/songbird-universal-ipc/src/introspection/mod.rs` — re-exports
- `crates/songbird-universal-ipc/src/service/dispatch.rs` — dispatch handler
- `crates/songbird-orchestrator/src/server/jsonrpc_api/mod.rs` — HTTP gateway handler

## Verification

- `cargo fmt --all -- --check` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 12,811 passed, 0 failed, 252 ignored

## Status

| Audit Item | Status |
|-----------|--------|
| GAP-MATRIX-03 TLS cipher compatibility | **Resolved** — expanded sig algs + session ID |
| Capability method gap | **Resolved** — normalization aliases + `capabilities.methods` endpoint |
