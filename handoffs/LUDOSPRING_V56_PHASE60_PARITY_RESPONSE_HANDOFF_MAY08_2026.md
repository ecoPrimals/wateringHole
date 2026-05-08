# SPDX-License-Identifier: AGPL-3.0-or-later

# ludoSpring V56 — Phase 60 Parity Response

**From:** ludoSpring V56 (game science, HCI, procedural generation)
**Date:** May 8, 2026
**To:** primalSpring (audit response), barraCuda (GAP-13), sweetGrass (capability hint), toadStool (naming)

---

## Response to Cross-Spring Parity Audit

primalSpring's Phase 60 audit scored ludoSpring **GOOD** with 3 targets:
1. **Registry cross-sync test** — DONE. Two tests in `niche.rs` validate bidirectionally.
2. **Paper notebooks** — DOCUMENTED. `docs/PAPER_QUEUE.md` maps papers 17-22, 24a, 26 and queues `.ipynb` creation.
3. **Git branch tracking** — CONFIRMED clean (main tracks origin/main, no detached HEAD).

---

## New Gaps Documented (handback)

| GAP | Owner | Action Required |
|-----|-------|-----------------|
| GAP-12 | **primalSpring** | Register 15 ludoSpring methods in canonical `config/capability_registry.toml` |
| GAP-13 | **barraCuda** | `tolerances/precision.rs:138` unconditionally imports `crate::device` which is `#[cfg(feature = "gpu")]` — breaks non-GPU consumers |
| GAP-14 | **ludoSpring** | Normalize provenance commit hashes across validator binaries (internal) |
| GAP-15 | **ludoSpring** | RESOLVED V56 — Squirrel AI node added to gaming niche graph |

---

## Composition Patterns for Upstream Absorption

### 1. Circuit Breaker (generic, primal-agnostic)

`barracuda/src/ipc/circuit_breaker.rs` (156 lines) implements:
- Static `AtomicU64` trip/cooldown tracking
- Configurable via env vars (`*_CIRCUIT_COOLDOWN_MS`, `*_MAX_RETRIES`, `*_RETRY_DELAY_MS`)
- `resilient_call<F>` wraps any `Fn(&NeuralBridge) -> Result<Value, IpcError>`
- Used by provenance trio, adaptable to any primal IPC

**Absorption target:** barraCuda (core IPC resilience pattern) or primalSpring (composition guidance).

### 2. Registry Cross-Sync Test Pattern

```rust
#[test]
fn capabilities_match_local_registry_toml() {
    let toml_str = include_str!("../../config/capability_registry.toml");
    // Parse TOML, collect methods, assert bidirectional match with CAPABILITIES constant
}

#[test]
fn capabilities_subset_of_primalspring_canonical() {
    let canonical = include_str!("../../../../primalSpring/config/capability_registry.toml");
    // Parse, filter domain prefix, assert superset
}
```

**Absorption target:** primalSpring (add to `exp095_proto_nucleate_template` scaffold).

### 3. Pure Composition (no spring binary in production)

ludoSpring's model: the spring binary is development/test infrastructure only.
Production deployment = biomeOS deploying `ludospring_cell.toml` (12-node primal graph).
Validation = `ludospring_guidestone` + `validate_composition` against golden JSON.

**Implication for neuralAPI:** When biomeOS orchestrates a ludoSpring cell, it
calls primals by capability. ludoSpring code isn't on the critical path — only
the primal graph definition and golden-value composition targets matter.

### 4. GPU Protocol Tag Centralization

All IPC envelopes tag `"ludospring_gpu_v1": true` via a single constant.
Pattern prevents version string drift when toadStool evolves the protocol.

---

## For Downstream Systems

### projectNUCLEUS

- ludoSpring's `ludospring_gaming_niche.toml` deploy graph is ready for NUCLEUS integration
- Squirrel AI node enables `inference.complete` for NPC dialogue without spring code changes
- Workload TOML template needed at `projectNUCLEUS/workloads/ludospring/`

### foundation

- Thread 9 (Gaming/Creative) and Thread 10 (Provenance/Economics) mapped
- `data/sources/thread09_gaming.toml` data manifest needed
- Papers 17-22, 24a, 26 are ludoSpring's scientific lineage

### sporeGarden / primals.eco

- `sporeprint/validation-summary.md` refreshed with correct metrics
- Ready for next `primals.eco` deploy

---

## State

| Metric | Value |
|--------|-------|
| Version | V56 |
| Tests | 820+ |
| Experiments | 100 crates |
| Deploy graphs | 12 |
| Capabilities | 30 FQN methods |
| GuideStone | L4 (54/54 checks) |
| Gaps (open) | 7 (GAP-01–06, 09, 12–14) |
| primalSpring | v0.9.25 |
| barraCuda | v0.3.11 (0.3.13 blocked) |

---

**License:** AGPL-3.0-or-later
