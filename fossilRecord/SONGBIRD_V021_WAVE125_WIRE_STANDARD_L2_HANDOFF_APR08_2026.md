# Songbird v0.2.1 — Wave 125: Capability Wire Standard Level 2

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 125  
**Status**: Complete — Wire Standard Level 2 compliant  
**Reference**: `CAPABILITY_WIRE_STANDARD.md` v1.0

---

## Changes

### `capabilities.list` — Wire Standard Envelope (Level 2 MUST)

Previously returned a bare JSON array of 14 NEST capability tokens:

```json
["network.discovery", "network.federation", ...]
```

Now returns the Wire Standard Level 2 envelope:

```json
{
  "primal": "songbird",
  "version": "0.2.1",
  "methods": [
    "health.liveness", "health.readiness", "health.check",
    "capabilities.list", "capabilities.methods",
    "identity", "identity.get",
    "primal.info", "primal.capabilities",
    "rpc.methods", "rpc.discover", "discover_capabilities",
    "ipc.register", "ipc.resolve", "ipc.discover", "ipc.list",
    "http.request", "http.get", "http.post",
    "stun.serve", "stun.stop", "stun.status", "stun.get_public_address",
    "stun.bind", "stun.probe_port_pattern", "stun.detect_nat_type",
    "igd.discover", "igd.map_port", "igd.unmap_port", "igd.status",
    "igd.external_ip", "igd.auto_configure",
    "relay.serve", "relay.stop", "relay.status", "relay.allocate",
    "discovery.peers", "discovery.announce",
    "rendezvous.register", "rendezvous.lookup", "peer.connect",
    "birdsong.generate_encrypted_beacon", "birdsong.decrypt_beacon",
    "birdsong.verify_lineage", "birdsong.get_lineage",
    "birdsong.advertise", "birdsong.schema",
    "mesh.init", "mesh.status", "mesh.find_path", "mesh.announce",
    "mesh.peers", "mesh.topology", "mesh.health_check", "mesh.auto_discover",
    "punch.request", "punch.coordinate", "punch.status",
    "onion.start", "onion.stop", "onion.status", "onion.connect", "onion.address",
    "federation.peers", "federation.status",
    "tor.status", "tor.connect", "tor.service.start", "tor.service.stop",
    "tor.consensus.fetch", "tor.circuit.build", "tor.circuit.close"
  ]
}
```

The `methods` array contains every callable JSON-RPC method from the dispatch table (73 methods). Every entry is callable — no "method not found" for advertised methods.

### `identity.get` — Wire Standard Level 2 (SHOULD)

New JSON-RPC method returning the standard identity envelope:

```json
{
  "primal": "songbird",
  "version": "0.2.1",
  "domain": "network",
  "license": "AGPL-3.0-or-later"
}
```

Added as `IdentityMethod::Get` in the `JsonRpcMethod` typed enum, wired through both the universal-ipc dispatch and the orchestrator HTTP JSON-RPC gateway.

The legacy `identity` method (returns `{primal, version, family_id, capabilities}`) is preserved for backward compatibility.

### Implementation Details

- **`capability_tokens.rs`**: `CALLABLE_METHODS` const lists all 73 dispatch methods. `capabilities_list()` builds the `{primal, version, methods}` envelope using `primal_names::SELF_NAME` and `env!("CARGO_PKG_VERSION")`.
- **`identity_payloads.rs`**: New `identity_get()` function returns Wire Standard response.
- **`domain_methods.rs`**: New `IdentityMethod` enum with `Get` variant.
- **`mod.rs` (json_rpc_method)**: `IdentityGet(IdentityMethod)` variant added, wire string `"identity.get"` mapped.
- **`dispatch.rs`**: New match arm routes `identity.get` to `identity_get()`.
- **`jsonrpc_api/mod.rs`**: Orchestrator gateway handles `identity.get`.

### Wire Standard Compliance

| Level | Requirement | Status |
|-------|-------------|--------|
| L1 | `capabilities.list` responds | ✓ (existed) |
| L1 | Response parseable by biomeOS | ✓ (format A → standard envelope) |
| L1 | `health.liveness` implemented | ✓ (existed) |
| L2 | `{primal, version, methods}` envelope | ✓ **NEW** |
| L2 | `identity.get` implemented | ✓ **NEW** |
| L2 | All methods callable | ✓ (all 73 entries dispatch to handlers) |
| L2 | Semantic `domain.verb` naming | ✓ (2 legacy aliases: `identity`, `discover_capabilities`) |
| L2 | Health triad implemented | ✓ (existed) |
| L3 | `provided_capabilities` grouping | Not yet (future) |
| L3 | `consumed_capabilities` declared | Not yet (future) |

### `capabilities.methods` — Ahead of Standard

Songbird's `capabilities.methods` endpoint (Wave 123) maps NEST capability tokens to callable methods. This is ahead of the Wire Standard — proposed for adoption as an extension.

---

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 12,860 | 12,863 |
| Wire Standard Level | 1 (bare array) | 2 (full envelope + identity.get) |
| Callable methods in envelope | 0 (bare tokens) | 73 (complete dispatch table) |

## Verification

- `cargo check --workspace` — clean
- `cargo clippy --workspace -- -D warnings` — clean
- `cargo fmt --all -- --check` — clean
- `cargo test --workspace` — 12,863 passed, 0 failed, 252 ignored

---

**Next**: Wire Standard Level 3 (`provided_capabilities` grouping, `consumed_capabilities`, `cost_estimates`). Also, propose `capabilities.methods` as Wire Standard extension.
