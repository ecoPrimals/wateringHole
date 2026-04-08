<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Deep Debt Sprint 2: Module Refactor & Doc Cleanup

**Date**: April 8, 2026  
**From**: loamSpine team  
**To**: primalSpring (coordinator), biomeOS team, downstream springs

---

## Summary

Second deep debt sprint for loamSpine v0.9.16. Three areas addressed:

1. **Smart module refactoring** — two largest production files split into focused submodules
2. **mDNS service discovery evolved** — stub → real implementation
3. **Root doc cleanup** — stale metrics, deprecated references, new methods documented

---

## Changes

### Smart Refactor: `jsonrpc/mod.rs` (773 → 3 modules)

| Module | Lines | Responsibility |
|--------|------:|---------------|
| `wire.rs` | 82 | JSON-RPC 2.0 wire types and error codes |
| `server.rs` | 428 | TCP and UDS transport infrastructure |
| `mod.rs` | 285 | Dispatch logic, method normalization, re-exports |

All public API surface unchanged. Tests reference submodules via `pub(crate)` re-exports.

### Smart Refactor: `capabilities.rs` (587 → 4-file directory)

| Module | Lines | Responsibility |
|--------|------:|---------------|
| `mod.rs` | 107 | Identifier constants (`loamspine::*`, `external::*`), re-exports |
| `types.rs` | 235 | `LoamSpineCapability`, `ExternalCapability`, `DiscoveredService`, `ServiceHealth` |
| `parser.rs` | 129 | `extract_capabilities()` — partner response parser (4 wire formats) |
| `tests.rs` | 116 | Unit tests |

### mDNS Service Discovery Evolved

`service/infant_discovery.rs:try_mdns_discovery()` evolved from synchronous stub (always returned `None` even with `mdns` feature enabled) to async implementation:
- Uses `tokio::task::spawn_blocking` + `mdns::discover::all`
- Queries `_discovery._tcp.local` on LAN
- Parses SRV records for endpoint resolution
- Feature-gated under `mdns`

### Root Doc Updates

- **README.md**: Test count 1,280 → 1,304. Source files 136 → 152. Architecture tree updated for new `capabilities/` and `neural_api/` directories. RPC table expanded with `health.liveness`, `health.readiness`, `capabilities.list`, `identity.get`, `tools.list`, `tools.call`.
- **CONTEXT.md**: Test count and source files updated. Methods list updated.
- **KNOWN_ISSUES.md**: Date updated.
- **WHATS_NEXT.md**: Date updated, new sprint section added.
- **CHANGELOG.md**: Refactoring section updated to reflect 8 large files refactored. Source files count corrected to 152.
- **STATUS.md**: Source files, max file, `#[allow]` count updated.

### Stale Reference Cleanup

- `discovery/manifest.rs`: "Songbird" → "mDNS or DNS SRV" (discovery fallback context)
- `config.rs`: Service registry list header generalized to "mDNS / DNS SRV" (Songbird kept as registry implementation reference)
- `CONTEXT.md`, `README.md`: References verified for correctness (Songbird = Tower Atomic TLS/HTTP primal, nestGate = Nest Atomic)

---

## Verification

```
cargo clippy --all-targets    → 0 warnings
cargo test                    → 1,304 passed, 0 failed
Source files                  → 152 .rs files
```

---

## What's NOT Changed

- All public API surfaces remain identical
- No wire format changes
- No dependency additions or removals
- Test count unchanged (structural refactoring only)
- Songbird references in transport docs preserved (legitimate Tower Atomic primal)
- `commit.session` alias preserved (backward-compatible normalization)
