# ToadStool S198 Handoff — Deep Debt Evolution + Gap Matrix Resolution

**Date**: April 9, 2026
**Session**: S198
**Author**: westgate
**Status**: Complete

---

## Summary

S198 executed comprehensive deep debt cleanup, gap matrix resolution from primalSpring audit, and modern Rust evolution across 228 files (net -5,157 lines).

---

## Changes

### Gap Matrix Resolution
- **TS-01 RESOLVED**: coralReef discovery evolved from 6-step legacy lookup to unified `capability.discover` — removed `CORALREEF_SOCKET`/`CORALREEF_URL` env, `coralreef-core.json` manifest, `coralreef*.sock` dir scan from `visualization_client.rs`
- **BTSP Phase 2 WIRED**: Handshake enforced on ALL UDS accept paths — tarpc_server.rs and daemon/jsonrpc_server.rs now run `BtspServer::accept_handshake` when FAMILY_ID is set (pure JSON-RPC already had it)
- **Health triad shaped**: `health.liveness` → `{"status":"alive"}`, `health.readiness` → `{"status":"ready","version":"..."}`, `health.check` → full envelope (Wire Standard L1/L2)
- **Musl-static binary**: 11MB x86_64 PIE stripped static binary built and validated (`cargo build --release --target x86_64-unknown-linux-musl`)

### OpenCL Deprecation (S198)
- Removed `ocl` dependency from gpu and universal crates
- Stubbed all OpenCL code paths with deprecation notices
- `GpuFramework::OpenCl` variant marked `#[deprecated]`
- OpenCL compute handled by barraCuda/coralReef via IPC; toadStool focuses on Vulkan/wgpu

### Smart Large File Refactoring (6 files → module directories)
- `handler/core.rs` (809L) → `core/{mod,health,identity,compute,wire_l3}.rs`
- `tarpc_server.rs` (663L) → `tarpc_server/{mod,connection,executor}.rs`
- `interned_strings.rs` (637L) → `interned_strings/{mod,capabilities,protocols,primals,socket_env,biomeos_manifest_serde}.rs`
- `ecosystem/types.rs` (616L) → `types/{mod,endpoint,discovery,storage,crypto}.rs`
- `storage_backend/storage.rs` (569L) → `storage/{mod,construct,ops,tests}.rs`
- `cloud_provider_trait.rs` (559L) → `cloud_provider_trait/{mod,types,provider,registry}.rs`

### Capability-Based Discovery Evolution
- `SocketPathEnv` connection hints: coordination, security, storage, routing
- `resolve_capability_socket_fallback` now uses connection hints for Unix path resolution
- 8 call sites updated to capability-based endpoint resolution
- Distributed discovery accepts capability strings alongside legacy node labels

### Production Placeholder Evolution
- BearDog token refresh: placeholder → real async `auth.token.refresh` RPC
- Embedded programmer/emulator: generic errors → `thiserror` platform-specific types
- BTSP-disabled stubs: now cleanly close connections (no NDJSON fallback)

### Unsafe Code Hardening
- nvpmu: `VfioIrqSetPayload` `#[repr(C)]` struct replaces `Vec<u8>` cast
- v4l2: `validate_v4l2_fd` guard before each ioctl
- hw-safe: `size > isize::MAX` bounds check, debug assertions for fd/alignment
- secure_enclave: page-alignment checks before `madvise`

### Lint Evolution
- `#[allow()]` → `#[expect()]` where lint actually fires; ~80 justified `#[allow]` remain
- Resolved all unfulfilled `#[expect]` warnings (dead_code on test-used items, unused_async after module extraction)

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | 0 diffs |
| `cargo clippy --all-features --all-targets` | 0 warnings |
| `cargo check --all-features` | Clean |
| `cargo test --all-features` | 0 failures |
| Production TODOs | 0 |
| Production unsafe | ~66 (all in hw-safe/GPU/VFIO/display containment) |
| `#[allow]` count | ~80 justified |
| File size | All production <500 lines |

---

## Metrics

- 228 files changed, +2,709 / -7,866 lines (net -5,157)
- Musl-static binary: 11MB x86_64-unknown-linux-musl PIE stripped
- 0 clippy warnings across full workspace (pedantic + nursery)

---

## Gap Matrix Status (post-S198)

| Gap | Status |
|-----|--------|
| TS-01: coralReef discovery | **RESOLVED** — unified capability.discover |
| BTSP Phase 1: Socket naming | **RESOLVED** (S192) |
| BTSP Phase 2: Handshake on accept | **WIRED** — all 3 UDS listeners |
| Health triad | **RESOLVED** — L1/L2 shapes correct |
| Musl-static binary | **BUILT** — 11MB x86_64 |
| `#[allow]` → `#[expect]` | **EVOLVED** — ~80 justified remain |

---

## Cross-Primal Impact

- **primalSpring**: All toadStool audit gaps addressed (TS-01, BTSP Phase 2, health triad, musl)
- **biomeOS**: Health triad wire-compliant; BTSP enforced on all accept paths
- **plasmidBin**: Fresh musl-static binary ready for harvest

---

## References

- Prior: `0e3549d8` (S194)
- Standards: `CAPABILITY_BASED_DISCOVERY_STANDARD.md`, `BTSP_PROTOCOL_STANDARD.md`, `DEPLOYMENT_VALIDATION_STANDARD.md`, `ECOSYSTEM_COMPLIANCE_MATRIX.md`
