# NestGate v4.7.0-dev — Session 43p Handoff

**Date**: April 15, 2026
**Session**: 43p — Deep debt execution, streaming storage, TCP wiring, supply chain
**Triggered by**: Continued deep debt evolution from Session 43m/43n audit findings

---

## Summary

Execution pass resolving 8 tracked debt items from prior audits. All verification
gates green: fmt, clippy (pedantic+nursery), doc, deny, tests (8,472/0), coverage
81.68%, zero files over 800 lines.

---

## Changes

### 1. Streaming Storage Protocol (resolves wateringHole upstream gap)

4 new JSON-RPC methods for chunked large-tensor transfer:

| Method | Purpose |
|--------|---------|
| `storage.store_stream` | Initiate upload, returns `stream_id` + `chunk_size` |
| `storage.store_stream_chunk` | Sequential chunk upload with offset validation |
| `storage.retrieve_stream` | Initiate download, returns `stream_id` + `total_size` |
| `storage.retrieve_stream_chunk` | Chunked download with `is_last` flag |

- 4 MiB max chunk size; staging file with atomic rename-on-complete
- 1-hour TTL session cleanup; in-memory stream maps pruned on access
- Wired into semantic router, legacy unix handler, and isomorphic IPC adapter
- Tests: multi-chunk store/retrieve integrity, out-of-order rejection

### 2. TCP Alongside UDS (UniBin Compliance)

`resolve_socket_only_tcp_listen_port` implements precedence:
`--listen` → `--port` → `NESTGATE_API_PORT`/`NESTGATE_HTTP_PORT`/`NESTGATE_PORT` →
`NESTGATE_JSONRPC_TCP=1` + `DEFAULT_API_PORT` → UDS only.

TCP listener shares same JSON-RPC semantic router as UDS. Tests cover all env
combinations and TCP bind/accept round-trip.

### 3. Supply Chain (cargo deny check PASS)

- Vendored `rustls-rustcrypto` → `rustls-webpki` 0.103.12 (eliminates 0.102.x RUSTSEC)
- `rand` bumped to 0.9.x (resolves RUSTSEC-2026-0097)
- `CDLA-Permissive-2.0` added to allowlist (webpki-roots cert data)
- `RUSTSEC-2023-0071` (rsa) documented ignore — no fixed release available

### 4. File Refactoring (0 files > 800 lines)

| File | Before | After |
|------|--------|-------|
| `unix_socket_server/tests.rs` | 1000L | 5 modules (storage, health, capability, transport, common) |
| `chaos_engineering_suite.rs` | 806L | 7 modules by chaos category |
| `pool_setup_comprehensive_tests.rs` | 805L | 5 modules by test domain |
| `installer.rs` | 862L | 8 modules (metadata, requirements, ops, uninstall, update, configure, doctor, tests) |

### 5. Primal Self-Knowledge

`"nestgate"` string literals replaced with `DEFAULT_SERVICE_NAME` constant in 6
production files: `capability_based_config.rs`, `knowledge.rs`,
`consolidated_canonical/mod.rs`, `consolidated_canonical/config.rs`,
`development.rs`, `orchestrator_registration.rs`.

### 6. Deprecated API Cleanup

3 dead items removed (unused traits `SecurityHealthProvider`/`SecurityMetricsProvider`,
unused re-export `LockFreeRingBuffer`). 187 → 183 markers remain as active compat
shims for canonical-config migration.

### 7. Coverage (81.13% → 81.68%)

Tests added for 15 lowest-coverage production files targeting error branches, edge
cases, and untested constructors. BTSP `block_on` inside async fixed to proper await.

---

## Items for primalSpring to Update

1. **UPSTREAM_GAP_STATUS**: Mark `storage.retrieve` for large/streaming tensors as
   **RESOLVED** — `storage.store_stream` / `storage.retrieve_stream` implemented.
2. **ECOSYSTEM_COMPLIANCE_MATRIX**: Update NestGate `--port` from DEBT to PASS.
   Update coverage from 80% to 81.68%.
3. **PRIMAL_GAPS.md**: Remove streaming storage and TCP wiring from NestGate findings.
   Remaining tracked: coverage 81.68%→90%, 183 deprecated config markers, aarch64 musl.

---

## Verification

```
Build:    cargo check --workspace                                    PASS
Clippy:   cargo clippy --workspace --lib -- pedantic+nursery         0 warnings
Format:   cargo fmt --check                                          PASS
Docs:     cargo doc --workspace --no-deps                            PASS
Deny:     cargo deny check                                           advisories ok, bans ok, licenses ok, sources ok
Tests:    cargo test --workspace --lib                               8,472 passed, 0 failed, 60 ignored
Coverage: cargo llvm-cov --workspace --lib --summary-only            81.68% line
Files:    find . -name '*.rs' | xargs wc -l | awk '$1>800'          0 files
```

---

## Files Changed (key)

| File | Change |
|------|--------|
| `nestgate-rpc/src/rpc/storage_stream.rs` | NEW — streaming storage protocol |
| `nestgate-rpc/src/rpc/semantic_router/storage.rs` | +4 streaming method routes |
| `nestgate-rpc/src/rpc/semantic_router/mod.rs` | +4 dispatch arms |
| `nestgate-rpc/src/rpc/semantic_router/capabilities.rs` | +4 methods in advertisement |
| `nestgate-rpc/src/rpc/unix_socket_server/mod.rs` | +4 streaming dispatch + test split |
| `nestgate-bin/src/commands/bind.rs` | `resolve_socket_only_tcp_listen_port` |
| `nestgate-bin/src/commands/service.rs` | TCP listener wiring in socket-only mode |
| `vendor/rustls-rustcrypto/` | Vendored with rustls-webpki 0.103.12 |
| `deny.toml` | CDLA-Permissive-2.0, RUSTSEC-2023-0071 ignore |
| `nestgate-installer/src/installer/` | 8-module split |
| 6 production files | `DEFAULT_SERVICE_NAME` replacing `"nestgate"` literals |
| 15 production files | New `#[cfg(test)]` tests for coverage |
| Root docs | README, STATUS, CONTEXT, CHANGELOG, CAPABILITY_MAPPINGS updated |
