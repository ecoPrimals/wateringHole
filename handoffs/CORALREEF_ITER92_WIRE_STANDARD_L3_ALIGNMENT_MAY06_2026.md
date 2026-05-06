<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 92: Wire Standard L3 Alignment

**Date**: May 6, 2026
**From**: coralReef team
**To**: primalSpring, all downstream springs

---

## Summary

`capabilities.list` response upgraded from Wire Standard L2 to L3 shape by adding `protocol` and `transport` fields. Cross-cutting BufReader post-negotiate audit confirmed correct. Whitespace-tolerant TCP detection assessed and determined unnecessary for our ecosystem.

## Wire Standard L3

`CapabilityListResponse` now includes:

```json
{
  "primal": "coralreef-core",
  "version": "0.1.0",
  "protocol": "jsonrpc-2.0",
  "transport": ["uds", "tcp", "tarpc"],
  "methods": ["shader.compile.spirv", "..."],
  "capabilities": ["health", "identity", "shader"]
}
```

- `protocol` field: always `"jsonrpc-2.0"` (our primary wire protocol)
- `transport` field: `["uds", "tcp", "tarpc"]` on Unix; `["tcp", "tarpc"]` on non-Unix
- Backward compatible: existing consumers ignore unknown fields via serde defaults

## Cross-Cutting Audit Results

| Item | Status | Detail |
|------|--------|--------|
| BufReader post-negotiate | Correct | BufReader passed through to `process_encrypted_frames` — buffered bytes consumed correctly by async reader |
| Whitespace-tolerant TCP | Not needed | BTSP marker classification (`{` = JSON, other = marker) correct for all ecosystem clients |
| Port 9730 | Confirmed | Operational on ironGate, primalSpring has `TCP_FALLBACK_CORALREEF_PORT = 9730` |

## Test Results

- 4,686 passing, 0 failures, 177 ignored (hardware-gated)
- Zero clippy warnings (`clippy::pedantic` + `clippy::nursery`)
- Test `capability_list_wire_standard_l2` → renamed to `capability_list_wire_standard_l3` with L3 assertions

## Downstream Impact

- No breaking changes (additive fields only)
- primalSpring and composition tooling can now read L3 envelope from coralReef
- Discovery escalation hierarchy: coralReef discoverable at tiers 3-5 (UDS/registry/TCP); tier-1 Songbird registration deferred

## primalSpring Phase 59 Gap Resolution

| Item | Status |
|------|--------|
| Wire Standard L3 on `capabilities.list` | **RESOLVED** (this iteration) |
| BufReader post-negotiate correctness | **VERIFIED** (no action needed) |
| Whitespace-tolerant TCP detection | **ASSESSED** — not applicable |
