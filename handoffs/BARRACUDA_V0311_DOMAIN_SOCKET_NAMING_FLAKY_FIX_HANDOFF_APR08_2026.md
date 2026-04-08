# barraCuda v0.3.11 — Sprint 36: Domain-Based Socket Naming & Flaky Test Serialization

**Date**: April 8, 2026
**Primal**: barraCuda
**Version**: 0.3.11
**Supersedes**: BARRACUDA_V0311_DEEP_DEBT_TYPED_ERRORS_TRANSPORT_REFACTOR_HANDOFF (archived)

---

## Summary

Sprint 36 evolves barraCuda's socket naming from primal-based to domain-based
per `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §3, and serializes the `three_springs_tests`
integration suite to prevent Mesa llvmpipe SIGSEGV under concurrent GPU access.

## Changes

### Domain-Based Socket Naming

Per §3: primals bind using their **capability domain stem**, not their primal name.

| Before | After |
|--------|-------|
| `barracuda.sock` | `math.sock` |
| `barracuda-{fid}.sock` | `math-{fid}.sock` |

- New `PRIMAL_DOMAIN = "math"` constant alongside existing `PRIMAL_NAMESPACE`
- `default_socket_path()` uses `PRIMAL_DOMAIN` for socket naming
- Legacy `barracuda.sock → math.sock` symlink created on startup, removed on shutdown
- `identity.get` and `primal.capabilities` domain field: `"compute"` → `"math"`
- CLI help text updated to reflect new naming

### Flaky Test Serialization

- `three_springs_tests` binary added to `gpu-serial` nextest group (`max-threads = 1`)
- Same mitigation as `fault_injection`, `fhe_chaos_tests`, etc.
- Root cause: Mesa llvmpipe thread safety under concurrent wgpu device access

### BTSP Phase 2 Status

BearDog shipped server-side BTSP handshake (Wave 31: `perform_server_handshake`,
X25519 + HMAC-SHA256 challenge-response, ChaCha20-Poly1305 cipher negotiation).
However, `btsp.session.*` JSON-RPC methods are still stub-style — server secrets
not persisted by session token. barraCuda BTSP Phase 2 (handshake-as-a-service
client) remains **blocked** on BearDog completing the RPC session layer.

## BTSP Compliance Checklist

```
Socket Naming:
  [x] Reads FAMILY_ID from environment (3-tier precedence)
  [x] Creates math-{family_id}.sock when FAMILY_ID is set
  [x] Creates math.sock when FAMILY_ID is not set (development)
  [x] Refuses to start when both FAMILY_ID and BIOMEOS_INSECURE are set
  [x] Legacy barracuda.sock symlink for backward compatibility

Handshake (Phase 2+):
  [ ] BTSP handshake on incoming connections — BLOCKED on BearDog session RPC
  [ ] Challenge-response family verification
  [ ] Ephemeral X25519 per connection

Cipher Negotiation (Phase 2+):
  [ ] ChaCha20-Poly1305 — BLOCKED
  [ ] Length-prefixed framing — BLOCKED
```

## Files Changed

- `crates/barracuda-core/src/lib.rs` — `PRIMAL_DOMAIN` constant
- `crates/barracuda-core/src/ipc/transport.rs` — domain socket, legacy symlink
- `crates/barracuda-core/src/ipc/mod.rs` — doc update
- `crates/barracuda-core/src/ipc/methods/primal.rs` — domain field
- `crates/barracuda-core/src/rpc.rs` — domain field
- `crates/barracuda-core/src/bin/barracuda.rs` — symlink lifecycle
- `crates/barracuda-core/tests/btsp_socket_compliance.rs` — updated assertions
- `.config/nextest.toml` — three_springs_tests gpu-serial

## Quality Gates

- **4,207 tests** pass, 0 fail, 14 skipped
- `cargo fmt --all --check` — clean
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` — clean
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` — clean
