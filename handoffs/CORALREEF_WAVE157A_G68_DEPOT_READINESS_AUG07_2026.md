# coralReef Wave 157a — G68 Platform Substrate + Depot Readiness

**Date**: 2026-08-07 | **Author**: coralReef code team (strandGate)
**Wave**: 157a | **From**: eastGate overwatch
**Gate**: strandGate | **Commit**: `b30da1d7`

---

## SUMMARY

coralReef is **depot-ready** and **G68-audited**. The Wave 157a blurb lists
coralReef as cross-arch 15/15 PASS (unchanged from 156z). G68 Platform
Substrate L1 evolution shipped: `create_local_symlink()` now uses
`std::os::windows::fs::symlink_file` on Windows instead of returning
`Unsupported`.

## G68 AUDIT — coralReef

| Layer | Exposure | Status |
|-------|----------|--------|
| **L1: Links** | 1 function (`create_local_symlink()`) | Evolved to G68 — `symlink` on Unix, `symlink_file` on Windows |
| **L2: Permissions** | 0 files | No `PermissionsExt`/`set_mode` usage |
| **L3: Device backends** | 0 files | No `rustix`/`libc` direct usage (pure compiler primal) |
| **G66 Transport** | Already done | `TransportStream`/`TransportListener` confine `#[cfg(unix)]` (Wave 156s) |

**Production files with `std::os::unix`**: 4 (all already `#[cfg(unix)]` gated or abstracted)
- `transport.rs` — G66 transport layer (confined)
- `service/provenance.rs` — signing via Unix socket (gated)
- `ipc/btsp_client.rs` — BTSP client (gated)
- `primal-rpc-client/transport.rs` — RPC client (abstracted via `LocalStream`)

**Test-only files**: 9 — excluded from G68 scope.

**coralReef's G68 exposure is minimal** — it's a pure compiler primal with no
hardware-direct APIs (L3). All Unix-specific code is already confined to the
transport/IPC layer via G66.

## CROSS-ARCH STATUS

- `cargo check --target x86_64-pc-windows-gnu --all-features` — zero errors, zero warnings
- `cargo clippy --target x86_64-pc-windows-gnu --all-features -- -D warnings` — zero warnings
- `cargo clippy --all-features -- -D warnings` — zero warnings (Linux)

## TEST STATUS

- 3,672 passed, 0 failed, 6 ignored
- Zero `unsafe` in production
- Zero clippy warnings on Linux + Windows

## HARDWARE (strandGate)

- RTX 3090: 65°C, 12% util, 722/24576 MiB
- coralReef not currently running (no NUCLEUS composition active at check time)

## NEXT WORK

1. **Deploy across NUCLEUS gates** — depot binary available, gate teams pull
2. **G68 convergence** — watch for sourDough L1 `platform_link()` pattern, converge when ready
3. **Coverage push** toward 90% (compiler backends are main gap)

---

*coralReef Wave 157a. G68 L1 evolved (symlink_file on Windows). 4 prod files
with std::os::unix, zero L2/L3 exposure. Cross-arch 15/15 PASS. Depot ready.
3,672 tests, zero unsafe, zero clippy warnings on Linux + Windows.*
