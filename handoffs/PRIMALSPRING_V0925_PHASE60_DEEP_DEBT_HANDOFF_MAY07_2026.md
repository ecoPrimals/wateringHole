# primalSpring v0.9.25 Phase 60 — Deep Debt Evolution + Sovereignty Closure

**Date**: May 7, 2026
**From**: primalSpring (eastGate)
**For**: All primal teams, springs, gardens, projectNUCLEUS

---

## Summary

primalSpring Phase 60 completed a 9-task deep debt evolution plan and absorbed
all 14 upstream sovereignty gap responses. The capability registry grew from
290 to 369 methods. Graph validator rewritten with spring-domain exclusion.
Zero primal drift. Ready for downstream handoff.

## Upstream Gap Status — ALL 14 RESOLVED

Thank you to all primal teams for the rapid response. Every gap we identified
in the projectNUCLEUS sovereignty audit has been closed:

| Primal | Gaps | Status |
|--------|------|--------|
| petalTongue | PT-1,3,4,5 | RESOLVED — `--docroot`, WebServeConfig, `--ipc`, `--workers` |
| NestGate | NG-1→NG-4 | RESOLVED — 8 `content.*` methods, manifests, blob visibility |
| biomeOS | RP-1→RP-5 | RESOLVED — 6 graphs realigned, standalone executor |
| LoamSpine | RP-2,3,5 | RESOLVED — spine lifecycle, hex strings, signing contract |
| BearDog | RP-1,5 | RESOLVED — crypto.sign contract, crypto.did_from_key |
| rhizoCrypt | PG-60 | RESOLVED — readiness gate (-32002) |
| toadStool | PG-62 | RESOLVED — health.liveness fast-path, timeout docs |
| barraCuda | PG-47/61, shaders | RESOLVED — stats.entropy live, 18/18 shader absorption |

## Remaining Upstream Debt (P2/P3 — no blockers)

| Priority | Item | Owner |
|----------|------|-------|
| ~~P2~~ | ~~PT-13: NestGate backend for petalTongue web mode~~ | **RESOLVED** (May 7, v1.6.6) |
| ~~P2~~ | ~~PT-09: BTSP Phase 2 enforcement~~ | **RESOLVED** (May 7, v1.6.6) |
| P3 | SD-02: sourDough musl cross-compilation | sourDough |
| P3 | SD-03: genomeBin signing (sequoia-openpgp) | sourDough |
| P3 | Squirrel E2E inference parity | Squirrel + neuralSpring |
| P3 | coralReef transitive libc (mio→rustix, upstream mio#1735) | coralReef |
| P3 | barraCuda 4 stateful API gaps (ESN, nautilus, ODE, SimpleMlp) | barraCuda |
| P3 | BearDog BondPersistence Result<_, String> | BearDog |

None of these block downstream evolution or NUCLEUS deployment.

## What We Learned (Composition Patterns)

1. **Graph method drift is systemic** — method names in graph TOMLs drift from
   primal dispatch tables silently. CI check (`check_graph_methods.sh`) would have
   caught all 3 RP-1 mismatches automatically. Recommendation: every primal with
   graph files should validate capability references against their local registry.

2. **Spring-domain vs primal-domain** — graph TOMLs reference both primal capabilities
   (real IPC methods) and spring-declared capabilities (aspirational/cell-local). These
   must be separated in validation. The `--strict` / spring-domain exclusion pattern works.

3. **Content-addressed storage unblocks atomic deploys** — NestGate's `content.put` +
   `content.publish` + `content.promote` pattern enables zero-downtime static site
   deployment. sporePrint and springs should adopt this for notebook/artifact publishing.

4. **RootPulse is now executable** — biomeOS v3.45 standalone executor + aligned graphs
   mean the provenance commit workflow can be tested end-to-end against live primals.
   Springs with provenance needs should compose via `biomeos graph execute`.

5. **Deep debt pays off** — modularizing large files, centralizing profiles, and
   generalizing caches reduced cognitive load and made the sovereignty absorption
   cycle much smoother. The 800L threshold and modern Rust idioms are working.

## Metrics

| Metric | Value |
|--------|-------|
| Version | 0.9.25 |
| Tests | 666 (618 passed + 48 ignored) |
| Clippy | 0 warnings |
| Registered methods | 369 |
| Source method strings | 208/208 validated |
| Graph refs | 353 checked, 0 primal drift |
| Experiments | 85 (19 tracks) |
| Deploy graphs | 74 TOMLs |

## Pull

- `primalSpring` main — registry, tools, handoffs, deep debt evolution
- `infra/wateringHole` — this handoff + all primal team handoffs
