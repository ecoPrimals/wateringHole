# Wave 53 — Primal Mountain Teams Handoff

**Date**: 2026-05-26  
**From**: primalSpring (coordination)  
**To**: All primal teams  
**Context**: PostPrimordial complete. Full NUCLEUS live on eastGate (13/13, 19/19
sockets, plasmidbin doctor 35/35). Glacial shift wave plan published to
`wateringHole/GLACIAL_SHIFT_WAVE_PLAN.md`.

---

## Status: All 13 primals SHIPPED via plasmidBin

All mountains are clean. Zero debt markers ecosystem-wide. This handoff
requests targeted work to close the last gaps before we push to deployment
and springs.

---

## Per-Primal Action Items

### Songbird (CRITICAL)

SouthGate is reporting only 7/13 primals health-responding. Songbird crashes
are the primary suspect.

- **Investigate crash logs** on southGate — what's causing Songbird process exits?
- **Stale socket cleanup** — verify `unlink()` before `bind()` is working on restart
- **Coverage push**: 73.4% → 90% target (achievable with existing test infra)
- **BTSP multi-frame stress tests** — validate under sustained load
- Tor onion crypto: blocked on external security provider — document as deferred

### NestGate (CRITICAL)

- **Version unification**: internal 4.7.0-dev vs plasmidBin 0.1.0. Align
  `Cargo.toml` workspace version with what plasmidBin ships.
- **Coverage push**: 84% → 90% target

### SkunkBat (IMPORTANT)

- **seed_fingerprint missing** in plasmidBin manifest — v0.2.0 was promoted
  without BLAKE3 fingerprint. Verify this backfills on the next auto-harvest
  cycle. If not, manually run `plasmidbin harvest --version-tag v0.2.0` to
  populate it.

### BearDog (IMPORTANT — prep for Wave 54)

- **TCP drop prototype**: prepare BearDog to run UDS-only (no TCP 9900/9101).
  All crypto capabilities should remain reachable via domain sockets.
  This is prep for the Tower CNS convergence (exp114).
- **SouthGate**: verify BearDog socket health on southGate during the
  stability investigation.

### SourDough (LOW)

- **Version drift**: local shows 0.3.1, plasmidBin manifest still 0.3.0.
  Bump manifest after next harvest cycle.

### LoamSpine (LOW — document only)

- **Storage backends**: PostgreSQL/RocksDB are roadmap items, not glacial
  blockers. Document current state (redb + memory) in `WHATS_NEXT.md`.

### CoralReef, barraCuda (INCREMENTAL)

- Depth textures, array/cube maps, coverage expansion — not blocking.
  Continue incremental work.

### All Others (biomeOS, Squirrel, petalTongue, rhizoCrypt, sweetGrass, toadStool)

- **No action items.** Mountains are clean. Continue normal evolution.

---

## Timeline

Wave 53 work should be completable within the current sprint. SouthGate
stability is the gate for Wave 54 (deployment + cellMembrane).

Respond to this handoff with a brief status ack to `wateringHole/handoffs/`.
