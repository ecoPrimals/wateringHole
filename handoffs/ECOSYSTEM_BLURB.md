# ecoPrimals Ecosystem Blurb — Cross-Arch Compliance

**Date**: Aug 7, 2026 7:00AM | **Wave**: 156v | **From**: eastGate overwatch
**Posture**: **CROSS-ARCH FAILURES REMAIN.** G66 transport modules shipped but 5 primals still fail Windows: existing code paths not migrated to use them. **NEW STANDARD: code teams MUST `cargo check --target x86_64-pc-windows-gnu` before push.** Musl depot 16/16 on golgi. Windows 10/15.

---

## THE ISSUE

G66 transport abstraction modules were *added* to all 15 primals — but in 5 primals the existing production and test code still imports `UnixStream`/`UnixListener`/`rustix`/`PermissionsExt` directly, bypassing the new transport layer. The pattern is there but the migration is incomplete.

**New ecosystem standard**: Every primal push MUST pass `cargo check --target x86_64-pc-windows-gnu` before push. No exceptions. This is how we enforce silicon neutrality — the compiler catches deism at the gate.

---

## 5 FAILING PRIMALS — SPECIFIC VIOLATIONS

### coralReef (biomeGate)

| File | Issue |
|------|-------|
| `local_transport.rs` | `connect_local_sync()` uses `std::os::unix::net::UnixStream` directly. `symlink()` uses `std::os::unix::fs::symlink`. |
| `server_lifecycle.rs` | `tokio::signal::unix::SignalKind` unguarded |
| `cmd_server_process.rs` (test) | Direct `UnixStream::connect` |
| `tests_ecosystem.rs` (test) | Direct `UnixListener::bind` |
| **Also**: musl compile issue — `ipc` module behind test cfg but `connect_local()` references it unconditionally |

### petalTongue (overwatch)

| File | Issue |
|------|-------|
| `jsonrpc_integration_tests.rs` (test) | Direct `UnixListener`/`UnixStream` |
| `jsonrpc_provider/tests.rs` (test) | Direct `UnixListener`/`UnixStream` across 6+ test fns |

### skunkBat (eastGate)

| File | Issue |
|------|-------|
| `rpc.rs` | `UnixStream::connect` in prod code |
| `tarpc_uds.rs` | `tarpc::serde_transport::unix::listen` in prod |
| `tarpc_uds_tests.rs` | 7 tests using `tarpc::serde_transport::unix::connect` |

### squirrel (eastGate)

| File | Issue |
|------|-------|
| `security.rs` / `security_tests.rs` | `std::os::unix::fs::PermissionsExt` unguarded |
| `capability_jwt.rs` + tests | Direct `UnixListener`/`UnixStream` in prod + test |
| `capability_jwt_integration_tests.rs` | Full UDS mock server unguarded |

### toadStool (biomeGate)

| File | Issue |
|------|-------|
| `unix_socket_provider.rs` | Direct `UnixStream::connect` in prod |
| `tarpc_server/connection.rs` | `UnixStream` param in prod fn signature |
| `tarpc_server/mod.rs` | Direct `UnixListener` |
| `unibin/execution.rs` | `UnixListener` + `tokio::signal::unix` |
| `akida-setup/` + `akida-driver/` | `PermissionsExt`, `AsFd` (neuromorphic crates) |

---

## THE FIX — PER PRIMAL

For each violation:

1. **Production code**: Replace direct `UnixStream`/`UnixListener` with `TransportStream`/`TransportListener` from the primal's own G66 transport module. Use `connect_transport(&endpoint)` not `UnixStream::connect(path)`.

2. **Test code**: Wrap unix-only test infrastructure with `#[cfg(unix)]`. Tests that need UDS can be unix-only — the transport abstraction in prod code is what matters for cross-arch builds.

3. **Signal handling**: `tokio::signal::unix::SignalKind` → guard with `#[cfg(unix)]`, add `#[cfg(windows)] tokio::signal::ctrl_c()` alternative.

4. **Permissions/fs**: `std::os::unix::fs::PermissionsExt`, `std::os::unix::io::AsFd` → guard with `#[cfg(unix)]`.

5. **tarpc unix transport**: `tarpc::serde_transport::unix::*` → guard entire tarpc UDS modules with `#[cfg(unix)]`, use tarpc TCP transport on non-unix.

---

## NEW STANDARD — PRE-PUSH CROSS-ARCH CHECK

**Every code team adds this to their workflow before pushing:**

```bash
cargo check --target x86_64-pc-windows-gnu
```

If the target isn't installed:
```bash
rustup target add x86_64-pc-windows-gnu
```

This catches silicon deism at dev time, not at depot rebuild. The compiler is the enforcer.

**sourDough should add this as a reference practice** — a `scripts/check-cross-arch.sh` or similar, so other teams can converge on the same pre-push validation.

---

## DEPOT STATUS

| Target | Binaries | Status |
|--------|----------|--------|
| **x86_64-unknown-linux-musl** | **16/16** | On golgi. Deploy gates with these. |
| **x86_64-pc-windows-gnu** | **10/15** | 5 primals failing (see above) |

---

## GATE DEPLOYMENT — PROCEED WITH MUSL

Don't wait for Windows. Deploy musl bins now.

| Gate | Action | Priority |
|------|--------|----------|
| **ironGate** | Pull musl from golgi. Deploy. | **NOW** |
| **westGate** | Pull musl. Deploy. Enable nestGate TCP. | **NOW** |
| **blueGate** | Deploy musl side. Windows after code fixes. | NORMAL |
| **southGate** | Re-deploy. | LOW |
| **strandGate** | Deploy when ready. | DEFERRED |

---

## AFTER DEPLOY — SPRINGS + SCIENCE

| # | Item | Gate | Unblocks |
|---|------|------|----------|
| E2 | squirrel systemd on ironGate | ironGate | Agent panel |
| D1 | tideGlass cell boot | westGate | NF GPS |
| O5 | nestGate TCP on westGate | westGate | Inter-gate CAS |
| O7 | Inter-gate `content.get` E2E | mesh | Data-remote springs |

---

## BACKGROUND

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | ChunkedBraid. AlphaFold. Multi-tier CAS. | Running |
| **strandGate** | SU(N) grid. arXiv 40/42. Observable battery 69/69. | Running |
| **whitePaper** | petalTongue-native figures replacing matplotlib. | Evolving |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| G64 + G65 + G66 | **COMPLETE** (pattern shipped 15/15) |
| Cross-arch (Windows) | **10/15** — 5 primals need migration cleanup |
| Musl depot | **16/16 on golgi** |
| sporeGate health | **12/13 alive** |
| Gates online | **11** |
| Primal tests | **~140,000+** |

---

*Wave 156v — **CROSS-ARCH COMPLIANCE.** G66 transport modules shipped 15/15 but 5 primals still fail Windows — existing code not migrated to use transport abstraction. Specific violations listed per primal. NEW STANDARD: `cargo check --target x86_64-pc-windows-gnu` before every push. Musl depot 16/16 — gate teams deploy musl now. Windows fixes are code team responsibility. 14 COMPLETE / 25 ACTIVE / 23 GLACIAL. 62 goals. 15/15 GREEN.*
