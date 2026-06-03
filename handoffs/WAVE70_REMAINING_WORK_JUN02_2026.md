# Wave 70 — Remaining Work & Status

**Date**: 2026-06-03 (morning, updated)
**Author**: eastGate (overwatch)
**Wave**: 71 (post Wave 70 overnight sprint)
**Status**: Active — guides Wave 72+ assignments
**Supersedes**: WAVE68_SOVEREIGN_EVOLUTION_REMAINING_WORK_JUN02_2026.md (archived)

---

## Executive Summary

Massive evolution sprint Waves 68-71. southGate delivered ALL P1 items. ironGate
executed sovereignty graduation AND S3 VPS readiness (cutover is a single DNS flip).
bearDog shipped grapheneGate keystore design. primalSpring hardened security
(deny on missing scopes, real latency probes). projectNUCLEUS built genomeBin
scaffold. projectFOUNDATION fixed 3 failing tests and typed all errors. strandGate
provenance trio fully resolved. biomeGate offline (kernel recovery) — compute trio
PAUSED.

Two operator-gated items remain on the glacial critical path: DNS NS registrar
cutover and eastGate mesh validation initiation.

---

## Track 1: Glacial Cutover (P0)

### 1A. Live Mesh Validation (eastGate + strandGate) — WAVE 72 UPDATE

| Item | Status | Notes |
|------|--------|-------|
| Songbird `latency_ms` in `discovery.peers` | **DONE** (wire) | Populated as null — HTTP probing not invoked (P2) |
| biomeOS endpoints ready | **DONE** | Cross-gate mesh partner verified |
| `discovery.peers` live 2-gate test | **DONE** | Wave 72: eastGate ↔ strandGate, 1 peer, quality 1.0 |
| `capability.call` cross-gate test | **BLOCKED** | Songbird raw TCP vs HTTP mismatch (P1 FRAGO filed) |
| Cross-subnet routing (192.168.4.x) | **DEFERRED** | Used strandGate (same subnet) instead. Eero doesn't route VLANs |
| 3+ gate plasmodium collective | BLOCKED | After capability.call fixed |

**Critical path**: Songbird `remote_dispatch.rs` must HTTP POST to `/jsonrpc` (not raw TCP).
See: `wave72-songbird-remote-dispatch-fix` FRAGO.

### 1B. Sovereignty Shadow Graduation

| Shadow | Status | Remaining |
|--------|--------|-----------|
| S1 TLS | **Infra verified** (198 probes, 0 failures, p95 < 120ms) | NS cutover (registrar manual) → remove Cloudflare |
| S2 NAT | **GRADUATED** | — |
| S3 Content | **Ready** (sporePrint 101 tests, zero-C, 67ms TTFB) | Cutover after DNS NS switch |
| S4 Auth | **7-day gate ACTIVE** (started Jun 2, ends ~Jun 9) | Monitoring via 15-min probes |
| S5 DNS | **Infra LIVE** (knot-dns, DNSSEC) | Registrar NS cutover (operator) |

**Critical path**: Operator DNS NS registrar cutover. S4 gate runs autonomously until ~Jun 9.

---

## Track 2: Primal Code Evolution (P1-P2)

### 2A. southGate — ALL P1 COMPLETE

| Primal | Delivered | Remaining |
|--------|-----------|-----------|
| **Songbird** v0.2.5 | latency_ms, mesh.probe_latency, virtual relay Phase 1 (shadow), relay pooling, hickory-resolver 0.25, sled eliminated (Wave 135) | Phase 2: flip virtual default, BTSP relay validation, TLS sovereignty (Phase C, horizon) |
| **biomeOS** v3.97 | L4 weighted routing, topology affinity, --tcp-only deprecated, HTTP removed, A/B shadow active, PathwayLearner, deep debt waves 71-72 (map_err sweep, test extraction 12 files) | A/B shadow analysis completion (1000 dispatches), perceptron shadow mode (needs barraCuda), String error types (GeneticsTier, EscalationManager) |
| **bearDog** v0.9.0 w129 | ring→aws-lc-rs, env migration COMPLETE (803+ constants), **grapheneGate keystore design** (KeystoreTransport trait, AndroidKeymaster variant, device detection), pure-Rust crypto horizon documented | S4 auth partner (7-day gate active), grapheneGate Phase 2 hardware wiring (NDK + device), pure-Rust crypto (P3) |

### 2B. biomeGate — OFFLINE (kernel recovery)

| Primal | Last State | Reassigned? |
|--------|------------|-------------|
| **toadStool** | Wave 68: PBDMA diagnostic, wgpu dispatch verified | **NO** — Titan V hardware-dependent, stays biomeGate |
| **coralReef** | Wave 68: SM120 barrier fix, SPIR-V prep | **PARTIAL** — SPIR-V compiler work → strandGate. SM120 Blackwell testing stays biomeGate |
| **barraCuda** | Wave 68: deep debt complete | **YES** — ml.mlp_train → strandGate (pure software) |

toadStool ownership stays biomeGate. Resume trigger: kernel recovery + cascade sync.
FRAGO: `wave72-strandgate-compute-trio-pickup` (supersedes `wave70-biomegate-down-compute-trio-paused`)

### 2C. strandGate — ACTIVE (provenance + compute trio pickup)

| Primal | Status |
|--------|--------|
| **loamSpine** | Tokio panic **FIXED**, anchoring pipeline **COMPLETE** |
| **rhizoCrypt** | Discovery fallback hardening **DONE** |
| **sweetGrass** | PROV-O completeness, privacy edge tests, store parity **DONE** |
| **barraCuda** (pickup) | ml.mlp_train implementation — 36-dim perceptron, pure software. **Unblocks** biomeOS L5 + primalSpring perceptron |
| **coralReef** (partial pickup) | SPIR-V output compiler (pure software). SM120 Blackwell testing remains biomeGate |

strandGate hardware: Dual EPYC 7452 (64c), 256GB ECC — ideal for pure-software compute work.
Hardware deployment (NUCLEUS) also proceeds on strandGate.

### 2D. ironGate — Sovereignty EXECUTED

| Project | Delivered | Remaining |
|---------|-----------|-----------|
| **cellMembrane** w71 | S1 verified, S4 activated, disk 60%, membrane on VPS, relay Rust-native, **legacy cascade() REMOVED**, **3 new commands** (relay.status, gate.health, content.verify), **S3 VPS READY** (Caddyfile configured, cutover = single DNS flip) | S4 monitoring (auto, ends ~Jun 9), NS cutover (operator), S3 cutover coord |
| **projectNUCLEUS** w71 | Shared registry, Forgejo CI primary, **genomeBin scaffold** (manifest + harvest.sh), biomeGate OFFLINE in gate_manifest, deep debt (unreachable!() eliminated, env-configurable ports) | Forgejo Actions CI evaluation (P2) |
| **projectFOUNDATION** w71 | **3 failing tests FIXED** (race conditions), **typed errors** (CliError enum, DegradationLevel enum, Box\<dyn Error\> eliminated), lineage counts synced (17,600+) | Validation workload freshness (P2), expression doc refresh |
| **NestGate** v0.5.0 s84b | /tmp centralized, doc hygiene, 12,522+ tests | Maintenance mode |
| **petalTongue** v1.6.8 | Error typing, Tokio narrowed (6 crates), dead code wired, cfg(test) accessors | Maintenance mode |

### 2E. flockGate

| Project | Delivered | Remaining |
|---------|-----------|-----------|
| **sporePrint** w70 | Zero-C deps, typed returns, paths module, 101 tests, source registry parity | S3 content cutover (post-DNS), NestGate CAS integration (P3) |

### 2F. eastGate

| Project | Status | Remaining |
|---------|--------|-----------|
| **primalSpring** v0.9.31 w71 | Security hardened (deny on missing scopes, real latency probes, per-primal cap validation), deprecated API migration (5 experiments), 842 tests | Live mesh test initiation, perceptron feature extraction (P2) |
| **squirrel** | Stable | Maintenance |
| **skunkBat** | Stable | Maintenance |

---

## Track 3: Dependency Evolution — LARGELY COMPLETE

| Dependency | Status |
|------------|--------|
| sled → redb | **N/A** — sled eliminated from Songbird (Wave 135), never in rhizoCrypt |
| ring → aws-lc-rs | **DONE** — bearDog Wave 125, deny.toml bans ring |
| rustls-pemfile | **DONE** — absorbed into cert stack |
| loamSpine Tokio panic | **DONE** — already fixed |
| neuralSpring target/release hardcode | Open (P3, low priority) |
| bincode 1.x RUSTSEC | Open — blocked on tarpc upstream (not actionable) |
| hickory-resolver 0.26 | Deferred — upstream SRV/TXT API unstable |

---

## Track 4: Strategic Evolution

### 4A. Songbird Routing Consolidation

| Phase | Status |
|-------|--------|
| A: TCP Tier 5 elimination | **DONE** |
| B: Virtual endpoint relay | **Phase 1 LIVE** (shadow mode, opt-in). Phase 2: flip default, BTSP validation, connection pooling |
| C: Membrane TLS sovereignty | Horizon — post S1 graduation |

### 4B. Neural API Perceptron

| Phase | Status |
|-------|--------|
| L4 weighted selection | **DONE** (biomeOS v3.94) |
| L4 topology affinity | **DONE** (biomeOS v3.94) |
| A/B shadow analysis | **ACTIVE** (1000 dispatch counter running) |
| PathwayLearner feedback | **WIRED** (per-node graph execution timing) |
| L5 perceptron training | **BLOCKED** — needs barraCuda ml.mlp_train (biomeGate down) |

### 4C. grapheneGate Trust Anchor

| Role | Status |
|------|--------|
| Manifest + standard | **DONE** |
| Role 1: Beacon | P2 — bearDog keystore design needed first |
| Role 2: BTSP Relay | P3 |
| Role 3: Mesh Seed | Horizon |

### 4D. Topology-Aware Routing

| Phase | Status |
|-------|--------|
| A: TOPOLOGY_MAP.toml + latency discovery | **DONE** |
| B: Locality-biased routing | **DONE** (biomeOS topology affinity factor) |
| C: Segment-aware deployment | Horizon |

---

## Track 5: Infrastructure Expansion (P3)

strandGate ACTIVATED for compute trio pickup. westGate expected back online this week.

| Gate | Planned Role | Status | Blocker |
|------|-------------|--------|---------|
| strandGate | Provenance trio + compute trio pickup (barraCuda, coralReef SPIR-V) | **ACTIVE** — assigned via FRAGO wave72 | NUCLEUS deployment needed |
| westGate | 76TB ZFS cold storage (Nest Atomic) | **INCOMING** — ETA this week | Gate setup + NUCLEUS deploy |
| northGate | Heavy compute, AI/LLM | Hardware ready | No blocker (P3) |
| swiftGate | Mobile/compact | Hardware ready | No blocker (P4) |
| kinGate | Staging | Hardware ready | No blocker (P4) |

---

## Immediate Critical Path (Priority Order)

1. **eastGate mesh validation** — paired test with southGate. Both ready.
2. **S4 Auth 7-day gate** — running autonomously, ends ~Jun 9.
3. **DNS NS registrar cutover** — operator manual action.
4. **S1 TLS graduation** — after NS cutover, remove Cloudflare.
5. **S3 content cutover** — after DNS, sporePrint targets VPS directly.
6. **strandGate compute trio pickup** — barraCuda ml.mlp_train + coralReef SPIR-V (pure software).
7. **westGate bring-up** — ETA this week. 76TB ZFS cold storage (Nest Atomic).
8. **biomeGate recovery** — toadStool + coralReef Blackwell testing resume when kernel is fixed.

---

## Decision Log (Wave 70 additions)

| Decision | Rationale | Wave |
|----------|-----------|------|
| Compute trio PAUSED, not transferred | Hardware-dependent work blocked; software items available for opportunistic pickup | 70 |
| strandGate FRAGO archived | All items resolved by upstream teams | 70 |
| 3 biomeGate FRAGOs consolidated | Superseded by single wave70 pause FRAGO | 70 |
| Wave 68 remaining work archived | Superseded by this document | 70 |
| Compute trio → strandGate (partial) | barraCuda (full) + coralReef SPIR-V (partial) moved to strandGate. toadStool stays biomeGate (hardware). | 72 |
| westGate incoming | ETA this week. 76TB ZFS cold storage, Nest Atomic role. | 72 |

---

*Wave 72. strandGate activated for compute trio software work. westGate incoming this week.
Two operator actions remain on the glacial critical path. Everything else is delivered,
running autonomously, or paused with clear resume triggers.*
