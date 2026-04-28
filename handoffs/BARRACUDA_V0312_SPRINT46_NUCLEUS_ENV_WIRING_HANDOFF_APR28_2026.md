# barraCuda v0.3.12 — Sprint 46/46b Handoff (NUCLEUS Env Wiring + Deep Debt)

**Date**: April 28, 2026
**Sprint**: 46/46b (Phase 55 alignment + role-based naming + 12-axis audit)
**Version**: 0.3.12
**Tests**: 269+ non-GPU pass, 29 BTSP tests pass, 0 failures
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

### Zero Open Gaps

barraCuda has zero open gaps. All Phase 55 env var requirements are now wired.

---

**License**: AGPL-3.0-or-later
