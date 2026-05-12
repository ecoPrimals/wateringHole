# biomeOS v3.29 — primalSpring Phase 55 Audit Response

**Date**: April 28, 2026
**Origin**: primalSpring v0.9.20 Phase 55 Audit
**Scope**: Graph signing, schema alignment gap closure, NUCLEUS evolution architecture

---

## Summary

Three items from the primalSpring Phase 55 audit addressed:

1. **Graph signing infrastructure** — BLAKE3 content hash + Ed25519 signature
   on `GraphMetadata`. `biomeos-graph::integrity` module for verification.
   `GraphLoader` enforces signature requirements by genetics tier. `graph.verify`
   JSON-RPC method. `biomeos graph sign/verify` CLI commands.

2. **Schema alignment gap closure** — `[graph.environment]` accepted as alias.
   Per-node `capabilities = [...]` arrays merged into `GraphNode.capabilities`.
   `graph.id` optional with filename derivation. `GraphId::unset()` sentinel.

3. **NUCLEUS evolution spec** — `coordination_pubkey` cached in `NeuralApiServer`
   from BearDog `crypto.derive_public_key`. Design spec at
   `specs/BIOMEOS_NUCLEUS_EVOLUTION.md` documenting 3-phase roadmap.

## Files Changed

### New files
- `crates/biomeos-graph/src/integrity.rs` — content hash + signature verification
- `crates/biomeos/src/modes/graph_ops.rs` — `biomeos graph sign/verify` CLI
- `specs/BIOMEOS_NUCLEUS_EVOLUTION.md` — architecture evolution roadmap

### Modified files
- `crates/biomeos-graph/src/graph.rs` — `GraphMetadata` signing fields, `GraphId::unset()`
- `crates/biomeos-graph/src/error.rs` — `Integrity` error variant
- `crates/biomeos-graph/src/lib.rs` — `integrity` module export
- `crates/biomeos-graph/src/loader.rs` — integrity verification in load path
- `crates/biomeos-graph/Cargo.toml` — `blake3`, `ed25519-dalek` deps
- `crates/biomeos-atomic-deploy/src/neural_graph.rs` — env alias, capabilities array, integrity log
- `crates/biomeos-atomic-deploy/src/neural_api_server/mod.rs` — `coordination_pubkey` field
- `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` — `GraphVerify` route
- `crates/biomeos-atomic-deploy/src/neural_api_server/server_lifecycle.rs` — key derivation call
- `crates/biomeos-atomic-deploy/src/neural_api_server/discovery_init.rs` — `derive_coordination_key()`
- `crates/biomeos-atomic-deploy/src/handlers/graph/mod.rs` — `verify_graph()` method
- `crates/biomeos/src/main.rs` — `Graph` subcommand, `--skip-signature-check`
- `crates/biomeos/src/modes/mod.rs` — `graph_ops` module
- `CHANGELOG.md`, `CURRENT_STATUS.md`, `README.md`, `START_HERE.md`

## Verification

- `cargo check --workspace`: PASS
- `cargo clippy --workspace -- -D warnings`: PASS (0 warnings)
- `cargo fmt --check`: PASS
- `cargo test --workspace`: 7,814+ tests (1 pre-existing env-dependent failure)
- `cargo test -p biomeos-graph`: 267 tests PASS (includes new integrity tests)
- `cargo test -p biomeos-unibin`: 472 tests PASS

## Impact on Downstream

### primalSpring
- Cell graphs without `graph.id` now load through biomeOS's `GraphLoader` path
  (ID derived from filename). `[graph.environment]` accepted as alias.
- `graph.verify` method available for integrity auditing.
- Per-node `capabilities` arrays preserved during conversion.

### petalTongue / UI
- `graph.verify` returns structured JSON integrity reports.

### BearDog
- biomeOS calls `crypto.derive_public_key` with `purpose = "coordination"` at
  startup. BearDog needs to support this RPC (or biomeOS degrades gracefully).
- `crypto.sign` used by `biomeos graph sign` CLI for offline graph signing.

### All primals
- Graphs with `genetics_tier = "mito_beacon"` or `"nuclear"` require valid
  signatures. Unsigned graphs are rejected at these tiers.
