<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — BTSP Phase 2 + Deep Debt Cleanup Handoff

**Date**: April 9, 2026  
**Primal**: LoamSpine (permanence)  
**Version**: 0.9.16  
**Session scope**: BTSP Phase 2 handshake integration, deep debt cleanup, zero-copy evolution, coverage expansion

---

## BTSP Phase 2 Handshake Integration

### What was done

- **New module `btsp.rs`** (696 lines) in `loam-spine-core` implements the consumer side of BTSP Phase 2. LoamSpine delegates all cryptographic operations to BearDog via JSON-RPC — zero crypto dependencies added to loamSpine.
- **4-step handshake**: `ClientHello` → `ServerHello` → `ChallengeResponse` → `HandshakeComplete`/`HandshakeError`. Wire format: 4-byte big-endian length-prefixed frames per `BTSP_PROTOCOL_STANDARD.md`.
- **BearDog JSON-RPC methods called**: `btsp.session.create`, `btsp.session.verify`, `btsp.negotiate`. Newline-delimited JSON-RPC 2.0 over UDS.
- **UDS listener gated**: `run_jsonrpc_uds_server` accepts `Option<BtspHandshakeConfig>`. When `BIOMEOS_FAMILY_ID` is set (non-default), every incoming UDS connection must complete the BTSP handshake before JSON-RPC methods are exposed. Without family ID, behavior is identical to pre-BTSP.
- **Socket resolution**: BearDog socket path resolved via `BEARDOG_SOCKET` env → `$BIOMEOS_SOCKET_DIR/beardog-{family_id}.sock` → platform fallback. No hardcoded primal names.
- **Consumed capability**: `"btsp"` registered in `capabilities::identifiers::external`, `niche.rs`, and `primal-capabilities.toml`.

### Limitations (documented in KNOWN_ISSUES.md)

- **`BTSP_NULL` cipher only**: Encrypted framing (ChaCha20-Poly1305) requires BearDog Phase 3 session key propagation.
- **Challenge placeholder**: Timestamp-derived bytes, not cryptographic RNG. BearDog validates regardless.

### 28 new tests

- Unit: `BtspHandshakeConfig` derivation, socket resolution (4 env combinations)
- Frame I/O: roundtrip, too-large rejection, truncated read
- Serde: `ClientHello`, `ServerHello`, `ChallengeResponse`, `HandshakeComplete`, `HandshakeError`
- Integration: mock BearDog server — full handshake success, verify rejection, cipher negotiation failure, BearDog unavailable, version mismatch

---

## Deep Debt Cleanup & Evolution

### Smart refactoring

- **`infant_discovery/mod.rs`** (711 → 570 lines): Extracted mDNS backend functions (`mdns_discover_impl`, `parse_mdns_response`, `capability_to_srv_name`) into `backends.rs` (158 lines). All production files now under 700 lines.

### Zero-copy evolution

- **`extract_rpc_result_typed`**: Eliminated `result.clone()` — replaced `serde_json::from_value(result.clone())` with borrowing `T::deserialize(result)`. Zero allocation on JSON-RPC deserialization hot path.
- **`parse_beardog_response`**: Same pattern applied to BTSP module.
- **Resilience retry**: `err_msg.clone()` eliminated — log before move instead.

### Dependency evolution

- **tarpc/opentelemetry advisory**: `RUSTSEC-2026-0007` (`opentelemetry_sdk` via tarpc 0.37) documented in `specs/DEPENDENCY_EVOLUTION.md`. Upstream blocker — awaiting tarpc 0.38+.

### Coverage expansion

- **6 tests**: `EphemeralProvenance` and `Attestation` serde roundtrips (temporal module — previously uncovered)
- **4 tests**: `StorageResultExt` trait (error module — previously untested directly)

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 1,316 | 1,373 |
| Source files | 163 | 167 |
| Max production file | 711 lines | 696 lines |
| Clippy warnings | 0 | 0 |
| Doc warnings | 0 | 0 |
| `unsafe` | 0 | 0 |
| `#[allow]` in production | 4 | 4 |

---

## Audit results (clean)

- **Zero TODOs/FIXMEs** in codebase
- **Zero mocks in production** — all `#[cfg(test)]` or feature-gated
- **Zero hardcoded primal names** outside self-knowledge
- **Zero `unwrap()`/`expect()`** in production code
- **Zero `unsafe`** — `#![forbid(unsafe_code)]` enforced
- **All `#[allow]` justified**: 2× feature-conditional `unused_async`, 2× tarpc macro `wildcard_imports`

---

## Downstream impact

| Consumer | Impact | Action needed |
|----------|--------|---------------|
| biomeOS | UDS connections to loamSpine now require BTSP when `FAMILY_ID` is set | Ensure biomeOS client performs BTSP handshake or connects without `FAMILY_ID` for dev |
| primalSpring | BTSP debt resolved — LS-03-04 closed, BTSP handshake stub evolved to full BearDog IPC | Re-validate compliance matrix |
| rhizoCrypt | `session.commit` calls via UDS will require BTSP in production | rhizoCrypt BTSP Phase 2 should be wired |
| sweetGrass | `braid.commit` calls via UDS will require BTSP in production | sweetGrass BTSP Phase 2 should be wired |
| BearDog | LoamSpine is now a BTSP consumer calling `btsp.session.*` and `btsp.negotiate` | BearDog must expose these methods on its UDS listener |

---

## Files changed

### New files
- `crates/loam-spine-core/src/btsp.rs` — BTSP handshake consumer module
- `crates/loam-spine-core/src/btsp_tests.rs` — BTSP test suite
- `crates/loam-spine-core/src/infant_discovery/backends.rs` — mDNS/DNS-SRV backend extraction

### Modified files
- `crates/loam-spine-core/src/lib.rs` — `pub mod btsp`
- `crates/loam-spine-core/src/capabilities/mod.rs` — `external::BTSP`
- `crates/loam-spine-core/src/niche.rs` — BTSP consumed capability
- `crates/loam-spine-core/src/error/mod.rs` — zero-copy `extract_rpc_result_typed`
- `crates/loam-spine-core/src/resilience.rs` — clone elimination in retry
- `crates/loam-spine-core/src/temporal/mod.rs` — new tests
- `crates/loam-spine-core/src/error/tests.rs` — StorageResultExt tests
- `crates/loam-spine-core/src/infant_discovery/mod.rs` — backend extraction
- `crates/loam-spine-core/src/infant_discovery/tests.rs` — updated references
- `crates/loam-spine-core/src/infant_discovery/tests_coverage.rs` — updated references
- `crates/loam-spine-api/src/jsonrpc/server.rs` — BTSP handshake gating
- `crates/loam-spine-api/src/jsonrpc/tests_protocol.rs` — updated call sites
- `bin/loamspine-service/main.rs` — BTSP config wiring
- `primal-capabilities.toml` — BTSP dependency
- `specs/DEPENDENCY_EVOLUTION.md` — tarpc/opentelemetry advisory
- `STATUS.md`, `KNOWN_ISSUES.md`, `README.md`, `CONTEXT.md`, `WHATS_NEXT.md` — updated metrics
