# primalSpring v0.8.0 — Substrate Validation: Primal Team Handoff

**Date**: March 28, 2026  
**From**: primalSpring (coordination spring)  
**To**: All primal teams (BearDog, Songbird, NestGate, ToadStool, Squirrel, biomeOS, petalTongue, rhizoCrypt, loamSpine, sweetGrass, skunkBat)  
**Scope**: Evolution debt exposed by deployment matrix + substrate validation, actionable per-primal

---

## Context

primalSpring now has a **43-cell deployment matrix** that tests primal compositions across
architectures (x86_64, aarch64), topologies (2-node → 10-node), network presets (localhost → deep space),
and transport modes (UDS, TCP). Combined with **59 deploy graphs**, **63 experiments**, and **15 benchScale
topologies**, the matrix systematically exposes gaps in primal behavior under diverse conditions.

This handoff documents **what each primal team needs to evolve** based on what the matrix found.

---

## Per-Primal Evolution Debt

### BearDog (crypto/security)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P0** | No `--listen <addr>` TCP server mode | tower-*-tcp, all mobile cells | Add TCP listener alongside UDS; honor `BEARDOG_PORT` env |
| **P0** | Hard-exits if UDS bind fails (~5s) | All mobile/GrapheneOS cells | Graceful fallback: try TCP if UDS fails, don't exit |
| **P1** | Cross-family ionic trust negotiation | ionic-x86-homelan-uds | `verify_foreign()` — validate signatures from different FAMILY_ID |
| **P2** | Mixed entropy hierarchy | mixed-entropy graphs | Document entropy sources for `generate_keypair` (hardware RNG, OS, human) |

### Songbird (network/discovery)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P1** | Capability-filtered `discovery.query` | All agentic/storytelling cells | `discovery.query({ capabilities: ["game.*"] })` — return only matching primals |
| **P1** | Albatross multiplex (tarpc saturation) | albatross-x86-basement-uds | Validate 3+ concurrent Songbird instances under tarpc saturation |
| **P2** | BirdSong mesh reformation after partition | chaos-x86-homelan-uds | Mesh must re-form after network partition heals |

### NestGate (storage)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P0** | aarch64-musl segfault (exit 139) | nucleus-aarch64-mixed-tcp | Debug and fix musl static build for ARM64 |
| **P1** | Announce MCP tools to Squirrel | All agentic cells | `storage.store`, `storage.retrieve` as MCP tools via `capability.announce` |
| **P1** | Content-addressed storage for fieldMouse frames | fieldmouse-x86-homelan-uds | `storage.content_address` for sensor data dedup |

### ToadStool (compute)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P1** | Announce MCP tools to Squirrel | All agentic cells | `compute.submit`, `compute.status` as MCP tools |
| **P1** | Gaming mesh 60Hz dispatch | gaming-x86-localhost-uds | GPU compute dispatch within 16.6ms tick budget |
| **P2** | Neuromorphic NPU dispatch | neuromorphic-x86-homelan-uds | ToadStool routes to NPU backends (Akida, Coral) |
| **P2** | `display.present` frame path | gen4 graphs with petalTongue | Complete the GPU render → petalTongue frame submission path |

### Squirrel (AI/MCP)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P0** | Abstract socket `@squirrel` vs filesystem | agentic-x86-homelan-uds, storytelling cells | Default to filesystem socket at `$XDG_RUNTIME_DIR/ecoPrimals/squirrel.sock` |
| **P1** | Capability string canonicalization | All graphs referencing `ai.*` | Align: `ai.query` (not `ai.coordinate`), `tool.execute` (not `ai.execute_tool`) |
| **P1** | Mechanical constraint enforcement | storytelling cells | Accept structured game context from esotericWebb, enforce in narration |

### biomeOS (orchestrator)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P0** | `api --port` ignored, forces UDS | tower-*-tcp, agentic-*-tcp, storytelling-*-tcp | Honor `--port` flag: bind TCP listener |
| **P0** | `capability.call` ignores `gate` param | federation-x86-mixed-uds, wan cells | Look up gate endpoint via Songbird mesh → forward request |
| **P1** | `neural-api` exits without biome.yaml | All benchScale topologies | `--standalone` flag for empty-graph health + routing |
| **P1** | `health.check` returns "Method not found" | All cells with Neural API probes | Register both `health.check` and `health.liveness` as aliases |
| **P2** | Abstract socket routing for Squirrel | agentic cells | `TransportEndpoint` handles `abstract://squirrel` |

### petalTongue (visualization)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P0** | SSE reconnection robustness | All cells with biomeOS + petalTongue | Exponential backoff reconnection, cache last-known state |
| **P1** | Dialogue-tree scene type | storytelling cells | `SceneType::DialogueTree` — NPC portraits, dialogue options, ability checks |
| **P1** | Provenance trio stamp on exports | nucleus-x86-basement-provenance | Embed Merkle root in SVG/PNG exports |
| **P2** | skunkBat defense dashboard | skunkbat-x86-homelan-uds | Trust boundary visualization, real-time violation alerts |
| **P2** | fieldMouse sensor dashboards | fieldmouse-x86-homelan-uds, agentic-fm cells | Time-series sensor data with domain-aware palettes |

### Provenance Trio (rhizoCrypt, loamSpine, sweetGrass)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P0** | loamSpine startup crash (Tokio nested runtime) | nucleus-x86-basement-provenance | Fix `infant_discovery` nested runtime panic |
| **P1** | Live E2E session provenance | storytelling cells, rpgpt graphs | Full chain: `dag.session.create` → `event.append` → `lineage.certify` → `braid.verify` |
| **P1** | petalTongue export stamps | All provenance cells | `sweetGrass.provenance.create_braid` for attributed exports |

### skunkBat (defensive security)

| Priority | Issue | Matrix Cell | Action |
|----------|-------|-------------|--------|
| **P1** | Wire defense events to petalTongue | skunkbat-x86-homelan-uds | `defense.violation_detected` → petalTongue threat dashboard |
| **P2** | External probe detection | skunkbat defensive mesh | Detect and log probes from non-family nodes |

---

## Patterns to Absorb

### From benchScale Topologies

1. **Network presets**: 7 conditions from `localhost` (0ms) to `deep_space` (2000ms RTT, 10% loss). Primals should test under all.
2. **Read-only filesystem**: `--read-only --tmpfs` simulates mobile/GrapheneOS. Primals must not write outside `/tmp` or `/run`.
3. **Memory-constrained**: 256MB Docker limit. Primals should handle OOM gracefully (exit clean, don't corrupt state).
4. **Mixed architecture**: x86_64 + aarch64 in same cluster. Crypto outputs must be byte-identical across arch.

### From Graph Compositions

1. **Continuous coordination @ 60Hz**: Storytelling and gaming graphs use `Continuous` pattern. Primals in the loop must respond within 16.6ms.
2. **Pipeline streaming**: Science graphs use `Pipeline` for data flow. Primals must handle streaming without buffering entire payloads.
3. **Bonding models**: Ionic (cross-family), metallic (delocalized), OMS (multi-trust). Primals need to understand their bond context.

### From Chaos Engineering

1. **Network partition + heal**: Primals must detect and recover from partition without manual restart.
2. **Process kill + restart**: biomeOS should detect dead primals and re-route.
3. **Slow start**: Random 0-30s startup delays. Graph execution must tolerate slow primals.

---

## Deployment Matrix Cells Available for Testing

The full matrix is in `springs/primalSpring/config/deployment_matrix.toml`. Primal teams can test their
changes against specific cells:

```bash
# From primalSpring root
scripts/validate_deployment_matrix.sh --cell tower-x86-homelan  # basic tower
scripts/validate_deployment_matrix.sh --cell agentic-x86-homelan-uds  # agentic loop
scripts/validate_deployment_matrix.sh --cell storytelling-x86-localhost-uds  # storytelling
scripts/validate_deployment_matrix.sh --dry-run --all  # see all 43 cells
```

---

## Related Specs

- `springs/primalSpring/specs/AGENTIC_TRIO_EVOLUTION.md` — biomeOS + Squirrel + petalTongue loop
- `springs/primalSpring/specs/STORYTELLING_EVOLUTION.md` — ludoSpring + esotericWebb AI DM
- `springs/primalSpring/specs/SHOWCASE_MINING_REPORT.md` — patterns from primal showcases
- `springs/primalSpring/specs/CROSS_SPRING_EVOLUTION.md` — full evolution path
- `infra/wateringHole/FIELDMOUSE_DEPLOYMENT_STANDARD.md` — fieldMouse chimera class
