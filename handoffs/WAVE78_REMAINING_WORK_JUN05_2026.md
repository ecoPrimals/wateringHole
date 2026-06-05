# Wave 78 Remaining Work — Full Parity & Mesh Deployment

**Date**: 2026-06-05  
**Author**: eastGate overwatch  
**Supersedes**: Wave 76 remaining work (archived)  
**Status**: Active  
**Updated**: Wave 78 — diderm membrane live, SB-TLS-01/02 resolved, BD-TRUST-01 delivered

---

## Strategic Context

Wave 77 delivered the diderm membrane architecture (3-layer sovereign TLS),
NUCLEUS deep debt evolution (TOML-driven routing, profile-driven launcher,
zero C deps), and live cross-gate trust chain proof (eastGate ↔ strandGate).

Wave 78 upstream deliveries resolved the two highest-priority blockers:
- **SB-TLS-01**: Songbird direct-mode TLS crypto routing (symmetric mesh unblocked)
- **SB-TLS-02**: Phase 3.5 Ed25519 relay signature verification shipped
- **BD-TRUST-01**: bearDog `auth.exchange_trust` (zero-operator trust seeding)
- **RC-POLL-01**: rhizoCrypt `MeshEventListener` polling wired

**Remaining critical path**: Wire `auth.exchange_trust` into Songbird `mesh.init`
→ 3-gate mesh proof → stadial entry.

---

## Ecosystem Freshness Assessment (Jun 5, 2026)

### Tier 1: HOT — Current Wave 77-78 (delivered Jun 3-5)

| Repo | Gate | Version/Wave | Delivery |
|------|------|--------------|----------|
| bearDog | southGate | v0.9.0 / w140 | `auth.exchange_trust`, auto trust seeding |
| songBird | southGate | v0.2.9-w79 | SB-TLS-01 fix, Phase 3.5 Ed25519, retry hardening |
| biomeOS | southGate | v4.07 / w77 | Perceptron training data pipeline |
| toadStool | biomeGate | S290 | CallerContext fan_out, coordination feature-gate |
| sweetGrass | strandGate | v0.7.48 / w78b | Zero hot-path env reads |
| rhizoCrypt | strandGate | v0.14.1 / w77e | MeshEventListener polling (RC-POLL-01) |
| loamSpine | strandGate | w76 | Trust ledger IPC wired |
| NestGate | ironGate | v0.5.0 / s93 | HTTP parity, content serving |
| coralReef | strandGate | v0.2.0 / w78 | Mesh propagation, SPIR-V E2E |
| petalTongue | ironGate | v1.6.6 / w77d | Typed errors, MIME notebook |
| skunkBat | eastGate | v0.2.2 | defense.status health probe |
| primalSpring | eastGate | w77d | UDS registry fix, deep debt, gap docs |
| wateringHole | eastGate | w78 | Overwatch, fossilized wave77 handoffs |
| cellMembrane | ironGate | w77b | Peptidoglycan formalization |
| barraCuda | strandGate | v0.4.0 / w76 | ML pipeline, mesh.trust_verify |

### Tier 2: WARM — 3-6 Days Behind Wave 78

| Repo | Gate | Last Wave | Gap | Parity Work Needed |
|------|------|-----------|-----|-------------------|
| wetSpring | southGate | w77 (Jun 4) | 1d | V196 forward evolution. southGate health 11/13. |
| neuralSpring | southGate | w76 (Jun 3-4) | 1-2d | V179 deep debt done. southGate mesh needs stabilization. |
| healthSpring | ironGate | w76 (Jun 2) | 3d | V65c glacial cutover done. Absorb Wave 78 patterns. |
| ludoSpring | ironGate | w76 (Jun 3) | 2d | V82 parity done. CONTEXT.md stale, no domain_profile.toml. |
| squirrel | eastGate | w76 (Jun 3) | 2d | 7,098 tests. Env centralization done. |

### Tier 3: COOL — 5+ Days Behind

| Repo | Gate | Last Wave | Gap | Parity Work Needed |
|------|------|-----------|-----|-------------------|
| airSpring | eastGate | w60 (May 29) | 7d | v0.10.0, 1,446 tests. Not on parity sprint. |
| groundSpring | eastGate | w63 (May 30) | 6d | V146, 1,123 tests. Squirrel integration done. |
| hotSpring | biomeGate | S284 (Jun 1) | 4d | v0.6.32, L6. Separate sovereign-compute track. |

### Tier 4: DORMANT (evolve on demand)

| Repo | Last Commit | Assessment |
|------|------------|------------|
| sourDough | Jun 4 | Meta-primal, scaffold tool. Current. |
| bingoCube | May 20 | Validation tool. Hygiene when convenient. |
| rustChip | Apr 30 | Utility crate. Not blocking. |

---

## Parity Gaps — Cross-Cutting

### Missing `domain_profile.toml` (3 springs)

Springs need root `domain_profile.toml` for `litho emit-pseudospore` and
ecosystem classification.

| Spring | Status |
|--------|--------|
| hotSpring | Has nested compchem profiles, no root profile |
| ludoSpring | Missing — composition-only spring |
| neuralSpring | Missing |

### Missing `capability_registry.toml` (6 primals)

Machine-readable TOML registry enables primalSpring `DOMAIN_OWNER_MAP` and
ecosystem tooling to auto-discover capabilities.

| Primal | Current State | Priority |
|--------|---------------|----------|
| songBird | `consumed_capabilities` in code only | MEDIUM |
| toadStool | `provided_capabilities` in handlers | MEDIUM |
| barraCuda | Inline in `primal.rs` | LOW |
| coralReef | Self-knowledge in code/CONTEXT | LOW |
| loamSpine | `CONSUMED_CAPABILITIES` in `niche.rs` | LOW |
| skunkBat | `CONSUMED_CAPABILITIES` in `dispatch.rs` | LOW |

### Coverage vs 90% Stadial Target

| Met (≥90%) | Below |
|------------|-------|
| bearDog (90.5%), biomeOS (90%+), squirrel (90.1%), sweetGrass (91.7%), loamSpine (90.9%), sourDough (95%+), skunkBat (90%+ fn) | **songBird (73%)**, nestGate (84%), petalTongue (~85%), toadStool (~84%), barraCuda (81% llvmpipe) |

---

## Remaining Work by Track

### Track 1: Parity Sprint — COMPLETE ✓ (Wave 76)

All teams absorbed Wave 76 trust infrastructure. 20 handoffs archived.

### Track 2: Live Cross-Gate Validation — PROVEN ✓ (Wave 77d)

Full trust chain proven live: eastGate ↔ strandGate via Songbird mesh +
bearDog ionic tokens + rhizoCrypt DAG provenance.

### Track 3: Diderm Membrane — LIVE ✓ (Wave 77-78)

| Layer | Domain | Status | TLS |
|-------|--------|--------|-----|
| Outer Membrane | primals.eco | LIVE (sporePrint) | Cloudflare |
| Inner Membrane | primal.eco | LIVE | Let's Encrypt (sovereign) |
| Content Layer | nestgate.io | LIVE | Let's Encrypt (sovereign) |
| Peptidoglycan (VPS) | golgiBody/golgiBody-ext | LIVE | Sovereign knot-dns |

### Track 4: Mesh Deployment (P0 — current critical path)

| Step | Owner | Status |
|------|-------|--------|
| Wire `auth.exchange_trust` in Songbird `mesh.init` | Songbird | **READY** — bearDog W140 + SB-TLS fix unblock |
| 3-gate mesh proof (eastGate + strandGate + westGate/southGate) | primalSpring overwatch | **UNBLOCKED** |
| S4 auth 7-day gate completion | bearDog + ironGate | ~Jun 9 |
| westGate enrollment | skunkBat + eastGate | Hardware pending |
| southGate 13/13 stabilization | wetSpring / neuralSpring ops | **INVESTIGATING** |

### Track 5: Caddy Reverse Proxy Wiring (P1)

| Endpoint | Backend | Status |
|----------|---------|--------|
| nestgate.io /content/* | Forgejo localhost:3000 | PENDING |
| mesh.primal.eco | Songbird 157.230.3.183:7700 | PENDING |
| auth.primal.eco | bearDog | PENDING |
| api.primal.eco | biomeOS neural-api | PENDING |

### Track 6: Lagging Codebase Parity (P2)

| Codebase | Gap | Action |
|----------|-----|--------|
| airSpring | Wave 60 → 78 (7d behind) | Trust pattern absorption, Wave 78 alignment |
| groundSpring | Wave 63 → 78 (6d behind) | Trust pattern absorption |
| songBird | 73% coverage (vs 90% target) | Coverage sprint — largest quantitative gap |
| hotSpring | Separate track, no root domain_profile.toml | Create root domain_profile.toml |
| ludoSpring | CONTEXT.md stale, no domain_profile.toml | Doc update + profile creation |
| neuralSpring | No domain_profile.toml | Profile creation |

### Track 7: Ongoing Evolution (P3)

| Work | Owner | Notes |
|------|-------|-------|
| biomeGate full NUCLEUS (9→13) | hotSpring + ops | PLANNED |
| northGate deployment planning | — | Heavy compute / AI |
| grapheneGate bootstrap | — | Portable trust anchor |
| Cloudflare → sovereign content cutover | cellMembrane | After Caddy wiring |

---

## Sovereignty Shadow Status

| Track | Status | Next Step |
|-------|--------|-----------|
| S1 TLS | **LIVE** (sovereign LE on primal.eco + nestgate.io) | Caddy reverse proxy wiring |
| S2 NAT | **GRADUATED** | Complete |
| S3 Content | READY (67ms TTFB, 101 tests) | Wire nestgate.io → Forgejo content |
| S4 Auth | 7-DAY GATE ACTIVE (started Jun 2, ends ~Jun 9) | Wait → graduate |

---

## Active FRAGOs

| FRAGO | From→To | Status |
|-------|---------|--------|
| `wave73-westgate-skunkbat-enrollment` | eastGate→westGate | **PENDING** — hardware incoming |

---

## Upstream Gap Summary

| Gap | Status |
|-----|--------|
| ~~SB-TLS-01~~ | **RESOLVED** — Songbird direct-mode TLS crypto |
| ~~SB-TLS-02~~ | **RESOLVED** — Phase 3.5 Ed25519 relay verification |
| **BD-TRUST-01** | bearDog DELIVERED `auth.exchange_trust`. **Needs Songbird mesh.init integration.** |
| ~~RC-POLL-01~~ | **RESOLVED** — rhizoCrypt MeshEventListener polling wired |

**Only remaining P1 gap**: BD-TRUST-01 Songbird integration (bearDog side complete).

---

*"The fastest teams wait for the slowest. The glacier moves as one."*
