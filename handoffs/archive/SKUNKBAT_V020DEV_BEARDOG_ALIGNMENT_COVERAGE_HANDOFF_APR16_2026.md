<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# skunkBat v0.2.0-dev — BearDog IPC Alignment & Coverage Push

**Date**: April 16, 2026
**Primal**: skunkBat
**Version**: 0.2.0-dev
**Previous**: SKUNKBAT_V010_PRIMALSPRING_AUDIT_DEEP_DEBT_HANDOFF_APR16_2026.md (archived)

---

## Session Summary

Three-phase evolution: (1) BearDog v0.9.0 IPC surface analysis revealing
parameter mismatches between skunkBat's BTSP handshake and BearDog's canonical
RPC types; (2) alignment of all method names, parameter shapes, and response
fields; (3) spec documentation evolution and coverage push to 89.6%.

## Build

| Metric | Value |
|--------|-------|
| Tests | 171 passing / 0 failures / 15 ignored (external-primal-gated) |
| Coverage | 89.6% line (cargo-llvm-cov; CI gate: 85%) |
| Clippy | CLEAN — pedantic + nursery, `-D warnings`, zero warnings |
| Format | PASS |
| Docs | PASS — zero warnings |
| Deny | PASS — advisories ok, bans ok, licenses ok, sources ok |
| Unsafe | `forbid(unsafe_code)` workspace-wide |
| Files | 28 `.rs` source files, 7,288 lines total, max 867 lines |
| Edition | 2024 |
| License | AGPL-3.0-or-later (scyBorg triple-copyleft) |

## Changes

### BearDog v0.9.0 IPC Surface Alignment

Thorough exploration of the BearDog codebase revealed several mismatches
between skunkBat's BTSP handshake assumptions and BearDog's actual v0.9.0
implementation. All corrected:

| Field | Before (wrong) | After (aligned) |
|-------|----------------|-----------------|
| Create method | `btsp.session.create` | `btsp.server.create_session` |
| Verify method | `btsp.session.verify` | `btsp.server.verify` |
| Negotiate method | `btsp.negotiate` | `btsp.server.negotiate` |
| Seed param | `family_seed_ref: "env:FAMILY_SEED"` | `family_seed: <base64>` |
| Session ref | `session_id` everywhere | `session_token` (create), `session_id` (verify) |
| Verify params | `session_id`, `challenge`, `client_response` | `session_token`, `client_ephemeral_pub`, `response`, `preferred_cipher` |
| Negotiate params | `session_id`, `preferred_cipher`, `bond_type` | `session_token`, `cipher` |
| Challenge gen | skunkBat via `rand_u128()` | BearDog generates (returned in create response) |

Removed dead code: `rand_u128()`, `challenge`/`server_ephemeral_pub` fields
from `HandshakeState`.

### Consumed Capabilities Update

`dispatch.rs` `capabilities.list` response now correctly advertises:
- `btsp.server.verify`
- `genetic.verify_lineage`
- `capabilities.list`
- `federation.broadcast`
- `discovery.find_by_capability`

### Spec Evolution

- **THYMIC_SELECTION_SPEC.md**: BearDog contract table lists canonical method
  names; notes `genetic.verify_lineage` for roster building; documents that
  `lineage.list` is not a BearDog server-side RPC
- **COMPOSABLE_PRIMITIVES_SPEC.md**: `lineage.verify` delegates to
  `genetic.verify_lineage` with correct param shapes; consumed capabilities
  updated
- **THREAT_DETECTION_SPEC.md**: Thymic section references `btsp.server.verify`
  and `genetic.verify_lineage`

### Coverage: 84.7% → 89.6%

New mock UDS provider tests exercise the full BTSP handshake path without
requiring a live BearDog instance:
- `provider_call_success` — mock UDS server, JSON-RPC success
- `provider_call_rpc_error` — mock UDS server, JSON-RPC error propagation
- `handshake_exchange_with_mock_provider` — full 6-step handshake, mock
  BearDog responds to create/verify/negotiate
- `handshake_verify_failure` — verify rejection path, error frame sent

`btsp.rs` coverage: 51% → 90%. New `test_beardog_capabilities` integration
test exercises real BearDog binary when `BEARDOG_BIN` env is set.

### Root Documentation

- `README.md`: Updated feature list (composable primitives, thymic model),
  consumed capabilities section, test/coverage numbers, specs listing
- `CONTEXT.md`: Added composable primitives table, thymic selection section,
  BearDog method names, updated test/status numbers

## Remaining Work

- **Coverage 89.6% → 90%+**: `ipc/mod.rs` (74 lines, server startup) and
  `transport/mod.rs` (163 lines, listeners) are 0% — require live socket tests
- **Thymic Selection**: Design spec complete; implementation blocked on live
  BearDog `genetic.verify_lineage` integration testing
- **T9/T10**: musl-static cross-compile and plasmidBin submission
- **Self-registration**: `capability.register` with ToadStool on startup

## For Other Teams

- **BearDog**: skunkBat now uses canonical `btsp.server.*` method names and
  correct parameter shapes (`session_token`, `family_seed`, `preferred_cipher`).
  Legacy `btsp.session.*` aliases no longer used.
- **No wire changes**: JSON-RPC responses unchanged. All callers unaffected.
- **No new dependencies**: Workspace dep set unchanged.
- **Integration test ready**: `BEARDOG_BIN=path/to/beardog cargo test --test integration_beardog -- --ignored`

## Verification

```bash
cargo fmt --all -- --check
cargo clippy --workspace -- -D warnings
cargo test --workspace
cargo doc --workspace --no-deps
cargo deny check
cargo llvm-cov --workspace
```

All gates green as of this handoff.
