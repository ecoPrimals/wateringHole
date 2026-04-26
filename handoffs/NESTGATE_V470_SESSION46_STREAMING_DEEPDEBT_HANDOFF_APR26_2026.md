# NestGate Session 46 — Streaming Storage, BTSP Relay Fixes, Deep Debt Elimination

**Date**: April 26, 2026  
**Version**: 4.7.0-dev  
**Primal**: NestGate (storage & discovery)

---

## Summary

Session 46 resolved three major audit findings from primalSpring and completed a
comprehensive deep debt elimination pass. The BTSP relay chain is now fully functional
(family_seed base64-encoded, persistent BufReader for multi-call relay, connection reuse
for create+verify). Streaming storage is wired end-to-end for both UDS and HTTP
transports. All remaining hardcoded ports, commented-out tests, and bare `#[ignore]`
annotations have been cleaned.

---

## Changes

### 1. BTSP Relay — family_seed Encoding Fix (primalSpring audit)

- `btsp_server_handshake/mod.rs`: base64-encode `family_seed` before sending to
  `btsp.session.create` (BearDog base64-decodes for HKDF key derivation)
- Resolves: `"BTSP: handshake failed — client could not prove family membership"`

### 2. BTSP Relay — Verify Connection Fix (primalSpring audit)

- `JsonRpcClient`: persistent `BufReader<UnixStream>` preserves buffered data across
  multiple `call()` invocations (no more nested BufReader)
- `btsp_server_handshake`: reuses same `bd_client` connection for both `create` and
  `verify` calls (was opening new connection, causing broken pipe)
- `resolve_family_seed()`: trims trailing whitespace from env value
- `HandshakeComplete` struct includes `status: "ok"` field

### 3. Streaming Storage — HTTP Dispatch & Large-Payload Guard (primalSpring audit)

- **HTTP dispatch**: new `storage_stream_methods.rs` registers `storage.store_stream`,
  `store_stream_chunk`, `retrieve_stream`, `retrieve_stream_chunk` with jsonrpsee
  (previously "method not found" for HTTP clients)
- **Large-payload guard**: `storage.retrieve` (UDS) and `storage.object.retrieve` (HTTP)
  return error with streaming guidance when objects exceed 64 MiB
- **Blob path fallback**: `retrieve_stream_begin` checks namespaced path first, falls
  back to flat blob path for cross-method interop (`store_blob` ↔ `retrieve_stream`)

### 4. Deep Debt Cleanup

- **Hardcoded port elimination**: added `JSONRPC` constant (8092) to
  `runtime_fallback_ports`; wired into `JsonRpcConfig::default()`; named
  `DEV_HTTP_FALLBACK` constant in ZFS health config
- **Commented-out tests removed**: dead tests referencing deleted types
  (`PerformanceProjection`, `CostQuery`) cleaned from `storage_tests.rs`
- **Bare `#[ignore]` annotated**: all 7 chaos tests in
  `network_failure_scenarios_modern.rs` now carry `= "Chaos test — run explicitly
  with --ignored"`

---

## Metrics

```
Tests:           8,822 passing, 0 failures, 60 ignored (cargo test --workspace --lib)
Clippy:          PASS — cargo clippy --workspace -- -D warnings (zero warnings)
Format:          CLEAN — cargo fmt --check
Build:           PASS — cargo check --workspace
Coverage:        84.12%+ line (last measured Apr 16; +288 tests since)
Files > 800L:    0
Unsafe:          0 (forbid on all crate roots)
#[allow] in prod: 0
todo!/unimpl!:   0 in production
Bare #[ignore]:  0
Commented-out tests: 0
Hardcoded ports: 0 (all named constants)
```

---

## Remaining Work

| Area | Status |
|------|--------|
| Coverage 84% → 90% | ~6 pp gap; ZFS (needs real ZFS), installer (platform), binary entrypoints |
| Vendored `rustls-rustcrypto` | Track upstream for `rustls-webpki` 0.103.12+ — drop `vendor/` when published |
| Cross-arch CI | aarch64/armv7/riscv64 musl builds pass `cargo check`; CI pipeline not yet wired |

---

## Verification

```bash
cargo check --workspace                                    # PASS
cargo clippy --workspace -- -D warnings                    # PASS (0 warnings)
cargo fmt --check                                          # PASS
cargo test --workspace --lib                               # 8,822 passed, 60 ignored, 0 failed
```

---

**Ref**: `primals/nestgate/STATUS.md`, `primals/nestgate/README.md`
