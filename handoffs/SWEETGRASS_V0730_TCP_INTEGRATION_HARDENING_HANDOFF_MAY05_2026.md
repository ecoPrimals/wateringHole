# sweetGrass v0.7.30 — TCP Integration Hardening + HTTP Port UX

**Date:** May 5, 2026
**From:** sweetGrass Team
**To:** All Ecosystem Partners (especially primalSpring, biomeOS)
**Re:** Gap 10 Resolution + HTTP Port Configuration

---

## Summary

Resolves three items from primalSpring Phase 58b downstream audit:

1. **Gap 10 — TCP BTSP misclassification** (FIXED): `detect_protocol` now
   skips leading ASCII whitespace before classifying connections. Clients
   sending `\n{"jsonrpc":"2.0",...}` are correctly routed to JSON-RPC
   instead of the length-prefixed BTSP path.

2. **HTTP port UX** (FIXED): New `--http-port` / `SWEETGRASS_HTTP_PORT`
   CLI flag for direct HTTP port configuration. HTTP is the primary
   integration surface for health probes and JSON-RPC.

3. **Port conflict 9800** (DOCUMENTED): Recommended TCP allocation is
   **9850** per primalSpring's `TCP_FALLBACK_SWEETGRASS_PORT` assignment.
   No code default — TCP port is always explicit via `--port`.

---

## What Changed

### Whitespace-Tolerant Protocol Autodetect

`peek.rs` `detect_protocol()` now skips leading `\n`, `\r`, `\t`, ` `
before reading the decisive first byte. This fixes a class of
misclassification bugs where:

- Clients sending `\n{"jsonrpc":"2.0",...}` had the `\n` (0x0A) treated
  as a BTSP frame length byte, producing "BTSP frame too large" errors
- Shell scripts or tools inserting blank lines before JSON payloads
  would be misrouted
- JSON-RPC batch `[{...}]` starting with `[` after whitespace would fail

Real BTSP length-prefixed framing is unaffected: valid BTSP length bytes
(big-endian u32) are never ASCII whitespace.

### New `--http-port` CLI Flag

```
sweetgrass server --http-port 8080
```

Equivalent to `--http-address 0.0.0.0:8080` but simpler for operators.
When both `--http-port` and `--http-address` are provided, `--http-port`
takes precedence. Environment: `SWEETGRASS_HTTP_PORT=8080`.

### Port Allocation Guide

| Transport | Flag | Default | Recommended |
|-----------|------|---------|-------------|
| HTTP REST+JSON-RPC | `--http-port` / `--http-address` | `0.0.0.0:0` (dynamic) | Explicit port for production |
| TCP JSON-RPC | `--port` | Disabled | **9850** (avoids biomeOS 9800) |
| tarpc | `--tarpc-address` | `0.0.0.0:0` (dynamic) | Dynamic OK |
| UDS | `--socket` | Auto-resolved | Default is correct |

---

## Discovery Tier Support

sweetGrass currently supports:

| Tier | Mechanism | Status |
|------|-----------|--------|
| 1 | Songbird `ipc.resolve` | Not implemented |
| 2 | biomeOS Neural API `capability.discover` | Not implemented |
| **3** | **UDS filesystem convention** | **Supported**: `sweetgrass.sock`, `sweetgrass-{family}.sock`, `provenance.sock` symlink |
| **4** | **Socket registry / manifests** | **Supported**: `RegistryDiscovery` via `DISCOVERY_ADDRESS` |
| 5 | TCP probing (tolerances) | Not implemented |

sweetGrass is UDS-primary. Tier 3 is the recommended discovery path.

---

## Metrics

- **Version:** 0.7.30
- **Tests:** 1,495 pass, 0 failures
- **Source files:** 199 `.rs` (55,960 LOC), max 763 lines
- **Clippy:** 0 warnings (`pedantic` + `nursery`, `-D warnings`)
- **`cargo deny check`:** clean (advisories, bans, licenses, sources)
- **Unsafe code:** 0 (`#![forbid(unsafe_code)]` on all 10 crates)

---

## For Downstream Partners

- **primalSpring**: Gap 10 is resolved. TCP JSON-RPC with leading
  whitespace will route correctly. Recommended port 9850 is documented.
- **biomeOS**: TCP 9800 conflict is avoided by not having a default TCP
  port. When deployed, use `--port 9850` or `SWEETGRASS_PORT=9850`.
- **All**: HTTP is the primary integration surface. Use `--http-port`
  for explicit port binding in compositions.
