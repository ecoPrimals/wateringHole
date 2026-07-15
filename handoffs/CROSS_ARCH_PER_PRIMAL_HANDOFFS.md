# Cross-Architecture Adoption — Per-Primal Handoffs

**Date**: Jul 15, 2026 | **Wave**: 141a | **From**: eastGate overwatch
**Reference**: `SILICON_ATHEISM_CONVERGENCE_WAVE140b.md`, `CROSS_PLATFORM_PARITY_AAR_WAVE139e.md`
**Pattern**: songBird (`NamedPipeServer`/`NamedPipeClient` behind `#[cfg(windows)]`)

**Each primal team**: apply the transformations below to your codebase.
When done, `cargo check --target x86_64-pc-windows-gnu` should succeed.
Report completion via commit message or handoff to overwatch.

---

## bearDog

**Blocked by**: UDS transport (Category 1)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `beardog-tower-atomic` | `src/lib.rs` | L61, L132-250 | `tokio::net::UnixStream` |

**Fix**: Replace `UnixStream` with `TransportEndpoint` dispatch or `#[cfg(unix)]`/`#[cfg(windows)]` guards. tower-atomic service layer needs platform-agnostic stream type.

**Estimated effort**: Small (1 file)

---

## biomeOS

**Blocked by**: UDS transport + platform FS (Categories 1, 3)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `biomeos-primal-sdk` | `src/communication.rs` | L39 | `UnixStream` |
| `biomeos-primal-sdk` | `src/capabilities.rs` | L17 | `UnixStream` |
| `biomeos-primal-sdk` | `src/provider.rs` | L304 | `UnixStream` |
| `biomeos-primal-sdk` | `src/tarpc_transport.rs` | L47 | `tarpc::serde_transport::unix` |
| `neural-api-client` | `src/connection.rs` | L11 | `UnixStream` |
| (FS) | disk space detection | — | `rustix::fs` + `rustix::system` |

**Fix**: Transport via `TransportEndpoint`. tarpc transport needs `#[cfg]` branching (tarpc has no built-in Windows transport — use TCP fallback). FS: `Platform::detect()` for disk space queries.

**Estimated effort**: Medium (5-6 files, tarpc requires care)

---

## nestGate

**Blocked by**: Platform FS (Category 3)
**Files to modify**:

| Crate | File | Issue |
|-------|------|-------|
| nestGate core | storage detector | `rustix::fs::statfs` — Linux-specific |

**Fix**: Abstract behind `Platform::detect()` with fallback using `std::fs::metadata` or `GetDiskFreeSpaceEx` on Windows.

**Estimated effort**: Small (1 module)

---

## rhizoCrypt

**Blocked by**: UDS transport (Category 1)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `rhizo-crypt-core` | `src/clients/adapters/unix_socket.rs` | L29, L144-170 | `UnixStream` |

**Fix**: Rename to `transport.rs`, add `#[cfg(windows)]` NamedPipe path or `TransportEndpoint`.

**Estimated effort**: Small (1 file, well-isolated adapter)

---

## squirrel

**Blocked by**: UDS transport (Category 1)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `squirrel/core/auth` | `src/capability_crypto.rs` | L32 | `UnixStream` |
| `squirrel/core/auth` | `src/security_provider_client.rs` | L27 | `UnixStream` |
| `squirrel/universal-patterns` | `src/ipc_client/connection.rs` | L6 | `UnixStream` |
| `squirrel/universal-patterns` | `src/registry/discovery.rs` | L15 | `UnixStream` |

**Fix**: All 4 files: `TransportEndpoint` or `#[cfg]` guards.

**Estimated effort**: Small-Medium (4 files, mechanical)

---

## sweetGrass

**Blocked by**: UDS transport (Category 1)
**Files to modify**:

| Crate | File | Issue |
|-------|------|-------|
| `sweet-grass-store-nestgate` | `src/client.rs` L10 | `UnixStream` |
| `sweet-grass-service` | multiple (transport_connect, handlers) | `UnixStream` |

**Fix**: `TransportEndpoint` for store client and service transport.

**Estimated effort**: Small-Medium (2-3 files)

---

## loamSpine

**Blocked by**: UDS transport + Unix signals (Categories 1, 2)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `loam-spine-core` | `src/btsp/provider_client.rs` | L18 | `UnixStream` |
| `loam-spine-core` | `src/transport/neural_api.rs` | L31 | `UnixStream` |
| `loam-spine-core` | `src/service/signals.rs` | L97 | `tokio::signal::unix` |

**Fix**: Transport: `TransportEndpoint`. Signals: `ProcessManager::wait_for_shutdown()` or `#[cfg]` with `ctrl_c()` on Windows.

**Estimated effort**: Small (3 files)

---

## skunkBat

**Blocked by**: UDS transport + Unix signals (Categories 1, 2)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `skunk-bat-server` | `src/ipc/transport/btsp.rs` | L78 | `UnixStream` |
| `skunk-bat-server` | `src/ipc/mod.rs` | L178 | `tokio::signal::unix::signal()` |

**Fix**: Transport: `TransportEndpoint`. Signal: `#[cfg]` + `ctrl_c()`.

**Estimated effort**: Small (2 files)

---

## coralReef

**Blocked by**: UDS transport (Category 1)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `coralReef/primal-rpc-client` | `src/transport.rs` | L64 | `UnixStream` |

**Fix**: `TransportEndpoint` or `#[cfg]` guards.

**Estimated effort**: Small (1 file)

---

## barraCuda

**Blocked by**: UDS transport + Unix signals (Categories 1, 2)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `barracuda-core` | `src/ipc/btsp.rs` | L153-546 | `UnixStream` (extensive) |
| `barracuda-core` | `src/ipc/transport/server.rs` | L2-3 | `UnixStream` |
| `barracuda-core` | `src/bin/barracuda/main.rs` | L158 | literal `unix` signal setup |

**Fix**: Transport: `TransportEndpoint` — this is the largest transport adoption (btsp.rs is ~400 lines of UDS code). Signal: `#[cfg]` + `ctrl_c()`.

**Estimated effort**: Medium (3 files, btsp.rs requires careful extraction)

---

## petalTongue

**Blocked by**: UDS transport + Android NDK (Categories 1, 5)
**Files to modify**:

| Crate | File | Line(s) | Issue |
|-------|------|---------|-------|
| `petal-tongue-core` | `src/transport.rs` | L221-300 | `UnixStream` |
| `petal-tongue-core` | `src/biomeos_discovery/client.rs` | L16 | `UnixStream` |
| (Android) | `android-activity` dependency | — | NDK Activity lifecycle |

**Fix**: Transport: `TransportEndpoint`. Android: target should be `cdylib` loaded by Android Application, not standalone binary.

**Estimated effort**: Medium (2 transport files + Android target config)

---

## sourDough

**Blocked by**: Platform FS (Category 3)
**Files to modify**:

| Issue | Detail |
|-------|--------|
| `std::os::unix::fs::PermissionsExt` | `mode()` for Unix file permissions |

**Fix**: Replace `PermissionsExt::mode()` with cross-platform check. On Windows use `GetFileAttributes` or `std::fs::metadata().permissions().readonly()`.

**Estimated effort**: Small (1 usage site)

---

## toadStool

**Blocked by**: Hardware/kernel deps (Category 4)
**Files to modify**:

| Crate | Issue |
|-------|-------|
| `toadstool-common/hw-safe` | `std::os::fd`, `rustix::mm` (mmap), `rustix::ioctl` (VFIO) |

**Fix**: Feature-gate entire `hw-safe` crate behind `#[cfg(target_os = "linux")]` or `linux-hw` feature flag. GPU compute via VFIO/mmap is fundamentally Linux kernel API. Windows GPU uses different APIs (DXGI, Vulkan).

**Estimated effort**: Small (feature-gate, not rewrite)

---

## Completion Tracking

| Primal | Categories | Effort | Status | Commit |
|--------|-----------|--------|--------|--------|
| songBird | — | — | **DONE** (reference) | `2091974d` cfg gate evolution |
| bearDog | 1 | Small | **DONE** | `1c3dc9de6` tower-atomic cross-platform IPC |
| barraCuda | 1,2 | Medium | **DONE** | `7582ac73` Windows cross-compilation |
| biomeOS | 1,3 | Medium | **DONE** | `16b25557` v4.34 cross-arch + capability discovery |
| coralReef | 1 | Small | **DONE** | `da5afe1` cfg-gate Unix-only code |
| skunkBat | 1,2 | Small | **DONE** | `6b3e6eb` cross-arch + deep debt sweep |
| squirrel | 1 | Small-Med | **DONE** | `da54c045` UDS→platform transport gating |
| toadStool | 4 | Small | **DONE** | `592248618` S329 Windows cargo check passes |
| petalTongue | 1,5 | Medium | **DONE** | `0c65a57` cross-arch transport Windows+Android |
| sourDough | 3 | Small | **DONE** | `320397e` Windows target support |
| rhizoCrypt | 1 | Small | **DONE** | `feff297` cross-arch + deep debt |
| sweetGrass | 1 | Small-Med | **DONE** | `d4f7da9` platform gates |
| loamSpine | 1,2 | Small | **DONE** | `850252c` cfg-gate Unix IPC |
| nestGate | 3 | Small | TODO | Platform FS (`rustix::fs::statfs`) |

**Score: 13/14 adopted. Only nestGate remaining (Platform FS — 1 module).**

Deep debt delivered alongside cross-arch (Waves 141a-141b):
- loamSpine: refactor, deprecation, clone reduction, test fix
- rhizoCrypt: method_gate split, magic numbers, branch/vertex coverage
- sweetGrass: postgres store purged (pure Rust dogma), cross-platform warnings suppressed
- (Wave 141a): barraCuda, bearDog, biomeOS, coralReef, skunkBat, songBird,
  squirrel, toadStool, petalTongue, sourDough — all delivered deep debt alongside cross-arch

---

*Updated Wave 141b: 13/14 primals cross-arch adopted. Only nestGate remaining.
sporeGate Windows harvest pending for 13 adopted primals.*
