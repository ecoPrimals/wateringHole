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

## Remaining Gaps (v0.2.0+)

| Item | Status | Notes |
|------|--------|-------|
| SD-02: musl cross-compilation | Open | sourDough binary not wired for plasmidBin yet |
| SD-03: genomeBin signing | Open | sequoia-openpgp stretch goal |
| `sourdough harvest` command | Planned (v0.4.0) | Interface with plasmidBin sources.toml |
| Ephemeral primal scaffolding | Planned (v0.3.0) | EphemeralOwner<T>, session-as-primal |
| sourdough validate ecobin in CI | Future | Static binary verification in generated CI |
