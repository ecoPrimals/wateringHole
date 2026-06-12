# Wave 111 — Remaining Work Across Ecosystem

**Date**: 2026-06-12 (reset to remaining work only)  
**From**: eastGate overwatch (cellMembrane)  
**FRAGO**: `impulses/active/2026-06-11T21-30_eastGate__wave111-gate-expansion-federation-sandbox.toml`

---

## What's Done (summary)

- Protocol convergence: 13/13 HEALTH, 6/6 startup, guideStone COMPLETE
- Stream 6 Divergence Pressure: **14/16 shipped** (cellMembrane 6/6, songBird 4/4, primalSpring 3/3, biomeOS 2/2)
- Federation: VALIDATED (64ms RTT, enabled=true, auto-reconnect functional)
- Sandbox + canary pipeline: SHIPPED (dependency-aware validation with bearDog injection)
- gate.provision CLI: SHIPPED (DO API, canary-fieldmouse profile)
- Bash fallback: REMOVED (pure Rust gate ops)
- strandGate: postPrimordial LIVE (Tower Atomic + hotSpring, 2 GPUs, 265/282 validation)
- VPS Surface Minimization: PLANNED (Phase 1 immediately actionable)

**Archived**: All completed AARs in `handoffs/archive/wave111/`

---

## Remaining Work by Team

### cellMembrane

| Item | Priority | Notes |
|------|----------|-------|
| **ironGate binary rebuild** | P1 | `cargo install --path crates/membrane-shadow` — activates diesel engine locally |
| **Dev gate cascade** (eastGate/ironGate/southGate) | P2 | `membrane temporal.cascade --with-restart` — pull fresh binaries |
| ~~VPS `MEMBRANE_AUTO_REBUILD=1`~~ | P1 | **DONE** (1baa2ec) — set, active, depot auto-rebuilds on staleness |
| ~~Freshness auto-publish~~ | P1 | **DONE** (1baa2ec) — auto_commit_freshness(), proven on golgiBody VPS |
| **VPS `plasmid.harvest --all`** | P2 | biomeOS depot hash mismatch — auto-rebuild should fix on next cascade cycle |
| **westGate gate.bootstrap** | P2 | Nest Atomic 7/7 on 76TB ZFS — hardware ready |
| **NUC canary bootstrap** | P2 | Phase 1 of VPS minimization — `canary-fieldmouse` profile |
| **NUCs + Pixle spin-up** | P2 | Quick Linux node enrollments |
| **blueGate + swiftGate** | P3 | Windows cross-platform validation (WSL2 or native) |
| **Tolerances in deployment.toml** | P3 | 4 named tolerances pending codification |
| **`membrane docs.publish` command** | P3 | Dual-push for documentation commits |
| **`membrane impulse.resolve` command** | P3 | FRAGO item status automation |
| northGate | LOW | Family gate — spare compute, LAST |
| qS signal graphs | DEFERRED | Not urgent until autonomous gates |
| Freshness → mesh gossip (endgame) | DEFERRED | Eliminates freshness.toml conflicts entirely |

### songBird

| Item | Priority | Notes |
|------|----------|-------|
| **Persistent relay on VPS** | P2 | VPS songBird rebuild to `fe47c012` enables persistent relay (not just mesh.init) |

songBird code is COMPLETE. All 4/4 divergence scenarios shipped. 8918 tests. Remaining work is operational (VPS rebuild).

### primalSpring

| Item | Priority | Notes |
|------|----------|-------|
| nucleus_launcher aarch64 cross-compile | P3 | For grapheneGate ARM deployment |
| Proto-nucleate manifest | P3 | Sub-NUCLEUS topology definition |
| BTSP cross-primal full chain | LOW | Documented gaps, non-blocking |

### toadStool

| Item | Priority | Notes |
|------|----------|-------|
| **TOADSTOOL-AUTO-REGISTER** | P2 | PCI/sysfs hardware enumeration on startup — auto-register GPU/NPU with biomeOS |

Discovered on strandGate: toadStool doesn't auto-discover hardware. Blocks autonomous `gate.bootstrap` for compute gates. Needs diesel engine ignition phase for hardware enumeration.

### ops (hardware)

| Item | Priority | Notes |
|------|----------|-------|
| **westGate hardware setup** | P2 | i7-4771 + 76TB ZFS — power on, network |
| **NUCs + Pixle power-on** | P2 | Quick Linux nodes |
| blueGate + swiftGate access | P3 | Windows machines for cross-platform |
| DEPLOY-THEN-STALE (Stream 6) | P2 | Deploy westGate, skip cascades 2 waves — measure skew |
| WINDOWS-ECOBIN-DIVERGENCE (Stream 6) | P3 | Deploy to blueGate — measure behavior delta |
| northGate | LOW | Family gate, spare compute, LAST |
| 10G backbone cables | LOW | Blocks high-throughput only |
| Akida NPU driver install | LOW | BrainChip AKD1000 on strandGate — needs akida-driver package |

---

## Remaining Work by Gate

| Gate | Status | Remaining |
|------|--------|-----------|
| **flockGate** (WAN) | VALIDATED (64ms RTT, triad deployed) | `plasmid.harvest --all` on VPS (biomeOS hash mismatch). Auto-rebuild should self-heal. |
| **eastGate/ironGate/southGate** (LAN) | 13/13 healthy | Cascade to fresh depot binaries + ironGate binary rebuild |
| **grapheneGate** (ARM) | 13/13 stale binaries | `temporal.cascade --with-restart` (depot fresh, tooling wired) |
| **strandGate** (compute) | LIVE (265/282) | TOADSTOOL-AUTO-REGISTER (manual registration needed for GPUs) |
| **westGate** (storage) | PENDING | Hardware setup → gate.bootstrap nest profile |
| **NUCs + Pixle** (canary/staging) | PENDING | Power on → gate.bootstrap |
| **blueGate + swiftGate** (Windows) | PENDING | Access + cross-platform validation |
| **northGate** (gaming) | LAST | Family gate — after all others stable |

---

## Pipeline Automation

| Command | Priority | Status |
|---------|----------|--------|
| ~~freshness auto-publish~~ | P1 | **DONE** (1baa2ec) — proven on VPS (b3dcf55) |
| ~~`MEMBRANE_AUTO_REBUILD=1`~~ | P1 | **DONE** (1baa2ec) — active on VPS service |
| `membrane docs.publish` | P2 | PENDING — dual-push for doc commits |
| `membrane git.publish` | P2 | PENDING — standard commit flow |
| `membrane impulse.resolve` | P3 | PENDING — FRAGO item automation |
| `membrane wave.close` | P3 | PENDING — archival at wave transitions |

---

## Convergence Gate (Pattern Deprecation)

Old patterns can be permanently excised when ALL criteria are GREEN:

| # | Criterion | State |
|---|-----------|-------|
| 1 | All gates run post-e230e10 membrane | PARTIAL — ironGate binary older |
| 2 | Depot includes partition-tolerant songBird | PARTIAL — needs harvest to fe47c012 |
| 3 | flockGate WAN federation validated | PARTIAL — 64ms RTT, persistent relay pending |
| 4 | No gate uses bash fallback | CODE DONE — binary rollout pending |
| 5 | canary.audit passes on canary nodes | NO CANARY YET — NUC bootstrap pending |
| 6 | 2 full cascade cycles, zero intervention | NOT YET TESTED |
| 7 | Version skew = 0 after cascade | NOT YET TESTED |

**To clear**: ironGate binary rebuild + VPS harvest + one full cascade cycle.

---

## Priority Order (What to Do Next)

1. **ironGate**: `cargo install --path crates/membrane-shadow` (5 min, unblocks criteria 1+4)
2. **VPS**: `plasmid.harvest --targets songbird` + set `MEMBRANE_AUTO_REBUILD=1` (unblocks criteria 2+3)
3. **All gates**: `membrane temporal.cascade --with-restart` (begins criteria 6+7)
4. **NUC**: `gate.bootstrap` with `canary-fieldmouse` profile (Phase 1 VPS minimization)
5. **westGate**: Hardware power-on + gate.bootstrap nest (gate expansion)
6. **toadStool team**: TOADSTOOL-AUTO-REGISTER evolution (unblocks compute gate autonomy)

---

## Active Documents

| Document | Purpose |
|----------|---------|
| This blurb | Remaining work overview |
| `impulses/active/...wave111-gate-expansion-federation-sandbox.toml` | Wave 111 FRAGO (14/16 Stream 6) |
| `handoffs/CONVERGENCE_GATE_WAVE111_PATTERN_DEPRECATION_JUN12_2026.md` | When old patterns die |
| `handoffs/AAR_PIPELINE_ADHOC_PATTERNS_WAVE111_JUN12_2026.md` | Pipeline automation roadmap |
| `handoffs/VPS_SURFACE_MINIMIZATION_EVOLUTION_JUN12_2026.md` | VPS sovereignty path ($24→$6/mo) |
| `handoffs/PREWAVE_SYNC_WAVE111_JUN12_2026.md` | Pre-wave sync state |

---

**Wave 111 is operationally complete in code. Remaining work is: binary rollout (rebuild + cascade), hardware enrollment (westGate, NUCs), and one evolution item (TOADSTOOL-AUTO-REGISTER). The ecosystem is converging toward full self-healing autonomy.**
