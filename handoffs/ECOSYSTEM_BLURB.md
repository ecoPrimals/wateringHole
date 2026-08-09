# ecoPrimals Ecosystem Blurb — Wave 157a VERTEBRATE EVOLUTION COMPLETE

**Date**: Aug 9, 2026 10:00AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **VERTEBRATE EVOLUTION RESPONSE ABSORBED. 2 P0s REMAIN. DEPOT REBUILD IN PROGRESS.** 12 teams responded to the vertebrate blurb with self-audits, code fixes, and structural evolution. P0-B RESOLVED (nestGate `content.ingest` was shipped, stale depot was root cause). P0-A code-fixed (bearDog health guard `766951004`, socket rename). P0-C remains (biomeOS FD leak). songBird shipped `CanonicalTransport` trait. swarmVine 39→124 tests. petalTongue decoupled doom-core. All audited primals: zero phantom methods. **sporeGate rebuilding depot — gates must pull from golgi postPrimordial, not self-build.**

---

## CRITICAL: UNIFY TO postPrimordial DEPOT

**Pattern leading to divergence**: gates are self-building primals from source, resulting in each gate running different versions. westGate's P0-B was a stale binary problem, not a missing feature. ironGate reports nestgate+toadstool exit after startup (primal team binary issues).

**Correct pattern**: sporeGate is the sole depot builder. sporeGate rebuilds all primals → pushes to golgi → gates pull from golgi via `plasmid.fetch`. No gate builds its own primals. This blurb goes to sporeGate first — sporeGate rebuilds, then gates pull.

---

## VERTEBRATE EVOLUTION — TEAM RESPONSES (12 teams)

### P0 Resolution Status

| P0 | Status | Code Fix | Depot Binary |
|----|--------|----------|-------------|
| **P0-A: bearDog sign stub** | **CODE FIXED** | `766951004` — health socket guard, -32601 for non-health methods, socket rename `beardog-default→beardog-health` | **STALE** — depot rebuild needed |
| **P0-B: nestGate API surface** | **RESOLVED** | `content.ingest` shipped since S136 (590 LOC, 7 tests). `content.stat` shipped (`4cafa535`). Self-audit: zero phantom methods | **STALE** — depot rebuild needed |
| **P0-C: biomeOS FD leak** | **OPEN** | Not yet fixed in code | 14→58K FDs after 4 `capability.call` — forwarding unusable |

### Primal Self-Audits (all verified RPC surface vs capability_registry.toml)

| Primal | Self-Audit | Key Evolution | Tests |
|--------|-----------|---------------|-------|
| **songBird** | DONE | `CanonicalTransport` trait shipped (`33e9a8be`). 9 transports converging. `mesh.capabilities_announce` delegated to swarmVine. | 14,840+ |
| **swarmVine** | DONE | Deep audit, async dispatch, zero-copy. Unknown methods → -32601. | **39→124** (82% coverage) |
| **petalTongue** | DONE | doom-core decoupled (ludoSpring-ready). Dep prune. RPC self-audit. | 6,755+ |
| **bearDog** | DONE (P0-A) | Health guard: no more silent swallowing. Socket naming fixed. | 14,019+ |
| **nestGate** | DONE (P0-B) | `content.ingest` confirmed, `content.stat` shipped, registry synced. | 1,630+ |
| **skunkBat** | DONE | RPC surface verified, registry synced. | 675 |
| **rhizoCrypt** | DONE | 40/40 registry-handler parity. Fixed undeclared `dag.session.tree_hash` + phantom `lifecycle.status`. | 1,900 |
| **loamSpine** | DONE | 54/54 RPC verified. `persist_tip` abstraction (18-site pattern). −89 LOC. | 1,752 |
| **coralReef** | DONE | 18/18 RPC methods verified against registry. | 3,580 |
| **barraCuda** | DONE | Zero phantom APIs. 4,996 tests. | 4,996 |
| **cellMembrane** | DONE | `LimitNOFILE=65536` in systemd units. 5 dispatch commands wired. `capability_registry` 75→103. | 1,327+ |
| **sourDough** | DONE | `rpc-surface` audit tool shipped (`aa1a2f8`): detects P0-A stub + P0-B divergence live. | 518 |

### Gate Responses

| Gate | Action | Finding |
|------|--------|---------|
| **ironGate** | G68 redeploy 11/13 | nestgate+toadstool exit after startup (primal binary issues). `nucleus-deploy verify --audit-rpc` shipped. |
| **FOUNDATION** | Self-audit AAR | bearDog has real crypto (ironGate build from source). biomeOS stopped cleanly. Core sovereignty stack operational. |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** — 12/16 self-audited (zero phantom methods) |
| P0 | **1 code-open** (biomeOS FD). 2 code-fixed, depot-stale (bearDog, nestGate) |
| Self-audits | **12 complete**. Remaining: biomeOS (P0-C), toadStool (S371 in progress), sweetGrass, bingoCube |
| Depot | **sporeGate rebuilding** — all 16 primals. golgi push pending. |
| songBird | `CanonicalTransport` trait shipped — transport abstraction underway |
| swarmVine | 124 tests, 82% coverage, async dispatch, self-audit conformance |
| petalTongue | doom-core decoupled — ready for ludoSpring extraction |
| sourDough | `rpc-surface` audit tool — detects health stubs + API divergence live |

---

## DEPOT REBUILD — sporeGate ACTION REQUIRED

sporeGate must rebuild ALL primals from current HEAD to unify the fleet. Key binaries that changed:

| Primal | Key Commit | What Changed |
|--------|-----------|-------------|
| **bearDog** | `766951004` | P0-A fix: health guard, -32601 for non-health, socket rename |
| **nestGate** | `4cafa535`+ | P0-B: `content.stat` shipped. `content.ingest` already in code. |
| **songBird** | `33e9a8be` | `CanonicalTransport` trait + swarmVine delegation |
| **swarmVine** | `2cd4964` | Deep audit, 124 tests, async dispatch |
| **petalTongue** | `87a2530` | doom-core decoupled, dep prune, RPC self-audit |
| **skunkBat** | `1ad84c1` | RPC surface verified, registry synced |
| **sourDough** | `aa1a2f8` | `rpc-surface` audit tool |

After rebuild: regenerate BLAKE3SUMS, push to golgi. Gates pull from golgi — **no self-builds**.

---

## REMAINING

### P0 (1 code-open)
- **biomeOS P0-C**: FD leak in auto-discovery loop. `capability.call` unusable. Needs code fix.
- **bearDog P0-A**: Code fixed (`766951004`). Needs depot rebuild.
- **nestGate P0-B**: RESOLVED. Code shipped. Needs depot rebuild.

### Vertebrate evolution (continuing)
- **songBird**: `CanonicalTransport` trait shipped — impl for each transport crate ongoing
- **petalTongue**: doom-core decoupled — ludoSpring extraction when spring is scaffolded
- **toadStool**: S371 `core` 272K splitting (24/48 WASM). Self-audit pending.
- **sweetGrass**: Self-audit pending
- **bingoCube**: Self-audit pending
- **All**: sourDough `rpc-surface` audit tool available for automated verification

### Deployment discipline
- **sporeGate**: Rebuild all primals → golgi push → BLAKE3SUMS
- **All gates**: Pull from golgi postPrimordial. No self-builds.
- **P1: FD exhaustion**: `LimitNOFILE=65536` on remaining gates (strandGate, blueGate, southGate)

### Data + science
- **westGate**: Spine commits deferred until bearDog depot binary ships with signing
- **arXiv**: `validate.sh` + reviewer send. 41/42.
- **cellMembrane**: `native_braid.py` → Rust

---

*Wave 157a VERTEBRATE EVOLUTION COMPLETE. 12 teams self-audited — zero phantom methods across all audited primals. P0-A code-fixed (bearDog health guard 766951004). P0-B RESOLVED (nestGate content.ingest was shipped, stale depot). P0-C OPEN (biomeOS FD leak). songBird CanonicalTransport trait shipped. swarmVine 39→124 tests (82% coverage). petalTongue doom-core decoupled. sourDough rpc-surface audit tool shipped. sporeGate rebuilding depot — gates pull from golgi, no self-builds. 16 primals.*
