<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — Deep Debt Reduction, Idiomatic Rust Evolution

**Date**: March 15, 2026 (session 6)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Deep debt reduction + modern idiomatic Rust + sovereignty hardening
**Supersedes**: `RHIZOCRYPT_V013_PEDANTIC_CLIPPY_UNIBIN_SIGNALS_HANDOFF_MAR14_2026.md`

---

## Summary

Comprehensive codebase audit against specs/, wateringHole standards, and
ecoPrimals governance. Executed on all findings: evolved adapter APIs to
borrow-first, eliminated `Box<dyn Error>`, centralized remaining magic
numbers, removed cloud vendor references from docs, extracted doctor module,
and added provenance trio wire types. All quality gates green.

1. **907 tests passing** (default features) — 0 failures, 0 ignored.

2. **0 clippy warnings** (pedantic + nursery + cargo, all features) —
   including new `redundant_clone` fixes.

3. **`ProtocolAdapter` trait evolved** — `call_json` and `call_oneway_json`
   now accept `&str` instead of `String`, borrowing at the trait boundary
   and allocating only where transport requires ownership (tarpc spawn,
   reqwest body).

4. **`Box<dyn Error>` eliminated** — `ServiceError::Storage` variant added;
   `check_redb_storage` returns typed error.

5. **JSON-RPC error logging** — `serialize_response()` helper logs
   serialization failures before fallback, replacing 7 silent
   `unwrap_or_default()` calls.

6. **Doctor module extracted** — `doctor.rs` (197 lines) from `lib.rs`
   (809 → 624 lines). Clean separation of diagnostic logic.

7. **Sovereignty hardened** — Cloud vendor names removed from all doc
   comments. Capability-agnostic language throughout.

8. **Provenance trio types** — `provenance-trio-types` workspace dep for
   canonical wire format between rhizoCrypt and sweetGrass.

---

## Changes

### Adapter API Evolution (`String` → `&str`)

| File | Change |
|------|--------|
| `adapters/mod.rs` | `ProtocolAdapter::call_json(&str, String)` → `call_json(&str, &str)` |
| `adapters/mod.rs` | `ProtocolAdapter::call_oneway_json(&str, String)` → `call_oneway_json(&str, &str)` |
| `adapters/tarpc.rs` | `.to_owned()` at spawn boundary only |
| `adapters/http.rs` | `.to_owned()` for reqwest body only |
| `adapters/unix_socket.rs` | `from_str()` works naturally with `&str` |
| `integration/mocks.rs` | `MockProtocolAdapter` updated + all test callers |

### Constants Centralized

| Constant | Value | Replaces |
|----------|-------|----------|
| `DEFAULT_GC_INTERVAL` | 120s | Inline `120` in `server.rs` |
| `RATE_LIMIT_CLEANUP_INTERVAL` | 60s | Inline `Duration::from_secs(60)` |
| `RATE_LIMIT_CLEANUP_INTERVAL_DEV` | 300s | Inline `Duration::from_secs(300)` |
| `DehydrationConfig::FULL_ATTESTATION_TIMEOUT_SECS` | 300s | Inline `300` |

### Sovereignty

| File | Before | After |
|------|--------|-------|
| `integration/mod.rs` | "CloudKMS (AWS KMS, GCP KMS, Azure Key Vault)" | "Capability-discovered signing providers" |
| `discovery/resolution.rs` | "could be NestGate, S3, Azure, etc." | "discovered at runtime via capabilities" |

### Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `rhizocrypt-service/src/lib.rs` | 809 lines | 624 lines |
| `rhizocrypt-service/src/doctor.rs` | (new) | 197 lines |

---

## Audit Findings (Addressed)

| Finding | Resolution |
|---------|------------|
| `cargo fmt` failure in `dehydration.rs` | Fixed (chain alignment) |
| Hardcoded `"127.0.0.1:9400"` in clap | References `constants::LOCALHOST:PRODUCTION_RPC_PORT` |
| `Box<dyn Error>` in `check_redb_storage` | `ServiceError::Storage` variant |
| Silent `unwrap_or_default()` in JSON-RPC | `serialize_response()` with `tracing::warn!` |
| Cloud vendor names in docs | Removed, capability-agnostic language |
| Inline magic numbers | Centralized to `constants.rs` |
| `String` params in adapter trait | Evolved to `&str` |
| Redundant clone in test | Removed (last-use consumed directly) |

## Audit Findings (Pre-existing, Not Changed)

| Finding | Status | Notes |
|---------|--------|-------|
| `Cow<'_, str>` for stored types | N/A | Types need owned `String` for `Serialize`/`Send`; builders use `impl Into<String>` |
| Hardcoded ports in tests | Acceptable | Test fixtures register mock endpoints; production uses discovery |
| 5 `cargo-deny` advisory ignores | Upstream | All from tarpc transitive deps (instant, opentelemetry, fxhash, bincode v1) |
| `libc` in transitive deps | Upstream | Via tokio; ecoBin compliance at application level |
| Stale showcase scripts | Deferred | 11 demo `.sh` scripts use deprecated `Session::new` / `SessionType::Ephemeral` |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Clean (0 warnings) |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace` | 907 pass, 0 fail |
| `#![forbid(unsafe_code)]` | All 4 crate entry points |
| SPDX headers | All 104 `.rs` files |
| Max file size | All under 1000 lines (max 858) |
| Zero `todo!()` / `unimplemented!()` / `TODO` / `FIXME` in source | Verified |
| `cargo-deny` | advisories ok, bans ok, licenses ok, sources ok |

---

## Files Modified

```
crates/rhizo-crypt-core/src/clients/adapters/mod.rs
crates/rhizo-crypt-core/src/clients/adapters/tarpc.rs
crates/rhizo-crypt-core/src/clients/adapters/http.rs
crates/rhizo-crypt-core/src/clients/adapters/unix_socket.rs
crates/rhizo-crypt-core/src/constants.rs
crates/rhizo-crypt-core/src/dehydration.rs
crates/rhizo-crypt-core/src/discovery/resolution.rs
crates/rhizo-crypt-core/src/integration/mocks.rs
crates/rhizo-crypt-core/src/integration/mod.rs
crates/rhizo-crypt-core/src/types_ecosystem/provenance/client.rs
crates/rhizo-crypt-rpc/src/jsonrpc/mod.rs
crates/rhizo-crypt-rpc/src/rate_limit.rs
crates/rhizocrypt-service/src/doctor.rs (new)
crates/rhizocrypt-service/src/lib.rs
crates/rhizocrypt-service/src/main.rs
Cargo.toml
Cargo.lock
README.md
CHANGELOG.md
```

---

## Next Steps

1. Run `cargo llvm-cov` to verify coverage target after refactoring
2. Update 11 stale showcase scripts from `Session::new` → `SessionBuilder`
3. Update `specs/00_SPECIFICATIONS_INDEX.md` reading order to V2 integration spec
4. Monitor tarpc upstream for advisory resolution (5 transitive ignores)
5. Evaluate `SmallVec` for store key allocation to reduce heap pressure
6. Add vertex-to-session index for O(1) `verify_proof` lookup
