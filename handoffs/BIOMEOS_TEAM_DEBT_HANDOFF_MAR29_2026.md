# biomeOS Team Debt Handoff

**Date:** 2026-03-29
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

## Blocking (ship / integration risk)

### B-1: Graph Rollback Is a No-Op

`GraphExecutor::rollback()` only logs and returns success. Graph execution is
forward-only despite `rollback_on_failure` being a configurable option.

**Location:** `crates/biomeos-atomic-deploy/src/neural_executor.rs` (~507-516)
**Impact:** Failed graph deployments cannot be automatically recovered
**Effort:** High — requires checkpoint storage, reverse operations, state tracking
**Note:** Comment says "Future Enhancement" — design is sketched but not implemented

### B-2: DNS-Based Discovery Not Implemented

DNS discovery path is logged as "not implemented."

**Location:** `crates/biomeos-core/src/universal_biomeos_manager/discovery.rs` (~424)
**Impact:** Blocks DNS-based primal resolution (enterprise/cloud patterns)
**Effort:** Medium

### B-3: Remote Primal Acquisition Returns Errors

GitHub/remote binary download in `primal_registry` returns errors. Primals must
be pre-deployed locally or via plasmidBin.

**Location:** `crates/biomeos-core/src/primal_registry/mod.rs` (~319, ~325)
**Impact:** No automatic binary fetch during graph deployment
**Effort:** Medium — HTTP client + checksum verification + plasmidBin integration

### B-4: Federation Manifest Deployment Not Implemented

Custom federation manifest deployment returns "not yet implemented."

**Location:** `crates/biomeos-federation/src/modules/manifest.rs` (~113)
**Impact:** Blocks programmatic federation configuration
**Effort:** Medium

---

## Significant (architecture, ops, or quality)

### S-1: Neural API Handler Depth Varies

The routing table in `routing.rs` (~82-212) is comprehensive — graphs, topology,
niches, lifecycle, protocol, capabilities, inference, MCP, agents, mesh. But some
routes are thin wrappers around `capability.call` while others have deep
implementations. A team should audit handler depth per domain.

**Location:** `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs`
**Action:** Create a coverage matrix: route name -> handler -> depth (full/thin/stub)

### S-2: Superficial Health Check in One Path

`node_health_check_all` treats socket file existence under `SOCKET_DIR` as health
signal without JSON-RPC probing. The NUCLEUS startup path does real JSON-RPC
health checks — this is only the deploy-graph path.

**Location:** `crates/biomeos-atomic-deploy/src/neural_executor_node_impls.rs` (~79-122)
**Impact:** Graph deploy may report "healthy" for primals that have sockets but aren't responding
**Effort:** Low — add JSON-RPC probe fallback

### S-3: Harvest Tool GitHub Path Placeholder

The `harvest` tool's GitHub acquisition path prints "not yet implemented."

**Location:** `tools/harvest/src/main.rs` (~497)
**Impact:** Cannot harvest binaries from GitHub releases via the tool
**Effort:** Medium

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

## Recommended Priority Order

1. **S-2:** Add JSON-RPC health probe to deploy-graph health check path (low effort, high value)
2. **M-1:** Fix eprintln -> tracing (trivial)
3. **B-3:** Implement remote primal acquisition from plasmidBin GitHub releases
4. **B-1:** Design graph rollback/checkpoint architecture
5. **S-1:** Audit Neural API handler depth per domain
6. **B-2:** Implement DNS-based discovery
7. **B-4:** Federation manifest deployment
