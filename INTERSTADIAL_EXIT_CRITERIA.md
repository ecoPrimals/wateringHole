<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Interstadial Exit Criteria — Full Sovereignty Pre-Wire

**Version**: 1.5 — May 13, 2026 (418 methods. Tower LIVE 6/6. H2-12 TLS shadow LIVE. lithoSpore 6/7 Tier 2. Wire routing fixed: 76 misroutes resolved, base64 encoding, routing consistency scenario)
**Status**: Active
**Phase**: Interstadial (entered April 16, 2026; exit gate defined here)

---

## Strategic Frame

The **interstadial** is the warm period between stadial advances. During this
phase the ecosystem pre-wires sovereignty capabilities — the plumbing that
enables external validation. The interstadial ends when sovereignty is
structurally wired and shadow runs can begin.

The **stadial** is the cold advance — external pressure (Cloudflare baselines,
upstream peers, Barrick Lab, community frameworks) drives evolution through
real-world validation. The stadial does not start until the interstadial exit
gate is cleared.

```
INTERSTADIAL (current)                    STADIAL (next)
├── Pre-wire sovereignty capabilities     ├── Shadow runs vs Cloudflare
├── NUCLEUS deployments ready             ├── Upstream crate contributions
├── ABG hosting compositions              ├── Community engagement (Dimforge)
├── lithoSpore Phase 2 started            ├── lithoSpore USB to Barrick Lab
└── River delta Tier 4 exemplars          └── Framework parity benchmarks
         │                                         │
         └──── EXIT GATE ─────────────────────────►│
               (capabilities wired,
                shadow runs can begin)
```

---

## Five Pillars

### Pillar 1: Primal Sovereignty Capabilities (Sentinel-Stadial)

Primals are **sentinels** — the least composed, most climate-responsive entities.
They have already shipped their capabilities and are in their own stadial cycle,
with primalSpring as their validation gate. The remaining items here split into
two categories: **upstream debt** (primal code gaps at the gate) and
**downstream absorption** (L3/L4 integration work using shipped capabilities).

**Upstream debt (blocked at the primalSpring gate):**

~~One critical gap exposed by downstream composition~~ **RESOLVED** (May 11, 2026):

- ~~NestGate `content.put` transport parity~~ **RESOLVED** (Session 60) — all 8
  `content.*` methods (`put`, `get`, `exists`, `list`, `publish`, `resolve`,
  `promote`, `collections`) now wired on all 4 transport surfaces (primary
  dispatch, SemanticRouter, isomorphic IPC, HTTP API). `lifecycle.status` also
  added. See `fossilRecord/handoffs-may11-2026-wave9-closure/NESTGATE_SESSION60_TRANSPORT_PARITY_HANDOFF_MAY11_2026.md`.

**All** primals pass the gate:
- MethodGate (JH-0 + JH-2): **13/13** — squirrel shipped `method_gate.rs`
- BTSP Phase 3 AEAD: **13/13**
- 418-method registry: zero drift
- Edition 2024, deny.toml (ring + openssl), plasmidBin: **13/13**

**Downstream-surfaced per-primal debt (composition gaps, not gate-blocking):**

| # | Primal | Finding | Status |
|---|--------|---------|--------|
| D1 | toadStool | ~~No env-var expansion~~ — S234 documents IPC contract as pre-resolved only | **RESOLVED** |
| D2 | squirrel | ~~`LocalProcessProvider` spawns directly~~ — `RemoteComputeProvider` for toadStool IPC shipped | **RESOLVED** |
| D3 | barraCuda | ~~Embeds own crypto~~ — bearDog Wave 101 shipped `crypto.hkdf_sha256` + `crypto.hmac_verify` IPC | **RESOLVED** |
| D4 | loamSpine | ~~`session.commit` mismatch~~ — method aliases + hex hash acceptance | **RESOLVED** |
| D5 | petalTongue | ~~Web mode blocked on NestGate~~ — SPA + CORS shipped, NestGate transport parity shipped | **RESOLVED** |

**Downstream absorption (shipped capabilities awaiting wiring):**

| # | Capability | Primal | Shipped | Absorption Owner |
|---|-----------|--------|---------|-----------------|
| 1a | TLS termination + rate limits | BearDog | Yes (Wave 100) | L4 (NUCLEUS): H2-3b shadow on :8443 |
| 1b | NAT chain (STUN/TURN) | Songbird | Yes (Waves 196-197) | L4 (NUCLEUS): H2-3c VPS relay |
| 1c | Content pipeline (`content.put`) | NestGate | **RESOLVED** (Session 60) | ~~L1 debt~~ → L4 absorption: wire `publish_sporeprint.sh` |
| 1d | Web mode (`--docroot`) | petalTongue | **UNBLOCKED** (SPA+CORS shipped, NestGate transport parity shipped) | L4 (NUCLEUS): H2-3a NestGate-backed static |
| 1e | BTSP authenticator | BearDog | Ready | L4 (NUCLEUS): H2-2b JupyterHub plugin |
| 1f | `composition.deploy(graph)` | biomeOS | API exists | L4 (NUCLEUS): gate wiring, membrane signals |
| 1g | Audit forwarding (JH-5) | skunkBat | **Phase 3 shipped** | ~~L3/L4~~ → L4 absorption: deploy graph integration |
| 1h | Cross-primal tokens (JH-11) | BearDog | Done | L3 (Springs): CompositionContext wiring |
| 1j | Sovereign DNS | Songbird/BearDog | DoT intermediate | L4 (NUCLEUS): H2-4 knot-dns (can defer to stadial) |

**Exit gate**: MethodGate **13/13 DONE**. NestGate transport parity **RESOLVED**
(Session 60). **Zero L1 upstream debt remains.** All Pillar 1 items are now either
resolved or L4 absorption work (BearDog TLS shadow, Songbird NAT relay, BTSP
dual-auth, deploy graph wiring). 1j (full sovereign DNS) may defer to stadial.

### Pillar 2: projectNUCLEUS Deployments

| # | Target | Current State | Interstadial Remaining |
|---|--------|---------------|----------------------|
| 2a | BTSP auth live (dual-auth period) | **CODE BUILT** (jupyterhub_btsp_auth.py + deploy script) | Start shadow period |
| 2b | BearDog TLS on :8443 | **SHADOW LIVE** (H2-12) | Measure parity vs Cloudflare |
| 2c | Songbird NAT operational | **cellMembrane VPS OPERATIONAL** — Songbird relay + RustDesk deployed, multi-gate SSH, hardened (fail2ban, droplet-agent purged) | Measure parity vs cloudflared |
| 2d | NestGate extracellular | GitHub Pages | Content pipeline serving `primals.eco` |
| 2e | Foundation workloads | **10/10 threads ACTIVE** | Threads 9+10 seeded by ludoSpring/healthSpring |
| 2f | lithoSpore workload dispatched | **6/7 modules Tier 2 LIVE** | ecoBin ingestion active |
| 2g | DoT baseline | **FIXED** (10/10 success) | Tunnel baseline clarified — not a bug |

**Exit gate**: H2-12 (BearDog TLS shadow) **LIVE** — shadow infrastructure running.
DoT baseline fixed (10/10 success). Foundation 10/10 threads active. lithoSpore
Pillar 4 **EXCEEDED** (6/7 Tier 2). Cutover is stadial work — shadow comparison
data accruing.

**Membrane channels**: Items 2b-2d map to the three membrane channels defined in
`MEMBRANE_CHANNEL_ARCHITECTURE.md`: 2b = Channel 3 (Surface/TLS), 2c = Channel 2
(Relay/NAT), 2d = Channel 3 (Surface/content). All deploy on a single VPS
(Model A) or tiered across providers (Model B).

### Pillar 3: ABG Hosting

| # | Target | Current State | Interstadial Remaining |
|---|--------|---------------|----------------------|
| 3a | ABG workspace on gate | Live (membrane + JupyterHub) | Maintenance |
| 3b | Foundation Thread 1 validation | Operational (genome/proteome/KEGG) | Expand to full Karr 2012 composition pipeline |
| 3c | ABG tier enforcement | Validated (darkforest pentest) | Maintenance |
| 3d | WCM compositions via NUCLEUS | Mapped in `ABG_WHOLE_CELL_REBUILD.md` | Exercise through deploy graphs with provenance trio |

**Exit gate**: Thread 1 WCM compositions exercised through NUCLEUS deploy
graphs (Nest + Node atomics) with provenance trio producing verifiable output.

### Pillar 4: lithoSpore

| # | Target | Current State | Interstadial Remaining |
|---|--------|---------------|----------------------|
| 4a | Spring LTEE paper queue started | **ACTIVE** — 4 springs reproducing | Continue B3+ reproductions |
| 4b | At least 2 modules functional | **ACTIVE** — ltee-fitness (Module 1) + ltee-mutations (Module 2) integrating groundSpring B2+B1 | Validate PASS at Tier 1 |
| 4c | Data fetched and hashed | **ACTIVE** — `fetch_wiser_2013.sh` + `fetch_barrick_2009.sh` shipped, `fitness_data.csv` + `mutation_parameters.json` in tree | BLAKE3-hash into NestGate |
| 4d | Python Tier 1 baselines running | **ACTIVE** — `power_law_fitness.py` (244L) + `mutation_accumulation.py` (210L) expanded, `expected/module1_fitness.json` + `module2_mutations.json` shipped | Run validation, confirm PASS |

LTEE reproduction status (May 13):
- **groundSpring**: B2 (Wiser 2013) Python 9/9 + Rust 10/10 PASS; B1 (Barrick 2009) Python 8/8 + Rust 8/8 PASS
- **hotSpring**: B2 (Anderson fitness) STARTED — Exp 189, notebook shipped
- **wetSpring**: B7 (Tenaillon 2016) **Tier 2 COMPLETE** — 264 NCBI genomes, guideStone L5
- **neuralSpring**: B1 (Barrick 2009) STARTED — Python baseline 8/8 PASS

**GATE EXCEEDED** (May 13): lithoSpore **6/7 modules at Tier 2 LIVE**, ecoBin
compliant. `litho-core` shared libraries extracted (`discovery`, `harness`, `stats`).
BLAKE3 `pure` feature resolved. 14 deep-debt items resolved in CATHEDRAL audit.
**groundSpring B2+B1 reproductions complete**; wetSpring B7 at Tier 2.

### Pillar 5: River Delta (Springs) — **GATE MET** (May 11, 2026)

| # | Target | Current State | Status |
|---|--------|---------------|--------|
| 5a | Tier 4: 4+ springs `optional=true` | **8/8** — all springs IPC-first (`default = []`) | **DONE** |
| 5b | wetSpring PG gaps below 5 | **4 open** (PG-02, PG-03, PG-04, PG-05 — all external) | **DONE** |
| 5c | guidestone convergence | airSpring **L4**, neuralSpring **L5**, wetSpring **L5** | **EXCEEDED** |
| 5d | Foundation seeding | **10/10** threads active (9+10 seeded by ludoSpring V71 + healthSpring V64m) | **EXCEEDED** |
| 5e | plasmidBin: all springs staged | 6/8 staged (ludoSpring composed, primalSpring special) | On track |
| 5f | LTEE paper queue progress | **4 springs reproducing** (groundSpring B2+B1 DONE, hotSpring B2, wetSpring B7, neuralSpring B1) | **DONE** |
| 5g | CompositionContext wiring | PrimalClient encapsulated (L2 design) | L2 coordination pass pending |

**Exit gate**: **ALL conditions met.** 8/8 Tier 4, wetSpring at 4 PG (below 5),
airSpring L4, neuralSpring L5 (exceeded L4 target), 10/10 foundation threads active
(EXCEEDED), LTEE reproductions active across 4 springs.

---

## Interstadial Exit Gate — Summary Checklist

```
[x] Pillar 1: NestGate `content.*` transport parity (Session 60, May 11) — all 8 methods on all 4 surfaces
[x] Pillar 1: BearDog TLS shadow running on :8443 — H2-12 LIVE
[x] Pillar 1: Songbird NAT + VPS relay operational — cellMembrane VPS deployed (Songbird + RustDesk + multi-gate SSH)
[x] Pillar 1: petalTongue web mode + NestGate backend — UNBLOCKED (SPA+CORS shipped, NestGate transport parity shipped)
[~] Pillar 1: BTSP auth dual-auth — code built, shadow period pending
[x] Pillar 1: JH-5 audit forwarding wired — skunkBat Phase 3 shipped (rhizoCrypt + sweetGrass forwarding)
[x] Pillar 1: MethodGate 13/13 (squirrel shipped May 11)
[x] Pillar 1: Wire routing fixes — security.audit_log→defense, crypto base64 encoding (May 13)
[~] Pillar 2: H2-2b/3a/3b/3c all in shadow-run state — H2-12 TLS LIVE, DoT FIXED, others pending
[x] Pillar 2: Foundation 10/10 threads active (Threads 9+10 seeded by ludoSpring V71 + healthSpring V64m)
[ ] Pillar 3: Thread 1 WCM compositions through provenance trio
[x] Pillar 4: lithoSpore 6/7 modules Tier 2 LIVE (EXCEEDED Tier 1 target). ecoBin compliant.
[x] Pillar 4: Real data fetched from Dryad/NCBI — Wiser 2013 + Barrick 2009 in tree
[x] Pillar 5: 8/8 springs at barraCuda optional=true (exceeded 4+ target)
[x] Pillar 5: wetSpring 4 open PG gaps (all external — below 5 threshold)
[x] Pillar 5: airSpring gS L4, neuralSpring L5, wetSpring L5 (exceeded L4 target)
[x] Pillar 5: 10/10 foundation threads active (exceeded 2+ new target)
```

When all items are checked, the interstadial is complete and the stadial
can begin.

---

## Shadow Run Readiness Tracker (May 12, 2026)

Shadow runs are the interstadial-to-stadial bridge: sovereign infrastructure
running in parallel with the existing external services, producing comparison
data that proves parity before cutover.

| Shadow Run | Upstream Ready? | Absorption Owner | Status |
|-----------|:--------------:|-----------------|--------|
| **BearDog TLS on :8443** | YES (Wave 102) | projectNUCLEUS | **SHADOW LIVE** (H2-12) — accruing comparison data vs Cloudflare |
| **Songbird NAT + VPS relay** | YES (cellMembrane VPS deployed) | projectNUCLEUS | **OPERATIONAL** — cellMembrane VPS live (Songbird relay + RustDesk), multi-gate SSH, hardened |
| **BTSP dual-auth** | YES (BearDog authenticator) | projectNUCLEUS | **CODE BUILT** — `jupyterhub_btsp_auth.py` + `deploy_btsp_auth_shadow.sh` shipped. Shadow period pending |
| **NestGate content serving** | YES (Session 60) | projectNUCLEUS | **UNBLOCKED** — `publish_sporeprint.sh` ready to wire |
| **lithoSpore Tier 2** | **EXCEEDED** (6/7 modules Tier 2 LIVE) | lithoSpore | **ACTIVE** — ecoBin compliant, `litho-core` extracted, 14 debt items resolved |
| **DoT baseline** | **FIXED** (10/10 success) | projectNUCLEUS | **RESOLVED** — tunnel baseline clarified (not a bug) |
| **ABG WCM composition** | PARTIAL (Thread 1 operational) | projectNUCLEUS | **PARTIAL** — needs provenance trio in deploy graph |

**Blocking dependency chain**: Songbird VPS relay → NestGate extracellular →
full content sovereignty. BearDog TLS shadow already live.

**Highest leverage action**: Songbird NAT relay + BTSP dual-auth are the two
remaining shadow runs to start. lithoSpore already exceeds Tier 1 gate.

---

## Evolution Pass Schedule

Four passes to reach interstadial exit. Ordered by the sentinel model:
downstream surfaces gaps, upstream owns fixes, primalSpring validates closure.
Upstream issues are escalated because primals (sentinels) are most sensitive
to the glacial shift — they must be stable before the stadial cold advance.

### Pass 11: Parallel Shadow Starts (no blockers — start immediately)

These shadow runs have zero dependencies on each other and all upstream work
is shipped. **Highest-leverage pass** — shadow runs are the literal exit gate.

| Action | Owner | Level | Upstream Ready? |
|--------|-------|-------|:-:|
| BearDog TLS shadow on :8443 — deploy script, measure vs Cloudflare | projectNUCLEUS | L4 absorption | YES |
| lithoSpore Tier 1 — groundSpring B2+B1 into modules, fetch Dryad/NCBI | lithoSpore | L4 integration | YES |
| NestGate content pipeline — wire `publish_sporeprint.sh` | projectNUCLEUS | L4 absorption | YES (S60) |

**Validates**: Pillars 1 (TLS shadow), 2 (H2-2b), 4 (2+ modules PASS)

### Pass 12: Upstream Sentinel (escalated — primals most climate-sensitive)

Upstream issues block downstream chains. These are sentinel priorities —
primals that must evolve before the stadial cold advance.

| Action | Owner | Level | Why Escalated |
|--------|-------|-------|---------------|
| ~~**toadStool Phase C**~~ — **COMPLETE** (S245-S250, 7 batches, 520 cylinder tests). Phase D plumbing in. `toadstool.validate` **IMPLEMENTED**. | toadStool | L1 | **RESOLVED** — Tier 2 Science API unblocked. E2E sovereign dispatch (factory + VFIO PBDMA) is stadial. |
| ~~**Songbird VPS relay**~~ — **OPERATIONAL** (cellMembrane VPS: Songbird relay + RustDesk, multi-gate SSH) | Songbird | L1 | **RESOLVED** — NAT shadow unblocked |
| ~~**coralReef timeout/FECS/GPCCS**~~ — **STABILITY PROOF SHIPPED** (Sprint 7): `boot_gr_falcons_with_recovery` (3× retry + PMC GR reset), structured `GrBootOutcome`, all boot paths recovery-aware. 4790 tests, zero debt. | coralReef | L1 | **RESOLVED** — sovereign dispatch proof unblocked for hotSpring. |

### Pass 13: Gate Composition (L3/L4 — wiring shipped capabilities)

| Action | Owner | Level | Dependency |
|--------|-------|-------|------------|
| BTSP dual-auth shadow (JupyterHub PAM plugin) | projectNUCLEUS | L4 | BearDog authenticator ready |
| ABG WCM via deploy graphs + provenance trio | projectNUCLEUS + ABG | L4 | Thread 1 operational |
| Foundation Threads 3, 4, 8 expressions | healthSpring (3,8), wetSpring+airSpring (4) | L3 | Seeding infra ready |
| Foundation Threads 9, 10 full seeding | ludoSpring (9), ludoSpring+primalSpring (10) | L3 | Expression+data+targets |
| healthSpring BTSP FAMILY_SEED interop | healthSpring + primalSpring | L3 | Root cause documented |

**Validates**: Pillars 2 (H2 shadow state), 3 (WCM through provenance)

### Pass 14: Convergence (stadial-ready)

| Action | Owner | Level | Dependency |
|--------|-------|-------|------------|
| ~~Tier 2 Science API (`toadstool.validate`)~~ — **IMPLEMENTED** (S250). `list_workloads` WIRED (S245+). | toadStool + primalSpring | L1/L2 | **RESOLVED** |
| ~~`barracuda.precision.route` wired~~ — **IMPLEMENTED** (precision.rs + 242 tests + 407 trio E2E tests) | barraCuda + primalSpring | L1/L2 | **RESOLVED** |
| Ionic runtime live (cross-spring RPC) | primalSpring + healthSpring | L2 | CompositionContext wiring |
| skunkBat E2E operational audit validation | skunkBat + primalSpring | L2 | JH-5 Phase 3 shipped |
| `capability.resolve` name-based discovery | Songbird | L1 | Unblocks discovery debt |
| CompositionContext L2 coordination pass | primalSpring | L2 | All shadows running |

**Exit condition**: All checklist items above checked. Shadow runs producing
comparison data. Stadial can begin.

---

## Stadial: External Validation Drives Evolution

The stadial is not a maintenance phase — it is an **advance** driven by
external selective pressure. Each external driver validates a different
facet of the ecosystem:

| External Driver | What It Validates | Ecosystem Target |
|----------------|-------------------|-----------------|
| **Cloudflare baselines** | BearDog TLS + Songbird NAT parity | H2-3b/3c: shadow → cutover when parity proven |
| **GitHub → Forgejo** | CI, plasmidBin, repo sovereignty | H3-02/03/04: migrate when Forgejo is primary |
| **Barrick Lab USB** | lithoSpore artifact end-to-end | Phase 5: first artifact leaving possession |
| **Upstream crates** (wgsl-precision, proc-sysinfo) | Community acceptance | Q2 2026: MIT/Apache-2.0 extraction |
| **Dimforge/wgmath** | Peer validation of WGSL corpus | Proof-of-work engagement |
| **Framework parity** (Kokkos, LAMMPS, SciPy) | Computational correctness | Per-spring benchmarks (Tier 2+) |
| **ABG users** | Real science on sovereign infra | Foundation Thread 1 in production |
| **Let's Encrypt / ACME** | TLS certificate sovereignty | BearDog ACME client |

### Stadial Exit Criteria (preliminary)

The stadial ends when:
- BearDog TLS has cut over from Cloudflare (parity proven via shadow)
- Songbird NAT has replaced cloudflared (relay proven via VPS)
- At least 1 upstream crate is published on crates.io
- lithoSpore has been validated on at least 1 external machine
- ABG users are running science on sovereign infrastructure
- All H2 sub-steps are cutover (not just shadow)

H3 (primal-only: JupyterHub → petalTongue, GitHub → Forgejo, plasmidBin →
NestGate) may span multiple stadial cycles.

---

## Cross-References

- `ECOSYSTEM_EVOLUTION_CYCLE.md` — water cycle model, season definitions
- `primalSpring/docs/PRIMAL_GAPS.md` — L1–L5 gap ownership model, Wave 8/9/10 tracking
- `primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` — per-spring metrics, Phase 32 gap sweep
- `primalSpring/docs/TEMPORAL_ECOSYSTEM_REVIEW_MAY12_2026.md` — full ecosystem temporal review
- `primalSpring/docs/LIVE_SCIENCE_API.md` — Tier 2 wire contract for downstream
- `primalSpring/docs/DOWNSTREAM_PATTERN_GUIDE.md` — spring-to-product pattern handoff
- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — H1/H2/H3 horizon tracker
- `lithoSpore/docs/UPSTREAM_GAPS.md` — per-module spring dependency analysis
- `TARGETED_GUIDESTONE_STANDARD.md` — Targeted GuideStone budding pattern
- `EXTERNAL_VALIDATION_AND_UPSTREAM_STRATEGY.md` — external validation tiers
- `UPSTREAM_CONTRIBUTIONS.md` — upstream crate extraction plan
- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — external surface design: Signal, Relay, and Surface channels
