# ecoPrimals Ecosystem Blurb — Wave 144b

**Date**: Jul 16, 2026 16:30 EDT | **Wave**: 144b | **From**: eastGate overwatch
**Posture**: **PUBLIC + SOVEREIGN. CAC 6/6 COMPLETE. PHASE 2: 12/14 SHIPPED.**

**This cascade**: biomeOS v4.35 shipped full Phase 2 transport (TransportStream,
TransportListener, trait dispatch — 42 files, 1,028 insertions). squirrel shipped
Phase 2 transport + SecretStore trait + production mock evolution (7,171 tests).
nestGate Session 115: ErrorContextExt trait (152 `map_err` sites evolved).
toadStool S335-S336: security migration + structural debt + 32GB cache freed.
cellMembrane round 2: ProbeResult + Priority::Urgent + dead code. bearDog: deep
evolution (mock elimination + libc removal + handoff fossilization). footPrint:
server validation + constants + dead code. songBird: IpcStream migration batch 2.

**12/14 primals shipped Phase 2 transport.** Only bearDog and nestGate remain.

---

## P0: sporePrint Root 404

`primals.eco` root returns 404. sporePrint sidebar slim (37KB→4KB) shipped.
`content.rebuild` needed on golgi to deploy the fix.

**Owner**: golgi operator | **Action**: `membrane content.rebuild`

---

## Phase 2 Transport Status: 12/14 SHIPPED

| Primal | Status | Tests |
|--------|--------|-------|
| songBird | **SHIPPED** — IpcStream + batch 2 (9 crates) | — |
| skunkBat | **SHIPPED** — TransportEndpoint | — |
| petalTongue | **SHIPPED** — PlatformLifecycle + metrics + WS | — |
| sweetGrass | **SHIPPED** — NestGateClient + transport_connect | 1,608 |
| rhizoCrypt | **SHIPPED** — TransportHint deleted | 1,905 |
| coralReef | **SHIPPED** — client+server de-cfg-gate | 3,647 |
| loamSpine | **SHIPPED** — endpoint dispatch + framing | 1,704 |
| barraCuda | **SHIPPED** — TransportListener unified | 5,153 |
| toadStool | **SHIPPED** — glowplug Vulkan + S334-336 | 9,232 |
| cellMembrane | **SHIPPED** — getrandom CSPRNG + registry | 1,073 |
| squirrel | **SHIPPED** — TransportEndpoint + SecretStore | 7,171 |
| biomeOS | **SHIPPED** — TransportStream + TransportListener | 1,001 |
| bearDog | P2 — HSM abstraction pending | — |
| nestGate | P2 — ErrorContextExt done, transport pending | 3,790 |

---

## Remaining Work

### Phase 2 — Last 2 Primals

| Primal | Work | Priority |
|--------|------|----------|
| bearDog | HSM provider → Android Keystore backend | P2 |
| bearDog | HSM provider → Windows DPAPI backend | P2 |
| bearDog | Transport: raw UDS → TransportEndpoint | P2 |
| nestGate | Transport abstraction | P2 |

### Platform-Specific Backends

| Primal | Abstraction | Priority |
|--------|-------------|----------|
| squirrel | SecretStore → Android Keystore backend | P2 |
| squirrel | SecretStore → Windows Credential Manager | P2 |

### Composition Wiring

| Item | Owner | Priority |
|------|-------|----------|
| footPrint: `WS_PATH` → agent bridge | petalTongue | P2 |
| footPrint: drawbridge wiring (`PROXY_PATH`) | songBird | P2 |
| footPrint: server composition deploy | sporeGate ops | P2 |
| tideGlass: drawbridge bonds | songBird | P2 |

### Infrastructure / Ops

| Item | Priority |
|------|----------|
| sporePrint rebuild on golgi (P0 — 404) | **P0** |
| northGate mesh enrollment | P1 |
| DNSSEC on primals.eco | P2 |
| primal.eco inner membrane separation | P2 |
| RustDesk transient to ironGate + flockGate | P2 |

---

## Depot (59 binaries — 4 architectures)

```
x86_64-linux-musl     14   FRESH
aarch64-linux-musl    14   FRESH
aarch64-android       14   FRESH
x86_64-windows-gnu    14   FRESH

BLAKE3 + Ed25519 signed. VPS depot serving.
```

---

*Wave 144b: Phase 2 transport 12/14 SHIPPED (biomeOS + squirrel this cascade).
CAC 6/6 COMPLETE. bearDog and nestGate are the last 2 primals for transport.
squirrel SecretStore trait lays credential store foundation. Active handoffs: 4.
Active impulses: 1. P0: sporePrint root 404.*
