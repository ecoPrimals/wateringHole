# Convergence Gate — Wave 111 Pattern Deprecation Criteria

**Date**: 2026-06-12  
**From**: eastGate overwatch  
**Purpose**: Define the conditions under which old patterns are permanently deprecated  
**Status**: WATCHING — 3/7 criteria GREEN, 4/7 pending operational validation

---

## Context

Wave 111 Stream 6 shipped 13/16 divergence scenarios. Each scenario produced a
robustness primitive that replaces a legacy approach. This document defines the
operational gate: when ALL criteria are GREEN, old patterns can be excised from
code, docs, and runbooks permanently.

---

## Convergence Criteria

| # | Criterion | Condition | State | Blocked By |
|---|-----------|-----------|-------|-----------|
| 1 | **All gates run post-e230e10 membrane** | `membrane --version` ≥ Wave 111 on all 5 active gates | ⚠️ PARTIAL | ironGate local binary older (pre-temporal.cascade) |
| 2 | **Depot includes partition-tolerant songBird** | provenance.toml → songBird ≥ 9903cf50 | ❌ STALE | Needs `plasmid.harvest --targets songbird` |
| 3 | **flockGate WAN federation validated** | `federation.status` → active_connections > 0, latency_ms present | ❌ BLOCKED | Depot rebuild → deploy |
| 4 | **No gate uses bash fallback paths** | Code removed (gate/mod.rs e230e10) + binaries updated | ⚠️ CODE DONE | Binary rollout pending |
| 5 | **canary.audit passes on all canary nodes** | `plasmid.canary.audit` → 0 stale entries | ⚠️ NO CANARY YET | NUC bootstrap pending |
| 6 | **2 full cascade cycles, zero manual intervention** | temporal.cascade runs 2x across all 5 gates, no human fix-up needed | ❌ NOT YET TESTED | Gate binary rollout |
| 7 | **Version skew = 0 across mesh after cascade** | `health.audit --mesh` reports no provenance mismatches | ❌ NOT YET TESTED | Criteria 1 + 2 first |

---

## Actions to Clear This Gate

**Immediate (no hardware required):**
1. `cargo install --path crates/membrane-shadow` on ironGate → clears Criterion 1
2. `membrane plasmid.harvest --targets songbird` on VPS → clears Criterion 2
3. `membrane plasmid.fetch --source wan --targets songbird` on flockGate → unblocks Criterion 3
4. `membrane temporal.cascade --with-restart` on all 5 gates → begins Criterion 6

**Short-term (hardware):**
5. Bootstrap NUC with `canary-fieldmouse` profile → enables Criterion 5
6. Run second cascade cycle → completes Criterion 6
7. Run `health.audit --mesh` → validates Criterion 7

---

## What Gets Deprecated (After Gate Clears)

### Code Excision
- [ ] Any remaining `cascade-pull.sh` references in docs/runbooks
- [ ] Hardcoded primal name strings in dispatch paths (if any remain beyond constants)
- [ ] Unconditional canary failover without freshness check (already removed in code)
- [ ] Single-attempt network operations without backoff (already removed in code)

### Documentation Cleanup
- [ ] Remove "workaround" sections referencing manual `mesh.init`
- [ ] Remove "manual cascade" instructions from runbooks
- [ ] Update GATE_SETUP_STANDARD.md to reflect pure Rust gate operations
- [ ] Archive pre-Wave-111 federation troubleshooting docs

### Operational
- [ ] Stop mentioning `cascade-pull.sh` in team blurbs
- [ ] Update FRAGO templates to assume self-healing cascade
- [ ] Remove "SONGBIRD_FEDERATION_ENABLED env var workaround" notes

---

## Signal: System Converging on Stability

Evidence that the system is approaching steady-state:

1. **songBird**: 4/4 Stream 6 done, 8918 tests, backward-compatible wire
2. **biomeOS**: 2/2 Stream 6 done, self-cleaning registry, partition-aware routing
3. **primalSpring**: 3/3 Stream 6 done, divergence detection validated
4. **cellMembrane**: 5/6 Stream 6 done, bash-free, capability-driven, atomic ops
5. **Membrane parity**: 12/12 repos at origin = forgejo = local
6. **Build determinism**: Zero warnings, forbid(unsafe_code), clean rebuilds <8s

The system is one operational step (depot rebuild + cascade) from full convergence.
Once this gate clears, Wave 112 enters with **only hardware-blocked items remaining**
(westGate, NUCs, blueGate, northGate) — all using proven, self-healing infrastructure.

---

## Watching For

After gate clears, watch for regression signals:
- `health.audit --mesh` should stay at 0 mismatches between cascades
- `plasmid.canary.audit` should stay at 0 stale across cascade cycles
- Federation `active_connections` should remain > 0 (auto-reconnect proves itself)
- No manual intervention required for any cascade cycle

**When these hold for 2+ waves: the system has converged. Old patterns are dead.**
