# projectNUCLEUS Trio: Deep Debt Evolution Sweep — Completion Handoff

**Date**: 2026-05-11
**From**: projectNUCLEUS (sporeGarden) — owns projectNUCLEUS, foundation, lithoSpore
**For**: All primal teams, spring teams, primalSpring, biomeOS
**Phase**: Post-interstadial — deep debt evolution sweep COMPLETE across all three owned products

---

## Summary

The deep debt evolution sweep across all three projectNUCLEUS-owned products is complete.
Structural debt resolved, Rust modernized, hardcoding eliminated, stubs evolved to
implementations, and the validation pipeline advanced from Tier 1 Python to Tier 2 Rust.

---

## What Changed — Per Product

### foundation (scientific knowledge layer)

- **THREAD_INDEX.toml** hygiene: 4 threads with wrong/empty paths corrected (v1.3.0)
- **7 workload TOMLs** gate-agnostic: replaced hardcoded `/home/{user}` with `${GROUNDSPRING_ROOT}`, `${FOUNDATION_ROOT}`
- **fetch_sources.sh** evolved: now covers all 10 threads, refactored to TOML-manifest-driven dispatch via `python3 -c "import tomllib"`
- **foundation_validate.sh** evolved: fixed phase numbering, added Phase 6 (target comparison against `data/targets/*.toml`), fixed bare `except:`, corrected path heuristics
- **Data coverage**: 10/10 threads seeded with source + target TOMLs, 150+ sources, 165+ targets

### projectNUCLEUS (sovereignty infrastructure)

- **Hardcoded path scrub**: Zero `/home/irongate` or `/home/eastgate` in deploy scripts or Python. Dynamic `pwd`-based resolution via `user_home()` helper
- **deploy.sh modularized**: per-primal start logic extracted to `deploy_primal_start.sh`, health checks to `deploy_health_check.sh`. Main script orchestrates via sourced functions
- **darkforest refactored**: `pentest.rs` (496L) → 3 submodules (external/compute/readonly). `crypto.rs` (489L) → 3 submodules (filesystem/keys/protocol). Total: 6 new focused modules from 2 monoliths
- **tunnelKeeper optimized**: 9 of 11 `.clone()` calls eliminated — 4 via `as_str()` helper, 3 via `serde_json::to_value`, 2 via `as_deref()`. Remaining 2 structurally required
- **Stale references fixed**: MethodGate 13/13 reconciled everywhere (SECURITY_VALIDATION.md, COMPLETE_DEPENDENCY_INVENTORY.md, tier_enforcement_test.sh), darkforest version aligned to v0.2.1, `publish_sporeprint.sh` status updated from STUB to READY
- **systemd templates** gate-agnostic: `gate.env.template` uses dynamic `$(whoami)` fallback

### lithoSpore (first Targeted GuideStone)

- **Tier 2 Rust validation WIRED** for modules 1+2:
  - Module 1 (fitness): Nelder-Mead simplex optimizer for nonlinear least squares, power-law/hyperbolic/logarithmic model fitting, AIC/BIC model selection — pure Rust, no external deps
  - Module 2 (mutations): Kimura fixation probability, xorshift64 PRNG with Knuth Poisson, Pearson correlation for molecular clock linearity — pure Rust, no external deps
- **`cmd_refresh`** evolved from `println!("TODO")` to real data.toml-driven fetch pipeline: parses `[[dataset]]` entries, executes `refresh_command` scripts, reports results
- **9 `expect()` calls** replaced with `match`-based error handling across all 8 module crates
- **liveSpore.json** wired: `ltee-cli validate` now appends a `LiveSporeEntry` after each run. First entry seeded (Tier 2 milestone)
- **Upstream deps status**: groundSpring B1+B2 COMPLETE (Wiser 2013 + Barrick 2009), feeding modules 1+2. Modules 3–7 awaiting spring reproductions

---

## Debt Resolution Summary

| Category | Before Sweep | After Sweep |
|----------|-------------|-------------|
| Hardcoded paths | ~30+ locations across 3 repos | **Zero** — gate-agnostic throughout |
| Stubs in production | 5 lithoSpore crates always SKIP + `cmd_refresh` stub | **2 modules PASS** at Tier 1+2, refresh implemented |
| Large monolithic files | 4 Rust (300-496L), 2 shell (~600L) | **Modularized** — pentest/crypto split, deploy.sh extracted |
| `expect()` / `unwrap()` | 9 `expect()` calls | **Zero** — all match-based |
| `.clone()` debt | 11 in tunnelKeeper | **2 remaining** (structurally required) |
| THREAD_INDEX mismatches | 4 threads with wrong paths | **Zero** — all 10 threads correct |
| fetch_sources.sh coverage | 4/10 threads | **10/10 threads** |
| Stale MethodGate refs | Mixed 9/10/11/12/13 across docs | **13/13 everywhere** |

---

## What This Means for Teams

### For primal teams
- All docs now accurately reflect 13/13 MethodGate enforcement
- NestGate `content.*` pipeline is marked READY (not STUB) — integrate accordingly
- darkforest pentest/crypto modules are now individually importable for team-specific security validation

### For spring teams
- foundation `fetch_sources.sh` now covers all 10 threads — spring data contributions auto-integrate
- lithoSpore Tier 2 demonstrates pure-Rust validation without scipy/numpy — pattern for spring Rust ports
- groundSpring B1+B2 reproductions successfully consumed by lithoSpore — cross-spring provenance chain validated

### For biomeOS / primalSpring
- `deploy_primal_start.sh` and `deploy_health_check.sh` are now independent, sourceable scripts — can be consumed by graph-driven germination tooling
- `composition.deploy(graph)` wired and tested; nohup loop still active for backwards compat but graph-based path is primary

---

## Ownership Status

```
NOW: projectNUCLEUS owns all three products
│
│ foundation thread work is independent of gate ops
▼
NEXT: foundation gains own team
│  criteria: fetch pipeline working (DONE), 10/10 threads (DONE),
│            Thread 1 WCM through NUCLEUS deploy graph
│
│ lithoSpore module science is independent of gate ops
▼
THEN: lithoSpore gains own team
   criteria: 2+ modules Tier 1 PASS (DONE), data fetched,
             Rust Tier 2 path started for at least 1 module (DONE)
```

Both foundation and lithoSpore have met their technical separation criteria.
Separation timing is a team capacity decision, not a technical blocker.

---

## Key References

- projectNUCLEUS deep debt sweep plan: `.cursor/plans/deep_debt_evolution_sweep_b66726da.plan.md`
- foundation THREAD_INDEX: `foundation/lineage/THREAD_INDEX.toml` (v1.3.0)
- lithoSpore liveSpore: `lithoSpore/artifact/liveSpore.json` (first entry)
- darkforest submodules: `projectNUCLEUS/validation/darkforest/src/{pentest,crypto}/`
- deploy modularity: `projectNUCLEUS/deploy/{deploy_primal_start,deploy_health_check}.sh`
