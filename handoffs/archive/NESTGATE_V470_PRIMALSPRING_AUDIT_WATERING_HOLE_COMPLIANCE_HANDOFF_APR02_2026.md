# NestGate v4.7.0-dev — primalSpring Audit Resolution, wateringHole Compliance & Deep Debt Evolution

**Date**: April 2, 2026  
**Primal**: nestgate (storage & permanence)  
**Session type**: primalSpring audit execution, wateringHole standards compliance, deep debt evolution, production mock elimination, NUCLEUS boundary enforcement  
**Supersedes**: NESTGATE_V470_DEEP_DEBT_COMPLETION_TRAIT_INJECTION_HANDOFF_APR02_2026.md

---

## Session Summary

Full execution on all primalSpring audit findings (NG-01 through NG-04), wateringHole standards compliance review and alignment, deep debt evolution across the entire workspace. Session covered: deprecated API cleanup, zero-copy evolution, production mock elimination, capability-based hardcoding replacement, REST deprecation, dependency trimming, `#![allow]` reduction, NUCLEUS boundary enforcement via discovery module deprecation, UniBin IPC compliance, health triad alignment, docs reconciliation, and debris cleanup.

---

## What Was Done

### primalSpring Audit Resolution

| Audit Item | Resolution |
|------------|-----------|
| NG-01: metadata backend in-memory default | `FileMetadataBackend` with XDG disk persistence (`$XDG_DATA_HOME/nestgate/metadata/`); `SemanticRouter::new()` defaults to disk with in-memory fallback |
| NG-02: session.\* not dispatched | Full `session.save/load/list/delete` handlers wired in `SemanticRouter` using `StorageBackend` + `MetadataBackend` |
| NG-03: data.\* still stubs | Evolved to delegation pattern (same as crypto.\*); removed from `capabilities.list` — NestGate is storage, not data |
| NG-04: compile broken | Already fixed in prior session; verified clean |
| Docs claim zero warnings | All docs reconciled with measured state and dated |

### wateringHole Compliance

| Standard | Action |
|----------|--------|
| UNIBIN v1.2: `server --port` | `--port` now starts TCP newline JSON-RPC alongside Unix socket; `server` is alias for `daemon` |
| CAPABILITY_BASED_DISCOVERY v1.1 | `storage.sock` → `nestgate.sock` symlink created in `biomeos/` dir with guard cleanup |
| SEMANTIC_METHOD_NAMING v2.0 | Health triad aligned: `health.liveness` (lightweight version probe), `health.readiness` (backend check), `health.check` (full status) |
| PRIMAL_IPC_PROTOCOL v3.1 | TCP + UDS dual transport when `--port` provided |
| STANDARDS_AND_EXPECTATIONS | Zero TODO/FIXME/HACK in committed code (was 15, now 0); `#![forbid(unsafe_code)]` on all 22 crates |

### Deprecated API Cleanup

- Removed primal-name struct fields and env var lookups (`beardog_url`, `songbird_url`, etc.) from `ServicesConfig` and `capability_helpers`
- Removed `BearDogClient` vendor type alias
- Evolved `ZeroCostFileStorage` from fake data to deprecation errors
- Evolved `stream_placeholder()` from fake text to proper 501 JSON-RPC error
- Replaced `DefaultHasher` cert fingerprint stub with real SHA-256 via `sha2`

### Zero-Copy Evolution

- `StorageBackend` trait: `Vec<u8>` → `bytes::Bytes` for `store_object`/`retrieve_object`
- `InMemoryStorageBackend` stores/returns `Bytes` directly (no allocation on retrieve)
- Single boundary conversion at tarpc wire edge only

### Production Mock Elimination

| Mock | Resolution |
|------|-----------|
| ZFS automation actions (fake `success: true`) | Compression/snapshot execute real `zfs` commands; others return honest `success: false` |
| REST snapshot handlers (fake data) | Return 501 NOT_IMPLEMENTED |
| `DevelopmentLoadBalancer` public export | Gated behind `#[cfg(any(test, feature = "dev-stubs"))]` |
| Storage detection placeholder probes | Documented as intentional placeholders with tests |

### Dependency Evolution

- Removed unused `pin-project` (zero usages found)
- Collapsed `futures` facade → `futures-util` across 8+ crates
- Consolidated `rand` → `fastrand` in `nestgate-api`
- `async-trait` justified: still required for `dyn StorageBackend`/`dyn MetadataBackend`

### NUCLEUS Boundary Enforcement

| Crate | LOC | Verdict | Action |
|-------|-----|---------|--------|
| `nestgate-discovery` | 24.6K | High overstep | `discovery_mechanism`, `service_discovery`, `orchestration` deprecated with notes pointing to Songbird/biomeOS |
| `nestgate-network` | 7.6K | Moderate | Documented; orchestration naming flagged |
| `nestgate-security` | 6.6K | Low-moderate | Correctly delegates to BearDog |
| `nestgate-automation` | 3.9K | Low | Storage lifecycle — NestGate's domain |
| `nestgate-installer` | 3.5K | Process/ecoBin | No C deps in Cargo.toml (uses system `curl`) |

### REST Deprecation

- Module-level deprecation notice on `nestgate-api/src/rest/mod.rs`
- `#[deprecated]` on 25+ REST handler functions pointing to JSON-RPC/tarpc

### `#![allow]` Reduction

- Removed blanket `#![allow(missing_docs)]` from `nestgate-core`
- Narrowed `#![allow(deprecated)]` in `nestgate-storage`, `nestgate-cache`, `nestgate-automation` to item-level with reason strings
- 7 targeted `#[expect(clippy::too_long_first_doc_paragraph)]` with reasons
- Zero TODO comments in `code/crates/` — replaced with `reason = "..."` on `#[allow(deprecated)]`

### Debris Cleanup

- Removed `tests/mdns_discovery_integration_tests.rs` (empty fossil placeholder)
- Archived headers added to `docs/guides/TESTING.md` and `TESTING_MODERN.md`
- Safety header added to `scripts/setup-test-substrate.sh`
- All TODO/FIXME/HACK markers removed from .md files

---

## Measured State

```
cargo fmt --check                                          PASS
cargo clippy --workspace --all-targets --all-features      PASS (0 warnings)
cargo doc --workspace --no-deps                            PASS (0 warnings)
cargo test --workspace                                     PASS (0 failures)
cargo check --workspace --all-targets --all-features       PASS
#![forbid(unsafe_code)]                                    All 22 crates
Files > 1000 lines                                         0 (largest: 733 LOC)
TODO/FIXME/HACK in code/crates/**/*.rs                     0
TODO/FIXME/HACK in *.md                                    0
Coverage (llvm-cov, excl test/bench/fuzz)                  ~80% line
```

---

## Remaining Work

- **Coverage 90% target**: At 80%; remaining gap in ZFS system-command execution paths and `unwrap-migrator` tool
- **Discovery extraction**: Deprecated modules should eventually be extracted to Songbird/shared crate
- **`nestgate-installer` ecoBin placement**: Move to ecoBin repo or document exception
- **aarch64 musl**: Not yet validated (x86_64 only in current CI)
- **`async-trait` migration**: Blocked on `dyn Trait` usage; remove when static dispatch refactor happens

---

## Key Files Modified

### New files
- `code/crates/nestgate-rpc/src/rpc/semantic_router/session.rs` — session handlers
- `code/crates/nestgate-rpc/src/rpc/metadata_backend.rs` — `FileMetadataBackend`
- `code/crates/nestgate-zfs/src/zero_cost_zfs_operations/manager/tests.rs` — ZFS ops tests

### Major changes
- `code/crates/nestgate-bin/src/cli.rs` — TCP JSON-RPC `--port` wiring
- `code/crates/nestgate-bin/src/commands/service.rs` — dual transport daemon
- `code/crates/nestgate-rpc/src/rpc/isomorphic_ipc/tcp_fallback.rs` — `start_bound` for fixed-port TCP
- `code/crates/nestgate-rpc/src/rpc/socket_config.rs` — domain symlink + guard
- `code/crates/nestgate-rpc/src/rpc/semantic_router/health.rs` — health triad alignment
- `code/crates/nestgate-rpc/src/rpc/semantic_router/data.rs` — delegation pattern
- `code/crates/nestgate-rpc/src/rpc/semantic_router/capabilities.rs` — data.\* removed
- `code/crates/nestgate-rpc/src/rpc/storage_backend.rs` — `Bytes` zero-copy
- `code/crates/nestgate-discovery/src/lib.rs` — NUCLEUS scope docs + deprecations
- `code/crates/nestgate-config/src/config/runtime/services.rs` — primal-name fields removed
- `code/crates/nestgate-discovery/src/primal_discovery/capability_helpers.rs` — legacy env removed
- `code/crates/nestgate-security/src/cert/utils.rs` — SHA-256 fingerprint
- `code/crates/nestgate-zfs/src/automation/actions.rs` — honest action results

---

## Pointers

- README: `/path/to/ecoPrimals/primals/nestgate/README.md`
- STATUS: `/path/to/ecoPrimals/primals/nestgate/STATUS.md`
- CHANGELOG: `/path/to/ecoPrimals/primals/nestgate/CHANGELOG.md`
