# rhizoCrypt — Wave 141b: Architecture Split + Coverage Expansion

**Date**: Jul 15, 2026 | **Commit**: `adbf83d`
**Tests**: 1,894 → 1,911 (+17) | **Files**: 213 → 217 `.rs`

## Changes

### Architecture: method_gate.rs Smart Split (790L → 468L + 334L)

The `CapabilityVerifier` subsystem (`TokenVerifier` trait, `PresenceVerifier`,
`NoopVerifier`, `CapabilityVerifier`, parse/extract/expiry helpers) extracted
into `method_gate_verifier.rs`. Public API unchanged via `pub use verifier::*`.
Motivated by the 800L threshold — file was at 790L and growing.

### Magic Numbers → Named Constants (5 replacements)

| File | Magic | Constant |
|------|-------|----------|
| `provenance/types.rs` | `300` | `DEFAULT_PROVENANCE_CACHE_TTL_SECS` |
| `compute/types.rs` | `1000` | `DEFAULT_EVENT_BUFFER_SIZE` (reused) |
| `rate_limit.rs` | `10000/1000/100` | `DEFAULT_RATE_LIMIT_DEV_{READ,WRITE,EXPENSIVE}_RPS` |
| `prometheus.rs` | `4096` | `PROMETHEUS_BUFFER_CAPACITY` |

### Test Extraction: Inline → External Modules

- `permanent.rs`: 650L → 260L (−390L, 22 tests → `permanent_tests.rs`)
- `provenance/client.rs`: 589L → 268L (−321L, 17 tests → `client_tests.rs`)

### Core-Layer Coverage: branch_ops + vertex_ops (+17 tests)

New `rhizocrypt_tests_branch_vertex.rs` covers:
- **branch_ops** (11): branch/diff/merge/federate paths + error cases
- **vertex_ops** (6): query by type/agent/limit, merkle root, proof success/not-found

Previously only tested indirectly through JSON-RPC handler tests.

## Gate Results

- `cargo fmt --all --check` — clean
- `cargo clippy --workspace --all-features -- -D warnings` — zero warnings
- `cargo test --workspace --all-features` — 1,911 passed, 0 failed
- `RUSTDOCFLAGS="-D warnings" cargo doc` — clean
