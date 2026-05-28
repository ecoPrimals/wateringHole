# Wave 58 — Remaining Work to Stadial Entry

**Date:** May 28, 2026
**From:** primalSpring coordination
**To:** All teams

---

## Ecosystem State

The mountain is clean. 8 of 12 non-biomeOS primals have centralized env vars
(pushed this wave). Downstream has converged: cellMembrane at 95.8% coverage
with typed errors, projectNUCLEUS at 166 tests with async-correct discovery.
NC-1 is COMPLETE (all code). The remaining path is live deployment.

---

## What's Done (no further action needed)

| Item | Owner | Wave |
|------|-------|------|
| NC-1 code: `biomeos-pseudospore` + emit materialization | biomeOS | 57 |
| VPS deployment standard: `--uds-only`, TransportMode, spring overlays | cellMembrane | 56 |
| Deploy scripts: all 13 primal `--uds-only` + socket health | projectNUCLEUS | 58 |
| Graph-driven health checks, env bootstrap | projectFOUNDATION | 56b |
| lithoSpore `--from-dir` emission path | lithoSpore | 56 |
| Env var centralization (8 primals) | primalSpring coord | 57b |
| primalSpring local debt: zero | primalSpring | 57 |
| Port SSOT reconciliation | cellMembrane + primalSpring | 56 |
| Wire-native newline JSON-RPC discovery | projectNUCLEUS | 58 |

---

## What Remains — Ordered by Critical Path

### P0: Live Deployment (blocks everything)

| Action | Owner | Blocker |
|--------|-------|---------|
| Deploy biomeOS v3.81 to VPS via plasmidBin | cellMembrane + ops | None |
| Test `biomeos deploy graphs/cells/hotspring_cell.toml` on VPS | cellMembrane + hotSpring | biomeOS v3.81 on VPS |

### P1: First Spring Emissions (blocks NC-5 + stadial)

| Action | Owner | Blocker |
|--------|-------|---------|
| hotSpring column U pass (first emission) | hotSpring + biomeOS | P0 |
| groundSpring column U pass (second emission) | groundSpring + biomeOS | P0 |

### P2: Gate Stabilization (blocks stadial NC-2/NC-4)

| Action | Owner | Blocker |
|--------|-------|---------|
| southGate 13/13 health (currently 7/13) | wetSpring/neuralSpring ops | Songbird peers config |
| biomeGate 13/13 primals (currently 9/13) | hotSpring ops | Primal binaries |

### P3: Sovereignty Completion (progressive, not blocking)

| Action | Owner | Blocker |
|--------|-------|---------|
| NS registrar cutover (NC-3.3) | cellMembrane + registrar | External |
| Forgejo releases (NC-3.4) | cellMembrane + plasmidBin | Forgejo config |
| sporePrint living content (NC-3.5) | cellMembrane + petalTongue | BearDog `auth.issue_session` scope |

### P4: Remaining Primal Env Debt (not blocking, team work)

| Primal | Env sites | Difficulty | Notes |
|--------|-----------|------------|-------|
| bearDog | ~550 / 130 files | High | `zero_hardcoding.rs` philosophy needs enforcement |
| songbird | ~70 / 35 files | Medium | `songbird-process-env` crate needs full adoption |
| squirrel | ~250 / 90 files | High | SDK `infrastructure/config.rs` sprawl |
| toadStool | ~200 / 95 files | High | `env_overrides.rs` split + VFIO domain work |

### P4b: Remaining Primal Clippy Debt

| Primal | `#[allow(clippy::` | Notes |
|--------|--------------------|-------|
| songbird | ~180 (test modules) | Batch `expect` migration |
| toadStool | ~17 | VFIO pipeline + `unused_async` |
| squirrel | 3 | Quick fix |

---

## projectNUCLEUS: NC-1 Status Correction

projectNUCLEUS handoffs still show NC-1 as **WIRED**. Correct status:

```
NC-1 → COMPLETE (biomeOS v3.81, May 27, 2026)
```

biomeOS shipped `biomeos-pseudospore` crate with `load_pseudospore`,
`verify_checksums`, `check_completeness` + full emit materialization
(scope.toml, validation.json, checksums.blake3, ferment_transcript.json,
data/, README). Please update local tracking.

---

## Stadial Entry Criteria

```
NC-1: 2+ springs pass column U        → GATED on P0/P1
NC-2: 3+ gates meshed                  → GATED on P2
NC-4: all 4 named gates healthy        → GATED on P2
NC-3: partial satisfaction sufficient   → ADVANCING
NC-5: progressive after NC-1 live      → UNBLOCKED
```

**Estimated timeline**: P0 (deploy v3.81) → P1 (2 emissions) → stadial candidate.

---

*Wave 58. All code delivered. Deploy and emit.*
