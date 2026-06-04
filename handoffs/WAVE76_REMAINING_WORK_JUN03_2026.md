# Wave 76 Remaining Work — Ecosystem Parity Sprint

**Date**: 2026-06-03  
**Author**: eastGate overwatch  
**Supersedes**: Wave 70 remaining work (archived)  
**Status**: Active

---

## Strategic Context

Wave 75-76 delivered the cross-gate trust infrastructure in a coordinated
push across all frontline teams. The mesh is now trust-aware: bearDog can
verify remote tokens, Songbird propagates capabilities, NestGate verifies
content integrity, and the compute trio protects methods behind BTSP.

**Before the next deployment steps** (DNS cutover, westGate enrollment,
live cross-gate validation), the ecosystem needs a parity sprint. Several
teams — particularly springs and the provenance trio — predate the trust
infrastructure wave and need alignment passes.

---

## Ecosystem Freshness Assessment (as of Jun 3 16:00 EDT)

### Tier 1: HOT — Current (20 repos, evolved today)

These teams delivered trust infrastructure. Next work: deep debt, hygiene,
or wait for lagging teams to catch up.

| Repo | Gate | Version | Wave 76 Delivery |
|------|------|---------|-----------------|
| bearDog | southGate | w135 | Cross-gate trust model (TrustedIssuerRegistry, Ed25519, multi-issuer) |
| Songbird | southGate | w75 | Capability propagation fix, HTTP/UDS unification, relay Phase 3 |
| biomeOS | southGate | v4.03 | Env alignment, AtomicType dedup, typed errors |
| toadStool | biomeGate (remote) | S286 | dispatch.verify_trust, telemetry schema, yield-to-owner |
| barraCuda | strandGate | w75 | Full ML pipeline (train→save→load→infer), mesh.trust_verify |
| coralReef | strandGate | w75 | Artifact provenance headers |
| NestGate | ironGate | s90 | BLAKE3 content trust in federation pull |
| cellMembrane | ironGate | w75 | Relay trust boundary spec |
| projectNUCLEUS | ironGate | w75 | Deploy graph trust validation |
| petalTongue | ironGate | w74+ | TRUE PRIMAL compliance, AppError typed |
| esotericWebb | ironGate | w73 | Mesh registration, coverage |
| projectFOUNDATION | eastGate | w74 | Drift detection, guideStone spec |
| primalSpring | eastGate | w75 | Cross-gate trust validation scenarios |
| sporePrint | flockGate | auto | Content auto-merge |
| plasmidBin | eastGate | w75 | Capability symlinks |
| wateringHole | eastGate | w76 | Overwatch codified, trust absorption |
| whitePaper | eastGate | w76 | Gen5 trust + overwatch papers |

### Tier 2: WARM — 1-2 Days Behind (8 repos)

These need alignment blurbs. They predate the capability propagation fix
and the cross-gate trust model.

| Repo | Gate | Last Commit | Gap | Parity Work |
|------|------|------------|-----|-------------|
| healthSpring | ironGate | Jun 2 | 1d | Composition vocabulary done. Absorb trust patterns. |
| sweetGrass | strandGate | Jun 2 | 1d | v0.7.44 PROV-O. Wire cross-gate attribution schema. |
| rhizoCrypt | strandGate | Jun 2 | 1d | w69 discovery fallback. Wire cross-gate DAG events. |
| loamSpine | strandGate | Jun 2 | 1d | w69 panic fix. Anchor cross-gate trust events. |
| hotSpring | biomeGate | Jun 1 | 2d | Hardware-blocked. Software alignment if possible. |
| neuralSpring | southGate | Jun 1 | 2d | w67 capability.call. Absorb Songbird w75 propagation. |
| wetSpring | southGate | Jun 1 | 2d | w67 cutover. Absorb bearDog w135 trust patterns. |
| ludoSpring | ironGate | Jun 1 | 2d | w67 cutover. Absorb NestGate s90 content trust. |

### Tier 3: COOL — 3-6 Days Behind (7 repos)

These predate the entire Wave 73+ sprint. Lower priority but some are
deployment-critical (skunkBat for westGate, benchScale for validation).

| Repo | Gate | Last Commit | Gap | Parity Work |
|------|------|------------|-----|-------------|
| airSpring | eastGate | May 31 | 3d | Domain profile done. Low priority — not mesh-critical. |
| lithoSpore | strandGate | May 30 | 4d | Product — evolves on demand. Not blocking. |
| groundSpring | eastGate | May 30 | 4d | Squirrel integration. Low priority — not mesh-critical. |
| squirrel | eastGate | May 29 | 5d | Env centralization. Mesh awareness next. |
| benchScale | eastGate | May 29 | 5d | Cross-gate test topology needed for live validation. |
| agentReagents | eastGate | May 29 | 5d | Container images. Trust validation containers. |
| skunkBat | eastGate | May 28 | 6d | westGate deployment primal. Needs freshening. |

### Tier 4: DORMANT (2 repos)

| Repo | Gate | Last Commit | Gap | Assessment |
|------|------|------------|-----|------------|
| bingoCube | eastGate | May 20 | 14d | Validation tool. Hygiene pass when convenient. |
| rustChip | eastGate | Apr 30 | 34d | Utility crate. Not blocking anything. |

### Products (evolve on collaborator demand, not infrastructure waves)

| Product | Last Commit | Status |
|---------|------------|--------|
| esotericWebb | Jun 3 | Active (ironGate) |
| sporePrint | Jun 3 | Active (flockGate, auto-merge) |
| helixVision | May 28 | Seed only — awaits Gonzales NF data |
| blueFish | May 28 | Seed only — awaits Jones PFAS pipeline |
| initioChem | May 28 | Seed only — ABG pseudoSpore delivered |
| lithoSpore | May 30 | Barrick LTEE — lab adoption pending |

---

## Remaining Work by Track

### Track 1: Parity Sprint (P0 — do before deployment)

**Goal**: Bring lagging teams to Wave 76 awareness so compositions work
with the new trust-aware mesh infrastructure.

| Team | Gate | Work | Priority |
|------|------|------|----------|
| neuralSpring | southGate | Absorb Songbird w75 propagation. Verify capability.call scenarios pass with new push model. Deep debt if clear. | P1 |
| wetSpring | southGate | Absorb bearDog w135 trust patterns. Verify compositions pass with new verify_ionic. Deep debt if clear. | P1 |
| healthSpring | ironGate | Verify compositions pass with NestGate s90 content trust. Deep debt if clear. | P1 |
| ludoSpring | ironGate | Verify compositions pass. Deep debt if clear. | P1 |
| sweetGrass | strandGate | Wire cross-gate attribution schema. Prepare for multi-gate provenance braids. | P1 |
| rhizoCrypt | strandGate | Wire cross-gate DAG event types. Session events for trust establishment. | P1 |
| loamSpine | strandGate | Anchor schema for cross-gate trust events. Ledger entries for key exchange. | P1 |
| skunkBat | eastGate | Freshen for westGate deployment. Verify defense.status works. | P2 |
| benchScale | eastGate | Cross-gate test topology definition for live validation. | P2 |

### Track 2: Live Cross-Gate Validation (P0 — after parity)

**Goal**: Prove the full chain works end-to-end.

| Work | Owner | Dependency |
|------|-------|-----------|
| Live `capability.call` from Gate A → Gate B with BTSP | primalSpring (overwatch) | Parity sprint complete |
| `s_covalent_mesh` scenario with security properties | primalSpring evolution | bearDog w135 + Songbird w75 |
| Content federation BLAKE3 end-to-end test | NestGate + benchScale | NestGate s90 |
| biomeOS L5 perceptron shadow mode | biomeOS + barraCuda | barraCuda ML pipeline |

### Track 3: Deployment Steps (P1 — after validation)

| Step | Owner | Blocker |
|------|-------|---------|
| DNS NS registrar cutover | Operator (manual) | — |
| S1 TLS graduation (remove Cloudflare) | cellMembrane | DNS cutover |
| S3 content cutover (sporePrint sovereign) | sporePrint + cellMembrane | DNS cutover |
| S4 auth 7-day gate completion | bearDog + ironGate | Time (~Jun 9) |
| westGate enrollment | skunkBat + eastGate | Hardware arrival |
| Songbird relay Phase 3.5 (full Ed25519) | Songbird + bearDog | bearDog w135 (done) |

### Track 4: Ongoing Evolution (P2 — continuous)

| Work | Owner | Notes |
|------|-------|-------|
| Hot teams deep debt / hygiene | bearDog, Songbird, barraCuda, NestGate, cellMembrane, toadStool, coralReef | Zero debt → forward evolution |
| biomeGate kernel recovery | Operator | Unblocks toadStool GPU dispatch |
| northGate deployment planning | — | Heavy compute / AI |
| grapheneGate bootstrap | — | Portable trust anchor |

---

## Sovereignty Shadow Status

| Track | Status | Next Step |
|-------|--------|-----------|
| S1 TLS | VERIFIED (198 probes, 0 failures) | DNS cutover → remove Cloudflare |
| S2 NAT | **GRADUATED** | Complete |
| S3 Content | READY (67ms TTFB, 101 tests) | DNS cutover → sporePrint cutover |
| S4 Auth | 7-DAY GATE ACTIVE (started Jun 2, ends ~Jun 9) | Wait → graduate |

---

## Active FRAGOs

| FRAGO | From→To | Status |
|-------|---------|--------|
| `wave72-strandgate-compute-trio-pickup` | eastGate→strandGate | **COMPLETE** — barraCuda + coralReef delivered. Archive pending. |
| `wave73-westgate-skunkbat-enrollment` | eastGate→westGate | **PENDING** — hardware incoming |
| `wave76-parity-sprint` (NEW) | eastGate→all | **ACTIVE** — springs + provenance trio alignment |

---

## Assessment

The ecosystem is in a **post-burst consolidation** phase. The frontline
teams (southGate, strandGate, ironGate) executed a remarkable coordinated
trust infrastructure delivery in Wave 75-76. But the springs (the validation
backbone), the provenance trio (the recording layer), and several eastGate
utilities haven't absorbed any of it yet.

**The risk**: if we push to live cross-gate validation or DNS cutover before
springs and provenance are aligned, compositions may fail against the new
trust-aware services, and trust events won't be properly recorded.

**The plan**: parity sprint first, then validate, then deploy.

---

*"The fastest teams wait for the slowest. The glacier moves as one."*
