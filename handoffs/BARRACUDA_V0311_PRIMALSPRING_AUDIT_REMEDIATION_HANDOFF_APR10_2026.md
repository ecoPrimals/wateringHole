# barraCuda v0.3.11 — Sprint 39: primalSpring Audit Remediation + Deep Debt Sweep

**Date**: 2026-04-10
**Scope**: BTSP full handshake, GPU panic fix, SIGSEGV profile gap, musl rebuild, 7-axis deep debt sweep
**Tests**: 4,422 pass / 0 fail / 14 skip

---

## Audit Items Resolved

### 1. BTSP Phase 2 Full Handshake (was: session-only guard)

**Problem**: `guard_connection()` called BearDog `btsp.session.create` per accept
but did not perform full X25519 challenge-response on the client stream. The guard
authenticated sessions but the handshake was incomplete.

**Fix**: Evolved `guard_connection()` from zero-arg fire-and-forget to
`guard_connection<S>(stream: &mut S)` with full 6-step handshake relay:

1. Read `ClientHello` from client (2s timeout for legacy fallback)
2. Forward `client_ephemeral_pub` to BearDog via `btsp.session.create`
3. Relay `ServerHello` (server ephemeral pub + challenge) to client
4. Read `ChallengeResponse` (HMAC proof) from client
5. Forward to BearDog via `btsp.session.verify`
6. Relay `HandshakeComplete` (session_id + cipher) to client

**Legacy compatibility**: If client doesn't send `ClientHello` within 2s (legacy
JSON-RPC client), or sends a non-`ClientHello` message, the guard degrades
gracefully and accepts the connection with a warning log.

**Files changed**:
- `crates/barracuda-core/src/ipc/btsp.rs` — full rewrite
- `crates/barracuda-core/src/ipc/transport.rs` — all 3 accept loops updated
- `crates/barracuda-core/tests/btsp_socket_compliance.rs` — tests updated

### 2. BC-GPU-PANIC (was: server panics on GPU-less machines)

**Problem**: `Auto::new()` called `test_pool::get_test_device()` which used
`.expect("No test device available")` — panicking when no adapter was available.
`BarraCudaPrimal::start()` had a graceful `Err(e)` path but it was dead code
because `Auto::new()` always returned `Ok(...)`.

**Fix**: Decoupled `Auto::new()` from the test pool entirely. Production path now:
1. Try `WgpuDevice::new()` (GPU, HighPerformance preference)
2. Fallback to `WgpuDevice::new_cpu_relaxed()` (software rasterizer)
3. Return `Err` if both fail

`BarraCudaPrimal::start()` already handled `Err` with graceful degradation:
- `PrimalState::Running` with `device = None`
- `health_status()` returns `Degraded { reason: "No GPU device available" }`
- `capabilities.list` reflects `hardware.gpu_available: false`
- All JSON-RPC methods that require device return proper error responses

Test code continues to use `test_pool::get_test_device()` for shared device pooling.

**Files changed**:
- `crates/barracuda/src/device/mod.rs` — `Auto::new()` rewritten

### 3. fault_injection SIGSEGV Profile Gap

**Problem**: `gpu-serial` override (max-threads=1) only existed for `ci` and
`default` nextest profiles. The `stress` profile (128 threads) and `gpu` profile
(8 threads) had no serialization, meaning `cargo nextest run --profile stress`
or `--profile gpu` could hit Mesa llvmpipe race conditions.

**Fix**: Added `gpu-serial` overrides to both `stress` and `gpu` profiles with
the same binary filter as `ci`/`default`.

**Files changed**:
- `.config/nextest.toml` — 2 new `[[profile.*.overrides]]` sections

### 4. Musl-Static Rebuild

Fresh binaries built after all fixes:
- x86_64-unknown-linux-musl: static-pie, 5,092,256 bytes, SHA256 `71003d8a...`
- aarch64-unknown-linux-musl: static, 3,998,104 bytes, SHA256 `af77cf52...`

**Files changed**:
- `../../infra/plasmidBin/barracuda/metadata.toml` — checksums, sizes, build_ref

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all --check` | PASS |
| `cargo clippy --workspace --all-features -- -D warnings` | PASS |
| `cargo doc --workspace --all-features --no-deps` | PASS |
| `cargo deny check` | PASS |
| `cargo nextest run --workspace --all-features` | 4,422 pass / 14 skip |

---

## What Remains for BTSP Phase 2 (Ecosystem-Wide)

barraCuda's handshake implementation is complete and will activate when:
- BearDog's `btsp.session.create` returns `server_ephemeral_pub` + `challenge`
  (currently may return session-only response — guard degrades gracefully)
- BearDog's `btsp.session.verify` accepts HMAC proof and returns `verified: true`
- Clients implement `ClientHello` / `ChallengeResponse` wire messages

Until then, the legacy fallback path ensures zero disruption.

---

## Deep Debt Sweep — 7-Axis Audit

### 5. Hardcoded Primal Names → Domain-Agnostic

**Problem**: `btsp.rs` used `beardog_*` function names (`discover_beardog_socket`,
`beardog_rpc`, `beardog_session_create`, `beardog_session_verify`). Runtime discovery
was already capability-based (`SECURITY_DOMAIN = "crypto"`), but identifiers encoded
coupling to a specific primal name.

**Fix**: All identifiers renamed to domain-agnostic equivalents:
- `discover_beardog_socket` → `discover_security_provider`
- `beardog_session_create` → `session_create_rpc`
- `beardog_session_verify` → `session_verify_rpc`
- `beardog_rpc` → `security_provider_rpc`
- `beardog_sock` → `provider_sock`
- `BearDogUnavailable` → `ProviderUnavailable`
- All doc comments updated to say "security-domain provider" instead of "BearDog"

**Result**: Zero hardcoded primal names in production code.

### 6. Comprehensive Audit Results (clean bill)

| Axis | Status | Detail |
|------|--------|--------|
| **Dependencies** | CLEAN | All direct deps pure Rust. No `build.rs`, no `-sys` crates, no FFI. `blake3` `pure` feature active. |
| **Large files** | CLEAN | All production files under 800L. Largest non-barrel: `invocation.rs` 753L (cohesive naga IR interpreter). |
| **Unsafe code** | CLEAN | 1 irreducible: `barracuda-spirv` wgpu SPIR-V passthrough. All others test-only. |
| **Hardcoding** | FIXED | Zero primal names in production. Capability-based discovery via `crypto` domain. |
| **Self-knowledge** | CLEAN | No imports from sibling primals. Runtime discovery only. |
| **Mocks** | CLEAN | All mocks in `#[cfg(test)]` only. |
| **Idioms** | CLEAN | Zero `#[allow(`, `todo!()`, `.unwrap()` in prod, `println!` in lib, `Box<dyn Error>` in sigs. |

### 7. Debris Audit

- Zero `.bak`/`.orig`/`.swp`/`.tmp`/`.log`/`.DS_Store` files
- Zero empty files
- Zero `TODO`/`FIXME`/`HACK`/`XXX` comments in `crates/**/*.rs`
- Zero `todo!()`/`unimplemented!()`
- Zero tracked test artifacts (lcov, profraw, junit)
- `showcase/**/Cargo.lock` files are `.gitignore`d (local-only)
- All spec dates refreshed to April 10, 2026
- All root doc dates and test counts synchronized
