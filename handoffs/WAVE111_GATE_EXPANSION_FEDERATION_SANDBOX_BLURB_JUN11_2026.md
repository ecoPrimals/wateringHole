# Wave 111 — Remaining Work

**Date**: 2026-06-13 (scoped to outstanding items only)  
**From**: eastGate overwatch (cellMembrane)  
**FRAGO**: `impulses/active/2026-06-11T21-30_eastGate__wave111-gate-expansion-federation-sandbox.toml`

---

## Exit State (What's Done)

- Protocol convergence: 13/13 HEALTH, 6/6 startup, guideStone COMPLETE
- Stream 6 Divergence: **14/16 shipped** — remaining 2 blocked on hardware
- Federation: VALIDATED (64ms RTT, triad deployed, auto-reconnect proven)
- Pipeline: P1 automation SHIPPED (freshness auto-publish + VPS auto-rebuild + race fix)
- **ironGate NUCLEUS DEPLOYED**: 13/13 via systemd, benchScale validated (Docker→VM→prod)
- **GATE_NUCLEUS_SYSTEMD_STANDARD**: Ecosystem standard published
- strandGate: LIVE (265/282 validation, 0 regressions)
- Bash fallback: REMOVED, gate.provision SHIPPED, sandbox/canary SHIPPED
- Freshness race fix: wave-ID guard prevents stale overwrites (`082d77c`)

**All AARs archived**: `handoffs/archive/wave111/`

---

## Remaining Work by Team

### cellMembrane

| Item | Priority | Notes |
|------|----------|-------|
| **VPS cellMembrane rebuild** | P1 | Deploy `082d77c` to VPS — fixes freshness wave-ID + race condition |
| **VPS `plasmid.harvest --all`** | P1 | biomeOS hash mismatch — depot integrity. Auto-rebuild should self-heal after VPS update |
| **Dev gate cascade** | P2 | `temporal.cascade --with-restart` on eastGate/southGate (ironGate already deployed) |
| **westGate gate.bootstrap** | P2 | Nest Atomic profile on 76TB ZFS |
| **NUC canary bootstrap** | P2 | `canary-fieldmouse` profile — Phase 1 VPS minimization |
| **Tolerances in deployment.toml** | P3 | 4 named tolerances pending codification |
| `membrane docs.publish` | P3 | Dual-push for doc commits |
| `membrane git.publish` | P3 | Standard commit flow wrapper |
| `membrane impulse.resolve` | P3 | FRAGO item status automation |
| `membrane wave.close` | P3 | Archival at wave transitions |
| blueGate + swiftGate | P3 | Windows cross-platform (WSL2 or native) |
| northGate | LOW | Family gate, spare compute, LAST |
| Freshness → mesh gossip | DEFERRED | Endgame — eliminates freshness.toml entirely |

### songBird

| Item | Priority | Notes |
|------|----------|-------|
| **VPS persistent relay** | P2 | VPS depot needs `dcc728fc` — auto-rebuild will pull latest |

Code COMPLETE (8918 tests, 4/4 divergence shipped). Remaining is operational.

### primalSpring

| Item | Priority | Notes |
|------|----------|-------|
| nucleus_launcher aarch64 | P3 | grapheneGate ARM cross-compile |
| Proto-nucleate manifest | P3 | Sub-NUCLEUS topology definition |

### toadStool

| Item | Priority | Notes |
|------|----------|-------|
| **TOADSTOOL-AUTO-REGISTER** | P2 | PCI/sysfs enumeration on startup — auto-register GPU/NPU with biomeOS |

Blocks autonomous `gate.bootstrap` for compute gates. Diesel engine ignition phase.

### ops (hardware)

| Item | Priority | Notes |
|------|----------|-------|
| **westGate power-on** | P2 | i7-4771 + 76TB ZFS — network + gate.bootstrap |
| **NUCs + Pixle** | P2 | Quick Linux node enrollments |
| DEPLOY-THEN-STALE (Stream 6) | P2 | Deploy westGate, skip cascades 2 waves |
| WINDOWS-ECOBIN-DIVERGENCE (Stream 6) | P3 | Deploy to blueGate, measure delta |
| blueGate + swiftGate access | P3 | Windows machines |
| Akida NPU driver | LOW | BrainChip AKD1000 on strandGate |
| northGate | LOW | LAST |

---

## Remaining Work by Gate

| Gate | Status | Next Action |
|------|--------|-------------|
| **ironGate** (workstation) | ✅ NUCLEUS DEPLOYED (13/13 systemd) | VPS rebuild for cascade integration |
| **flockGate** (WAN) | VALIDATED, triad deployed | VPS depot rebuild → persistent relay |
| **eastGate/southGate** (LAN) | 13/13 healthy | `temporal.cascade --with-restart` |
| **grapheneGate** (ARM) | Stale binaries | `temporal.cascade --with-restart` |
| **strandGate** (compute) | LIVE (265/282) | TOADSTOOL-AUTO-REGISTER only |
| **westGate** (storage) | PENDING | Hardware power-on → gate.bootstrap |
| **NUCs + Pixle** (canary) | PENDING | Power on → gate.bootstrap |
| **blueGate + swiftGate** (Windows) | PENDING | Access + cross-platform |
| **northGate** (gaming) | LAST | After all others stable |

---

## Convergence Gate

Old patterns permanently excised when ALL criteria GREEN:

| # | Criterion | State |
|---|-----------|-------|
| 1 | All gates run post-e230e10 membrane | ⚠️ ironGate DEPLOYED, eastGate/southGate pending cascade |
| 2 | Depot fully fresh (all 13 BLAKE3 match) | ⚠️ biomeOS stale — VPS auto-rebuild pending |
| 3 | flockGate persistent relay active | ⚠️ needs VPS songBird rebuild |
| 4 | No gate uses bash fallback | ✅ CODE DONE — ironGate systemd deployed |
| 5 | canary.audit passes on canary node | ❌ NUC bootstrap pending |
| 6 | 2 full cascade cycles, zero intervention | ❌ Not yet tested |
| 7 | Version skew = 0 after cascade | ❌ Not yet tested |

**To clear**: VPS rebuild (`082d77c`) → harvest cycle → cascade eastGate/southGate → NUC bootstrap.

---

## NEW: FBSP — First-Byte Signal Protocol (Stream 7)

**Standard**: `FIRST_BYTE_SIGNAL_PROTOCOL_STANDARD.md`  
**Root cause**: ironGate/cellMembrane found peek-based routing hangs on encrypted first bytes. Primals disagree on "unknown byte" meaning. Jelly-sting pattern that must converge.

**Each team evolves independently** — no shared crate, no cross-primal dependency. The standard defines the target; each team implements idiomatically.

| Team | Wave 111 Task |
|------|---------------|
| bearDog | FBSP detection in server accept loops. Legacy WARN. |
| songBird | FBSP detection in pure_rust_server + bin_interface. Mito for federation. |
| biomeOS | FBSP detection in API + neural-api sockets. |
| sweetGrass | Reference implementation in peek.rs. |
| primalSpring | nucleus_launcher + harness send clear signal. |
| cellMembrane | `uds_jsonrpc_call()` prepends `[0xEC, 0x01]`. Config in membrane.toml. |

**Deprecation**: WARN (111-112) → ERROR (112) → REJECT (113) → REMOVE (114)

---

## Priority Order (What to Do Next)

1. **VPS**: Rebuild cellMembrane to `082d77c` (fixes race condition + freshness wave-ID)
2. **VPS**: `plasmid.harvest --all` (fixes biomeOS hash mismatch, rebuilds songBird)
3. **eastGate/southGate**: `membrane temporal.cascade --with-restart` (criteria 6+7)
4. **NUC**: `gate.bootstrap` with `canary-fieldmouse` profile (criteria 5)
5. **westGate**: Hardware power-on + gate.bootstrap (gate expansion)
6. **toadStool**: TOADSTOOL-AUTO-REGISTER (compute gate autonomy)
7. **ALL TEAMS**: Begin FBSP convergent evolution (Stream 7)

---

## Active Documents

| Document | Purpose |
|----------|---------|
| This blurb | Remaining work overview |
| `impulses/active/...wave111...toml` | Wave 111 FRAGO (14/16 Stream 6 + Stream 7 FBSP) |
| `FIRST_BYTE_SIGNAL_PROTOCOL_STANDARD.md` | **NEW** — FBSP convergent evolution standard |
| `GATE_NUCLEUS_SYSTEMD_STANDARD.md` | systemd deployment standard |
| `BENCHSCALE_NUCLEUS_VALIDATION_IRONGATE_DEPLOY_JUN12_2026.md` | **NEW** — ironGate deploy handoff |
| `CONVERGENCE_GATE_WAVE111_PATTERN_DEPRECATION_JUN12_2026.md` | Pattern deprecation criteria |
| `AAR_PIPELINE_ADHOC_PATTERNS_WAVE111_JUN12_2026.md` | Pipeline automation roadmap |
| `VPS_SURFACE_MINIMIZATION_EVOLUTION_JUN12_2026.md` | VPS sovereignty path |

---

**Wave 111 is code-complete. ironGate NUCLEUS deployed. FBSP standard published — all teams begin convergent evolution away from fragile peek patterns. Remaining: VPS rebuild, cascade, hardware enrollment, TOADSTOOL-AUTO-REGISTER, and per-team FBSP adoption. The ecosystem is self-deploying and self-declaring.**
