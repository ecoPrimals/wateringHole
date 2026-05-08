# NestGate v4.7.0-dev Session 52 Handoff

**Date**: May 3, 2026
**Session**: 52
**Trigger**: primalSpring downstream audit — Phase 3 transport verification + JWT NUCLEUS gate

---

## Summary

Two audit items resolved plus a deep debt sweep addressing duplicate code,
dead feature flags, stale primal references, and migration commentary.

---

## What Changed

### Phase 3 Transport Hardening

primalSpring audit asked to verify the Phase 3 transport actually transitions
to encrypted I/O after `btsp.negotiate`. Confirmed working — both accept
paths enter `run_encrypted_frame_loop` with real ChaCha20-Poly1305 AEAD.

Hardening applied:
- Non-EOF read errors and decrypt failures now return `Err` instead of
  silently returning `Ok(())` — callers can distinguish clean shutdown
  from corruption/tampering
- EOF detection broadened: `"early eof"`, `"unexpected end of file"` added
  alongside existing `UnexpectedEof` checks
- New test: `encrypted_loop_returns_err_on_corrupt_frame`

### JWT NUCLEUS Bypass

`Cli::run()` now auto-detects BTSP composition via `is_btsp_required()`.
When `FAMILY_ID` is set to a non-default value and `BIOMEOS_INSECURE` is
not `"1"`, JWT validation is skipped. NUCLEUS stacks no longer need
`NESTGATE_JWT_SECRET` or explicit `NESTGATE_AUTH_MODE=delegated` to start.

Bypass hierarchy: explicit `NESTGATE_AUTH_MODE=delegated|external` >
auto-detected BTSP composition > JWT enforcement (standalone only).

### `is_btsp_required` Unified

`btsp_client.rs` now delegates to the canonical `btsp_server_handshake`
version. Eliminates divergence where the client didn't check
`BIOMEOS_FAMILY_ID`/`NESTGATE_FAMILY_ID` and didn't handle `"standalone"`.

### Deep Debt Sweep

- **Dead features**: nestgate-zfs `zfs`/`advanced`/`ai`/`performance` removed
  (declared but never cfg-gated)
- **BEARDOG refs**: `SECURITY_SOCKET` added to `storage_encryption.rs`
  discovery chain; doc/comment references updated
- **Migration commentary**: nestgate-api `config.rs` — 120 lines of duplicated
  canonical alias banners collapsed (-105 lines net)
- **Stale placeholder comment** removed from `AlertThresholds` (already concrete)

---

## Verification

```
cargo fmt --all --check          PASS
cargo clippy --workspace         PASS (zero own-code warnings)
  --all-targets -- -D warnings
cargo test --workspace --lib     8,872 passing / 0 failures / 60 ignored
```

---

## Downstream Impact

- **JWT**: NUCLEUS compositions no longer need `NESTGATE_JWT_SECRET` — if
  `FAMILY_ID` is set, BTSP handles auth automatically
- **BTSP client**: Now uses identical env-var resolution as server — springs
  setting `NESTGATE_FAMILY_ID` or `BIOMEOS_FAMILY_ID` will be detected
- **Phase 3**: Transport error propagation may surface new log messages at
  connection handler level for corrupt/tampered traffic (previously silent)
