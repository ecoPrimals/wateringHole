# skunkBat v0.2.0-dev — Neural API Self-Registration Implemented

**Date**: May 4, 2026
**From**: skunkBat team
**To**: primalSpring, Songbird, biomeOS, ecosystem
**Triggered by**: primalSpring Phase 58 debt handoff (Neural API registration gap)

---

## Summary

skunkBat now self-registers with the discovery service on startup, following the
`PRIMAL_SELF_REGISTRATION.md` v1.0 pattern. On IPC bind, skunkBat probes for
a discovery provider and sends `ipc.register` with its ID, capabilities, and
endpoint. Standalone-safe: if no discovery service exists, continues without error.

---

## What Was Implemented

### Self-Registration Module (`ipc/registration.rs`)

- Follows the three-step probe sequence:
  1. `DISCOVERY_SOCKET` env var
  2. `{BIOMEOS_SOCKET_DIR}/discovery-{FAMILY_ID}.sock`
  3. `{BIOMEOS_SOCKET_DIR}/discovery.sock`
- Sends `ipc.register` with:
  - `primal_id`: `"skunkbat"`
  - `capabilities`: `["security", "baseline", "metadata", "response", "lineage", "health"]`
  - `endpoint`: UDS path (preferred) or TCP fallback
- 3-second timeout; fires-and-forgets in a spawned task
- Logs `info` on success (virtual endpoint), `debug` on unavailable

### Capabilities Registered

The 6 capabilities map to skunkBat's composable domains:

| Capability | Domain |
|-----------|--------|
| `security` | Aggregate tag for semantic routing |
| `baseline` | Statistical anomaly detection |
| `metadata` | Network fingerprinting / OS detection |
| `response` | Graduated defense state machine |
| `lineage` | Genetic trust verification (BearDog delegation) |
| `health` | Primal liveness / health checks |

### Integration Point

Called from `ipc::serve()` after both TCP and UDS listeners bind, before entering
`tokio::select!` loop. Uses the existing `skunk_bat_integrations::rpc::call_uds`
RPC client — no new dependencies.

---

## Audit Response (Phase 58)

| Finding | Resolution |
|---------|-----------|
| Phase 3 transport encryption (HIGH) | **Already shipped** (prior handoff) |
| Neural API registration (MEDIUM) | **DONE** — this handoff |
| Thymic selection (LOW) | Blocked on BearDog `lineage.list` integration |
| Coverage 89.6% → 90% (LOW) | **92.02%** lines / 90.81% functions — closed |

---

## Deep Debt Evolution (same session)

| Item | Before | After |
|------|--------|-------|
| `server.rs` | 945 lines (tests inline) | **322L** prod + **478L** extracted `server_tests.rs` (DRY helpers) |
| `derive_session_keys` | `.expect()` panics | `Result<_, TransportError::Crypto>` — zero panics |
| Provider hardcoding | `"beardog"` literal default | `"btsp"` capability-based (agnostic) |
| `handle_negotiate` | 107 lines (clippy violation) | Under 100 via `negotiate_error()` helper |
| Threat type counts | Mixed 4/5 across showcase | **5** everywhere (Intrusion added) |
| Demo counts | 16/22 (stale) | **21** (actual `demo.sh` count) |
| Stale references | `docs/DEPLOYMENT.md`, `--features beardog-integration` | Removed/fixed |
| Workspace version | `0.1.0` vs `0.2.0-dev` narrative | **0.2.0-dev** unified |
| Spec versions | "0.1.0 (Draft)" | **0.2.0-dev** (implemented specs) |

---

## Build Health

| Metric | Value |
|--------|-------|
| Tests | 332 passing / 0 failures / 15 ignored |
| Coverage | 92.02% lines, 90.81% functions (cargo-llvm-cov) |
| Clippy | CLEAN (pedantic + nursery, `-D warnings`) |
| Format | CLEAN |
| Docs | CLEAN |
| Deny | CLEAN |
| Source files | 42 |
| Max file | 790 lines (`negotiate.rs`, test-inclusive) |
| Version | 0.2.0-dev |

---

## Remaining from Phase 58

- **Thymic selection**: blocked on BearDog `lineage.list` IPC endpoint
- **Network defense execution**: needs OS/firewall abstraction
- All integration tests are `#[ignore]`-gated and ready to activate
