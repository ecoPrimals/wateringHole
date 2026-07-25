# ecoPrimals Ecosystem Blurb — Wave 151a

**Date**: Jul 25, 2026 16:05 EDT | **Wave**: 151a | **From**: eastGate overwatch
**Posture**: **TOWER ATOMIC COMPLETE. DEPOT DIVERGENCE P0: 12/13 primals stale (Jun 15), no aarch64 target. cellMembrane code + sporeGate full harvest required.**

---

## WAVE 150 HANDOFF — TOWER ATOMIC DONE

Tower Atomic sprint (150v–150x) is **DONE**. All 7 remaining debt items resolved:

| Delivered | Evidence |
|-----------|----------|
| Tower 353x LAN, 1.7x WAN | 700+ shadow samples, 50-probe benchmarks |
| Genetic enrollment (two-layer) | Mito gate + nuclear lineage → trust tiers |
| Bond-type cipher + backpressure | bearDog 13,973 tests, all P2 clear |
| LAN mesh.init + dispatch priority | songBird peers sorted LAN→overlay→direct |
| CallerContext + UDS hardening | 7 pen scenarios resolved |
| skunkBat publication | SPDX + maturity badge, now public |
| Crash-loop self-recovery | App breaker + systemd, ecosystem-wide |
| Sovereign CI pipeline | Forgejo→build→depot→lineage, 4 phases |
| 5 security architecture docs | whitePaper subGen/ (1,262 lines) |
| Divergence AAR | 5 classes → rootPulse capability map |
| Known debt | 36 → **1** (grapheneGate HSM only) |
| Scenarios | 197, all PASS |
| P0 | CLEAR across all gates |

### Final Wave — 7/7 Remaining Debt RESOLVED

| # | Was | Resolved By | How |
|---|-----|-------------|-----|
| 1 | bearDog retry on connect fail | songBird | `forward_to_local_provider_with_retry` — exponential backoff (100ms, 300ms) |
| 2 | Health check in dispatch path | songBird | `capability.health` JSON-RPC — probes all providers, reports reachability + latency |
| 3 | Socket filesystem watch | songBird | Adaptive socket watch: 2s poll empty → 30s populated (near-instant recovery) |
| 4 | UDS connect-per-call cost | songBird | `ipc_pool.execute_jsonrpc` wired into dispatch path |
| 5 | BTSP on local UDS | bearDog | `BEARDOG_UDS_REQUIRE_BTSP=1` — defense-in-depth, rejects plain JSON-RPC with `-32600` |
| 6 | Capability announcement validation | songBird | `challenge_verify_capabilities` — probe peer after announce, `is_known_peer` gate |
| 7 | Capability revocation | songBird | `mesh.capabilities_revoke` + `revoke_capabilities_to_peers()` — explicit mesh-wide withdrawal |

### bearDog Deep Debt Sweep (this cascade)

| Item | Status |
|------|--------|
| `enrollment.rs` 1,061L monolith → 7 modules | SHIPPED |
| `lineage_proof.rs` tests extracted | SHIPPED |
| Hardcoded `"eth0"` → `BEARDOG_MDNS_INTERFACE` | SHIPPED |
| Hardcoded `/tmp` → `std::env::temp_dir()` | SHIPPED |
| All `redundant_pub_crate` clippy warnings | RESOLVED |
| 13,973+ tests, 0 clippy warnings | CLEAN |

Continuing P2: crypto delegation (6 seams), grapheneGate Android Keystore,
bearDog publication pen test, chimera Phase 0 (post composition).

---

## P0 — DEPOT DIVERGENCE

The `golgiBody` depot (`plasmidBin`) is **stale and incomplete**:

| Problem | Evidence |
|---------|----------|
| `provenance.toml` generated **Jun 15** | 40 days stale |
| Builder identity | `"unknown"` — no gate attribution |
| 12/13 x86_64 binaries from Jul 15 or earlier | Predate Tower hardening, crash-loop breakers, deep debt |
| songBird only recent rebuild (Jul 24) | All others lag by weeks |
| **No aarch64 target directory** | grapheneGate has zero binaries |
| bearDog binary predates defense-in-depth | Enrollment decomp, BTSP strict, genetic enrollment ALL missing |
| skunkBat binary predates public release | Cipher floor, spawn-rate detection missing |

**The sovereign CI pipeline (Phase 2 drift detection) should catch this**, but
sporeGate hasn't run a full harvest since June. The pipeline only fires on
push-triggered rebuilds (Phase 1), not periodic full sweeps.

### cellMembrane code (sporeGate team)

| # | Task | Priority |
|---|------|----------|
| 1 | `provenance.toml` must record `builder = "<gate>"` on harvest | P0 |
| 2 | `plasmid.harvest --all` command: full sweep of all 13 primals | P0 |
| 3 | Multi-target harvest: `targets` field in manifest drives x86_64 + aarch64 | P1 |
| 4 | Periodic drift alarm: `plasmid.status` warns when >7 days stale | P1 |

### sporeGate topology/hardware (deployment)

| # | Task | Priority |
|---|------|----------|
| 1 | Run `membrane plasmid.harvest --all` — full 13-primal rebuild for x86_64 | P0 |
| 2 | Push to golgiBody depot: `membrane plasmid.refresh` | P0 |
| 3 | Install `aarch64-unknown-linux-musl` rustup target + cross-linker | P1 |
| 4 | Run `membrane plasmid.harvest --all --target aarch64-unknown-linux-musl` | P1 |
| 5 | grapheneGate: deploy as floating gate (own cellMembrane, Tower Atomic, LAN/WAN mesh) | P2 |

### grapheneGate evolution path

Current: ADB-tethered to eastGate → primalSpring validates via `PRIMAL_BIND_MODE=tcp_only`

Target: Autonomous LAN/WAN gate → enrolled via `mesh.enroll` with BTSP HMAC,
running Tower Atomic transport, own `cellMembrane` instance, Titan M2 HSM
backing bearDog `CredentialStore::AndroidKeystore`. Interfaces as a peer,
not a peripheral.

---

## NEXT WAVE: NEST ATOMIC — DATA + PROVENANCE + rootPulse

The Nest Atomic is the **neutron** — where Tower Atomic (electron) provides
transport and Node Atomic (proton) provides coordination, the Nest Atomic
provides the data layer that makes both meaningful:

### What Nest Atomic Enables

1. **Real data movement + encryption** — content-addressed objects flowing
   through Tower transport with bearDog per-object encryption, not just
   ping/latency benchmarks
2. **Provenance Trio fully composed** — `rhizoCrypt` (DAG lineage) +
   `loamSpine` (ledger anchoring) + `sweetGrass` (semantic braids) working
   together as a live composition
3. **rootPulse via biomeOS** — the sovereign VCS that replaces the waterFall
   cascade's git-based coordination with DAG-native operations
4. **golgiBody rootPulse deployment** — golgiBody becomes the first gate
   running rootPulse, solving the 5 divergence classes (140 merge commits,
   34 calibration thrashes, 3 data losses) documented in the Wave 150x AAR
5. **nestGate CAS as the backbone** — content-addressable storage provides
   the substrate for both rootPulse (DAG state) and sporePrint pipeline
   (replacing Zola)

### Nest Atomic Composition

| Primal | Role in Nest | Current Status |
|--------|-------------|----------------|
| nestGate | CAS backbone, data storage | LIVE, vendor-free (150u) |
| rhizoCrypt | DAG lineage tracking | Design phase |
| loamSpine | Ledger anchoring | Design phase |
| sweetGrass | Semantic braids | Design phase |
| biomeOS | Orchestration, rootPulse host | Beacon LIVE on eastGate |
| bearDog | Per-object encryption | Genetic enrollment LIVE |
| songBird | Transport for data objects | Tower 353x LAN |

### Phase Plan

| Phase | Scope | Teams |
|-------|-------|-------|
| 0 | nestGate CAS integration testing — put/get/verify cycle | eastGate + flockGate |
| 1 | loamSpine prototype — append-only DAG ledger for gate heads | eastGate |
| 2 | rhizoCrypt wiring — cross-repo dependency tracking in DAG | eastGate + flockGate |
| 3 | sweetGrass semantic braids — per-gate attestations replacing KNOWN_DEBT | all |
| 4 | rootPulse composition — biomeOS orchestrates Trio over Tower transport | all |
| 5 | golgiBody deployment — rootPulse replaces waterFall cascade git workflow | sporeGate + golgiBody |

### What This Solves (from Divergence AAR)

| Divergence Class | Nest Atomic Solution |
|-----------------|---------------------|
| golgiBody auto-publish race | loamSpine append-only ledger (no merge) |
| KNOWN_DEBT calibration thrash | sweetGrass per-gate attestations |
| Blurb overwrite / data loss | rootPulse materialized views from impulses |
| AAR temporal collision | Context braids with TTL (WIP visibility) |
| Cross-repo semantic drift | rhizoCrypt DAG lineage (dep tracking) |

---

## CONTINUING WORK (all teams, parallel to Nest Atomic)

### songBird (flockGate) — Tower debt CLEAR, P2 remaining

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | ~~Failover resilience~~ | ~~P1~~ | **DONE** — retry, health, socket watch |
| 2 | ~~Capability trust~~ | ~~P1~~ | **DONE** — announce validation, revocation |
| 3 | ~~Wire IPC pool into dispatch~~ | ~~P2~~ | **DONE** — `ipc_pool.execute_jsonrpc` |
| 4 | Crypto delegation to bearDog (6 seams remaining) | P1 | IN PROGRESS |
| 5 | songBird `ClientHello` for BTSP strict mode | P2 | NEW — consumer-side of bearDog defense-in-depth |

### bearDog (flockGate) — P2 remaining

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | ~~BTSP on local UDS~~ | ~~P2~~ | **DONE** — `BEARDOG_UDS_REQUIRE_BTSP=1` |
| 2 | grapheneGate Android Keystore validation | P2 | Blocked on hardware |
| 3 | Publication readiness pen test | P2 | Post crypto delegation |

### sporeGate — deployment + depot

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | **Full depot harvest** (all 13 primals x86_64) | **P0** | 12/13 stale |
| 2 | **Depot refresh** to golgiBody | **P0** | After harvest |
| 3 | aarch64 cross-compile setup + harvest | P1 | No target dir |
| 4 | Gate enrollment (southGate, strandGate) | P1 | |
| 5 | grapheneGate as floating autonomous gate | P2 | ADB-only now |

### Chimera Phase 0 (gate: composition validated)

Shared library extraction — bearDog crypto, songBird routing, skunkBat
defense into `libtower.so`. Blocked on songBird crypto delegation (6 seams).

### sporePrint Pipeline (parallel)

Zola → petalTongue + nestGate CAS + cellMembrane. Converges with
Nest Atomic Phase 0 (nestGate CAS integration testing).

---

## DIMENSIONAL SCORECARD

| # | Dimension | Status |
|---|-----------|--------|
| 1 | Temporal/Coordination | GREEN — 43/43 synced |
| 2 | Ecological | GREEN — 197 scenarios, **1 debt** (grapheneGate HSM) |
| 3 | Hardware | AMBER — 4 offline gates |
| 4 | Sovereignty | **AMBER** — Tower 353x, CI LIVE, **depot 40 days stale** |
| 5 | Public Surface | GREEN — 6/6 healthy, skunkBat public |
| 6 | Compositions | GREEN — Tower composition validated, chimera Phase 0 ready |
| 7 | Documentation | GREEN — 33+ docs archived, deep debt swept |
| 8 | Campus | GREEN — vision documented |

**Fossilized** (F1–F7): Glacial Shift, CAC, Silicon Atheism, Depot/Build,
Cascade, Tower Deep Analysis, sporePrint Transplant.

---

*Wave 151a: Tower Atomic COMPLETE (7/7 debt resolved, 197 scenarios PASS).
**P0 DEPOT DIVERGENCE**: golgiBody provenance 40 days stale, 12/13 binaries
predate Tower hardening, no aarch64 target. cellMembrane code team: builder
identity + full harvest command + multi-target. sporeGate topology: execute
full harvest + depot refresh + aarch64 cross-compile. grapheneGate: evolve
from ADB peripheral to floating autonomous gate on LAN/WAN mesh. 43/43 converged.*
