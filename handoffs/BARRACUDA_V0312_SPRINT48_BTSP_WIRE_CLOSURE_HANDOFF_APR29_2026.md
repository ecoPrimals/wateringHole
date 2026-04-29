# barraCuda v0.3.12 — Sprint 48 Handoff (BTSP-BARRACUDA-WIRE Closure + Phase 56 Response)

**Date**: April 29, 2026
**Sprint**: 48 (Phase 56 — BTSP-BARRACUDA-WIRE closure + tarpc cipher enforcement)
**Version**: 0.3.12
**Tests**: 272+ non-GPU pass, 26 BTSP compliance tests pass, 0 failures
**IPC Methods**: 50 registered
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT45_JSONRPC_EXPANSION_HANDOFF_APR26_2026.md`

---

## Context

primalSpring v0.9.20 (Phase 55) published `NUCLEUS_TWO_TIER_CRYPTO_MODEL.md`,
establishing that every primal in a NUCLEUS deployment MUST receive:
- `BEARDOG_SOCKET` — crypto delegation endpoint
- `BTSP_PROVIDER_SOCKET` — BTSP tunnel provider
- `DISCOVERY_SOCKET` — Songbird capability resolution
- `FAMILY_SEED` — Tier 1 key derivation input
- `BIOMEOS_SOCKET_DIR` — socket directory for all primals

barraCuda already had `FAMILY_SEED` and `BIOMEOS_SOCKET_DIR`. This sprint
wires the remaining three env vars.

## What Changed

### `BEARDOG_SOCKET` / `BTSP_PROVIDER_SOCKET` (composition-injected)

`discover_security_provider()` resolution chain updated:
1. **NEW**: `$BEARDOG_SOCKET` env var (first check)
2. **NEW**: `$BTSP_PROVIDER_SOCKET` env var
3. `$BIOMEOS_SOCKET_DIR/{SECURITY_DOMAIN}-{family_id}.sock`
4. `$BIOMEOS_SOCKET_DIR/{SECURITY_DOMAIN}.sock`
5. Discovery files `*.json` advertising `btsp.session.create`

When the env var points to a non-existent path, falls through with
`tracing::debug!` to the next resolution step.

### `DISCOVERY_SOCKET` (Songbird async fallback)

New `resolve_via_discovery_socket()` async function:
- Connects to Songbird via `$DISCOVERY_SOCKET` UDS
- Sends `ipc.resolve` JSON-RPC with `capability` param
- Parses the `unix` or `socket` field from the response
- Only invoked when local filesystem discovery fails AND env vars are unset
- Graceful degradation: any failure silently falls through

### `FAMILY_SEED` error message

Error text updated from:
> "BTSP handshake requires BEARDOG_FAMILY_SEED or FAMILY_SEED env var"

To:
> "BTSP handshake requires FAMILY_SEED, BEARDOG_FAMILY_SEED, or BIOMEOS_FAMILY_SEED env var"

Matches the actual 3-variable resolution chain in `resolve_family_seed_raw()`.

---

## Env Var Coverage Summary

| Variable | Status | Where |
|----------|--------|-------|
| `BEARDOG_SOCKET` | **Wired** (Sprint 46) | `btsp.rs` `discover_security_provider()` |
| `BTSP_PROVIDER_SOCKET` | **Wired** (Sprint 46) | `btsp.rs` `discover_security_provider()` |
| `DISCOVERY_SOCKET` | **Wired** (Sprint 46) | `btsp.rs` `resolve_via_discovery_socket()` |
| `FAMILY_SEED` | Wired (Sprint 44e) | `btsp.rs` `resolve_family_seed_raw()` |
| `BEARDOG_FAMILY_SEED` | Wired (Sprint 44e) | `btsp.rs` `resolve_family_seed_raw()` |
| `BIOMEOS_FAMILY_SEED` | Wired (Sprint 44e) | `btsp.rs` `resolve_family_seed_raw()` |
| `BIOMEOS_SOCKET_DIR` | Wired (Sprint 34) | `transport.rs` `resolve_socket_dir()` |

---

## Outstanding

### Tensor Encryption (P2 — nice-to-have)

Per `NUCLEUS_TWO_TIER_CRYPTO_MODEL.md`, barraCuda's purpose is `tensor` with
use case "encrypt tensor data in transit." This is explicitly rated as
**low priority** by primalSpring Phase 55. Tracked in `WHATS_NEXT.md` under P2.
Crypto deps already present (`chacha20poly1305`, `hmac`, `sha2`).

### Sprint 46b: Role-Based Naming + 12-Axis Audit

- Refactored `btsp.rs` internal identifiers from primal-specific (`beardog_stream`, `beardog`, `beardog_rpc`) to role-based (`provider_stream`, `provider`, `security_provider_rpc`) — zero hardcoded sibling primal names in runtime code
- Ecosystem-standard env var names (`BEARDOG_SOCKET`, etc.) preserved as wire contract
- 12-axis deep debt audit clean bill across all axes (file size, unsafe, unwrap, expect, TODO, deps, hardcoding, mocks, println, #[allow(, Box<dyn Error>, async-trait)

### Sprint 47: Discovery Self-Registration (Phase 55b)

- **`register_with_discovery()`** in `transport.rs` — `ipc.register` RPC to discovery service via `DISCOVERY_SOCKET` at startup
- **`discovery_capability_domains()`** in `discovery.rs` — 11 semantic capability tags derived from `REGISTERED_METHODS`: `tensor`, `math`, `stats`, `linalg`, `ml`, `spectral`, `activation`, `noise`, `rng`, `fhe`, `device`
- Wired into all startup paths (UDS server, TCP-only, service mode)
- Fire-and-forget: graceful degradation if discovery service absent
- NDJSON wire format, same pattern as `resolve_via_discovery_socket()`

### Sprint 47b: Deep Debt — Role-Based Naming + naga-exec Correctness

- Role-based naming: `register_with_songbird`→`register_with_discovery`, `songbird_capability_domains`→`discovery_capability_domains`, `SONGBIRD_EXCLUDED_DOMAINS`→`DISCOVERY_EXCLUDED_DOMAINS`
- naga-exec `binary_*_arr` silent `_ => 0.0` fallbacks → typed `NagaExecError::TypeMismatch` errors
- autotune.rs `let _ = fs::write` → `tracing::debug` observability
- 12-axis audit clean: zero files >800L (max 787L), all quality gates green

### Sprint 48: BTSP-BARRACUDA-WIRE Closure (Phase 56 Response)

primalSpring Phase 56 flagged **BTSP-BARRACUDA-WIRE (P1)**: "`guard_connection()` does
session creation but not full X25519 challenge-response on client stream. BTSP security
incomplete."

**Finding: gap is stale (resolved Sprint 44h-44i).** The full 7-step relay has been
implemented since April 24-26:

1. Read `ClientHello` (with `client_ephemeral_pub`) from client
2. `btsp.session.create` to security provider (with `family_seed`, `client_ephemeral_pub`)
3. Relay `ServerHello` (with `server_ephemeral_pub`, `challenge`) to client
4. Read `ChallengeResponse` (with HMAC `response`, `preferred_cipher`) from client
5. `btsp.session.verify` to security provider (same connection per SOURDOUGH pattern)
6. `HandshakeComplete` with `session_id`, negotiated `cipher` to client
7. Return `BtspSession` for Phase 3 frame encryption

barraCuda is a relay — it does not perform X25519 itself. The client and security
provider perform the actual DH key exchange. barraCuda forwards opaque wire values
between them. This is the correct pattern per `SOURDOUGH_BTSP_RELAY_PATTERN.md`.

**Additional fixes in Sprint 48:**

- **tarpc keyed-cipher enforcement**: `serve_tarpc_unix` now rejects BTSP connections
  that negotiated a keyed cipher (ChaCha20-Poly1305 / HMAC-SHA256). tarpc's binary
  `LengthDelimitedCodec` framing is incompatible with BTSP frame encryption. JSON-RPC
  is the correct transport for encrypted connections. Previously the tarpc path accepted
  the connection but silently bypassed post-handshake encryption.
- **2 new full-relay integration tests**: `btsp_full_relay_authenticated_null_cipher`
  and `btsp_full_relay_rejected_by_provider` in `btsp_socket_compliance.rs` — exercises
  mock security provider with `session.create` and `session.verify` over Unix sockets.

### Zero Open Gaps

barraCuda has zero open gaps. All Phase 55/55b/56 requirements are resolved.
`PRIMAL_GAPS.md` BTSP-BARRACUDA-WIRE entry should be marked RESOLVED.

---

**License**: AGPL-3.0-or-later
