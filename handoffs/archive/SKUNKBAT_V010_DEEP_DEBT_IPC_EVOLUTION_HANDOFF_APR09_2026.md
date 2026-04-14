# skunkBat v0.1.0 — Deep Debt Evolution & IPC Surface Handoff

**Date**: April 9, 2026
**Primal**: skunkBat
**Version**: 0.1.0
**Matrix**: ECOSYSTEM_COMPLIANCE_MATRIX v2.7.0

---

## Summary

skunkBat evolved from a library-only primal with no IPC surface to a fully
compliant ecosystem participant with JSON-RPC 2.0 server, BTSP Phase 1, and
Wire Standard L2/L3 compliance. All production stubs replaced with real
implementations. Deep debt systematically resolved.

---

## Changes

### IPC Surface (NEW)

- `skunk-bat-server` binary crate: UniBin with `server`, `health`, `scan`, `detect` subcommands via `clap`
- TCP listener (`--port`, default from `SKUNKBAT_PORT` env or 9140)
- UDS listener (`$BIOMEOS_SOCKET_DIR/skunkbat-{family_id}.sock`)
- BTSP Phase 1: `FAMILY_ID` socket scoping, `BIOMEOS_INSECURE` guard, `XDG_RUNTIME_DIR` fallback
- Wire Standard L2: `capabilities.list` returns primal/version/methods envelope
- Wire Standard L3: `identity.get` returns primal/version/domain/capabilities
- Domain symlink: `security.sock` created on bind, removed on shutdown
- JSON-RPC dispatch: `health.*`, `security.*`, `lifecycle.*`, `capabilities.*`, `identity.*`

### Integration Evolution

- `rpc.rs`: Shared JSON-RPC 2.0 client (UDS-first, TCP-fallback, configurable timeout)
- `toadstool.rs`: Rewritten from stubs to real JSON-RPC discovery client
  - `discover_all()`, `discover_by_capability()` via `discovery.find_all`/`discovery.find_by_capability`
  - `discover_local()` scans `BIOMEOS_SOCKET_DIR` and probes with `capabilities.list`
  - `from_env()` constructor probes `discovery.sock` and `DISCOVERY_ENDPOINT`
- `songbird.rs`: Rewritten from stubs to real JSON-RPC federation client
  - `connect()` probes via `health.liveness`, updates connected state
  - `broadcast_threat()` and `subscribe_threats()` via `federation.broadcast`/`federation.subscribe`
  - `from_env()` constructor probes `federation.sock` and `FEDERATION_ENDPOINT`
- Graceful degradation: all clients return empty/log warnings when providers unavailable

### Hardcoding Elimination

- Port default from `SKUNKBAT_PORT` env var, not literal
- Discovery via `DISCOVERY_ENDPOINT` env var and `discovery.sock` symlink
- Federation via `FEDERATION_ENDPOINT` env var and `federation.sock` symlink
- Zero primal names in routing code

### Code Quality

- Unused deps removed: `toml`, `anyhow`, `chrono`
- `async-trait` retained with justification (dyn-dispatch async methods)
- `VecDeque` rolling window profiler (was `Vec::remove(0)`)
- `/proc/loadavg` system load normalized by CPU count (was hardcoded `0.1`)
- `dispatch.rs` smart-refactored: `try_serialize`/`serialize`/`dispatch_respond` helpers
- `or_default()` for HashMap entries, `let...else` for manual matches
- Clippy `unreachable_pub`/`redundant_pub_crate` conflict resolved via module-level allow

### Documentation

- 11 stale Dec 2025 root docs archived to `fossilRecord/skunkBat/dec-2025-root-docs/`
- `README.md` rewritten: workspace structure, server usage, env vars, quality gates
- `CONTEXT.md` updated: IPC surface, transport, BTSP, wire standard, real integrations
- `specs/00_SPECIFICATIONS_INDEX.md` updated: all specs marked COMPLETE

---

## Quality Gate

| Check | Result |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --workspace -- -D warnings` | PASS (0 warnings) |
| `cargo test --workspace` | 124+ passed, 0 failed |
| `cargo doc --no-deps` | PASS |
| `cargo deny check` | PASS |
| All files <1000 lines | PASS |
| Zero TODO/FIXME/HACK in production | PASS |
| SPDX headers | PASS |
| `forbid(unsafe_code)` | PASS |

---

## Compliance Matrix Update

| Tier | Before | After | Notes |
|------|--------|-------|-------|
| T1 Build | A | A | Already clean; now 124+ tests |
| T2 UniBin | -- | A | `server`/`health`/`scan`/`detect` subcommands |
| T3 IPC | -- | A | TCP + UDS, domain symlink, socket cleanup |
| T4 Discovery | -- | B | `capabilities.list`, `identity.get`, health triad; no self-register yet |
| T5 Naming | -- | A | `domain.verb` throughout |
| T6 Responsibility | A | A | No overstep |
| T7 Workspace | A | A | `[workspace.dependencies]`, `{ workspace = true }` |
| T8 Presentation | B | A | README rewritten, CONTEXT current, `deny.toml`, zero PII |
| T9 Deploy | -- | -- | musl-static and plasmidBin submission pending |
| T10 Live | -- | -- | Not yet deployed to plasmidBin |
| **Rollup** | **A** | **A** | Maintained; now with full IPC compliance |

---

## Remaining Work

- **T9/T10**: musl-static cross-compile and plasmidBin submission
- **BTSP Phase 2**: Server-side handshake enforcement (blocked on BearDog `btsp.session.*` availability)
- **Self-registration**: `capability.register` with ToadStool on startup
- **Coverage**: Run `cargo llvm-cov` for measured coverage report
