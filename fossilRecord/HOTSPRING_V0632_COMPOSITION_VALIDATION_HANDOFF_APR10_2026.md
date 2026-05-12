# HOTSPRING v0.6.32 — Composition Validation Pattern Handoff

**Date:** April 10, 2026
**Spring:** hotSpring v0.6.32
**License:** AGPL-3.0-or-later
**Status:** Active

---

## Summary

hotSpring has evolved from Phase 1 (Python→Rust validation) to Phase 2
(Rust+Python→NUCLEUS composition validation). This handoff documents the
pattern for sibling springs to follow.

## Evolution Model

```
Phase 1: Python baseline → Rust validation (completed)
Phase 2: Rust+Python baseline → NUCLEUS primal composition validation (this handoff)
Phase 3: Composition → sovereign dispatch via coralReef (future)
```

The key insight: **the same validation methodology applies at every level**.
Python was the trusted baseline for Rust. Now Rust is the trusted baseline
for NUCLEUS composition. The IPC-wired composition must produce results
consistent with the direct Rust execution path.

## Pattern: Composition Validation Binaries

### File Structure

```
src/composition.rs          — Atomic health probes, capability routing
src/niche.rs                — Self-knowledge: capabilities, dependencies, proto-nucleate
src/bin/validate_nucleus_composition.rs  — Full NUCLEUS (all 9 primals)
src/bin/validate_nucleus_tower.rs        — Tower atomic (BearDog + Songbird)
src/bin/validate_nucleus_node.rs         — Node atomic (compute dispatch)
src/bin/validate_nucleus_nest.rs         — Nest atomic (provenance trio)
```

### Atomic Hierarchy

| Atomic | Particle | Primals | Validates |
|--------|----------|---------|-----------|
| Tower | electron | BearDog, Songbird | Trust + discovery |
| Node | proton | Tower + ToadStool, barraCuda, coralReef | Compute dispatch |
| Nest | neutron | Tower + NestGate, rhizoCrypt, loamSpine, sweetGrass | Storage + provenance |
| NUCLEUS | atom | Tower + Node + Nest (9 primals) | Full composition |

### Standalone Mode

When no primals are detected (`HOTSPRING_NO_NUCLEUS=1` or empty biomeos
directory), validators skip-pass — never fake-pass. This allows the binaries
to run in CI without requiring a full NUCLEUS deployment.

### Validation Model

```rust
// Same pattern as Python→Rust validation:
// 1. Known-good baseline: direct Rust execution
// 2. Validation target: IPC composition result
// 3. Tolerance: exact match for deterministic, justified for stochastic
harness.check_bool("tower healthy", tower.passed);
```

## IPC Surface

hotspring_primal now serves composition health via JSON-RPC:

| Method | Description |
|--------|-------------|
| `composition.health` | Full composition health (all atomics) |
| `composition.tower_health` | Tower atomic health |
| `composition.node_health` | Node atomic health |
| `composition.nest_health` | Nest atomic health |
| `composition.science_health` | Physics subsystem health |
| `health.readiness` | GPU + capability readiness probe |
| `mcp.tools.list` | MCP tool definitions for AI integration |

## ecoBin Packaging

`scripts/harvest-ecobin.sh` builds musl-static binaries and harvests to
`infra/plasmidBin/hotspring/`. Generates `metadata.toml` per ecoBin v3.0.

## For Sibling Springs

To adopt this pattern:

1. **Create `composition.rs`** with `AtomicType` enum and `validate_atomic()`
2. **Create `niche.rs`** with capabilities, dependencies, proto-nucleate ref
3. **Create `validate_nucleus_*.rs`** binaries per atomic
4. **Wire `composition.*` handlers** into your primal server
5. **Add ecoBin harvest script** if your spring produces harvestable binaries
6. **Document gaps** in `docs/PRIMAL_GAPS.md` and hand back to primalSpring

## Proto-nucleate Reference

`primalSpring/graphs/downstream/hotspring_qcd_proto_nucleate.toml`

The proto-nucleate declares a Phase 5 validation node:
```toml
[[graph.nodes]]
name = "validate_hotspring_qcd"
binary = "primalspring_primal"
capabilities = ["coordination.validate_composition"]
```

This ties hotSpring's local validation back to primalSpring's ecosystem-wide
composition experiments.

## Related Documents

- `NUCLEUS_SPRING_ALIGNMENT.md` — Spring-to-NUCLEUS mapping
- `PRIMALSPRING_COMPOSITION_GUIDANCE.md` — Composition validation protocol
- `ECOBIN_ARCHITECTURE_STANDARD.md` — ecoBin v3.0 packaging
- `hotSpring/docs/PRIMAL_GAPS.md` — Active gaps and handback protocol
