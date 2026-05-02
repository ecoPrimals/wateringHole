# sourDough v0.2.0 — Scaffold Evolution Handoff

**Date**: April 30, 2026
**From**: sourDough development session (responding to primalSpring Phase 56c audit)
**Scope**: Full scaffold v0.2.0 evolution — absorbing ecosystem convergence patterns

---

## Context

primalSpring Phase 56c identified that the ecosystem converged significantly in April 2026.
Every NUCLEUS primal now ships with CI workflows, capability wire handlers, first-byte peek,
and socket naming conventions — but sourDough scaffolds were still generating only a core
crate with lifecycle/health traits. This session brings scaffolds to parity with the
ecosystem standard.

## What Changed

### 1. Scaffold Now Generates Server Crate

`sourdough scaffold new-primal {name}` now creates **two** crates:

- `{name}-core/` — Lifecycle, health, error traits (unchanged from v0.1.0)
- `{name}-server/` — **NEW**: JSON-RPC 2.0 server with full capability wire standard

Server crate includes:
- `main.rs` — Clap CLI with `--family-id` arg + `FAMILY_ID` env var
- `server.rs` — UDS listener with first-byte peek (JSON-RPC vs BTSP auto-detection)
- `dispatch.rs` — 4 capability wire handlers + tests:
  - `health.liveness` → `{ "alive": true }`
  - `health.readiness` → `{ "ready": true, "capabilities": [...] }`
  - `health.check` → full diagnostic report
  - `capabilities.list` → `{ "primal": name, "version": semver, "methods": [...] }`

### 2. CI/CD Workflows Generated

Scaffold produces `.github/workflows/`:
- `ci.yml` — lean single-job: checkout → toolchain → cache → fmt → clippy → test
- `notify-plasmidbin.yml` — repository-dispatch to `ecoPrimals/plasmidBin` on push to main

### 3. deny.toml Generated

Every scaffolded primal gets ecoBin v3.0 supply chain auditing:
- 16-crate C-sys ban list (openssl-sys, cc, bindgen, etc.)
- FOSS license allow list (MIT, Apache-2.0, MPL-2.0, AGPL-3.0-or-later, etc.)
- Advisory + source control

### 4. PeekedStream in sourdough-core (Convergence)

New `sourdough_core::transport` module provides shared implementations:
- `PeekedStream<S>` — replays one consumed byte before delegating to inner stream
- `peek_protocol()` — async first-byte peek, returns `Protocol::JsonRpc` or `Protocol::Binary`
- `resolve_socket_path()` — `$BIOMEOS_SOCKET_DIR` or `$XDG_RUNTIME_DIR/biomeos/{name}-{fid}.sock`
- `socket_path_in()` — pure function for testable socket path construction

This consolidates the pattern independently implemented in BearDog (PrefixedStream),
skunkBat (PeekedStream), songbird (composite BufReader), coralReef (guard_from_first_byte),
and petalTongue (fill_buf). Future primals can use this directly.

### 5. CONVENTIONS.md Drift Fixed

IPC section corrected: JSON-RPC 2.0 is now documented as primary IPC (was incorrectly
showing tarpc as primary). Capability wire standard table added.

### 6. Scaffold Core Crate Bug Fixed

Generated core crate `Cargo.toml` now includes `[lints] workspace = true` —
was missing, so workspace pedantic/nursery lints weren't being inherited.

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 239 | 247 |
| Scaffold output | 1 crate (core) | 2 crates (core + server) |
| Generated files | 9 | 16+ |
| E2e assertions | basic build/test | + deny.toml, CI, server, dispatch, peek |
| sourdough-core modules | 9 | 10 (+ transport) |

## What Scaffolded Primals Now Get

```
{name}/
├── .github/workflows/
│   ├── ci.yml                    Lean single-job CI
│   └── notify-plasmidbin.yml     genomeBin auto-distribution
├── crates/
│   ├── {name}-core/              Lifecycle, health, error traits
│   └── {name}-server/            JSON-RPC server + capability wire
├── deny.toml                     ecoBin v3.0 supply chain
├── specs/                        Specification stub
├── README.md                     With capability wire table
└── CONVENTIONS.md                ecoPrimals coding standards
```

## Deep Debt Cleanup (April 30, 2026 — Session 2)

### 7. Template Module Refactored

Monolithic `templates.rs` (862 lines) refactored into domain-organized module:
- `templates/core.rs` (440L) — Core crate templates
- `templates/server.rs` (319L) — Server crate templates
- `templates/infra.rs` (110L) — CI/CD + deny.toml templates
- `templates/mod.rs` (18L) — Module orchestration

Largest file in codebase: `ipc.rs` at 637 lines (well under 800L threshold).

### 8. Hardcoding Removed

- CLI help examples: `rhizoCrypt` → `myPrimal` (generic)
- Discovery doc examples: `rhizocrypt`, `loamspine` → `my-primal`, `another-primal`
- Discovery grade: A (zero hardcoded primal names in crate code)

### 9. Dependency Alignment

- `chrono` and `tempfile` in sourdough/sourdough-core aligned to `workspace = true`
- Eliminates version drift between workspace-defined and locally-pinned deps

### 10. Documentation Refresh

- All root docs updated to 0.2.0-dev: README, STATUS, WHATS_NEXT, ROADMAP, ARCHITECTURE, START_HERE
- Broken `DEVELOPMENT.md` link in sourdough-genomebin README fixed → `CONVENTIONS.md`
- Binary artifacts (6MB tar.gz) removed from `archive/` directory
- `.gitignore` updated to prevent future binary artifact creep

### 11. tarpc Dependency Removed (Major)

The `tarpc` crate (v0.34) was only used for a `#[tarpc::service]` proc macro annotation
on the `PrimalRpc` trait. The generated tarpc code was never consumed — the client/server
modules were custom implementations. This removal:

- Eliminates 40 unique transitive deps (211 → 171 total)
- Removes deprecated `opentelemetry v0.18`, `tracing-opentelemetry v0.18`, `thiserror v1.x`, `rand v0.8`
- Clears 3 advisory ignores from `deny.toml` (RUSTSEC-2025-0141, RUSTSEC-2026-0007, RUSTSEC-2024-0387)
- Also removed unused dev-deps: `tokio-serde`, `bincode`, `tokio-util`

`PrimalRpc` is now a standard transport-agnostic async trait using `impl Future` return
position (Rust 2024 edition feature). Any binary framing implementation can satisfy it.

### 12. bytes 1.11.1 Security Patch

`bytes` updated from 1.11.0 to 1.11.1 resolving RUSTSEC-2026-0007 (integer overflow in
`BytesMut::reserve`).

### 13. PrimalRpcClient Typed Error

`PrimalRpcClient::connect` now returns `std::io::Result` instead of
`Box<dyn Error + Send + Sync>` — proper typed error handling.

### Verification (post-cleanup)

- `cargo fmt --all -- --check` — clean
- `cargo clippy --workspace --all-targets` — zero warnings
- `cargo test --workspace` — 247 tests passing
- `cargo deny check` — passing (zero advisory ignores, zero suppression)
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — zero warnings
- Total dependencies: 171 (down from 211)

### 14. BTSP Phase 3 Scaffold (May 2, 2026)

Scaffolded primals now generate a `btsp.negotiate` JSON-RPC method handler that
returns `{"cipher":"null","server_nonce":null}` — the graceful NULL cipher fallback.
This makes new primals immediately compatible with primalSpring Phase 3 encrypted
channel negotiation (ChaCha20-Poly1305 client-side) without implementing actual crypto.

Teams can evolve to real AEAD by replacing the NULL response with:
1. Generate 12-byte server_nonce
2. Derive keys via HKDF-SHA256(handshake_key, client_nonce || server_nonce)
3. Return `{"cipher":"chacha20-poly1305","server_nonce":"<hex>"}`
4. Switch to encrypted framing

Reference: petalTongue `crates/petal-tongue-ipc/src/btsp/json_line.rs`

## Remaining Gaps (v0.2.0+)

| Item | Status | Notes |
|------|--------|-------|
| SD-02: musl cross-compilation | Open | sourDough binary not wired for plasmidBin yet |
| SD-03: genomeBin signing | Open | sequoia-openpgp stretch goal |
| BTSP Phase 3 real crypto | Future | Scaffold provides NULL fallback; real ChaCha20 is per-team |
| `sourdough harvest` command | Planned (v0.4.0) | Interface with plasmidBin sources.toml |
| Ephemeral primal scaffolding | Planned (v0.3.0) | EphemeralOwner<T>, session-as-primal |
| sourdough validate ecobin in CI | Future | Static binary verification in generated CI |
