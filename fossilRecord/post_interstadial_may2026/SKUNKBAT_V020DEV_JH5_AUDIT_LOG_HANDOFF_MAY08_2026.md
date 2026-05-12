# skunkBat JH-5 Audit Log Implementation — May 8 2026

**Status**: Phase 2 COMPLETE — all event kinds emitted from live code + L3 capabilities drift fixed
**Priority**: Medium (JH-5)
**Registry**: 389 methods (registered in ecosystem)
**Commit context**: primalSpring `0d7841b`, Phase 60

---

## What Was Done

### 1. `AuditLog` Ring Buffer (`observability::audit_log`)

New module: `crates/skunk-bat-core/src/observability/audit_log.rs`

- Thread-safe bounded ring buffer (default 1024 events)
- Cursor-based polling via monotonic sequence numbers
- Structured `SecurityEvent` with `seq`, `timestamp`, `source`, `severity`, `kind`, `correlation_id`

### 2. Event Types (`EventKind` enum)

| Variant | Source | Trigger |
|---------|--------|---------|
| `GateRejection` | MethodGate | Enforced mode rejects unauthenticated protected call |
| `GatePermissiveAllow` | MethodGate | Permissive mode allows unauthenticated protected call (warning) |
| `ThreatDetected` | ThreatDetection | Behavioral/genetic/intrusion anomaly detected |
| `DefenseAction` | DefenseEngine | Quarantine/alert/block action taken |
| `BtspNegotiate` | Transport | Phase 3 negotiate completion (success or failure) |
| `BtspDecryptFailure` | Transport | AEAD frame decryption error |
| `LifecycleTransition` | Lifecycle | Primal state changes |

### 3. Dispatch Integration

- `dispatch()` automatically records `GateRejection` on enforced rejection
- `dispatch()` records `GatePermissiveAllow` on permissive-mode protected calls without token
- Events flow into the `SkunkBat.audit_log` instance (accessible via `audit_log()`)

### 4. RPC Method: `security.audit_log`

```json
{
  "method": "security.audit_log",
  "params": { "since_seq": 0, "limit": 100 }
}
```

Response:
```json
{
  "events": [ ... ],
  "latest_seq": 42,
  "count": 5
}
```

Cursor-based pagination: pass `latest_seq` as next `since_seq` for polling.

---

## Phase 2 — Event Instrumentation (May 8)

All `EventKind` variants are now emitted from live code paths:

| EventKind | Emission Site | Trigger |
|-----------|--------------|---------|
| `GateRejection` | `dispatch()` | Enforced mode rejects protected call |
| `GatePermissiveAllow` | `dispatch()` | Permissive mode allows unauthenticated protected call |
| `ThreatDetected` | `security.detect` dispatch | Each detected threat |
| `DefenseAction` | `security.respond` dispatch | Successful defense response |
| `BtspNegotiate` | `try_negotiate_upgrade()` | Negotiate success or failure |
| `BtspDecryptFailure` | `run_encrypted_frame_loop()` | AEAD decrypt error |
| `LifecycleTransition` | `PrimalLifecycle::start/stop` | State transitions |

### L3 Wire Compliance Fix

`capabilities.list` security methods now includes `"audit_log"` (was missing in Phase 1).

---

## Remaining (Phase 3 — pending external deps)

- **rhizoCrypt DAG forwarding**: Push events to `provenance.create` / `provenance.attribute` via IPC
- **sweetGrass provenance braiding**: Forward security attestations via `braid.create` / `braid.anchor`
- **Heterogeneous source ingestion**: systemd journal adapter, tunnel log parser
- **Ionic token gating**: `security.audit_log` should require valid ionic token in enforced mode

---

## Test Coverage

- 7 tests in `audit_log.rs` + 1 dispatch integration test for `security.audit_log`
- Total: 363 passing (up from 356 pre-JH-5)
- Clippy: 0 warnings, `cargo fmt`: clean

---

## For primalSpring

JH-5 Phases 1–2 are complete. All event kinds are emitted from live code. The audit trail is
fully functional for local observability. `security.audit_log` is the stable IPC interface for
downstream consumers (rhizoCrypt, sweetGrass) to poll security events.

Phase 3 (DAG forwarding, external source ingestion) is blocked on:
1. rhizoCrypt providing `provenance.create` / `provenance.attribute` IPC methods
2. sweetGrass providing `braid.create` / `braid.anchor` IPC methods
3. BearDog shipping ionic tokens (JH-1) for authenticated cross-primal IPC
