<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 101: Crypto IPC Surface for barraCuda Delegation

**Date**: May 11, 2026
**Primal**: bearDog
**Audit ref**: primalSpring Full Stadial Gate Blurb (all 13) — bearDog LOW
**Status**: RESOLVED

---

## Summary

BearDog's `crypto.*` IPC surface now covers the three crypto operations barraCuda
embeds for BTSP framing:

| barraCuda operation | Crate used directly | BearDog IPC method |
|---------------------|--------------------|--------------------|
| ChaCha20-Poly1305 AEAD | `chacha20poly1305` | `crypto.chacha20_poly1305_encrypt` / `decrypt` (pre-existing) |
| HMAC-SHA256 compute | `hmac` + `sha2` | `crypto.hmac_sha256` (pre-existing) |
| HMAC-SHA256 verify | `hmac` + `sha2` | **`crypto.hmac_verify`** (NEW) |
| HKDF-SHA256 expand | `hkdf` + `sha2` | **`crypto.hkdf_sha256`** (NEW) |

---

## New Methods

### `crypto.hkdf_sha256`

HKDF-SHA256 extract-and-expand. API contract:

```json
{
  "method": "crypto.hkdf_sha256",
  "params": {
    "ikm": "<base64 input key material>",
    "salt": "<base64 optional>",
    "info": "<base64 or UTF-8 optional>",
    "length": 32
  }
}
→ { "okm": "<base64>", "algorithm": "HKDF-SHA256", "length": 32 }
```

Tested against barraCuda's exact BTSP Phase 3 pattern:
`Hkdf::<Sha256>::new(Some(&[client_nonce ‖ server_nonce]), &session_key).expand(b"btsp-v1-phase3", &mut derived)`.

### `crypto.hmac_verify`

Constant-time HMAC-SHA256 tag verification using `subtle::ConstantTimeEq`:

```json
{
  "method": "crypto.hmac_verify",
  "params": {
    "key": "<base64>",
    "data": "<base64>",
    "mac": "<base64 expected tag>"
  }
}
→ { "valid": true, "algorithm": "HMAC-SHA256" }
```

---

## Architecture Note: IPC vs Shared Crate

Per `wateringHole` triage (`BARRACUDA_V0313_SPRINT56_CRYPTO_DEDUP_TRIAGE_MAY11_2026.md`),
per-frame BTSP AEAD via IPC adds ~1ms latency per operation — acceptable for
session setup and negotiation, but impractical for bulk data frames at line rate.

Recommended dedup path for barraCuda:
1. **Negotiate-time**: delegate HKDF, HMAC verify, session operations to BearDog IPC
2. **Frame-time**: use a shared `btsp-crypto` workspace crate that both bearDog and barraCuda depend on, avoiding IPC overhead and eliminating version skew

BearDog's IPC surface is now **sufficient** — barraCuda chooses the delegation boundary.

---

## Metrics

| Metric | Value |
|--------|-------|
| Crypto IPC methods | 105 (was 103) |
| New tests | 14 (9 handler + 5 router) |
| Total tests | 14,925+ |
| Failures | 0 |
| Quality gates | 4/4 (fmt, clippy, doc, test) |

---

## Remaining Debt

- **Secondary (stadial)**: upstream crate extraction (`wgsl-precision` if applicable, `proc-sysinfo`). No action until stadial gate.
- **barraCuda-side**: barraCuda decides delegation boundary — IPC for negotiate-time ops, shared crate for frame-time ops. Not blocked on bearDog.

---

## Dependency Chain Impact

```
bearDog crypto IPC surface  ──→  barraCuda crypto dedup (UNBLOCKED)
```

barraCuda can now:
1. Switch `btsp.negotiate` HKDF to `crypto.hkdf_sha256` IPC
2. Switch HMAC verification to `crypto.hmac_verify` IPC
3. Continue using direct crate for per-frame AEAD (performance)
4. Or extract shared `btsp-crypto` crate for full dedup
