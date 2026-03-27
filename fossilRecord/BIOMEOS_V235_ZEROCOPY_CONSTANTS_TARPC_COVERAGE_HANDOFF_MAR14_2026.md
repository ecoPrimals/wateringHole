# biomeOS V2.35 — Zero-Copy + Primal Constants + tarpc Wiring + Coverage Push

**Date**: March 14, 2026
**Version**: 2.35
**Previous**: V2.34 (Deep Debt Evolution + ecoBin v3.0 Compliance)
**Status**: PRODUCTION READY

---

## Summary

Continued deep debt evolution across 5 phases:

1. **Zero-copy binary payloads** — `bytes::Bytes` replaces `Vec<u8>` in tarpc types with base64 serde helpers for JSON wire compatibility
2. **Centralized primal name constants** — new `primal_names` module eliminates all hardcoded primal strings across 15 files in 8 crates
3. **tarpc transport helpers** — Unix socket preparation, naming conventions, protocol escalation documentation
4. **Major test expansion** — +183 new tests (4,275 total), covering capability taxonomy, subfederation, beacon, service types, error types
5. **Code compliance** — test extraction from 6 large files, 0 clippy warnings, 0 files >1000 LOC

---

## Changes

### Zero-Copy Evolution

| File | Change |
|------|--------|
| `biomeos-types/src/tarpc_types.rs` | `SignatureResult.signature`: `Option<Vec<u8>>` → `Option<Bytes>` |
| `biomeos-types/src/tarpc_types.rs` | New `bytes_serde` and `option_bytes_serde` modules for base64 JSON serialization |
| `biomeos-types/Cargo.toml` | Added `bytes = "1.0"`, `base64 = "0.21"` |
| `Cargo.toml` (workspace) | Added `bytes = "1.0"` to workspace deps |

### Centralized Primal Constants

| File | Change |
|------|--------|
| `biomeos-types/src/primal_names.rs` | **NEW** — `BEARDOG`, `SONGBIRD`, `TOADSTOOL`, `NESTGATE`, `SQUIRREL`, `LOAMSPINE`, `RHIZOCRYPT`, `SWEETGRASS` constants; `CORE_PRIMALS`, `PROVENANCE_PRIMALS` slices; `is_known_primal()` |
| `biomeos-types/src/capability_taxonomy/definition.rs` | `known_primals()` → delegates to `primal_names::CORE_PRIMALS` |
| `biomeos/src/modes/nucleus.rs` | All primal string literals → imported constants |
| `biomeos/src/modes/enroll.rs` | `"beardog"` → `BEARDOG` constant |
| `biomeos/src/modes/doctor/checks_primal.rs` | Hardcoded array → `CORE_PRIMALS` |
| `biomeos/src/modes/cli.rs` | `name.contains("primal")` → `CORE_PRIMALS.iter().any()` |
| `biomeos/src/modes/verify_lineage.rs` | Fallback string → `BEARDOG` constant |
| `biomeos-atomic-deploy/src/capability_domains.rs` | Provider fields → constants |
| `biomeos-federation/src/subfederation/beardog.rs` | Fallback → `BEARDOG` constant |
| `biomeos-core/src/plasmodium/mod.rs` | Discovery loop → `CORE_PRIMALS` |
| `biomeos-primal-sdk/src/discovery.rs` | Match arms → constants |
| `biomeos-core/src/model_cache/cache.rs` | Default → `NESTGATE` constant |
| `biomeos-graph/src/ai_advisor.rs` | AI provider → `SQUIRREL` constant |
| `biomeos-ui/src/primal_client.rs` | Fallbacks → constants |
| `biomeos-cli/src/commands/niche.rs` | Icon match → constants |

### tarpc Transport Wiring

| File | Change |
|------|--------|
| `Cargo.toml` (workspace) | `tarpc` features: added `"unix"` |
| `biomeos-primal-sdk/src/tarpc_transport.rs` | **NEW** — `prepare_socket()`, `tarpc_socket_name()`, `tarpc_socket_path()` |
| `biomeos-primal-sdk/Cargo.toml` | Added `tarpc`, `tracing` workspace deps; `tempfile` dev-dep |

### Test Expansion (+183 tests)

| Module | Tests Added | Focus |
|--------|-------------|-------|
| `capability_taxonomy/definition` | 35 | resolve, ambiguity, fallback, strict discovery, all-primals |
| `subfederation/manager` | 20 | registration, routing, health scoring, statistics |
| `dark_forest/beacon` | 22 | ECDH exchange, renewal, lineage verification, expiry |
| `service/core` | 27 | serde roundtrips, method equality, defaults, error codes |
| `service/security` | 20 | JWT, signing, trust level transitions, key operations |
| `manifest/networking_services` | 22 | relay config, STUN, mesh routing, NAT traversal |
| `tarpc_transport` | 7 | naming conventions, socket prep, path conversion |

### Test Extraction (1000-line compliance)

| Source File | Lines Before | Lines After | Extracted To |
|-------------|-------------|-------------|--------------|
| `biomeos/src/modes/nucleus.rs` | 1285 | 628 | `nucleus_tests.rs` |
| `biomeos-types/src/capability_taxonomy/definition.rs` | 1203 | 680 | `definition_tests.rs` |
| `biomeos-spore/src/dark_forest/beacon.rs` | 1065 | 572 | `beacon_tests.rs` |
| `biomeos-types/src/service/core.rs` | 1148 | 794 | `core_tests.rs` |
| `biomeos-types/src/service/security.rs` | 987 | 610 | `security_tests.rs` |
| `biomeos-types/src/manifest/networking_services.rs` | 1120 | 812 | `networking_services_tests.rs` |

---

## Metrics

| Metric | V2.34 | V2.35 |
|--------|-------|-------|
| Tests | 4,092 | 4,275 |
| Failures | 0 | 0 |
| Clippy warnings | 0 | 0 |
| Files >1000 LOC | 0 | 0 |
| Unsafe code | 0 | 0 |
| Hardcoded primals | scattered | 0 (centralized) |
| Zero-copy payloads | partial | `bytes::Bytes` + base64 serde |
| tarpc transport | JSON-RPC only | + Unix socket helpers |

---

## ecoBin Compliance

- **ecoBin v3.0**: COMPLIANT — pure Rust, zero -sys crates, zero C dependencies
- **Zero-copy**: `bytes::Bytes` for binary payloads, `Arc<str>` for identifiers
- **Primal discovery**: Capability-based at runtime, no hardcoded primal knowledge
- **tarpc**: Binary protocol escalation ready for performance-critical paths
- **XDG**: All paths via centralized `SystemPaths`
- **License**: AGPL-3.0-only

---

## Inter-Primal Notes

The `primal_names` module defines constants for all 8 known primals. Other primals in the ecosystem (springs, petalTongue, etc.) are discovered at runtime via capability taxonomy — biomeOS does not hardcode knowledge of their existence.

The tarpc transport helpers (`tarpc_transport.rs`) establish naming conventions:
- JSON-RPC: `{primal}-{family_id}.sock`
- tarpc: `{primal}-{family_id}.tarpc.sock`

Primals can implement both protocols. biomeOS will escalate from JSON-RPC to tarpc when a `.tarpc.sock` file is discovered, enabling zero-overhead binary IPC for hot paths.

---

## Next Steps

1. **Coverage to 90%** — integration test infrastructure for CLI handlers, neural API server, boot modules
2. **ARM64 biomeOS genomeBin** — blocks Pixel deployment
3. **tarpc service trait** — define `BiomePrimalService` trait for primals to implement
4. **Protocol escalation runtime** — automatic JSON-RPC → tarpc upgrade when `.tarpc.sock` exists
