<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# rhizoCrypt v0.13.0-dev — Deep Debt: Structured IPC, tarpc 0.37, NDJSON Streaming Handoff

**Date**: March 16, 2026 (session 14)
**Primal**: rhizoCrypt v0.13.0-dev
**Status**: Production Ready
**Previous**: RHIZOCRYPT_V013_CONTENT_INDEX_SPEC_CLEANUP_HANDOFF_MAR16_2026 (session 13)

---

## Summary

Executed deep debt resolution across 7 absorption candidates identified in the
cross-ecosystem review. Structured IPC errors replace opaque strings, tarpc
bumped to 0.37, capability domain introspection enables biomeOS routing
decisions, NDJSON streaming types support pipeline coordination, DI config
pattern reduces test env mutation, and constant provenance documentation
explains every magic number.

---

## Changes

### 1. Structured IPC Error Types (absorbed: healthSpring V28)

- **Pattern source**: healthSpring V28 `SendError` enum
- **What**: Added `IpcErrorPhase` enum with 7 variants to `error.rs`
  - `Connect` — socket unreachable or missing
  - `Write` — broken pipe, request write timeout
  - `Read` — response read timeout, malformed response
  - `InvalidJson` — response body is not valid JSON
  - `HttpStatus(u16)` — non-2xx HTTP status
  - `NoResult` — JSON-RPC response missing `result` field
  - `JsonRpcError(i64)` — remote primal returned error object
- **Impact**: Evolved `unix_socket.rs` from `RhizoCryptError::Integration(String)` to
  `RhizoCryptError::Ipc { phase, message }` across all IPC lifecycle points
- **Ecosystem benefit**: Enables targeted retry strategies (retry on Connect/Write,
  don't retry on JsonRpcError/-32601)

### 2. tarpc 0.34 → 0.37

- Bumped workspace dependency, resolving `RUSTSEC-2024-0387` (opentelemetry_api)
- Updated `deny.toml`: removed resolved advisory ignore, 4 transitive advisories remain tracked
- Upgraded transitive deps: opentelemetry 0.30, tokio-serde 0.9, tarpc-plugins 0.14

### 3. Capability Domain Introspection (absorbed: ludoSpring V20)

- **Pattern source**: ludoSpring V20 `capability_domains.rs`
- Added `CapabilityDomain`, `CapabilityMethod` structs with `external: bool` flag
- `CAPABILITY_DOMAINS` constant organizes 23 methods into 3 domains (dag, health, capability)
- `capability_list()` now includes:
  - `domains` — structured domain descriptors
  - `locality` — `{ local: 23, external: 0 }` counts
  - Per-method `external` flag
- All rhizoCrypt methods are local (CPU-only infrastructure)
- biomeOS can now distinguish in-process vs IPC-routed capabilities

### 4. DI Config Reader (absorbed: sweetGrass v0.7.15)

- Added `RpcConfig::from_env_reader(F)` accepting any `Fn(&str) -> Result<String, VarError>`
- `from_env_or_default()` delegates to `from_env_reader(|key| std::env::var(key))`
- Tests use mock readers: zero `temp-env` dependency, zero `unsafe` env mutation

### 5. NDJSON Streaming (absorbed: biomeOS v2.43)

- New `streaming` module in `rhizo-crypt-rpc`:
  - `StreamItem` enum: `Data`, `Progress`, `End`, `Error` (recoverable/fatal)
  - `StreamingAppendResult` for streaming `event.append_batch` responses
  - `parse_ndjson_line()` for pipeline consumption
  - `to_ndjson_line()` for pipeline production
- biomeOS Pipeline graphs can wire bounded `mpsc` channels between springs

### 6. Constant Provenance Documentation

- All key constants in `constants.rs` now include provenance:
  - `Derivation:` — how the value was determined
  - `Source:` — external specification reference
  - `Chosen:` — rationale for the specific value
  - `Validated:` — which tests or benchmarks confirm it

### 7. Debris Cleanup

- Fixed `Edition: 2021` → `Edition: 2024` in `rhizocrypt version` output
- Fixed K8s ConfigMap: `RHIZOCRYPT_HOST` → `RHIZOCRYPT_RPC_HOST`, `RHIZOCRYPT_PORT` → `RHIZOCRYPT_RPC_PORT`
- Updated README: 1222→1244 tests, 110→118 SPDX files, tarpc 0.37, NDJSON streaming

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy` (pedantic + nursery + cargo, all features) | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps -D warnings` | Clean |
| `cargo test --workspace --all-features` | 1244 pass, 0 fail |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `unsafe_code = "deny"` | Workspace-wide |
| `unwrap_used`/`expect_used` | `"deny"` workspace-wide |
| SPDX headers | All 118 `.rs` files |
| Max file size | All under 1000 lines (max 867) |
| Production unwrap/expect | Zero |
| TODOs/FIXMEs in production | Zero |

---

## Artifacts

### New Files
- `crates/rhizo-crypt-rpc/src/streaming.rs` — NDJSON streaming types (233 lines)
- `wateringHole/handoffs/RHIZOCRYPT_V013_DEEP_DEBT_IPC_TARPC_STREAMING_HANDOFF_MAR16_2026.md`

### Modified Files
- `crates/rhizo-crypt-core/src/error.rs` — `IpcErrorPhase` enum, `Ipc` error variant
- `crates/rhizo-crypt-core/src/clients/adapters/unix_socket.rs` — structured IPC errors
- `crates/rhizo-crypt-core/src/niche.rs` — `CapabilityDomain`, `CapabilityMethod`, `all_methods()`
- `crates/rhizo-crypt-core/src/constants.rs` — provenance documentation on all constants
- `crates/rhizo-crypt-core/src/config.rs` — `from_env_reader()` DI pattern
- `crates/rhizo-crypt-core/src/lib.rs` — re-export `IpcErrorPhase`
- `crates/rhizo-crypt-rpc/src/lib.rs` — register streaming module, exports
- `crates/rhizocrypt-service/src/lib.rs` — Edition 2024 version string
- `Cargo.toml` — tarpc 0.34 → 0.37
- `deny.toml` — removed stale advisory, tightened wildcards
- `k8s/deployment.yaml` — canonical env var names
- `README.md` — updated metrics
- `CHANGELOG.md` — session 14 entry

---

## Absorption Sources

| Pattern | Source | Priority |
|---------|--------|----------|
| Structured IPC errors | healthSpring V28 `SendError` | P1 |
| Capability domain introspection | ludoSpring V20 `capability_domains.rs` | P2 |
| DI config reader | sweetGrass v0.7.15 | P2 |
| NDJSON streaming | biomeOS v2.43 Pipeline coordination | P2 |
| tarpc 0.37 | biomeOS ecosystem alignment | P1 |
| Constant provenance | neuralSpring v1.06 pattern | P2 |

---

## Next Steps

1. **NDJSON handler wiring**: Connect `StreamItem` types to axum SSE or chunked response in handler
2. **Content Similarity Index Phase 1**: Implement LSH function (ISSUE-012)
3. **ProvenancePipeline impl**: Implement `ProvenancePipeline` trait from `provenance-trio-types`
4. **Collision Layer coordination**: Research spec with LoamSpine (ISSUE-013)

---

## Cumulative Session Stats (sessions 1–14)

| Metric | Value |
|--------|-------|
| Tests | 1244 passing |
| Coverage | 92.32% line coverage |
| Clippy warnings | 0 |
| `unsafe` blocks | 0 |
| Source files | 118 `.rs` |
| Max file size | 867 lines |
| Specs | 8 complete + 1 experimental |
| AGPL-3.0 SPDX | All files |

---

*rhizoCrypt: The memory that knows when to forget — and now knows how to say what went wrong.*
