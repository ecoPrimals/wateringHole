# Wave 59 Mountain Blurb — Upstream Primals

**Date:** May 28, 2026
**From:** primalSpring coordination
**To:** All 13 primal teams (upstream mountain)

---

## State of the Mountain

Code debt is eliminated. Documentation is aligned. Glacial review complete.

primalSpring Wave 58b shipped: dispatch telemetry persistence (Layer 4/5
training data), PermissiveVerifier rename, blake3 correctness fix, primal
name constants, zero `#[allow]` anywhere. 21 docs refreshed to canonical
metrics. Sovereignty and niche climate docs corrected for false readiness
signals. 11 wateringHole handoffs archived. SSOT is clean.

**Glacial gate assessment**: software ~90%; operational ~35-40%. The gap
is deployment operations, not code. Your mountain is ready.

---

## Env Centralization — Final Status

| Tier | Primals | Status |
|------|---------|--------|
| Done (primalSpring pushed) | sourDough, sweetGrass, skunkBat, rhizoCrypt, loamSpine, petalTongue, coralReef, barraCuda | **188 constants / 96 files** |
| Done (team-owned) | bearDog (290), songbird (48), biomeOS (90+) | **RESOLVED** |
| In progress | squirrel (316 constants; ~93 files raw remaining) | SDK config layer next |
| Pending | toadStool (~200 sites) | `env_overrides.rs` split needed |

**11 of 13 primals have fully centralized env vars.**

---

## Remaining Per-Primal Work

### biomeOS — **P0 CRITICAL PATH**
- NC-1 **CODE COMPLETE** (v3.84). **Deploy to VPS** — unblocks all spring emissions.

### squirrel — Tier 2 (in progress)
- 316 constants built. ~93 files still have raw `std::env::var`. SDK config layer next.

### toadStool — Tier 2 (pending)
- ~200 env sites. `env_overrides.rs` split needed. ~17 `#[allow(clippy::` fixes.

### bearDog
- Env debt RESOLVED. Residual: `PRIMAL_CONTRACTS` method catalog stale.
- NC-3.5: `auth.issue_session` scope for sporePrint.

### lithoSpore
- NC-5 UNBLOCKED. Prepare for first live emission after 2 springs pass column U.

---

## Niche Climate (corrected — false readiness signals retired)

```
NC-1  postPrimordial Spore Gateway    CODE COMPLETE    Deploy v3.84 → column U
NC-2  Multi-Gate NUCLEUS Mesh          IN PROGRESS      southGate 7/13, biomeGate 9/13
NC-3  cellMembrane Sovereignty         CODE CONSUMED    Cutovers open: DNS NS, Forgejo, CI
NC-4  Spring NUCLEUS Depth             ADVANCING        east/iron OK, south/biome partial
NC-5  lithoSpore postPrimordial        UNBLOCKED        Gated on VPS + 2 column U passes
```

---

## Sovereignty Reality Check

| Layer | Status |
|-------|--------|
| S1 TLS | bearDog ACME live; Cloudflare/Caddy still in data path |
| S2 DNS | knot-dns **deployed** on VPS (DNSSEC); NS registrar cutover **pending** |
| S4 Git | Forgejo primary; **CI still GitHub Actions** |
| S5 Binary | plasmidBin provenance-elevated; **Forgejo releases pending** |

**~76% declared sovereignty; ~50% production cutover.**

---

## Critical Path to Stadial

```
P0  Deploy biomeOS v3.84 to VPS     → cellMembrane + ops
P1  hotSpring + groundSpring col U   → first 2 live emissions
P2  southGate 13/13, biomeGate 13/13 → gate stabilization
P3  NS cutover, Forgejo releases     → sovereignty (progressive)
P4  squirrel + toadStool env debt    → non-blocking
```

**Stadial entry**: P0 → P1 → P2 → candidate.

---

*Wave 59. Mountain clean. Docs clean. Deploy the ecosystem.*
