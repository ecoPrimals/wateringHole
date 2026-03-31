# biomeOS V2.80 — Deep Debt Completion + Dependency Governance + Smart Refactoring

**Date**: March 30, 2026
**Scope**: SystemPaths centralization, graph.rs bounded-context refactor, dependency governance, hostname consolidation, doctest fixes
**Tests**: Full workspace passing (0 failures)
**Blocking debt**: 0

---

## Changes

### 1. Path Centralization — Hardcoded paths → SystemPaths

Replaced duplicated XDG/UID/temp fallback chains with the canonical `SystemPaths` API.

| File | Before | After |
|------|--------|-------|
| `biomeos-spore/beacon_genetics/capability.rs` (`NeuralApiCapabilityCaller::default_socket`) | Manual `XDG_RUNTIME_DIR` → `UID` → `temp_dir()` chain | `SystemPaths::new_lazy().primal_socket("neural-api")` |
| `biomeos-spore/beacon_genetics/capability.rs` (`DirectBeardogCaller::default_socket`) | Same 3-tier manual chain | `SystemPaths::new_lazy().primal_socket(BEARDOG)` |
| `biomeos-primal-sdk/discovery.rs` (`resolve_socket_dir`) | 5-tier resolution (env → XDG → UID → `/proc/self` → Android → SystemPaths) | `BIOMEOS_SOCKET_DIR` override → `SystemPaths::new_lazy().runtime_dir()` |
| `biomeos-core/model_cache/cache.rs` (`default_cache_dir`) | `$HOME/.biomeos/model-cache` | `SystemPaths::new_lazy().cache_dir().join("models")` (XDG: `~/.cache/biomeos/models`) |

**Impact**: All socket/cache paths now flow through `SystemPaths`, which handles XDG → `/run/user/$UID` → temp fallback. Single source of truth. Tests updated to match new XDG-compliant paths.

### 2. Smart Refactoring — graph.rs bounded context split

`biomeos-atomic-deploy/src/handlers/graph.rs` (953 LOC) → `graph/` module directory:

| Module | LOC | Responsibility |
|--------|-----|---------------|
| `graph/mod.rs` | ~316 | Types (`ExecutionStatus`, `ContinuousSession`), constructor, CRUD (`list`/`get`/`save`), `get_status`, `suggest_optimizations`, `resolve_primal_name`, `extract_session_id` |
| `graph/execute.rs` | ~234 | `execute()` (sequential), `register_capabilities_from_graph`, `load_translations_from_graph` |
| `graph/continuous.rs` | ~195 | `start_continuous`, `pause_continuous`, `resume_continuous`, `stop_continuous` |
| `graph/pipeline.rs` | ~159 | `execute_pipeline`, `execute_pipeline_node` |

**Decision rationale**: `sovereignty_guardian.rs` (898 LOC) and `continuous.rs` (845 LOC) were left as-is — both are cohesive single bounded contexts where splitting would add indirection without benefit. Smart refactoring, not mechanical splitting.

All 1074 biomeos-atomic-deploy tests pass unchanged. Public API (`GraphHandler`, `ExecutionStatus`) re-exported from `graph/mod.rs` — zero import changes needed downstream.

### 3. Dependency Governance

#### Unused workspace deps removed (11)
`tower-http`, `bincode`, `tungstenite`, `tokio-tungstenite`, `dotenvy`, `temp-env`, `mdbook`, `validator`, `num_cpus`, `env_logger`, `regex`

These were declared in `[workspace.dependencies]` but never consumed via `{ workspace = true }` by any crate. Some crates (e.g., `biomeos-api`) use the same crate with explicit versions — those are unaffected.

#### hostname → gethostname consolidation
- Removed `hostname` crate (0.3 in biomeos-system, 0.4 in biomeos-core)
- Both now use `gethostname = { workspace = true }` (0.5)
- `hostname::get()` → `gethostname::gethostname()` (same semantics, single dep)
- `hostname` crate fully eliminated from `Cargo.lock`

#### Code duplication eliminated
- `discover_primal_endpoint()` (40 LOC standalone function duplicating `AtomicClient::discover()`) → 3-line delegation via `AtomicClient::discover().endpoint().clone()`

### 4. Doctest Fixes

Fixed `.await` on synchronous functions in module-level doctests:
- `biomeos-core/primal_adapter/mod.rs`: `adapter.start(9010).await?` → `adapter.start(9010)?`; `adapter.check_health().await?` → `adapter.check_health()?`
- `biomeos-ui/src/lib.rs`: `InteractiveUIOrchestrator::new("...").await?` → `InteractiveUIOrchestrator::new("...")?`

### 5. Root Documentation Updated

- `README.md`: Version 2.79 → 2.80, primals 6/6 → 7/7, architecture diagram includes barraCuda + coralReef, Atomics table updated, Primal Status table expanded, dependency governance section updated
- `CHANGELOG.md`: v2.80 entry added
- `CURRENT_STATUS.md`: Version and component counts updated

---

## Verification

| Check | Result |
|-------|--------|
| `cargo test --workspace` | 0 failures |
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-targets` | 0 errors |
| `cargo audit` | 0 vulnerabilities, 3 transitive warnings (upstream) |
| `cargo tree -i hostname` | "did not match any packages" (fully removed) |
| Files > 1000 LOC | 0 (largest: 970, a test file) |
| TODO/FIXME/HACK | 0 in production code |

---

## For Other Primals

### barraCuda / coralReef
- biomeOS now has full capability domain registration for `math`, `tensor`, `stats`, `noise`, `activation`, `rng` (barraCuda) and `shader`, `wgsl`, `spirv` (coralReef) in `tower_atomic_bootstrap.toml` and fallback capability domains
- Auto-discovery probes both `capabilities.list` and `capability.list` method names
- Pipeline executor extracts domain from dotted capability names (e.g., `math.sigmoid` → discovers via `math` domain) — consistent with `capability.call` routing

### All Primals
- `SystemPaths::new_lazy()` is the canonical way to resolve runtime directories. Never hardcode `$XDG_RUNTIME_DIR/biomeos/` or `/run/user/$UID/biomeos/` — use `SystemPaths`.
- Socket naming convention: `{primal_name}-{family_id}.sock` in `SystemPaths.runtime_dir()`
