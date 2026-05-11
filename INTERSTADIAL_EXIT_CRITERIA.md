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

None. **13/13 primals pass the primalSpring gate** (May 11, 2026):
- MethodGate (JH-0 + JH-2): **13/13** — squirrel shipped `method_gate.rs`
- BTSP Phase 3 AEAD: **13/13**
- 413-method registry: zero drift
- Edition 2024, deny.toml (ring + openssl), plasmidBin: **13/13**

**Downstream absorption (L3/L4 integration — shipped capabilities awaiting wiring):**

| # | Capability | Primal | Shipped | Absorption Owner |
|---|-----------|--------|---------|-----------------|
| 1a | TLS termination + rate limits | BearDog | Yes (Wave 100) | L4 (NUCLEUS): H2-3b shadow on :8443 |
| 1b | NAT chain (STUN/TURN) | Songbird | Yes (Waves 196-197) | L4 (NUCLEUS): H2-3c VPS relay |
| 1c | Content pipeline (`content.put`) | NestGate | Partial | L4 (NUCLEUS): H2-3a publish pipeline |
| 1d | Web mode (`--docroot`) | petalTongue | Partial | L4 (NUCLEUS): H2-3a NestGate-backed static |
| 1e | BTSP authenticator | BearDog | Ready | L4 (NUCLEUS): H2-2b JupyterHub plugin |
| 1f | `composition.deploy(graph)` | biomeOS | API exists | L4 (NUCLEUS): gate wiring, membrane signals |
| 1g | Audit forwarding (JH-5) | skunkBat | Phase 2 | L3/L4: wire deploy graphs |
| 1h | Cross-primal tokens (JH-11) | BearDog | Done | L3 (Springs): CompositionContext wiring |
| 1j | Sovereign DNS | Songbird/BearDog | DoT intermediate | L4 (NUCLEUS): H2-4 knot-dns (can defer to stadial) |

**Exit gate**: MethodGate **13/13 DONE**. Remaining: downstream absorption items
1a–1h in active shadow-run or wiring state.
1j (full sovereign DNS) may defer to stadial — DoT is sufficient for exit.

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
| 4a | Spring LTEE paper queue started | 36 items queued in 6 springs | Springs begin B1/B2/B3 reproductions |
| 4b | At least 2 modules functional | All 7 modules SKIP | groundSpring B2 → ltee-fitness (critical path) |
| 4c | Data fetched and hashed | Templates in data.toml | Fetch Wiser 2013, Barrick 2009 from Dryad/NCBI |
| 4d | Python Tier 1 baselines running | Scaffold only | Implement modules 1+2 with real data |

**Exit gate**: At least 2 modules producing PASS at Tier 1 (Python) with real
data fetched and BLAKE3-hashed. groundSpring is the critical path — it
contributes statistical methods to all 7 modules.

### Pillar 5: River Delta (Springs)

| # | Target | Current State | Interstadial Remaining |
|---|--------|---------------|----------------------|
| 5a | Tier 4: 4+ springs `optional=true` | 3 (ludoSpring, wetSpring, neuralSpring) | airSpring, groundSpring, healthSpring, or hotSpring |
| 5b | wetSpring PG gaps | 8 open (PG-02,03,04,05,06,10,17,18) | Close at least 4 of 8 |
| 5c | guidestone convergence | airSpring L2+, neuralSpring L3 | Both → gS L4 |
| 5d | Foundation seeding | 5/10 threads active | Threads 3, 5, 8, 10 need sources/targets |
| 5e | plasmidBin: all springs staged | 6/8 staged | ludoSpring (composed), primalSpring (special) |
| 5f | LTEE paper queue progress | 36 items queued | Begin reproductions (feeds Pillar 4) |
| 5g | CompositionContext wiring | PrimalClient encapsulated (L2 design) | L2 coordination pass |

**Exit gate**: 4+ springs at `optional=true`, wetSpring below 5 open PG gaps,
airSpring and neuralSpring at gS L4, at least 2 foundation threads newly
seeded with sources/targets.

---

## Interstadial Exit Gate — Summary Checklist

```
[ ] Pillar 1: BearDog TLS shadow running on :8443
[ ] Pillar 1: Songbird NAT + VPS relay operational
[ ] Pillar 1: NestGate content pipeline serving content
[ ] Pillar 1: petalTongue web mode operational
[ ] Pillar 1: BTSP auth dual-auth shadow running
[ ] Pillar 1: JH-5 audit forwarding wired in deploy graphs
[x] Pillar 1: MethodGate 13/13 (squirrel shipped May 11)
[ ] Pillar 2: H2-2b/3a/3b/3c all in shadow-run state
[ ] Pillar 2: Foundation Threads 4+7 workloads running
[ ] Pillar 3: Thread 1 WCM compositions through provenance trio
[ ] Pillar 4: 2+ lithoSpore modules PASS at Tier 1
[ ] Pillar 4: Real data fetched from Dryad/NCBI
[ ] Pillar 5: 4+ springs at barraCuda optional=true
[ ] Pillar 5: wetSpring < 5 open PG gaps
[ ] Pillar 5: airSpring + neuralSpring at gS L4
[ ] Pillar 5: 2+ new foundation threads seeded
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
