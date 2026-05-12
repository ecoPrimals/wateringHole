<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation and creative text in this file: CC-BY-SA-4.0
-->

# ludoSpring V18 — Upstream Primal Evolution Tasks

**Date:** April 3, 2026
**From:** ludoSpring (game science spring)
**To:** biomeOS, Squirrel, petalTongue, Songbird, rhizoCrypt, loamSpine, sweetGrass teams
**Status:** Active
**License:** AGPL-3.0-or-later

---

## Context

ludoSpring V15-V18 validated primal composition for game science across 11
experiments (exp067-exp077), 9 deploy graphs, 9 proto sketches for esotericWebb,
and a full composition recipe. This work surfaced concrete gaps in the primal
layer that block the next evolution wave.

This handoff documents what each primal team needs to evolve. Evidence comes
from ludoSpring experiments, esotericWebb's EVOLUTION_GAPS.md, primalSpring's
PRIMAL_GAPS.md, and the IPC_COMPLIANCE_MATRIX.md.

Springs are reference implementations — they prove patterns work but can't own
anything in the primal layer. These are tasks for primals to absorb.

---

## biomeOS — P0 (Blocks Orchestrated Composition)

### 1. Fix `neural-api` health (GAP-017)

**Priority:** P0 (critical)
**Evidence:** In benchScale `tower-2node` live run, BearDog and Songbird come
up LIVE, but biomeOS `neural-api` is ZOMBIE (fails health check after startup).
**Impact:** Blocks ALL graph-orchestrated composition testing. Webb and
ludoSpring both drive their own loops as workaround.
**Resolution:** `neural-api` must start healthy and respond to `health.liveness`
within configured timeout in benchScale topologies.

### 2. Expose graph executors on JSON-RPC (GAP-018)

**Priority:** P0 (high)
**Evidence:** biomeOS has `ConditionalDag`, `Pipeline`, `ContinuousExecutor`,
and `PathwayLearner` in the codebase but none are exposed as JSON-RPC methods.
**Impact:** Webb cannot submit storytelling graphs for orchestrated execution.
ludoSpring cannot validate continuous 60Hz graphs via biomeOS orchestration.
**Resolution:** Expose at minimum:
- `ConditionalDag` execution via JSON-RPC
- `Pipeline` chaining via JSON-RPC
- `ContinuousExecutor` session start/stop via JSON-RPC
- `PathwayLearner`: `pathway.learn` and `pathway.suggest`

### 3. Add `[[graph.node]]` BYOB ingestion (GAP-020)

**Priority:** P1
**Evidence:** `neural_graph.rs` accepts `[[nodes]]` and `[[graph.nodes]]` but
not `[[graph.node]]` (the BYOB array key used by springs and gardens). Both
ludoSpring and primalSpring independently validated this schema. 18+ TOML files
across the ecosystem use it.
**Resolution:** Add a `[[graph.node]]` detection path to `neural_graph.rs`
alongside existing formats. Convert BYOB nodes to the internal schema on the
fly (same pattern as existing `convert_deployment_node`). See
`wateringHole/BYOB_DEPLOY_GRAPH_SCHEMA.md` for the schema spec.

### 4. Socket path policy documentation

**Priority:** P2
**Evidence:** ludoSpring has 3 different socket resolution paths in one crate
(discovery, server bind, and UniBin binary). Each uses slightly different env
var precedence.
**Resolution:** Document canonical socket path policy in wateringHole. biomeOS
enforces as the socket directory owner. Policy covers: env precedence
(`BIOMEOS_SOCKET_DIR` > `XDG_RUNTIME_DIR/biomeos` > `/tmp`), naming convention
(`{primal_name}.sock` vs `{primal_name}-{family_id}.sock`), and discovery
directory scanning behavior.

---

## Squirrel — P1

### NPC personality cert as hard constraint (GAP-003)

**Priority:** P1
**Evidence:** Webb's NPC personality certs define knowledge bounds, trust gates,
lies with detection DCs, and voice constraints. When Webb calls `ai.query` with
NPC context, the AI primal needs to enforce these mechanically — not as soft
prompt guidance.
**Impact:** Without mechanical enforcement, Webb must validate NPC responses
client-side and reject/retry. GameDirector enforces independently of AI.
**Resolution:** `ai.query` and `ai.analyze` accept a personality cert parameter
and enforce knowledge bounds, lies, and trust gates as hard constraints on
generated output. The cert structure is defined by Webb's content spec.

---

## petalTongue — P1

### `DialogueTreeScene` payload (GAP-002)

**Priority:** P1
**Evidence:** Webb defines `DialogueTreeScene` payloads but
`visualization.render.scene` has not confirmed support for dialogue tree
rendering with choice highlighting, voice interjection panels, or skill check
result display.
**Impact:** Webb uses text-mode preview (`esotericwebb preview`) which renders
to stdout without the visualization primal.
**Resolution:** `visualization.render.scene` accepts a `DialogueTreeScene`
payload type and renders it as an interactive dialogue UI with choices, voice
notes, and skill checks.

---

## Songbird — P1

### Capability-filtered `discovery.query` (GAP-006)

**Priority:** P1
**Evidence:** Webb's `PrimalRegistry::discover()` probes filesystem socket
directories but does not call `discovery.query` for tier-5 lookup. In a
composed niche, the discovery primal is the canonical mechanism.
**Impact:** Filesystem probe covers tiers 1-4. Tier-5 is logged as degraded.
**Resolution:** `discovery.query` accepts capability filter parameters and
returns matching primal endpoints. Response format documented in capability
discovery standard.

### IPC compliance

**Priority:** P1
**Evidence:** IPC_COMPLIANCE_MATRIX.md flags Songbird discovery compliance as
**X** (non-compliant) with 2558 references.
**Resolution:** Align with CAPABILITY_BASED_DISCOVERY_STANDARD.md.

---

## Provenance Trio — P1

### rhizoCrypt: save/load and bulk import (GAP-004)

**Priority:** P1
**Evidence:** Webb V4 wired provenance lifecycle (create, append, complete).
Still missing: `dag.slice.checkout` for save/load, `dag.event.append_batch`
for bulk import of local ProvenanceClient vertex logs.
**Resolution:** Implement `dag.slice.checkout` and `dag.event.append_batch` as
JSON-RPC methods.

### Live binary integration test

**Priority:** P1
**Evidence:** GAP-004 states "wiring complete (V4), live end-to-end validation
pending." plasmidBin has binaries (rhizocrypt v0.14.0-dev, loamspine v0.9.13,
sweetgrass v0.7.27) but no live integration test from Webb or ludoSpring.
**Resolution:** Run ludoSpring exp052 or Webb exp004 against live plasmidBin
binaries. Confirm round-trip: create session, append vertices, query, verify
Merkle root.

### sweetGrass transport normalization

**Priority:** P2
**Evidence:** IPC_COMPLIANCE_MATRIX.md notes sweetGrass TCP is HTTP-based, not
raw newline JSON-RPC.
**Resolution:** Align with ecosystem JSON-RPC transport standard.

---

## Cross-Primal IPC Compliance — P2

### CLI flag consistency

loamSpine uses `--jsonrpc-port`, nestGate uses `daemon` not `server`, etc.
UniBin standard says `--listen` / `--port`. Align all primals.

### `lifecycle.status` field naming

ludoSpring server returns `primal` in the health response; discovery probes
expect `name`. Both should be present, or one canonical field chosen and
documented in wateringHole.

### `health.liveness` as canonical method

IPC_COMPLIANCE_MATRIX.md recommends newline JSON-RPC `health.liveness` as the
standard health check method. Some primals use HTTP `/health` endpoints instead.
Standardize.

---

## Cross-References

- `ludoSpring/specs/ECOSYSTEM_EVOLUTION_MAP.md` — full gap analysis
- `ludoSpring/specs/PRIMAL_LEVERAGE_MAP.md` — primal-to-game-science mapping
- `gardens/esotericWebb/EVOLUTION_GAPS.md` — Webb gap registry
- `infra/wateringHole/IPC_COMPLIANCE_MATRIX.md` — IPC compliance status
- `infra/wateringHole/BYOB_DEPLOY_GRAPH_SCHEMA.md` — BYOB TOML schema standard
- `springs/primalSpring/docs/PRIMAL_GAPS.md` — per-primal gap registry
