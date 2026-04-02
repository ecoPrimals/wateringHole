# ToadStool S169 — Primal Overstep Cleanup + Deep Debt Evolution

**Session**: S169
**Date**: March 31, 2026
**Focus**: Primal Overstep Cleanup + Deep Debt Evolution
**Status**: All quality gates green (`cargo check`, `fmt`, `test --no-run`)

---

## Summary

Major overstep cleanup removing 30+ JSON-RPC methods that belonged to other primals (Squirrel, coralReef, biomeOS, songBird). Deep debt evolution evolving hardcoded ports, paths, and mocks to capability-based discovery, platform-agnostic temp dirs, and test-gated mocks. Smart refactoring of the largest file (1123→4 semantic submodules) and standardization of workspace dependency inheritance. Net: **-10,659 lines**, **+656 lines**, 134 files changed.

---

## Overstep Removed

| Removed Surface | Domain Owner | Details |
|----------------|-------------|---------|
| `inference.list_models`, `inference.execute`, `inference.load_model`, `inference.unload_model` | **Squirrel** (AI) | Ollama handler + handler wiring |
| `shader.compile.wgsl`, `shader.compile.spirv`, `shader.compile.status`, `shader.compile.capabilities`, `shader.compile.wgsl.multi` | **coralReef** (compilation) | Shader compile proxy; `shader.dispatch` kept (legitimate) |
| `science.compute.*`, `science.gpu.*`, `science.npu.*`, `science.substrate.*`, `science.activations.*`, `science.rng.*`, `science.special.*` | **barraCuda** / biomeOS | Science domains relay |
| `ecology.*` | **biomeOS** (ecology) | airSpring science offload routing |
| `discovery.primals`, `discovery.primal_health`, `discovery.direct_rpc`, `discovery.topology` | **biomeOS** (discovery) | NUCLEUS primal discovery |
| `deploy.capability_call`, `deploy.graph_status` | **biomeOS** (deploy) | Science primal capability routing |
| HTTP server stack (handlers/, routes.rs, lifecycle.rs, server.rs) | **songBird** (HTTP) | axum REST API — daemon now uses pure JSON-RPC over UDS |
| CLI HTTP daemon (http_server.rs) | **songBird** (HTTP) | Removed; daemon uses jsonrpc_server |

## Deep Debt Resolved

| Item | Before | After |
|------|--------|-------|
| **Hardcoded ports** | `discovery_fallback`, `fallback` modules with SONGBIRD/BEARDOG/NESTGATE named constants | Removed; pure `capability_fallback` with env var override |
| **Network constants** | `DEFAULT_COORDINATION_ENDPOINT = "http://127.0.0.1:8080"`, WebSocket, Consul/etcd helpers | Removed HTTP-centric constants; kept address primitives only |
| **Production mock** | `InMemoryAuthBackend` with `ed25519:mock:` signatures shipped in prod | Gated behind `#[cfg(any(test, feature = "test-mocks"))]` |
| **Large file** | `embedded/types.rs` at 1123 lines | Semantic split: `job.rs` (267), `toolchain.rs` (251), `interfaces.rs` (183), `tests.rs` (447) |
| **/tmp hardcoding** | 6+ files with `"/tmp"` literals | `std::env::temp_dir()` + XDG conventions |
| **Service discovery** | TCP localhost fallback when discovery fails | Unix socket fallback: `$XDG_RUNTIME_DIR/ecoPrimals/{capability}.sock` tried before TCP |
| **Embedded stubs** | Bare stubs without error types | Feature-gated `embedded-placeholder-impls`, proper `SpecialtyRuntimeError` variants |
| **Workspace deps** | `indicatif` unused; `url`/`futures`/`clap` pinned locally | Removed `indicatif`; standardized `workspace = true` inheritance |

## Dependency Changes

| Dependency | Crate(s) | Reason |
|-----------|----------|--------|
| `axum`, `tower`, `tower-http` | server, cli | HTTP is songBird's domain |
| `hyper`, `tower` | distributed, analytics | Unused / HTTP overstep |
| `pyo3`, `pyo3-asyncio` | workspace | FFI violates ecoBin v3.0 |
| `linfa` | performance | ML → barraCuda/Squirrel |
| `gbm` | display | C dep (wayland-sys transitive) |
| `hmac` | workspace | Unused |
| `indicatif` | workspace | Unused |

## Impact on Other Primals

| Primal | Impact |
|--------|--------|
| **coralReef** | toadStool no longer proxies `shader.compile.*` — springs should call coralReef directly for compilation |
| **Squirrel** | toadStool no longer proxies `inference.*` — springs should call Squirrel directly for AI/ML |
| **biomeOS** | toadStool no longer handles `ecology.*`, `discovery.*`, `deploy.*` routing — biomeOS owns these |
| **songBird** | toadStool no longer serves HTTP — pure JSON-RPC over Unix sockets only |

## Service Discovery Evolution

- **TCP localhost fallback deprecated** in favor of Unix socket fallback
- **Socket path convention**: `$XDG_RUNTIME_DIR/ecoPrimals/{capability}.sock`
- **Resolution order**: mDNS → env var → XDG socket → TCP (last resort with deprecation warning)

## Build Verification

- `cargo check --workspace`: clean, 0 errors
- `cargo test --workspace --no-run`: all test binaries compile
- `cargo fmt --all`: 0 diffs
- Net: 134 files changed, +656 / -10,659 lines

## Next Steps for Downstream

1. **Springs calling `inference.*`**: Route to Squirrel via IPC instead of through toadStool
2. **Springs calling `shader.compile.*`**: Route to coralReef directly; toadStool only handles `shader.dispatch`
3. **Springs calling `ecology.*`/`discovery.*`/`deploy.*`**: Route to biomeOS
4. **HTTP clients of toadStool daemon**: Migrate to JSON-RPC over Unix socket (`$XDG_RUNTIME_DIR/biomeos/toadstool.sock`)
5. **Primals using `{PRIMAL}_PORT` env vars**: Migrate to `TOADSTOOL_{CAPABILITY}_PORT` convention
6. **Socket discovery**: Primals should expose `$XDG_RUNTIME_DIR/ecoPrimals/{capability}.sock` for fallback discovery
