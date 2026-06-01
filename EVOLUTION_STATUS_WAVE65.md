# Evolution Status — Wave 65 Checkpoint

**Date**: 2026-05-31  
**Phase**: Interstadial exit → Stadial entry  
**Authority**: eastGate overwatch

---

## Where We Are

The ecosystem has reached a stable plateau at Wave 65. All critical
infrastructure bash scripts have been evolved to idiomatic Rust.
Five gates are operational. Three sovereignty shadows are live. The
K-Derm diderm envelope is deployed and validated. impulsePotential
coordination and context braids are operational. 838 tests pass.

---

## System Topology

### K-Derm Diderm Envelope (VPS)

```
GitHub ←──weak──── golgiBody-ext (137.184.197.151)
                        │ ionic
                   peptidoglycan (157.230.209.218)
                        │ metallic
                   golgiBody-inner (157.230.3.183)
                   ┌────┤ covalent
              eastGate   ironGate   southGate   biomeGate   flockGate
              (LAN)      (LAN)      (LAN)       (LAN)       (WAN)
```

### Gate Status

| Gate | Status | Role | Temporal Sync |
|------|--------|------|---------------|
| eastGate | OPERATIONAL | Orchestrator, overwatch | Full superset (39 repos) |
| ironGate | OPERATIONAL | ABG compute, dev | Core + health/ludo |
| southGate | OPERATIONAL | Gaming + compute | Core + wet/neural |
| biomeGate | OPERATIONAL | HBM2 test bench, air-gap validation | Core + hotSpring (19/19 sync) |
| flockGate | OPERATIONAL | WAN covalent, sporePrint | Full superset (~1.3s Forgejo) |
| strandGate | Hardware ready | Bioinformatics | Not deployed |
| northGate | Hardware ready | Heavy compute | Not deployed |
| westGate | Hardware ready | Cold storage (76TB ZFS) | Not deployed |

### Sovereignty Shadows

| Track | Status | Remaining |
|-------|--------|-----------|
| S1 TLS | 7-day gate running (~June 7) | Wait for gate completion |
| S2 NAT | LIVE (100%) | Complete |
| S3 Content | LIVE (67ms TTFB) | Complete |
| S4 Auth | Shadow on ironGate | ironGate services restart for formal gate |
| DNS | ns1+ns2 LIVE, DNSSEC | Registrar NS cutover |

---

## What's Evolved (Wave 61-65)

### Bash → Rust Critical Path

| Script | Lines | Rust Module | Lines | Status |
|--------|-------|-------------|-------|--------|
| `cascade-pull.sh` | ~300 | `temporal.rs` | 638 | Fully Rust (`temporal.cascade`) |
| `fetch_primals.sh` | 513 | `plasmid.rs` | 423 | Fully Rust (`plasmid.fetch`) |
| `membrane.sh` (original) | ~600 | `dispatch.rs` + 11 modules | 3,500+ | Fully Rust |

### Module Architecture (membrane-shadow)

| Module | Lines | Domain |
|--------|-------|--------|
| `dispatch.rs` | 709 | Command routing |
| `temporal.rs` | 638 | WaterFall sync engine |
| `impulse.rs` | 712 | Impulse/potential coordination |
| `context.rs` | 464 | Context braid weaving |
| `plasmid.rs` | 423 | Binary artifact fetching |
| `cli.rs` | 176 | Argument parsing |
| `main.rs` | 129 | Thin entry point |
| `git_ops.rs` | 94 | Shared git operations |
| `signal.rs` | 20 | Deprecated shim → remove Wave 66 |
| Others | ~600 | forgejo, gate, config, manifest, identity |

### Validation

| Metric | Wave 62 | Wave 65 |
|--------|---------|---------|
| primalSpring tests | 789 | 838 |
| Scenarios | 53 | 57 |
| Experiments | 92 | 96 |
| Deploy graphs | 95 | 110 |
| Method registry | 458 | 490+ |
| Clippy warnings | Multiple | Zero (actionable) |

---

## Remaining Evolution Work

### HIGH Priority — Blocks Glacial Shift

| Item | Owner | Blocked By |
|------|-------|-----------|
| S1 TLS 7-day gate completion | cellMembrane | Time (~June 7) |
| S4 formal 7-day gate | ironGate | Services restart |
| DNS NS registrar cutover | Manual action | User's registrar login |
| Cross-gate `discovery.peers` smoke test | primalSpring | Same-subnet gate test |
| Cross-gate `capability.call` smoke test | primalSpring | `discovery.peers` first |
| `signal.rs` removal | cellMembrane | Wave 66 (one-wave deprecation window) |

### MEDIUM Priority — Strengthens Sovereignty

| Item | Owner | Notes |
|------|-------|-------|
| Transport quorum Phase 1 | cellMembrane | Timer-based `potential.sense` on VPS nodes |
| Forgejo Actions CI | projectNUCLEUS | Self-hosted runner, reduces GitHub dependency |
| Cross-subnet routing | infra/network | southGate on different subnet needs routing/TURN |
| Multi-vendor peptidoglycan | cellMembrane | Additional VPS provider for redundancy |
| strandGate/northGate deployment | ops | Hardware ready, NUCLEUS not deployed |
| pseudoSpore delta coverage | springs | 2/7 springs have spores |
| Songbird coverage 73→90% | Songbird | Not blocking but incremental |

### LOW Priority — Enhancements

| Item | Owner | Notes |
|------|-------|-------|
| Caddy → BearDog ACME replacement | cellMembrane | Caddy works fine |
| BearDog Vault (encrypted creds at rest) | bearDog | Phase 2 design |
| Central fossilRecord sync | all primals | 7/8 reference paths that don't exist |
| neuralSpring composition fix | neuralSpring | Stale `target/release/` hardcode |
| loamSpine Tokio runtime-in-runtime | loamSpine | Upstream bug |

---

## Concept Evolution (gen4 → gen5)

The following gen5 foundation documents have been written to bridge
the conceptual evolution from gen4:

| gen4 Document | gen5 Document | What Changed |
|---------------|---------------|-------------|
| `K_DERM_RECONCILIATION.md` | `KDERM_DIDERM_ENVELOPE.md` | Naming reconciliation → physical deployment |
| `SOVEREIGNTY_EVOLUTION_NARRATIVE.md` | `SOVEREIGNTY_SHADOW_EVOLUTION.md` | Narrative → operational S1-S4 tracks |
| (no precedent) | `TRANSPORT_EVOLUTION.md` | Nanowire → quorum sensing progression |
| (no precedent) | `IMPULSE_POTENTIAL_COORDINATION.md` | Neural API triad + provenance trio integration |
| (existed) | `CONTEXT_BRAID_PATTERN.md` | sweetGrass external analog |
| (existed) | `EXTERNAL_SOVEREIGNTY_PATTERN.md` | Collaborator gate routing |

---

## Handoff Status

| Archive | Contents |
|---------|----------|
| `handoffs/archive/wave63/` | 10 Wave 63 documents |
| `handoffs/archive/wave64/` | 8 Wave 64 documents |
| Active handoffs | None — all fossilized |

---

## Next Wave Priorities

### Wave 66 — Mesh Validation Sprint
1. Same-subnet `discovery.peers` test (eastGate ↔ ironGate)
2. Cross-gate `capability.call` via `s_covalent_mesh` scenario
3. Remove deprecated `signal.rs` shim
4. S1 TLS gate assessment (should complete by June 7)

### Wave 67 — Quorum Phase 1
1. Timer-based `potential.sense` on peptidoglycan
2. Timer-based `potential.sense` on golgiBody-ext
3. Begin transport evolution from nanowire to quorum sensing

### Wave 68+ — Expansion
1. strandGate NUCLEUS deployment (bioinformatics workloads)
2. northGate NUCLEUS deployment (heavy compute)
3. Multi-vendor peptidoglycan node
4. Forgejo Actions CI on ironGate

---

*The ecosystem is past the construction phase and into the validation
phase. The infrastructure is built; the remaining work is proving it
under real distributed load across the gate mesh.*
