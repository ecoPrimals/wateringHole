# BearDog v0.9.0 — Wave 11: Deep Coverage Push, Crypto Fault Injection & Zero-Copy IPC

**Date**: March 23, 2026
**Primal**: BearDog (cryptographic service provider)
**Session Focus**: Per-crate coverage push toward 90%, crypto fault injection testing, IPC hot path zero-copy optimization, root doc reconciliation

---

## What Changed

### Coverage Push (86.1% → 87.0%)

122+ new tests across 6 crates targeting lowest-coverage files:

| Crate | New Tests | Key Areas Covered |
|-------|-----------|-------------------|
| beardog-deploy | 16 | `SystemCommandRunner::run_bounded` timeouts, `DeviceManager` mock paths, `AndroidDeployment`/`RustBuilder` construction, `DeploymentConfig` validation |
| beardog-discovery | 13 | `Announcer` lifecycle (new, start, mDNS/DNS-SD/disabled), `capability_env` wrappers, `primary_url_to_ipc_socket_path` parsing |
| beardog-installer | 30 | `Architecture::to_rust_target` all combos, `binary_extension`, `PrimalName` parsing, `DeploymentReport` display, `BinaryValidator`, `BiomeOSPaths` |
| beardog-cli | 14 | `resolve_server_socket_path`, `handle_hsm_*` commands, `handle_cross_primal` dispatch (all 5 capabilities), `prepare_daemon_pid_file` |
| beardog-tunnel | 25 | `aliases_and_beardog::route` (crypto.hash, beardog.crypto.*), `TcpIpcClient` happy/error paths, `modes::client::run`, + 14 crypto fault injection |
| beardog-types | 11 | `KubernetesDiscovery::try_create` error, `create_service_discovery` DNS fallback, `UnifiedProductionConfig` lifecycle, `UniversalDiscoveryRequest` serde |

### Crypto Fault Injection (14 Tests)

Adversarial input tests for all major crypto handlers:
- **Blake3**: Malformed base64 input
- **ChaCha20-Poly1305**: Wrong nonce length, corrupted ciphertext, wrong authentication tag
- **Ed25519**: All-zero/all-ones keys, corrupted signatures
- **X25519**: Wrong-length DH secrets, zero public key
- **Tor ntor**: Wrong-length client state

All handlers confirmed to detect and report errors cleanly — no panics, no invalid output.

### Zero-Copy IPC Optimization

`unix_socket_ipc::server.rs` hot path audit and optimization:
- **Before**: Byte-at-a-time `read_exact` with `Vec::push` — O(n) reallocations per message
- **After**: `BufReader::read_until` with pre-allocated reusable buffer — single allocation, cleared per iteration
- Both initial protocol detection read and main JSON-RPC request loop optimized
- `bytes::Bytes`/`Arc<str>` adoption deferred — message sizes don't justify complexity; buffer reuse addresses the primary bottleneck

### Root Doc Reconciliation

All root docs aligned to consistent numbers:
- STATUS.md, ROADMAP.md, README.md, START_HERE.md — all now reflect 14,161 tests / 87.0% coverage
- Wave 11 section added to STATUS.md
- ROADMAP.md: Fault Injection and Zero-Copy items marked DONE
- Per-crate coverage table refreshed with Wave 11 boosts

---

## Session Metrics

| Metric | Value |
|--------|--------|
| `cargo test --workspace` | **14,161** passed, **0** failed |
| Line coverage (`llvm-cov`) | **87.0%** (105,989/121,844 lines) |
| Format / clippy / doc / deny | All clean |

---

## Quality Gates (all green)

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-features` | 0 warnings |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo deny check` | Advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace` | 14,161 passed, 0 failed |
| `cargo llvm-cov --workspace --summary-only` | 87.0% line coverage |

---

## Architecture Compliance

- **Edition 2024**, **MSRV 1.93.0**, **Pure Rust** (ecoBin), **UniBin**, **DI-based** composition
- **JSON-RPC + tarpc** IPC, **`forbid(unsafe_code)`** workspace-wide, **AGPL-3.0-only**
- **91+ JSON-RPC methods** with semantic naming (including `capability.list`, `primal.capabilities` aliases)

---

## Remaining Work / Next Session Priorities

| Item | Notes |
|------|--------|
| Coverage → **90%** | Current **87.0%** — remaining gap is in integration-heavy paths requiring live services |
| Remaining **85** `.unwrap()` | Mostly platform-specific and coverage-extension files |
| `api_demo` example | Minor Cargo name collision warning |
| License alignment | AGPL-3.0-only vs wateringHole standards |
| Docs provenance | scyBorg ORC + CC-BY-SA headers on docs (if applicable) |

---

## Verification Commands

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-features
cargo doc --workspace --all-features --no-deps
cargo deny check
cargo test --workspace
cargo llvm-cov --workspace --summary-only
```
