# ecoPrimals Ecosystem Blurb — Deployment Wave

**Date**: Aug 6, 2026 EVE | **Wave**: 156r | **From**: eastGate overwatch → sporeGate depot rebuild
**Posture**: **DEPOT REBUILT. GOLGI UPDATED. DEPLOY.** 16/16 G65 binaries on golgi (15 primals + cellMembrane). sporeGate local: 12/13 ALIVE. blueGate Windows builds in progress.

---

## sporeGate EXECUTION COMPLETE

| Step | Status |
|------|--------|
| Pull all 15 primals to G65 HEADs | **DONE** — all verified against blurb |
| cellMembrane f6f1e62 | **BUILT + PUSHED** (16.8MB) |
| sporeGate musl harvest (15) | **DONE** — 15/15 built |
| Deploy to sporeGate NUCLEUS | **DONE** — 14/14 system + user petalTongue |
| petalTongue G65 health evolution | **DONE** — BTSP+plain fallback, 12/13 alive |
| Push depot to golgi | **DONE** — 16/16 fresh binaries (15 primals + membrane) |
| petalTongue commit `6c47ae0` | **PUSHED** — G65-aware health with BTSP+plain fallback |
| blueGate Windows builds (15) | **RUNNING** (re-dispatched after session crash) |

---

## GOLGI DEPOT — ALL MUSL BINARIES CURRENT

| Binary | Size | Date |
|--------|------|------|
| barracuda | 11.0M | Aug 6 |
| beardog | 7.8M | Aug 6 |
| bingocube | 10.5M | Aug 6 |
| biomeos | 15.6M | Aug 6 |
| coralreef | 8.6M | Aug 6 |
| loamspine | 4.8M | Aug 6 |
| **membrane** | **16.1M** | **Aug 6** |
| nestgate | 8.5M | Aug 6 |
| petaltongue | 28.3M | Aug 6 |
| rhizocrypt | 7.6M | Aug 6 |
| skunkbat | 3.2M | Aug 6 |
| songbird | 17.5M | Aug 6 |
| sourdough | 3.0M | Aug 6 |
| squirrel | 8.0M | Aug 6 |
| sweetgrass | 8.1M | Aug 6 |
| toadstool | 11.6M | Aug 6 |

---

## HEALTH — 12/13 ALIVE

| Primal | Status | Notes |
|--------|--------|-------|
| barracuda | ALIVE | G65 plain JSON-RPC |
| beardog | ALIVE (v0.9.0) | beardog-default.sock |
| biomeos | ALIVE (v4.56.0) | BTSP signal |
| coralreef | ALIVE | **G65 EVOLUTION** — now accepts plain JSON-RPC |
| loamspine | ALIVE | |
| nestgate | ALIVE | |
| petaltongue | ALIVE | |
| rhizocrypt | ALIVE (v0.14.17) | |
| skunkbat | ALIVE | Family socket /run/user/0/biomeos/ |
| songbird | ALIVE | |
| squirrel | ALIVE (v0.1.0) | |
| sweetgrass | ALIVE | BTSP signal enforced |
| toadstool | ERROR | Socket `srw-------` — B1/B2 perm fix needed |

---

## DIVERGENCES — G65 TRANSPORT SIGNAL

G65 protocol negotiation is NOT uniform. Three categories:

1. **BTSP Required**: sweetgrass, biomeos — reject plain JSON, require `0xEC 0x01` signal
2. **Full BTSP Handshake**: beardog — requires ClientHello, `-default.sock` fallback
3. **Plain JSON-RPC**: coralReef, barracuda, squirrel — accept `{` directly

petalTongue health module handles all three: BTSP first, plain fallback.

---

## GATE DEPLOYMENT — READY

golgi depot updated Aug 6. Gate teams: pull and deploy.

| Gate | Action |
|------|--------|
| **ironGate** | Deploy. Activate downstream springs. |
| **westGate** | Deploy. Enable nestGate TCP (O5). |
| **blueGate** | Deploy latest bins (Windows builds completing). |
| **southGate** | Re-deploy cephalization baseline. |
| **strandGate** | Deploy when thermalization batch completes. |

---

*Wave 156r — sporeGate depot rebuild COMPLETE. 16/16 G65 binaries on golgi. 12/13 alive on sporeGate. Gate teams: deploy.*
