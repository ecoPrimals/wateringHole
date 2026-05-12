# Songbird Team Debt Handoff

**Date:** 2026-03-29
**From:** primalSpring ecosystem audit
**To:** Dedicated Songbird team
**Scope:** All known debt categorized by severity and type

---

## Recent Fixes (this session)

- `SONGBIRD_DARK_FOREST`, `SONGBIRD_ACCEPT_LEGACY_BIRDSONG`, and `SONGBIRD_DUAL_BROADCAST`
  env vars now wired into `BirdSongConfig` construction in `discovery_startup.rs`
  (all three struct literals updated from `..Default::default()`)

---

## Blocking (ship / integration risk)

### B-1: BearDog beacon.try_decrypt_with_id Dependency

A Dark Forest integration test is explicitly ignored until BearDog exposes
`beacon.try_decrypt_with_id`. This blocks multi-beacon decryption testing.

**Location:** `crates/songbird-discovery/tests/dark_forest_integration_tests.rs` (~246-255)
**Impact:** Dark Forest multi-beacon path untested end-to-end
**Dependency:** BearDog Phase 1 work
**Action:** Track as cross-team dependency; unblock when BearDog delivers

### B-2: Discovery Runtime Backends Not Implemented

DNS-SD, Consul, etcd, and Kubernetes discovery backends return structured
`NotImplemented` errors. Only env-based, static, and mDNS discovery work.

**Location:** `crates/songbird-config/src/discovery/runtime_engine.rs`
**Impact:** Blocks enterprise/k8s deployment patterns
**Effort:** High per backend — each is a separate integration
**Note:** Failures are explicit and structured, not silent

### B-3: Hardware Attestation Verification

Trust escalation via hardware attestation is not implemented.
BTSP/provider `verify_attestation` path returns placeholder.

**Location:** `crates/songbird-orchestrator/src/trust/escalation.rs`
**Impact:** No hardware-rooted trust for high-security deployments
**Effort:** High — requires BearDog HSM integration

### B-4: Registry Service API Stubs

`ServiceRegistry`/`ServiceInfo` API not fully implemented. Tests are stubs.

**Location:** `crates/songbird-registry/tests/service_registration_comprehensive_tests.rs`
**Impact:** Service registration via IPC incomplete
**Effort:** Medium

---

## Significant (architecture, ops, or quality)

### S-1: 269 Ignored Tests

`CONTEXT.md` reports 11,471 tests with 269 ignored. Categories:
- BearDog/Neural API/live orchestrator required
- Unix socket/STUN/Tor/Bluetooth hardware
- Universal adapter API gaps (rollback, circuit breaker)
- Expensive chaos tests
- Config scanner (external hardcoding scanner)

**Action:** Plan staged CI with fixtures: `cargo test -- --ignored` with per-suite env

### S-2: Universal Capability Adapter Gaps

- `execute_with_rollback` not implemented
- `start_workflow`/`resume_workflow`/persistence not implemented
- No circuit breaker API on `UniversalCapabilityAdapter`

**Location:** `crates/songbird-universal/tests/integration_workflow_tests.rs`,
`crates/songbird-universal/tests/error_handling_comprehensive_tests.rs`
**Impact:** Reliability patterns incomplete

### S-3: Tor Onion Service Placeholders

Introduction point handling and descriptor publishing are placeholders,
pending BearDog signing/encryption wiring.

**Location:** `crates/songbird-tor-protocol/src/onion_service/introduction.rs`,
`crates/songbird-tor-protocol/src/onion_service/descriptor.rs`
**Dependency:** BearDog signing

### S-4: Stub Implementations (Intentional Degradation)

These return errors or no-ops when their dependency is absent:

| Stub | Location | When Active |
|------|----------|-------------|
| `NoOpBearDogProvider` | `crates/songbird-network-federation/src/beardog/noop.rs` | BearDog unavailable |
| Security setup placeholder | `crates/songbird-orchestrator/src/app/security_setup.rs` | No security provider |
| Execution agent shell | `crates/songbird-execution-agent/src/server.rs` | Placeholder |
| Static discovery watch | `crates/songbird-discovery/src/abstraction/adapters/static_adapter.rs` | Watch path |
| Sovereignty adapter | `crates/songbird-universal/src/sovereignty/adapter.rs` | Federation |
| Bluetooth legacy | `crates/songbird-genesis/src/physical_channels/bluetooth.rs` | Redirects to bluetooth_pure |
| SoloKey FIDO2 | `crates/songbird-genesis/src/physical_channels/solokey.rs` | Hardware absent |

### S-5: Dark Forest Mock Uses XOR

In-process tests use `MockDarkForestProvider` with XOR, not production
ChaCha20-Poly1305. Validates flow, not crypto strength.

**Location:** `crates/songbird-discovery/tests/dark_forest_integration_tests.rs`
**Action:** Add a test with real BearDog provider when available

---

## Minor

### M-1: Hardcoded Default Ports

`crates/songbird-config/src/config/hardcoded_elimination.rs` centralizes
default port construction (8080 family). Env-overridable but worth reviewing
for deployments.

### M-2: Non-Linux Platform Gaps

Network interface enumeration on non-Linux bails with partial behavior.
`crates/songbird-orchestrator/src/network/binding.rs`

### M-3: Websocket State Placeholder

`crates/songbird-orchestrator/src/server/websocket_api.rs` (~351) uses `0`
as placeholder for a value that could live in `FederationState`.

---

## Positive Signals

- Zero `TODO`/`FIXME`/`HACK` markers
- Federation coordinator is implemented (not stubbed) — `FederationCoordinator`
  with IPC, rendezvous, join, heartbeats, health
- Dark Forest broadcaster/listener fully branching on config flags
- `CONTEXT.md` and `README.md` current and detailed
- 11,471 tests (269 ignored — structured, not random)

---

## Recommended Priority Order

1. **S-1:** Plan staged ignored-test CI with BearDog/orchestrator fixtures
2. **B-1:** Coordinate with BearDog on `beacon.try_decrypt_with_id`
3. **S-2:** Implement universal adapter rollback/circuit breaker
4. **B-4:** Complete service registry API
5. **B-2:** Implement DNS-SD backend (most requested enterprise path)
6. **S-3:** Wire Tor onion service when BearDog signing is ready
