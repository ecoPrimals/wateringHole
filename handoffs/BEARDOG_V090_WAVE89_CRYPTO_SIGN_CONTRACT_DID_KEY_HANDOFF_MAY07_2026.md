# BearDog v0.9.0 — Wave 89: crypto.sign Contract Fix, did:key Derivation, RP-1/RP-5 Resolution

**Date**: May 7, 2026
**Primal**: BearDog (security)
**Wave**: 89
**Status**: Complete — all CI gates green (clippy 0 warnings, tests passing, fmt clean)
**Triggered by**: primalSpring projectNUCLEUS sovereignty testing audit (May 7, 2026)

---

## Context

primalSpring's projectNUCLEUS audit identified BearDog involvement in two RootPulse gaps:

- **RP-1**: biomeOS `rootpulse_commit.toml` uses `data` as the param for `crypto.sign` — actual param is `message`. The graph also passes `did` which is not a parameter.
- **RP-5**: Entry signing lifecycle unclear — who signs what, how does the orchestrator obtain a DID for the `committer` field?

BearDog's `PRIMAL_CONTRACTS.md` was significantly out of date for `crypto.sign_ed25519`, documenting `data` and `key` (client-supplied private key) as parameters, when the actual implementation uses `message` (base64 bytes) and derives keys internally via BLAKE3 KDF from `key_id` + `purpose`.

---

## Changes

### RP-1: `crypto.sign` Contract Documentation Fix

**`docs/PRIMAL_CONTRACTS.md`** — Complete rewrite of the Ed25519 Signature section:

| Aspect | Before (stale) | After (actual) |
|--------|----------------|----------------|
| Param for data | `data` | `message` (base64) |
| Key material | `key` (client sends private key) | `key_id` + `purpose` (BearDog derives key internally) |
| Response fields | `signature` only | `signature`, `algorithm`, `key_id`, `public_key` |
| Semantic alias | Not documented | `crypto.sign` → `crypto.sign_ed25519` |
| Additional aliases | Not documented | `crypto.ed25519.sign`, `beardog.crypto.sign_ed25519` |
| DID param | Not mentioned | Explicitly documented as NOT a parameter |

Method index updated to include `crypto.sign` and `crypto.did_from_key` with param lists.

### RP-5: `crypto.did_from_key` — New Method (103rd CryptoHandler method)

**New JSON-RPC method**: `crypto.did_from_key`

Derives a W3C `did:key:z6Mk...` identifier from BearDog's Ed25519 signing key. Uses multicodec Ed25519 prefix (`0xed01`) + 32-byte public key, base58btc-encoded.

**Request**: `{ "key_id": "...", "purpose": "..." }` (both optional, same defaults as `crypto.sign`)
**Response**: `{ "did": "did:key:z6Mk...", "public_key": "...", "algorithm": "Ed25519", "key_id": "..." }`

**Cross-primal signing workflow documented**:
1. Orchestrator calls `crypto.did_from_key` → obtains `committer` DID
2. Orchestrator calls `crypto.sign` with entry bytes in `message`
3. Orchestrator passes `signature` + `did` to LoamSpine `entry.append` / `session.commit`

BearDog signs raw bytes and has no knowledge of LoamSpine entry formats. The orchestrator is responsible for serialization.

**Implementation**:
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto/asymmetric.rs` — `handle_did_from_key()` (34 LOC)
- Routed via `aliases_and_beardog.rs`
- Registered in `method_list.rs`
- Re-exported in `crypto/mod.rs`
- 4 tests: basic, deterministic, different-purposes, cross-check-with-public-key

**Dependency**: `bs58 = "0.5"` added to workspace (pure Rust base58 encoding, 0 transitive deps)

### Method Count Update

CryptoHandler: 97 → 98 methods (102 → 103 total with IonicBondHandler's 5)

---

## Ecosystem Impact

### For biomeOS (RP-1 fix)
`rootpulse_commit.toml` Phase 3 should change:
- `crypto.sign` param: `data` → `message` (base64-encoded)
- Remove `did` from `crypto.sign` params (not consumed)
- Add a Phase 0 or early phase: call `crypto.did_from_key` to obtain committer DID

### For LoamSpine (RP-5 clarification)
- BearDog signs raw bytes — it does not know LoamSpine entry format
- The `committer` DID can now be obtained via `crypto.did_from_key`
- LoamSpine should NOT call BearDog internally — the graph orchestrates signing

### For primalSpring capability registry
- New method to register: `crypto.did_from_key` under `beardog` ownership

---

## Remaining Debt (not addressed this wave)

- **`BondPersistence` trait** uses `Result<_, String>` — moderate refactoring effort, deferred
- **10 test files > 800 LOC** — all are test/coverage files, acceptable
- **`sslkeylog.rs`** `export_to_sslkeylogfile` uses `Result<(), String>` — minor, deferred

---

## Validation

| Gate | Result |
|------|--------|
| `cargo check --workspace` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 warnings |
| `cargo test --workspace` | All passing, 0 failures |
| `cargo fmt --check` | Clean |
