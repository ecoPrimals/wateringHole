# ecoPrimals Ecosystem Blurb — Wave 133b

**Date**: Jul 7, 2026 07:51 EDT | **Wave**: 133b | **From**: eastGate overwatch
**Posture**: **ENMESH + HARDEN + VALIDATE** — 30/30 ecobins in pepti. 1097 tests GREEN. CI convergence in progress. Pattern hardening wave.

---

## Ecosystem State

```
LIVE:
  ✅ E2E HTTP: lab.primals.eco → 200 (JupyterHub 5.4.5)
  ✅ LAN mesh: eastGate ↔ ironGate (Omada 10G backbone)
  ✅ WAN mesh: flockGate via golgi relay (2 peers)
  ✅ Mobile: grapheneGate 12/13 primals LIVE via ADB (nestGate+coralReef: UDS fatal)
  ✅ Pepti warehouse: 30/30 ecobins (15 x86_64 + 15 aarch64), checksums verified
  ✅ Relay: golgi synced, 17 repos shallow-cloned, disk 75%
  ✅ 13/13 primals STANDBY — zero code debt
  ✅ Sovereignty: S1-S4 ALL GRADUATED on inner membrane
  ✅ primalSpring: 1097 pass, 0 fail, 124 scenarios (SHADER_F64 RESOLVED)

MESHED:
  eastGate ←✅→ ironGate      (LAN, 10G Omada)
  eastGate ←✅→ golgi         (WG relay)
  flockGate ←✅→ golgi        (WAN, 2 peers)
  grapheneGate ←✅→ eastGate  (ADB, 12/13 primals)
  strandGate: ALIVE .103       (SSH pending)
```

---

## EVOLUTION ABSORBED THIS WAVE

| What | Commit | Impact |
|------|--------|--------|
| grapheneGate full NUCLEUS | AAR filed | 12/13 primals on Pixel 8a. nestGate + coralReef UDS-fatal on Android. |
| Sovereign CI 30/30 ecobins | AAR filed | Pepti confirmed complete. 8 CI divergences flagged. |
| biomeOS CI-DIV-01 fix | `f77886d1` | `default-members` fixed — `cargo build --bin biomeos` works. **RESOLVED.** |
| primalSpring 124th scenario | `9154ea4` | WAN dispatch validation scenario added. 1099 total tests. |
| sporePrint deep debt sprint | `89606fd` | Nucleus refactor, profile-driven probes, sovereign AAR. 226 pages. |
| sporePrint content evolution | `84b5d06`+ | Living systems, sovereign CI pages, SVG diagrams, contact page. |
| golgi disk + freshness | manual | Recovered 100%→75%. HEAD metadata published. Cascade timestamp bug found. |
| sporePrint sovereignty AAR | handoff filed | DNS cutover path mapped. VPS NUCLEUS architecture defined. |

---

## REMAINING WORK BY TEAM

### RESOLVED since last blurb

| ID | Resolution |
|----|------------|
| ~~PS-F64-01~~ | **RESOLVED** (`4e7f888`) — SHADER_F64 + compute precision added to manifest. 1097 tests GREEN. |
| ~~CI-DIV-01~~ | **RESOLVED** (`f77886d1`) — biomeOS `default-members` fixed. |
| ~~golgi HEAD~~ | **RESOLVED** — golgiBody auto-publishing freshness every 15 min. |

---

### Active P1 items

| Team | ID | Item |
|------|----|------|
| cellMembrane | CI-DIV-07 | `temporal.cascade` doesn't commit freshness (workaround active, needs proper fix) |
| flockGate | WAN-DISPATCH-01 | Cross-gate `capability.call` validation (primalSpring scenario ready) |
| eastGate hw | STRAND-SSH-01 | strandGate SSH key deploy (house 2, .103) |
| sporePrint | SP-DIV-01 | DNS cutover blocked on VPS NUCLEUS + bearDog ACME |

---

### Active P2 items

| Team | ID | Item |
|------|----|------|
| eastGate hw | DARK-FOREST-01 | Re-enable dark-forest after 3+ LAN peers have bearDog |
| cellMembrane | VPS-NUCLEUS | Deploy NUCLEUS on golgi for sporePrint (~70MB) |
| cellMembrane | CI-DIV-08 | ecosystem_manifest.toml schema validation |
| cellMembrane | SP-DIV-04 | Post-cascade `zola build` hook for sporePrint |
| sporePrint | SP-DIV-02 | Dual-push workaround until DNS cutover |

---

## Repo Status

```
bearDog       6ef436864  gatehouse + Android fix
songBird      40699793   drawbridge wired into orchestrator
skunkBat      e7eaa5d    stable
biomeOS       f77886d1   CI-DIV-01 RESOLVED (default-members)
toadStool     1ec3749    DH-1 resolved
nestGate      d355c8db   platform_detection simplified
squirrel      45b186b    Wave 129 mock evolution
coralReef     3078d0b    stable
barraCuda     b2618db0   stable
loamSpine     e68873d    stable
petalTongue   0f8da6b    stable
rhizoCrypt    ef85124    stable
sweetGrass    bab4657    stable
primalSpring  e3c4b35    124 scenarios, 1099 tests (4 fail: SHADER_F64 gap)
wateringHole  ce7fd16    Wave 133a + AARs
sporePrint    89606fd    deep debt sprint + living systems
projectNUCLEUS ce928f0   synced to Wave 132f
```

---

## Critical Path

```
✅ 30/30 ecobins in pepti (verified)
✅ 1097 tests GREEN, 124 scenarios (PS-F64-01 RESOLVED)
✅ grapheneGate 12/13 LIVE
✅ biomeOS CI-DIV-01 RESOLVED
✅ golgi freshness auto-publishing (every 15 min)

ACTIVE:
1. [GATE]     STRAND-SSH-01: strandGate enrollment → 3rd LAN peer
2. [GATE]     WAN-DISPATCH-01: flockGate cross-gate validation
3. [GATE]     DARK-FOREST-01: re-enable after enrollment
4. [DEPLOY]   VPS-NUCLEUS + DNS cutover → sovereign public site
5. [CONVERGE] Pattern hardening (see addendum below)
```

---

## ADDENDUM: Convergence Cleanup — Pattern Hardening

**Context**: Sovereign CI (Wave 133a) built all 30 ecobins but exposed
pattern divergences across primals. grapheneGate NUCLEUS deploy exposed
Android socket gaps. These are P2/P3 cleanup items — the ecosystem works,
but these divergences create CI friction and block 13/13 mobile. Fixing
them hardens the patterns so every primal is interchangeable in the pipeline.

**The standard every primal must meet**:

```
1. BUILDABLE:  cargo build --release --target $TRIPLE --bin $PRIMAL_LOWERCASE
               (no --package flag, no special linker deps)
2. RUNNABLE:   PRIMAL_BIND_MODE=tcp_only → starts on TCP, no UDS attempt
               (required for Android/grapheneGate)
3. TOOLCHAIN:  rust-toolchain.toml present (can be "stable" — just explicit)
4. CONFIG:     .cargo/config.toml inherits ecosystem defaults unless documented exception
```

**Lagging primals and what each needs**:

| Primal | Issue | What to do | Pattern to follow |
|--------|-------|------------|-------------------|
| **skunkBat** | CI-DIV-02: `--bin skunkbat` fails without `--package skunk-bat-server` | Add `default-members = ["crates/skunk-bat-server"]` to workspace `Cargo.toml` | biomeOS `f77886d1` — same fix, same pattern |
| **nestGate** | CI-DIV-03: `.cargo/config.toml` requires `ld.lld` (12 other primals use `gcc`) | Document exception with rationale (gcc CRT segfaults) OR re-test with current gcc | If exception: add `# EXCEPTION: ld.lld required — see CI-DIV-03` comment block |
| **nestGate** | NESTGATE-ANDROID-01: UDS fatal on Pixel 8a | Honor `PRIMAL_BIND_MODE=tcp_only` — skip UDS bind, use TCP | 11 primals already do this successfully on grapheneGate |
| **coralReef** | CORALREEF-ANDROID-01: UDS fatal on Pixel 8a | Honor `PRIMAL_BIND_MODE=tcp_only` — skip UDS bind, use TCP | Same as nestGate — these are the only 2 of 13 that fail |
| **sweetGrass** | CI-DIV-06: aarch64 binary 101% of x86 size (only primal where arm > x86) | Investigate `cfg(target_arch)` in deps — may have x86-only code compiled unconditionally on arm | All other primals are 75-92% — sweetGrass is the outlier |

**Ecosystem-wide (P3 — all primals, no rush)**:

| Issue | What | Current state |
|-------|------|---------------|
| CI-DIV-04 | 13/14 primals have project-level `.cargo/config.toml` (8-135 lines) | Standardize a shared template; inherit unless documented exception |
| CI-DIV-05 | Rust toolchain pinning: bearDog=1.93, songBird=1.94, nestGate=1.94.1, 5="stable", 5=none | Pick one strategy: either all pin explicit version or all use "stable" |

**When this cleanup is done**:
- Sovereign CI builds all 30 ecobins with zero manual workarounds
- 13/13 primals run on grapheneGate (Android)
- Every primal meets the 4-point standard above
- CI pipeline is a single loop: `for primal in *; do cargo build --bin $primal; done`

**Priority**: P2 for skunkBat/nestGate/coralReef (blocking CI automation + 13/13 mobile).
P3 for sweetGrass/ecosystem-wide (hygiene, not blocking).

After fixes: `git push origin main && git push forgejo main`

---

*Wave 133b — Pattern hardening. Bring lagging primals to par. The ecosystem works — make it uniform.*
