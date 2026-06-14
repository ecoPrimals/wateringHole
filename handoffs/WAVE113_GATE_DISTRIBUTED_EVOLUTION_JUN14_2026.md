# Wave 113 — Remaining Work

**Date**: 2026-06-14 (rescoped after NUCLEUS interaction audit)  
**From**: eastGate overwatch  
**Progress**: 3/6 exit criteria met (REJECT, federation, rootpulse)  
**New Debt**: 5 categories of primal interaction gaps exposed by VPS audit  
**Critical Path**: Primal teams implement health + riboCipher → guideStone amendment

---

## Wave 113 Shipped (this cycle)

cellMembrane `1775b64`+`83ad975`:
- ServerContract enum (per-primal CLI, replaces broken template units)
- riboCipher default → REJECT (client-side, graduated enforcement)
- Profile-aware health (Tower=2/2, Nest=7/7, Full=13/13)
- Gate identity file (`/etc/membrane/gate_identity`)
- neuralAPI-routed probes with UDS fallback
- `temporal.cascade.stress --cycles N`
- Freshness single-writer policy (golgiBody only publishes)
- BufReader NDJSON fix (prevents probe hangs)
- flockGate + eastGate enrolled as VPS peers (2/2 reachable!)
- rootpulse graph execution WORKING through neuralAPI

---

## NEW: NUCLEUS Primal Interaction Debt (5 gap categories)

Full audit of 13 VPS primals reveals deep interoperability gaps.

### Gap 1: riboCipher Signal Acceptance (1/13)

| Response | Primals |
|----------|---------|
| ✅ Accepts signal | songbird |
| ❌ Rejects (BTSP error) | beardog, nestgate, rhizocrypt |
| ❌ No response (timeout) | skunkbat, sweetgrass, loamspine, toadstool, barracuda, squirrel, petaltongue |
| ❌ HTTP 400 | biomeos |
| ❌ Parse error | coralreef |

**Action**: ALL primal teams — accept `[0xEC, 0x01]` as prefix, ignore 2 bytes, parse remainder as JSON.

### Gap 2: Health Method (8/13 respond, 4 missing, 1 silent)

| Response | Primals |
|----------|---------|
| ✅ Healthy response | songbird, nestgate, sweetgrass, rhizocrypt, barracuda, biomeos, petaltongue, beardog |
| ⚠️ Method not found (-32601) | skunkbat, loamspine, coralreef, squirrel |
| ❌ Silent (no response) | toadstool |

**Action**: ALL primals implement `health` method: `{status, primal, version}`. toadStool: fix silent socket.

### Gap 3: neuralAPI Hollow (0 registered capabilities)

- Live and functional for graph execution (rootpulse proven)
- BUT: 0 primals registered, 0 capabilities routed
- biomeOS in "Bootstrap" mode with no primal discovery
- `capability.call` always falls through to direct UDS

**Action**: biomeOS team — implement primal auto-registration so orchestration layer becomes operational.

### Gap 4: Undocumented Sockets (28 total)

bearDog: 5 extra (btsp, crypto, ed25519, x25519, security)  
barracuda: 2 extra (compute-tarpc)  
loamspine: 2 extra (ledger, permanence)  
sweetgrass: 1 extra (provenance)  
biomeOS: 2 extra (neural-api, ai)  
petaltongue: 2 extra (visualization)

**Action**: guideStone amendment — document multi-socket primals and their purposes.

### Gap 5: Service Integration Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| bearDog BTSP-locked socket | Health probes can't reach plain JSON-RPC | Expose `--health-socket` or beardog-default.sock |
| toadStool silent | Connection accepted, no response ever | Protocol violation — fix |
| biomeOS dual-socket confusion | cellMembrane probes biomeos.sock (HTTP) not neural-api.sock | Probe correct socket |
| songBird self-connect loop | VPS songbird reconnects to own :7700 every 30s | Don't self-target in reconnect |
| songBird federation not signalled | TCP outbound on :7700 doesn't send riboCipher | Signal on federation path |
| membrane-bridge-biomeos | Deprecated socat UDS→TCP pattern, broken pipe | Remove |

---

## Remaining Per-Gate Work (post-audit)

### cellMembrane / ironGate — P1

| Task | Status |
|------|--------|
| Probe biomeOS on neural-api.sock (not biomeos.sock) | TODO |
| Accept -32601 as "alive" in S4 probe | TODO |
| Remove membrane-bridge-biomeos (deprecated socat) | TODO |
| aarch64 depot harvest for grapheneGate | TODO |

### Primal Teams (guideStone evolution) — P1

| Primal | Required |
|--------|----------|
| ALL | Implement `health` JSON-RPC method |
| ALL | Accept riboCipher `[0xEC, 0x01]` prefix |
| bearDog | Expose plaintext health socket |
| toadStool | Fix silent socket |
| biomeOS | Primal auto-registration in neuralAPI |
| songBird | riboCipher on federation TCP + fix self-connect |
| coralreef | Don't parse-error riboCipher prefix |

### southGate — P2

| Task | Status |
|------|--------|
| DEPLOY-THEN-STALE simulation | ⬜ |

### grapheneGate — P3

| Task | Status |
|------|--------|
| Cross-arch deploy | Blocked until aarch64 depot harvested |
| songBird `--state-dir` | Blocked on songBird evolution |

### ops (physical only)

| Task | Status |
|------|--------|
| NUC placement + power + cable | ⬜ |
| westGate power on | ⬜ |

---

## Exit Criteria (updated)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | riboCipher REJECT deployed | ✅ DONE (client-side + hotSpring + strandGate) |
| 2 | flockGate persistent federation | ✅ DONE (2 peers, 2 reachable — flockGate+eastGate enrolled) |
| 3 | DEPLOY-THEN-STALE validated | ⬜ |
| 4 | New hardware gate enrolled | ⬜ (ops) |
| 5 | rootpulse real commit chain | ✅ DONE (graph execution working via neuralAPI) |
| 6 | Gate-clearing issues resolved | ✅ DONE (ServerContract, identity, profile-aware) |

**4/6 MET.** Remaining: DEPLOY-THEN-STALE (southGate) + hardware (ops).

---

## Evolution Debt (both solutions)

| Problem | Short-term | Robust Solution |
|---------|-----------|-----------------|
| **riboCipher 1/13 acceptance** | Document per-primal signal handling | guideStone amendment: MANDATORY accept |
| **health 8/13** | cellMembrane accepts -32601 as alive | guideStone: MANDATORY health method |
| **neuralAPI hollow** | Direct UDS fallback works | biomeOS auto-registration of capabilities |
| **28 undocumented sockets** | cellMembrane probes known sockets | guideStone: socket manifest per primal |
| **bearDog BTSP-locked** | Skip health probe for beardog | beardog-default.sock or --health-socket |
| **songBird self-connect** | Filter self from peer list | Fix reconnect target list |
| **Freshness divergence** | ✅ Single-writer shipped | mesh.publish (long-term) |

---

**Wave 113 sprint: 4/6 exit criteria met. Remaining work is southGate STALE sim + physical hardware. New debt is primal interaction quality — needs guideStone amendment and per-team evolution tasks.**
