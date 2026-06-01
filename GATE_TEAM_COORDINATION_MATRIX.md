# Gate-Team Coordination Matrix

**Purpose**: Single-page view of which team operates which gate, what hardware
it has, what projects it owns, and where it sits in the evolution/validation
hierarchy. Consolidates data from `GATE_SPRING_OWNERSHIP.md` (canonical
spring routing), `GLACIAL_SHIFT_READINESS.md` (operational status), and
`ecosystem_manifest.toml` (sync profiles).

**Last updated**: 2026-06-01 (Wave 67)

**Authority**: wateringHole consensus

---

## Gate Inventory

| Gate | Team | Hardware | Role | NUCLEUS | Network | Status |
|------|------|----------|------|---------|---------|--------|
| **eastGate** | eastGate (overwatch) | i9-12900, RTX 4070 + Akida, 32GB | Orchestrator, coordination hub | 13/13 | LAN 1G | OPERATIONAL |
| **ironGate** | ironGate (cellMembrane, projectNUCLEUS) | i9-14900K, RTX 5070, 96GB | Agentic dev, ABG, deployment infra | 13/13 (23 UDS) | LAN 1G | OPERATIONAL |
| **southGate** | southGate | 5800X3D, RTX 4060 + 3090s, 128GB | Gaming + compute, pattern node | 9/9 | LAN 1G | OPERATIONAL |
| **biomeGate** | biomeGate (hotSpring) | Threadripper 3970X, Titan V + K80, 256GB | HPC physics, GPU shader validation | 62/62 | LAN 1G | OPERATIONAL |
| **flockGate** | flockGate (sporePrint) | i9-13900K, RTX 3070 Ti, 64GB | WAN covalent, sporePrint hosting | OPERATIONAL | WAN via cellMembrane | OPERATIONAL |
| **strandGate** | — (undeployed) | Dual EPYC 7452 (64c), 256GB ECC | Bioinformatics, ABG science | — | LAN 1G | HARDWARE READY |
| **northGate** | — (undeployed) | Ryzen 9950X3D, RTX 5090, 96GB | Heavy compute, AI/LLM | — | LAN 1G (10G ready) | HARDWARE READY |
| **westGate** | — (undeployed) | i7-4771, RTX 2070 Super, 32GB | 76TB ZFS cold storage (Nest Atomic) | — | LAN 1G (10G ready) | HARDWARE READY |
| **swiftGate** | — (undeployed) | Ryzen 5800X, RTX 3070, 64GB | Mobile/compact | — | LAN 1G | HARDWARE READY |
| **kinGate** | — (undeployed) | i7-6700K, RTX 3070, 32GB | Staging | — | LAN 1G | HARDWARE READY |

### VPS Nodes (cellMembrane — Inner Membrane)

| Node | K-Derm Layer | IP | Specs | Role | Status |
|------|-------------|-----|-------|------|--------|
| **golgiBody** | Inner (cis face) | 157.230.3.183 | 1 vCPU, 2GB, 50GB | Forgejo, NUCLEUS relay, sovereign DNS (ns1) | OPERATIONAL |
| **peptidoglycan** | Structural | 157.230.209.218 | 2 vCPU, 4GB, 80GB | Temporal sync hub, relay mediator | OPERATIONAL |
| **golgiBody-ext** | Outer (trans face) | 137.184.197.151 | — | Caddy TLS, sporePrint serving, DNS (ns2), GitHub push | OPERATIONAL |

---

## Project Ownership

| Project | Owner Team (Gate) | Description |
|---------|-------------------|-------------|
| **primalSpring** | eastGate | Coordination, composition validation, ecosystem bonding |
| **cellMembrane** | ironGate | VPS provisioning, relay infrastructure, deployment tooling |
| **projectNUCLEUS** | ironGate | Deploy graphs, dark forest, genomeBin, Forgejo CI |
| **sporePrint** | flockGate | Ecosystem website, content pipeline, petalTongue integration |
| **hotSpring** | biomeGate | GPU physics, toadStool diesel engine |
| **ludoSpring** | ironGate | Game science, ludic composition |
| **healthSpring** | ironGate | Clinical/compliance science |
| **wetSpring** | southGate | Biology, analytical chemistry |
| **neuralSpring** | southGate | ML inference patterns |
| **airSpring** | eastGate | Ecology science |
| **groundSpring** | eastGate | Geoscience |
| **esotericWebb** | ironGate | Interactive product garden |

---

## Spring → Gate Routing

| Gate | Springs | Gardens | Sync Profile |
|------|---------|---------|--------------|
| eastGate | primalSpring, airSpring, groundSpring | — | Full superset (39 repos) |
| ironGate | healthSpring, ludoSpring | esotericWebb | Core + health/ludo + infra |
| southGate | wetSpring, neuralSpring | — | Core + wet/neural |
| biomeGate | hotSpring | — | Core + hotSpring |
| flockGate | sporePrint | — | Core + sporePrint/petalTongue |
| strandGate (planned) | hotSpring (science) | helixVision, initioChem, blueFish, lithoSpore | Core + hot + ABG gardens |

---

## Evolution Hierarchy

### Validation Tiers

```
Tier 1 — Coordination (eastGate)
  primalSpring validates all compositions work together.
  835 tests, 57 scenarios, 33 compositions, 490+ methods.
  Owns the bonding mechanics, not the atoms.

Tier 2 — Deployment (ironGate)
  projectNUCLEUS validates deploy graphs, genomeBin, CI.
  cellMembrane validates VPS infrastructure, relay chain.

Tier 3 — Domain Science (per-gate)
  Each gate validates its own springs independently.
  primalSpring's scenarios verify cross-gate composition parity.
```

### Current Wave Assignments (Wave 67+)

| Gate | Active Work | Priority |
|------|-------------|----------|
| **eastGate** | Vocabulary evolution complete. Doc cleanup done. Next: `discovery.peers` + `capability.call` live mesh tests | P0 glacial |
| **ironGate** | S4 auth formal 7-day gate. Songbird security socket fix. Forgejo Actions CI shadow | P0 glacial |
| **southGate** | Federation verify post-redeploy. wetSpring provenance trio integration | P1 |
| **biomeGate** | hotSpring Exp 234 Run #6 (catalyst NOP teardown/rebind). toadStool kernel patch validation | P2 |
| **flockGate** | sporePrint Wave 68 deep debt + live viz complete. petalTongue VizRegistry operational | Clear |
| **golgiBody** | Disk pressure 68%. Relay bash→Rust evolution (4 scripts). Family seed deployment | P1 |

---

## Sovereignty Shadow Status

| Track | Commercial | Sovereign | Gate | Status |
|-------|-----------|-----------|------|--------|
| S1 TLS | Cloudflare (INACTIVE) | Caddy + LE on golgiBody-ext | cellMembrane | **13d PASSED** — ready to graduate |
| S2 NAT | cloudflared (INACTIVE) | Songbird TURN :3478 | cellMembrane | **DONE** |
| S3 Content | GitHub Pages | NestGate + Caddy (67ms TTFB) | cellMembrane + sporePrint | **LIVE** — cutover after DNS |
| S4 Auth | OAuth2/PAM | BearDog BTSP dual-auth | ironGate | **Shadow live** — formal 7-day gate pending |
| S5 DNS | Cloudflare NS | knot-dns ns1+ns2 (DNSSEC) | cellMembrane | **Infra LIVE** — registrar cutover pending |

---

## Cross-References

- `GATE_SPRING_OWNERSHIP.md` — canonical spring routing, evolution biology
- `GLACIAL_SHIFT_READINESS.md` — operational status, glacial criteria
- `GLACIAL_SHIFT_WAVE_PLAN.md` — phased wave assignments
- `EVOLUTION_STATUS_WAVE66.md` — Wave 66 checkpoint + context braids
- `ecosystem_manifest.toml` — machine-readable gate sync profiles

---

*Wave 67. Colonial phase. Gates coordinate through periplasm, mesh next.*
