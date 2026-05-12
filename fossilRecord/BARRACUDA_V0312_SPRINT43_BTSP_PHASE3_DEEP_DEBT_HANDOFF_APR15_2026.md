# barraCuda v0.3.12 — Sprint 43 Handoff (BTSP Phase 3 + Deep Debt Evolution)

**Date**: April 15, 2026
**Sprint**: 43 (Phase 3 encryption) + 43b (deep debt evolution)
**Version**: 0.3.12
**Tests**: 4,393+ passed, 0 failures
**IPC Methods**: 32 registered
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT42_FULL_DEEP_DEBT_HANDOFF_APR12_2026.md` (archived)

---

## What Changed

### Sprint 43: BTSP Phase 3 Post-Handshake Stream Encryption

1. **BtspCipher + BtspSession types** — `BtspCipher` enum (Null/HmacPlain/ChaCha20Poly1305),
   `BtspSession` struct carrying session_id + cipher + session_key. `BtspOutcome::Authenticated`
   now carries `BtspSession` instead of bare `session_id`.

2. **BtspFrameReader/BtspFrameWriter** — Length-prefixed frame I/O per
   `BTSP_PROTOCOL_STANDARD.md` §Wire Framing. 4-byte big-endian length prefix, 16 MiB max
   frame size. Cipher-suite-dependent payload format:
   - `BTSP_NULL`: raw JSON-RPC plaintext
   - `BTSP_HMAC_PLAIN`: plaintext ‖ HMAC-SHA256(32)
   - `BTSP_CHACHA20_POLY1305`: nonce(12) ‖ ciphertext ‖ tag(16)

3. **Pure Rust crypto** — `chacha20poly1305 0.10`, `hmac 0.12`, `sha2 0.10`, `base64ct 1.6`
   (RustCrypto ecosystem). Counter-based nonce generation (4 zero bytes ‖ 8-byte BE counter).
   All new deps banned by `deny.toml` from having C/FFI equivalents — aligns with ecoBin pure-Rust chain.

4. **Transport integration** — `handle_btsp_connection` for encrypted framing on TCP and
   UDS accept loops. Automatic cipher routing: non-null cipher → `BtspFrameReader/Writer`,
   null/dev/degraded → existing NDJSON `handle_connection` with consumed-line replay.

5. **BufReader lifetime fix** — Single `BufReader` across entire handshake relay with
   `get_mut()` for writes. Previous code created two separate `BufReader` instances,
   risking buffered data loss between Steps 1 and 4 of the handshake relay.

6. **14 new frame tests** — Roundtrip for all 3 ciphers, tamper detection (HMAC + ChaCha),
   wrong-key rejection, multi-frame sequences, EOF handling, frame-too-large rejection,
   line adaptor roundtrip. 20 total BTSP tests pass.

7. **primalSpring audit items resolved**:
   - plasma_dispersion feature-gate verified (Sprint 40 dual gate `gpu+domain-lattice`)
   - 18/18 neuralSpring V131 shader absorption candidates confirmed upstream
     (per-shader audit table in `SPRING_ABSORPTION.md`; 29 total = 18 candidates
     + 6 neuralSpring-specific + wildcard expansion)
   - Provenance registry path fixed for `batch_ipr` (`special/` → `spectral/`)

### Sprint 43b: Deep Debt Evolution

8. **Smart WGSL refactoring** — `math_f64.wgsl` 840→725 lines. 10 fossil functions
   + Newton-Raphson `sqrt_f64` extracted to `math_f64_fossils.wgsl` (134L). `asin_f64`
   evolved from fossil `sqrt_f64()` to native `sqrt()` (probe-confirmed on all SHADER_F64
   hardware). Fossil→active dependency edge eliminated.

9. **biomeos namespace hardcoding evolved** — `ECOSYSTEM_SOCKET_NAMESPACE` (discovery.rs)
   and `ECOSYSTEM_SOCKET_DIR` (transport.rs) evolved from public constants to private
   defaults with `BIOMEOS_SOCKET_DIR` env var override. All 4 discovery function call
   sites updated. Integration test adapted.

10. **HMAC expect elimination** — 2 `expect("HMAC accepts any key size")` in `btsp_frame.rs`
    evolved to `map_err` with typed `BtspFrameError::AuthFailed`. `compute_hmac` return
    type evolved from `Vec<u8>` to `Result<Vec<u8>, BtspFrameError>`.

11. **12-axis deep debt audit clean bill**:

| Dimension | Finding |
|-----------|---------|
| Files > 800 LOC (Rust) | All under 800L (max: 783L `tests.rs`) |
| Files > 800 LOC (WGSL) | `math_f64.wgsl` 840→725L (refactored) |
| `unsafe` code | 1 site (barracuda-spirv wgpu passthrough, documented) |
| TODO/FIXME/HACK | Zero |
| `Result<T, String>` | Zero in production |
| `println!` in library | Zero |
| Mocks in production | Zero (all test-isolated) |
| External deps | All pure Rust (`deny.toml` enforced) |
| Hardcoded primal names | Zero in runtime code |
| `unwrap()`/`expect()` in production | 6 ownership-invariant expects (pool.rs/guard.rs); zero in crypto/IO |
| Python/C benchmarks | None in-tree; Kokkos parity bench operational |
| Build artifacts | Clean (no stray .o/.so/.a outside target/) |

---

## Files Changed

### New files
- `crates/barracuda-core/src/ipc/btsp_frame.rs` — Frame I/O with encryption
- `crates/barracuda/src/shaders/math/math_f64_fossils.wgsl` — Extracted fossils

### Modified files
- `crates/barracuda-core/src/ipc/btsp.rs` — BtspCipher, BtspSession, handshake relay
- `crates/barracuda-core/src/ipc/mod.rs` — Re-exports for frame types
- `crates/barracuda-core/src/ipc/transport.rs` — Encrypted connection handler + routing
- `crates/barracuda-core/src/ipc/transport_tests.rs` — Updated constant references
- `crates/barracuda-core/tests/btsp_socket_compliance.rs` — Updated imports
- `crates/barracuda/Cargo.toml` — Crypto workspace deps
- `crates/barracuda-core/Cargo.toml` — Crypto deps
- `crates/barracuda/src/shaders/math/math_f64.wgsl` — Fossils extracted, asin_f64 evolved
- `crates/barracuda/src/shaders/precision/polyfill.rs` — 3-file preamble inclusion
- `crates/barracuda/src/shaders/provenance/registry.rs` — batch_ipr path fix
- `crates/barracuda/src/device/coral_compiler/discovery.rs` — Env-overridable namespace
- `crates/barracuda/src/device/coral_compiler/mod.rs` — Updated re-exports

---

## For primalSpring

All 4 primalSpring audit items from the post-Phase 43 blurb are resolved:
1. ✅ BTSP Phase 3 stream encryption — operational with all 3 cipher suites
2. ✅ `plasma_dispersion` feature-gate — verified correct (Sprint 40)
3. ✅ 18/18 neuralSpring shader absorption — per-shader audit in `SPRING_ABSORPTION.md`
4. ✅ `BufReader` lifetime edge-case — fixed (single instance + `get_mut()`)

## For BearDog

BTSP Phase 3 integration is complete on the barraCuda side. The handshake relay now:
- Parses `cipher` and `session_key` from `btsp.session.verify` response
- Relays `HandshakeComplete` with the actual cipher name
- Routes authenticated connections through `BtspFrameReader/Writer` for encrypted I/O
- Falls back to NDJSON for Null cipher / dev mode / degraded connections

## For All Teams

- `BIOMEOS_SOCKET_DIR` env var is now respected in both `barracuda` (discovery) and
  `barracuda-core` (transport) crates. Ecosystem namespace is no longer hardcoded.
- All quality gates remain green. No breaking API changes.
