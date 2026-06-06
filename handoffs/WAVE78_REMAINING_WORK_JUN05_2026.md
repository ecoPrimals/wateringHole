# Wave 79 Remaining Work — Full Parity & Mesh Deployment

**Date**: 2026-06-05  
**Author**: eastGate overwatch  
**Supersedes**: Wave 76 remaining work (archived)  
**Status**: Active  
**Updated**: Wave 79c — sweetGrass localhost fix landed (P1→RESOLVED), Caddy proxy wired (mesh.primal.eco LIVE), plasmidBin harvest evolved to Rust-canonical, 10G backbone install incoming

---

## Strategic Context

Wave 77 delivered the diderm membrane architecture (3-layer sovereign TLS),
NUCLEUS deep debt evolution (TOML-driven routing, profile-driven launcher,
zero C deps), and live cross-gate trust chain proof (eastGate ↔ strandGate).

Wave 78 upstream deliveries resolved the two highest-priority blockers:
- **SB-TLS-01**: Songbird direct-mode TLS crypto routing (symmetric mesh unblocked)
- **SB-TLS-02**: Phase 3.5 Ed25519 relay signature verification shipped
- **BD-TRUST-01**: bearDog `auth.exchange_trust` (zero-operator trust seeding)
- **RC-POLL-01**: rhizoCrypt `MeshEventListener` polling wired

Wave 79 established the UDS-only stadial gate in primalSpring: launcher defaults
port-free, TCP discovery gated, all graphs `uds_only`, deploy profiles port-free.
BD-TRUST-01 resolved — Songbird wired `auth.exchange_trust` into `mesh.init`.
All 4 upstream gaps are closed. Songbird Wave 81 deep debt pass absorbed.

**Remaining critical path**: Fix 3 headless VPS regressions (toadstool/coralreef/squirrel)
→ redeploy → mesh.init with gate peers → 3-gate mesh proof → stadial entry.
10/13 VPS binaries refreshed. Full pipeline validated (build→harvest→deploy→verify).

---

## Ecosystem Freshness Assessment (Jun 5, 2026)

### Tier 1: HOT — Current Wave 77-78 (delivered Jun 3-5)

| Repo | Gate | Version/Wave | Delivery |
|------|------|--------------|----------|
| bearDog | southGate | v0.9.0 / w140 | `auth.exchange_trust`, auto trust seeding |
| songBird | southGate | v0.2.9-w81 | SB-TLS-01, BD-TRUST-01 mesh.init, deep debt (ports→constants, prod stubs hardened) |
| biomeOS | southGate | v4.07 / w77 | Perceptron training data pipeline |
| toadStool | biomeGate | S290 | CallerContext fan_out, coordination feature-gate |
| sweetGrass | strandGate | v0.7.51 / w79b | Localhost-only default bind, zero hot-path env reads |
| rhizoCrypt | strandGate | v0.14.1 / w77e | MeshEventListener polling (RC-POLL-01) |
| loamSpine | strandGate | w76 | Trust ledger IPC wired |
| NestGate | ironGate | v0.5.0 / s93 | HTTP parity, content serving |
| coralReef | strandGate | v0.2.0 / w78 | Mesh propagation, SPIR-V E2E |
| petalTongue | ironGate | v1.6.6 / w77d | Typed errors, MIME notebook |
| skunkBat | eastGate | v0.2.2 | defense.status health probe |
| primalSpring | eastGate | w79 | UDS-only stadial gate, 893 tests, all upstream gaps resolved |
| wateringHole | eastGate | w78 | Overwatch, fossilized wave77 handoffs |
| cellMembrane | ironGate | w77b | Peptidoglycan formalization |
| barraCuda | strandGate | v0.4.0 / w76 | ML pipeline, mesh.trust_verify |

### Tier 2: WARM — 3-6 Days Behind Wave 78

| Repo | Gate | Last Wave | Gap | Parity Work Needed |
|------|------|-----------|-----|-------------------|
| wetSpring | southGate | w77 (Jun 4) | 1d | V196 forward evolution. southGate health 11/13. |
| neuralSpring | southGate | w76 (Jun 3-4) | 1-2d | V179 deep debt done. southGate mesh needs stabilization. |
| healthSpring | ironGate | w76 (Jun 2) | 3d | V65c glacial cutover done. Absorb Wave 78 patterns. |
| ludoSpring | ironGate | w76 (Jun 3) | 2d | V82 parity done. CONTEXT.md stale, no domain_profile.toml. |
| squirrel | eastGate | w76 (Jun 3) | 2d | 7,098 tests. Env centralization done. |

### Tier 3: COOL — 5+ Days Behind

| Repo | Gate | Last Wave | Gap | Parity Work Needed |
|------|------|-----------|-----|-------------------|
| airSpring | eastGate | w60 (May 29) | 7d | v0.10.0, 1,446 tests. Not on parity sprint. |
| groundSpring | eastGate | w63 (May 30) | 6d | V146, 1,123 tests. Squirrel integration done. |
| hotSpring | biomeGate | S284 (Jun 1) | 4d | v0.6.32, L6. Separate sovereign-compute track. |

### Tier 4: DORMANT (evolve on demand)

| Repo | Last Commit | Assessment |
|------|------------|------------|
| sourDough | Jun 4 | Meta-primal, scaffold tool. Current. |
| bingoCube | May 20 | Validation tool. Hygiene when convenient. |
| rustChip | Apr 30 | Utility crate. Not blocking. |

---

## Parity Gaps — Cross-Cutting

### Missing `domain_profile.toml` (3 springs)

Springs need root `domain_profile.toml` for `litho emit-pseudospore` and
ecosystem classification.

| Spring | Status |
|--------|--------|
| hotSpring | Has nested compchem profiles, no root profile |
| ludoSpring | Missing — composition-only spring |
| neuralSpring | Missing |

### Missing `capability_registry.toml` (6 primals)

Machine-readable TOML registry enables primalSpring `DOMAIN_OWNER_MAP` and
ecosystem tooling to auto-discover capabilities.

| Primal | Current State | Priority |
|--------|---------------|----------|
| songBird | `consumed_capabilities` in code only | MEDIUM |
| toadStool | `provided_capabilities` in handlers | MEDIUM |
| barraCuda | Inline in `primal.rs` | LOW |
| coralReef | Self-knowledge in code/CONTEXT | LOW |
| loamSpine | `CONSUMED_CAPABILITIES` in `niche.rs` | LOW |
| skunkBat | `CONSUMED_CAPABILITIES` in `dispatch.rs` | LOW |

### Coverage vs 90% Stadial Target

| Met (≥90%) | Below |
|------------|-------|
| bearDog (90.5%), biomeOS (90%+), squirrel (90.1%), sweetGrass (91.7%), loamSpine (90.9%), sourDough (95%+), skunkBat (90%+ fn) | **songBird (73%)**, nestGate (84%), petalTongue (~85%), toadStool (~84%), barraCuda (81% llvmpipe) |

---

## Remaining Work by Track

### Track 1: Parity Sprint — COMPLETE ✓ (Wave 76)

All teams absorbed Wave 76 trust infrastructure. 20 handoffs archived.

### Track 2: Live Cross-Gate Validation — PROVEN ✓ (Wave 77d)

Full trust chain proven live: eastGate ↔ strandGate via Songbird mesh +
bearDog ionic tokens + rhizoCrypt DAG provenance.

### Track 3: Diderm Membrane — LIVE ✓ (Wave 77-78)

| Layer | Domain | Status | TLS |
|-------|--------|--------|-----|
| Outer Membrane | primals.eco | LIVE (sporePrint) | Cloudflare |
| Inner Membrane | primal.eco | LIVE | Let's Encrypt (sovereign) |
| Content Layer | nestgate.io | LIVE | Let's Encrypt (sovereign) |
| Peptidoglycan (VPS) | golgiBody/golgiBody-ext | LIVE | Sovereign knot-dns |

### Track 4: VPS Binary Refresh (P0 — blocks mesh)

**Wave 79 deployment (Jun 5)**:
- `nucleus_launcher` v0.9.31 deployed to VPS (musl-static, Wave 79 UDS-only default)
- All 13 systemd units updated: Nest/Node/Meta switched to UDS-only or localhost-bound
- `membrane-socket-bridge.service` created for `/run/membrane/` → `/run/biomeos/` path alignment
- Legacy Nest TCP firewall rules (9500, 9601, 9700, 9850) removed from ufw
- Stale /tmp sockets cleaned

**VPS health (Jun 5, post Wave 79 unit refresh)**: 13/13 services active, 10/12 UDS ALIVE.
`skunkbat` TCP-only (needs binary rebuild for UDS), `squirrel`/`petaltongue` UDS connected
but health probe silent (binary-level framing difference). Mesh not yet initialized.

**Binary versions on VPS** (Wave 79b refresh):
10/13 primals refreshed to HEAD builds (Jun 5). skunkBat v0.2.5, rhizoCrypt v0.14.2,
sweetGrass v0.7.50, nestGate v0.5.0 (notable version jumps). 3 rolled back to pre-refresh
(toadstool/coralreef/squirrel) — headless VPS regressions in new code.

| Step | Owner | Status |
|------|-------|--------|
| Build fresh musl-static binaries for all 13 primals | plasmidBin / eastGate ops | **DONE** — 13 built, harvested with blake3 checksums |
| Deploy to golgiBody `/opt/membrane/` | operator | **DONE** — 10/13 refreshed, 3 rolled back (toadstool/coralreef/squirrel need repo fixes) |
| `nucleus_launcher` v0.9.31 to VPS | eastGate ops | **DONE** — Wave 79 binary deployed |
| Systemd units → UDS-only / localhost | eastGate ops | **DONE** — 13 units updated + songbird-mesh.service created |
| Wire `auth.exchange_trust` in Songbird `mesh.init` | Songbird (code) | **RESOLVED** — Binary refreshed on VPS |
| Fix toadstool/coralreef/squirrel headless mode | cellMembrane (ironGate) | **HANDED OFF** — see WAVE79_VPS_REFRESH_HANDOFF_JUN05_2026.md |
| Call `mesh.init` on VPS Songbird with gate peers | operator | **READY** — can proceed once all 13 binaries confirmed |
| 3-gate mesh proof | primalSpring overwatch | **BLOCKED** on mesh.init |
| S4 auth 7-day gate completion | bearDog + ironGate | ~Jun 9 |
| westGate enrollment | skunkBat + eastGate | Hardware pending |

### Track 4b: DH-1 Socket Standardization + UDS-Only Migration

**Wave 79 (Jun 5)**: Full systemd unit refresh. All 13 primals now have
UDS-only or localhost-bound units. `deploy_membrane.sh` updated: Nest units
generate `--socket` flags, skunkBat unit uses `--socket --no-tcp`, firewall
no longer opens standalone primal ports.

**UDS posture** (13/13 services active, 10/12 UDS health ALIVE):

| Primal | Transport | Socket | TCP | Status |
|--------|-----------|--------|-----|--------|
| beardog | UDS+TCP | `/run/membrane/beardog.sock` | 127.0.0.1:9100 (binary default) | ALIVE via UDS |
| songbird | UDS+TCP | `/run/membrane/songbird.sock` | :7700 (federation, correct) | ALIVE via UDS |
| biomeos | UDS | `/run/membrane/biomeos.sock` | — | ALIVE via UDS |
| barracuda | UDS | `/run/membrane/barracuda.sock` | — | ALIVE via UDS |
| coralreef | UDS | `/run/membrane/coralreef.sock` | 127.0.0.1:random | ALIVE via UDS |
| toadstool | UDS | `/run/membrane/toadstool.sock` | 127.0.0.1:random | ALIVE via UDS |
| nestgate | UDS+TCP | `/run/membrane/nestgate.sock` | 127.0.0.1:9500 | ALIVE via UDS |
| rhizocrypt | UDS | `/run/membrane/rhizocrypt.sock` | — | ALIVE via UDS |
| loamspine | UDS | `/run/membrane/loamspine.sock` | — | ALIVE via UDS |
| sweetgrass | UDS+HTTP | `/run/membrane/sweetgrass.sock` | 127.0.0.1:random (HTTP) | ALIVE via UDS |
| squirrel | UDS | `/run/membrane/squirrel.sock` | — | Socket connects, health silent |
| petaltongue | UDS | `/run/membrane/petaltongue.sock` | — | Socket connects, health silent |
| skunkbat | TCP-only | (no UDS in current binary) | 127.0.0.1:9140 | ALIVE via TCP |

**Socket path bridge**: `/run/membrane/*.sock` → symlinked to `/run/biomeos/*.sock`
and `/run/user/0/biomeos/*.sock` via `membrane-socket-bridge.service`.

**Firewall (ufw)**: Default deny incoming. Allows: SSH(22), DNS(53), HTTP/S(80/443),
Forgejo(2222), Songbird(3478/7700), TURN data(49152-65535/udp). Zero standalone
primal TCP ports exposed externally.

**Remaining for full UDS purity**:
- skunkBat binary needs rebuild with UDS support
- ~~sweetgrass `--http-address` defaults to `0.0.0.0:0`~~ **RESOLVED** — v0.7.51 defaults to `127.0.0.1:0`
- squirrel/petaltongue health probe framing investigation

### Track 5: Caddy Reverse Proxy Wiring — PARTIALLY LIVE ✓

| Endpoint | Backend | Status |
|----------|---------|--------|
| mesh.primal.eco | Songbird 157.230.3.183:7700 | **LIVE** (LE cert, reverse proxy) |
| auth.primal.eco | bearDog UDS | DNS+TLS live, backend 503 (cross-node proxy needed) |
| api.primal.eco | biomeOS UDS | DNS+TLS live, backend 503 (cross-node proxy needed) |
| nestgate.io /content/* | Forgejo localhost:3000 | DNS+TLS live, backend 200 placeholder (cross-node proxy needed) |

Cross-node proxy (golgiBody-ext → golgiBody inner) needed for UDS backends.
cellMembrane recommends socat forwarders in systemd units.

### Track 6: Lagging Codebase Parity (P2)

| Codebase | Gap | Action |
|----------|-----|--------|
| airSpring | Wave 60 → 78 (7d behind) | Trust pattern absorption, Wave 78 alignment |
| groundSpring | Wave 63 → 78 (6d behind) | Trust pattern absorption |
| songBird | 73% coverage (vs 90% target) | Coverage sprint — largest quantitative gap |
| hotSpring | Separate track, no root domain_profile.toml | Create root domain_profile.toml |
| ludoSpring | CONTEXT.md stale, no domain_profile.toml | Doc update + profile creation |
| neuralSpring | No domain_profile.toml | Profile creation |

### Track 7: Ongoing Evolution (P3)

| Work | Owner | Notes |
|------|-------|-------|
| biomeGate full NUCLEUS (9→13) | hotSpring + ops | PLANNED |
| northGate deployment planning | — | Heavy compute / AI |
| grapheneGate bootstrap | — | Portable trust anchor |
| Cloudflare → sovereign content cutover | cellMembrane | After Caddy wiring |

---

## Sovereignty Shadow Status

| Track | Status | Next Step |
|-------|--------|-----------|
| S1 TLS | **LIVE** (sovereign LE on primal.eco + nestgate.io) | Caddy reverse proxy wiring |
| S2 NAT | **GRADUATED** | Complete |
| S3 Content | READY (67ms TTFB, 101 tests) | Wire nestgate.io → Forgejo content |
| S4 Auth | 7-DAY GATE ACTIVE (started Jun 2, ends ~Jun 9) | Wait → graduate |

---

## Active FRAGOs

| FRAGO | From→To | Status |
|-------|---------|--------|
| `wave73-westgate-skunkbat-enrollment` | eastGate→westGate | **P1** — hardware + 10G backbone incoming (Jun 7-8) |
| `wave79-transport-evolution-capability-routing` | eastGate→all | **Phase 1 COMPLETE**, Phase 2 in progress |
| `wave79c-cross-node-proxy` | cellMembrane | **NEW** — socat forwarders for ext→inner UDS backends |

---

## Upstream Gap Summary — ALL RESOLVED

| Gap | Status |
|-----|--------|
| ~~SB-TLS-01~~ | **RESOLVED** — Songbird direct-mode TLS crypto |
| ~~SB-TLS-02~~ | **RESOLVED** — Phase 3.5 Ed25519 relay verification |
| ~~BD-TRUST-01~~ | **RESOLVED** — Songbird `ec978b86` wires `auth.exchange_trust` into `mesh.init`. Zero-operator cross-gate trust seeding. |
| ~~RC-POLL-01~~ | **RESOLVED** — rhizoCrypt MeshEventListener polling wired |

**Zero P0/P1 upstream gaps.** VPS binary refresh 10/13 complete. 3 headless regressions
handed off to cellMembrane. mesh.init ready once all 13 confirmed.

---

*"The fastest teams wait for the slowest. The glacier moves as one."*
