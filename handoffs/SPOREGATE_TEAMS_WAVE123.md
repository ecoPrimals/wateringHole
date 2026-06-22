# sporeGate Teams — Wave 123 Dispatch

**Date**: Jun 22, 2026 | **From**: eastGate overwatch
**Gate**: sporeGate (.2, LAN Hub 1) | **Composition**: 13/13 NUCLEUS
**Role**: Build authority + Nest provenance + LAN topology overwatch

---

## Subteam: sporeGate Overwatch (Topology + Hardware + Deploy)

### P1: Nest Provenance Depth

- Ledger commit height → 4+ (periodic provenance commits via loamSpine)
- Stage NestGate content for cross-gate federation test (Wave 124)
- BLAKE3 verify all depot artifacts post dual-target build

### P1: Relay Push (strandGate/southGate)

- Use RustDesk relay to push sovereign config to strandGate, southGate
- Pattern: connect via public relay → push sovereign relay config → reconnect via sovereign
- Lower priority than trust/quorum work, but opportunistic when gates are online

### P2: Hardware Enrollment (when operator provides)

- Flint 2 #2 (incoming) — enroll as bridge AP or mesh node
- strandGate/southGate — enroll when relay push succeeds
- Pattern: SSH key → WG config → NUCLEUS deploy → Forgejo remote → done

---

## Subteam: cellMembrane (Code Evolution + CI)

### P1: Quorum Phase 1 — Autonomous Cascade

This is the highest-impact evolution for reducing manual coordination:

```
Current (Nanowire):   gate pushes → nothing happens until someone pulls
Target (Quorum P1):   gate pushes → golgi senses within 60s → auto-relays
```

**Implementation**:
1. Deploy systemd timer on golgi: `membrane temporal.cascade --check` every 60s
2. If new commits on any repo, auto-pull to golgi and update depot
3. Validate: push from eastGate, wait 60s, confirm golgi has it without SSH trigger
4. Document operational pattern in `wateringHole/TRANSPORT_EVOLUTION_OPS.md`

### P2: Tier 3 Isomorphism

- `gate.migrate` — move a gate's identity to new hardware
- `gate.bootstrap --absorb` — new gate absorbs role from decommissioned gate
- Credential portability across gates

### P2: Auth Evolution Path

- BearDog BTSP → composition auth (coordinate with flockGate Tower team)
- cellMembrane's role: wire BTSP verification into membrane-shadow dispatch
- `membrane gate.check` should validate BTSP tokens, not just SSH connectivity

### P2: golgi-as-NUCLEUS

- Evolve golgi VPS from "18 ad-hoc services" to "NUCLEUS-managed primal composition"
- Long-term: golgi runs primals via the same systemd pattern as gates
- This makes golgi agentically manageable (deploy, update, restart via membrane CLI)

---

## Build Authority Responsibilities (ongoing)

- Sovereign CI continues: Forgejo push → golgi hook → sporeGate build → rsync depot
- Dual-target: musl (all 14) + gnu (barracuda, coralReef) for ironGate
- Build time target: <14 min full, <5 min incremental
- BLAKE3 checksums on all artifacts

---

## Context

- sporeGate is **peptidoglycan** in K-Derm topology — structural, builds, mediates
- Nest atomic (NestGate + RhizoCrypt + LoamSpine + SweetGrass) = storage + provenance
- Quorum Phase 1 is from `gen5/foundations/TRANSPORT_EVOLUTION.md`
- membrane-shadow is a 12-module Rust crate (744 tests) — all control plane ops in Rust
- The cascade becomes autonomous when golgi senses changes without being told

## Coordination

- flockGate Tower team is deploying BTSP — coordinate key exchange
- ironGate Node team needs gnu binaries — ensure depot is fresh
- eastGate overwatch validates via primalSpring scenarios

---

*You are the structural layer. Build, mediate, sense.*
