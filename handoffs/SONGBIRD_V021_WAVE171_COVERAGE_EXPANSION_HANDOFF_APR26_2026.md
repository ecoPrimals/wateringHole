# Songbird v0.2.1 Wave 171 — Test Coverage Expansion

**Date**: April 26, 2026
**From**: Songbird team
**For**: primalSpring, ecosystem
**Triggered by**: primalSpring April 26 audit — test coverage at 72% vs 90% target

## Summary

Systematic coverage expansion across 13 crates, 30+ files. Coverage
measured via `cargo llvm-cov --workspace --lib`:

| Metric | Before | After |
|--------|--------|-------|
| Line coverage | 71.28% | 73.41% |
| Lib tests | 7,387 | 7,658 |
| New tests | — | +271 |
| Clippy warnings | 0 | 0 |
| Failures | 0 | 0 |

## What Changed

### Fixes (3 broken/flaky tests)

- `birdsong_handler/tests.rs`: 2 beacon tests failed due to evolved error
  messages. Switched to existing helper that matches broader error patterns.
- `rpc/tarpc_server/mod.rs`: `test_tarpc_config_default` was flaky under
  parallel test execution (env var pollution). Added env lock + guard.

### New Tests (by crate)

- **songbird-orchestrator** (largest crate, ~74K lines): information layers,
  capability adapters, AI workload types, storage IPC key helpers,
  graph intelligence handlers, service registry handlers, in-memory storage,
  deployment helpers, task API serde, compute routing, discovery startup,
  discovery bridge, connectivity, command handler, HTTP gateway errors
- **songbird-config**: primal endpoints, connection/tuning constants,
  Consul/etcd/Kubernetes discovery pure helpers, timeout/resource constants
- **songbird-discovery**: BirdSong encryption dispatch, network region
  detection, resource parsing, static discovery backend, abstraction
  adapters/delegation
- **songbird-universal**: capability types, unified adapter error edges
- **songbird-network-federation**: security factory, federation discovery
  modes, crypto helpers, network config
- **songbird-http-client**: crypto capability extraction, key exchange parsing
- **songbird-lineage-relay**: packet masking, protocol encode/parse
- **songbird-cli**: template rendering, discovery scanning, compatibility scoring
- **songbird-compute-bridge**: CSV normalization, tower ID resolution
- **songbird-remote-deploy**: SSH commands, deployment config, tower finder
- **songbird-execution-agent**: health check, error responses
- **songbird-sovereign-onion**: storage socket parsing
- **songbird-onion-relay**: NAT classification

## Remaining

73.41% → 90% target. Remaining gap (~17pp) is mostly in:
- I/O-heavy code paths (live socket, network, filesystem)
- Integration-style orchestrator paths
- Large dispatcher modules (server/mod.rs, app/http_server.rs)

Further progress requires either deeper mock infrastructure or E2E
integration test expansion.

## Verification

```bash
cargo fmt --check          # clean
cargo clippy --workspace -- -D warnings  # 0 warnings
cargo test --workspace --lib  # 7,658 passed, 0 failed, 22 ignored
cargo llvm-cov --workspace --lib --summary-only  # 73.41%
```
