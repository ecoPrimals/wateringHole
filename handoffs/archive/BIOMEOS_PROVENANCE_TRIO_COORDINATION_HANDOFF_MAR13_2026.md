# biomeOS Provenance Trio + Ecosystem Coordination Handoff

**Date**: March 13, 2026
**Author**: biomeOS + sweetGrass teams
**Status**: Active
**Scope**: Cross-primal coordination, ISSUE resolution, RootPulse evolution

---

## Summary

Comprehensive coordination pass across the Provenance Trio (rhizoCrypt + LoamSpine +
sweetGrass), biomeOS Neural API, Spring ecosystem, and RootPulse workflow graphs.
Four SPRING_EVOLUTION_ISSUES resolved, RootPulse extended with branch/merge/diff/federate
workflows, and cross-Spring pipeline testing infrastructure created.

---

## Changes Made

### 1. ISSUE-003 RESOLVED: capability.call Parameter Format Standardized

**Files changed**:
- `crates/biomeos-atomic-deploy/src/handlers/capability.rs`
- `crates/biomeos-spore/src/beacon_genetics/capability.rs`

**Canonical format**: `{ "capability": "domain", "operation": "method", "args": {...} }`

Backward-compatible:
- Dotted sugar: `{ "capability": "domain.method", "args": {...} }` splits on first dot
- `"params"` accepted as alias for `"args"` for older callers

`NeuralApiCapabilityCaller` updated to emit canonical format. Two new tests added.

### 2. ISSUE-001 RESOLVED: Ecology Domain Already in Registry

Confirmed: `[domains.ecology]` with 30+ translations already present in
`config/capability_registry.toml` since biomeOS v2.33. No code changes needed.

### 3. ISSUE-007 RESOLVED: Spring-as-Provider Pattern Documented

**File created**: `wateringHole/SPRING_AS_PROVIDER_PATTERN.md`

Comprehensive guide covering:
- Socket binding convention
- `capability.register` call format with semantic mappings
- Incoming request handling
- Deploy graph node template
- Registry configuration template
- Current registration status of all Springs

### 4. ISSUE-004 RESOLVED: Cross-Spring Pipeline Tests Created

**Files created**:
- `graphs/cross_spring_soil_microbiome.toml` — airSpring soil → wetSpring diversity → provenance
- `crates/biomeos-atomic-deploy/tests/cross_spring_pipeline_e2e.rs` — 4 E2E tests
- `soil-microbiome` niche template registered

### 5. Provenance Trio E2E Test Infrastructure

**Files created**:
- `crates/biomeos-atomic-deploy/tests/provenance_trio_e2e.rs` — 5 E2E tests
  - Health checks for all trio primals
  - Capability registration verification
  - Full RootPulse commit flow (create session → dehydrate → sign → store → commit → attribute → verify)
  - Graph execution test via `graph.execute(rootpulse_commit)`
  - Niche deployment test via `niche.deploy("rootpulse")`
- `scripts/test_provenance_trio_e2e.sh` — convenience runner

### 6. ludoSpring ContinuousExecutor Wiring + CLI

**Files changed**:
- `config/capability_registry.toml` — added `game.tick_logic`, `game.tick_physics` translations
- `graphs/ludospring_deploy.toml` — added tick capabilities to `capabilities_provided`

**Files created**:
- `crates/biomeos/src/modes/continuous.rs` — new `biomeos continuous` CLI mode

The `game_engine_tick.toml` continuous graph already existed with 60Hz tick loop.
These changes wire the full path from CLI to primal:

1. **`biomeos continuous graphs/game_engine_tick.toml`** — new CLI subcommand loads a
   continuous coordination graph and runs it in a real-time tick loop
2. **IPC node executor** — each tick dispatches node capabilities to primals via
   JSON-RPC over Unix domain sockets. Socket resolution follows wateringHole
   `UNIVERSAL_IPC_STANDARD_V3` priority: `BIOMEOS_SOCKET_DIR` > XDG > `/tmp`
3. **Feedback edges** — physics → game-logic collision feedback injected as `_feedback`
   param on next tick
4. **Budget enforcement** — per-node time budgets from the graph; cached output reuse
   on overrun (handled by `ContinuousExecutor` in `biomeos-graph`)
5. **Dry run** — `biomeos continuous --dry-run graphs/game_engine_tick.toml` shows the
   full pipeline with capabilities, primals, budgets, and feedback edges
6. **Graceful shutdown** — Ctrl-C sends `SessionCommand::Stop`
7. **11 unit tests** — socket resolution, param building with/without feedback, JSON-RPC
   roundtrip against mock server, graph validation, dry-run mode

### 7. RootPulse Branch/Merge/Diff/Federate Graphs

**Files created**:
- `graphs/rootpulse_branch.toml` — fork history at a commit point
- `graphs/rootpulse_merge.toml` — merge a branch spine into a target
- `graphs/rootpulse_diff.toml` — compare two commits, produce structured diff
- `graphs/rootpulse_federate.toml` — synchronize provenance across peer nodes

**Niche templates registered** (5 new):
- `rootpulse-branch`, `rootpulse-merge`, `rootpulse-diff`, `rootpulse-federate`, `soil-microbiome`

Total niche templates: 20 (was 15)

---

## Test Results

- **biomeos-atomic-deploy**: 131 capability tests pass, 11 niche tests pass
- **biomeos-spore**: 14 beacon_genetics capability tests pass
- All E2E tests compile and are gated behind `#[ignore]` for CI (require running primals)
- Full `cargo check` clean across workspace

---

## No API Changes

All changes are backward-compatible. The `capability.call` handler accepts all
three formats (canonical, dotted, params-alias). No breaking changes to any
existing graph or primal interface.

---

## SPRING_EVOLUTION_ISSUES Status

| Issue | Title | Status |
|-------|-------|--------|
| ISSUE-001 | Ecology Domain Missing | **RESOLVED** |
| ISSUE-002 | Sync Neural API Client | OPEN |
| ISSUE-003 | capability.call Format | **RESOLVED** |
| ISSUE-004 | Cross-Primal Pipeline | **RESOLVED** |
| ISSUE-005 | Safe UID Discovery | OPEN |
| ISSUE-006 | NPU Convergence | OPEN |
| ISSUE-007 | Spring-as-Provider | **RESOLVED** |
| ISSUE-008 | ET₀ GPU Promotion | OPEN |
| ISSUE-009 | Benchmark Schema | OPEN |
| ISSUE-010 | Cross-Spring Data Flow | OPEN |
| ISSUE-011 | GPU f64 Cancellation | OPEN |

---

### 8. biomeOS RootPulse CLI + Coverage Push

**Files created**:
- `crates/biomeos/src/modes/rootpulse.rs` — `biomeos rootpulse --session-id ... --agent-did ...`
  sends `graph.execute(rootpulse_commit)` via Neural API Unix socket

**Coverage progress**: biomeOS workspace line coverage pushed from 69.9% to 73.64%.
Tests added across `biomeos-types`, `biomeos-ui`, `neural-api-client`, `biomeos-atomic-deploy`,
and `biomeos-unibin` (modes). Remaining gap is largely binary entry points and I/O-heavy
server code.

### 9. sweetGrass Provenance Integration in rhizoCrypt

**Files changed**:
- `rhizoCrypt/crates/rhizo-crypt-core/src/types_ecosystem/provenance/client.rs` — `ProvenanceNotifier`
  now sends `contribution.recordDehydration` JSON-RPC with `DehydrationSummary` to sweetGrass
- `rhizoCrypt/crates/rhizo-crypt-core/src/rhizocrypt.rs` — auto-notifies sweetGrass after
  successful dehydration commit to permanent storage

### 10. Deployment Graph Format Normalization

**Files changed**:
- `graphs/loamspine_deploy.toml` — converted from legacy `action`/`params` to `[nodes.operation]` format
- `graphs/rhizocrypt_deploy.toml` — same normalization
- `graphs/sweetgrass_deploy.toml` — same normalization
- `graphs/provenance_trio_deploy.toml` — same normalization

All deployment graphs now use the `GraphNode` schema from `biomeos-atomic-deploy`:
`operation.name`, `operation.params`, `operation.environment`, `capabilities`, `config`.
A new `register_capabilities` handler was added to `node_handlers.rs`.

---

## Next Steps

1. **Execute E2E tests with live primals** — start trio + Tower, run `test_provenance_trio_e2e.sh`
2. **Ship `neural-api-client-sync`** (ISSUE-002) — airSpring workaround is the template
3. **Absorb NPU model into ToadStool** (ISSUE-006) — unblocks NPU for all Springs
4. ~~**RootPulse CLI wrapper**~~ — **DONE**: `biomeos rootpulse` ships with biomeOS
5. **ludoSpring `game.tick_logic` / `game.tick_physics` handlers** — stubs needed in ludoSpring
   so `biomeos continuous graphs/game_engine_tick.toml` can actually route to them
6. **Connection pooling for continuous mode** — current impl opens a new socket per node per tick;
   future optimization should keep persistent connections to primals
