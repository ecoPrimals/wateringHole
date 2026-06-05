# Wave 79 Primal Blurbs — Copy-Paste to Teams

**Date**: 2026-06-05 | **From**: eastGate overwatch
**Context**: All 4 upstream gaps RESOLVED. UDS-only stadial gate established.
Transport evolution formalized (Phase 2: Songbird-routed IPC).

Copy each section to its team. Primals only — springs inherit.

---

## bearDog

Wave 142, 15,004+ tests, 90.5% coverage. Ecosystem reference tier.

**What landed**: BD-TRUST-01 `auth.exchange_trust` is LIVE in Songbird
`mesh.init` (commit `ec978b86`). Zero-operator bidirectional trust
seeding works end-to-end. Your work is shipping in the mesh. Thank you.

**Wave 79 ecosystem update**: UDS-only is now the stadial gate default.
No standalone TCP ports. Songbird handles all routing. Transport
evolution formalized — primals must evolve toward transport ignorance
(no hardcoded `TcpListener::bind` or `UnixListener::bind`). See
`primalSpring/docs/TRANSPORT_EVOLUTION.md`.

**Action items**: NONE. You are reference tier. S4 auth graduation ~Jun 9.

---

## songBird

Wave 81, 14,004+ tests, 73.4% coverage. BD-TRUST-01 + deep debt shipped.

**What landed**:
- `auth.exchange_trust` wired into `mesh.init` — the P0 blocker is DONE
- Deep debt: 8 hardcoded port literals → `songbird_types::defaults` constants
- Production stubs hardened (NFC x25519_dh, lineage verify, TLS extract)
- `capability_registry.toml` shipped
- Race conditions + flaky test patterns eliminated

**Wave 79 ecosystem update**: You are now the universal routing bus.
Transport evolution FRAGO issued (`wave79-transport-evolution-capability-routing`).

**P0 — Transport Phase 2**: Evolve `ipc.resolve` to return
transport-qualified endpoints:
```json
{ "transport": "uds", "path": "/run/membrane/beardog.sock" }
{ "transport": "mesh_relay", "peer_id": "strand-gate", "capability": "security" }
{ "transport": "tcp", "host": "192.168.1.144", "port": 7700 }
```
This enables Tower Atomic to select transport without string parsing.
`CompositionContext` will query Songbird instead of probing sockets.
This is the keystone for O(n) gate deployment.

**P1 — Coverage**: 73.4% → 90%. Largest quantitative gap in the ecosystem.
Every other primal with significant surface is 80%+. Focus on pure-logic
modules in `songbird-config`, `songbird-nfc`, `songbird-tls`.

**P3 — Doc drift**: README says v0.2.8-wave76. You're at v0.2.9-wave81.
Sync banner.

---

## biomeOS

Wave 78, v4.08, 7,983+ tests, 90%+ coverage. Ecosystem reference tier.

**Wave 79 ecosystem update**: UDS-only stadial gate established. Transport
evolution target: `graph.deploy` evolves to capability-only node declarations
(no `transport` field in graph metadata — biomeOS + Songbird select transport
at deploy time based on topology). This is Phase 3 target, not immediate.

**Action items**: NONE. You are reference tier.

---

## toadStool

Session 293, 23,000+ tests, ~83.6% coverage. Largest test suite.

**Wave 79 ecosystem update**: `capability_registry.toml` delivered — thank you.
UDS-only stadial gate: no standalone TCP ports in Tower Atomic. Transport
evolution FRAGO issued — primals must evolve toward transport ignorance.
toadStool's hardware containment crates (VFIO, DRM) are justified exceptions
but all IPC entry points should accept transport injection from the launcher.

**P2 — Coverage**: 83.6% → 90%. Hardware-dependent paths are inherently
gapped. Focus coverage on non-VFIO code paths: coordination, dispatch,
JSON-RPC surface, CallerContext logic.

**P2 — Transport prep**: Ensure `--socket` / `--unix` flags are respected
when passed by `nucleus_launcher`. VPS binary needs update to respect
UDS socket path from launcher (currently uses `/tmp/biomeos/`).

---

## nestGate

Session 94b, 12,551+ tests, ~84% coverage.

**Wave 79 ecosystem update**: `capability_registry.toml` delivered — thank you.
UDS-only stadial gate active. VPS binary currently uses symlink
(`/run/membrane/nestgate.sock` → `/tmp/`). Target: native `--socket`
flag so the launcher controls the path.

**P1 — Binary UDS compliance**: The deployed binary must respect
`--socket /run/membrane/nestgate.sock` natively (not via `/tmp` symlink).
This is blocking the VPS binary refresh. When the binary supports `--socket`
path specification, plasmidBin can deploy port-free.

**P2 — Coverage**: 84% → 90%. Focus on content pipeline and HTTP API handlers.

---

## squirrel

Wave 76, 7,098+ tests, 90.1% coverage. `config/capability_registry.toml` ✓.

**Wave 79 ecosystem update**: UDS-only stadial gate established. Transport
evolution formalized. No action required — your primal is clean.

**Action items**: NONE. Clean.

---

## barraCuda

Wave 78, 4,393+ tests, ~81% coverage. `config/capability_registry.toml` ✓.

**Wave 79 ecosystem update**: UDS-only stadial gate. Transport evolution
FRAGO issued. All IPC entry points should be transport-agnostic.

**P2 — Coverage**: 81% → 90%. GPU hardware coverage requires real hardware
(llvmpipe cap). Focus coverage on non-GPU paths: stats, linalg,
precision routing, dispatch coordination.

**P2 — Transport prep**: Ensure `--socket` / `--unix` flags work for
launcher-injected UDS paths. No `0.0.0.0` bind in default mode.

---

## petalTongue

Wave 78, 6,259+ tests, ~85%+ coverage. Deep debt passes 4-5 done.

**Wave 79 ecosystem update**: UDS-only stadial gate. Coverage sprint
active — continue momentum. Transport evolution: ensure IPC listener
accepts launcher-injected transport (UDS path from `--socket`).

**P2 — Coverage**: 85% → 90%. Continue sprint on content-backend and
discovery integration paths. You're close.

**P2 — Transport compliance**: Kill stale process on port :8080 was needed
on VPS. Ensure binary doesn't default to TCP bind when `--socket` is passed.

---

## rhizoCrypt

Wave 78, 1,683+ tests. `config/capability_registry.toml` ✓.

**What landed**: ALL previous blurb items DELIVERED:
- Mesh-trust session auto-provision ✓
- DAG append wired to `poll_events()` ✓
- Lifecycle wiring (`spawn_mesh_poller()`) ✓
- Registry moved to `config/` ✓

**Wave 79 ecosystem update**: UDS-only stadial gate. Your binary already
supports `--unix` for UDS. VPS unit updated (Wave 78, `--port` removed).
Clean posture.

**Action items**: NONE. VPS binary refresh will deploy your latest.

---

## loamSpine

Wave 76, 1,600+ tests, 90.9% coverage. `config/capability_registry.toml` ✓.

**Wave 79 ecosystem update**: UDS-only stadial gate. VPS unit already
updated (Wave 78, `--port 9700` removed, `--socket` only). Clean posture.

**Action items**: NONE. Clean.

---

## sweetGrass

Wave 78b, v0.7.49, 1,623+ tests, 91.7% coverage. `config/capability_registry.toml` ✓.

**Wave 79 ecosystem update**: UDS-only stadial gate. VPS unit updated
(Wave 78, `--port 9850` removed). rhizoCrypt DAG append + lifecycle
wiring is DELIVERED — attribution braid testing against live mesh events
is now UNBLOCKED. This is your next evolution path.

**Action items**: Attribution braid testing against live mesh events
(unblocked by rhizoCrypt delivery). Low priority until VPS binary refresh.

---

## coralReef

Wave 78, 3,307+ tests. `config/capability_registry.toml` ✓.

**Wave 79 ecosystem update**: UDS-only stadial gate. Transport evolution
formalized. Pure compiler domain — transport compliance is straightforward.

**Action items**: NONE. Clean.

---

## skunkBat

Wave 76b, v0.2.3, 500+ tests, 90%+ fn coverage. `config/capability_registry.toml` ✓.

**Wave 79 ecosystem update**: UDS-only stadial gate. westGate enrollment
FRAGO updated for UDS-only posture + BD-TRUST-01 auto trust.

**P1 — Binary UDS compliance**: The deployed binary currently runs
TCP-only on VPS (localhost :9140, `--no-uds`). Target: native UDS support
so skunkBat can run port-free like other primals. This blocks full Tower
Atomic compliance on VPS.

**P2 — westGate readiness**: When westGate hardware arrives, skunkBat is
the primary primal. Enrollment FRAGO at
`impulses/active/wave73-westgate-skunkbat-enrollment.toml`.

---

## sourDough (meta-primal, no action)

v0.3.1, 281+ tests. Meta-tool, not a runtime service. No action needed.
