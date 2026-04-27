<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 70: Identity Fallback Alignment

> April 27, 2026

## Summary

Resolved ludoSpring launcher audit: "BearDog needs both NODE_ID and BEARDOG_NODE_ID set, or fails silently."

**Root cause:** BearDog has always accepted either variable (not both). The actual issue was inconsistent fallback values — `get_node_id()` in handler utils returned `"unknown"` while `PrimalIdentity::from_env()` and `SocketConfig` returned `standalone-{uuid}`. This meant the identity reported by `primal.info` could diverge from the socket path's identity when no env vars were set.

## Changes

| File | Change |
|------|--------|
| `handlers/utils.rs` | `get_node_id_with()` now falls back to `resolve_process_node_id()` (same ephemeral `standalone-{uuid}` as `PrimalIdentity`); `get_family_id_with()` now falls back to `"standalone"` instead of `"unknown"` |
| `README.md` | Explicit note: only ONE of `NODE_ID` / `BEARDOG_NODE_ID` needed (not both) |

## Env var resolution (all three sites now aligned)

```
BEARDOG_NODE_ID → NODE_ID → HOSTNAME → standalone-{uuid} (ephemeral, stable per-process)
BEARDOG_FAMILY_ID → FAMILY_ID → BIOMEOS_FAMILY → "standalone"
```

## Downstream impact

- **ludoSpring / plasmidBin launchers**: No launcher changes needed — BearDog works correctly with just `NODE_ID` set. The plasmidBin patch that sets both vars is harmless but unnecessary.
- **hotSpring HS-005/006**: Ionic bond negotiation and BTSP stream encryption for GPU lease noted as future ecosystem needs — no BearDog changes needed now.
