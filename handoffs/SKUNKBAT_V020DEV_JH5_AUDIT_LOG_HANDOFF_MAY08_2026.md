# skunkBat JH-5 Audit Log Implementation — May 8 2026

**Status**: Phase 1 COMPLETE — local audit pipeline live
**Priority**: Medium (JH-5)
**Registry**: 382 methods (added `security.audit_log`)
**Commit context**: primalSpring `eb0f73f`, Phase 60

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

## Remaining (Phase 2 — pending external deps)

- **rhizoCrypt DAG forwarding**: Push events to `rhizoCrypt.event.record` via JSON-RPC IPC when rhizoCrypt is discoverable
- **sweetGrass provenance braiding**: Forward security attestations as provenance entries
- **Heterogeneous source ingestion**: systemd journal adapter, tunnel log parser
- **Ionic token gating**: `security.audit_log` should require valid ionic token in enforced mode (pending JH-1 BearDog ionic tokens)

---

## Test Coverage

- 6 new tests in `audit_log.rs`: record/query, cursor pagination, ring buffer eviction, seq tracking, correlation IDs, serialization roundtrip
- Total: 362 passing (up from 356)
- Clippy: 0 warnings, `cargo fmt`: clean

---

## For primalSpring

JH-5 Phase 1 is now live. The `security.audit_log` RPC method provides the structured event feed that rhizoCrypt and sweetGrass can poll. The gate rejection events emitted by JH-0 are the primary signal — these are now captured in the audit trail rather than only existing as ephemeral tracing output.

Phase 2 (DAG forwarding, external source ingestion) is blocked on:
1. rhizoCrypt providing `event.record` IPC method (or equivalent)
2. sweetGrass providing provenance entry API
3. BearDog shipping ionic tokens (JH-1) for token-gated access to the audit log
