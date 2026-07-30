# ecoPrimals Ecosystem Blurb — Wave 155j

**Date**: Jul 29, 2026 20:30 EDT | **Wave**: 155j | **From**: eastGate overwatch
**Posture**: **NUCLEUS ACHIEVED. Active teams delivered: toadStool S347 Windows fix, coralReef `--bind` alias + Windows fix, cellMembrane `dns.configure`/`dns.apply` shipped. Windows depot 13/14 ready (only beardog.exe stale). 10 teams STANDBY. 2 teams ACTIVE (biomeOS + bearDog). Remaining: biomeOS lifecycle + bearDog crypto.sign.**

---

## NUCLEUS — ACHIEVED

strandGate is the first gate to run all 13 primals as a full NUCLEUS composition:

```
strandGate NUCLEUS (Jul 29, 19:20 EDT):
  Tower:  bearDog ✓  songBird ~ (degraded)  skunkBat ✓
  Nest:   nestGate ✓  loamSpine ✓  sweetGrass ✓  rhizoCrypt ✓
  Node:   barraCuda ✓  coralReef ✓
  Orch:   biomeOS ✓ (COORDINATED, 1,742 caps, 20 ACTIVE endpoints)
  Score:  8/9 healthy | 25 sockets | 674 direct IPC methods
  GPU:    RTX 3090 matmul p50 0.30ms | Pipeline ~2,000 ops/sec
```

blueGate followed with 13/13 primals on Windows (147.5 MB, TCP-only, all stable 2+ hours).

**What NUCLEUS proved**: cross-atomic IPC at sub-ms latency, biomeOS discovers all primals
and transitions endpoints to ACTIVE, GPU compute pipelines work, BTSP trust chain holds.

**What NUCLEUS exposed**: startup ordering is critical (Tower → Nest → Node → biomeOS LAST),
biomeOS graph executor can't reach primals with riboCipher enforcement, bearDog crypto.sign
still returns health stub, songBird TCP registration not wired.

---

## REMAINING WORK — 3 CHAINS

### Chain 1: biomeOS Orchestration Lifecycle (CRITICAL PATH)

| # | Item | Priority | Status |
|---|------|----------|--------|
| 1 | **Graph executor riboCipher fix** | P1 | One-line: `send_ribocipher_jsonrpc_request()` |
| 2 | **BTSP composition broker** for live E2E | P1 | sweetGrass→loamSpine blocked at BTSP auth boundary |
| 3 | **Composition lifecycle management** | P1 | cellMembrane `boot_order` shipped (b7707ee) — biomeOS needs to consume it |
| 4 | **Socket evaporation fix** | P2 | Caps wiped on restart; startup ordering masks it |
| 5 | **Socket path unification** | P2 | `biomeos/` vs `membrane/` — one canonical path |

### Chain 2: bearDog Crypto + Provenance 7/7

| # | Item | Priority | Status |
|---|------|----------|--------|
| 1 | **`crypto.sign_ed25519` real signing** | P1 | Sole blocker for Provenance Trio 7/7 |
| 2 | **bearDog Windows platform gating** | P1 | `UnixStream` not gated — blocks depot `beardog.exe` |

### Chain 3: Windows Depot Freshness (1 stale binary)

| # | Item | Priority | Owner | Status |
|---|------|----------|-------|--------|
| 1 | **beardog.exe** — `UnixStream` not `#[cfg(unix)]` gated | P1 | bearDog | **OPEN** |
| 2 | ~~**toadstool.exe** — GPU module~~ | ~~P1~~ | ~~toadStool~~ | **FIXED** (S347, `2df71399b`) |
| 3 | ~~**coralreef.exe** — unix_jsonrpc~~ | ~~P1~~ | ~~coralReef~~ | **FIXED** (`339eeb7` + `edcd696`) |

Windows depot: **13/14 ready** (toadStool + coralReef fixed, sporeGate can rebuild). Only beardog.exe remains blocked.

---

## TEAMS — ACTIVE vs STANDBY

### ACTIVE (2 teams — blocking NUCLEUS lifecycle)

| Team | Gate | What They Must Do |
|------|------|-------------------|
| **biomeOS** | eastGate | **P1**: Graph executor riboCipher fix. BTSP composition broker. Consume cellMembrane boot_order for composition lifecycle. Socket unification + evaporation. |
| **bearDog** | eastGate | **P1**: `crypto.sign_ed25519` (Provenance 7/7). Windows platform gating (`UnixStream` → beardog.exe, last stale depot binary). |

### STANDBY (10 teams — work complete, close IDE until needed)

| Team | Gate | Why Standby | Resume When |
|------|------|-------------|-------------|
| **cellMembrane** | sporeGate | boot_order SHIPPED (b7707ee). `dns.configure`/`dns.apply` SHIPPED (2b82722, 1,247 tests). | biomeOS needs composition lifecycle integration. |
| **toadStool** | strandGate | S347 Windows fix SHIPPED (`2df71399b`). 9,193 tests. depot unblocked. | sporeGate depot rebuild of `toadstool.exe`. |
| **coralReef** | strandGate | Windows fix + `--bind` alias SHIPPED (`edcd696`). 3,527 tests. STANDBY-ready. | sporeGate depot rebuild of `coralreef.exe`. |
| **songBird** | eastGate | P0 fixed. `d9bda555` shipped. 14,835 tests. | biomeOS TCP registration (P2). |
| **sweetGrass** | westGate | G3 E2E + UUID fix shipped. 1,639 tests. | bearDog crypto.sign (Provenance 7/7). |
| **rhizoCrypt** | westGate | Cross-compile clean. `--bind` alias. 1,900 tests, 93.8% coverage. | NUCLEUS lifecycle testing. |
| **loamSpine** | westGate | Registry fixed. `--bind` alias. 1,739 tests. | bearDog crypto.sign (Provenance 7/7). |
| **nestGate** | westGate | CAS verified. 13,095+ tests. Zero unsafe. | AlphaFold ingestion. |
| **petalTongue** | westGate | Stable. 6,605 tests. v1.7.0. | WASM validation. |
| **squirrel** | westGate | Stable. 763 tests. | Capability testing. |

### GATE STANDBY

| Gate | Status | Resume When |
|------|--------|-------------|
| **strandGate** | **NUCLEUS ACHIEVED.** Maintain composition. | NUCLEUS lifecycle ships (biomeOS manages startup). |
| **blueGate** | **13/13 Windows.** Infrastructure proof. | biomeOS orchestration + fresh depot (3 binaries). |
| **swiftGate** | HW ready. | After blueGate NUCLEUS stable. |
| **ironGate** | Online. | Tower + HDD enclave experiment. |
| **southGate** | HW ready. | Enrollment. |

### GATE ACTIVE

| Gate | Status | Next |
|------|--------|------|
| **eastGate** | Overwatch. | Coordinate biomeOS + bearDog. Windows CI gate. |
| **westGate** | Broker LIVE. 704 caps. 3,216 CAS. | **Add Compute Trio → second NUCLEUS.** Then AlphaFold. |
| **sporeGate** | 9/11 healthy. Depot 33 binaries. | **Rebuild toadstool.exe + coralreef.exe** (fixes shipped). Await beardog.exe. |

---

## METRICS

| Metric | Value |
|--------|-------|
| NUCLEUS gates | **1** (strandGate) + 1 infrastructure proof (blueGate) |
| Primal tests | **~63K+** |
| Signal graphs | **27** |
| BTSP | **13/13** |
| Linux depot | **19/19** (16 musl + 3 glibc) |
| Windows depot | **13/14 ready** (toadStool + coralReef fixed; beardog.exe stale) |
| Gates online | **10** |
| strandGate NUCLEUS caps | **1,742** |
| strandGate IPC methods | **674** |
| GPU | RTX 3090 matmul p50 **0.30ms**, pipeline **~2,000 ops/sec** |
| CAS objects (westGate) | **3,216** on ZFS 25.3TB |
| Provenance Trio | **6/7** (bearDog crypto blocks 7/7) |
| sweetGrass P2 UUID | **FIXED** (`4b5167b`) |
| cellMembrane boot_order | **SHIPPED** (b7707ee) |
| cellMembrane dns.configure | **SHIPPED** (2b82722, 1,247 tests) |
| Fossilized dimensions | **13** |
| P0s | **ZERO** |

---

## WHAT'S NEXT — NUCLEUS LIFECYCLE

```
Achieved:    strandGate = NUCLEUS (manual startup)
             blueGate = 13/13 (no orchestration)

Next:        biomeOS lifecycle (auto startup ordering + health gates)
             bearDog crypto.sign (Provenance 7/7)
             3 Windows platform gates (beardog.exe, toadstool.exe, coralreef.exe)
             westGate = second NUCLEUS (add Compute Trio to existing Broker+Nest)
             AlphaFold ~1TB ingestion through Nest Atomic pipeline

End state:   NUCLEUS self-managing on multiple gates via biomeOS
             Provenance 7/7 with real Ed25519 signing
             Full Windows depot (14/14)
             AlphaFold data with full provenance chain
```

---

*Wave 155j — NUCLEUS ACHIEVED. toadStool S347 + coralReef --bind + cellMembrane
dns.configure all shipped. Windows depot 13/14 ready. 10 teams STANDBY, 2 ACTIVE
(biomeOS + bearDog). Remaining: biomeOS composition lifecycle, bearDog crypto.sign +
Windows platform gate. ~63K+ tests. 10 gates. 13 fossilized dimensions.*
