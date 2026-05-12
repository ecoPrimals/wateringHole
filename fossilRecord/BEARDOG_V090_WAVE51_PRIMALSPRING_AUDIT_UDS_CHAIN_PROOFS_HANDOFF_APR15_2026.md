<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 51: primalSpring Audit Resolution Handoff

**Date**: April 15, 2026

## Summary

Resolved 5 of 5 remaining items from the primalSpring April 16 review audit. UDS first-byte peek, genetic RPC chain proofs, bond persistence trait, HSM dispatch path, and async-trait migration. Additionally eliminated `ring` transitive dependency, evolved `Box<dyn Error>` to typed errors, and centralized hardcoded addresses.

## Changes

### 1. UDS First-Byte Peek (Composition Priority #1)

| Component | Change |
|-----------|--------|
| `platform/mod.rs` | New `PrefixedStream` struct — wraps `PlatformStream` + prepends consumed byte for `AsyncRead`/`AsyncWrite` |
| `unix_socket_ipc/server.rs` | Production UDS peek: 5s timeout, `0x7B` → JSON-RPC bypass, else → BTSP handshake |

BearDog now matches all other BTSP-enforcing primals (NestGate, Songbird, coralReef, petalTongue) for UDS protocol auto-detection.

### 2. Genetic RPC → Full Chain Proofs

| Component | Change |
|-----------|--------|
| `crypto_handlers_genetic_types.rs` | Extended request/response: `chain_id`, `node_id`, `generation`, `head_commitment`, `mode` |
| `crypto_handler/router.rs` | Threads `btsp_provider` to genetic handler |
| `crypto_handler/genetic.rs` | Retrieves `BirdSongManager` from provider for chain-aware dispatch |
| `crypto_handlers_genetic/lineage.rs` | Chain mode: `LineageProofManager.generate_lineage_proof()` / `verify_lineage_proof()`; simple mode: Blake3 fallback |

### 3. Bond Persistence

| Component | Change |
|-----------|--------|
| `ionic_bond/persistence.rs` | New `BondPersistence` trait + `InMemoryBondPersistence` default |
| `ionic_bond/mod.rs` | `IonicBondHandler` holds `Arc<dyn BondPersistence>`; `with_persistence()` constructor |
| `ionic_bond/lifecycle.rs` | `handle_seal` → store, `handle_list` → merge persistence + in-memory, `handle_revoke` → remove |

Ready for runtime wiring to loamSpine `bonding.ledger.store/retrieve/list` via capability discovery.

### 4. HSM/Titan M2 Dispatch

| Component | Change |
|-----------|--------|
| `crypto/asymmetric.rs` | `handle_generate_keypair_with_hsm`: routes by `hsm_backend` param with availability signaling |
| `crypto_handler/aliases_and_beardog.rs` | `crypto.generate_keypair` checks for `hsm_backend` in params |

### 5. Dependency Evolution

| Item | Change |
|------|--------|
| `ring` eliminated | `beardog-discovery` aligned to `hickory-resolver 0.24` (ring-free); DNS-SD adapted to 0.24 API |
| `Box<dyn Error>` evolved | `SafeOps::safe_execute` generic bound; doctests in security/client use typed errors |
| Hardcoded addresses | 9 production files centralized to `WILDCARD_IPV4`/`DEFAULT_EXTERNAL_HOST`/`LOCALHOST_NAME` |
| `async-trait` | `SecureTunnelProvider` migrated to native async fn (~50 → 49 instances) |

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | Clean |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Clean |
| `cargo test --workspace` | 14,785 pass, 0 fail |
| `cargo tree -i ring` | No matches (eliminated) |

## Net Impact

- **30 files changed, +593 / −299 lines**
- 1 new file (`ionic_bond/persistence.rs`)
- `ring` + `cc` removed from dependency graph
- All 5 primalSpring audit items resolved

## Remaining Cross-Primal

| Item | Status |
|------|--------|
| Bond persistence wiring | Trait ready; needs runtime discovery of `bonding.ledger.*` from loamSpine/NestGate |
| HSM hardware backends | Dispatch path ready; `strongbox`/`titan_m2` return availability errors until hardware wiring |
| async-trait: 49 remaining | All behind `dyn Trait` objects; requires RPITIT stabilization for full elimination |
