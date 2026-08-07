# ecoPrimals Ecosystem Blurb — Wave 157a Stage 2 Depot Rebuild

**Date**: Aug 7, 2026 PM | **Wave**: 157a | **From**: eastGate overwatch → sporeGate depot ops
**Posture**: **STAGE 2 DEPOT REBUILT. GOLGI CURRENT.** biomeOS `680e83f` (riboCipher pool + auto-transition + TOML caps) compiled and deployed. Musl: 17/17. Windows: 14/15. 12/13 ALIVE.

---

## WHAT CHANGED — biomeOS Stage 2 (`52f7f9e → 680e83f`)

3 commits, 862 insertions:

| Feature | Files | Impact |
|---------|-------|--------|
| **riboCipher dual-lane pooling** | `biomeos-core/src/ipc/pool.rs` (+105) | Pool handles raw JSON-RPC and `0xEC`-prefixed sockets |
| **Bootstrap→Coordinated auto-transition** | `neural_api_server/server_lifecycle.rs` (+49) | Probes every 15s, auto-transitions when Tower comes online |
| **TOML capability translations** | `capability_translation/toml_loader.rs` (+193) | Runtime capability evolution without recompiling biomeOS |
| **N1 forwarding fix (G67)** | `neural_router/forwarding.rs` (+103) | Pool path for `capability.call`, outer timeout for escalation |

Binary size: 16.2MB → 21.2MB (musl). Stage 2 routing infra is in the binary.

---

## BUILDER PATTERN — blueGate PRIMARY

| Builder | Role | This Session |
|---------|------|--------------|
| **blueGate** | Primary Windows | All 15 Windows builds dispatched. 14/15 success. |
| **sporeGate** | Lean musl | biomeOS only (clean rebuild: `cargo clean -p biomeos-unibin` → 2m 10s). All other G66 musl bins unchanged. |

---

## DEPOT STATUS ON GOLGI

### Musl — 17/17 ALL CURRENT

| Binary | Size | Built |
|--------|------|-------|
| biomeOS | 21MB | Aug 7 16:50 (Stage 2 `680e83f`) |
| petalTongue | 30MB | Aug 7 12:37 |
| songBird | 19MB | Aug 7 01:37 |
| membrane | 17MB | Aug 7 01:29 |
| toadStool | 14MB | Aug 7 12:53 |
| barracuda | 12MB | Aug 7 01:57 |
| + 11 more | — | Aug 7 |

### Windows — 14/15

| Status | Primals |
|--------|---------|
| **STAGE 2 BUILT** | barraCuda, bearDog, bingoCube, biomeOS (19.8MB, 3m 22s fresh build), coralReef, loamSpine, nestGate, petalTongue, rhizoCrypt, skunkBat, songBird, sourDough, sweetGrass, toadStool |
| **FAILED** | squirrel (cross-arch `typenum`/`futures` — eastGate team) |

---

## HEALTH — 12/13

12 ALIVE on sporeGate NUCLEUS. biomeOS running `4.56.0` — needs restart with `4.57.0` (Stage 2) binary.

| Issue | Root Cause | Resolution |
|-------|-----------|------------|
| toadStool `Permission denied` | B1/B2 socket permissions | Pending biomeGate deploy |
| biomeOS version `4.56.0` | Running pre-Stage-2 binary | Restart `membrane-biomeos` with depot binary |

---

## DEPLOYMENT SEQUENCE (from blurb)

1. ~~Depot rebuild with Stage 2 biomeOS~~ — **DONE**
2. **N2-N5 verification on eastGate** — primalSpring team (test script ready)
3. **Deploy across all 6 NUCLEUS gates** — gate teams pull from golgi depot
4. **Activate springs** — hotSpring, tideGlass, esotericWebb on stable substrate

---

## DIVERGENCES

| ID | Issue | Owner | Severity |
|----|-------|-------|----------|
| DIV-1 | squirrel Windows compile (typenum/futures) | eastGate team | P3 — not blocking deployment |
| DIV-2 | toadStool socket permissions (B1/B2) | biomeGate | P2 — health check blocked |
| DIV-3 | biomeOS local version 4.56 vs depot 4.57 | sporeGate ops | P2 — restart needed |
| DIV-7 | `plasmid.harvest` exit code unreliable | cellMembrane | P3 — known, verify manually |

---

## G68 PLATFORM SUBSTRATE STATUS

| Primal | L1 (Links) | L2 (Perms) | L3 (Device) | Status |
|--------|-----------|-----------|------------|--------|
| sourDough | reference | reference | reference | SHIPPED |
| **nestGate** | **DONE** | **DONE** | **DONE** | **SHIPPED** |
| others | pending | pending | pending | — |

---

*Wave 157a — Stage 2 depot rebuilt. biomeOS `680e83f` (riboCipher pool, auto-transition, TOML caps) compiled fresh: musl 21MB, Windows 20MB. Golgi depot: musl 17/17, Windows 14/15. sporeGate 12/13 ALIVE. nestGate ships G68 platform substrate (L1/L2/L3). N2-N5 verification next, then gate deployment, then springs activation.*
