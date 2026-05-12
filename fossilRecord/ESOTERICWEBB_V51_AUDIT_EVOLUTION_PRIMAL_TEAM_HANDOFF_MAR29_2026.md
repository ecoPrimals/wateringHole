<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# HANDOFF: Esoteric Webb V5.1 — Audit Evolution + Primal Team Feedback

- **Date**: 2026-03-29
- **Source**: esotericWebb V5.1 (gardens/esotericWebb)
- **Audience**: petalTongue, Squirrel, rhizoCrypt, loamSpine, sweetGrass, Songbird, ludoSpring, biomeOS/primalSpring
- **Type**: Evolution feedback + pattern dissemination + per-primal requests

---

## Context

Esoteric Webb V5.1 is a deep audit evolution pass on the first gen4 consumer.
Webb composes 8 primal domains via JSON-RPC IPC with graceful degradation.
This handoff communicates evolution status, corrects documentation gaps, and
makes specific requests to primal teams.

**V5.1 numbers:** 335 tests, 37 Rust files (~12.5k LOC), 90.84% coverage,
zero `#[allow]` in production, zero unsafe, zero C deps, all quality gates clean.

---

## Per-Primal Requests

### petalTongue — GAP-002 (medium)

Webb defines `DialogueTreeScene` payloads for CRPG dialogue rendering. The
`visualization.render.scene` bridge method fires-and-forgets scene payloads.

**Request:** Confirm or implement `scene_type: "dialogue_tree"` payload
support with fields: `choices` (labeled options), `voice_notes` (interjection
panels), `skill_checks` (result display with DC and outcome). Webb will
exercise immediately once available.

### Squirrel — GAP-003 (medium), GAP-007 (medium)

Webb's NPC personality certs carry hard constraints (knowledge bounds, trust
gates, lies with detection DCs, voice parameters). Currently `ai.chat`
receives these as context with prompt-based enforcement only.

**Request (GAP-003):** Accept NPC personality cert as a structured constraint
parameter on `ai.chat` or `game.npc_dialogue`. Enforce knowledge bounds, lie
detection, and trust gates mechanically rather than via system prompt.

**Request (GAP-007):** No action needed from Squirrel — offline voice preview
is self-owned by Webb. Noted for awareness.

### rhizoCrypt — GAP-004 (low, wiring complete)

All DAG lifecycle methods wired and tested structurally. Bridge methods:
`dag.session.create`, `dag.event.append`, `dag.session.complete`,
`dag.frontier.get`, `dag.merkle.root`, `dag.query.vertices`.

**Request:** Stable binary in plasmidBin for live end-to-end integration test.
Next methods Webb wants: `dag.slice.checkout` (save/load), `dag.event.append_batch`
(bulk import of locally recorded vertices).

### loamSpine — GAP-004 (low)

`certificate.mint` is bridge-ready. Session lifecycle methods (`spine.create`,
`entry.append`, `session.commit`) are documented in GAP-004 expectations.

**Request:** Stable binary in plasmidBin. Confirm `certificate.mint` request
schema matches Webb's NPC personality cert format.

### sweetGrass — GAP-004 (low, documentation corrected)

**Honesty note:** Webb's earlier documentation claimed sweetGrass was "Bridge
ready" with `attribution.record`. This was inaccurate — `domain::PROVENANCE`
is discovered via `primal_names` but **no bridge methods exercise it**. V5.1
corrected README and VISION_AND_EVOLUTION to "Discovered, not yet exercised."

**Request:** When attribution methods (`braid.create`, `attribution.chain`,
`provenance.graph`) are stable, notify Webb. Bridge method implementation is
straightforward (1-3 line delegation to existing call helpers).

### Songbird — GAP-006 (medium)

Webb's `PrimalRegistry::discover()` uses filesystem probes (tiers 1-4) but
does not call `discovery.query` for tier-5 capability-filtered lookup.

**Request:** Confirm `discovery.query` response format. Specifically: can Webb
query by capability domain (e.g. "ai", "game") and receive endpoint addresses?

### ludoSpring — GAP-009 (medium)

Webb loads `rulesets/*.yaml` as opaque `serde_json::Value`. No structural
validation against game science RulesetCert schema exists.

**Request:** Publish RulesetCert JSON Schema or provide `game.ruleset_validate`
method that accepts a YAML ruleset and returns validation results.

### biomeOS / primalSpring — GAP-010 (medium)

plasmidBin deployment automation remains the primary blocker for gen4
adoption. Webb's deploy graphs reference primals by capability but cannot
resolve them until binaries land.

**Request:** CI pipelines or `genome fetch` tooling to populate `plasmidBin/`
with versioned, checksummed primal binaries.

---

## Patterns for Absorption

These patterns matured in Webb V5.1 and are recommended for ecosystem adoption:

### 1. `#[expect]` over `#[allow]`

Replace all `#[allow(clippy::...)]` with `#[expect(clippy::..., reason = "...")]`.
Benefits: dead suppression detection (unfulfilled expectations warn), mandatory
documentation. During migration, remove dead suppressions entirely rather than
converting them.

### 2. Directory Modules for Growing Impl Blocks

When a struct's impl block approaches 1000 lines, convert the file to a
directory module. Child modules in Rust can access parent private methods
without visibility changes. Domain-specific delegations go in a submodule;
core infrastructure stays in `mod.rs`.

Example: `bridge.rs` (943 LOC) → `bridge/mod.rs` (565) + `bridge/domains.rs`
(396). New primal domains extend only `domains.rs`.

### 3. Dynamic Port Allocation in Tests

Replace hardcoded ports with `TcpListener::bind("127.0.0.1:0")` to get
OS-assigned ephemeral ports. Prevents port collision in parallel CI runs.

### 4. Capability Registry Cross-Validation

Add a test that iterates all methods in `capability_registry.toml` and
verifies none return "method not found" from the server. Catches capability
drift between documentation and implementation.

---

## Files Modified in V5.1

| File | Change |
|------|--------|
| `webb/src/content/types.rs` | **New** — extracted content data model |
| `webb/src/ipc/bridge/mod.rs` | **New** — core bridge (was `bridge.rs`) |
| `webb/src/ipc/bridge/domains.rs` | **New** — domain delegations |
| `webb/src/ipc/bridge.rs` | **Deleted** — replaced by bridge/ directory |
| `webb/src/ipc/listener.rs` | Refactored handler signatures to references |
| `webb/src/ipc/bridge.rs` → `bridge/` | All `#[allow]` → `#[expect]` |
| `webb/src/ipc/handlers/mcp.rs` | Removed dead lint suppression |
| `webb/src/bin/commands/mod.rs` | `#[allow]` → `#[expect]` with reasons |
| `webb/tests/e2e_ipc.rs` | 6 new tests (TCP E2E + capability cross-validation) |
| `webb/tests/validation_experiments.rs` | Dynamic port, narrowed `#[expect]` |
| `experiments/exp002_*/src/main.rs` | Fixed tautological assertion, capability-based |
| `experiments/exp004_*/src/main.rs` | Dynamic port allocation |
| `experiments/exp005_*/src/main.rs` | Fixed tautological assertion |
| `specs/PAPER_REVIEW_QUEUE.md` | **New** — ecosystem compliance |
| All docs | Dates, metrics, sweetGrass honesty correction |
