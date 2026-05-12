<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- Copyright (c) 2026 ecoPrimals. All rights reserved. -->

# BearDog v0.9.0 — Wave 18-20: Deep Debt Evolution, 90% Coverage, Semantic Naming

**Date**: March 28, 2026
**Primal**: BearDog (cryptographic service provider)
**Version**: v0.9.0
**Tests**: 15,085+ passing (0 failures)
**Coverage**: 90.03% line | 89.18% region | 84.90% function (llvm-cov workspace)
**All Gates Green**: fmt, clippy `-D warnings`, doc, build, test

---

## Summary

Three concentrated waves (18, 19, 20) resolved all deep debt from the March 27 comprehensive audit, hit the 90% line coverage target, and evolved semantic method naming to align with wateringHole standards.

---

## Wave 18: Deep Audit Execution (March 27-28)

### UniBin v1.1 Standalone Identity Compliance

- `PrimalIdentity::from_env()` evolved from hard-fail to infallible standalone fallback
- Added `is_standalone: bool` field and `is_standalone()` accessor
- All callers updated (beardog-cli, beardog-tunnel)
- Primals now start cleanly without orchestrator environment variables

### primalSpring Composition Fixes

- **TCP read timeout**: All NDJSON read sites (`tcp_ipc/server.rs`, `unix_socket_ipc/server.rs`, `ipc_server.rs`) wrapped with `tokio::time::timeout(30s)`. Idle connections from probes (`nc`, `curl`) now time out instead of blocking forever.
- **NDJSON wire format documented**: README transport section explains NDJSON framing. Capability metadata includes `wire_format: "ndjson"` and `protocol: "jsonrpc-2.0"`.

### Clippy/Fmt/Doc Regression Fixes

- `absurd_extreme_comparisons` (usize `>= 0`)
- `float_cmp` (floating-point assertions)
- `unfulfilled_lint_expectations` (#[expect(dead_code)] on pkcs11 fields)
- `unused_mut` (3 benchmark files)
- `await_holding_lock` (deploy coverage tests)
- HTML tag in doc comment escaped
- `large_stack_frames` threshold raised for test harness

### Code Cleanup

- Orphan files deleted: `ai_powered_analysis.rs` (682 LOC), `quantum_optimizations.rs` (633 LOC)
- Commented-out code removed from 15+ files
- Showcase `#[allow(dead_code)]` replaced with `_` prefixes + `#[serde(rename)]`
- Songbird IPC registration added (best-effort, non-fatal)

---

## Wave 19: Semantic Naming + Coverage Push (March 28)

### Semantic Method Naming Evolution

Added primary `domain.operation` names per SEMANTIC_METHOD_NAMING_STANDARD.md:

| Domain | Primary Names | Backward-Compat Aliases |
|--------|--------------|------------------------|
| Security | `birdsong.encrypt`, `birdsong.decrypt` | `beardog.birdsong.*` |
| BTSP | `btsp.contact.exchange`, `btsp.tunnel.*` | `beardog./btsp/...` |
| Crypto | `crypto.derive_onion_address` | `beardog.crypto.*` |
| Health | `health.liveness` | `beardog.ping` |
| Capabilities | `capabilities.list` | `beardog.capabilities` |

Method list tests enforce semantic names appear before aliases.

### Coverage Push (+138 Tests)

- beardog-tunnel: modes/server, doctor, tls12_dot, tls_ops, software_hsm, ios_safe
- beardog-types: security/authorization, discovery/providers, workflow/retry, ipc_discovery
- beardog-core: ecosystem_storage/operations, production adapter

---

## Wave 20: 90% Coverage Target Met (March 28)

### Coverage Push (+200 Tests)

Targeted the highest missed-line files across 11 crates:

- **beardog-tunnel**: multi_transport, crypto manager, audit storage, diagnostics, zero-cost HSM
- **beardog-genetics**: metrics, evolution engine, interaction capture types
- **beardog-integration**: UPA client, heartbeat
- **beardog-types**: health monitoring, network client, key management discovery, workflow, AI config, discovery builder, capabilities, PKCS#11, system/math constants, HSM discovery, config implementations
- **beardog-core**: network discovery, performance optimizer, universal discovery types, crypto service types, serving/deployment types, external functions
- **beardog-errors**: android error types
- **beardog-auth**: genetics impl
- **beardog-discovery**: announcements

### Clippy Issues Resolved

- `redundant_clone` on atomic types and configs
- `io_other_error` (use `Error::other()` instead of `Error::new(ErrorKind::Other, ...)`)
- `into_iter` on single-element collections (use `HashMap::from([...])`)
- `manual RangeInclusive::contains`
- `drop()` on non-Drop types
- Unit-value `let` bindings

---

## Metrics Progression

| Metric | Wave 17 | Wave 18 | Wave 19 | Wave 20 |
|--------|---------|---------|---------|---------|
| Tests | 14,600+ | 14,756+ | 14,894+ | **15,085+** |
| Line Coverage | 87.31% | 88.07% | 88.46% | **90.03%** |
| Region Coverage | — | 88.77% | 89.19% | **89.18%** |
| Function Coverage | — | 83.68% | 84.06% | **84.90%** |

---

## Remaining Work (Low Priority)

| Item | Status | Notes |
|------|--------|-------|
| `Box<dyn Error>` migration | Deferred | 425 instances, internal trait boundaries, not public API |
| Binary entrypoint coverage | N/A | `main.rs` files (cli, tunnel, deploy, installer) can't be unit-tested |
| `modes/server.rs` coverage | 52% | Async networking code, hard to unit-test without integration harness |
| CI scaffold cleanup | Noted | `.github/workflows/` aspirational files reference scripts that don't exist |

---

## Cross-Primal Notes

### For Songbird

BearDog now attempts Songbird IPC registration at server startup. If Songbird's registry socket is not found, BearDog logs the absence and continues in standalone mode. Registration includes capabilities: `Crypto`, `BTSP`, `Ed25519`.

### For biomeOS

Wire format is now explicitly `ndjson` in capability metadata. Callers can read `wire_format` from the `capabilities.list` response to confirm framing requirements.

### For All Primals

- Semantic method names (`domain.operation`) are now primary; `beardog.*` prefixes are backward-compatible aliases
- NDJSON framing: every request must be a single JSON-RPC object terminated by `\n`
- Idle connections time out after 30 seconds (TCP and Unix socket)
- `PrimalIdentity` works without orchestrator env vars (standalone mode)

---

**BearDog**: 100% Pure Rust | AGPL-3.0-only | 90% Coverage | 15,085+ Tests | Production Ready
