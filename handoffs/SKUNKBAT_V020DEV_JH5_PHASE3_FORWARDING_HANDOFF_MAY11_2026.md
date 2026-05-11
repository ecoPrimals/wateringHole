# skunkBat JH-5 Phase 3 — Cross-Primal Audit Forwarding — May 11 2026

**Status**: SHIPPED
**Priority**: Medium (JH-5 Phase 3)
**Unblocked by**: JH-11 (resolved May 10)
**Tests**: 369 passing (up from 363)
**Files**: 47 source files

---

## What Was Done

### `forwarding.rs` (`skunk-bat-integrations`)

New module implementing the cross-primal audit event forwarding pipeline:

**Architecture:**
- Background `tokio::spawn` task started on server boot
- Polls `AuditLog` ring buffer every 10 seconds (cursor-based, no duplicate delivery)
- Forwards events with severity >= Warn to two targets:
  - **rhizoCrypt** via `dag.event.append` (tamper-evident DAG vertices)
  - **sweetGrass** via `braid.create` (provenance attribution braids)

**Endpoint Resolution (capability-based, zero hardcoding):**
- UDS primary: `$BIOMEOS_SOCKET_DIR/provenance.sock` / `attribution.sock`
- TCP fallback: `$RHIZOCRYPT_ENDPOINT` / `$SWEETGRASS_ENDPOINT` env vars
- Uses existing `rpc::call()` with UDS-first/TCP-fallback transport

**Event Payload (to rhizoCrypt `dag.event.append`):**
```json
{
  "event_type": "security_audit",
  "source_primal": "skunkbat",
  "seq": 42,
  "timestamp": "...",
  "severity": "Warn",
  "event_source": "MethodGate",
  "payload": { "GateRejection": { "method": "...", "origin": "..." } },
  "correlation_id": null
}
```

**Event Payload (to sweetGrass `braid.create`):**
```json
{
  "braid_type": "security_attestation",
  "source": "skunkbat",
  "anchor": { "seq": 42, "timestamp": "...", "source": "MethodGate", "severity": "Warn" },
  "payload": { "GateRejection": { "method": "...", "origin": "..." } },
  "correlation_id": null
}
```

**Behavior:**
- Best-effort delivery: if targets are unreachable, warn-log and retry next poll
- Severity filtering: Info events (lifecycle transitions) stay local-only
- No infinite retry: cursor advances after attempt, preventing unbounded memory/backlog
- Configurable: `ForwardingConfig` controls interval, timeout, min severity, per-target enable

### Server Wiring

`ipc/mod.rs` spawns `forwarding::run_forwarding_loop` with a clone of the audit log after
TCP/UDS listeners are active.

---

## For rhizoCrypt Team

skunkBat will call your `dag.event.append` method via UDS (`provenance.sock`) or TCP
(`RHIZOCRYPT_ENDPOINT`). Please ensure this method accepts the payload shape above.
If `dag.event.append` is not your canonical method name, let us know and we'll align.

## For sweetGrass Team

skunkBat will call your `braid.create` method via UDS (`attribution.sock`) or TCP
(`SWEETGRASS_ENDPOINT`). Please ensure this method accepts the payload shape above.

## For primalSpring

JH-5 is complete (Phases 1–3). The full pipeline:
1. Security events generated from live code paths (gate, threats, defense, BTSP, lifecycle)
2. Stored in local ring buffer, queryable via `security.audit_log` RPC
3. Forwarded to rhizoCrypt DAG + sweetGrass braids via authenticated cross-primal IPC

The 8 springs that wire skunkBat into deploy graphs will get cross-primal audit logging
once rhizoCrypt and sweetGrass accept the forwarded events in composition.

---

## Test Coverage

- 6 new tests: unreachable DAG/braid, default config, endpoint resolution, cursor advance, severity filtering
- Total: 369 passing
- Clippy: 0 warnings, `cargo fmt`: clean, `cargo deny`: clean
