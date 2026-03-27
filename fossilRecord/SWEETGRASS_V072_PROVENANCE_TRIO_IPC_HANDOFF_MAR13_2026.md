# SweetGrass v0.7.2 — Provenance Trio Coordination + biomeOS IPC Handoff

**Date**: March 13, 2026
**From**: SweetGrass (v0.7.2)
**To**: rhizoCrypt, biomeOS, LoamSpine, ludoSpring, wetSpring teams
**License**: AGPL-3.0-only

---

## Summary

SweetGrass v0.7.2 completes the **Provenance Trio coordination layer** — the
concrete IPC wiring that connects rhizoCrypt dehydration → sweetGrass attribution
→ LoamSpine permanence. It also adds Unix domain socket transport for biomeOS
and enforces the Tower Atomic pattern via `cargo deny`.

### New JSON-RPC 2.0 Methods

| Method | Purpose |
|--------|---------|
| `braid.commit` | Package a Braid for LoamSpine anchoring (BraidId → UUID, ContentHash → `[u8; 32]`) |
| `contribution.recordDehydration` | Accept a `DehydrationSummary` from rhizoCrypt and create provenance Braids |

### Previous Methods (v0.7.0)

| Method | Purpose |
|--------|---------|
| `contribution.record` | Record a single contribution from any primal |
| `contribution.recordSession` | Record a batch of contributions from a session |

---

## For rhizoCrypt Team

### DehydrationSummary Contract

SweetGrass now accepts a shared `DehydrationSummary` type. When rhizoCrypt
dehydrates a session, send this via `contribution.recordDehydration`:

```json
{
  "jsonrpc": "2.0",
  "method": "contribution.recordDehydration",
  "params": {
    "summary": {
      "source_primal": "rhizoCrypt",
      "session_id": "rhizo-session-uuid",
      "merkle_root": "sha256:abc123...",
      "vertex_count": 47,
      "branch_count": 3,
      "agents": ["did:key:z6MkAlice", "did:key:z6MkBob"],
      "attestations": [
        {
          "agent": "did:key:z6MkAlice",
          "signature": "base64-sig",
          "timestamp": 1710000000
        }
      ],
      "operations": [
        {
          "op_type": "merge",
          "vertex_id": "v-uuid",
          "agent": "did:key:z6MkAlice",
          "timestamp": 1710000000
        }
      ],
      "session_start": 1710000000,
      "dehydrated_at": 1710003600,
      "frontier": ["vertex-a", "vertex-b"],
      "niche": "rootpulse",
      "compression_ratio": 0.73
    }
  },
  "id": 1
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "braids_created": 2,
    "braid_ids": ["urn:braid:uuid:...", "urn:braid:uuid:..."]
  },
  "id": 1
}
```

### Key Change: `source_primal` Field

The `source_primal` field in `DehydrationSummary` replaces any hardcoded primal
name. SweetGrass reads this at runtime — no embedded knowledge of rhizoCrypt.

---

## For LoamSpine Team

### braid.commit Method

SweetGrass can now package Braids for LoamSpine anchoring:

```json
{
  "jsonrpc": "2.0",
  "method": "braid.commit",
  "params": {
    "braid_id": "urn:braid:uuid:550e8400-e29b-41d4-a716-446655440000"
  },
  "id": 1
}
```

### Type Translation

SweetGrass performs the type translations LoamSpine expects:

| SweetGrass Type | LoamSpine Type | Method |
|-----------------|----------------|--------|
| `BraidId` (`urn:braid:uuid:{uuid}`) | `Uuid` | `BraidId::extract_uuid()` |
| `ContentHash` (`sha256:hex...`) | `[u8; 32]` | `ContentHash::to_bytes32()` |

These are implemented in `sweet-grass-core` and available to any consumer.

---

## For biomeOS Team

### Unix Domain Socket Transport

SweetGrass now listens on a UDS for biomeOS IPC alongside HTTP and tarpc:

- **Path resolution**: XDG-compliant (`$XDG_RUNTIME_DIR/sweetGrass/sweetGrass.sock`)
- **Protocol**: Newline-delimited JSON-RPC 2.0
- **Cleanup**: Socket file removed on graceful shutdown

### Updated Neural API Translations

| Capability | Method | Provider |
|-----------|--------|----------|
| `attribution.record` | `contribution.record` | sweetGrass |
| `attribution.recordSession` | `contribution.recordSession` | sweetGrass |
| `attribution.recordDehydration` | `contribution.recordDehydration` | sweetGrass |
| `provenance.commit` | `braid.commit` | sweetGrass |

### Updated RootPulse Commit Graph

```
rhizoCrypt.dehydrate → sweetGrass.recordDehydration → sweetGrass.commit → loamspine.commit
```

### Niche Manifest

```yaml
sweetGrass:
  version: ">=0.7.2"
  capabilities:
    - semantic-attribution
    - braiding
    - contribution-tracking
    - session-recording
    - dehydration-import
    - braid-commit
```

---

## Tower Atomic Enforcement

SweetGrass v0.7.2 enforces the Tower Atomic pattern via `cargo deny`:

- `ring`, `rustls`, `openssl`, `native-tls` are **banned** in production
- Dev-only exemptions for `testcontainers` subtree via `wrappers`
- HTTP is handled through biomeOS Songbird (pure Rust TLS via rustls at the biomeOS layer, not within sweetGrass)

---

## Shared Hash Utilities

New centralized `sweet_grass_core::hash` module:

| Function | Purpose |
|----------|---------|
| `hex_encode(bytes)` | Encode bytes to hex string |
| `hex_decode(hex)` | Decode hex string to bytes (returns `Option`) |
| `hex_decode_strict(hex)` | Decode hex string to bytes (returns `Result`) |
| `sha256(data)` | Compute SHA-256 and return hex-encoded digest |

These replace 3 duplicate implementations across the codebase.

---

## SweetGrass v0.7.2 Metrics

| Metric | Value |
|--------|-------|
| Version | 0.7.2 |
| Tests | 570 passing |
| Crates | 9 |
| Protocols | JSON-RPC 2.0 + tarpc + REST + UDS |
| License | AGPL-3.0-only |
| ecoBin | Compliant (zero C deps in production) |
| UniBin | `sweet-grass-service server`, `sweet-grass-service status` |
| Zero-copy | BraidId, Did, ContentHash use Arc\<str\> |
| Tower Atomic | cargo deny enforced (ring/rustls/openssl banned) |

---

## Supersedes

Updates and extends `SWEETGRASS_V070_CONTRIBUTION_API_HANDOFF_MAR12_2026.md`.
All v0.7.0 methods remain valid. v0.7.2 adds trio coordination, UDS transport,
and Tower Atomic enforcement.
