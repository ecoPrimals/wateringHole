# ecoPrimals Ecosystem Blurb — Wave 133a

**Date**: Jul 6, 2026 10:36 EDT | **Wave**: 133a | **From**: eastGate overwatch
**Posture**: **ENMESH + HARDEN + VALIDATE** — All primal code shipped. Pepti-first deployment enforced. Omada 10G backbone LIVE (house 1 ↔ house 2). Gates coming online as hardware allows.

---

## Ecosystem State

```
LIVE:
  ✅ E2E HTTP: lab.primals.eco → 200 (JupyterHub 5.4.5)
  ✅ LAN mesh: eastGate ↔ ironGate (Omada 10G backbone, house 1 ↔ house 2)
  ✅ WAN mesh: flockGate via golgi relay (2 peers)
  ✅ Mobile: grapheneGate Tower LIVE (bearDog+songBird+skunkBat via ADB)
  ✅ Pepti warehouse: 15/15 binaries per arch — SOLE deployment source
  ✅ Relay: golgi bidirectional, 39/39 parity, 15min timer
  ✅ 13/13 primals STANDBY — zero debt
  ✅ primalSpring: 1096 pass, 0 fail, 123 scenarios
  ✅ Sovereignty: S1-S4 ALL GRADUATED on inner membrane

PHYSICAL TOPOLOGY:
  House 1:  eastGate (orchestrator, neuromorphic, SFP+ to Omada)
            ─── Omada 10G backbone ───
  House 2:  ironGate (basement HPC, SFP+ to Omada)
            strandGate (Dual EPYC, ALIVE .103, SSH pending)
            northGate, southGate, westGate, swiftGate, kinGate
            biomeGate — many already SFP+ into Omada
  Remote:   flockGate (WAN via golgi relay)
  VPS:      golgi (peptidoglycan — built by sporeGate)
  Mobile:   grapheneGate (Pixel 8a, ADB)

MESHED NOW:
  eastGate ←✅→ ironGate      (LAN, 10G Omada backbone)
  eastGate ←✅→ golgi         (WG relay)
  flockGate ←✅→ golgi        (WAN, 2 peers)
  grapheneGate ←✅→ eastGate  (ADB, Tower running)

MESH CANDIDATES (house 2, SFP+ ready, bring online as available):
  strandGate: ALIVE .103 — needs SSH key only
  northGate, southGate, others: OS + pepti pull + mesh.init
```

---

## WAVE 133 FOCUS: Enmesh → Harden → Validate

**The code is done. The architecture is proven. The backbone is live.**

Wave 133 is about three things:

1. **ENMESH** — Bring available house 2 gates into the mesh. Each gate that comes online pulls from pepti and runs `mesh.init`. The 10G Omada backbone is already connecting the houses. Many gates already have SFP+ — enrollment is: SSH + pepti pull + mesh.init.

2. **HARDEN** — Re-enable dark-forest once enrolled gates have bearDog. Validate BTSP enforcement. Confirm security posture meets DARK_FOREST_GLACIAL_GATE_STANDARD.

3. **VALIDATE** — Prove post-primordial deployment model works at scale. Every gate pulls exclusively from pepti. No local builds. Cross-gate `capability.call` works over the mesh. `mesh.peers` shows all enrolled gates. The deployment is deterministic and pepti-authoritative.

**Constraint**: Hardware availability at house 2 is the gating factor. Gates come online as the user physically provisions them. Overwatch optimizes: prioritize highest-value gates, parallelize where possible, never block on a single gate.

---

## FOR: All Gate Enrollments (pepti-first protocol)

Every new gate follows this enrollment sequence:

```bash
# 1. SSH access (physical or key deploy)
ssh <gate>

# 2. Pull binaries from pepti (SOLE source — no local builds)
wget https://membrane.primals.eco/depot/x86_64-unknown-linux-musl/songbird
wget https://membrane.primals.eco/depot/x86_64-unknown-linux-musl/beardog
# ... all 14 primals + nucleus_launcher

# 3. Deploy + start tower composition
chmod +x songbird beardog skunkbat
# Start via nucleus_launcher or systemd

# 4. Mesh enrollment
mesh.init --bootstrap 10.13.37.2:7700
# Verify: mesh.peers shows existing gates
# Verify: capability.call routes correctly

# 5. Validation
health.liveness → {"status":"alive"}
mesh.peers → peer_count >= 1
capability.call → routes through mesh
```

Pepti is the SOLE deployment source. If a binary isn't in pepti, it doesn't deploy. If a gate builds locally, that's a violation of post-primordial standard.

---

## FOR: sporeGate team (CI + VPS builder)

**Context**: sporeGate builds for golgi (VPS). Owns Sovereign CI, pepti warehouse.

**Your items**:

1. **Pepti depot freshness** (P1 — validate)
   - Confirm all 15 binaries (14 primals + nucleus_launcher) are current in depot
   - Both triples: `x86_64-unknown-linux-musl`, `aarch64-unknown-linux-musl`
   - Verify `checksums.toml` matches published binaries

2. **golgi relay metadata** (P2 — investigate)
   - `heads/golgi.toml` last updated Jul 4 (2 days stale)
   - Check: `ssh golgi "systemctl --user status membrane-temporal-cascade.timer"`
   - If dead: restart. If alive: diagnose why HEAD metadata isn't publishing.

3. **strandGate enrollment support** (P1 — when user has physical access)
   - Alive at 192.168.4.103 (DHCP shifted from .100)
   - User deploys SSH key physically → then pepti pull + mesh.init

---

## FOR: flockGate team (WAN mesh validation)

**Context**: WAN validation via golgi relay. Peering DONE.

**Your items**:

1. **Cross-gate dispatch validation** (P1)
   ```json
   {"method":"capability.call","params":{"capability":"jupyter","method":"GET","path":"/hub/api"}}
   ```
   Expected: JupyterHub response routes through mesh relay

2. **Latency characterization** (P2)
   - Measure cross-gate `capability.call` RTT via golgi relay
   - Baseline: ~15ms RTT NYC↔Michigan
   - Document p50/p95/p99

---

## FOR: eastGate (orchestrator + gate enrollment)

**Context**: You are house 1. You connect to house 2 via Omada 10G. You bring gates online as hardware allows.

**Gate enrollment priority** (optimize for highest ecosystem value first):

| Priority | Gate | Why | Blocker |
|----------|------|-----|---------|
| **P1** | strandGate | 64-core EPYC, 256GB ECC — highest raw compute | SSH key deploy (physical) |
| **P2** | northGate | RTX 5090, 9950X3D — most capable single GPU | OS + pepti pull |
| **P2** | westGate | 76TB ZFS — cold storage archive for mesh | Physical delivery + setup |
| **P3** | southGate | 128GB RAM, dual boot, work card slots | OS + pepti pull |
| **P3** | swiftGate | Mobile/compact — staging | OS + pepti pull |
| **P3** | kinGate | Staging/utility | OS + pepti pull |

**After each enrollment**: run primalSpring validation (`cargo test --lib`) to confirm mesh topology reflects new peer. Update `heads/eastGate.toml` with new gate's HEAD SHAs.

**After 3+ LAN peers meshed**: re-enable dark-forest security. All LAN peers will have bearDog — the enrollment prerequisite is met.

---

## Validation Checklist (post-primordial proof)

This wave's success is measured by these assertions:

| # | Assertion | How to validate |
|---|-----------|-----------------|
| 1 | Every deployed gate runs binaries from pepti, not local builds | `sha256sum` matches `checksums.toml` on depot |
| 2 | `mesh.peers` shows all enrolled gates | Query from any gate |
| 3 | Cross-gate `capability.call` routes correctly | flockGate → golgi → ironGate JupyterHub |
| 4 | `health.liveness` returns alive on all enrolled gates | Sweep from eastGate |
| 5 | Dark-forest re-enabled after full LAN enrollment | DARK_FOREST_GLACIAL_GATE_STANDARD check |
| 6 | No gate has local builds in `plasmidBin/primals/` | `ls` should be empty (just `.gitkeep`) |
| 7 | Pepti checksums match across all deployed gates | `checksums.toml` parity |

---

## Repo Status

```
bearDog       6ef436864  gatehouse + Android fix
songBird      40699793   drawbridge wired into orchestrator
skunkBat      e7eaa5d    stable
toadStool     1ec3749    DH-1 resolved
nestGate      d355c8db   platform_detection simplified
biomeOS       0e54e93    v4.33 mega-test split complete
squirrel      45b186b    Wave 129 mock evolution
primalSpring  548e49b    1096 tests, 0 debt
wateringHole  88a78d8    pepti-only deployment model
sporePrint    99bfc9e    living topology
```

---

## Critical Path

```
✅ All primal code DONE
✅ 7/7 stadial criteria CLEAR
✅ Omada 10G backbone LIVE (house 1 ↔ house 2)
✅ Pepti warehouse populated (15/15 per arch)

WAVE 133 — ENMESH + HARDEN + VALIDATE:
1. [ENMESH]   strandGate SSH + pepti pull + mesh.init       → 3rd LAN peer
2. [ENMESH]   northGate/westGate as hardware allows         → fleet expansion
3. [HARDEN]   re-enable dark-forest (after 3+ LAN bearDog)  → security posture
4. [VALIDATE] flockGate cross-gate dispatch                  → WAN mesh proven
5. [VALIDATE] pepti-first deployment proof (checklist above) → post-primordial confirmed
6. [VALIDATE] grapheneGate full NUCLEUS from pepti           → mobile stack complete
7. [OPS]      golgi HEAD metadata fix (D2)                   → freshness publishing

FUTURE:
  - biomeOS cross-gate graph executor → HPC fan-out
  - golgi bearDog gatehouse → sovereign TLS
  - songBird 10G peer detection → large payload routing
  - nestGate westGate ZFS integration → 76TB in mesh
```

---

*Wave 133a — Enmesh what's available. Harden the perimeter. Validate pepti-first. The code waited for the hardware — the hardware is here.*
