# biomeOS Team Debt Handoff

**Date:** 2026-03-29 (updated: biomeOS v2.78 resolved all blocking debt)
**From:** primalSpring ecosystem audit
**To:** Dedicated biomeOS team
**Scope:** All known debt categorized by severity and type

---

## Context

biomeOS is the composition primal — it orchestrates all other primals via the
Neural API. Its debt profile is different from BearDog/Songbird: most gaps are
in orchestration features (rollback, remote acquisition, federation manifests)
rather than core crypto or network protocol.

The Dark Forest gate is real and functional. NUCLEUS CLI mode works end-to-end
with socket-based health checks. Neural API routing table covers 26 domains
with 290+ translations.

---

## Blocking — ALL RESOLVED in v2.78

### B-1: Graph Rollback — RESOLVED

Real checkpoint/restore with reverse topological `lifecycle.stop` + `capability.unregister`.
**Location:** `crates/biomeos-atomic-deploy/src/neural_executor.rs` — `save_checkpoint_before_phase()`, `restore_from_checkpoint()`, `rollback()`

### B-2: DNS-Based Discovery — RESOLVED

mDNS/DNS-SD (RFC 6762) over `_biomeos._tcp.local` with SRV/TXT parsing, health probes, and LAN fallback.
**Location:** `crates/biomeos-core/src/universal_biomeos_manager/discovery/dns_sd.rs` (663 lines)

### B-3: Remote Primal Acquisition — RESOLVED

GitHub releases (curl subprocess) + HTTP downloads (hyper pure Rust) + SHA256 verification + XDG cache.
**Location:** `crates/biomeos-core/src/primal_registry/remote.rs` (337 lines)

### B-4: Federation Manifest Deployment — RESOLVED

YAML manifest parsing, topology validation (acyclic trust graph), per-gate JSON-RPC `federation.configure` + `federation.join`.
**Location:** `crates/biomeos-federation/src/modules/manifest.rs` (555+ lines)

---

## Significant (architecture, ops, or quality)

### S-1: Neural API Handler Depth Varies

The routing table in `routing.rs` (~82-212) is comprehensive — graphs, topology,
niches, lifecycle, protocol, capabilities, inference, MCP, agents, mesh. But some
routes are thin wrappers around `capability.call` while others have deep
implementations. A team should audit handler depth per domain.

**Location:** `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs`
**Action:** Create a coverage matrix: route name -> handler -> depth (full/thin/stub)

### S-2: Superficial Health Check in One Path — RESOLVED in v2.78

Deploy-graph health path evolved from socket-existence to real JSON-RPC
`health.liveness` probes with 3s timeout.

**Location:** `crates/biomeos-atomic-deploy/src/neural_executor_node_impls.rs`

### S-3: Harvest Tool GitHub Path — RESOLVED in v2.78

GitHub acquisition implemented — curl + asset matching + SHA256 checksum + manifest provenance.

**Location:** `tools/harvest/src/main.rs`

### S-4: Large Ignored Test Surface

Clusters of `#[ignore]` tests requiring specific environments:

| Category | Location | Needs |
|----------|----------|-------|
| BearDog lineage | `crates/biomeos-federation/tests/genetic_lineage_tests.rs` | Running BearDog |
| Spring niche E2E | `crates/biomeos-atomic-deploy/tests/spring_niche_deploy_e2e.rs` | Full stack |
| Tower Atomic E2E | `crates/biomeos-atomic-deploy/tests/tower_atomic_e2e.rs` | BearDog + Songbird |
| Provenance trio E2E | `crates/biomeos-atomic-deploy/tests/provenance_trio_e2e.rs` | Trio running |
| Cross-spring pipeline | `crates/biomeos-atomic-deploy/tests/cross_spring_pipeline_e2e.rs` | Multiple springs |
| Rootfs build | `tests/integration/rootfs_build.rs` | Sudo |
| Discovery/HTTP | `crates/biomeos-core/tests/*` | Various |
| Niche integration | `crates/biomeos-manifest/tests/niche_integration_tests.rs` | Graph format updates |

**Action:** Plan staged CI; document which suites are release gates vs optional

### S-5: Interactive Mode Not Supported

Universal biomeOS manager interactive mode via atomic client is flagged as
"not yet supported."

**Location:** `crates/biomeos-core/src/universal_biomeos_manager/runtime.rs` (~299)

### S-6: Chimera Builder Generated Stubs

`biomeos-chimera` generates capability-forwarding stubs with stub errors on miss.
Intentional pattern but still a "generated surface" maintenance cost.

**Location:** `crates/biomeos-chimera/src/builder.rs`, `fusion.rs`

---

## Minor

### M-1: eprintln in Library Code

One `eprintln!` in non-test library code when capability registry config is missing.

**Location:** `crates/biomeos-atomic-deploy/src/capability_domains.rs` (~780)
**Action:** Replace with `tracing::warn!` (fixing in this session)

### M-2: VM Federation Test Placeholders

VM federation tests are explicit placeholders needing a VM harness.

**Location:** `tests/e2e/vm_federation.rs`

### M-3: Niche Integration Tests Pending Graph Format Updates

Tests depend on graph format changes not yet landed.

**Location:** `crates/biomeos-manifest/tests/niche_integration_tests.rs`

---

## Positive Signals

- Zero `TODO`/`FIXME`/`HACK` markers
- Zero `unsafe` in production code
- Zero clippy warnings
- `CONTEXT.md` and `README.md` current
- Dark Forest gate is real (not stubbed) — `dark_forest_gate.rs` with token verification
- NUCLEUS CLI mode works end-to-end: socket wait + JSON-RPC health + lifecycle manager
- Neural API routing covers 26 domains
- 7,202 tests, 90%+ llvm-cov coverage
- Socket discovery has a well-documented 5-8 step resolution order

---

## Recommended Priority Order (post-v2.78)

All blocking and S-2/S-3 items resolved. Remaining priorities:

1. **S-1:** Audit Neural API handler depth per domain (coverage matrix)
2. **S-4:** Plan staged CI for ignored test suites
3. **S-5:** Interactive mode support
4. **M-3:** Niche integration tests pending graph format updates
