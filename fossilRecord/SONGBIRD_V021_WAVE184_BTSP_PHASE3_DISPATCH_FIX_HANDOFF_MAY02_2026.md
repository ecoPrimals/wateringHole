# Songbird v0.2.1 — Wave 184: BTSP Phase 3 Dispatch Fix

**Date**: May 2, 2026
**Primal**: Songbird (orchestrator)
**Wave**: 184
**Scope**: Wire btsp.negotiate into binary-framed BTSP transport path
**Source**: primalSpring May 2 audit — Songbird listed as Phase 3 "NONE"

---

## Problem

The primalSpring May 2 audit listed Songbird as Phase 3: **NONE** despite the
handler existing since Wave 180. Investigation revealed the root cause:

- `handle_ndjson_session` (NDJSON path) — **had** `btsp.negotiate` interception
- `handle_btsp_frames` (binary BTSP path) — **did not** intercept `btsp.negotiate`,
  routing it through `handle_jsonrpc_request` which returned "method not found"
- `bin_interface/server.rs` (NDJSON path) — **had** `btsp.negotiate` interception

Binary-protocol clients (length-prefixed 4-byte BE framing) hit the unpatched
path and received a JSON-RPC error instead of cipher negotiation.

## Fix

**`crates/songbird-orchestrator/src/ipc/pure_rust_server/server/connection.rs`**:

1. Added `btsp.negotiate` interception in `handle_btsp_frames` before the generic
   `handle_jsonrpc_request` dispatch — same pattern as the existing NDJSON path
2. On successful cipher negotiation, the binary-framed session transitions to
   encrypted framing via `tokio::io::split(stream)` → `handle_encrypted_session`
3. `handle_btsp_on_stream` signature changed from `&mut S` to owned `S`
   (with `Send + 'static`) to enable the `split` transition
4. `PeekedStream` ownership moved from `&mut` to owned at the call site

## Transport Path Coverage (post-fix)

| Path | `btsp.negotiate` | Encrypted transition |
|------|:-:|:-:|
| NDJSON session (`handle_ndjson_session`) | YES (Wave 180) | YES → `handle_encrypted_session` |
| Binary BTSP (`handle_btsp_frames`) | **YES (Wave 184)** | **YES → `tokio::io::split` → `handle_encrypted_session`** |
| bin_interface (`handle_json_rpc_lines`) | YES (Wave 180) | YES → `handle_encrypted_json_rpc` |

## Files Modified

- `crates/songbird-orchestrator/src/ipc/pure_rust_server/server/connection.rs`
  - `handle_btsp_frames`: added btsp.negotiate interception + encrypted session transition
  - `handle_btsp_on_stream`: owned `S` instead of `&mut S`, `Send + 'static` bounds
  - Call site: `PeekedStream` passed by value
- `REMAINING_WORK.md`: Wave 184, Phase 3 status → FULL
- `CHANGELOG.md`: v0.2.1-wave184 entry

## Test Results

- 28/28 btsp_phase3 unit tests pass
- 0 new clippy warnings (`-D warnings`)
- Clean compilation across all 30 crates
- Pre-existing flaky tests (env var leakage) unchanged

## Audit Response

| Audit Finding | Status |
|--------------|--------|
| Songbird Phase 3: **NONE** | **FULL** — all 3 transport paths now dispatch `btsp.negotiate` |
