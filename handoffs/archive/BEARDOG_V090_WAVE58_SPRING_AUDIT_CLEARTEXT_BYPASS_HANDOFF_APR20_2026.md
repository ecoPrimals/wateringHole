# BearDog v0.9.0 — Wave 58 Handoff

**Date**: April 20, 2026
**Trigger**: primalSpring April 20 consolidated spring audit (hotSpring L5, healthSpring L4, wetSpring L4, ludoSpring L4, neuralSpring L3)
**Commit**: `353c65f87`

## What Changed

### 1. FAMILY_SEED Documentation (README)

Springs reported "connection reset without BTSP handshake" with no guidance on the `BEARDOG_FAMILY_SEED` requirement. README now documents:

- **Three security modes** (Development / Production / Startup error) with env var matrix
- **Seed resolution order**: `FAMILY_SEED` → `BEARDOG_FAMILY_SEED` → `.family.seed` file
- **First-byte cleartext bypass**: `{` (0x7B) on first byte auto-detects cleartext JSON-RPC on both UDS and TCP, no BTSP handshake needed

### 2. Cleartext Method Advertisement (capabilities.list)

`transport_security` block in `capabilities.list` response updated:

| Field | Before | After |
|-------|--------|-------|
| `cleartext_available` | `false` in production | `true` always (first-byte bypass works in all modes) |
| `cleartext_detection` | — | `"first-byte 0x7B auto-detect on UDS and TCP"` |
| `cleartext_methods` | — | `["crypto.hash", "crypto.blake3_hash", "health.liveness", "health.readiness", "health.version", "capabilities.list", "identity.get"]` |
| `note` (production) | "BTSP handshake required" | "BTSP preferred. Cleartext JSON-RPC accepted via first-byte 0x7B bypass for listed methods." |

### For Springs

To call `crypto.hash` (or any listed cleartext method) without BTSP:
1. Open a UDS or TCP connection to BearDog
2. Send `{"jsonrpc":"2.0","method":"crypto.hash","params":{"data":"<base64>"},"id":1}\n` as the first bytes
3. The leading `{` triggers cleartext mode — no BTSP handshake needed

## Quality Gate

| Check | Status |
|-------|--------|
| `cargo fmt` | Clean |
| `cargo clippy --workspace -D warnings` | 0 warnings |
| `cargo test --workspace` | 14,786+ passing (1 pre-existing flaky: `key_export_roundtrip` HOME-sensitivity) |
| `cargo deny check` | All 4 checks pass |

## No Regressions

- No new dependencies added
- No API breaking changes (additive fields only in capabilities response)
- All existing BTSP handshake behavior preserved
