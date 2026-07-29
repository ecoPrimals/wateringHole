# ecoPrimals Ecosystem Blurb — Wave 155i

**Date**: Jul 29, 2026 18:30 EDT | **Wave**: 155i | **From**: eastGate overwatch
**Posture**: **NUCLEUS CONVERGENCE. All three atomics proven (Tower 6 gates, Nest 2 gates, Node 1 gate). biomeOS composition broker LIVE (704 caps, COORDINATED). ZERO P0s. Remaining: biomeOS full composition lifecycle, bearDog crypto.sign, Windows depot pipeline. First NUCLEUS deployment is the next milestone.**

This is the single handoff document for every team — gate teams and code teams.
Read "Where We Are", find your work, act.

---

## WHERE WE ARE — NUCLEUS CONVERGENCE

All three atomic compositions are now **proven independently**:

```
NUCLEUS = Tower + Nest + Node + biomeOS
        = (bearDog + songBird + skunkBat)                    ← 6 gates LIVE
        + (nestGate + rhizoCrypt + loamSpine + sweetGrass)    ← 2 gates LIVE
        + (toadStool + barraCuda + coralReef)                 ← 1 gate VALIDATED
        + biomeOS                                             ← COORDINATED on westGate
```

| Composition | Gates | Status | biomeOS Orchestrated? |
|-------------|-------|--------|-----------------------|
| **Tower** (3) | westGate, strandGate, blueGate, grapheneGate, eastGate, sporeGate | LIVE | 8 signal graphs. Direct IPC works. |
| **Nest** (7+Tower) | westGate (ZFS, 3,216 CAS), blueGate (Windows, 10/10) | LIVE | 9 signal graphs. Capability routing E2E. Graph execution needs riboCipher fix. |
| **Node** (3+Tower) | strandGate (RTX 3090, 746 pipelines/sec) | VALIDATED | 3 signal graphs. Not yet orchestrated live. |
| **NUCLEUS** (13) | — | **NEXT** | 27 signal graphs defined. Full lifecycle: NOT YET. |

**The gap is not the primals — it's the orchestration.** All 13 primals compile, pass tests, and run independently. What remains is biomeOS evolving from composition broker (capability routing) to **composition lifecycle manager** (startup ordering, health gating, composition transitions, graph execution across all atomics).

---

## WHAT REMAINS — ORGANIZED BY BLOCKER CHAIN

### Chain 1: biomeOS → NUCLEUS Orchestration

biomeOS must evolve from "routes capabilities" to "manages compositions":

| # | Item | Priority | Owner | Blocks |
|---|------|----------|-------|--------|
| 1 | **Graph executor riboCipher fix** — `send_ribocipher_jsonrpc_request()` | P1 | biomeOS | Orchestrated graph execution across compositions |
| 2 | **Socket unification** — `biomeos/` vs `membrane/` split, symlink workarounds | P2 | biomeOS | Clean multi-composition deployments |
| 3 | **Socket evaporation** — Neural API restart wipes capabilities | P2 | biomeOS | Stable long-running NUCLEUS |
| 4 | **Composition lifecycle management** — startup ordering, health gates, Tower→Nest→Node→NUCLEUS transitions | P1 | biomeOS + cellMembrane | NUCLEUS deployment without shell scripts |
| 5 | **Primal CLI flag standardization** — `--bind` vs `--host` vs `--bind-address` vs `--http-port` | P2 | Multi | biomeOS can't uniformly start primals |

### Chain 2: bearDog → Provenance Trio 7/7

| # | Item | Priority | Owner | Blocks |
|---|------|----------|-------|--------|
| 1 | **`crypto.sign_ed25519` real signing** — returns health stub today | P1 | bearDog | loamSpine `entry.append`, Provenance Trio 7/7, Nest Atomic full E2E |

### Chain 3: Depot Pipeline → Windows + Multi-Gate

| # | Item | Priority | Owner | Blocks |
|---|------|----------|-------|--------|
| 1 | **Windows depot rebuild** — 14 `.exe` from 07/16, need `d9bda555` + Wave 155i | P1 | sporeGate | Depot-path Windows deployments (swiftGate, future gates) |
| 2 | **Windows CI gate** — `cargo check --target x86_64-pc-windows-gnu` | P1 | eastGate/CI | Compile errors slip through (3 missed in P0 fix) |
| 3 | **blueGate sub-builder enrollment** — second build node under sporeGate | P2 | blueGate + sporeGate | Windows-native builds, depot throughput |

### Chain 4: Gate Expansion → NUCLEUS on Multiple Gates

| # | Item | Priority | Owner | Blocks |
|---|------|----------|-------|--------|
| 1 | **Node Atomic on blueGate** — add toadStool+barraCuda+coralReef to existing Nest 10/10 | P2 | blueGate | First NUCLEUS on Windows |
| 2 | **Node Atomic on westGate** — add Compute Trio to existing Nest+Broker deployment | P2 | westGate | First NUCLEUS on Linux |
| 3 | **swiftGate Tower** — second Windows proof | P3 | swiftGate | Fleet depth |
| 4 | **AlphaFold ingestion** — ~1TB from northGate through Nest Atomic pipeline | P3 | westGate | First real data through provenance pipeline |

### Remaining P2s (not blocking NUCLEUS)

| # | Item | Owner |
|---|------|-------|
| 1 | songBird `services: 0` — TCP primal registration not wired | songBird |
| 2 | songBird PID file Unix paths on Windows | songBird |
| 3 | sweetGrass braid_id→UUID mismatch | sweetGrass |
| 4 | sporeGate mesh.reachability + rootpulse.ledger (2/11 degraded) | sporeGate |
| 5 | hotSpring Forgejo pack corruption | eastGate admin |

---

## GATE TEAMS — STATUS + NEXT WORK

### House 1 (peptidoglycan anchor: sporeGate)

| Gate | Status | NEXT |
|------|--------|------|
| **sporeGate** | 9/11 HEALTHY. Linux depot 19/19 current. | **Windows depot rebuild.** Sub-builder integration with blueGate. |
| **eastGate** | ONLINE. Overwatch. | **Windows CI gate.** bearDog crypto handoff. biomeOS composition lifecycle. |
| **northGate** | ONLINE (Windows). DAILY DRIVER. | **Data source only.** AlphaFold ~1TB staged for westGate Nest ingestion. |

### House 2 (peptidoglycan anchor: blueGate)

| Gate | Status | NEXT |
|------|--------|------|
| **blueGate** | **NEST 10/10** (Windows). 107.6 MB, TCP-only. | **Node Atomic** (add Compute Trio). Then NUCLEUS. Sub-builder enrollment. |
| **strandGate** | **NODE ATOMIC VALIDATED**. 450 methods, 746 pipelines/sec. | Add Nest primals → **NUCLEUS**. Full BTSP validation. |
| **westGate** | **BROKER LIVE**. 704 caps. 3,216 CAS. 20 sockets. | **Graph executor fix → Add Node Atomic → NUCLEUS.** AlphaFold ingestion. |
| **swiftGate** | ONLINE (Windows) | Tower Atomic (G1 second Windows proof). |
| **ironGate** | ONLINE | Tower + HDD enclave experiment. |
| **southGate** | HW READY | Enroll → Tower. |

---

## CODE TEAMS — NEXT WORK

### biomeOS (eastGate — composition lifecycle evolution)

> **biomeOS** — Wave 155i. **COMPOSITION BROKER LIVE. NUCLEUS ORCHESTRATOR: NEXT.**
> v4.45 | 8,564 tests | 27 signal graphs | 704 capabilities on westGate
>
> **Delivered**: riboCipher framing, BTSP session propagation, capability routing E2E.
>
> **Next**:
> 1. Graph executor riboCipher fix (one-line: `send_ribocipher_jsonrpc_request()`)
> 2. Socket path unification (`biomeos/` = `membrane/` — one canonical path)
> 3. Socket evaporation fix (capability persistence across restarts)
> 4. **Composition lifecycle management**: biomeOS starts/stops primals in correct order,
>    gates composition transitions (Tower healthy → start Nest → Nest healthy → start Node),
>    replaces `nucleus_launcher.sh` with signal-graph-driven orchestration.
> 5. Standardize primal bind flags (proposal → teams adopt)

### bearDog (eastGate — crypto signing)

> **bearDog** — Wave 155i. 11,993 tests. BTSP 13/13.
>
> **Next**: `crypto.sign_ed25519` — replace health stub with real Ed25519 signing.
> This is the **sole P1 blocker for Provenance Trio 7/7**. loamSpine `entry.append`
> calls bearDog to sign, gets a health response instead of a signature.

### songBird (eastGate — Windows transport maturity)

> **songBird** — Wave 155i. 14,835+ tests. `d9bda555` (3 Windows fixes).
>
> **Next**: TCP primal registration (services: 0 on blueGate), PID file path
> portability, riboCipher probe noise reduction. These are P2s — songBird is
> operational on all gates.

### Provenance Trio: nestGate + rhizoCrypt + loamSpine + sweetGrass (westGate)

> **Provenance Trio** — Wave 155i. **6/7 live.** G3 CLOSED (sweetGrass v0.8.0 E2E).
>
> | Primal | Tests | Key Status |
> |--------|-------|------------|
> | nestGate | 13,095+ | CAS on ZFS, 3,216 objects, zero unsafe |
> | rhizoCrypt | 1,456 | BTSP→DAG bridge, cross-gate chain |
> | loamSpine | 1,739 | Registry drift fixed, BTSP handshake dedup |
> | sweetGrass | 1,636 | G3 E2E, LedgerClient, 11 ledger tests |
>
> **Blocked on**: bearDog `crypto.sign_ed25519` (Provenance 7/7).
> **P2**: sweetGrass braid_id→UUID mismatch on `braid.commit`.

### Compute Trio: toadStool + barraCuda + coralReef (strandGate)

> **Compute Trio** — Wave 155i. **NODE ATOMIC VALIDATED.**
>
> | Primal | Tests | Key Status |
> |--------|-------|------------|
> | toadStool | 9,193+ | S346 deep debt, security fail-closed, doctor fixed |
> | barraCuda | 4,957 | RTX 3090 + RX 6950 XT, FHE bit-perfect, 100% pass |
> | coralReef | 3,527 | 463 `.expect()` purged, PTX modernized |
>
> **Next**: Deploy to westGate or blueGate alongside existing Nest Atomic.
> **Needs**: glibc depot refresh for GPU primals (musl can't dlopen Vulkan).

### cellMembrane (sporeGate — deployment fabric)

> **cellMembrane** — Wave 155i. 1,221 tests. 45+ magic numbers centralized.
>
> **Next**: Windows depot pipeline (cross-build or sub-builder integration).
> `InitSystem` dispatch shipped (systemd/launchd/windows-service/bare) — evolve
> to work with biomeOS composition lifecycle for NUCLEUS deployments.

---

## METRICS

| Metric | Value |
|--------|-------|
| Primal tests | **~63K+** |
| Signal graphs | **27** (Tower 8, Nest 9, Node 3, Meta 5, Braid 2) |
| BTSP | **13/13** |
| Linux depot | **19/19 current** (16 musl + 3 glibc) |
| Windows depot | **14 `.exe` STALE** (07/16) |
| Gates online | **10** (blueGate moved from enrolling) |
| CAS objects | **3,216** on westGate ZFS (25.3TB, ARC 99.98% hit) |
| westGate capabilities | **704** (COORDINATED mode) |
| GPU | RTX 3090 FP64 104T + RX 6950 XT — dual-GPU validated |
| blueGate | **10 primals, 107.6 MB, TCP-only** |
| Jelly strings | **7/8** (FOSSILIZED — D10→F13) |
| Threat categories | **9** (skunkBat) |
| Provenance Trio | **6/7** (bearDog crypto blocks 7/7) |
| P0s | **ZERO** |

---

## NUCLEUS ROADMAP

```
Current state:
  westGate:   Tower ✓  Nest ✓  Node ✗  biomeOS ✓ (COORDINATED)  → add Node = NUCLEUS
  strandGate: Tower ✓  Nest ✗  Node ✓  biomeOS ✗                → add Nest + biomeOS = NUCLEUS
  blueGate:   Tower ✓  Nest ✓  Node ✗  biomeOS ✓ (depot v0.1.0) → add Node + biomeOS v4.45 = NUCLEUS

Fastest path to first NUCLEUS:
  1. biomeOS graph executor fix (unblocks orchestrated execution)
  2. Deploy toadStool + barraCuda + coralReef on westGate (glibc builds)
  3. biomeOS composition lifecycle (startup ordering, health gates)
  4. westGate = first NUCLEUS gate
```

**ZERO P0s.** All prior P0s resolved. The project has shifted from "make primals work"
to "make biomeOS orchestrate all compositions into NUCLEUS." Every primal is code-complete
and test-passing. The remaining work is orchestration, signing, and depot freshness.

---

*Wave 155i — NUCLEUS convergence. Tower (6 gates), Nest (2 gates), Node (1 gate) all
proven. biomeOS broker LIVE (704 caps). bearDog crypto blocks Provenance 7/7. Windows
depot stale. Next: biomeOS composition lifecycle → first NUCLEUS deployment. ~63K+ tests.
27 signal graphs. 10 gates. 13 fossilized dimensions.*
