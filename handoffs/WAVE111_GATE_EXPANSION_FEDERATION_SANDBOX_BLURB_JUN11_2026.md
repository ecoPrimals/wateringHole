# Wave 111 — Remaining Work

**Date**: 2026-06-13 (overwatch cascade assessment)  
**From**: eastGate overwatch  
**FRAGO**: `impulses/active/2026-06-11T21-30_eastGate__wave111-gate-expansion-federation-sandbox.toml`

---

## Convergence State

### riboCipher (Stream 7) — 7/9 Primals Converged

| Team | Status | Evidence |
|------|--------|----------|
| biomeOS | ✅ SHIPPED | v4.26 — `consume_ribocipher_signal()` UDS+TCP, WARN on legacy |
| songBird | ✅ SHIPPED | 3 accept loops, `songbird_types::constants::ribocipher` module, 8929 tests |
| sweetGrass | ✅ SHIPPED | v0.7.57 — reference impl in peek.rs, 1647 tests |
| primalSpring | ✅ SHIPPED | `93207ac` — clear signal `[0xEC, 0x01]` on all IPC |
| cellMembrane | ✅ SHIPPED | `35ad803` — mito-tier HKDF+HMAC, clear on 6 UDS clients, `[transport.ribocipher]` config |
| strandGate/hotSpring | ✅ SHIPPED | server detect + client prepend, 627 tests |
| **bearDog** | ❌ PENDING | No riboCipher commits — oldest peek-and-guess patterns live here |
| **sourDough** | ❌ PENDING | Reference impl + validate + scaffold (accelerator role) |

### Infrastructure

- **Protocol convergence**: 13/13 HEALTH, 6/6 startup, guideStone COMPLETE
- **Stream 6 Divergence**: 14/16 shipped — remaining 2 blocked on hardware
- **Federation**: VALIDATED (64ms RTT, triad deployed, auto-reconnect proven)
- **Pipeline**: P1 automation SHIPPED (freshness auto-publish + VPS auto-rebuild + race fix `082d77c`)
- **ironGate NUCLEUS**: DEPLOYED 13/13 via systemd, benchScale validated
- **Bash fallback**: REMOVED, gate.provision SHIPPED, sandbox/canary SHIPPED
- **strandGate**: LIVE (265/282 validation, riboCipher COMPLIANT)

### Parity

| Repo | origin = forgejo = local |
|------|--------------------------|
| wateringHole | ✅ `74d4bb9` |
| cellMembrane | ✅ `082d77c` |
| bearDog | ✅ `945de60` |
| songBird | ✅ `677ec34` |
| biomeOS | ✅ `4648ffd` |
| sweetGrass | ✅ `a675425` |
| primalSpring | ✅ `44469a9` |
| sourDough | ⚠️ forgejo 500 error — origin `e052ba9`, forgejo `367876d` |

### Freshness Drift

freshness.toml records Wave 111 but is stale for primals that evolved post-publish:
- primalSpring: fresh=`d98c2b1` actual=`44469a9` (riboCipher + port dedup)
- songBird: fresh=`fe47c01` actual=`677ec34` (deep debt + SRP extractions)
- cellMembrane: fresh=`e230e10` actual=`082d77c` (race fix + riboCipher mito-tier)

**Action**: cellMembrane `temporal.cascade --publish-freshness` should self-heal this. NOT an overwatch manual edit.

---

## Remaining Work by Team

### bearDog

| Item | Priority | Notes |
|------|----------|-------|
| **riboCipher server detection** | P1 | unix_socket_ipc/server.rs + tcp_ipc/server.rs — signal before peek |
| **riboCipher client signal** | P1 | BTSP client connections prepend `[0xEC, 0x02]` |
| Legacy WARN path | P2 | Unsignalled connections → WARN log during deprecation period |

The oldest peek-and-guess patterns live in bearDog. This is the critical convergence target.

### sourDough

| Item | Priority | Notes |
|------|----------|-------|
| **Reference implementation** | P1 | Own IPC server implements riboCipher — teams study this |
| **`validate ribocipher`** | P1 | Audit subcommand checks primal accept loops for compliance |
| **Scaffold templates** | P2 | `sourdough scaffold new-primal` emits riboCipher-compliant code |
| Forgejo parity | P2 | Fix 500 error — origin at `e052ba9`, forgejo at `367876d` |

### cellMembrane

| Item | Priority | Notes |
|------|----------|-------|
| **VPS cellMembrane rebuild** | P1 | Deploy `082d77c` to VPS — fixes freshness race + riboCipher mito-tier |
| **VPS `plasmid.harvest --all`** | P1 | biomeOS hash mismatch — depot integrity |
| **Freshness publish** | P1 | `temporal.cascade --publish-freshness` to update stale SHAs |
| Dev gate cascade | P2 | `temporal.cascade --with-restart` on eastGate/southGate |
| westGate gate.bootstrap | P2 | Nest Atomic profile on 76TB ZFS |
| NUC canary bootstrap | P2 | `canary-fieldmouse` profile — Phase 1 VPS minimization |
| Tolerances in deployment.toml | P3 | 4 named tolerances pending codification |
| Pipeline commands (docs.publish, git.publish, impulse.resolve, wave.close) | P3 | Elevate ad-hoc to idiomatic Rust |
| blueGate + swiftGate | P3 | Windows cross-platform (WSL2 or native) |
| northGate | LAST | Family gate, spare compute when not in use |

### songBird

| Item | Priority | Notes |
|------|----------|-------|
| **VPS persistent relay** | P2 | Depot needs latest — auto-rebuild will pull after VPS update |

Code COMPLETE. Remaining is operational (VPS deploy).

### primalSpring

| Item | Priority | Notes |
|------|----------|-------|
| nucleus_launcher aarch64 | P3 | grapheneGate ARM cross-compile |
| Proto-nucleate manifest | P3 | Sub-NUCLEUS topology definition |

### toadStool

| Item | Priority | Notes |
|------|----------|-------|
| **TOADSTOOL-AUTO-REGISTER** | P2 | PCI/sysfs enumeration — auto-register GPU/NPU with biomeOS |

### ops (hardware)

| Item | Priority | Notes |
|------|----------|-------|
| **westGate power-on** | P2 | i7-4771 + 76TB ZFS — network + gate.bootstrap |
| NUCs + Pixle | P2 | Quick Linux node enrollments |
| DEPLOY-THEN-STALE (Stream 6) | P2 | Deploy westGate, skip cascades 2 waves |
| WINDOWS-ECOBIN-DIVERGENCE (Stream 6) | P3 | Deploy to blueGate, measure delta |
| Akida NPU driver | LOW | BrainChip AKD1000 on strandGate |
| northGate | LAST | After all others stable |

---

## Convergence Gate

Old patterns permanently excised when ALL criteria GREEN:

| # | Criterion | State |
|---|-----------|-------|
| 1 | All gates run post-082d77c membrane | ⚠️ ironGate DEPLOYED, eastGate/southGate pending cascade |
| 2 | Depot fully fresh (all 13 BLAKE3 match) | ⚠️ biomeOS stale — VPS auto-rebuild pending |
| 3 | flockGate persistent relay active | ⚠️ needs VPS songBird rebuild |
| 4 | No gate uses bash fallback | ✅ CODE DONE — ironGate systemd deployed |
| 5 | canary.audit passes on canary node | ❌ NUC bootstrap pending |
| 6 | 2 full cascade cycles, zero intervention | ❌ Not yet tested |
| 7 | Version skew = 0 after cascade | ❌ Not yet tested |

**To clear**: VPS rebuild (`082d77c`) → harvest cycle → cascade eastGate/southGate → NUC bootstrap.

---

## Priority Order (What to Do Next)

1. **VPS**: Rebuild cellMembrane to `082d77c` (fixes race + freshness + riboCipher mito)
2. **VPS**: `plasmid.harvest --all` (fixes depot integrity, rebuilds songBird)
3. **cellMembrane**: `temporal.cascade --publish-freshness` (self-heals stale SHAs)
4. **bearDog**: riboCipher convergence (last major primal without signal detection)
5. **sourDough**: Reference impl + validate command (accelerator for fleet convergence)
6. **eastGate/southGate**: `membrane temporal.cascade --with-restart` (criteria 6+7)
7. **NUC**: `gate.bootstrap` with `canary-fieldmouse` profile (criteria 5)
8. **westGate**: Hardware power-on + gate.bootstrap (gate expansion)
9. **toadStool**: TOADSTOOL-AUTO-REGISTER (compute gate autonomy)

---

## Active Documents

| Document | Purpose |
|----------|---------|
| This blurb | Remaining work overview |
| `impulses/active/...wave111...toml` | Wave 111 FRAGO (Stream 6 + Stream 7 riboCipher) |
| `RIBOCIPHER_TRANSPORT_SIGNAL_STANDARD.md` | riboCipher convergent evolution standard |
| `GATE_NUCLEUS_SYSTEMD_STANDARD.md` | systemd deployment standard |
| `CONVERGENCE_GATE_WAVE111_PATTERN_DEPRECATION_JUN12_2026.md` | Pattern deprecation criteria |
| `handoffs/CELLMEMBRANE_RIBOCIPHER_DISPATCH_SRP_WAVE111_JUN13_2026.md` | cellMembrane mito-tier handoff |

---

**riboCipher convergence at 7/9 — the ecosystem is signaling, not guessing. bearDog and sourDough are the remaining convergence targets. VPS rebuild unblocks cascade automation and depot integrity. The system is approaching self-healing autonomy.**
