<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 92 Handoff

**Date**: May 7, 2026
**Primal**: BearDog (P3)
**Wave**: 92
**Scope**: Contract signing IPC confirmation & documentation

---

## Summary

primalSpring Phase 60 audit reported `crypto.sign_contract` and `crypto.verify_contract` as "not yet exposed as IPC-routable methods for cross-family compositions." Investigation confirms they have been **IPC-routable since Wave 38/42** — registered on `IonicBondHandler::methods()` and dispatched through `HandlerRegistry::route()`. The actual gap was **documentation and discoverability**, not routing.

---

## Findings

### Methods ARE IPC-routable (since Wave 38/42)

Both methods are registered in `IonicBondHandler::methods()` (8 methods total):

```
"crypto.ionic_bond.propose"
"crypto.ionic_bond.accept"
"crypto.ionic_bond.seal"
"crypto.ionic_bond.verify"
"crypto.ionic_bond.revoke"
"crypto.ionic_bond.list"
"crypto.sign_contract"        ← IPC-routable since Wave 38
"crypto.verify_contract"      ← IPC-routable since Wave 38
```

Dispatched through `HandlerRegistry::route()` — the same O(1) method map that routes all 111 JSON-RPC methods. Any client connecting to BearDog's UDS/TCP IPC socket can call these methods.

Tests verify: `methods_list` asserts `methods.len() == 8`, `methods_list_includes_contract_signing` asserts presence, plus 4 functional tests (sign, roundtrip, tamper-detection, deterministic-hash).

### Root Cause of the Audit Gap

1. **`PRIMAL_CONTRACTS.md` had no Ionic Bond section** — the 8 IonicBondHandler methods were counted in the total but not individually documented
2. **Method count was doubly wrong** — reported "103 (98 CryptoHandler + 5 IonicBondHandler)" when actual was 111 (103 CryptoHandler + 8 IonicBondHandler)
3. **primalSpring capability registry** doesn't include these methods (that's a primalSpring-side update)

---

## Changes

### `docs/PRIMAL_CONTRACTS.md`

- **New Ionic Bond section** — 8 methods fully documented with JSON-RPC request/response examples
- Detailed parameter tables for `crypto.sign_contract` and `crypto.verify_contract`
- Cross-spring signing workflow documented (for healthSpring/hotSpring/wetSpring)
- Method index expanded: items 90–97 (IonicBondHandler)
- API categories overview: added "12. Ionic Bond (8 methods)"
- Total corrected: "100+" → "111 JSON-RPC methods"
- Method index total: "103 (98+5)" → "111 (103+8)"

### `STATUS.md`

- Crypto Methods line: "103 CryptoHandler methods (98) + IonicBondHandler methods (5)" → "111 JSON-RPC methods — 103 CryptoHandler + 8 IonicBondHandler"
- Wave 78 historical entry: IonicBondHandler 5 → 8
- Wave 92 entry added

### `ROADMAP.md`

- Two historical entries: IonicBondHandler 5 → 8

### `CHANGELOG.md`

- Wave 92 entry added

---

## Method Count Reconciliation

| Handler | Documented (before) | Actual (test-verified) | Documented (after) |
|---------|--------------------|-----------------------|-------------------|
| CryptoHandler | 98 | 103 | 103 |
| IonicBondHandler | 5 | 8 | 8 |
| **Total** | **103** | **111** | **111** |

---

## Action Items for primalSpring

The following are **primalSpring-side** updates (not BearDog):

1. **`capability_registry.toml`**: Add the 8 IonicBondHandler methods (especially `crypto.sign_contract` and `crypto.verify_contract`)
2. **`PRIMAL_GAPS.md`**: Mark BearDog contract signing as RESOLVED — methods were always IPC-routable; documentation gap is now closed

---

## Files Changed (4)

1. `docs/PRIMAL_CONTRACTS.md` — Ionic Bond section + method index + count corrections
2. `STATUS.md` — method count fix + Wave 92 entry
3. `ROADMAP.md` — historical IonicBondHandler count corrections
4. `CHANGELOG.md` — Wave 92 entry
