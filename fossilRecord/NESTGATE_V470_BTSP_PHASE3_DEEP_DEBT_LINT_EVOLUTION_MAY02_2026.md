# NestGate v4.7.0-dev — BTSP Phase 3, Deep Debt Sweep, Lint Evolution

**Date**: May 2, 2026
**Trigger**: primalSpring downstream audit (BTSP Phase 3 gap) + continuation of deep debt sweep

---

## Summary

Two major workstreams completed in a single session:

1. **BTSP Phase 3 (`btsp.negotiate`)** — Server-side encrypted channel negotiation, closing the last gap from the primalSpring BTSP audit
2. **Deep debt sweep** — Lint mega-list narrowing across 5 crates, hardcoding evolution, dead code cleanup, doc fixes, test isolation, and orphaned test removal

---

## What Changed

### BTSP Phase 3 — Encrypted Channel Negotiation

**Problem**: NestGate implemented BTSP Phase 1 (family-scoped sockets) and Phase 2 (server-side handshake) but had no Phase 3 (`btsp.negotiate`) — the post-handshake cipher negotiation that upgrades connections to encrypted transport.

**Fix**: Two new modules in `nestgate-rpc`:

- `btsp_phase3/mod.rs` — Core types (`Phase3Cipher`, `NegotiateParams`, `NegotiateResult`), `SessionKeys` with `ZeroizeOnDrop`, HKDF-SHA256 key derivation from `FAMILY_SEED`, ChaCha20-Poly1305 AEAD encrypt/decrypt, cipher selection logic
- `btsp_phase3/transport.rs` — `try_phase3_negotiate()` handler for `btsp.negotiate` JSON-RPC method, `run_encrypted_frame_loop()` with length-prefixed framing, generic dispatch closure

**Integration points**:
- `unix_socket_server/mod.rs` — Post-handshake intercept: first message checked for `btsp.negotiate`, switches to encrypted loop if accepted
- `isomorphic_ipc/server/mod.rs` — Same pattern for isomorphic connections
- `btsp_server_handshake/mod.rs` — `BtspSession` now stores `handshake_key` for Phase 3 derivation; `resolve_family_seed()` visibility changed to `pub(crate)`

**New dependencies**: `hkdf = "0.12"`, `sha2 = "0.10"` (workspace), `zeroize = "1"` (workspace)

**Tests**: 28 new (20 unit + 8 integration-style), all passing

### Lint Mega-List Narrowing

Crate-level `#![expect(...)]` blocks were narrowed via **real code fixes** (not relocated suppressions):

| Crate | Before | After | Key fixes |
|-------|--------|-------|-----------|
| nestgate-core | 22 lints | 16 | `mul_add`, `f64::midpoint`, char patterns, collapsible-if, `#[must_use]`, `try_from` casts |
| nestgate-zfs | 24 lints | 17 | Function refactoring, hoisted imports, explicit match patterns, `Default::default()`, variable renames, doc paragraphs |
| nestgate-api | 14 lints | 12 | `pub_underscore_fields` and `struct_excessive_bools` scoped to specific files |
| nestgate-installer lib | 12 lints | 2 | Dead code removed, unnecessary async/debug/ref_mut fixed, error docs added |
| nestgate-installer main | 12 lints | 4 | Shared fixes + `trivially_copy_pass_by_ref`, `unnecessary_wraps` |
| nestgate-storage | 5 + dead_code | 1 | `missing_const_for_fn`, `unused_self`, `needless_pass_by_value` fixed; dead_code scoped to items |

### Hardcoding Evolution

- `BEARDOG_*` env vars deprioritized behind capability-agnostic `SECURITY_*` names across `btsp_client.rs`, `storage_encryption.rs`, `btsp_server_handshake/mod.rs`
- Discovery deprecation warnings no longer embed `http://orchestration-service:8080` — reference `ORCHESTRATION_DISCOVERY_ENDPOINT` via IPC capability discovery instead

### Safety and Code Quality

- `nestgate-zfs` `#![forbid(unsafe_code)]` now **unconditional** (was `cfg_attr(not(test), ...)`)
- Dead code suppressions in nestgate-storage and nestgate-installer narrowed to per-item `#[expect(dead_code, reason = "...")]`
- 9 doc-link warnings fixed across nestgate-config, nestgate-types, nestgate-installer, nestgate-api

### Documentation

- `nestgate-core` lib.rs overview expanded to list all 9 re-export families (was missing platform, cache, security, observe)
- `nestgate-middleware` placeholder doc replaced with real crate documentation
- `tests/README.md` and `tests/DISABLED_TESTS_REFERENCE.md` updated to current metrics

### Test Isolation and Stability

- Installer tests (`configure`, `uninstall`, `doctor`) migrated from manual `HOME` mutation to `temp_env` + `XDG_DATA_HOME` scoping (fixes etcetera home-directory caching across test runs)
- Discovery timeout tests wrapped in `temp_env` to prevent `NESTGATE_CONNECT_TIMEOUT` leakage
- ETXTBSY retry loop added to `verify_installation`
- `create_pool` / `create_dataset` validation reordered (input validation before tool availability check)
- `discover_single_pool` returns `Ok(None)` when zpool binary unavailable

### Debris Removal

- `tests/integration/` (36 orphaned files — never imported by any top-level test binary)
- `tests/performance/` (1 orphaned file)
- `tests/common/templates.rs` (unused macro module)
- `tests/test.env` (unreferenced env fixture)

---

## Verification

```
cargo fmt --all --check          PASS
cargo clippy --workspace         PASS (zero own-code warnings)
  --all-targets -- -D warnings
cargo doc --workspace --no-deps  PASS (zero own-code warnings)
cargo test --workspace --lib     8,841 passing / 0 failures / 60 ignored
                                 3 consecutive clean runs
```

---

## Remaining Known Debt

- **Coverage**: 84.12%+ line — wateringHole 80% met, 90% target pending
- **Specs**: Several spec files reference `nestgate-network` (removed crate) and stale module paths — need reconciliation or archival to ecoPrimals fossil record
- **Vendor TODOs**: `vendor/rustls-webpki` contains upstream TODO/XXX comments — policy: upstream code, not first-party
- **`unreadable_literal` / `used_underscore_items`**: Remain at crate-level in nestgate-zfs (>10 hits each)

---

## Downstream Impact

- **Springs using BTSP**: Can now negotiate encrypted channels via `btsp.negotiate` against NestGate. Plaintext fallback is automatic — no breaking change for existing clients.
- **Env var consumers**: `BEARDOG_SOCKET` still works but `SECURITY_SOCKET` / `SECURITY_PROVIDER_SOCKET` / `CRYPTO_PROVIDER_SOCKET` are preferred.
- **Capability discovery**: Deprecation warnings now guide operators toward env-based endpoint configuration rather than hardcoded URLs.
