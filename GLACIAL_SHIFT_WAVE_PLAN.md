# Glacial Shift Wave Plan — PostPrimordial to Sovereignty

**Status**: Active roadmap  
**Phase**: PostPrimordial (Wave 52b) → Glacial Shift  
**Last updated**: 2026-05-26  
**Owner**: primalSpring (coordination); cellMembrane (deployment); primal teams (mountains)

---

## Current Position

Interstadial exit achieved. 13/13 NUCLEUS primals shipped via plasmidBin with
checksums. eastGate is the reference deployment (13/13, 19/19 sockets, doctor
35/35 pass). 4 gates operational (eastGate, ironGate, southGate, biomeGate)
with varying completeness. 8/8 springs at zero code debt, primordial patterns
extinct, covalent HPC confirmed.

Three phases below are ordered by dependency: mountains feed deployment,
deployment feeds springs, springs feed cross-gate interaction.

---

## Phase 1 — Wave 53: Primal Mountains (RESOLVED)

### Resolution status (reviewed May 26, 2026)

| Item | Status | Detail |
|------|--------|--------|
| Songbird stale socket cleanup | **DONE** | `unlink()` before `bind()` hardened at 2 bind sites (connection.rs, unix_listener.rs). Ignores `NotFound`. |
| Songbird BTSP stress tests | **DONE** | 3 new tests: 100-request sequential, varying payload (1B–4KB), 10-client concurrent sessions. |
| Songbird coverage 73→90% | **OPEN** | Still at 73.41%. I/O-heavy + integration paths remain. Not blocking deployment. |
| Songbird Tor onion | **DEFERRED** | Reclassified from BLOCKED to DEFERRED. Not a glacial-shift blocker. |
| BearDog TCP opt-in | **DONE** | TCP now opt-in only (`--port`/`--listen`/`BEARDOG_TCP_IPC_PORT`). UDS-only by default. All 127 methods available via UDS. |
| SkunkBat seed_fingerprint | **DONE** | BLAKE3 fingerprint backfilled in plasmidBin manifest.toml. |
| SourDough manifest drift | **DONE** | plasmidBin manifest bumped 0.3.0→0.3.1. |
| LoamSpine storage backends | **DONE** | Documented as roadmap (not blocker) in WHATS_NEXT.md. Wave 53 ack filed. Zero mountain debt. |
| CoralReef depth/array/cube | **DONE** | Depth texture comparison PTX, array/cube sampling, vector math. +18 tests (3,220 total). |
| BarraCuda coverage | **DONE** | +24 handler-level tests (4,501+ total). All IPC handler gaps closed. |
| ToadStool ipc.register | **DONE** | Aligned from stale 2-cap set to full 9-cap Node Atomic set. S276 deep debt evolution: zero production panics, sovereign split, memmap2→rustix. |
| NestGate version unify | **DONE** | Unified to 0.5.0 across all 21 workspace crates + plasmidBin manifest (Session 77). Coverage 83.61% (Session 78); 90% target ongoing. |
| SouthGate crash investigation | **OPEN** | Ops/deployment follow-up — Songbird socket hardening shipped but southGate redeploy not yet done. |

### Summary

12/13 Wave 53 items resolved. 1 remaining item (SouthGate ops redeploy) carries into
Wave 54. NestGate unified to v0.5.0 (Session 77). Songbird coverage (73→90%) is
incremental, not blocking. All mountain code debt is clear — remaining work is
ops/deployment.

---

## Phase 2 — Wave 54: Deployment + cellMembrane

Stabilize all gates and hand off deployment infrastructure to cellMembrane.

Wave 53 resolved most mountain code debt. Wave 54 focuses on ops/deployment
and the glacial shift infrastructure blockers.

### Primal prep (DONE — Wave 53 + 54-prep)

| Item | Status | Detail |
|------|--------|--------|
| BearDog TCP opt-in | **DONE** | UDS-only by default. TCP requires `--port`/`BEARDOG_TCP_IPC_PORT`. All 127 methods via UDS validated. |
| Songbird socket hardening | **DONE** | `unlink()` before `bind()` at all sites. BTSP 3-test stress suite. |
| ToadStool ipc.register | **DONE** | 9-cap Node Atomic set. S276 deep debt: zero panics, sovereign split. |
| BarraCuda coverage | **DONE** | +24 handler tests, all IPC gaps closed. |
| CoralReef ptx_emit | **DONE** | Depth textures, array/cube, vector math. 3,220 tests. |
| LoamSpine ack | **DONE** | Zero mountain debt. PostgreSQL/RocksDB documented as roadmap. |
| primalSpring scenarios | **DONE** | 3 new: `s_cephalization`, `s_tower_cns`, `s_kderm_boundary`. 56 total. |

### Gate stabilization

| Item | Owner | Detail |
|------|-------|--------|
| SouthGate redeploy | plasmidBin + southGate operator | Fresh NUCLEUS with Songbird socket hardening: `plasmidbin fetch --all --force && plasmidbin launch`. Target: 13/13 primals. Songbird socket cleanup is now hardened (Wave 53). Verify `SONGBIRD_PEERS=192.168.1.144:7700`. |
| BiomeGate federation | biomeGate operator | Restart Songbird with `SONGBIRD_FEDERATION_PORT=7700` + `SONGBIRD_PEERS`. Push to 13/13. |
| Live covalent mesh | primalSpring | Run `s_covalent_mesh` against all 4 gates after redeploy. |
| NestGate version unify | NestGate team | **DONE** — v0.5.0 across 21 workspace crates (Session 77). Coverage at 83.61%, pushing toward 90%. Ready for VPS deploy. |

### cellMembrane handoffs

| Item | Owner | Detail |
|------|-------|--------|
| 2nd CI runner on eastGate | cellMembrane | Eliminate ironGate runner SPOF. |
| VPS Nest expansion | cellMembrane | Deploy rhizoCrypt, loamSpine, sweetGrass, NestGate on VPS. Glacial blocker 1. loamSpine confirmed mountain-clean (90.92% coverage, 1,528 tests). |
| Sovereign DNS | cellMembrane | Deploy knot-dns on VPS (Channel 1). Glacial blocker 2. |
| K-Derm wire contract | cellMembrane → wateringHole | Publish `membrane.toml` schema, layer placement, `BoundaryPolicy` set. primalSpring `s_kderm_boundary` scenario ready to consume. |

### Cephalization + Tower CNS (primalSpring-validated)

| Item | Owner | Status | Detail |
|------|-------|--------|--------|
| BearDog TCP drop | BearDog + primalSpring | **VALIDATED** | BearDog UDS-only running on eastGate (nucleus01, no `--port`). All 5 domain sockets confirmed. primalSpring `s_tower_cns` scenario passes. |
| Socket namespacing | primalSpring + biomeOS | **SCENARIO READY** | `s_cephalization` scenario validates ownership map, orphan detection. Phase A (beardog/5 + barracuda/5) ready for live prototype after gate stabilization. |
| K-Derm boundary | primalSpring | **SCENARIO READY** | `s_kderm_boundary` validates all 13 primals placed in K-Derm layers. Zero boundary violations. Pending cellMembrane `membrane.toml` for channel protein integration. |

---

## Phase 3 — Wave 55+: Springs Launch + Cross-Gate NUCLEUS

Mountains clean, gates stable — springs connect and interact across the mesh.

### Spring proto-nucleate deployment

All 7 delta springs deploy `proto_nucleate_template.toml` on their assigned gates:

| Gate | Springs | Status |
|------|---------|--------|
| eastGate | airSpring, groundSpring | Already operational |
| ironGate | ludoSpring, healthSpring | Already operational |
| southGate | wetSpring, neuralSpring | Pending gate stabilization |
| biomeGate | hotSpring | Pending federation fix |

### Cross-gate capability routing

| Item | Owner | Detail |
|------|-------|--------|
| capability.call smoke tests | primalSpring | From each gate, call capabilities on every other gate via Songbird braid relay. |
| Provenance trio roundtrips | wetSpring | PG-02 (provenance trio live) and PG-04 (NestGate storage) verification. |
| Ionic cross-family GPU lease | hotSpring + BearDog | GAP-HS-005: `crypto.sign_contract` for cross-family GPU scheduling. |

### Membrane interaction

| Item | Owner | Detail |
|------|-------|--------|
| Channel proteins live | cellMembrane | K-Derm channels (TLS, NAT, content, auth) as formal NUCLEUS boundary. |
| S1 TLS shadow cutover | cellMembrane | Cloudflare → sovereign TLS via Caddy. Key sovereignty milestone. |
| Forgejo Actions | cellMembrane | Deploy Forgejo on ironGate as shadow CI, then invert (Forgejo-primary). |

### Per-spring next steps

| Spring | Key next step |
|--------|--------------|
| wetSpring | PG-02/PG-04 live verification on stable southGate |
| neuralSpring | Resolve loamSpine Tokio double-runtime crash; Squirrel provider registration |
| hotSpring | BiomeGate federation fix; ionic GPU lease prototype |
| healthSpring | BTSP `btsp.capabilities` probe pattern (avoid unconditional negotiation) |
| ludoSpring | 6 game.* methods for esotericWebb; notebook gap |
| groundSpring | Squirrel composition integration (additive) |
| airSpring | AG-006 coralReef compile, AG-009 petalTongue direct IPC |

---

## Glacial Shift Exit Criteria

| Criterion | Current (post-Wave 53) | Target |
|-----------|----------------------|--------|
| Shadow cutover S1–S4 | 3/4 | 4/4 (S1 TLS cut) |
| Mountain code debt | **12/13 resolved** (SouthGate ops redeploy remains) | 13/13 |
| Multi-gate mesh validated | 4 gates up, mesh not validated | `s_covalent_mesh` PASS on 4 gates |
| VPS Nest expansion | NOT DEPLOYED | rhizoCrypt + loamSpine + sweetGrass live |
| Sovereign DNS | NOT DEPLOYED | knot-dns on VPS |
| CI on inner membrane | 1 runner (SPOF) | 2+ runners, Forgejo shadow |
| Cloudflare removed | S1 not cut | TLS via Caddy |
| Primals 90%+ coverage | ~10/13 (songbird 73%, coralReef/barraCuda incremental) | 13/13 |
| BearDog TCP drop | **VALIDATED** — UDS-only on eastGate | All gates UDS-only |
| K-Derm boundary scenarios | **3 scenarios PASS** (56 total) | + channel protein live validation |
| primalSpring lib tests | **787/799** (10 live-tier) | All pass with full graph deploy |
