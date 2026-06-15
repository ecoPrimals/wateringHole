# Wave 113 — Active Tasks + Debt Tracking

**Status**: 5/6 exit criteria met | VPS FULL GREEN (8/8) | Diderm auto-reconciliation SHIPPED  
**Only exit blocker**: Hardware enrollment (ops-physical)  
**Focus now**: Per-primal interaction quality + remaining evolution debt

---

## Per-Primal riboCipher Signal Compliance

| Primal | Signal | Health | Remaining Debt |
|--------|--------|--------|----------------|
| songBird | ✅ | ✅ | ✅ outbound signal + self-connect fix + state-dir shipped (`4169c47a`) |
| nestGate | ✅ `17baed59` | ✅ | DONE |
| sweetGrass | ✅ v0.7.58 | ✅ | DONE |
| biomeOS | ✅ v4.28/4.29 | ✅ | Auto-registration shipped. Remaining: complete primal discovery beyond Bootstrap |
| hotSpring | ✅ REJECT | ✅ | DONE (legacy removed) |
| strandGate | ✅ REJECT | ✅ | DONE (legacy removed) |
| bearDog | ❌ BTSP-locked | ✅ (via BTSP) | Accept prefix + expose `--health-socket` |
| rhizoCrypt | ❌ BTSP reject | ✅ | Accept prefix |
| barracuda | ❌ timeout | ✅ | Accept prefix |
| petalTongue | ✅ `cdcb1ee` | ✅ | **DONE** — riboCipher prefix acceptance shipped (Jun 14). Depot rebuild needed. |
| skunkBat | ❌ timeout | ⚠️ -32601 | Accept prefix + implement `health` method |
| loamSpine | ❌ timeout | ⚠️ -32601 | Accept prefix + implement `health` method |
| coralReef | ❌ parse error | ⚠️ -32601 | Accept prefix + implement `health` method |
| squirrel | ❌ timeout | ⚠️ -32601 | Accept prefix + implement `health` method |
| toadStool | ❌ timeout | ❌ silent | **P1**: Fix silent socket + accept prefix + implement `health` |

**Score**: 7/15 signal-compliant, 10/15 health-responding. Target: 15/15 both.

---

## cellMembrane / ironGate

### DONE (shipped)
- ✅ Diderm auto-reconciliation (`951c96a` + `bd9dfcb`) — auto-rebase on non-ff push
- ✅ ServerContract per-primal CLI
- ✅ riboCipher REJECT (client-side)
- ✅ neuralAPI-routed probes with UDS fallback
- ✅ Profile-aware health expectations
- ✅ Gate identity file
- ✅ Freshness single-writer
- ✅ S4 auth probe fix (read before shutdown, BTSP recognition)
- ✅ membrane-bridge-biomeos REMOVED
- ✅ Cascade stress (`temporal.cascade.stress --cycles N`)
- ✅ Federation: 2 peers enrolled, persistent

### Remaining

| Task | Priority | Notes |
|------|----------|-------|
| Probe biomeOS on neural-api.sock | P2 | Currently probes biomeos.sock (HTTP) |
| Accept -32601 as alive | P2 | 4 primals return method_not_found = still alive |
| aarch64 depot harvest | P2 | Unblocks grapheneGate cross-arch |
| Pepti build orchestration | P3 | Route builds through neuralAPI graph |
| DO SSH key auto-register | P3 | Manual key management during provision |
| Cascade remote canary discovery | P3 | Only VPS visible in mesh currently |
| checksums.toml songBird skew | P3 | Depot `c42ef13` vs checksums `334b695b` |

---

## bearDog

| Task | Priority |
|------|----------|
| Accept riboCipher `[0xEC, 0x01]` prefix | P1 |
| Expose plaintext health socket (`--health-socket`) | P1 |
| Implement `health` JSON-RPC method | P2 |

BTSP-locked main socket. cellMembrane S4 workaround (BTSP error = alive proof) works, but proper compliance needed.

---

## toadStool

| Task | Priority |
|------|----------|
| Fix silent socket (protocol violation) | P1 |
| Accept riboCipher prefix | P1 |
| Implement `health` method | P1 |
| TOADSTOOL-AUTO-REGISTER (PCI/sysfs GPU enumeration) | P2 (carry) |

---

## songBird

| Task | Priority |
|------|----------|
| Accept riboCipher on inbound UDS | P2 |
| Periodic peer reachability probing (without active connection) | P2 |

Outbound TCP signal, self-connect fix, state-dir all shipped. Reachability is STATIC without active connection (gap from partition test).

---

## biomeOS

| Task | Priority |
|------|----------|
| Complete primal discovery (transition beyond Bootstrap mode) | P2 |
| neuralAPI: trigger rescan to populate capability registry | P2 |

Auto-registration shipped. 0 capabilities still registered operationally — needs topology.rescan trigger after all primals boot.

---

## skunkBat, loamSpine, coralReef, squirrel

| Task | Priority |
|------|----------|
| Accept riboCipher prefix | P2 |
| Implement `health` JSON-RPC method | P2 |

Currently return -32601 (method_not_found) — alive but non-compliant.

---

## rhizoCrypt, barracuda

| Task | Priority |
|------|----------|
| Accept riboCipher prefix | P2 |

Already respond to raw health probes — just need signal acceptance.

## petalTongue — **DONE**

All Wave 113 tasks shipped:
- ✅ riboCipher `[0xEC, 0x01]` prefix acceptance (`cdcb1ee`, Jun 14) — peek + consume before BTSP classification
- ✅ HEALTH-01 bare `"health"` → enriched `{status, primal, version, uptime_s}` (`2dba46f`, Jun 11)
- 6,460+ tests, zero clippy warnings. **Depot rebuild needed** to deploy to VPS.

---

## sourDough

| Task | Priority |
|------|----------|
| Validate ribocipher subcommand | P2 |
| Scaffold update for compliant accept loops | P2 |

---

## sporePrint / primalSpring (eastGate)

| Task | Priority |
|------|----------|
| `nucleus --launch` flag (start primals from depot in profile order) | P3 |
| Cascade recipient validation (zero-skew after VPS cascade) | P2 |

Proto-nucleate manifest SHIPPED. guideStone health validation SHIPPED.

---

## grapheneGate

| Task | Priority |
|------|----------|
| Cross-arch deploy (blocked on aarch64 depot harvest) | P3 |

nucleus_launcher works, TCP bind works. Blocked by stale depot + songBird state-dir (now shipped).

---

## ops (physical only)

| Task | Priority |
|------|----------|
| NUC: placement, power, cable | P2 |
| westGate: power on | P2 |

**Only remaining exit criterion.** Once networked → `gate.bootstrap`.

---

## guideStone Amendments

| Amendment | Status |
|-----------|--------|
| `health` method MANDATORY | sporePrint validation ships enforcement. 10/15 comply. |
| riboCipher signal MANDATORY on UDS | 7/15 comply (petalTongue `cdcb1ee` shipped, depot rebuild pending). Standard documented. |
| Socket manifest per primal | Documented in NUCLEUS audit AAR (28 sockets) |
| neuralAPI capability registration | biomeOS auto-registration shipped, needs operational validation |
| Per-primal `server` arg standard | ServerContract enum codifies it. Template units replaced. |

---

## Long-term Debt (carry beyond Wave 113)

| Debt | Owner | Notes |
|------|-------|-------|
| Diderm leader election / mesh-native state | cellMembrane | Rebase works but content conflicts still manual |
| freshness.mesh via songbird mesh.publish | songBird + cellMembrane | Eliminate VCS as coordination layer |
| benchScale Windows/Pixle topologies | sporePrint | No cross-platform gate simulation yet |
| NUCLEUS template → per-primal units | cellMembrane | ServerContract shipped, templates deprecated but not removed |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | riboCipher REJECT | ✅ |
| 2 | Persistent federation | ✅ |
| 3 | DEPLOY-THEN-STALE | ✅ |
| 4 | Hardware enrollment | ⬜ ops |
| 5 | rootpulse execution | ✅ |
| 6 | Gate-clearing issues | ✅ |

**5/6. Wave 113 closes when any hardware gate bootstrapped.**

---

**Primal interaction compliance: 7/15 signal, 10/15 health. Target: all 15. This is the primary evolution pressure for Wave 114.**
