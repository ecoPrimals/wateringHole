<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Interstadial Exit Criteria — Full Sovereignty Pre-Wire

**Version**: 1.0 — May 11, 2026
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
- 413-method registry: zero drift
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
| 2a | BTSP auth live (dual-auth period) | PAM only | Build plugin, start shadow period |
| 2b | BearDog TLS on :8443 | Not running | Start shadow, measure parity vs Cloudflare |
| 2c | Songbird NAT operational | cloudflared only | VPS relay, test NAT chain |
| 2d | NestGate extracellular | GitHub Pages | Content pipeline serving `primals.eco` |
| 2e | Foundation workloads | Thread 1 WCM validated | Add Threads 4, 7 (LTEE-relevant) |
| 2f | lithoSpore workload dispatched | Workload TOMLs exist | Integration after lithoSpore Phase 2 |

**Exit gate**: H2 sub-steps 2b/3a/3b/3c all in shadow-run state. Cutover
is stadial work — interstadial only requires the shadow infrastructure to be
running and producing comparison data.

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
| 4b | At least 2 modules functional | groundSpring B2+B1 **COMPLETE** (Python+Rust) | Integrate into lithoSpore ltee-fitness + ltee-mutation |
| 4c | Data fetched and hashed | Templates in data.toml | Fetch Wiser 2013, Barrick 2009 from Dryad/NCBI |
| 4d | Python Tier 1 baselines running | groundSpring `control/ltee_*` + `validate` bins | Wire into lithoSpore module structure with real data |

LTEE reproduction status (May 11):
- **groundSpring**: B2 (Wiser 2013) Python 9/9 + Rust 10/10 PASS; B1 (Barrick 2009) Python 8/8 + Rust 8/8 PASS
- **hotSpring**: B2 (Anderson fitness) STARTED — Exp 189, notebook shipped
- **wetSpring**: B7 (Tenaillon 2016) STARTED — 264 NCBI genomes, mutation accumulation
- **neuralSpring**: B1 (Barrick 2009) STARTED — Python baseline 8/8 PASS

**Exit gate**: At least 2 modules producing PASS at Tier 1 (Python) with real
data fetched and BLAKE3-hashed. **groundSpring B2+B1 reproductions are complete** —
remaining work is integration into lithoSpore module structure and data fetching.

### Pillar 5: River Delta (Springs) — **GATE MET** (May 11, 2026)

| # | Target | Current State | Status |
|---|--------|---------------|--------|
| 5a | Tier 4: 4+ springs `optional=true` | **8/8** — all springs IPC-first (`default = []`) | **DONE** |
| 5b | wetSpring PG gaps below 5 | **4 open** (PG-02, PG-03, PG-04, PG-05 — all external) | **DONE** |
| 5c | guidestone convergence | airSpring **L4**, neuralSpring **L5** | **EXCEEDED** |
| 5d | Foundation seeding | **7/10** threads with spring seeds (2, 3, 5, 6, 7, 9, 10) | **DONE** |
| 5e | plasmidBin: all springs staged | 6/8 staged (ludoSpring composed, primalSpring special) | On track |
| 5f | LTEE paper queue progress | **4 springs reproducing** (groundSpring B2+B1 DONE, hotSpring B2, wetSpring B7, neuralSpring B1) | **DONE** |
| 5g | CompositionContext wiring | PrimalClient encapsulated (L2 design) | L2 coordination pass pending |

**Exit gate**: **ALL conditions met.** 8/8 Tier 4, wetSpring at 4 PG (below 5),
airSpring L4, neuralSpring L5 (exceeded L4 target), 7/10 foundation threads seeded,
LTEE reproductions active across 4 springs.

---

## Interstadial Exit Gate — Summary Checklist

```
[x] Pillar 1: NestGate `content.*` transport parity (Session 60, May 11) — all 8 methods on all 4 surfaces
[ ] Pillar 1: BearDog TLS shadow running on :8443
[ ] Pillar 1: Songbird NAT + VPS relay operational
[x] Pillar 1: petalTongue web mode + NestGate backend — UNBLOCKED (SPA+CORS shipped, NestGate transport parity shipped)
[ ] Pillar 1: BTSP auth dual-auth shadow running
[x] Pillar 1: JH-5 audit forwarding wired — skunkBat Phase 3 shipped (rhizoCrypt + sweetGrass forwarding)
[x] Pillar 1: MethodGate 13/13 (squirrel shipped May 11)
[ ] Pillar 2: H2-2b/3a/3b/3c all in shadow-run state
[ ] Pillar 2: Foundation Threads 4+7 workloads running
[ ] Pillar 3: Thread 1 WCM compositions through provenance trio
[ ] Pillar 4: 2+ lithoSpore modules PASS at Tier 1
[ ] Pillar 4: Real data fetched from Dryad/NCBI
[x] Pillar 5: 8/8 springs at barraCuda optional=true (exceeded 4+ target)
[x] Pillar 5: wetSpring 4 open PG gaps (all external — below 5 threshold)
[x] Pillar 5: airSpring gS L4, neuralSpring gS L5 (exceeded L4 target)
[x] Pillar 5: 7/10 foundation threads seeded (exceeded 2+ new target)
```

When all items are checked, the interstadial is complete and the stadial
can begin.

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
- `primalSpring/docs/PRIMAL_GAPS.md` — L1–L5 gap ownership model
- `primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` — per-spring metrics
- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — H1/H2/H3 horizon tracker
- `lithoSpore/docs/UPSTREAM_GAPS.md` — per-module spring dependency analysis
- `TARGETED_GUIDESTONE_STANDARD.md` — Targeted GuideStone budding pattern
- `EXTERNAL_VALIDATION_AND_UPSTREAM_STRATEGY.md` — external validation tiers
- `UPSTREAM_CONTRIBUTIONS.md` — upstream crate extraction plan
