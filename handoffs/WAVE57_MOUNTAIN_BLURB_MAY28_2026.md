# Wave 57 Mountain Blurb — Upstream Primals

**Date:** May 28, 2026
**From:** primalSpring coordination
**To:** All 13 primal teams (upstream mountain)

---

## State of the Mountain

primalSpring is clean. Wave 57 completed the final local debt sweep: main.rs
split into 3 focused modules, all env vars centralized, zero production
unwraps/unsafe/todo, zero clippy suppressions without reason, all doctests fixed.
797 lib tests, 56 scenarios, zero clippy warnings.

Downstream has fully converged: cellMembrane shipped the typed VPS standard
(`TransportMode`), projectNUCLEUS has `--uds-only` deploy for all 13 primals,
projectFOUNDATION has graph-driven health. **The ecosystem is aligned.**

**NC-1 is COMPLETE.** biomeOS v3.81 delivered `biomeos-pseudospore` + full emit
materialization. The remaining path is live deployment and spring emissions.

---

## Per-Primal Action Items

### biomeOS — **CRITICAL PATH**
- NC-1 COMPLETE code-side. **Action: deploy v3.81 to cellMembrane VPS via plasmidBin**
- Once live: hotSpring column U pass becomes unblocked (first spring emission)
- `biomeos deploy graphs/cells/hotspring_cell.toml` — test on live VPS
- `FAMILY_ID` discovery via JSON-RPC confirmed by projectFOUNDATION (used in `env.sh`)

### bearDog
- NC-3.5 sporePrint living content is **BLOCKED** on `auth.issue_session` scope expansion
- **Action**: scope expansion to unblock cellMembrane sporePrint integration
- Wave 56 orphan modules deleted + ionic bond refactor absorbed — clean

### songbird
- GAP-17/18 **partially resolved** — capability socket constants centralized, `ipc.resolve` migration path available
- **Action**: complete `ipc.resolve` migration for full capability socket resolution
- southGate 7/13 health likely `SONGBIRD_PEERS` env or cold-start timing — not a code bug

### lithoSpore
- NC-5 **UNBLOCKED** — NC-1.4 resolved, `--from-dir` emission path shipped
- **Action**: prepare for first live lithoSpore postPrimordial emission once 2 springs pass column U
- 7/7 tier-0 in CI, parity workflow active

### skunkBat, rhizoCrypt, loamSpine, sweetGrass, coralReef, barraCuda
- No blocking action items
- Port SSOT fully reconciled across all repos (verified cellMembrane `ports.env` ↔ primalSpring `tolerances/mod.rs`)
- VPS deploys will use UDS-only — zero TCP ports in production

### squirrel
- No blocking items. Meta-tier UDS deployment ready.

### toadStool
- No blocking items. Node-tier UDS deployment ready.
- `TOADSTOOL_AUTH_MODE` env var resolved in prior wave

### petalTongue / sourDough
- No blocking items. plasmidBin harvests current (May 28).

---

## Canonical Health Method

**`health.liveness`** is the canonical health method across all primals.
primalSpring also aliases `health.check`. Certification Layer 2 uses
`health.liveness`. projectFOUNDATION's `foundation_validation.toml` uses
`health.liveness` for all nodes. **All primals should respond to
`health.liveness`.**

---

## Niche Climate Summary

```
NC-1  postPrimordial Spore Gateway    COMPLETE     Deploy v3.81 → first emission
NC-2  Multi-Gate NUCLEUS Mesh          IN PROGRESS  Songbird GAP-17/18 partial
NC-3  cellMembrane Sovereignty         CONSUMED     VPS standard absorbed
NC-4  Spring NUCLEUS Depth             ADVANCING    --uds-only across all deploy tooling
NC-5  lithoSpore postPrimordial        UNBLOCKED    Waiting on 2 spring emissions
```

**Critical path**: biomeOS v3.81 on VPS → hotSpring column U → groundSpring column U → NC-5 → stadial.

---

*Wave 57. Mountain clean. Ecosystem converged. Deploy the primals.*
