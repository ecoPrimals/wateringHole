# biomeOS v2.71 — Deep Debt + Multi-Transport IPC Evolution Handoff

**Date**: March 28, 2026
**Version**: v2.70 → v2.71 (4 commits: v2.70, v2.71, v2.71a, v2.71b)
**Tests**: 7,167 passing (0 failures)
**Clippy**: 0 warnings (pedantic + nursery)

---

## Summary

This session resolved all P0/P1 gaps from the primalSpring universal deployment
review and executed comprehensive deep debt resolution across the biomeOS
workspace.

---

## Multi-Transport IPC Evolution (v2.70)

Resolved the critical "Neural Router is Unix-Socket-Only" gap. The entire
`capability.call` → `forward_request` path now supports all transport types.

| Component | Before | After |
|-----------|--------|-------|
| `RegisteredCapability.socket_path` | `PathBuf` | `TransportEndpoint` (enum) |
| `DiscoveredPrimal.socket_path` | `PathBuf` | `TransportEndpoint` |
| `DiscoveredAtomic.primary_socket` | `PathBuf` | `TransportEndpoint` |
| `forward_request` | `AtomicClient::unix()` | `AtomicClient::from_endpoint()` |
| Health checks | `Path::exists()` | `AtomicClient`-based probing |
| `capability.register` handler | Socket path only | Parses transport strings |
| `TransportEndpoint` | Internal only | `+ Serialize + Deserialize` |

Transport string parsing: `@abstract` → abstract socket, `tcp://host:port` →
TCP, `http://host:port` → HTTP JSON-RPC, `/path.sock` → Unix socket.

## Deep Debt Resolution + Standards Compliance (v2.71)

| Change | Detail |
|--------|--------|
| `CONTEXT.md` | Created per `PUBLIC_SURFACE_STANDARD` |
| README footer | Added "Part of ecoPrimals" + version reconciliation |
| `forwarding.rs` | 1001 → 357 LOC (tests extracted to `forwarding_routing_tests.rs`) |
| `deployment_graph.to_toml()` | Stub → real `toml::to_string_pretty()` + 2 tests |
| Chimera codegen | Stub error → capability-based IPC forwarding pattern |
| `#[allow]` → `#[expect]` | `cast_possible_wrap`, `unsafe_code` migrated with reasons |

## Zero-Copy + Clone Audit (v2.71a)

| Change | Detail |
|--------|--------|
| `ResourceInfo` | Added `Copy` derive (all `usize` fields) — 6 `.clone()` eliminated |
| `neural_executor.rs` | Redundant `String` clone in topological sort removed |
| `neural_executor.rs` | Redundant `Value` clone in rpc_call circuit breaker removed |
| `env_helpers.rs` | `#[allow(unsafe_code)]` → `#[expect(unsafe_code, reason)]` |
| `fractal.rs` | "Not yet implemented" stub → architectural constraint message |

## BearDog Client Dead Code Removal (v2.71b)

| Change | Detail |
|--------|--------|
| `BearDogEndpoint::Http` | Variant removed (all 5 methods returned "deprecated" errors) |
| Method bodies | `match` arms → `let` destructuring (single-variant enum) |
| `with_endpoint()` | `String` → `impl AsRef<str>`, rejects HTTP at construction |
| `BearDogClient` | Added `#[derive(Debug)]` |
| Dead code | 73 lines eliminated |
| Tests | 4 deprecated-path tests updated to verify construction rejection |

---

## Audit Results (Clean)

| Metric | Value |
|--------|-------|
| Files >1000 LOC | 0 |
| `#[allow()]` in production | 0 |
| `TODO`/`FIXME`/`HACK` | 0 |
| `todo!`/`unimplemented!` | 0 |
| `unsafe` in production | 0 |
| Production mocks | 0 |
| Clippy warnings | 0 |
| `cargo deny` | PASS (licenses, advisories, bans, sources) |
| `cargo doc` | 0 warnings |

## Remaining P2 Items (Future)

| Item | Priority | Notes |
|------|----------|-------|
| `route.register` JSON-RPC | P2 | Cross-gate routing API (foundation complete) |
| ARM64 biomeOS binary | P0 (deploy) | Pure Rust, cross-compile straightforward |
| biomeOS on gate2 | P2 | Validates cross-gate routing end-to-end |
