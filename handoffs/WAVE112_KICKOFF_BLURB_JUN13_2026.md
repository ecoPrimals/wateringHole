# Wave 112 — Remaining Work

**Date**: 2026-06-13 (updated Jun 13 cascade)  
**From**: eastGate overwatch  
**Closes**: Wave 111 (code-complete, 9/9 riboCipher converged)  
**Opens**: Wave 112 (operational convergence + riboCipher deprecation escalation)

---

## Context

Wave 111 closed: 9/9 riboCipher converged, 14/16 Stream 6 divergence shipped, ironGate NUCLEUS 13/13, federation validated. Wave 112 escalates the deprecation clock and proves operational self-healing.

---

## Wave 112 Goals

### Theme: Operational Convergence + Deprecation Escalation

Wave 112 shifts from code delivery to operational validation. The code is done — now the infrastructure must converge.

### 1. riboCipher Deprecation Escalation (ALL TEAMS)

**Wave 112 policy**: Unsignalled connections produce **ERROR** logs (was WARN in 111).

**SHIPPED (6/8):**
- cellMembrane: `922eb24` ✅
- bearDog: `cdcdff56f` ✅
- songBird: `acf20b6e` ✅
- strandGate/hotSpring: ✅ (acknowledged)
- sourDough: `28c0636` ✅
- primalSpring: N/A (no accept loop, hard-asserts signal) ✅

**PENDING (2/8):**
- **sweetGrass**: Currently at WARN in peek.rs — needs one-line escalation to ERROR
- **biomeOS**: Currently at DEBUG in neural_api_server/connection.rs — needs escalation to ERROR

No connections are rejected yet (that's Wave 113). The ERROR logs surface any remaining unsignalled callers.

### 2. VPS Rebuild (cellMembrane — P1)

Deploy `922eb24` (latest) to VPS. This:
- Stops junk Wave 109 auto-publish commits (race-condition fix from 082d77c)
- Enables riboCipher mito-tier + WARN→ERROR on WAN connections
- Includes health probe fix + plasmidBin resolution
- Triggers depot harvest cycle (fixes BLAKE3 mismatches)
- Unblocks cascade automation testing

**Status**: cellMembrane code shipped (`922eb24`). VPS deployment pending ops execution.

### 3. Cascade Validation (cellMembrane — P2)

After VPS rebuild:
- `temporal.cascade --with-restart` on eastGate, southGate, grapheneGate
- Run 2 full cascade cycles with zero manual intervention
- Validate `health.audit --mesh` reports version skew = 0

### 4. Hardware Enrollment (ops — P2)

- **westGate**: Power on, network, `gate.bootstrap` (76TB ZFS cold storage)
- **NUC canary**: `gate.bootstrap` with `canary-fieldmouse` profile
- **Pixle**: Linux node enrollment

### 5. sourDough Tooling (sourDough — P2)

- `sourdough validate ribocipher` — fleet compliance auditing
- Scaffold template update — new primals born with riboCipher
- Fix forgejo parity (HTTP 500 error)

### 6. TOADSTOOL-AUTO-REGISTER (toadStool — P2)

PCI/sysfs enumeration on startup — auto-register GPU/NPU with biomeOS.
Blocks autonomous `gate.bootstrap` for compute gates.

---

## Wave 112 Exit Criteria

Wave 112 closes when:

1. ⬜ VPS rebuilt to `922eb24` (ops)
2. ⬜ 2 cascade cycles, zero intervention (Convergence Gate criterion 6)
3. ⬜ Version skew = 0 after cascade (criterion 7)
4. ⚠️ riboCipher ERROR logs: 6/8 shipped, sweetGrass + biomeOS pending
5. ⬜ At least 1 new hardware gate enrolled (westGate or NUC)

---

## Per-Team Summary

| Team | Wave 112 Work | Priority | Status |
|------|---------------|----------|--------|
| **cellMembrane** | VPS deploy 922eb24 → cascade validation → NUC bootstrap | P1 | Code shipped, ops pending |
| **sweetGrass** | riboCipher WARN→ERROR (one-line in peek.rs) | P2 | PENDING |
| **biomeOS** | riboCipher DEBUG→ERROR (connection.rs) | P2 | PENDING |
| **sourDough** | validate ribocipher + scaffold update | P2 | PENDING |
| **toadStool** | TOADSTOOL-AUTO-REGISTER | P2 | PENDING |
| **ops** | westGate + NUC + Pixle enrollment | P2 | PENDING |
| **primalSpring** | Proto-nucleate manifest (sub-NUCLEUS topologies) | P3 | PENDING |

---

## Documents Carried Forward

| Document | Status |
|----------|--------|
| `CONVERGENCE_GATE_WAVE111_PATTERN_DEPRECATION_JUN12_2026.md` | Active — 2/8 GREEN (4+8), 6 pending ops |
| `VPS_SURFACE_MINIMIZATION_EVOLUTION_JUN12_2026.md` | Active — Phase 1 (NUC replaces droplet) |
| `RIBOCIPHER_TRANSPORT_SIGNAL_STANDARD.md` | Standard — 9/9 converged, 6/8 at ERROR |
| `GATE_NUCLEUS_SYSTEMD_STANDARD.md` | Standard — deployed on ironGate |

---

## Glacial Position

**All 7 criteria CLEAR for stadial entry.** The ecosystem has crossed the interstadial exit gate. Wave 112's operational convergence (VPS rebuild + cascades) is the final validation before the glacial shift is formally declared.

riboCipher represents a qualitative leap: the ecosystem no longer guesses what connections want — it knows. This is the biological equivalent of evolving from chemotaxis (sense and respond to gradients) to nervous system (intentional signaling). The deprecation clock is ticking. By Wave 114, peek-and-guess will be extinct.

---

**Wave 112: Make it operational. The code is done. Prove the system self-heals.**
