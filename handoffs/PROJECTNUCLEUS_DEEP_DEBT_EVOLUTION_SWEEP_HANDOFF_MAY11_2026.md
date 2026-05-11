# projectNUCLEUS: Deep Debt Evolution Sweep + NestGate Priority Handoff

**Date**: 2026-05-11
**From**: projectNUCLEUS (sporeGarden)
**For**: All primal teams, all spring teams, primalSpring, biomeOS
**Phase**: Post-interstadial — deep debt evolution sweep complete, NestGate pipeline is the critical next target

---

## Summary

projectNUCLEUS has completed its deep debt evolution sweep. The codebase
is structurally clean: zero hardcoded paths, modular Python, gate-agnostic
systemd, reconciled specs, and upstream handbacks delivered. The structural
debt is resolved. **The next evolution target is the data/compute chain** —
which requires NestGate content pipeline as a prerequisite.

This handoff documents what was done, what was learned, and what each team
should prioritize for the next round of evolution.

---

## 1. What Was Done (Deep Debt Evolution Sweep)

### Code Quality

| Item | Before | After |
|------|--------|-------|
| pappusCast.py | 953-line monolith (5 responsibilities) | 7 modules: config, state, tiers, publisher, export, daemon + thin CLI (146L) |
| Hardcoded paths in Rust | 13 `/home/irongate` in pentest.rs + crypto.rs | Zero — `gate_home()` env-var pattern (`$GATE_HOME` with `$HOME` fallback) |
| Systemd units | 4 units with literal `/home/irongate` | `EnvironmentFile=/etc/projectnucleus/gate.env` + `${GATE_HOME}` |
| Python exception handling | Broad `except Exception` in 3 files | Narrowed to `subprocess.SubprocessError`, `json.JSONDecodeError`, `OSError` |
| Superseded tier test | `tier_test_observer.py` (314L) in active tree | Archived to `validation/archive/legacy/` (replaced by darkforest) |

### Spec Reconciliation

| Document | Drift | Fix |
|----------|-------|-----|
| `COMPLETE_DEPENDENCY_INVENTORY.md` | Cluster 7 "~10% gaps" / "blocks Steps 2b-3b" | Updated to ~90%, JH-11 added, no longer blocking |
| `VALIDATION_RESULTS.md` | Security table predated upstream closure | Updated: JupyterHub TLS resolved, JH-11 resolved, toadStool/squirrel gap added |
| `TUNNEL_EVOLUTION.md` | Step 3a lacked cell membrane context | Added cell membrane framing for sovereignty target |

### Upstream Handbacks Delivered

| Team | Item | File | Priority |
|------|------|------|----------|
| toadStool | MethodGate pre-dispatch | `crates/server/src/pure_jsonrpc/handler/mod.rs` | Low |
| squirrel | MethodGate pre-dispatch | `crates/main/src/rpc/jsonrpc_request_processing.rs` | Low |
| squirrel | `LocalProcessProvider` → toadStool IPC | `crates/main/src/compute_client/provider_trait.rs` | Low |
| barraCuda | Crypto delegation to bearDog IPC | `crates/barracuda-core/Cargo.toml` | Medium |

---

## 2. NestGate: Critical Upstream Priority

### Why NestGate Is Next

The full Python→Rust→Primal validation chain is proven for compute
(workloads dispatched via toadStool, provenance tracked via rhizoCrypt/
loamSpine/sweetGrass). But the **data** side of the chain is incomplete:

```
Current:  workload TOML → toadStool dispatch → provenance pipeline ✅
Missing:  content → NestGate storage → petalTongue serving → sovereign hosting
Missing:  binary → NestGate blob → plasmidBin fetch → workload dispatch
Missing:  experiment → NestGate manifest → foundation seeding → geological layer
```

### What NestGate Needs

NestGate is **running** in the composition (port 9500, alive, health check
passing). What's missing are the higher-level operations that production
workflows need:

| Capability | Current | Needed |
|------------|---------|--------|
| `storage.put` / `storage.get` | KV storage works | ✅ |
| `content.put` | **Not implemented** | Content-addressed file storage |
| `content.list` / `content.get` | **Not implemented** | Content retrieval by hash |
| Collections/manifests | **Not implemented** | Versioned sets of content (e.g. "sporeprint-v1.2") |
| OCI blob store | **Not implemented** | Store container images for toadStool |

### What It Unblocks

| Downstream | Blocked By | Impact |
|------------|-----------|--------|
| Sovereign primals.eco (H2-05→H2-08) | No content pipeline | Can't replace GitHub Pages |
| plasmidBin binary hosting | No blob storage + manifest | Springs can't ship release binaries to NUCLEUS |
| Foundation geological layers | No content-addressed experiment storage | Science results can't be load-bearing |
| toadStool container workloads | No OCI blob store | Container dispatch stays on Docker Hub |

### For the NestGate Team

Priority features in order:
1. **`content.put(data) → hash`** — content-addressed storage, return BLAKE3 hash
2. **`content.get(hash) → data`** — retrieve by hash
3. **Collection API** — group hashes into named, versioned sets
4. **Manifest query** — list collections, resolve "latest" to hash set

projectNUCLEUS has `deploy/publish_sporeprint.sh` (skeleton) and
`TUNNEL_EVOLUTION.md` Step 3a ready to wire as soon as `content.put` ships.

---

## 3. Composition Patterns Validated in Production

### Pattern: Python → Rust → Primal Evolution

The ecosystem's core methodology, now proven end-to-end:

```
Python prototype (pappusCast.py, 953L monolith)
  → Modular Python (7 modules, clean boundaries)
    → Rust binary (darkforest replaced tier_test_observer.py)
      → Primal composition (darkforest validates observer via NUCLEUS)
```

This pattern was applied to:
- **Security validation**: Python pentest scripts → darkforest Rust binary
- **Observer testing**: `tier_test_observer.py` → `darkforest --suite observer`
- **Infrastructure management**: bash scripts → tunnelKeeper Rust crate
- **Content propagation**: pappusCast monolith → pappusCast modules (Rust next)

### Pattern: Gate-Agnostic Configuration

All runtime paths derive from `$GATE_HOME` (env var with `$HOME` fallback).
No hardcoded usernames, home directories, or machine names in production code.

```bash
# Bash: source deploy/nucleus_config.sh
# Rust: gate_home() → std::env::var("GATE_HOME").or(std::env::var("HOME"))
# Python: from nucleus_paths import ABG_SHARED, PUBLIC_ROOT
# Systemd: EnvironmentFile=/etc/projectnucleus/gate.env
```

### Pattern: Cell Membrane Architecture

Accept that the extracellular world (CDN, DNS, TLS edge) is uncontrolled.
Inside the membrane, total sovereign control. The membrane boundary is:
- The audit boundary (skunkBat monitors crossings)
- The deployment boundary (replicas are membrane-only gates)
- The future bonding boundary (ion channels for scoped cross-gate access)

### Pattern: Modular Deploy Tooling

Deploy scripts source shared configuration and can be replaced incrementally:
- `deploy.sh` (nohup loop) → `composition.deploy(graph)` (biomeOS)
- `gate_watchdog.sh` → tunnelKeeper membrane monitoring
- `security_validation.sh` → thin bash around darkforest binary
- `pappusCast.py` → eventual Rust binary → pappusCast primal

---

## 4. Lessons for All Teams

### What We Got Right

| Lesson | Evidence |
|--------|---------|
| **Env-var-driven from day one** | Zero `gate_provision.sh` failures on replicas |
| **Error propagation, not panic** | `Result<T,E>` + `thiserror` + `?` — zero `unwrap()` in darkforest/tunnelKeeper |
| **Slim dependencies** | tokio `rt-multi-thread,macros` not `full`; `rand_core` not `rand` |
| **Static surfaces are sovereign-friendly** | Zero-compute HTML survives any hosting model |
| **Pre-primal solutions validate primal architecture** | gate_provision.sh proved Plasmodium multi-gate before the primal exists |

### What We Got Wrong (and Fixed)

| Mistake | Cost | Fix |
|---------|------|-----|
| Hardcoded `/home/irongate` in 25 Rust lines | Couldn't provision replica gates | `gate_home()` env-var pattern |
| Monolithic pappusCast.py | Couldn't test or evolve individual tiers | 7-module split |
| `13/13 MethodGate` claim | False confidence in security posture | Source-audited to 11/13, handback delivered |
| Broad `except Exception` | Silent failure masking | Narrowed to specific exception types |
| Spec docs not reconciled with reality | Drift between docs and code | Systematic reconciliation pass |

### What Remains

| Target | Owner | Priority |
|--------|-------|----------|
| NestGate content pipeline | NestGate team | **High** |
| `composition.deploy(graph)` replaces deploy.sh | biomeOS + projectNUCLEUS | High |
| toadStool/squirrel MethodGate | toadStool/squirrel teams | Low |
| barraCuda crypto → bearDog IPC | barraCuda team | Medium |
| BearDog TLS shadow run (H2-12) | projectNUCLEUS (ops) | High |
| Songbird NAT VPS relay (H2-14) | projectNUCLEUS (ops) | Medium |
| Foundation workload orchestration | All springs | Medium |

---

## 5. For primalSpring

The evolution cycle is documented. Key refs for the next primalPSing audit:

- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — canonical absorption targets (updated May 11)
- `projectNUCLEUS/specs/COMPLETE_DEPENDENCY_INVENTORY.md` — dependency clusters (reconciled May 11)
- `projectNUCLEUS/specs/VALIDATION_RESULTS.md` — security/rigor assessment (updated May 11)
- `infra/wateringHole/handoffs/PROJECTNUCLEUS_DEEP_DEBT_UPSTREAM_HANDBACK_MAY11_2026.md` — per-team handback
- `infra/wateringHole/handoffs/PROJECTNUCLEUS_CELL_MEMBRANE_COMPOSITION_HANDOFF_MAY10_2026.md` — architecture

**The gate is clean. The membrane is live. The NestGate pipeline is the next frontier.**
