# ecoPrimals Ecosystem Blurb — Cross-Arch First

**Date**: Aug 7, 2026 7:30AM | **Wave**: 156w | **From**: eastGate overwatch
**Posture**: **WINDOWS FIRST. skunkBat CROSS-ARCH CLEAN.** 4 primals still fail Windows. We fix all 15/15 clean across musl + Windows, rebuild depot once, deploy everywhere at once. strandGate + westGate atomic composition learnings feed back into patterns.

---

## WHY WINDOWS FIRST

Deploying musl while Windows is broken means another rebuild after fixes land. Every partial deploy is a tail-chase. The composition patterns we're building (atomics, cross-gate systems, springs) need to work everywhere once — not "mostly everywhere, except."

strandGate and westGate have been actively using primal compositions in production. Their atomic patterns (Tower, provenance trio, node atomic) are the template for all gates. If the primals those atomics compose from can't build cross-arch, the composition can't either.

**Fix once. Build once. Deploy everywhere.**

---

## 5 PRIMALS — SPECIFIC VIOLATIONS

### coralReef (biomeGate)

| File | Violation | Fix |
|------|-----------|-----|
| `local_transport.rs:46-47` | `std::os::unix::net::UnixStream::connect` in prod | Use G66 `connect_transport()` |
| `local_transport.rs:92` | Direct `tokio::net::UnixListener::bind` | Use G66 `TransportListener` |
| `local_transport.rs:138` | `std::os::unix::fs::symlink` | `#[cfg(unix)]` guard |
| `server_lifecycle.rs:132` | `tokio::signal::unix::SignalKind` unguarded | `#[cfg(unix)]` + `#[cfg(windows)] ctrl_c()` |
| `cmd_server_process.rs` (test) | Direct `UnixStream::connect` | `#[cfg(unix)]` on test |
| `tests_ecosystem.rs` (test) | Direct `UnixListener::bind` | `#[cfg(unix)]` on tests |
| **musl issue** | `ipc` module behind test cfg but `connect_local()` references it | Export `ipc::transport` types outside test cfg |

### petalTongue (overwatch)

| File | Violation | Fix |
|------|-----------|-----|
| `jsonrpc_integration_tests.rs` (test) | Direct `UnixListener`/`UnixStream` (6+ fns) | `#[cfg(unix)]` on entire test module |
| `jsonrpc_provider/tests.rs` (test) | Direct `UnixListener`/`UnixStream` (6+ fns) | `#[cfg(unix)]` on test fns |

### ~~skunkBat (eastGate)~~ — **FIXED W156w**

~~All violations resolved.~~ `TarpcUdsServer` + tests `#[cfg(unix)]` gated. `rpc.rs` was already clean. `cargo check --target x86_64-pc-windows-gnu` PASSES — zero warnings, zero errors. 648 tests.

### squirrel (eastGate)

| File | Violation | Fix |
|------|-----------|-----|
| `security.rs:282` | `std::os::unix::fs::PermissionsExt` | `#[cfg(unix)]` guard |
| `security_tests.rs:411` | `PermissionsExt` in test | `#[cfg(unix)]` guard |
| `capability_jwt.rs:557,625` | `UnixListener::bind` in prod code | `#[cfg(unix)]` or use transport |
| `capability_jwt_integration_tests.rs` | Full UDS mock server | `#[cfg(unix)]` on test module |

### toadStool (biomeGate)

| File | Violation | Fix |
|------|-----------|-----|
| `unix_socket_provider.rs:30,90` | `UnixStream::connect` in prod | Use G66 `TransportStream` |
| `tarpc_server/connection.rs:73-75` | `UnixStream` in fn signature | Abstract to `TransportStream` |
| `tarpc_server/mod.rs:139` | Direct `UnixListener` | Use `TransportListener` |
| `unibin/execution.rs:313,526` | `UnixListener` + `tokio::signal::unix` | Transport + signal guards |
| `akida-setup/` verification + permissions | `PermissionsExt` | `#[cfg(unix)]` (neuromorphic is unix-only hardware) |
| `akida-driver/io.rs:25` | `std::os::unix::io::AsFd` | `#[cfg(unix)]` |

---

## PRE-PUSH STANDARD — NON-NEGOTIABLE

```bash
cargo check --target x86_64-pc-windows-gnu
```

If the target isn't installed: `rustup target add x86_64-pc-windows-gnu`

**Every push must pass this.** The compiler enforces silicon neutrality. Code teams: run this locally before pushing. Depot team: reject bins that fail cross-arch.

---

## LEARNINGS FROM STRANDGATE + WESTGATE

strandGate and westGate have been running full atomic compositions in production:
- **Tower Atomic** (bearDog + songBird + skunkBat) — security mesh
- **Provenance Trio** (rhizoCrypt + loamSpine + sweetGrass) — data braiding
- **Node Atomic** (toadStool + barraCuda + coralReef) — compute/GPU

These composition patterns are the reusable template for all gates. Once cross-arch is clean, the same atomic definitions work on any gate without platform-specific surprises. The learnings from strandGate (compute memoization, NPU) and westGate (data braiding, multi-tier CAS) feed back into the patterns that every gate inherits.

---

## SEQUENCE — AFTER CROSS-ARCH CLEARS

1. **Code teams fix 4 remaining primals** — specific violations above (skunkBat DONE)
2. **All 15 pass `cargo check --target x86_64-pc-windows-gnu`** (11/15 done)
3. **Depot rebuild** — musl 16/16 + Windows 15/15
4. **Single clean deploy** — all gates at once
5. **Verify health** — 13/13 on sporeGate, other gates
6. **Springs + downstream** — compositions on clean foundation

---

## BACKGROUND — CONTINUING

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | ChunkedBraid. AlphaFold. Multi-tier CAS. Atomic compositions LIVE. | Running |
| **strandGate** | SU(N) grid. arXiv 40/42. Observable battery 69/69. NPU + compute memo. | Running |
| **whitePaper** | petalTongue-native figures replacing matplotlib pipeline. | Evolving |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| G64 + G65 + G66 | **COMPLETE** (pattern 15/15) |
| Cross-arch (Windows) | **11/15 pass** — skunkBat fixed, 4 primals remain |
| Musl depot | **16/16 on golgi** |
| sporeGate health | **12/13 alive** |
| Gates online | **11** |
| Primal tests | **~140,000+** |

---

*Wave 156w — **WINDOWS FIRST.** No partial deploys. skunkBat cross-arch CLEAN (648 tests). 4 primals remain (coralReef, petalTongue, squirrel, toadStool) with specific violations listed. Code teams clear these, verify with `cargo check --target x86_64-pc-windows-gnu`, then single clean depot rebuild + deploy. 14 COMPLETE / 25 ACTIVE / 23 GLACIAL. 62 goals. 15/15 GREEN.*
