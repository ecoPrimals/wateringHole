# ecoPrimals Ecosystem Blurb — Wave 146a

**Date**: Jul 17, 2026 07:30 EDT | **Wave**: 146a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. PHASE 2 14/14 COMPLETE. CAC 6/6 COMPLETE.**

**This wave**: northGate deployment plan formalized — final validation target.
benchScale + agentReagents validate before deployment. squirrel credential
boundary absorbed (`c1203f9f`). Manifest fix: northGate target corrected
`x86_64-unknown-linux-musl` → `x86_64-pc-windows-gnu`.

---

## Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 1 (cross-compile 14/14) | **COMPLETE** |
| Silicon Atheism Phase 2 (transport abstraction 14/14) | **COMPLETE** |
| Content-Addressed Convergence (6/6 layers) | **COMPLETE** |
| Glacial Shift Criteria (8/8) | **ALL CLEAR** |
| Depot (59 binaries, 4 architectures) | **OPERATIONAL** |
| sporePrint root 404 | **RESOLVED** |

---

## northGate Deployment — Final Validation Target

northGate (Ryzen 9950X3D, RTX 5090, 96GB, Windows) is the final
ecosystem deployment target. It validates the full pipeline on Windows:
depot fetch → binary deploy → mesh enrollment → IPC validation.

### Validation Before Deployment

| Tool | What It Validates | Status |
|------|-------------------|--------|
| **benchScale** | IPC compliance (liveness, readiness, capabilities) | Available — needs Windows scenario |
| **agentReagents** | Agent configuration, deployment reagents | Available |
| **primalSpring** | E2E scenarios (169 scenarios, 1,202 tests) | Available — `full-cross-compile` scenario |
| **bingoCube** | Validation framework | Available |

### northGate Deployment Steps

1. `membrane plasmid.fetch` — pull 14 Windows ecobins from VPS depot
2. benchScale: `validate ipc` against fetched binaries (pre-deploy smoke)
3. Deploy NUCLEUS (songbird.exe → mesh enrollment → biomeOS orchestration)
4. benchScale: `validate ipc` against live NUCLEUS (post-deploy compliance)
5. primalSpring: run `full-cross-compile` + `benchscale-ipc-x86-uds` scenarios
6. Validate cross-gate `capability.call` (northGate ↔ eastGate via mesh)

### Manifest Fix

northGate target was `x86_64-unknown-linux-musl` (copy-paste from Linux gates).
Corrected to `x86_64-pc-windows-gnu` to match actual hardware.

---

## Project Assignment Inventory

### Assigned (active teams)

| Project | Type | Team/Owner |
|---------|------|------------|
| 14 primals | primal | Individual primal teams |
| cellMembrane | garden | cellMembrane team (sporeGate) |
| projectNUCLEUS | garden | NUCLEUS team |
| sporePrint | infra | sporePrint team (golgi) |
| primalSpring | spring | primalSpring team (eastGate) |
| footPrint | protist | Composition target (flockGate) |
| wateringHole | infra | eastGate overwatch |

### Gardens — Priority Order (P2, team pickup when ready)

| Priority | Project | What It Enables |
|----------|---------|-----------------|
| **1** | **lithoSpore** / pseudoSpore | Portability — makes any work USB-deployable and recreatable. All primals/gardens can become spores. initioChem made the first. |
| **2** | **projectFOUNDATION** | Data layer — knowledge, thread lineage, validation evidence |
| **3** | **esotericWebb** | Living game state — leverages petalTongue UI + primals for interactive experience |
| 4 | initioChem | Computational chemistry (hotSpring consumer, first pseudoSpore) |
| 5 | helixVision | Sovereign genomics discovery (16S/WGS → taxonomy) |
| 6 | blueFish | Analytical chemistry ETL |

### Validation Infra (available, need northGate scenarios)

| Project | What |
|---------|------|
| benchScale | IPC compliance validation |
| agentReagents | Agent configuration reagents |
| bingoCube | Validation framework |

### Not Yet Cloned

| Project | Status |
|---------|--------|
| tideGlass | Sovereign GPS platform — Phase 0 |
| rustChip | Rust toolchain chip |

---

## Remaining Work

### bearDog Credential Authority (P2)

| Work | Status |
|------|--------|
| HSM → Windows DPAPI backend | **SHIPPED** |
| HSM → Linux SecretService backend | **SHIPPED** |
| HSM → Android Keystore backend | NEW |

### Composition Wiring (P2)

| Item | Owner |
|------|-------|
| footPrint: `WS_PATH` → agent bridge | petalTongue |
| footPrint: drawbridge wiring (`PROXY_PATH`) | songBird |
| footPrint: server composition deploy | sporeGate ops |
| tideGlass: drawbridge bonds | songBird |

### Infrastructure / Ops

| Item | Priority |
|------|----------|
| northGate deployment + validation | **P1** |
| DNSSEC on primals.eco | P2 |
| primal.eco inner membrane separation | P2 |
| RustDesk transient to ironGate + flockGate | P2 |

---

## Depot (59 binaries — 4 architectures)

```
x86_64-linux-musl     16   FRESH
aarch64-linux-musl    16   FRESH
aarch64-android       13   FRESH
x86_64-windows-gnu    14   FRESH

BLAKE3 + Ed25519 signed. VPS depot serving.
```

---

*Wave 146a: northGate formalized as final validation target. benchScale +
agentReagents + primalSpring validate before deployment. Manifest target
corrected. 7 garden/infra projects identified as unassigned (available for
team pickup). All milestones hold: Phase 2 14/14, CAC 6/6, Glacial 8/8.*
