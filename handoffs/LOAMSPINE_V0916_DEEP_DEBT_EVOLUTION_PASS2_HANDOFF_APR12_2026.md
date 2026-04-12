<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Deep Debt & Evolution Pass 2 Handoff

**Date**: April 12, 2026
**Version**: 0.9.16
**Tests**: 1,382 (0 failures)
**Source files**: 175 `.rs` (+ 3 fuzz targets)
**Coverage**: 90.92% line / 89.09% branch / 92.92% region

---

## Summary

Second deep debt evolution pass on LoamSpine v0.9.16, driven by primalSpring
downstream audit findings and continued cleanup of hardcoding, stale primal
name coupling, and inline test sprawl.

---

## Changes

### Connection-Close Bug Fixed (primalSpring Audit Item)

**Root cause**: `handle_http_request` in JSON-RPC TCP server was single-shot —
wrote `Connection: close` after every HTTP response and returned. Clients had
to reconnect for each JSON-RPC call.

**Fix**: Evolved to HTTP/1.1 keep-alive loop. Server reads subsequent HTTP
requests on the same TCP connection until the client sends `Connection: close`
or EOF. NDJSON path was already persistent (unaffected).

**Tests**: `tcp_http_persistent_connection_keepalive` (3 sequential requests on
one socket) and `tcp_http_connection_close_header_respected` (verifies EOF after
client-requested close).

**Resolves**: primalSpring audit item — "loamSpine connection closes after first
response (workaround: call capabilities() before health_check())".

### BTSP Provider Decoupled from Hardcoded Primal Name

`BTSP_PROVIDER_PREFIX` ("beardog") evolved from hardcoded constant to
env-configurable `BTSP_PROVIDER` with "beardog" as default fallback.

- `BtspHandshakeConfig.beardog_socket` → `provider_socket`
- `beardog_socket_name()` → `provider_socket_name(family_id, provider_override)`
- `resolve_beardog_socket_with()` → `resolve_provider_socket_with(family_id, socket_dir, provider_override)`
- Backward-compatible `beardog_socket()` accessor retained
- 2 new tests for custom provider name resolution

### Smart Test Extraction (5 Files)

| File | Before → After | Extracted to |
|------|---------------|-------------|
| `streaming.rs` | 354 → 203 | `streaming_tests.rs` |
| `health.rs` | 482 → 347 | `health_tests.rs` |
| `service/mod.rs` | 438 → 277 | `service/service_mod_tests.rs` |
| `config.rs` | 370 → 285 | `config_tests.rs` |
| `lib.rs` | 532 → 374 | `lib_tests.rs` |

All using `#[path = "..."] mod tests;` pattern — zero churn, production code
cohesion preserved.

### Stale Primal Name Cleanup

All production doc comments referencing deprecated "Songbird" discovery primal
evolved to generic capability-based language across 7 files. Transport docs now
describe "capability-discovered HTTP provider" instead of coupling to a specific
primal.

### Doc Infrastructure

- Broken `read_ndjson_stream_with` intra-doc link → `read_ndjson_stream_bounded`
- Root docs (README, CONTEXT, CONTRIBUTING) reconciled with STATUS.md metrics
- WHATS_NEXT.md updated with latest pass

---

## Gates

| Check | Status |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-targets --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (1,382 tests, 0 failures) |
| `cargo deny check` | PASS (advisories, bans, licenses, sources ok) |

---

## Ecosystem Impact

- **Trio IPC**: Connection-close fix directly benefits any partner (wetSpring,
  ludoSpring, healthSpring) that uses HTTP-mode JSON-RPC over TCP. Partners
  no longer need to reconnect between calls.
- **BTSP**: Provider socket naming is now runtime-configurable. Deployments
  with non-BearDog handshake providers can set `BTSP_PROVIDER=custodian` (or
  similar) without code changes.
- **Compliance Matrix**: Tier 10 re-validation now possible — the LS-03
  connection stability issue that blocked composition checks is resolved.

---

## Remaining Debt (LOW)

- `sweetGrass` coverage 87→90% (not LoamSpine scope)
- Witness chain validation under NUCLEUS mesh (composition-level, low urgency)
- `bincode v1 → v2` migration (tracked in `specs/DEPENDENCY_EVOLUTION.md`)
- `mdns` crate evolution (`async-std` advisories; feature-gated, optional)

---

## Files Changed

- `crates/loam-spine-api/src/jsonrpc/server.rs` — HTTP/1.1 keep-alive loop
- `crates/loam-spine-api/src/jsonrpc/tests_protocol.rs` — 2 new HTTP tests
- `crates/loam-spine-core/src/btsp/config.rs` — Provider-agnostic naming
- `crates/loam-spine-core/src/btsp/mod.rs` — Re-export updates
- `crates/loam-spine-core/src/btsp_tests.rs` — Updated for new APIs
- `crates/loam-spine-api/src/jsonrpc/uds.rs` — `provider_socket` field
- `bin/loamspine-service/main.rs` — Provider log message
- 5 new test files (streaming, health, service_mod, config, lib)
- 7 production files with Songbird doc cleanup
- 5 root markdown docs reconciled
- `STATUS.md` — Updated metrics and changelog
