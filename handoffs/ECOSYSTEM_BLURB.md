# ecoPrimals Ecosystem Blurb — Wave 151a

**Date**: Jul 25, 2026 22:10 EDT | **Wave**: 151b | **From**: eastGate overwatch
**Posture**: **grapheneGate scenario EVOLVED (golgiBody depot-sourced). bearDog TRANSPLANTED to eastGate for HSM access. SUB-WAVE 151b: all primals evolve to BTSP standard before Nest Atomic.**

---

## WHERE WE ARE

Wave 150 (Tower Atomic) is **done**. Every P0 and P1 is resolved:

| Metric | Value |
|--------|-------|
| Tower vs WireGuard | 353x LAN latency, 1.7x WAN throughput |
| Scenarios | 197, all PASS |
| Known debt | **2** (grapheneGate provenance stale in git — depot fresh on golgiBody) |
| Depot | 28 binaries × 2 architectures, provenance fresh |
| Crypto delegation | songBird → bearDog **6/6 seams DONE** |
| bearDog tests | 13,973+ |
| songBird tests | 14,332+ |
| Fossilized docs | 42+ |

---

## THIS CASCADE — WHAT SHIPPED

| Primal | Delivery | Impact |
|--------|----------|--------|
| bearDog | Publication pen test (Wave 151d) | 3 CRITICAL fixed: error sanitization, auth gating, cipher floor. Android compile fixes for eastGate readiness |
| songBird | BTSP `ClientHello` (268L) | Full 4-step handshake, HMAC-SHA256 challenge-response. Strict mode consumer-side DONE |
| primalSpring | Shadow data + recalibration | 108 new shadow samples across 7 gates. KNOWN_DEBT recalibrated |

### flockGate code teams — ALL CLEAR

Zero remaining Tower code tasks. Tower continues to evolve alongside
Nest Atomic — the electron matures as we build the neutron.

### bearDog TRANSPLANTED to eastGate

bearDog team now operates from **eastGate** — direct ADB access to
grapheneGate (Pixel 8, Titan M2 HSM). This enables:
- Hardware-backed `CredentialStore::AndroidKeystore` validation
- Titan M2 key generation + BTSP enrollment with HSM keys
- grapheneGate deployment testing without cross-gate coordination

---

## SUB-WAVE 151b — BTSP STANDARD EVOLUTION (ALL PRIMALS)

Before Nest Atomic begins, **every primal** that talks to bearDog must
evolve to BTSP. sporeGate already deployed strict mode — legacy plaintext
JSON-RPC is now **rejected**. Primals that don't evolve will lose bearDog
crypto access in Nest Atomic.

### What Each Primal Needs

Implement songBird-style BTSP `ClientHello` handshake (268 lines reference):
1. Send `ClientHello { protocol: "btsp", version: 1, client_ephemeral_pub }`
2. Read `ServerHello { challenge, session_id }`
3. Compute `HMAC-SHA256(FAMILY_SEED, challenge)` → send `ChallengeResponse`
4. Read `HandshakeComplete { cipher, session_id }`

Reference: `primals/songBird/crates/songbird-crypto-provider/src/btsp_client.rs`

### Primal BTSP Status

| Primal | Uses bearDog? | BTSP Status | Action |
|--------|--------------|-------------|--------|
| songBird | Yes (crypto delegation 6/6) | **DONE** | Reference implementation |
| barracuda | Yes (signing) | NEEDS EVOLUTION | Implement ClientHello |
| loamSpine | Yes (DAG signing) | NEEDS EVOLUTION | Implement ClientHello |
| sweetGrass | Yes (braid attestation) | NEEDS EVOLUTION | Implement ClientHello |
| rhizoCrypt | Yes (lineage crypto) | NEEDS EVOLUTION | Implement ClientHello |
| coralReef | Minimal | NEEDS EVOLUTION | Implement ClientHello |
| squirrel | Yes (secrets) | NEEDS EVOLUTION | Implement ClientHello |
| biomeOS | Yes (identity) | NEEDS EVOLUTION | Implement ClientHello |
| nestGate | Minimal (CAS hashing) | LOW PRIORITY | Can use local crypto |
| toadStool | No direct | SKIP | No bearDog dependency |
| petalTongue | No direct | SKIP | No bearDog dependency |
| skunkBat | Yes (cipher negotiation) | NEEDS EVOLUTION | Implement ClientHello |
| cellMembrane | Yes (lineage validation) | NEEDS EVOLUTION | Implement ClientHello |

### Deployment Rollout (sporeGate — ALREADY LIVE)

sporeGate has already deployed `BEARDOG_AUTH_MODE=enforced` +
`BEARDOG_UDS_REQUIRE_BTSP=1`. Remaining gates:

| # | Gate | Status |
|---|------|--------|
| 1 | sporeGate | **DEPLOYED** |
| 2 | eastGate | Deploy after bearDog team validates |
| 3 | flockGate | Deploy after code teams evolve primals |
| 4 | golgiBody | Deploy after confirming depot operations |
| 5 | Future gates | USB bundle updated with BTSP defaults |

---

## EXECUTING NOW

### bearDog (eastGate) — grapheneGate HSM Validation

Scenario `s_graphenegate_readiness` evolved to check golgiBody depot provenance
(not local filesystem). Deploy path: golgiBody → eastGate → ADB → grapheneGate.
Future: phone self-enrolls via Tower mesh.

Remaining debt (2): provenance.toml stale in git (sporeGate refreshed via
rsync but didn't commit). Resolve by committing provenance on golgiBody.

### Gate Enrollment (sporeGate)

| # | Task | Priority |
|---|------|----------|
| 1 | southGate enrollment (house2) | P1 |
| 2 | strandGate enrollment (dual EPYC) | P1 |

### Overwatch (eastGate)

| # | Task | Priority |
|---|------|----------|
| 1 | GLOSSARY.md refresh (138b → 151b) | P2 |
| 2 | PRIMAL_REGISTRY.md refresh (109 → 15 primals) | P2 |

---

## FORWARD WORK — CHIMERA + NEST ATOMIC

### Chimera Phase 0 — UNBLOCKED

Shared library extraction: bearDog crypto + songBird routing + skunkBat
defense → `libtower.so`. Crypto delegation 6/6 means composition model
is validated. This is pure refactoring — no new APIs, just collapsing UDS
hops into shared memory.

### grapheneGate → Standalone Android Platform

**Phase 1** (eastGate, NOW): HSM validation executing — see EXECUTING NOW above.

**Phase 2** (eastGate + sporeGate): Full NUCLEUS deploy — Tower Atomic transport,
cellMembrane instance, depot-sourced aarch64 binaries, mesh enrollment as
autonomous peer with BTSP strict mode from day one. grapheneGate becomes
the ecosystem's Android platform — peer, not peripheral.

### Nest Atomic (Wave 151) — DATA + PROVENANCE + rootPulse

The neutron layer: real data movement through Tower transport, per-object
encryption via bearDog, content-addressed storage via nestGate CAS.

| Phase | Scope | Teams |
|-------|-------|-------|
| 0 | nestGate CAS integration testing (put/get/verify) | eastGate + flockGate |
| 1 | loamSpine prototype (append-only DAG ledger) | eastGate |
| 2 | rhizoCrypt wiring (cross-repo DAG tracking) | eastGate + flockGate |
| 3 | sweetGrass semantic braids (per-gate attestations) | all |
| 4 | rootPulse composition (biomeOS orchestrates Trio) | all |
| 5 | golgiBody deployment (rootPulse replaces waterFall) | sporeGate |

### sporePrint Pipeline (parallel)

Zola → petalTongue + nestGate CAS + cellMembrane. Converges with
Nest Atomic Phase 0.

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — 43/43 synced |
| 2 | Ecological | GREEN — 197 scenarios, 2 debt (provenance) |
| 3 | Hardware | AMBER — 4 offline gates |
| 4 | Sovereignty | GREEN — depot fresh, BTSP strict, chimera unblocked |
| 5 | Public Surface | GREEN — 6/6 healthy |
| 6 | Compositions | GREEN — crypto delegation validated |
| 7 | Documentation | GREEN — 42+ docs fossilized |
| 8 | Campus | GREEN — vision documented |

**Fossilized** (F1–F8): Glacial Shift, CAC, Silicon Atheism, Depot/Build,
Cascade, Tower Deep Analysis, sporePrint Transplant, **Tower Completion + Depot**.

---

*Sub-wave 151b: BTSP standard evolution across all primals before Nest Atomic.
bearDog transplanted to eastGate for grapheneGate HSM access. grapheneGate
scenario evolved to golgiBody depot-sourced deploy path. sporeGate BTSP strict
mode LIVE. Tower matures as we build the neutron. 197 scenarios PASS.
43/43 converged.*
