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

## Phase 1 — Wave 53: Primal Mountains

Close all remaining primal-level debt so the mountain is fully clean before
downstream pushes.

### Critical (blocks deployment)

| Item | Owner | Detail |
|------|-------|--------|
| SouthGate primal instability | Songbird + BearDog + biomeOS | 7/13 primals health-responding; Songbird crashes, stale socket issues. Investigate crash logs, stale socket cleanup, BearDog reconnect. Highest priority — blocks cross-gate mesh validation. |
| NestGate version unify | NestGate | Internal 4.7.0-dev vs plasmidBin 0.1.0. Align Cargo.toml workspace version. Coverage push 84% → 90%. |
| SkunkBat seed_fingerprint | SkunkBat / plasmidBin CI | Promoted without BLAKE3 manifest fingerprint. Auto-harvest CI should backfill; verify after next cycle. |

### Important (mountain hygiene)

| Item | Owner | Detail |
|------|-------|--------|
| Songbird coverage + BTSP stress | Songbird | 73.4% → 90% coverage target. BTSP multi-frame stress tests. Tor onion crypto blocked on external security provider (not forceable). |
| SourDough version drift | SourDough / plasmidBin | Local 0.3.1 vs manifest 0.3.0. Bump manifest after next harvest. |
| LoamSpine storage backends | LoamSpine | PostgreSQL/RocksDB not implemented (redb + memory only). Document as deferred; not a glacial-shift blocker. |

### Low priority (incremental)

- CoralReef: depth textures, array/cube maps, 90% coverage
- barraCuda: coverage expansion, spring absorption
- Cold-start latency (rhizoCrypt, sweetGrass, toadStool): 8s timeout workaround documented

---

## Phase 2 — Wave 54: Deployment + cellMembrane

Stabilize all gates and hand off deployment infrastructure to cellMembrane.

### Gate stabilization

| Item | Owner | Detail |
|------|-------|--------|
| SouthGate repair | plasmidBin + southGate operator | Fresh NUCLEUS: `plasmidbin fetch --all --force && plasmidbin launch`. Target: 13/13 primals, all sockets healthy. Verify Songbird mesh seeding to eastGate. |
| BiomeGate federation | biomeGate operator | Restart Songbird with `SONGBIRD_FEDERATION_PORT=7700` + `SONGBIRD_PEERS`. Verify federation with eastGate. Push from 6–9 to 13/13. |
| Live covalent mesh | primalSpring | Run `s_covalent_mesh` scenario against all 4 gates. Key cross-gate validation. |

### cellMembrane handoffs

| Item | Owner | Detail |
|------|-------|--------|
| 2nd CI runner on eastGate | cellMembrane | Eliminate ironGate runner SPOF. |
| VPS Nest expansion | cellMembrane | Deploy rhizoCrypt, loamSpine, sweetGrass, NestGate on VPS. Glacial blocker 1. |
| Sovereign DNS | cellMembrane | Deploy knot-dns on VPS (Channel 1). Glacial blocker 2. |
| K-Derm wire contract | cellMembrane → wateringHole | Publish `membrane.toml` schema, layer placement, `BoundaryPolicy` set. primalSpring consumes `cellmembrane-types`. |

### Cephalization + Tower CNS

| Item | Owner | Detail |
|------|-------|--------|
| Socket namespacing prototype | primalSpring + biomeOS | Phase A: beardog/ (5 domain sockets) and barracuda/ (5 domain sockets). Backward compat via symlinks. Validate Neural API routing. |
| BearDog TCP drop prototype | BearDog + primalSpring | BearDog UDS-only (no TCP 9900/9101) on test NUCLEUS. Verify crypto caps reachable via UDS. |

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

| Criterion | Current | Target |
|-----------|---------|--------|
| Shadow cutover S1–S4 | 3/4 | 4/4 (S1 TLS cut) |
| Multi-gate mesh validated | 4 gates up, mesh not validated | `s_covalent_mesh` PASS on 4 gates |
| VPS Nest expansion | NOT DEPLOYED | rhizoCrypt + loamSpine + sweetGrass live |
| Sovereign DNS | NOT DEPLOYED | knot-dns on VPS |
| CI on inner membrane | 1 runner (SPOF) | 2+ runners, Forgejo shadow |
| Cloudflare removed | S1 not cut | TLS via Caddy |
| All primals 90%+ coverage | 10/13 | 13/13 |
