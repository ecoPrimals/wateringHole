# Wave 113 — Active Tasks

**Status**: 5/6 exit criteria met | VPS FULL GREEN (8/8) | **Only hardware enrollment remains**  
**Primal compliance**: riboCipher acceptance evolving (nestGate, biomeOS, sweetGrass shipped this wave)  
**Convergence**: DEPLOY-THEN-STALE proven, federation persistent, rootpulse operational

---

## cellMembrane / ironGate — P1/P2

| Task | Priority | Notes |
|------|----------|-------|
| **Diderm auto-reconciliation** | P1 | ALL gate commits must push to BOTH remotes. If second push fails (non-ff), auto-rebase + retry. This is the #1 source of overwatch manual intervention. |
| aarch64 depot harvest | P2 | `plasmid.harvest --targets beardog,songbird,skunkbat --arch aarch64` from HEAD — unblocks grapheneGate |
| Pepti build orchestration | P3 | Route depot rebuilds through neuralAPI graph |

### Diderm Divergence (chronic — needs systemic fix)

Every gate that commits to a shared repo (wateringHole) must push to **both** origin (GitHub) AND forgejo (VPS). Currently only freshness has single-writer policy. AARs, impulse syncs, and handoffs from different gates still create parallel histories requiring manual `--force-with-lease`.

**Required evolution:**
1. All `git push` operations in cellMembrane push to both remotes (not just freshness)
2. If second push fails non-ff: `fetch → rebase → push` automatically
3. Long-term: leader election OR mesh-native state (eliminate dual-remote coordination)

---

## bearDog — P1

- [ ] Accept riboCipher `[0xEC, 0x01]` prefix (ignore 2 bytes, parse JSON)
- [ ] Implement `health` JSON-RPC method → `{status, primal: "beardog", version}`
- [ ] Expose plaintext health socket (`--health-socket` or `beardog-default.sock`)

Main socket BTSP-locked. cellMembrane recognizes BTSP error as "alive + enforcing" (S4 workaround), but proper plaintext endpoint still needed.

---

## songBird — MOSTLY DONE

✅ Outbound riboCipher signalling (`4169c47a`)  
✅ Self-connect fix  
✅ `--state-dir` / `SONGBIRD_STATE_DIR`

Remaining:
- [ ] Accept riboCipher prefix on UDS (inbound — currently only outbound TCP is signalled)

---

## toadStool — P1

- [ ] Fix silent socket (accepts connection, produces no response)
- [ ] Accept riboCipher prefix
- [ ] Implement `health` method

---

## biomeOS — MOSTLY DONE

✅ riboCipher REJECT (`b10ad05f`)  
✅ Auto-registration (`topology.rescan`)

Remaining:
- [ ] Complete primal discovery in operational mode (currently Bootstrap → needs rescan trigger)

---

## nestGate — DONE

✅ riboCipher signal acceptance on all handlers (`17baed59`)

---

## sweetGrass — DONE

✅ v0.7.58 riboCipher REJECT

---

## hotSpring / strandGate — DONE

✅ riboCipher REJECT shipped. Legacy removed.

---

## skunkBat, loamSpine, coralReef, squirrel — P2

- [ ] Implement `health` JSON-RPC method (currently -32601)
- [ ] Accept riboCipher prefix

---

## rhizoCrypt, barracuda, petalTongue — P2

- [ ] Accept riboCipher prefix (currently reject/timeout)

Already respond to raw health — just need signal acceptance.

---

## grapheneGate — P3

- Cross-arch deploy blocked until aarch64 depot harvested
- songBird `--state-dir` ✅ shipped — can test once depot fresh

---

## ops (physical only)

- NUC: placement, power, network cable
- westGate: power on (i7-4771 + 76TB ZFS)

Once networked → cellMembrane `gate.bootstrap`. This is the only remaining exit criterion.

---

## guideStone Amendments (in progress)

| Amendment | Status |
|-----------|--------|
| `health` method MANDATORY | sporePrint validation shipped (`nucleus --probe`) |
| riboCipher signal MANDATORY on UDS | nestGate, biomeOS, sweetGrass compliant. Others in progress. |
| Socket manifest per primal | Documented in NUCLEUS audit AAR |
| neuralAPI capability registration | biomeOS auto-registration shipped |

---

## Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | riboCipher REJECT | ✅ |
| 2 | Persistent federation | ✅ |
| 3 | DEPLOY-THEN-STALE | ✅ |
| 4 | Hardware enrollment | ⬜ ops |
| 5 | rootpulse execution | ✅ |
| 6 | Gate-clearing issues | ✅ |

**5/6. Wave 113 closes when any hardware gate bootstrapped (ops-dependent).**
