# ecoPrimals Ecosystem Blurb — Deployment Wave

**Date**: Aug 6, 2026 EVE | **Wave**: 156r | **From**: eastGate overwatch → sporeGate depot rebuild
**Posture**: **DEPOT REBUILT. GOLGI UPDATED. DEPLOY.** 15/15 G65 musl binaries on golgi. sporeGate local: 12/13 ALIVE. blueGate Windows builds in progress.

---

## sporeGate EXECUTION COMPLETE

| Step | Status |
|------|--------|
| Pull all 15 primals to G65 HEADs | **DONE** — all verified against blurb |
| Pull all 15 on blueGate | **DONE** |
| blueGate Windows builds (15) | **RUNNING** (sequential) |
| sporeGate musl harvest (15) | **DONE** — 15/15 built |
| Deploy to sporeGate NUCLEUS | **DONE** — 14/14 system + user petalTongue |
| petalTongue G65 health evolution | **DONE** — BTSP+plain fallback, 12/13 alive |
| Push depot to golgi | **DONE** — 15/15 fresh musl binaries |
| petalTongue commit `6c47ae0` | **PUSHED** to Forgejo |

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

G65 protocol negotiation is NOT uniform. Three categories emerged:

1. **BTSP Required**: sweetgrass, biomeos — reject plain JSON, require `0xEC 0x01` signal
2. **Full BTSP Handshake**: beardog — requires ClientHello, `-default.sock` fallback
3. **Plain JSON-RPC**: coralReef, barracuda, squirrel — accept `{` directly

petalTongue health module now handles all three: BTSP first, plain fallback.

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

*Wave 156r — sporeGate depot rebuild COMPLETE. 15/15 G65 musl on golgi. 12/13 alive on sporeGate. Gate teams: deploy.*
