# BearDog v0.9.0 — Wave 22: Deep Debt Evolution — Hot-Path Clones, iOS Fake Crypto, Mock Cleanup

**Date**: March 28, 2026
**Primal**: BearDog
**Version**: 0.9.0
**Coverage**: 90.05% line | 89.22% region | 84.84% function
**Tests**: 15,100+ passing, 0 failures

---

## Context

Continued deep debt resolution after Wave 21's StrongBox HSM abstraction, self-knowledge renames, and 90%+ coverage milestone. This wave focused on hot-path performance, security-critical stub fixes, production mock label cleanup, and documentation hygiene.

---

## What Changed

### Hot-Path `serde_json::Value` Clone Elimination

**File**: `crates/beardog-tunnel/src/unix_socket_ipc/handlers/crypto_handler/genetic.rs`

Genetic RPC handlers previously cloned the entire `serde_json::Value` per request on a hot path. Refactored to accept `&serde_json::Value` and use `Deserialize::deserialize(params)` for zero-copy deserialization from borrowed data.

### iOS safe_ffi: Fake Crypto → Proper Errors

**File**: `crates/beardog-tunnel/src/tunnel/hsm/safe_ffi/ios_safe.rs`

Placeholder crypto implementations returned "fake success" — zeroed signatures, length-only verification, hardcoded key bytes. These were a security risk: callers would receive `Ok(...)` for operations that never actually executed cryptographic work.

All stubs now return `Err(BearDogError::not_implemented("iOS Secure Enclave: Phase 2"))`. The `test_secure_enclave_availability_check` test was marked `#[serial]` to prevent env-var race conditions during parallel workspace test runs.

### Production Mock Label Cleanup

- `mobile_setup.rs`: `"(mock)"` → `"(software fallback)"` — accurate for what the software HSM actually is
- `universal_adapter/core.rs`: Removed stale "Mock processing" comment (real `Instant` timing has been in place since Wave 20)

### Example Binary Evolution

- `integration_api_demo.rs` and `genetics_evolution_demo.rs`: `Box<dyn Error>` → `anyhow::Result<()>`
- `anyhow` added as dev-dependency to `beardog-genetics/Cargo.toml`

### Socket Path Centralization

`doctor.rs` updated to use `DEFAULT_SOCKET_PATH` constant for default primal socket discovery, eliminating the last inline socket path string.

### InMemoryStorageBackend Documentation

`software_hsm/types.rs`: Documented the ephemeral, no-op semantics of the in-memory storage backend with a `///` doc comment.

### TCP NDJSON Read Timeout (Wave 21 carry-over)

- `multi_transport.rs` line 418: `lines.next_line().await` wrapped with `tokio::time::timeout(Duration::from_secs(30), ...)` — drops idle connections instead of holding them indefinitely
- `registry_client.rs`: Client-side `read_line` also wrapped with 30s timeout

### Documentation & Cleanup

- `STATUS.md` and `CHANGELOG.md` updated with Wave 22 entry
- Per-crate coverage date corrected to March 28, 2026
- `beardog-ipc/README.md`: Fixed broken `../../wateringHole/` relative links; genericized "Songbird" references to "orchestrator"
- `deploy.sh` archived to `fossilRecord/beardog/scripts/` (referenced non-existent Helm chart)
- `scripts/README.md` updated to reflect deployment script archival

---

## Dependency Audit

| Check | Result |
|-------|--------|
| `ring` in tree | None |
| `openssl-sys` in tree | None |
| `sled` in tree | None |
| `unsafe` blocks | 0 (`forbid(unsafe_code)` workspace-wide) |
| `blake3` C deps | Inert — `pure` feature active |
| Files > 1000 LOC | 0 |
| Active TODO/FIXME in .rs | 0 |

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy -D warnings` | Pass (0 warnings) |
| `cargo test --workspace` | Pass (15,100+ tests, 0 failures) |
| `cargo llvm-cov` | 90.05% line coverage |
| AGPL-3.0 / scyBorg triple license | Compliant |
| ecoBin (zero C on non-Android) | Compliant |

---

## Remaining Debt (Known)

- **iOS Secure Enclave**: Phase 2 implementation needed when iOS FFI target is prioritized
- **deploy.sh equivalent**: When deployment automation is needed, build from current architecture (no stale scaffolding)
- **Old HSM traits**: 5 legacy trait hierarchies have migration doc comments pointing to `HsmKeyProvider`; removal planned for v0.10.0

---

## For primalSpring

Wave 22 resolves all concrete debt items from the composition experiment handoff. TCP read timeouts are now on all NDJSON sites (both server and client). Hot-path clone on genetic RPC handler is eliminated. No fake crypto success paths remain in any HSM stub.
