# Glacial Shift Readiness

**Status**: Active tracking document  
**Phase**: Interstadial exit → Stadial entry  
**Last updated**: 2026-05-20

---

## Position

The ecosystem has cleared the interstadial exit gate (~9.5/10). 13/13 primals
at zero debt. cellMembrane VPS operational (relay + TLS/content shadows).
Shadow tracks S1-S3 proven. Single-gate NUCLEUS validated on ironGate + eastGate.

**LAN is live** — Cat6 1G backbone on unmanaged switch connects all gates.
10G (switch + NICs installed, Cat6a cables pending) is an elevation goal for
Tier 2+ large-dataset science, not a deployment blocker.

---

## Readiness Matrix

### Sovereignty Shadows (H2)

| Track | What | Sovereign | Commercial | Status | Cutover gate |
|-------|------|-----------|------------|--------|--------------|
| **S1** | TLS termination | BearDog :8443 (~10ms) | Cloudflare (~120ms) | **LIVE** | 7-day p95 <= 1.5x |
| **S2** | NAT relay | Songbird TURN :3478 | cloudflared tunnel | **LIVE** (100% 3+ days) | 7-day 100% reachable |
| **S3** | Content serving | NestGate + petalTongue (67ms TTFB) | GitHub Pages (111ms) | **LIVE** | 7-day TTFB parity |
| **S4** | Auth | BearDog BTSP dual-auth | OAuth2/PAM proxy | **READY** (code built) | 7-day p95 < 50ms |

**Remaining**: Complete S4 shadow period, then formal 7-day all-track cutover gate.

### cellMembrane (inner membrane)

| Component | Status |
|-----------|--------|
| VPS (157.230.3.183, DO nyc1) | **OPERATIONAL** |
| Channel 2: Songbird TURN relay | **LIVE** |
| Channel 2b: RustDesk hbbs/hbbr | **LIVE** |
| Channel 3: TLS surface (Caddy + ACME) | **LIVE** |
| Tower composition (BearDog + Songbird + SkunkBat) | **DEPLOYED** |
| Nest expansion (rhizoCrypt + loamSpine + sweetGrass) | Tooling shipped, **not deployed on VPS yet** |
| Channel 1: Sovereign DNS (knot-dns) | **PLANNED** |
| Caddy → BearDog ACME replacement | Shadow live, **not cut over** |
| BearDog Vault (encrypted creds at rest) | **PLANNED** (Phase 2) |

### LAN Gate Deployment

| Gate | Hardware | Role | NUCLEUS status | LAN |
|------|----------|------|----------------|-----|
| **ironGate** | i9-14900K, RTX 5070, 96GB | Agentic dev, ABG | **VALIDATED** | 1G |
| **eastGate** | i9-12900, RTX 4070 + Akida, 32GB | Orchestrator, neuromorphic | **VALIDATED** | 1G |
| **northGate** | Ryzen 9950X3D, RTX 5090, 96GB | Gaming primary, heavy compute | Hardware ready, **not deployed** | 1G (10G NIC ready) |
| **southGate** | 5800X3D, RTX 4060 + float 3090s, 128GB | Gaming + compute | Hardware ready, **not deployed** | 1G (10G NIC ready) |
| **westGate** | i7-4771, RTX 2070 Super, 32GB | 76TB ZFS cold storage | Hardware ready, **not deployed** | 1G (10G NIC ready) |
| **strandGate** | Dual EPYC 7452 (64c), 256GB ECC | Bioinformatics | Hardware ready, **not deployed** | 1G |
| **biomeGate** | Threadripper 3970X, 256GB | HBM2 test bench | Active HBM2 bench, **not full mesh** | 1G |
| **swiftGate** | Ryzen 5800X, RTX 3070, 64GB | Mobile/compact | Hardware ready | 1G |
| **flockGate** | i9-13900K, RTX 3070 Ti, 64GB | Remote covalent (WAN) | Config ready, **not deployed** | WAN via cellMembrane |
| **kinGate** | i7-6700K, RTX 3070, 32GB | Staging | Hardware ready | 1G |

**Deployment order** (over existing 1G LAN):
1. westGate (Nest Atomic — cold storage)
2. northGate (Node Atomic — heavy GPU)
3. strandGate (Full NUCLEUS — bioinformatics)
4. biomeGate / southGate (expansion)
5. Plasmodium collective validation

### Deployment Matrix (primalSpring)

| Cell | Status |
|------|--------|
| `tower-x86-homelan-uds` | **PASS** (golden path) |
| `lithospore-x86-vm-uds` | **PASS** |
| `nucleus-aarch64-mixed-tcp` | **BLOCKED** (nestgate aarch64-musl segfault) |
| 41 other cells | **UNTESTED** |

**P0 target**: `nucleus-x86-mixed-uds` — full NUCLEUS over LAN.

### Distributed Covalent (Phase 4)

| Item | Status |
|------|--------|
| Family seed + bootstrap tooling | **READY** |
| cellMembrane VPS rendezvous | **OPERATIONAL** |
| Songbird TCP/WAN fallback | **SHIPPED** (Wave 213-214) |
| NAT traversal (STUN/punch/TURN) | Shipped, **not field-tested** on residential NAT |
| toadStool yield-to-owner dispatch | **DESIGNED** (`max_guest_load`) |
| Cross-gate data dependency staging | **PROTOTYPED** (primalSpring `validation::dependency`) |
| flockGate live deployment | **NOT DEPLOYED** |

### Software Remaining

| Item | Owner | Priority |
|------|-------|----------|
| Ionic bond runtime (WS-1) | biomeOS + primalSpring | MEDIUM |
| biomeOS route `capability.call` → Songbird for remote | biomeOS | MEDIUM |
| Cross-gate `nest.sync` live orchestration | biomeOS | MEDIUM |
| Sovereign DNS (knot-dns) | projectNUCLEUS | LOW |
| BearDog ACME Phase 3 renewal daemon | bearDog | LOW |
| `content.put` publish pipeline (SP-4) | sporePrint + bearDog | LOW |
| Forgejo Actions CI | projectNUCLEUS | LOW |

---

## Glacial Shift Criteria

The glacial shift (stadial entry) is reached when:

1. All 4 sovereignty shadows **cut over** (S1-S4 formal 7-day gate passed)
2. Multi-gate LAN mesh **operational** (3+ gates in Plasmodium collective)
3. cellMembrane Nest expansion **deployed** on VPS
4. At least one remote covalent node (flockGate) **validated** over WAN
5. DNS pointed to sovereign infrastructure
6. Cloudflare/cloudflared **removed** from production data path

---

## References

- `INTERSTADIAL_EXIT_CRITERIA.md` — 5 pillars + shadow schedule
- `SOVEREIGNTY_STANDARDS.md` — calibrate → shadow → cutover protocol
- `CELLMEMBRANE_FIELDMOUSE_DEPLOYMENT.md` — VPS composition spec
- `MEMBRANE_CHANNEL_ARCHITECTURE.md` — 3 channels + RustDesk
- `DARK_FOREST_GLACIAL_GATE_STANDARD.md` — 5 security invariants
- `DISTRIBUTED_COVALENT_DEPLOYMENT.md` — multi-household compute architecture
- `DESKTOP_NUCLEUS_DEPLOYMENT.md` — single-machine full stack
