# Provenance Trio End-to-End Validation & Whitepaper Completion

> **Archived**: Metrics below reflect state at time of writing. As of Mar 17 2026: rhizoCrypt 1102+ tests / 92.32% cov, sweetGrass 843+ tests, LoamSpine 770+ tests.

**Date**: March 13, 2026  
**Scope**: rhizoCrypt v0.13.0-dev + LoamSpine v0.8.0 + sweetGrass v0.7.3 + biomeOS + ludoSpring  
**Session**: Provenance trio live validation, type alignment, whitepaper gap closure

---

## What Was Accomplished

### 1. Provenance Trio Deployed with Live Binaries

Started the full provenance trio stack from live binaries:

| Service | Binary | Port | Status |
|---------|--------|------|--------|
| BearDog | `/tmp/trio-deploy/beardog` | Unix socket | Running |
| Songbird | `/tmp/trio-deploy/songbird` | 7500 | Running |
| LoamSpine | `/tmp/trio-deploy/loamspine` | 8301 (JSON-RPC) + 8302 (tarpc) | Running |
| rhizoCrypt | `/tmp/trio-deploy/rhizocrypt` | 9400 | Running |
| sweetGrass | `/tmp/trio-deploy/sweet-grass-service` | 9200 | Running |

### 2. Full 6-Phase RootPulse Commit Workflow Validated

Executed `rootpulse_commit.toml` against the live trio:

1. **Health Check** — All primals healthy
2. **Session/Dehydration** — rhizoCrypt session created, events appended, Merkle root computed, dehydration summary produced
3. **Sign** — BearDog signed the dehydration summary via `crypto.sign`
4. **Store** — NestGate-compatible content stored
5. **Commit** — LoamSpine `permanence.commit_session` accepted the session with full DehydrationSummary
6. **Attribute** — sweetGrass `contribution.recordDehydration` recorded provenance; `braid.create` created attribution braid

### 3. DehydrationSummary Type Alignment Validated

Compared the `DehydrationSummary` serde contract across all three primals:

- **rhizoCrypt → LoamSpine**: Perfect wire-format match. `PermanentStorageDehydrationSummary` fields map 1:1.
- **rhizoCrypt → sweetGrass**: sweetGrass has a richer struct (`source_primal`, `branch_count`, `attestations`, `operations`, `frontier`), but accommodates the simpler rhizoCrypt output through optional and defaulted fields.
- **Conclusion**: No breaking type mismatches. The trio is serde-compatible at the JSON-RPC boundary.

### 4. ludoSpring exp052 Validated

- Fixed relative path dependencies in 4 experiment `Cargo.toml` files (`exp052`, `exp053`, `exp054`, `exp061`): `../../../phase2/` → `../../../../phase2/`
- exp052 ran successfully against live trio binaries: **37/37 checks passing**
- Validates game session provenance pipeline end-to-end

### 5. ContinuousGraph Executor Confirmed

biomeOS `ContinuousExecutor` in `biomeos-graph` crate is fully implemented:
- `TickClock` with configurable Hz (default 60)
- `SessionState` for cross-tick state
- Feedback edges for inter-node data flow
- Per-tick budget enforcement
- `game_engine_tick.toml` graph template
- 15 tests passing

### 6. Whitepaper Gap Closure

Four missing spec documents authored:

| Document | Lines | Content |
|----------|-------|---------|
| `neuralAPI/03_GRAPH_EXECUTION.md` | 189 | biomeOS graph executor, coordination patterns, TOML graphs, capability routing |
| `neuralAPI/09_ROOTPULSE_CASE_STUDY.md` | 138 | Worked example with actual JSON-RPC calls from live trio validation |
| `RootPulse/06_COORDINATION_PATTERNS.md` | 125 | Sequential/parallel/conditional patterns, node dependencies, capability translation |
| `RootPulse/12_API_REFERENCE.md` | 164 | Concrete JSON-RPC calls for each commit workflow phase, service endpoint table |

---

## Bugs Fixed

### rhizoCrypt: Core Engine Not Started

`RhizoCrypt::new()` creates the primal in `Created` state but `start()` was not called in `rhizocrypt-service/src/lib.rs`. Added `primal.start().await?` and `use rhizo_crypt_core::primal::PrimalLifecycle` import. Without this, all operations fail with "primal not running".

### LoamSpine: Premature Server Shutdown

`run_jsonrpc_server()` returns a `ServerHandle` immediately. The spawned task in `main.rs` was completing when the handle was returned (not when the server stopped), causing `tokio::select!` to resolve and shut down. Fixed by awaiting `handle.stopped()` inside the spawned task.

---

## What Was Updated

### Root Documentation
- `wateringHole/README.md` — Date updated to March 13, 2026
- `wateringHole/PRIMAL_REGISTRY.md` — rhizoCrypt (862 tests), sweetGrass (v0.7.3, 746 tests), LoamSpine (700 tests), date
- `wateringHole/INTER_PRIMAL_INTERACTIONS.md` — Trio interactions updated from "Planned" to "Validated", next steps refreshed
- `neuralAPI/README.md` — Graph Execution, Continuous Coordination, RootPulse Case Study marked complete
- `whitePaper/RootPulse/README.md` — Version refs updated, e2e status added
- `whitePaper/RootPulse/00_INTRODUCTION.md` — All primal versions updated
- `whitePaper/RootPulse/02_ARCHITECTURE.md` — Dependency versions updated
- `whitePaper/RootPulse/08_SEMANTIC_ATTRIBUTION.md` — Integration versions updated
- `phase2/rhizoCrypt/crates/rhizocrypt-service/README.md` — v0.11.0 → v0.13.0
- `phase2/biomeOS/niches/rootpulse/README.md` — LoamSpine, sweetGrass status updated

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Combined trio tests | 2,308 (862 + 700 + 746) |
| Combined trio coverage | ~90% average |
| RootPulse workflow phases validated | 6/6 |
| ludoSpring exp052 checks | 37/37 |
| ContinuousExecutor tests | 15/15 |
| Whitepaper docs written | 4 (616 lines total) |
| Bugs fixed in production code | 2 (rhizoCrypt start, LoamSpine shutdown) |

---

## What's Next

1. **NestGate ↔ LoamSpine** — Content-addressed storage backing immutable history
2. **Cross-Spring provenance** — wetSpring, airSpring consuming `provenance_pipeline.toml`
3. **Songbird federation** — Multi-tower discovery and routing
4. **RootPulse CLI** — Unified `rootpulse` command coordinating trio via biomeOS
5. **neuralAPI pathway learning** — Co-occurrence metrics from trio usage to optimize routing

---

**The provenance trio is no longer theoretical — it is validated, tested, and documented.**
