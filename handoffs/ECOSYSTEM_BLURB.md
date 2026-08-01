# ecoPrimals Ecosystem Blurb — Wave 155n Checkpoint (Updated)

**Date**: Jul 31, 2026 20:10 EDT | **Wave**: 155n | **From**: eastGate overwatch
**Posture**: **ZERO P0/P1/P2. J12 sub-builder WIRED (sporeGate dispatch) + PROVEN (blueGate local build). SSH key enrollment is the last thread. Springs+gardens gate is opening.**

---

## WHERE WE ARE

All three blurbed teams delivered. The runway to springs+gardens is nearly clear.

```
CHECKPOINT STATUS — ALL 4 MUST-CLEAR ITEMS RESOLVED:
  ✓ Item 1: G22 — COMPLETE + VALIDATED (single-process, no socket evaporation)
  ✓ Item 2: J12 — WIRED (sporeGate foreman dispatch) + PROVEN (blueGate local build).
            Remaining: SSH key enrollment on blueGate, then live E2E test.
  ✓ Item 3: sporePrint — LIVE + AUTO-PUBLISH WIRED (Forgejo hook)
  ✓ Item 4: J18 — CODE SHIPPED (882ad09). Gate validation pending.
```

**What changed since last cascade:**

| Team | Delivery | Impact |
|------|----------|--------|
| **biomeOS** | G22 COMPLETE (`b82f0925`): api + neural-api → dual-protocol in both modes. `neural-api` subcommand deprecated. | Springs can build against ANY biomeOS entry point. Socket evaporation on restart → resolved by single-process. |
| **cellMembrane** | J18 gate coupling FIX (`882ad09`): `env_or()` migration, gate-name identity bridge. User-space deploy paths resolve correctly. | southGate, steamGate can bootstrap without `/etc/environment` jelly strings. |
| **sporeGate** | sporePrint published + auto-publish hook wired (D7). GNU depot COMPLETE (46 bins). Sovereign CI cloning fixed (D5). **G22 single-process VALIDATED** (D1+D6 resolved). | 5/10 divergences resolved this wave. |
| **westGate** | biomeOS v4.56 G22-complete deployed. Prov 7/7 pass #8. 30/30 sockets stable. 835 caps. | First gate with full G22 convergence validated. |
| **blueGate** | Platform detection P2 CONFIRMED FIXED. biomeOS v4.56 deployed. 13/13 NUCLEUS. Target triple: `x86_64-pc-windows-gnu`. | J12 at platform layer is DONE. Remaining: IPC transport TCP fallback. |

---

## REMAINING BEFORE SPRINGS+GARDENS

### MUST CLEAR

| # | Item | Owner | Status |
|---|------|-------|--------|
| ~~1~~ | ~~G22 steps 3-5~~ | ~~biomeOS~~ | **COMPLETE + VALIDATED** — single-process on sporeGate + westGate. |
| ~~2~~ | ~~J12 sub-builder~~ | ~~sporeGate + blueGate~~ | **WIRED + PROVEN.** sporeGate: foreman dispatch in sovereign CI, dry-run validated. blueGate: local build proof (skunkBat 2.6 MB, matches depot), IPC caps registered. **Remaining**: SSH key enrollment on blueGate → live E2E test. |
| ~~3~~ | ~~sporePrint publish~~ | ~~sporeGate~~ | **CLEARED + AUTO-PUBLISH** — Forgejo hook wired. |
| ~~4~~ | ~~J18 gate coupling~~ | ~~cellMembrane~~ | **CODE SHIPPED** (`882ad09`). Gate validation pending. |

**All 4 MUST-CLEAR items are resolved at the code level.** J12 needs SSH key enrollment (manual) then live E2E validation.

### SHOULD CLEAR (before fleet expansion)

| # | Item | Owner | Status |
|---|------|-------|--------|
| 5 | southGate NUCLEUS launch + J18 validation | eastGate | ENROLLED. Validates portability + bonding + J18 fix. |
| 6 | ironGate: esotericWebb from flockGate | eastGate | flockGate DOWN. |
| 7 | strandGate v4.56 redeploy | strandGate | Still on v4.51. Needs G22 convergence. |
| ~~8~~ | ~~sporePrint auto-publish hook~~ | ~~sporeGate~~ | **RESOLVED** (D7) — Forgejo post-receive hook wired. |
| 9 | checksums.toml automation | sporeGate/cellMembrane | D3: `depot.seal` command. Manual format is error-prone. |
| ~~10~~ | ~~Sovereign CI source tree fix~~ | ~~sporeGate~~ | **RESOLVED** (D5) — root SSH key + fresh clone on trigger. |

### DIVERGENCES (10 documented by sporeGate)

| ID | Issue | Resolves With |
|----|-------|---------------|
| ~~D1~~ | ~~Socket evaporation on biomeOS restart~~ | **VALIDATED RESOLVED** (G22 single-process on sporeGate) |
| D2 | `/run/membrane` permission reset | **PARTIALLY RESOLVED** — group perms work. Needs biomeOS socket `0660` config. |
| D3 | checksums.toml format drift | `depot.seal` command codification (ops debt) |
| D4 | Candidate self-test probe fails | Lightweight version-check probe (biomeOS) |
| ~~D5~~ | ~~Sovereign CI source tree divergence~~ | **RESOLVED** — root SSH key registered on Forgejo, fresh clone on trigger |
| ~~D6~~ | ~~Dual-service architecture~~ | **VALIDATED RESOLVED** (G22 single-process on sporeGate) |
| ~~D7~~ | ~~sporePrint publish not automated~~ | **RESOLVED** — Forgejo post-receive hook wired |
| D8 | Neural API capability routing gaps | Primal capability registration (biomeOS) |
| D9 | `nucleus_launcher` GNU build missing | Extract from biomeOS workspace (low priority) |
| D10 | Zola warnings (4 lab pages) | Frontmatter fix (trivial) |

---

## GATE STATUS

| Gate | biomeOS | Status | Next |
|------|---------|--------|------|
| **westGate** | **v4.56 G22** | NUCLEUS. Prov 7/7 ×8. 30/30 sockets. ZFS 50.7 TB. | AlphaFold ingestion. |
| **sporeGate** | v4.56 G22 | 11/11 HEALTHY. 46 depot bins. G22 VALIDATED. Auto-publish. Sovereign CI fixed. J12 foreman dispatch WIRED. | SSH key enrollment on blueGate → live E2E. |
| **blueGate** | v4.56 | NUCLEUS 13/13. P2 FIXED. J12 local build PROVEN (skunkBat matches depot). 11 IPC services, 37 caps. `blueGate-builder` registered. | SSH key enrollment → receive sporeGate dispatch. |
| **strandGate** | v4.51 | NUCLEUS 12/12. RTX 3090. Node Atomic Landmark. | v4.56 redeploy. |
| **southGate** | — | VALIDATION GATE. HW enrolled. | NUCLEUS launch + J18 + bonding. |
| **ironGate** | — | Online. 14TB HDD. | esotericWebb + Tower. |
| **flockGate** | — | DOWN. | Recover or decommission. |

---

## TEAM POSTURE

### ACTIVE (one item left)

| Team | Delivery This Wave | Remaining |
|------|-------------------|-----------|
| **sporeGate** | sporePrint LIVE + GNU depot 46 bins | J12 sub-builder wire (sole MUST-CLEAR). |

### SHIPPED — READY FOR SPRINGS+GARDENS

| Team | What They Shipped | Springs+Gardens Role |
|------|-------------------|---------------------|
| **biomeOS** | G22 COMPLETE (v4.56, dual-protocol, 244 caps) | Foundation for ALL spring dispatch. |
| **cellMembrane** | J18 gate coupling fix + P2 platform fix | Gate provisioning + garden CI. |
| **squirrel** | 7,138 tests, 90.1% cov, 0 unsafe | G18: AI agent → biomeOS dispatch. |
| **petalTongue** | 6,605 tests, modern idiom pass | G19: Rendering pipeline. |
| **toadStool** | 9,193 tests | G19/G20: GPU compute dispatch. |
| **barraCuda** | 4,957 tests | G19: Tensor math. |
| **coralReef** | 3,527 tests | G20: Shader pipeline. |
| **nestGate** | 13,095+ tests | AlphaFold ingestion (50.7 TB ready). |

### STANDBY

| Team | Resume When |
|------|-------------|
| bearDog (14,019) | Garden-specific crypto |
| songBird (14,835) | J12 IPC wire (then standby) |
| sweetGrass / rhizoCrypt / loamSpine | Garden provenance wiring |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| MUST-CLEAR items | **4/4 CODE RESOLVED** — J12 needs SSH key enrollment + live E2E |
| Depot | **46 binaries** (16 musl + 15 gnu + 15 windows). BLAKE3 verified. |
| biomeOS | **v4.56 G22 COMPLETE** — dual-protocol, 244 caps, unified namespace |
| Gates current (v4.56) | westGate + sporeGate + blueGate. strandGate needs redeploy. |
| Provenance 7/7 | westGate pass #8 (consecutive across v4.50→v4.56) |
| Jelly strings | **10/11 KILLED** (J18 CODE SHIPPED). J12 WIRED (SSH key enrollment pending). |
| Divergences | **5/10 RESOLVED** (D1, D5, D6, D7 fully; D2 partially). 5 open: D3, D4, D8 (ops/biomeOS), D9, D10 (trivial). |
| Glacial goals | 23 tracked. G3+G4+G21+G22 COMPLETE. G23 NEW. |

---

## WHAT'S NEXT

```
IMMEDIATE (loose threads):
  J12 SSH key enrollment on blueGate (2 keys provided by sporeGate)
  J12 live E2E dispatch test (sporeGate → blueGate → depot push)
  J18 gate validation on southGate/steamGate

GATE OPS:
  strandGate v4.56 redeploy
  southGate NUCLEUS launch + J18 validation + bonding proof
  ironGate esotericWebb migration
  sporePrint auto-publish hook (D7)

SPRINGS+GARDENS (NEXT PHASE):
  G18: squirrel → biomeOS agent orchestration
  G19: petalTongue + Node Atomics live rendering pipeline
  G20: esotericWebb game engine on NUCLEUS (ironGate)
  Science: tideGlass Phase 0 → NF → pseudoSpore → JOSS
  Data: AlphaFold ~23 TB through westGate Nest Atomic CAS

GLACIAL:
  G6: bearDog public | G8: Plasmodium (southGate) | G11: steamGate
  G12: darwinGate | G13: iosGate | G17: Portability (southGate)
  G23: nestGate CAS-layer fractional replication
```

---

*Wave 155n — ZERO P0/P1/P2. ALL 4 MUST-CLEAR CODE RESOLVED. G22 VALIDATED.
J12 sub-builder WIRED (sporeGate) + PROVEN (blueGate). sporePrint auto-publish.
Sovereign CI fixed. 5/10 divergences resolved. 46 depot bins. Loose threads:
SSH key enrollment on blueGate, J18 gate validation, strandGate v4.56 redeploy.
Springs+gardens gate is opening. ~101K+ tests. 23 glacial goals (4 COMPLETE).*
