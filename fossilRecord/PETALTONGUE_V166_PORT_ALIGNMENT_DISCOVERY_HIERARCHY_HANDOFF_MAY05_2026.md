# petalTongue v1.6.6 — Port Alignment + Discovery Escalation Hierarchy

**Date**: May 5, 2026
**Version**: 1.6.6
**Primal**: petalTongue
**Triggered by**: primalSpring downstream audit (port conflict + cross-cutting discovery)

---

## Summary

Two items from primalSpring audit addressed:
1. **TCP port 9600→9900 alignment** — ecosystem-assigned fallback port constant added
2. **Discovery Escalation Hierarchy** — 5-tier docs aligned with primalSpring standard

## 1. Port Alignment (LOW)

### Problem
primalSpring moved petalTongue's TCP fallback port from 9600 to 9900 to avoid
conflict with rhizoCrypt's tarpc port (9600) on ironGate. petalTongue had no
local constant for its ecosystem-assigned TCP port.

### Fix
- Added `ECOSYSTEM_TCP_FALLBACK_PORT: u16 = 9900` to `constants/network.rs`
- Added 9900 to `DEFAULT_DISCOVERY_PORTS` for Tier-5 TCP probing
- Port overridable via `PETALTONGUE_TCP_PORT` env var
- Documented the 9600→9900 history in the constant's doc comment

### Ecosystem Port Map (reference)
| Primal | tarpc | JSON-RPC | Notes |
|--------|-------|----------|-------|
| rhizoCrypt | 9600 | 9601 | Unchanged |
| petalTongue | — | 9900 | Moved from 9600 |
| BearDog | — | 9100 | Moved from 9900 |

## 2. Discovery Escalation Hierarchy (cross-cutting)

### Tier Mapping

| Tier | primalSpring Standard | petalTongue Implementation |
|------|----------------------|---------------------------|
| 1 | Songbird `ipc.resolve` | **Not yet implemented** — backlog item |
| 2 | biomeOS Neural API (`capability.discover`) | `NeuralApiProvider` (uses `primal.list`) |
| 3 | UDS filesystem (`primal-family.sock`) | `DiscoveryServiceProvider`, `UnixSocketProvider` |
| 4 | Socket registry / manifests | `DiscoveryServiceProvider` + `discovery.query` |
| 5 | TCP probing (well-known ports) | `default_discovery_ports()` incl. 9900 |

### Changes
- `crates/petal-tongue-discovery/src/lib.rs` module docs rewritten to document
  the 5-tier hierarchy with each tier mapped to its implementation module
- mDNS documented as a parallel lane (not a numbered tier)
- Tier 1 (Songbird `ipc.resolve`) noted as future evolution path

### Future Work
- **Tier 1 wire-up**: When Songbird exposes `ipc.resolve`, add it as Priority 0
  in `discover_visualization_providers`
- **`capability.discover` alignment**: Current Neural API path uses `primal.list`;
  consider adding `capability.discover` as an alias or preferred method
- **Phase 3 self-hosted sporePrint**: Requires petalTongue + Songbird coordination;
  added to CONTEXT.md backlog

## Verification

```
cargo clippy --workspace --all-features: 0 warnings
cargo doc --workspace --no-deps -D warnings: 0 warnings
cargo test --workspace --all-features: 6,200+ passed, 0 failed
```

---

*Ref: `BEARDOG_V090_WAVE86_PORT_ALIGNMENT_DISCOVERY_HIERARCHY_HANDOFF_MAY05_2026.md`*
