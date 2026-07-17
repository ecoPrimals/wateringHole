# ecoPrimals Ecosystem Blurb — Wave 145a (revised)

**Date**: Jul 17, 2026 07:30 EDT | **Wave**: 145a (revised) | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. PHASE 2 TRANSPORT: 14/14 COMPLETE. CAC 6/6 COMPLETE.**

**This revision**: Full dimension sweep across sporePrint + primalSpring.
Re-emitted certification manifest (stale LOC/tests). Fixed page counts
(lab 127, notebooks 98, guidestone 6). Fixed depot arch split to ground
truth (16/16/13/14 = 59). Resolved primalSpring P0: 4 test failures
from missing tideGlass in ecosystem_manifest.toml — now registered.
Fossilized 268 lines of resolved Wave 6-12 content from PRIMAL_GAPS.
bearDog shipped HSM platform backends (WindowsDpapi + LinuxSecretService).
songBird at Wave 145b (AAR + last 3 inline cfg gates eliminated).
sporePrint root 404 on golgi: **RESOLVED** (site serving 200, last-modified today).

---

## Milestones

| Milestone | Status |
|-----------|--------|
| Silicon Atheism Phase 1 (cross-compile 14/14) | **COMPLETE** (Wave 142a) |
| Silicon Atheism Phase 2 (transport abstraction 14/14) | **COMPLETE** (Wave 145a) |
| Content-Addressed Convergence (6/6 layers) | **COMPLETE** (Wave 144a) |
| Glacial Shift Criteria (8/8) | **ALL CLEAR** (since Wave 137b) |
| Depot (59 binaries, 4 architectures) | **OPERATIONAL** |

---

## Phase 2 Transport — Final Tally (14/14)

| Primal | Pattern | Tests |
|--------|---------|-------|
| songBird | `IpcStream` + batch 2 (9 crates) | — |
| skunkBat | `TransportEndpoint` | — |
| petalTongue | `PlatformLifecycle` + metrics + WS | — |
| sweetGrass | `NestGateClient` + `transport_connect` | 1,608 |
| rhizoCrypt | `TransportHint` deleted, all `TransportEndpoint` | 1,905 |
| coralReef | client+server de-cfg-gate, `BoundAddr::Local` | 3,647 |
| loamSpine | endpoint dispatch + framing tests | 1,704 |
| barraCuda | `TransportListener` unified accept | 5,153 |
| toadStool | glowplug Vulkan S332-S336 | 9,232 |
| cellMembrane | `getrandom` CSPRNG + registry filter | 1,073 |
| squirrel | `TransportEndpoint` + `SecretStore` | 7,171 |
| biomeOS | `TransportStream` + `TransportListener` | 1,001 |
| bearDog | raw UDS → `TransportEndpoint` dispatch | — |
| nestGate | `TransportStream` + `TransportListener` | 3,790 |

---

## Remaining Work

### Platform-Specific Backend Evolution (P2)

| Primal | Abstraction | Status |
|--------|-------------|--------|
| bearDog | HSM provider → Windows DPAPI backend | **SHIPPED** (Wave 145a) |
| bearDog | HSM provider → Linux SecretService backend | **SHIPPED** (Wave 145a) |
| bearDog | HSM provider → Android Keystore backend | NEW |
| squirrel | SecretStore → Android Keystore backend | Deferred to bearDog IPC |
| squirrel | SecretStore → Windows Credential Manager | Deferred to bearDog IPC |

### Composition Wiring (P2)

| Item | Owner |
|------|-------|
| footPrint: `WS_PATH` → agent bridge | petalTongue |
| footPrint: drawbridge wiring (`PROXY_PATH`) | songBird |
| footPrint: server composition deploy | sporeGate ops |
| tideGlass: drawbridge bonds | songBird |

### Infrastructure / Ops

| Item | Priority | Status |
|------|----------|--------|
| ~~sporePrint rebuild on golgi (root 404)~~ | ~~P0~~ | **RESOLVED** — serving 200 |
| northGate mesh enrollment | P1 | |
| DNSSEC on primals.eco | P2 | |
| primal.eco inner membrane separation | P2 | |
| RustDesk transient to ironGate + flockGate | P2 | |

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

## Dimension Sweep Findings (July 17, 2026)

### Resolved this sweep
- sporePrint certification manifest: re-emitted (was stale — wrong LOC/tests/date)
- sporePrint page counts: lab 132→127, notebooks 104→98, guidestone 7→6
- sporePrint depot arch: "14×4" → ground truth 16/16/13/14
- sporePrint Zola build: cleared warning (biomeos-validation-summary.md weight)
- primalSpring 4 test failures: tideGlass registered in ecosystem_manifest.toml
- primalSpring PRIMAL_GAPS: fossilized Waves 6-12 (268 lines → summary table)
- primalSpring doc counts: tests 1284→1202, experiments 96→93, depot arch split

### Known remaining drift (P2-P3)
- primalSpring: 128 clippy warnings (mostly `missing_docs` on struct fields)
- primalSpring README body: scenario count says 122 (header says 169 correctly)
- primalSpring: CROSS_SPRING_EVOLUTION.md ecosystem table stale (v0.9.30)
- sporePrint: 129 entity shortcodes in prose not reflected in page taxonomies

---

## Ecosystem Totals (machine-verified July 17, 2026)

| Metric | Value |
|--------|-------|
| LOC (Rust) | 3,571,808 |
| Tests | 116,472 |
| Repos | 42 |
| Primals | 15 |
| Springs | 8 |
| Organizations | 4 |
| sporePrint pages | 302 |
| sporePrint entities | 79 |
| primalSpring scenarios | 169 |
| primalSpring lib tests | 1,202 |
| Depot binaries | 59 (16+16+13+14) |

---

*Wave 145a revised: Full dimension sweep complete. sporePrint certification
re-emitted, page counts corrected, depot arch grounded. primalSpring P0
(4 test failures) resolved — tideGlass registered in ecosystem manifest.
bearDog shipped HSM platform backends. 268 lines fossilized from PRIMAL_GAPS.
All milestones hold: Phase 2 14/14, CAC 6/6, Glacial 8/8. Next: northGate
mesh enrollment, primalSpring clippy triage, remaining composition wiring.*
