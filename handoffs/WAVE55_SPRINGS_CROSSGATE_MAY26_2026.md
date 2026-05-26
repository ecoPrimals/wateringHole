# Wave 55+ — Springs Launch + Cross-Gate NUCLEUS Handoff

**Date**: 2026-05-26  
**From**: primalSpring (coordination)  
**To**: All spring teams  
**Context**: PostPrimordial complete. Waves 53–54 clear primal mountains and
stabilize gates. This handoff previews Wave 55+ spring launch work so teams
can prepare. Glacial shift wave plan at `wateringHole/GLACIAL_SHIFT_WAVE_PLAN.md`.

---

## Prerequisites (Waves 53–54)

Before spring launch:
- All 4 gates at 13/13 primals (southGate + biomeGate fixes)
- `s_covalent_mesh` PASS on all 4 gates (Songbird mesh validated)
- cellMembrane VPS Nest expansion complete

---

## Spring Proto-Nucleate Deployment

Each spring deploys its `proto_nucleate_template.toml` graph on its assigned
gate. The graph is pure-primal (no spring binaries as nodes) — springs
validate externally via `primalspring::composition::validate_parity()`.

| Gate | Springs | Current Status |
|------|---------|----------------|
| eastGate | airSpring, groundSpring | Already operational |
| ironGate | ludoSpring, healthSpring | Already operational |
| southGate | wetSpring, neuralSpring | Pending gate stabilization |
| biomeGate | hotSpring | Pending federation fix |

**Action**: If your spring is already operational on its gate, no deployment
action needed. If pending, prepare your deploy graph and wait for the gate
stabilization signal from Wave 54.

---

## Per-Spring Action Items

### wetSpring

- **PG-02**: Provenance trio live roundtrip verification on stable southGate
- **PG-04**: NestGate storage roundtrip verification
- These are deployment verification only — upstream gaps are resolved

### neuralSpring

- **loamSpine Tokio double-runtime crash**: investigate and fix. This blocks
  full Nest Atomic on southGate.
- **Squirrel provider registration**: wire Squirrel AI into composition
- **toadStool `health.liveness`**: verify -32601 error is resolved after
  southGate redeploy

### hotSpring

- **BiomeGate federation**: after gate operator restarts Songbird (Wave 54),
  verify hotSpring's NUCLEUS composition is fully healthy
- **Ionic GPU lease prototype**: GAP-HS-005 — BearDog `crypto.sign_contract`
  for cross-family GPU scheduling. Begin prototype once BearDog confirms
  contract signing capability.

### healthSpring

- **BTSP probe pattern**: implement `btsp.capabilities` query before
  attempting BTSP negotiation. Currently `FAMILY_SEED` presence causes
  unconditional BTSP negotiation which fails against primals that don't
  support it yet.
- **Ionic bridge**: dual-tower enclave pattern is live; cross-tower ionic
  bridge validation next.

### ludoSpring

- **6 game.* methods for esotericWebb**: `game.push_scene`, `game.state`,
  `game.inventory`, `game.dialogue`, `game.combat`, `game.save` — wire
  these for the gen4 CRPG product
- **Notebook gap**: ludoSpring has 0 Jupyter notebooks vs other springs
  averaging 20+. Not blocking but noted for parity.

### groundSpring

- **Squirrel composition integration**: additive, low priority. Wire Squirrel
  AI into composition context for geology/measurement workflows.

### airSpring

- **AG-006**: coralReef shader compilation for ecology visualization
- **AG-009**: petalTongue direct IPC (bypass Neural API for latency-sensitive
  rendering)
- **AG-021**: Akida NPU driver integration (hardware-specific, deferred)

---

## Cross-Gate Capability Routing (all springs)

Once gates are stable, primalSpring will run cross-gate smoke tests:

1. From each gate, `capability.call` to capabilities on every other gate
   via Songbird braid relay
2. Verify provenance trio roundtrips across gates
3. Validate ionic cross-family patterns

Springs should be prepared to run their validation scenarios against
remote gates (set `PRIMALSPRING_HOST` + `PRIMALSPRING_TCP_TIER5=1`
for TCP-based cross-gate probing).

---

## Membrane Interaction (FYI — cellMembrane-owned)

After springs are connected:
- K-Derm channel proteins go live (TLS, NAT, content, auth boundaries)
- S1 TLS shadow cutover: Cloudflare → sovereign TLS via Caddy
- Forgejo Actions: shadow CI on ironGate, then invert to Forgejo-primary

Springs don't need to act on membrane items directly — cellMembrane handles
the boundary. But springs should be aware that cross-gate traffic will
eventually route through formal K-Derm channel proteins rather than direct
Songbird TCP.

---

## Timeline

Wave 55 begins after gates are stable (all 4 at 13/13, mesh validated).
Spring deployment is incremental — already-operational springs continue;
pending springs deploy as their gates come online.

No ack needed for this preview handoff. Action handoffs will follow per-spring
when Wave 54 completes.
