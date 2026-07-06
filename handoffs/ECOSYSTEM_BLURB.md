# ecoPrimals Ecosystem Blurb — Wave 133a (afternoon refresh)

**Date**: Jul 6, 2026 15:13 EDT | **Wave**: 133a | **From**: eastGate overwatch
**Posture**: **ENMESH + HARDEN + VALIDATE** — 30/30 ecobins in pepti. grapheneGate 12/13 LIVE. CI divergences surfaced. sporePrint evolving. DNS cutover path mapped.

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
  ⚠️ primalSpring: 1093 pass, 4 fail (SHADER_F64 manifest gap), 2 ignored

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

### primalSpring team (parallel tab)

| ID | Priority | Item | Status |
|----|----------|------|--------|
| PS-F64-01 | **P1** | Add `SHADER_F64` / f64 precision to ecosystem manifest | Causes 4 test failures (shader pipeline + registry gate) |
| PS-WAN-01 | P2 | Push 124th scenario to origin (ahead=2 after rebase reconciliation) | Local only |

**Test suite**: 1093 pass, 4 fail, 2 ignored. Was 1096/0 — regression is manifest gap, not code.

---

### biomeOS team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| ~~CI-DIV-01~~ | ~~P2~~ | ~~`--package biomeos-unibin` needed~~ | **RESOLVED** (`f77886d1`) |

**Zero remaining items.** STANDBY.

---

### skunkBat team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| CI-DIV-02 | P2 | `cargo build --bin skunkbat` fails without `--package skunk-bat-server` | Fix: add `skunk-bat-server` to `default-members` in workspace Cargo.toml |

---

### nestGate team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| CI-DIV-03 | P2 | `.cargo/config.toml` requires `ld.lld` — diverges from ecosystem | Fix: converge on ecosystem linker strategy or document exception |
| NESTGATE-ANDROID-01 | P2 | UDS fatal on Android (grapheneGate) | Needs Android socket adaptation |

---

### coralReef team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| CORALREEF-ANDROID-01 | P2 | UDS fatal on Android (grapheneGate) | Needs Android socket adaptation |

---

### sweetGrass team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| CI-DIV-06 | P3 | aarch64 binary larger than x86 (101% ratio — only primal where this happens) | Investigate conditional compilation in deps |

---

### cellMembrane / sporeGate team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| CI-DIV-07 | **P1** | `temporal.cascade` doesn't commit freshness updates — root cause of golgi HEAD staleness | Fix `publish_freshness()`: re-read HEADs, bump timestamp, commit + push |
| CI-DIV-08 | P2 | ecosystem_manifest.toml has no schema validation — caused manifest parse failures | Pre-commit hook or CI validation |
| SP-DIV-04 | P2 | `temporal.cascade` doesn't rebuild Zola — VPS serves stale sporePrint | Post-cascade hook for `zola build` |
| VPS-NUCLEUS | P2 | Deploy minimal NUCLEUS on golgi for sporePrint serving (petalTongue + NestGate + songBird + bearDog, ~70MB) | Handoff filed: `EASTGATE_WAVE133_SPOREPRINT_VPS_NUCLEUS.md` |

---

### sporePrint team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| SP-DIV-01 | **P1** | `primals.eco` DNS still points to GitHub Pages — not sovereign | Blocked on VPS NUCLEUS + bearDog ACME |
| SP-DIV-02 | P2 | Dual-push required (origin + forgejo) — workaround until DNS cutover | Operational friction |
| SP-DIV-05 | P3 | `.github/workflows/deploy.yml` still load-bearing — archive after cutover | Cleanup |
| — | — | Content evolution | ACTIVE — 226 pages, 254 tests, SVG viz, living systems pages |

**Workaround**: continue `git push origin main && git push forgejo main` until DNS cutover.

---

### flockGate team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| WAN-DISPATCH-01 | **P1** | Validate cross-gate `capability.call` via golgi relay | Not yet tested. primalSpring scenario ready (124th). |
| WAN-LATENCY-01 | P2 | Characterize cross-gate RTT (p50/p95/p99) | After dispatch validation |

---

### eastGate hardware team

| ID | Priority | Item | Status |
|----|----------|------|--------|
| STRAND-SSH-01 | **P1** | strandGate SSH key deploy (house 2, .103) | Physical access required |
| DARK-FOREST-01 | P2 | Re-enable dark-forest after 3+ LAN peers have bearDog | Blocked on STRAND-SSH-01 |
| GRAPHENE-FULL-01 | P2 | grapheneGate full NUCLEUS — nestGate + coralReef adaptation | 12/13 running, 2 primals need Android UDS fix |
| FLEET-ENROLL | P3 | northGate/westGate/swiftGate/kinGate enrollment | As hardware allows |
| LAUNCHER-02 | P3 | nucleus_launcher: skip failed primals, continue with available | Filed in grapheneGate AAR |

---

### All primal teams (P3 — ecosystem convergence, no rush)

| ID | Priority | Item |
|----|----------|------|
| CI-DIV-04 | P3 | 13/14 primals have project-level `.cargo/config.toml` — standardize shared template |
| CI-DIV-05 | P3 | Rust toolchain pinning inconsistent (1.93→1.94.1→stable→none) — single strategy |

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
✅ grapheneGate 12/13 LIVE
✅ biomeOS CI-DIV-01 RESOLVED
✅ golgi disk recovered + HEAD metadata published
✅ sporePrint sovereignty path mapped

ACTIVE — ENMESH + HARDEN + VALIDATE:
1. [CODE]     PS-F64-01: SHADER_F64 manifest gap → 4 tests back to green
2. [CODE]     CI-DIV-07: cascade freshness publishing → automated HEAD updates
3. [GATE]     STRAND-SSH-01: strandGate enrollment → 3rd LAN peer
4. [GATE]     WAN-DISPATCH-01: flockGate cross-gate validation → WAN mesh proven
5. [GATE]     DARK-FOREST-01: re-enable after enrollment → security posture
6. [DEPLOY]   VPS-NUCLEUS: sporePrint on golgi → sovereignty cutover path
7. [DEPLOY]   SP-DIV-01: DNS cutover (primals.eco → VPS) → sovereign public site

CONVERGENCE (P2-P3 — as teams have cycles):
  - CI-DIV-02: skunkBat default-members fix
  - CI-DIV-03: nestGate linker convergence
  - NESTGATE-ANDROID-01 + CORALREEF-ANDROID-01: Android UDS adaptation
  - CI-DIV-04/05: ecosystem-wide config + toolchain standardization
```

---

*Wave 133a — 30/30 ecobins deployed. 12/13 mobile. CI divergences surfacing and resolving. Sovereignty cutover path clear. Enmesh, harden, validate.*
