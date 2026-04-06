<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# wetSpring Science NUCLEUS — Gaps & Evolution Requests

**Date:** April 6, 2026
**From:** wetSpring (science facade + full NUCLEUS deployment)
**To:** primalSpring, biomeOS, RootPulse, loamSpine, petalTongue, plasmidBin
**Status:** Gaps documented — requesting evolution time from owning teams

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

## Gap 1: Neural API Method Name Alignment

**Owner:** biomeOS
**Priority:** HIGH — blocks Tier 2/3 provenance, Dark Forest, and NestGate caching

**Problem:** The facade calls top-level JSON-RPC methods (`provenance.begin`, `provenance.record`, `provenance.complete`, `birdsong.decrypt`) on the Neural API socket. The `NeuralApiServer` route table in biomeOS does not register these as top-level methods — they need to go through `capability.call` with the appropriate capability + operation shape.

**Evidence:** `$XDG_RUNTIME_DIR/biomeos/` contains 237 primal sockets (`cycle-primal-*`, `storm-primal-*`, `ta-*`) but **zero `neural-api-*.sock`** sockets. No biomeOS processes running. No systemd user units loaded.

**Options:**
1. biomeOS adds `provenance.begin`, `provenance.record`, `provenance.complete`, `birdsong.decrypt` as top-level route sugar in the Neural API (preferred — simpler client code)
2. wetSpring rewrites facade to use `capability.call` wrappers (works but verbose)

**Request:** biomeOS team to decide on approach and document the canonical pattern for springs consuming Neural API. Every spring facade will hit this same friction.

---

## Gap 2: Ionic Contract Negotiation Protocol

**Owner:** primalSpring Track 4 (`BondingConstraint + BondingPolicy`)
**Priority:** HIGH — blocks external researcher collaboration

**Problem:** wetSpring declares bonding metadata (`bonding_metadata.json`) and exposes it via `GET /api/v1/system/composition`. But there is no protocol for:

- Establishing a new ionic bond (handshake, capability scoping, duration, attribution)
- Modifying scope mid-bond
- Terminating with a final provenance seal
- Validating bond status during request dispatch

**What wetSpring has scaffolded:**
- `Covalent` (LAN mesh, GeneticLineage trust) and `Ionic` (cloudflared, Contractual trust) bond types declared
- Capability scopes per bond type enumerated
- Trust model requirements documented
- Contract fields spec'd: `collaborator_identity`, `capability_scope`, `duration`, `attribution_requirements`, `data_return_policy`

**Request:** primalSpring to define the concrete negotiation protocol. wetSpring will be the first consumer/validator.

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

## Gap 4: Public Chain Anchor for Provenance

**Owner:** loamSpine team (Paper 20 Section 6 — marked "Needed")
**Priority:** MEDIUM — blocks external verification

**Problem:** The provenance trio produces rhizoCrypt DAG sessions, loamSpine ledger commits, and sweetGrass semantic braids. These are verifiable within the ecosystem trust boundary. Without a public anchor (timestamp service, blockchain, etc.), external parties must trust the ecosystem's own ledger.

**Request:** loamSpine team to define the public anchoring mechanism. wetSpring's `verify_url` pattern in Tier 3 provenance is ready to link to it.

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

## Summary for primalSpring

wetSpring is the first spring to deploy the full NUCLEUS composition pattern against real science. The architecture is proven (compiles, routes wired, provenance emitted). The gaps found are **ecosystem-wide** — every spring will hit the same Neural API alignment, ionic negotiation, and cross-spring data exchange issues. Resolving these for wetSpring resolves them for the entire garden.
