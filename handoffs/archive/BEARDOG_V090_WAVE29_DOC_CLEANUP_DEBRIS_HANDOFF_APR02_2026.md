# BearDog v0.9.0 — Wave 29: Doc Cleanup, BTSP Rewrite, Debris Removal

**Date**: April 2, 2026
**Scope**: Root documentation alignment, BTSP modernization, build artifact and comment debris cleanup

---

## Changes

### Root Documentation Updated

All root `.md` files aligned to current codebase state:

| File | Changes |
|------|---------|
| **README.md** | License badge `AGPL-3.0-or-later`; test count 14,366+; serial tests 35 (was 0) |
| **ARCHITECTURE.md** | Date April 2; test count 14,366+; `#[serial]` minimized row |
| **CONTEXT.md** | Rust sources 1,888 (was 1,892); test count 14,366+ |
| **ROADMAP.md** | Date April 2; test count 14,366+; serial tests updated; file count 1,888 |
| **STATUS.md** | Fixed stale 14,610+ in Wave 21 history line |
| **SECURITY.md** | Date April 2 |
| **START_HERE.md** | Methods 93; test count 14,366+; coverage 90.16%; serial 35; date April 2 |
| **Dockerfile** | SPDX `AGPL-3.0-or-later`; OCI label `AGPL-3.0-or-later` |

### BTSP Rewrite

`wateringHole/btsp/BEARDOG_TECHNICAL_STACK.md` was fully rewritten from a stale v0.15.0 HTTP REST description to the current v0.9.0 JSON-RPC architecture:

- Reflects 29-crate workspace, 93 JSON-RPC methods, NDJSON wire format
- HSM abstraction hierarchy, multi-family isolation, platform support table
- Quality metrics (14,366+ tests, 90.16% coverage, zero unsafe)
- Architectural compliance table (UniBin, ecoBin, self-knowledge, zero hardcoding)
- Wave 26-28 evolution summary
- Future work roadmap

### Debris Removed

- `crates/beardog-cli/audit.log` (3.6 KB)
- `crates/beardog-tunnel/audit.log` (197 KB)

### Stale Comment Cleanup

| File | Change |
|------|--------|
| `beardog-types/.../config/mod.rs` | Removed stale "bootstrap.rs needs integration" note (already integrated) |
| `beardog-auth/.../node_registry.rs` | Removed 2 "Test removed" tombstone comments |
| `beardog-core/.../integration_engine_tests.rs` | Removed 4 "Tests private method" tombstone comments |
| `beardog-genetics/.../birdsong/mod.rs` | Updated outdated doc example to match current `BirdSongManager::new(secret, config)` API |
| `beardog-core/.../primal_discovery.rs` | Reworded "not yet implemented" to neutral "Unimplemented discovery methods" |

### Not Changed (Legitimate)

- `beardog-tunnel/.../windows.rs:81` — "needs proper implementation" is accurate Phase 2 status
- `beardog-tunnel/.../collaboration_service.rs` — Blocker note about `beardog-adapters` wiring is accurate
- `examples/solokey_genetic_experiments.rs` — FIDO2 API disabled note is accurate
- Historical wave entries in CHANGELOG.md/STATUS.md with old metrics — kept as fossil record
- `CONTEXT.md` mentions of Songbird/NestGate/biomeOS — ecosystem context, not hardcoded primal coupling

---

## Gate Status

- `cargo fmt --all` — clean
- `cargo clippy --workspace -- -D warnings` — 0 warnings
- `cargo test --workspace` — 14,366+ passing, 0 failures
- `cargo deny check` — 4/4 pass
