# ecoPrimals Ecosystem Blurb — Wave 151c

**Date**: Jul 26, 2026 10:50 EDT | **Wave**: 151c | **From**: eastGate overwatch
**Posture**: **BTSP SUB-WAVE LANDED. 9/13 primals shipped ClientHello. grapheneGate validated (10/13, software crypto PASS, HSM needs Keystore2 binder). ironGate BACK ONLINE. sporePrint SEO search doors + query routing shipped. Wave 150 wrapping.**

---

## WHERE WE ARE

Wave 150 (Tower Atomic) is closing out. The sub-wave 151b BTSP evolution
landed across 9 primals in a single cascade cycle.

| Metric | Value |
|--------|-------|
| Tower vs WireGuard | 353x LAN, 1.7x WAN |
| Scenarios | 197, all PASS |
| Known debt | **2** (grapheneGate provenance stale in git) |
| BTSP primals | **9/13** shipped ClientHello (2 pending, 2 skip) |
| Depot | 28 binaries × 2 arch (x86_64 + aarch64-musl) |
| grapheneGate validation | 10/13 checks PASS |

---

## THIS CASCADE — WHAT SHIPPED

### BTSP ClientHello (Sub-Wave 151b Response)

| Primal | BTSP Status | Additional Work |
|--------|-------------|-----------------|
| songBird | **DONE** (reference) | Deep debt audit, doc refresh |
| barraCuda | **DONE** | 3-stage BTSP, hardcode elimination, doc refresh |
| coralReef | **DONE** | Deep debt dedup (Wave 152), 3669 tests |
| loamSpine | **DONE** | ProviderConn wiring, TransportEndpoint compliance |
| rhizoCrypt | **DONE** | NDJSON adapter, fail-closed transport, 1883 tests |
| skunkBat | **DONE** | Duplicate getrandom eliminated |
| sweetGrass | **DONE** | sporeprint validation updated |
| cellMembrane | **DONE** | Deep debt sweep, hardcode elimination, getrandom 0.4 |
| squirrel | PENDING | Needs BTSP ClientHello |
| biomeOS | PENDING | Needs BTSP ClientHello |
| nestGate | LOW | Can use local crypto |
| toadStool | SKIP (S340-341 cleanup) | Stale refs, dead code, hardcoded economics fixed |
| petalTongue | SKIP | No bearDog dependency |

### grapheneGate Validation (eastGate AAR)

bearDog built for `aarch64-linux-android` and validated on Pixel 8a:

| Check | Result |
|-------|--------|
| bearDog starts on aarch64 | **PASS** |
| Ed25519 keypair gen | **PASS** |
| Sign/verify roundtrip | **PASS** |
| AES-256-GCM encrypt/decrypt | **PASS** |
| Store/retrieve/list/delete secret | **PASS** (4/4) |
| HSM StrongBox registration | **FAIL** — needs JVM (Keystore2 binder is the path) |
| Persistence across restart | **FAIL** — in-memory only |
| Backend reports keystore | **FAIL** — in-memory |

**Score: 10/13. Software crypto fully operational. Hardware HSM blocked on
Keystore2 binder IPC (Android 12+ exposes hardware keys without JVM).**

**4 depot deployment failures found**: wrong target triple (musl vs android),
UDS bind failure (filesystem vs abstract socket), no HSM code compiled,
binary identity drift. grapheneGate needs `aarch64-linux-android` as a
**third depot architecture**.

### sporePrint (2 AARs)

**SEO Search Doors (151b)**: 8 pages rewritten for unbranded search queries
(e.g., "GPU-Accelerated DADA2 Benchmark"). 96 auto-gen descriptions replaced.
Canonical URLs consolidated. Reproduce/Limitations sections added.

**Query Routing (151c)**: Title templates specialized — only homepage has
full keyword suffix. 313 pages, each with its own search contract. Sidebar
compressed to contextual navigation.

### ironGate BACK ONLINE

ironGate head published (Wave 150t, Jul 21). 4 days behind current HEAD.
Running NUCLEUS services. **Future: self-recovery via mesh** — when a gate
comes back online, cellMembrane should auto-cascade, detect drift, rebuild
stale primals, and re-enroll without manual intervention.

### Other

- **lithoSpore**: External claim convergence standard applied, deep debt sweep
- **toadStool**: S340-341 cleanup (stale refs, dead code, hardcoded economics)

---

## REMAINING — WAVE 150 CLOSE-OUT

### Code (flockGate + eastGate)

| # | Task | Priority | Owner |
|---|------|----------|-------|
| 1 | squirrel BTSP ClientHello | P1 | squirrel (flockGate) |
| 2 | biomeOS BTSP ClientHello | P1 | biomeOS (flockGate) |
| 3 | bearDog Keystore2 binder IPC | P2 | bearDog (eastGate) |
| 4 | `aarch64-linux-android` depot target | P2 | sporeGate + eastGate |

### Deployment (sporeGate)

| # | Task | Priority |
|---|------|----------|
| 1 | ironGate catch-up cascade (4 days behind) | P1 |
| 2 | BTSP strict mode on remaining gates | P1 |
| 3 | Gate enrollment (southGate, strandGate) | P1 |
| 4 | provenance.toml commit on golgiBody | P1 |

### User Tasks (from sporePrint AARs)

| # | Task | Priority |
|---|------|----------|
| 1 | Google Search Console: verify `sporeprint.primals.eco` ownership | P1 |
| 2 | JOSS submission (barraCuda or wetSpring) | P2 |
| 3 | crates.io releases (barraCuda, wetSpring) | P2 |
| 4 | Scientific Computing in Rust Monthly submission | P3 |
| 5 | DADA2 community engagement | P3 |
| 6 | `eco.primal@primal.eco` activation | P3 |

### Overwatch (eastGate)

| # | Task | Priority |
|---|------|----------|
| 1 | GLOSSARY.md refresh | **DONE** (eastGate AAR) |
| 2 | PRIMAL_REGISTRY.md refresh | **DONE** (eastGate AAR) |

---

## FORWARD — NEST ATOMIC + SELF-RECOVERY

### Chimera Phase 0 — UNBLOCKED

`libtower.so`: bearDog crypto + songBird routing + skunkBat defense.
Crypto delegation 6/6 validated. Pure refactoring.

### grapheneGate → Standalone Android Platform

**Phase 1 DONE**: Software crypto validated (10/13).
**Phase 2**: Keystore2 binder for hardware HSM, `aarch64-linux-android` depot target.
**Phase 3**: Full NUCLEUS deploy, mesh enrollment as autonomous peer.

### ironGate Self-Recovery (new goal)

When a gate comes back online after downtime, the mesh should detect it
and the gate should self-heal: cascade, detect stale binaries, rebuild
from depot, re-enroll services. This is a cellMembrane + biomeOS
composition — auto-cascade on mesh reconnect.

### Nest Atomic (Wave 151)

| Phase | Scope | Teams |
|-------|-------|-------|
| 0 | nestGate CAS integration testing | eastGate + flockGate |
| 1 | loamSpine prototype (DAG ledger) | eastGate |
| 2 | rhizoCrypt wiring (dep tracking) | eastGate + flockGate |
| 3 | sweetGrass semantic braids | all |
| 4 | rootPulse composition | all |
| 5 | golgiBody deployment | sporeGate |

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — 43/43 synced |
| 2 | Ecological | GREEN — 197 scenarios, 2 debt, 9/13 BTSP |
| 3 | Hardware | AMBER — ironGate BACK, 3 still offline |
| 4 | Sovereignty | GREEN — BTSP strict LIVE, depot fresh |
| 5 | Public Surface | GREEN — sporePrint SEO shipped |
| 6 | Compositions | GREEN — chimera unblocked |
| 7 | Documentation | GREEN — GLOSSARY + REGISTRY refreshed |
| 8 | Campus | GREEN |

---

*Wave 151c: BTSP sub-wave landed (9/13 primals). grapheneGate validated
(10/13 software, HSM needs Keystore2 binder). ironGate back online.
sporePrint SEO search doors + query routing shipped. 2 primals pending
BTSP (squirrel, biomeOS). Then Nest Atomic. 197 scenarios. 43/43 converged.*
