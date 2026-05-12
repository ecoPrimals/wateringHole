# rhizoCrypt v0.14.0-dev — Session 28 Handoff

**Date**: April 8, 2026
**Session**: 28
**Focus**: reqwest elimination (banned dep), docs cleanup, showcase debris audit

---

## Summary

Removed `reqwest` entirely from rhizoCrypt — all HTTP clients now use pure Rust
`hyper-util`/`http-body-util` stack via a new `EcoHttpClient` wrapper. Updated
root docs, CHANGELOG, deployment checklist, and crate READMEs with correct metrics.
Audited showcase scripts for stale references and dead paths.

---

## Changes

### 1. reqwest Elimination — ecoBin Full Compliance

- **EcoHttpClient**: New lightweight HTTP client in `clients/adapters/http.rs` built on `hyper_util::client::legacy::Client` — provides `post_json()`, `get()`, `validate_url()` with configurable timeout
- **5 clients migrated**: BearDog (signing), NestGate (storage), ToadStool (BYOB compute), LoamSpine (permanent storage JSON-RPC), HttpAdapter (generic capability REST)
- **Error types evolved**: `reqwest::Error` source variants replaced with `String` transport errors — no more `reqwest` type in any public API
- **deny.toml**: Added `reqwest` + `ring` to banned crate list (18 total banned)
- **Cargo.toml**: `http-clients` feature now activates `hyper`, `hyper-util`, `http-body-util`; `hyper-util` added to workspace deps
- **NestGate `exists()`**: HEAD → GET (hyper client simplification, functionally equivalent)

### 2. Documentation Refresh

- **README.md**: `.rs` count 130 → 135, domain count, ecoBin note, audit crate count
- **CONTEXT.md**: Method count 27 → 28, file count 130 → 135, registry line
- **DEPLOYMENT_CHECKLIST.md**: Session 26 → 28, file count, date
- **crate README**: `http-clients` feature description updated
- **CHANGELOG.md**: Full session 28 entry

### 3. Showcase Debris Audit (findings, not yet fixed)

Identified stale showcase references:
- NestGate scripts reference non-existent `demo-real-retrieval.sh`, `demo-real-content-addressed.sh`
- Squirrel AI scripts reference non-existent `demo-pattern-recognition.sh`, `demo-adaptive-workflows.sh`
- `demo-query-dag.sh` has wrong relative path for next step
- Songbird `start-songbird.sh` help text says `songbird-rendezvous` but binary is `songbird-cli`

---

## Quality Gates

- `cargo fmt` — clean
- `cargo clippy --workspace --all-features` — 0 warnings
- `cargo test --workspace --all-features` — **1,425 tests**, 0 failures
- Zero `reqwest` in `.rs` source files (only in CHANGELOG historical reference)
- Zero `unsafe` blocks
- SPDX headers on all **135** `.rs` files

---

## Ecosystem Impact

- **ecoBin**: Full compliance — no reqwest, no ring in application dependency tree
- **Capability Wire Standard**: Still Level 3 (unchanged from session 27)
- **HTTP clients remain feature-gated**: Default build has zero HTTP client deps
- **API surface**: Unchanged — all primal-specific client methods have identical signatures

---

## Next Steps

- Fix showcase script dead references (non-blocking — demos are progressive)
- Consider adding HTTPS support via `rustls` + `hyper-rustls` (pure Rust TLS) when inter-primal HTTPS is needed
- Registry alignment: 4 methods in handler not in `capability_registry.toml` (health.liveness, health.readiness, tools.list, tools.call)
