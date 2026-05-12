# hotSpring v0.6.32 — Audit & Execution Cycle Handoff

**Date:** April 10, 2026  
**From:** hotSpring (`springs/hotSpring`)  
**To:** barraCuda, toadStool, coralReef, primalSpring, biomeOS, and sibling springs  
**Version:** hotSpring v0.6.32  
**License:** AGPL-3.0-or-later

**Related handoffs (same day):**

- [`HOTSPRING_V0632_PRIMAL_EVOLUTION_NUCLEUS_DEPLOYMENT_HANDOFF_APR10_2026.md`](HOTSPRING_V0632_PRIMAL_EVOLUTION_NUCLEUS_DEPLOYMENT_HANDOFF_APR10_2026.md) — primal evolution, NUCLEUS deployment via neuralAPI / biomeOS, absorption tiers, TensorSession gap  
- [`HOTSPRING_V0632_COMPOSITION_VALIDATION_HANDOFF_APR10_2026.md`](HOTSPRING_V0632_COMPOSITION_VALIDATION_HANDOFF_APR10_2026.md) — composition validation binaries, atomic hierarchy, IPC surface, standalone skip-pass mode  

---

## Summary

A full **ecosystem audit plus execution cycle** completed on hotSpring: formatting, lint hygiene, intentional lint attributes, tolerance centralization, client and discovery wiring, orphan cleanup, deduplication of plaquette variance helpers, and Python environment pinning for reproducible science baselines. This handoff captures what was fixed, what was learned, and what downstream projects should absorb or track.

---

## What Was Fixed

| Area | Outcome |
|------|---------|
| **cargo fmt** | Workspace formatted to a consistent style. |
| **Clippy** | **42** errors cleared; **83** warnings addressed (remaining noise driven down per policy). |
| **Lint attributes** | `#[allow(...)]` migrated to **`#[expect(...)]`** where the lint is intentionally accepted — documents intent and surfaces if the compiler stops firing. |
| **Tolerances** | Thresholds consolidated into shared tolerance constants (**20+** new / centralized) for auditability and cross-binary consistency. |
| **Squirrel client** | Client surface aligned for neural-side capabilities (see gaps: full proto-nucleate wiring still tracked). |
| **Capability-based discovery** | Routing and discovery paths improved toward capability-addressed lookup (named accessors still present where needed). |
| **Orphan cleanup** | Dead or duplicated code paths removed in the audit pass. |
| **`plaquette_variance`** | Duplicate logic removed; hotSpring delegates to **`barracuda::stats`** for shared statistics. |
| **Python env** | Environment **pinning** for reference scripts and validation baselines (reproducible Python↔Rust checks). |

---

## What Was Learned

1. **Composition validation patterns** — The same discipline used for Python→Rust parity extends to **Rust↔NUCLEUS IPC**: direct Rust as baseline, composition as target, tolerances and exit codes as gates.  
2. **Three-tier validation architecture** — **Python baselines → Rust implementations → NUCLEUS IPC compositions**, with standalone validators that **skip-pass** when no deployment is present (CI-safe, never fake-pass).  
3. **NUCLEUS deployment via neuralAPI from biomeOS** — hotSpring is positioned for standard socket discovery and health-driven orchestration aligned with biomeOS deployment flows (see NUCLEUS deployment handoff for neuralAPI detail).

---

## Absorption Candidates (Update)

| Pattern / asset | Suggested recipients |
|-----------------|---------------------|
| **20+ tolerance constants** | Any spring with multi-binary validation — centralize in one module per crate. |
| **`squirrel_client.rs` pattern** | Springs that need neural/inference IPC without hard-wiring socket names everywhere. |
| **`call_by_capability` pattern** | biomeOS / primal bridge consumers moving from named primal accessors to capability routing. |

---

## For barraCuda

- **`plaquette_variance`** now **delegates to `barracuda::stats`** — single source of truth for plaquette statistics helpers.  
- **`TensorSession`** remains **not adopted** for fused multi-op pipelines — still **GAP-HS-007** (deferred until API stable for lattice workloads; natural first use: HMC trajectory fusion).

---

## For primalSpring

- **Composition validation binary pattern** is **proven in production** on hotSpring (`validate_nucleus_*`, `niche.rs`, `composition.rs`).  
- **Active gaps** for ecosystem handback remain documented in hotSpring `docs/PRIMAL_GAPS.md`: **GAP-HS-001, GAP-HS-002, GAP-HS-005, GAP-HS-006, GAP-HS-007, GAP-HS-010** (Squirrel proto-nucleate, pure capability discovery, ionic GPU lease, BTSP session crypto, TensorSession adoption, inline threshold migration). Resolved items include MCP/readiness/composition binaries/ecoBin (HS-003/004/008/009).

---

## For Sibling Springs

Recommended adoption:

- **`niche.rs` + `composition.rs` + `validate_nucleus_*`** — self-description, atomic probes, and gated validators.  
- **Standalone mode** — validators run in CI with skip-pass when NUCLEUS is absent.  
- **`#[expect]` over `#[allow]`** — intentional suppressions only.  
- **Centralized tolerances** — avoid magic numbers scattered across `validate_*` binaries.

---

## For biomeOS

- hotSpring is **discoverable at the standard socket** (see `infra/plasmidBin/hotspring/metadata.toml`: `socket_convention`, health and capabilities methods).  
- Serves **health**, **capability**, **composition**, and **MCP** JSON-RPC endpoints via `hotspring_primal`.  
- **Proto-nucleate** alignment documented in niche/proto-nucleate TOML — consistent with NUCLEUS composition narrative in the cross-referenced handoffs.

---

## ecoBin / plasmidBin

- **Harvested** to `infra/plasmidBin/hotspring/` — **musl-static** ecoBin packaging (~**4 MB**), metadata and standard socket/health/capability conventions recorded for plasmid distribution.

---

## Cross-Reference Index

| Document | Focus |
|----------|--------|
| **This file** | Audit + execution fixes, learnings, absorption, downstream notes |
| **NUCLEUS deployment handoff** | Primal evolution, neuralAPI, deployment phases, barraCuda usage stats, absorption tiers |
| **Composition validation handoff** | Binaries, atomics, IPC methods, standalone mode, Phase 1→2→3 model |

---

*End of handoff.*
