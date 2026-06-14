# Wave 113 — Active Tasks

**Status**: 4/6 exit criteria met | **Remaining**: STALE sim + hardware  
**New priority**: NUCLEUS primal interaction quality (5 gap categories from VPS audit)

---

## cellMembrane / ironGate — P1

**Remaining membrane tasks:**
- Probe biomeOS on `neural-api.sock` (not `biomeos.sock`)
- Accept `-32601` (method_not_found) as "alive" in S4 probe
- Remove `membrane-bridge-biomeos` (deprecated socat pattern)
- `plasmid.harvest --targets beardog,songbird,skunkbat --arch aarch64` from HEAD
- Route depot rebuilds through neuralAPI graph (pepti orchestration)

**southGate task (owns):**
- DEPLOY-THEN-STALE: Skip 1-2 cascade cycles on southGate, verify `health.audit --mesh` detects skew

---

## bearDog — P1

- [ ] Accept riboCipher `[0xEC, 0x01]` prefix (ignore 2 bytes, parse JSON)
- [ ] Implement `health` JSON-RPC method → `{status, primal: "beardog", version}`
- [ ] Expose plaintext health socket (`--health-socket` or `beardog-default.sock`)

BTSP-locked main socket blocks plain JSON-RPC probes. cellMembrane can't health-check without BTSP handshake.

---

## songBird — P1

- [ ] Accept riboCipher `[0xEC, 0x01]` prefix on UDS
- [ ] Send riboCipher signal on federation TCP outbound (:7700)
- [ ] Fix self-connect loop (VPS reconnects to own :7700 every 30s)
- [ ] Add `--state-dir` / `SONGBIRD_STATE_DIR` for PID/state placement (GrapheneOS read-only FS)

---

## toadStool — P1

- [ ] Fix silent socket (accepts connection, produces no response — protocol violation)
- [ ] Accept riboCipher prefix
- [ ] Implement `health` method

---

## biomeOS — P1

- [ ] Accept riboCipher prefix on `neural-api.sock` (currently returns HTTP 400)
- [ ] Implement primal auto-registration so `capability.call` routing works (0 registered currently)
- [ ] Transition from Bootstrap mode to operational orchestration

neuralAPI is live, graph execution works (rootpulse proven), but 0 primals registered = hollow orchestration layer.

---

## skunkBat, loamSpine, coralReef, squirrel — P2

- [ ] Implement `health` JSON-RPC method (currently -32601 method_not_found)
- [ ] Accept riboCipher `[0xEC, 0x01]` prefix

---

## nestGate, sweetGrass, rhizoCrypt, barracuda, petalTongue — P2

- [ ] Accept riboCipher prefix (currently reject/timeout)

Already respond to raw JSON-RPC health — just need signal acceptance.

---

## hotSpring / strandGate — DONE

riboCipher REJECT shipped. Legacy removed. No remaining Wave 113 tasks.

---

## grapheneGate — P3

- Cross-arch deploy blocked until aarch64 depot harvested
- songBird `--state-dir` needed for GrapheneOS

---

## ops (physical only)

- NUC: placement, power, network cable
- westGate: power on (i7-4771 + 76TB ZFS)

Once networked → cellMembrane `gate.bootstrap`.

---

## guideStone Amendments Needed

| Amendment | Scope |
|-----------|-------|
| `health` method MANDATORY for all primals | `{status, primal, version}` minimum |
| riboCipher signal handling MANDATORY on UDS | Accept `[0xEC, 0x01]` prefix, ignore, parse JSON |
| Socket manifest per primal | Document all exposed sockets and purposes |
| neuralAPI capability registration | Standard for primals to register with orchestration |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | riboCipher REJECT | ✅ |
| 2 | Persistent federation | ✅ |
| 3 | DEPLOY-THEN-STALE | ⬜ southGate |
| 4 | Hardware enrollment | ⬜ ops |
| 5 | rootpulse graph execution | ✅ |
| 6 | Gate-clearing issues | ✅ |

**4/6. Close when southGate STALE sim validated + any hardware gate bootstrapped.**
