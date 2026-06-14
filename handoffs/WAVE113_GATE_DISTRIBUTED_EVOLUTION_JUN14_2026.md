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
| **riboCipher REJECT prep** | Implement reject-mode in accept loops. Test on VPS — 0 unsignalled in ERROR logs before enabling REJECT. | ✅ hotSpring+strandGate SHIPPED. VPS remaining. |
| **flockGate persistent federation** | Sustained (not ephemeral) peer enrollment — `active_connections > 0` continuous | ⚠️ BLOCKED — enroll flockGate on VPS |
| **NUCLEUS-aware probes** | Replace socat with neuralAPI-routed `capability.call` | ⬜ |
| **Pepti build orchestration** | Route depot rebuilds through neuralAPI graph | ⬜ |
| **rootpulse ledger init** | First real commit chain through trio (not dry-run) | ⬜ |
| **Cascade stress** | Schedule cascade cycles against eastGate/southGate — catch regressions | ⬜ |
| **Primal CLI contract** | Standardize server subcommand args (guideStone amendment) — exposed by canary | ⬜ NEW |
| **Gate identity file** | Write `/etc/membrane/gate_identity` during bootstrap | ⬜ NEW |
| **Profile-aware health** | Tower-only = 2/2 PASS, full = 13/13 — fix verify expectations | ⬜ NEW |

### eastGate (primalSpring + overwatch) — P2

| Task | Detail | Status |
|------|--------|--------|
| **Cascade recipient** | Accept cascades from VPS, validate zero-skew | ⬜ |
| **Proto-nucleate manifest** | Design sub-NUCLEUS topologies (nest, tower, compute profiles) | ✅ SHIPPED (sporePrint `69e850c`) |
| **Validation monitoring** | Run `s_ecosystem_freshness` + full suite after cascades | ✅ 929 tests green |
| **Overwatch auditing** | Monitor cascade logs for manual intervention signals | ⬜ |

### southGate — P2

| Task | Detail |
|------|--------|
| **Parallel cascade target** | Second LAN gate for cascade diversity |
| **DEPLOY-THEN-STALE** | Skip 1-2 cascade cycles intentionally, verify `health.audit --mesh` detects skew (Stream 6 without new hardware) |

### grapheneGate (aarch64) — P3

| Task | Detail | Status |
|------|--------|--------|
| **Cross-arch cascade** | Confirm x86 VPS → ARM gate cascade works | ⬜ (stale depot blocks) |
| **nucleus_launcher deploy** | Deploy 1.9MB ELF, validate NUCLEUS subset startup | ⚠️ launcher works, blocked by pre-riboCipher depot binaries + songBird PID dir |

### flockGate (WAN) — P2

| Task | Detail | Status |
|------|--------|--------|
| **Persistent federation** | Sustained (not ephemeral) `active_connections > 0` — VPS must enroll flockGate | ⚠️ BLOCKED on VPS peer enrollment |
| **WAN cascade** | Cascade over WAN link, measure latency/reliability | ✅ VALIDATED (2.2 MB/s, BLAKE3 verified) |
| **Partition tolerance** | Kill VPS songBird, verify auto-reconnect | ⚠️ GAP: reachability is STATIC without active connection — needs enrollment first |

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
| 1 | riboCipher REJECT deployed on at least 1 gate with 0 unsignalled callers | ✅ DONE — hotSpring `c0245b6` + strandGate: -32002, legacy removed |
| 2 | flockGate persistent federation: `active_connections > 0` (sustained) | ⚠️ BLOCKED — VPS must enroll flockGate as peer |
| 3 | DEPLOY-THEN-STALE validated (southGate skips cascades, mesh detects) | ⬜ |
| 4 | At least 1 new hardware gate enrolled (NUC or westGate — ops-dependent) | ⬜ |
| 5 | rootpulse: first real (non-dry-run) commit chain through trio | ⬜ |
| 6 | Issues exposed by gate clearing resolved: CLI contracts, gate identity, profile-aware health | ⚠️ PARTIAL — proto-nucleate SHIPPED, CLI+identity pending |

---

## Deprecation Timeline

| Wave | riboCipher Policy | Status |
|------|-------------------|--------|
| 111 | WARN on legacy | ✅ DONE |
| 112 | ERROR on legacy | ✅ DONE (8/8) |
| **113** | **REJECT unsignalled** | IN PROGRESS |
| 114 | REMOVE legacy paths | — |

---

## Critical Findings (this wave)

| Finding | Impact | Action |
|---------|--------|--------|
| **Multi-gate freshness divergence** | ironGate + golgiBody both auto-publish → parallel histories → manual `--force-with-lease` required | P2 cellMembrane: Single-writer policy (golgiBody only) + evolve to mesh.publish |
| **songBird reachability is STATIC** | Partition tolerance undetectable without active connection — `last_seen_ms` climbs forever | P2 songBird: Add periodic reachability probing even without established federation |
| **grapheneGate depot stale** | Pre-riboCipher binaries misinterpret `[0xEC, 0x01]` as BTSP frame (3.9GB) | P1 cellMembrane: `plasmid.harvest --targets beardog,songbird --arch aarch64` from HEAD |
| **songBird PID dir portability** | Read-only filesystem on GrapheneOS blocks startup | P2 songBird: Add `--state-dir` / `SONGBIRD_STATE_DIR` with XDG fallback |
| **flockGate enrollment missing** | Code proven via ephemeral canary, but persistent ops not yet done | P1 cellMembrane: Update VPS SONGBIRD_PEERS + restart |

### Divergence Pattern (chronic, needs evolution)

Multiple gates auto-publish freshness independently → different SHAs for same content → remotes diverge → manual reconciliation. The membrane **detects** it (writes impulse notifications) but doesn't **resolve** it. This is the same class of problem we've manually fixed 4+ times.

**Recommended**: Designate golgiBody VPS as sole freshness publisher (short-term). Evolve to `freshness.mesh` via songbird `mesh.publish` (long-term, eliminates VCS as coordination layer).

---

## Key Principle

> Gates are evolution arenas. Every gate that's alive should be running something. The mesh is the test environment. The mesh IS the system under test.

---

**Wave 113: 1/6 exit criteria met. Critical path: VPS peer enrollment → persistent federation.**
