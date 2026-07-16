# ecoPrimals Ecosystem Blurb — Wave 144a

**Date**: Jul 16, 2026 13:00 EDT | **Wave**: 144a | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. CAC 6/6 SOLVED. PHASE 2 TRANSPORT SURGE.**

**This cascade**: **CAC COMPLETE — all 6 layers solved.** cellMembrane delivered
L3 (tree-parity heads) + L6 (cascade policy) + `getrandom` CSPRNG. rhizoCrypt
shipped L5 (SessionTreeHash full RPC wire, 1,905 tests). Transport Phase 2 surge:
coralReef (client+server de-cfg-gated, 3,647 tests), loamSpine (endpoint dispatch
wired, 1,704 tests), sweetGrass (SHIPPED — was incorrectly TODO), barraCuda
(TransportListener unified accept, 5,153 tests). petalTongue: 163 bare unwrap
eliminated. squirrel transport IN PROGRESS. toadStool S336: security_impl migration, −3,164L extracted, 32GB cache freed.
nestGate debris cleanup (6 dead files, 7 stubs, 44.9GB cache freed).

---

## P0: sporePrint Root 404

`primals.eco` root returns 404. sporePrint shipped sidebar slim (37KB→4KB per
page). `content.rebuild` needed on golgi to pick up the fix.

**Owner**: golgi operator | **Action**: `membrane content.rebuild`

---

## CAC — Newton-Leibniz Pattern: 6/6 COMPLETE

| Layer | What | Status |
|-------|------|--------|
| L1 | Git repos: tree hashes | **SOLVED** (Wave 138c) |
| L2 | Depot: BLAKE3 diff | **SOLVED** (Wave 139e) |
| L3 | Heads: TreeParity auto-publish | **SOLVED** (cellMembrane Wave 143b) |
| L4 | Impulses: content-hash dedup | **SOLVED** (cellMembrane Wave 141b) |
| L5 | rhizoCrypt: SessionTreeHash | **SOLVED** (rhizoCrypt Wave 143b — `ce3d534`) |
| L6 | Cascade: tree-parity policy | **SOLVED** (cellMembrane Wave 143b) |

**The Newton-Leibniz pattern is fully implemented.** Content identity supersedes
temporal identity at every layer of the ecosystem.

---

## Phase 2 Transport Adoption (Abstraction Over Gating)

| Primal | Status | Detail |
|--------|--------|--------|
| songBird | **SHIPPED** | `IpcStream` platform abstraction |
| skunkBat | **SHIPPED** | `TransportEndpoint` adoption |
| petalTongue | **SHIPPED** | `PlatformLifecycle` + metrics + WS bridge |
| sweetGrass | **SHIPPED** | `NestGateClient` + `transport_connect` (1,608 tests) |
| rhizoCrypt | **SHIPPED** | `TransportHint` deleted, all on `TransportEndpoint` (1,905 tests) |
| coralReef | **SHIPPED** | Client+server de-cfg-gated, `BoundAddr::Local` (3,647 tests) |
| loamSpine | **SHIPPED** | Outbound dispatch wired, framing tests (1,704 tests) |
| barraCuda | **SHIPPED** | `TransportListener` enum, unified accept (5,153 tests) |
| toadStool | **SHIPPED** | glowplug Vulkan + security migration + structural debt (S332-S336) |
| cellMembrane | **SHIPPED** | `getrandom` CSPRNG, registry filter (1,073 tests) |
| squirrel | IN PROGRESS | 16 files modified, `endpoint.rs` added (uncommitted) |
| biomeOS | Partial | TCP fallback exists, needs trait dispatch |
| bearDog | P2 | Test extraction wave 4 done, HSM abstraction pending |
| nestGate | Clean | Session 114 PROJECTS_PATH CAS wiring |

**10/14 primals SHIPPED Phase 2 transport.** 1 in progress (squirrel), 3 remaining.

---

## Remaining Work

### Platform-Specific Abstraction Targets

| Primal | Abstraction | Priority |
|--------|-------------|----------|
| bearDog | HSM provider → Android Keystore backend | P2 |
| bearDog | HSM provider → Windows DPAPI backend | P2 |
| squirrel | Credential store → Android Keystore | P2 |
| squirrel | Credential store → Windows Credential Manager | P2 |
| squirrel | Transport: `TransportEndpoint` (in progress) | P1 |
| biomeOS | Neural API transport → trait dispatch | P2 |

### Composition Wiring

| Item | Owner | Priority |
|------|-------|----------|
| footPrint: `WS_PATH` → agent bridge | petalTongue | P2 |
| footPrint: drawbridge wiring (`PROXY_PATH`) | songBird | P2 |
| footPrint: CAS wiring (`PROJECTS_PATH`) | nestGate | P2 |
| footPrint: server composition deploy | sporeGate ops | P2 |
| tideGlass: drawbridge bonds (LINCS, GEO, ChEMBL, NF) | songBird | P2 |

### Infrastructure / Ops

| Item | Owner | Priority |
|------|-------|----------|
| sporePrint rebuild on golgi (P0 — 404) | golgi operator | **P0** |
| northGate mesh enrollment (songbird.exe) | sporeGate ops | P1 |
| DNSSEC on primals.eco | operator | P2 |
| primal.eco inner membrane separation | operator | P2 |
| RustDesk transient to ironGate + flockGate | investigate | P2 |

---

## Depot (59 binaries — 4 architectures)

```
x86_64-linux-musl     14   FRESH
aarch64-linux-musl    14   FRESH
aarch64-android       14   FRESH
x86_64-windows-gnu    14   FRESH

BLAKE3 + Ed25519 signed. VPS depot serving.
```

## Gate Status

```
eastGate     — PRIMARY. Cascade authority.
sporeGate    — NUCLEUS. 13-target builder. 59 depot bins.
golgiBody    — Outer membrane. footprint/ + live. ROOT 404 (P0).
ironGate     — ABG/NF compute. JupyterHub. RustDesk transient.
flockGate    — WAN covalent. 16 bonds. RustDesk transient.
northGate    — Windows mesh target. Enrollment pending.
grapheneGate — StrongBox target. 14/14 Android ecobins.
westGate     — OFFLINE. ZFS cold storage.
```

---

*Wave 144a: CAC 6/6 COMPLETE — Newton-Leibniz fully implemented. Phase 2 transport
surge: 10/14 primals shipped. squirrel in progress. cellMembrane `getrandom` + L3/L6.
rhizoCrypt SessionTreeHash L5 wired. coralReef full de-cfg-gate. barraCuda TransportListener.
P0: sporePrint root 404 (sidebar slim shipped, rebuild needed).*
