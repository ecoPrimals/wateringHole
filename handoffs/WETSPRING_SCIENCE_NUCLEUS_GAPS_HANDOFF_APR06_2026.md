<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# wetSpring Science NUCLEUS — Gaps & Evolution Requests

**Date:** April 6, 2026
**From:** wetSpring (science facade + full NUCLEUS deployment)
**To:** primalSpring, biomeOS, RootPulse, loamSpine, petalTongue, plasmidBin
**Status:** 2 of 7 gaps RESOLVED, 1 PARTIALLY RESOLVED, 1 CLOSED, 3 OPEN (reconciled April 6)

---

## Context

wetSpring has deployed a full NUCLEUS science pipeline: Tower (BearDog + Songbird) for auth, Node (ToadStool) for compute, Nest (NestGate) for storage, the provenance trio (rhizoCrypt + loamSpine + sweetGrass) for lineage, petalTongue for visualization, and the science facade as an HTTP gateway through Dark Forest. The deploy graph is `wetspring_science_nucleus.toml`.

The system compiles cleanly, the facade architecture is solid, and Tier 1 provenance (guideStone validation, BLAKE3 hashing, reproduction manifests, NFT vertex structure) works fully locally. But **live end-to-end operation is blocked by gaps in the supporting primals**, documented below.

This is the first spring to attempt the full NUCLEUS pattern against real science data (Gonzales 2014 dermatitis, Anderson localization). The gaps found here apply to every spring that will follow this pattern.

---

## What Works Today

| Layer | Status | Notes |
|-------|--------|-------|
| Facade (Axum HTTP) | **Compiles, routes wired** | 14 science endpoints + grammar rendering + validation chain + composition |
| Dark Forest middleware | **Code complete** | Mirrors biomeOS gate; needs live BearDog + Neural API socket |
| Tier 1 provenance | **Fully functional** | guideStone version, BLAKE3 hash, reproduction manifest, NFT vertex |
| Reproduction envelope | **Embedded in every response** | plasmidBin manifest, deploy graph, fetch/deploy/recompute commands |
| NFT vertex structure | **Emitted per computation** | vertex_id, parent_vertices, agents, derivation, scyBorg license triple |
| Composition endpoint | **Live** | `GET /api/v1/system/composition` returns graph, versions, bonding metadata |
| composition.science_health | **IPC handler wired** | Follows primalSpring `composition.*_health` pattern |
| Bonding metadata | **Declared** | Covalent + Ionic bond types, capability scopes, trust models |
| Deploy graph | **Proven** | 11-node sequential graph, all by_capability |
| Reference registry | **3 papers** | Gonzales 2014, Fleck/Gonzales 2021, Gonzales 2013 with DOIs + validation |
| Explorer UI | **Functional** | Plotly.js charts, parameter sliders, validation tab, reproduce button |

---

## Gap 1: Neural API Method Name Alignment — **RESOLVED**

**Owner:** biomeOS
**Priority:** ~~HIGH~~ **RESOLVED** (biomeOS v2.90)

**Problem:** The facade calls top-level JSON-RPC methods (`provenance.begin`, `provenance.record`, `provenance.complete`, `birdsong.decrypt`) on the Neural API socket. The `NeuralApiServer` route table in biomeOS does not register these as top-level methods — they need to go through `capability.call` with the appropriate capability + operation shape.

**Resolution:** biomeOS v2.90 implements **universal semantic routing fallback**. Any `domain.operation` method auto-routes through `capability.call`. 32 new provenance trio translations. 9 composition health aliases. Springs need no code changes — both direct `domain.operation` calls and explicit `capability.call` work. See `BIOMEOS_V290_NEURAL_API_SEMANTIC_ROUTING_PROVENANCE_TRIO_HANDOFF_APR06_2026.md`.

primalSpring v0.8.1 verified compatibility: `NeuralBridge::capability_call()` path works. DEBT-03 closed.

**Remaining operational note:** biomeOS process must be running and `neural-api.sock` present for live calls. The API shape problem is fully resolved.

---

## Gap 2: Ionic Contract Negotiation Protocol — **PARTIALLY RESOLVED**

**Owner:** primalSpring Track 4 (`BondingConstraint + BondingPolicy`)
**Priority:** ~~HIGH~~ **MEDIUM** — protocol defined, crypto handshake pending BearDog

**Problem:** wetSpring declares bonding metadata (`bonding_metadata.json`) and exposes it via `GET /api/v1/system/composition`. But there is no protocol for:

- Establishing a new ionic bond (handshake, capability scoping, duration, attribution)
- Modifying scope mid-bond
- Terminating with a final provenance seal
- Validating bond status during request dispatch

**What primalSpring v0.8.1 resolved (DEBT-06):**
- `bonding.propose` JSON-RPC handler: deserializes and validates `IonicProposal` (proposer identity, requested capabilities, trust model, duration, attribution requirements). Returns structured validation result or rejection.
- `bonding.status` JSON-RPC handler: queries contract by ID (currently returns `not_found` — contract store pending).
- Full Rust type system: `BondType` (5 variants), `TrustModel` (4 variants), `BondingConstraint` (glob allow/deny, bandwidth, concurrency), `BondingPolicy` with validation, `IonicProposal`, `ContractState` FSM, `IonicContract`, `ProvenanceSeal`. All `Serialize + Deserialize`.

**What remains:**
- **Runtime contract store** — needs BearDog `crypto.sign_contract` + `crypto.verify_contract` for propose→accept→seal handshake
- **Shared type crate** — bonding types ready for extraction to `ecoPrimals-contracts` (wateringHole governance)
- **Scope modification** and **provenance seal on termination** — additive once store exists

See `PRIMALSPRING_V081_WETSPRING_NUCLEUS_ELEVATION_DEBT_RESOLUTION_HANDOFF_APR06_2026.md`.

---

## Gap 3: Cross-Spring Data Exchange via RootPulse

**Owner:** RootPulse team
**Priority:** HIGH — blocks data sharing between springs

**Problem:** NestGate stores data locally. The `data.fetch.*` handlers hash and provenance-wrap fetched data. The `vault.*` handlers provide consent-gated storage. But there is no protocol for another spring's NUCLEUS to pull provenance-wrapped data subsets.

**Specific missing pieces:**
- Remote NestGate query (how does spring B ask spring A's NestGate for a key?)
- Provenance chain continuity across the pull (spring B's braid must reference spring A's braid)
- Differential sync (fetch only what changed, not full re-fetch)

**Request:** RootPulse team to define the cross-spring data exchange protocol. wetSpring's NestGate integration is ready to be the test case.

---

## Gap 4: Public Chain Anchor for Provenance — **CLOSED**

**Owner:** loamSpine team (Paper 20 Section 6 — marked "Needed")  
**Priority:** ~~MEDIUM — blocks external verification~~ **RESOLVED** (loamSpine v0.9.16)  
**Resolution:** See `LOAMSPINE_V0916_PUBLIC_CHAIN_ANCHOR_HANDOFF_APR06_2026.md`

**Problem:** The provenance trio produces rhizoCrypt DAG sessions, loamSpine ledger commits, and sweetGrass semantic braids. These are verifiable within the ecosystem trust boundary. Without a public anchor (timestamp service, blockchain, etc.), external parties must trust the ecosystem's own ledger.

**Resolution detail:** loamSpine v0.9.16 implements `anchor.publish` / `anchor.verify` (JSON-RPC + tarpc). `PublicChainAnchor` entry type records receipts from any append-only ledger. Chain submission is delegated to a capability-discovered `"chain-anchor"` primal. wetSpring Tier 3 `verify_url` can now link to `anchor.verify`.

---

## Gap 5: plasmidBin Reproduction Flow

**Owner:** plasmidBin / wateringHole
**Priority:** MEDIUM — blocks "click to clone" reproduction

**Problem:** The reproduction manifest (`reproduction_manifest.toml`) pins exact primal versions. The `fetch.sh --tag` flow exists. But the end-to-end reproduction has not been tested:

- Does `fetch.sh --tag v0.7.0` actually produce a working set of binaries?
- Does `biomeos deploy --graph wetspring_science_nucleus.toml` succeed on a fresh machine?
- Can the reproduced system compute the same result with matching BLAKE3 hash?

**What wetSpring provides:**
- `reproduction_manifest.toml` in plasmidBin `manifest.lock` format
- Fetch, deploy, and recompute commands embedded in every provenance envelope
- BLAKE3 content hash for verification

**Request:** plasmidBin team to validate the reproduction flow and evolve `fetch.sh` if needed. This is the first spring to embed reproduction metadata in API responses.

---

## Gap 6: petalTongue Client WASM

**Owner:** petalTongue team
**Priority:** LOW (Phase 3) — currently mitigated by Plotly.js fallback

**Problem:** Grammar rendering is server-side SVG via petalTongue RPC. The endgame is client-side WASM for offline-capable rendering. Not urgent — Plotly.js works well as fallback.

---

## Gap 7: Radiating Attribution Calculator

**Owner:** sweetGrass + sunCloud (Paper 20 Section 6 — "Low, Phase 4")
**Priority:** LOW — not needed until ionic bonding is live

**Problem:** NFT vertices record derivation chains but do not compute attribution weights for downstream use across ionic bonds.

---

## Files Reference

All scaffolding is committed in `springs/wetSpring/`:

| File | Purpose |
|------|---------|
| `barracuda/data/reproduction_manifest.toml` | Pinned versions for reproduction |
| `barracuda/data/bonding_metadata.json` | Ionic/Covalent bond declarations |
| `barracuda/data/reference_registry.json` | Paper DOIs, validation chains |
| `barracuda/src/facade/provenance.rs` | Tier 1-3 + reproduction + NFT vertex |
| `barracuda/src/facade/dark_forest.rs` | Dark Forest middleware |
| `barracuda/src/facade/routes.rs` | All facade endpoints inc. composition |
| `graphs/wetspring_science_nucleus.toml` | Full NUCLEUS deploy graph |
| `GAPS.md` | Local gap tracking document |

---

## Summary

wetSpring is the first spring to deploy the full NUCLEUS composition pattern against real science. The architecture is proven (compiles, routes wired, provenance emitted). The gaps found are **ecosystem-wide** — every spring will hit the same Neural API alignment, ionic negotiation, and cross-spring data exchange issues.

**Status (April 6 reconciliation):**
- **Gap 1** (Neural API): **RESOLVED** — biomeOS v2.90 semantic routing
- **Gap 2** (Ionic negotiation): **PARTIALLY RESOLVED** — types + handlers in primalSpring v0.8.1; crypto pending BearDog
- **Gap 3** (RootPulse cross-spring): **OPEN** — no protocol defined yet
- **Gap 4** (Public chain anchor): **CLOSED** — loamSpine v0.9.16
- **Gap 5** (plasmidBin reproduction): **OPEN** — needs E2E validation
- **Gap 6** (petalTongue WASM): **LOW** — mitigated by Plotly.js fallback; `petal-tongue-wasm` crate exists
- **Gap 7** (Radiating attribution): **LOW** — blocked on ionic protocol completion
