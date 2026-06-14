# Convergence Gate — Wave 111 Pattern Deprecation Criteria

**Date**: 2026-06-12  
**From**: eastGate overwatch  
**Purpose**: Define the conditions under which old patterns are permanently deprecated  
**Status**: WATCHING — Criterion 4+8 GREEN, riboCipher ERROR 8/8 complete. VPS DEPLOYED (0ef6c38). Criterion 1: VPS+ironGate at post-34e472d, dev gates pending cascade. 4 criteria pending operational.

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
| 1 | **All gates run post-34e472d membrane** | `membrane --version` ≥ Wave 111 (riboCipher mito-tier) on all 5 active gates | ⚠️ PARTIAL | VPS at `0ef6c38` (13/13 alive). ironGate DEPLOYED (systemd). cellMembrane latest: `06f9ad2`. Dev gates (eastGate/southGate) pending cascade. |
| 2 | **Depot includes partition-tolerant songBird** | provenance.toml → songBird ≥ 9903cf50 | ⚠️ BLOCKED | songBird depot binary still at 32a8d700 (pre-riboCipher). Needs `plasmid.harvest --targets songbird`. |
| 3 | **flockGate WAN federation validated** | `federation.status` → active_connections > 0, latency_ms present | ⚠️ BLOCKED | VPS songBird rejects riboCipher prefix (pre-standard binary). Needs depot rebuild + deploy. Hub listening, 0 peers enrolled. |
| 4 | **No gate uses bash fallback paths** | Code removed (gate/mod.rs e230e10) + binaries updated | ✅ GREEN (ironGate) | ironGate systemd NUCLEUS has no bash path. Cascade propagates to others. |
| 5 | **canary.audit passes on all canary nodes** | `plasmid.canary.audit` → 0 stale entries | ⚠️ NO CANARY YET | NUC bootstrap pending |
| 6 | **2 full cascade cycles, zero manual intervention** | temporal.cascade runs 2x across all 5 gates, no human fix-up needed | ❌ NOT YET TESTED | Gate binary rollout |
| 7 | **Version skew = 0 across mesh after cascade** | `health.audit --mesh` reports no provenance mismatches | ❌ NOT YET TESTED | Criteria 1 + 2 first |

---

## Actions to Clear This Gate

**Immediate (no hardware required):**
1. `plasmid.harvest --targets songbird` on VPS → unblocks Criterion 2 + 3
2. Deploy fresh songBird binary to VPS → clears federation UTF-8 rejection
3. Configure dev gates with VPS peer → enables mesh enrollment
4. `membrane temporal.cascade --with-restart` on eastGate, southGate → advances Criterion 1
5. Run cascade cycle → begins Criterion 6

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
