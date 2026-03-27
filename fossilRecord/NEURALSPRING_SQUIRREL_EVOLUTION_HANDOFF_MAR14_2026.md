# neuralSpring → Squirrel: Ecosystem Evolution Handoff

**Date:** March 14, 2026
**From:** neuralSpring S148 (playGround: Squirrel MCP adapter + interactive runner)
**To:** Squirrel team
**Scope:** Ecosystem standard gaps, evolution targets, MCP integration readiness
**License:** AGPL-3.0-or-later

---

## Executive Summary

- neuralSpring built its first **Squirrel MCP integration** via `playGround/` — an adapter binary that bridges 14 `science.*` capabilities to Squirrel's `tool.execute` API, and an interactive runner using `ai.query`
- Squirrel v1.7.0 is architecturally sound (gRPC removed, capability discovery, `forbid(unsafe_code)`, AGPL-3.0-only) but **lags on lint discipline, doc freshness, and legacy cleanup** relative to the ecosystem
- This handoff summarizes what needs to evolve for Squirrel to match the standard set by neuralSpring, petalTongue, ludoSpring, and barraCuda

---

## Part 1: What neuralSpring Built (for Squirrel)

### playGround MCP Adapter

`neuralspring_mcp_adapter` binary:
- Discovers neuralSpring primal and Squirrel via biomeOS 5-tier socket resolution
- Registers 14 `science.*` capabilities with Squirrel via `capability.announce`
- Forwards `tool.execute` calls to neuralSpring primal socket
- Supports `tool.list` for capability enumeration
- Graceful degradation: runs in standalone mode if Squirrel unavailable

### playGround Interactive Runner

`neuralspring_interactive` binary:
- Connects to both Squirrel (`ai.query`) and neuralSpring primal (`science.*`)
- Commands: `run <experiment>`, `analyze`, `ask <question>`, natural language
- Conversation context includes last experiment results
- Model selection via `--model` flag

### MCP Tool Definitions

14 tool definitions with JSON Schema in `mcp_tools.rs`:

| Tool | Domain |
|------|--------|
| `science.spectral_analysis` | Spectral |
| `science.anderson_localization` | Spectral |
| `science.hessian_eigen` | Spectral |
| `science.agent_coordination` | Spectral |
| `science.ipr` | Spectral |
| `science.disorder_sweep` | Spectral |
| `science.training_trajectory` | Spectral |
| `science.evoformer_block` | coralForge |
| `science.structure_module` | coralForge |
| `science.folding_health` | coralForge |
| `science.gpu_dispatch` | GPU |
| `science.cross_spring_provenance` | Cross-spring |
| `science.cross_spring_benchmark` | Cross-spring |
| `science.precision_routing` | Cross-spring |

**Squirrel action:** Ensure `tool.execute` dispatches correctly when the adapter registers these capabilities. The adapter binds its own socket and handles forwarding.

---

## Part 2: Ecosystem Standard Gaps

### P0 — Lint Discipline

| Gap | Ecosystem Standard | Squirrel Status | Action |
|-----|-------------------|-----------------|--------|
| `#[allow()]` → `#[expect()]` | All springs/primals use `#[expect(..., reason = "...")]` | 100+ `#[allow()]` remain | Migrate all with documented reasons |
| PRIMAL_REGISTRY | Versioned with test counts (neuralSpring V100, barraCuda v0.3.5, petalTongue v1.6.3) | No version, sparse detail | Update to v1.7.0 with 3,969 tests, crate count, architecture |
| Spec freshness | Current as of March 2026 | `CURRENT_STATUS.md` dated Nov 2025, roadmap dated Jan 2025 | Refresh all specs |

### P1 — Legacy Removal

| Item | Status | Action |
|------|--------|--------|
| `grpc_port` config field | Present despite gRPC removal | Remove field, migrate to constants |
| `SongbirdClient` wrapper | Deprecated but still in tree | Remove once consumers use capability discovery |
| gRPC references in mcp-protocol specs | Multiple specs reference gRPC | Update to JSON-RPC-only |

### P2 — Evolution Targets

| Target | Ecosystem Standard | Squirrel Current |
|--------|-------------------|-----------------|
| Test coverage | 90% (neuralSpring: 92%, ludoSpring: 93.2%) | 70% |
| ecoBin certification | ToadStool certified | Not formally certified |
| Lysogeny awareness | All primals document obligations | Not documented |
| scyBorg compliance | Triple copyleft documented | License correct but trio not documented |

---

## Part 3: Cross-Pollination Patterns

neuralSpring offers proven patterns Squirrel could adopt:

### Tolerance Registry
`tolerances/mod.rs` — 80+ named constants with doc justifications. If Squirrel
adds numerical validation (AI metric thresholds, latency SLOs), this pattern
prevents magic numbers.

### ValidationHarness
`check_abs` / `check_rel` / `check_abs_or_rel` + exit code 0/1. Standard
pattern for all validation binaries across the ecosystem.

### BaselineProvenance
Struct with script, commit, date, command, environment fields. Tracks where
expected values came from. Useful for AI provider benchmarking.

### Socket-Decoupled Architecture
playGround talks to primals only via Unix sockets — no library imports.
This is the correct pattern for MCP integration: the adapter is a bridge
process, not a monolith.

---

## Part 4: MCP Integration Readiness

For the playGround adapter to work optimally, Squirrel should:

1. **Verify `capability.announce` handler** — the adapter sends primal name,
   capability list, and socket path. Squirrel should store this for routing.

2. **Verify `tool.execute` forwarding** — when Squirrel receives a `tool.execute`
   for a `science.*` tool, it should forward to the adapter's socket.

3. **Verify `tool.list` includes announced tools** — after registration, the
   adapter's tools should appear in Squirrel's tool listing.

4. **AI provider for local Ollama** — the interactive runner uses `ai.query`.
   Squirrel needs an AI provider socket (Ollama/llama.cpp) configured via
   `AI_PROVIDER_SOCKETS` for local inference.
