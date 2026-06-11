# Wave 110 — Last Mile Health + Gate Expansion

**Date**: 2026-06-11 (prepared; activate on Wave 109 closure)
**From**: eastGate overwatch (cellMembrane)
**FRAGO**: `impulses/active/2026-06-11T07-20_eastGate__wave109-guidestone-deployment-convergence.toml` (carries forward)

---

## Wave 109 Exit Summary

Wave 109 proved guideStone infrastructure lands at scale:
- **39/59 FRAGO items resolved** (66% closed)
- **Startup contract 5/6** — barraCuda, coralReef, nestGate, biomeOS, skunkBat all converged
- **HEALTH-01 10/13** — schema, sweetGrass, biomeOS, healthSpring all compliant
- **Build pipeline landed** — `plasmid.build` Rust, `deployment.toml`, gate profiles, JSON-RPC health sweep
- **BTSP server ready** — sweetGrass v0.7.56, 88 BTSP tests
- **grapheneGate 13/13** — first cross-arch full NUCLEUS on mobile hardware

**Carried from Wave 109** (20 items): bearDog startup, 3 primals health, LAUNCHER-01, BTSP-E2E-01, build hardening (5), gate engine, all Stream 5 (7 cascade/qS/rP items), flockGate federation, sourDough segfault.

---

## Wave 110 Focus

**Theme**: Close HEALTH-01 13/13, execute BTSP E2E proof, begin gate expansion, primalSpring self-convergence.

---

## 6 Work Streams

### Stream 1: HEALTH-13/13 — Close the Health Contract

**Owner**: songBird, rhizoCrypt, petalTongue teams
**guideStone**: P3 (Self-Verifying), P5 (Tolerance-Documented)

| Item | Owner | Priority | Notes |
|------|-------|----------|-------|
| HEALTH-RC-01 | rhizoCrypt | P2 | Enrich `health_liveness()` → add `primal`, `version`, `uptime_s` |
| HEALTH-PT-01 | petalTongue | P2 | Bare `"health"` alias + schema enrichment |
| HEALTH-SB-01 | songBird | P2 | Standard health endpoint (ties to federation investigation) |
| STARTUP-BD-01 | bearDog | P2 | Abstract socket auto-detect (last startup holdout) |

**Exit criterion**: 13/13 primals respond to `{"method":"health"}` with `{status, primal, version, uptime_s}`.

### Stream 2: BTSP End-to-End — Encrypted Composition Proof

**Owner**: primalSpring + bearDog + sweetGrass
**guideStone**: P3 (Self-Verifying)

| Item | Owner | Priority |
|------|-------|----------|
| BTSP-E2E-01 | primalSpring | P2 |
| grapheneGate BTSP TCP validation | primalSpring | P3 |

**Exit criterion**: Full bearDog→client→sweetGrass handshake validated (pass or documented failure mode with root cause).

### Stream 3: Build Hardening — Pipeline Determinism

**Owner**: cellMembrane
**guideStone**: P1 (Deterministic), P2 (Reference-Traceable)

| Item | Priority |
|------|----------|
| BUILD-CACHE-01: clean staging before `--all` | P2 |
| BUILD-ELF-01: ELF arch validation at build time | P2 |
| HARVEST-NAME-01: cargo-vs-primal naming audit | P2 |
| GATE-PROFILE-01: gate.bootstrap reads profile TOML | P2 |
| Gate engine: `deploy_pixel.sh` → transport backend | P3 |

### Stream 4: Gate Expansion — northGate + westGate

**Owner**: cellMembrane + biomeOS + eastGate ops
**guideStone**: P1 (Deterministic), P4 (Environment-Agnostic)

| Gate | Hardware | Target Composition | Notes |
|------|----------|-------------------|-------|
| **northGate** | Ryzen 9950X3D, RTX 5090 (32GB), 96GB | Full NUCLEUS (13/13) | Heaviest compute node in fleet |
| **westGate** | i7-4771, RTX 2070 Super, 76TB ZFS | Nest Atomic (7 primals) | Cold storage specialization |

**Phase**:
1. `gate.bootstrap` enrollment (6-phase + deployment.toml)
2. NUCLEUS binary fetch from VPS depot
3. Health sweep (13/13 or 7/7 Nest)
4. Songbird mesh enrollment (:7700)
5. primalSpring validation scenario (`s_graphenegate_readiness` pattern)

**Exit criterion**: northGate 13/13 alive + meshed. westGate Nest Atomic 7/7 alive.

### Stream 5: primalSpring Dogfood — Self-Convergence

**Owner**: primalSpring evolution team (parallel chat)
**guideStone**: P4 (Environment-Agnostic), P5 (Tolerance-Documented)

| Item | Priority | Notes |
|------|----------|-------|
| STARTUP-PS-01: `--bind-mode`/`--port` on `primalspring_primal` | P1 | Dogfood own standard |
| HEALTH-PS-01: bare `"health"` + `uptime_s` on own server | P1 | Dogfood HEALTH-01 |
| LAUNCHER-01: `nucleus_launcher` aarch64 cross-compile | P2 | On-device orchestration |
| Inline tolerance migration (~15 scenarios) | P2 | guideStone P5 compliance |
| Proto-nucleate manifest completion (4 springs) | P3 | Composition readiness |
| Clippy test compliance (test targets passing `-D warnings`) | P3 | CI quality |

### Stream 6: Federation Debug — flockGate WAN

**Owner**: songBird team + flockGate ops
**guideStone**: P1 (Deterministic)

| Investigation | Question |
|---------------|----------|
| Client activation | What enables `federation.enabled = true`? |
| Auth dependency | Is `SECURITY_PROVIDER_SOCKET` required? |
| Config delta | What do LAN gates have that flockGate/VPS don't? |
| Push model | Should VPS initiate federation TO flockGate? |

**Exit criterion**: Root cause documented. Fix shipped OR architecture decision recorded.

---

## Housekeeping (Wave 110)

| Item | Priority |
|------|----------|
| PRIMAL_REGISTRY.md refresh (done this wave — versions updated) | DONE |
| ecosystem_manifest.toml bump to v2.6.0 / Wave 109 | DONE |
| Archive nestGate/sweetGrass handoffs | DONE |
| GLACIAL_SHIFT_READINESS update | DONE |

---

## Carry Forward (deferred to Wave 111+)

| Item | Owner | Notes |
|------|-------|-------|
| Stream 5 cascade/qS/rP (7 items) | cellMembrane | Infrastructure not urgent until autonomous gates |
| healthSpring 14 upstream gaps | Various primals | LOW, stable workarounds |
| sourDough depot segfault | sourDough | LOW, manual `b3sum` fallback |
| 10G backbone cables | ops | Blocks high-throughput only |
| biomeGate recovery | ops/kernel | hotSpring can use strandGate |

---

## Success Criteria (Wave 110 exit gate)

- [ ] 13/13 HEALTH-01 compliant (or 12/13 with songBird federation documented)
- [ ] BTSP-E2E-01 first execution documented (pass or root cause)
- [ ] northGate NUCLEUS 13/13 bootstrapped and meshed
- [ ] primalSpring serves on own standard (`--bind-mode`, `"health"`)
- [ ] bearDog STARTUP-BD-01 resolved → **6/6 startup contract**
- [ ] flockGate federation root cause documented
- [ ] Registry versions reflect ground truth (maintained this wave)

---

## Routing — Primal Status (Wave 110 entry)

| Primal | Work | Status |
|--------|------|--------|
| **bearDog** | STARTUP-BD-01 + BTSP-E2E-01 client | ACTIVE |
| **songBird** | HEALTH-SB-01 + federation investigation | ACTIVE |
| **rhizoCrypt** | HEALTH-RC-01 | ACTIVE |
| **petalTongue** | HEALTH-PT-01 | ACTIVE |
| All others (9) | — | STANDBY |

---

## Active Documents

| Document | Purpose |
|----------|---------|
| This blurb | Wave 110 per-level guidance |
| `impulses/active/...wave109-guidestone-deployment-convergence.toml` | Main FRAGO (carries forward) |
| `impulses/active/...wave109-wan-federation-disabled.toml` | flockGate federation gap |
| `cellMembrane/AAR_CELLMEMBRANE_WAVE106_DETERMINISTIC_DEPLOYMENT_JUN10_2026.md` | Living deployment standard |
| `GLACIAL_SHIFT_READINESS.md` | Stadial entry tracking |

---

**Wave 109 proved the infrastructure works. Wave 110 closes the last mile.**
