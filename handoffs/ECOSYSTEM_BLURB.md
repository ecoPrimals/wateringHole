# ecoPrimals Ecosystem Blurb — Wave 157a Code Team Handoff

**Date**: Aug 7, 2026 9:20AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **STAGE 2 HANDOFF. Forwarding fix compiled & verified. Two parallel code teams on eastGate: primalSpring (N2-N5 activation) + biomeOS (routing infrastructure). Overwatch moves to ecosystem coordination.**

---

## HANDOFF: TWO CODE TEAMS ON EASTGATE

### 1. primalSpring team — Neural API Activation Testing (N2-N5)

**Mission**: Verify the forwarding fix routes `capability.call` through Neural API to live primals.

**Setup**:
- Build the fixed binary: `cargo build --release -p neural-api-server` (in `primals/biomeOS`)
- The forwarding fix is in `crates/biomeos-atomic-deploy/src/neural_router/forwarding.rs`
- Test script: `scripts/neural-api-test.sh` (automates N1-N5 verification)
- NUCLEUS is live: 13 primals running on systemd, sockets at `/run/user/1000/biomeos/`

**Known**: Some primals (sweetGrass) require riboCipher prefix (`0xEC 0x01`) before JSON-RPC. bearDog accepts raw JSON-RPC. Neural API socket at `biomeos-neural.sock` also requires riboCipher prefix.

| # | Task | Owner | Status |
|---|------|-------|--------|
| **N1** | Forwarding fix | overwatch | **DONE** — compiles clean |
| **N2** | `capability.call` routes to bearDog | primalSpring | **NEXT** |
| **N3** | Tower Atomic composition (bearDog+songBird+skunkBat) | primalSpring | PENDING |
| **N4** | Provenance Trio composition (rhizoCrypt+loamSpine+sweetGrass) | primalSpring | PENDING |
| **N5** | squirrel agent routing via Neural API | primalSpring | PENDING |
| **N6** | Deploy to production gates | gate teams | BLOCKED on N2-N5 |

**NUCLEUS option**: primalSpring can run its own NUCLEUS (second instance on eastGate, or via beanchScale VM/image) to keep overwatch NUCLEUS undisturbed.

### 2. biomeOS team — Routing Infrastructure

**Mission**: Evolve the Neural API routing layer for Stage 2 readiness.

**Focus areas**:
- riboCipher-aware connection pooling (pool currently sends raw JSON-RPC, needs `0xEC` prefix for G65 sockets)
- Bootstrap→Coordinated mode transition (currently stuck in Bootstrap with 0 registered capabilities)
- Graph execution through capability semantics (`graph.execute` → `capability.call` chain)
- Spec: `specs/NEURAL_API_ACTIVATION_SPEC.md` (G67)

---

## STAGE 2 — NEURAL API AS ROUTING SUBSTRATE

biomeOS Neural API is the routing layer for all primal communication within a gate. Consumers call capabilities, not sockets. Stage 1 (direct socket wiring) is now the primordial bootstrap pattern.

**Why Stage 2 matters**:
- **Isomorphic deployment**: same graph, different hardware, same composition
- **Fractal self-similarity**: each gate is a self-similar NUCLEUS
- **Jelly string elimination**: no consumer imports a socket path
- **Deprecation boundary**: Stage 1 is fully primordial when no consumer calls sockets directly

---

## FORWARDING FIX (N1 — DONE)

Two changes to `forwarding.rs`:

| Change | What it fixes |
|--------|--------------|
| `forward_request_with_timeout` always uses pool path | `capability.call` dispatch uses pooled JSON-RPC with clean timeout, skips heavy tarpc→BTSP escalation |
| `forward_request()` wrapped in outer `request_timeout` | Graph/inference/proxy callers can't accumulate unbounded wall time |

---

## CASCADE: STRANDGATE HOTSPRING

hotSpring team on strandGate pushed AAR for compute trio work. Rung 1 experiment queue status:
- Plaquette ×4 normalization: **BLOCKER** (diagnostic needed before production runs)
- LaTeX source: `whitePaper/subGen/lattice_qcd_consumer_gpu.tex`
- Experiment queue: `wateringHole/handoffs/HOTSPRING_RUNG1_EXPERIMENT_QUEUE.md`
- 6-rung ladder: `wateringHole/handoffs/OVERWATCH_LATTICE_QCD_LADDER.md`

---

## PRIMALS CLEAR — 15/15 CROSS-ARCH

All 15 primals pass Windows cross-compilation. G64+G65+G66 COMPLETE. Zero primal debt.

---

## DEPLOYMENT SEQUENCE

1. ~~Fix cross-arch~~ — **DONE. 15/15 PASS.**
2. ~~Fix forwarding~~ — **DONE. N1 compiles clean.**
3. **Build fixed binary** → primalSpring team
4. **Verify on eastGate** (N2-N5) → primalSpring team
5. **Depot rebuild** — 15/15 musl + 15/15 Windows → sporeGate golgi
6. **Deploy with Neural API** — all NUCLEUS gates enter Stage 2

---

## BACKGROUND PROJECTS

| Gate | Project | Status |
|------|---------|--------|
| **westGate** | 343 GB federation. native_braid deployed. AlphaFold tiering. | Running |
| **strandGate** | SU(N) grid. arXiv Rung 1 (plaquette blocker). Compute memoization. | Running |
| **whitePaper** | DF64 theory. MILC interop roadmap. petalTongue-native figures. | Evolving |
| **ironGate** | G18 dispatch LIVE. esotericWebb + footPrint. Novel ferment CAS. | Stable |

---

## METRICS

| Metric | Value |
|--------|-------|
| P0/P1/P2 | **ZERO** |
| G64 + G65 + G66 | **COMPLETE** (15/15 cephalization, protocol negotiation, transport abstraction) |
| G67 Neural API | **Forwarding fix compiled. Stage 2 spec written. N2-N5 handed to code teams.** |
| Neural API tests | **456** |
| Musl depot | **17/17 on golgi** |
| Primal tests | **~140,000+** |
| Glacial goals | **14 COMPLETE / 26 ACTIVE / 23 GLACIAL — 63 total** |

---

*Wave 157a — **STAGE 2 CODE TEAM HANDOFF.** Forwarding fix compiled & verified post-reboot. Two parallel code teams on eastGate: primalSpring (N2-N5 live activation testing) and biomeOS (routing infra, riboCipher-aware pooling, bootstrap→coordinated transition). Overwatch moves to ecosystem coordination. strandGate hotSpring compute trio AAR cascaded. 15/15 cross-arch, zero debt, 14 COMPLETE, 63 goals, ~140K tests, 15/15 GREEN.*
