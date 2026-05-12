# NestGate v4.7.0-dev Sessions 55-56 Handoff

**Date**: May 6-7, 2026
**Sessions**: 55, 56
**Trigger**: primalSpring downstream audit (PG-56 security, P2 namespace/streaming), deep debt sweep

---

## Summary

Session 55 fixed a BTSP authentication gap (PG-56 MEDIUM) where plain JSON-RPC
bypass allowed unauthenticated access to sensitive storage methods. Session 56
added namespace support to legacy handlers, confirmed streaming retrieval is
fully wired, then executed a deep debt sweep (storage_handlers split, lint
reason attrs, stub docs, hardcoded cleanup).

---

## Session 55: BTSP Method-Level Auth Gating (PG-56)

### Root Cause

When BTSP is required, a first-byte `{` bypass exists for biomeOS compositions
that skip the handshake. This bypass allowed **all** JSON-RPC methods through,
including sensitive ones like `storage.list`.

### Fix

- `rpc::is_btsp_exempt_method()` — shared allow-list of 10 methods: health,
  identity, capabilities, discovery
- Both server paths (`isomorphic_ipc/server/mod.rs`,
  `unix_socket_server/mod.rs`) now gate unauth connections through
  `dispatch_or_reject_unauth()` which returns `-32604 BTSP authentication
  required` for non-exempt methods

### Downstream Impact

Any client sending plain JSON-RPC over a BTSP-required connection now only
gets health/identity/capabilities/discovery. All storage, session, bonding,
model, template, audit, NAT, and ZFS methods require BTSP authentication.

---

## Session 56: Namespace + Deep Debt Sweep

### Namespace on Legacy Dispatch (primalSpring P2 Item 2)

All 10 legacy Unix socket storage handlers accept `namespace` parameter.
Path layout: `{family}/{namespace}/{key}` when provided, flat `{family}/{key}`
otherwise. Retrieve/exists fall back to flat layout for migration compat.
Path traversal validated (no `..`, `/`, `_`-prefix).

### Streaming Retrieval (primalSpring P2 Item 1)

Confirmed fully implemented — `retrieve_stream`, `retrieve_stream_chunk`,
`retrieve_range`, `object.size` all wired on all dispatch paths.
`storage.retrieve` caps at 64 MiB with error directing to streaming.

### Deep Debt Sweep

- **Split `storage_handlers.rs`** (942L → 838L): shared path/namespace helpers
  extracted to `storage_paths.rs` (124L)
- **Lint reason attrs**: All crate-root `#![expect]` blocks in nestgate-core,
  nestgate-zfs, nestgate-api, nestgate-performance now carry `reason` attrs
- **Commented-out code**: Removed disabled assertion in nestgate-config
- **Placeholder stubs**: `ConsolidatedCanonicalAdapter` and
  `ObjectStorageBackend` stub methods documented as "deferred capability"
- **Hardcoded cleanup**: `PATH_STYLE_ENDPOINT_HINTS` constant extracted;
  deprecated discovery log messages cleaned in registry.rs

---

## Verification

```
cargo fmt --all --check          PASS
cargo clippy --workspace         PASS (zero own-code warnings)
  -- -D warnings
cargo test --workspace --lib     8,879 passing / 0 failures / 60 ignored
cargo test --workspace           12,353 passing / 0 failures
```

---

## Root Docs Updated

STATUS.md, README.md, START_HERE.md, QUICK_REFERENCE.md, QUICK_START.md,
DOCUMENTATION_INDEX.md, CONTRIBUTING.md, CAPABILITY_MAPPINGS.md — all updated
from Session 50 references to Session 56 with current test counts.

---

## Downstream Impact

- **PG-56 resolved**: storage.list and other sensitive methods no longer accessible
  without BTSP handshake
- **Namespace parameter**: springs can now scope storage via `namespace` field on
  all storage methods — enables cross-spring data sharing without filesystem coupling
- **Lint reason attrs**: crate-root suppressions now justified per ecosystem standard
