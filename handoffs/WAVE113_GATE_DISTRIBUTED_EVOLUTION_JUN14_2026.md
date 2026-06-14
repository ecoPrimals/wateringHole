# Wave 113 — Gate-Distributed Evolution

**Date**: 2026-06-14  
**From**: eastGate overwatch  
**Closes**: Wave 112 (6/6 exit criteria met — ephemeral DO canary cleared hardware dependency)  
**Convergence Gate**: ✅ 7/7 GREEN — old patterns are dead  
**Theme**: Every alive gate is an evolution arena. Idle gates are wasted convergence pressure.

---

## Wave 112 Closure

Wave 112 proved operational convergence — **ALL 6/6 exit criteria met**:
- VPS deployed, songBird rebuilt, 2 clean cascades, version skew 0, riboCipher ERROR 8/8
- Hardware enrollment criterion: **CLEARED** via ephemeral DO canary (gate.provision lifecycle proven in <5 min)
- cellMembrane/ironGate shipped: freshness sparse-fix, rootpulse sovereignty, NUCLEUS activation, sourDough forgejo fix, -213 LOC refactor, gate.provision.verify, mesh.init JSON-RPC fix
- Convergence Gate: 7/7 GREEN — cascade-pull.sh dead, manual mesh dead, peek-and-guess dead

**Wave 112: CLOSED.** Self-healing operational convergence proven. Old patterns deprecated.

---

## Wave 113 Model: Gate-Distributed Evolution

While ops physically builds NUCs, the existing 5-gate mesh + WAN continues to evolve. Each gate runs something — testing deployments, validating cascades, exercising federation, stressing the mesh.

```
LAN:  eastGate ←→ ironGate ←→ southGate
                      ↕ (owns)
VPS:            golgiBody (13/13 HEALTHY)
                      ↕ (federation relay)
WAN:              flockGate
ARM:            grapheneGate
```

---

## Per-Gate Assignments

### cellMembrane / ironGate (owns VPS) — P1

| Task | Detail | Status |
|------|--------|--------|
| **riboCipher REJECT prep** | Implement reject-mode in accept loops. Test on VPS — 0 unsignalled in ERROR logs before enabling REJECT. | ⬜ |
| **flockGate persistent federation** | Sustained (not ephemeral) peer enrollment — `active_connections > 0` continuous | ⚠️ proven ephemeral |
| **NUCLEUS-aware probes** | Replace socat with neuralAPI-routed `capability.call` | ⬜ |
| **Pepti build orchestration** | Route depot rebuilds through neuralAPI graph | ⬜ |
| **rootpulse ledger init** | First real commit chain through trio (not dry-run) | ⬜ |
| **Cascade stress** | Schedule cascade cycles against eastGate/southGate — catch regressions | ⬜ |
| **Primal CLI contract** | Standardize server subcommand args (guideStone amendment) — exposed by canary | ⬜ NEW |
| **Gate identity file** | Write `/etc/membrane/gate_identity` during bootstrap | ⬜ NEW |
| **Profile-aware health** | Tower-only = 2/2 PASS, full = 13/13 — fix verify expectations | ⬜ NEW |

### eastGate (primalSpring + overwatch) — P2

| Task | Detail |
|------|--------|
| **Cascade recipient** | Accept cascades from VPS, validate zero-skew |
| **Proto-nucleate manifest** | Design sub-NUCLEUS topologies (nest, tower, compute profiles) |
| **Validation monitoring** | Run `s_ecosystem_freshness` + full suite after cascades |
| **Overwatch auditing** | Monitor cascade logs for manual intervention signals |

### southGate — P2

| Task | Detail |
|------|--------|
| **Parallel cascade target** | Second LAN gate for cascade diversity |
| **DEPLOY-THEN-STALE** | Skip 1-2 cascade cycles intentionally, verify `health.audit --mesh` detects skew (Stream 6 without new hardware) |

### grapheneGate (aarch64) — P3

| Task | Detail |
|------|--------|
| **Cross-arch cascade** | Confirm x86 VPS → ARM gate cascade works |
| **nucleus_launcher deploy** | Deploy 1.9MB ELF, validate NUCLEUS subset startup |

### flockGate (WAN) — P2

| Task | Detail | Status |
|------|--------|--------|
| **Persistent federation** | Sustained (not ephemeral) `active_connections > 0` — ephemeral canary proved code, now validate ops | ⚠️ proven ephemeral |
| **WAN cascade** | Cascade over WAN link, measure latency/reliability | ⬜ |
| **Partition tolerance** | Kill VPS songBird, verify auto-reconnect (operational validation of Stream 6 code) | ⬜ |

---

## ops (physical only)

Hardware that requires human hands. Cannot be agentified.

| Task | Detail |
|------|--------|
| NUC setup | Physical placement, power, network cable |
| westGate | Power on, cable (i7-4771 + 76TB ZFS) |

Once powered and networked, `gate.bootstrap` is cellMembrane's job.

---

## Wave 113 Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | riboCipher REJECT deployed on at least 1 gate (VPS) with 0 unsignalled callers in ERROR logs | ⬜ |
| 2 | flockGate persistent federation: `active_connections > 0` (not ephemeral — sustained) | ⚠️ PROVEN ephemeral, needs persistent |
| 3 | DEPLOY-THEN-STALE validated (southGate skips cascades, mesh detects) | ⬜ |
| 4 | At least 1 new hardware gate enrolled (NUC or westGate — ops-dependent) | ⬜ |
| 5 | rootpulse: first real (non-dry-run) commit chain through trio | ⬜ |
| 6 | Issues exposed by gate clearing resolved: per-primal CLI contracts, gate identity file, profile-aware health | ⬜ |

---

## Deprecation Timeline

| Wave | riboCipher Policy | Status |
|------|-------------------|--------|
| 111 | WARN on legacy | ✅ DONE |
| 112 | ERROR on legacy | ✅ DONE (8/8) |
| **113** | **REJECT unsignalled** | IN PROGRESS |
| 114 | REMOVE legacy paths | — |

---

## Key Principle

> Gates are evolution arenas. Every gate that's alive should be running something. The mesh is the test environment. The mesh IS the system under test.

---

**Wave 113: Distribute. Evolve. Stress. Every gate earns its place.**
