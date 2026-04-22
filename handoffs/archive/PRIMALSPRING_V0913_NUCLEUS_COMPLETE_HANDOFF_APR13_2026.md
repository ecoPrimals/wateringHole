# primalSpring v0.9.13 — Phase 40: NUCLEUS Complete

**Date:** 2026-04-13  
**Spring:** primalSpring  
**Version:** v0.9.13  
**Milestone:** Phase 40 — NUCLEUS Complete  
**License:** AGPL-3.0-or-later  

---

## Summary

Phase 40 closes the NUCLEUS integration milestone for primalSpring **v0.9.13**. All
layer-debt items **LD-01** through **LD-10** are **RESOLVED**. The integration
harness reports **12/12 primals ALIVE**, **exp094** at **19/19 PASS** with **0 FAIL**
and **0 SKIP**. The workspace test suite reports **455 tests passed**, **0 failures**.

Infrastructure and packaging are aligned with this milestone: **`nucleus_launcher.sh`**
Phase 5 registry seeding validates all **9 core NUCLEUS primals**; **`IpcError::is_transport_mismatch()`**
enables graceful handling when wire transport expectations diverge; **plasmidBin v4.1.0**
ships with refreshed **BLAKE3** checksums; and **67+ TOML graphs** are hardened with
**actual wire method capabilities** (no placeholder capability drift).

---

## What Changed

| Area | Outcome |
|------|---------|
| **Primals ALIVE** | 12/12 |
| **exp094** | 19/19 PASS; 0 FAIL; 0 SKIP |
| **LD-01 — LD-10** | All gaps RESOLVED |
| **primalSpring tests** | 455 pass; 0 failures |
| **nucleus_launcher.sh (Phase 5)** | Registry seeding validates 9 core NUCLEUS primals |
| **IPC / errors** | `IpcError::is_transport_mismatch()` for graceful transport handling |
| **plasmidBin** | v4.1.0 with fresh BLAKE3 checksums |
| **TOML graphs** | 67+ graphs hardened with real wire method capabilities |

---

## Per-Primal Evolution

| Primal | Version | Methods (approx.) | Notes |
|--------|---------|-------------------|--------|
| **BearDog** | v0.9.0 | 185 | `crypto.hash` base64 normalized |
| **Songbird** | v0.2.1 | 79 | `ipc.resolve` with `native_endpoint` / `virtual_endpoint` |
| **ToadStool** | v0.1.0 | 163 | BTSP auto-detect on all transports (**LD-04**) |
| **barraCuda** | v0.3.12 | 32 | JSON-RPC via BTSP guard line replay (**LD-10**); `math-{family}.sock` (**LD-05**) |
| **coralReef** | v0.1.0 | 10 | `shader.compile.capabilities` |
| **NestGate** | v0.1.0 | 30 | Persistent UDS connections (**LD-02** / **LD-03**) |
| **rhizoCrypt** | v0.14.0-dev | 28 | UDS at `rhizocrypt-{family}.sock` (**LD-06**) |
| **loamSpine** | v0.9.16 | 34 | UDS-first; TCP opt-in via `--listen` (**LD-09**) |
| **sweetGrass** | v0.7.27 | 32 | Braid / anchoring |
| **Squirrel** | v0.1.0 | 30 | `inference.complete` / `embed` / `models` |
| **petalTongue** | v1.6.6 | — | `--socket` CLI flag |
| **biomeOS** | v0.1.0 | — | Neural API orchestrator |

---

## exp094 Results (19/19)

Checks are grouped by tower scope as exercised by the harness.

### Tower

| Check |
|-------|
| `beardog_alive` |
| `songbird_alive` |
| `crypto_hash_nonempty` |
| `crypto_hash_base64_valid` |
| `crypto_hash_deterministic` |
| `resolve_security` |
| `resolve_compute` |
| `resolve_storage` |
| `songbird_method_catalog` |

### Node

| Check |
|-------|
| `tensor_stats_mean` |
| `shader_supported_archs` |
| `shader_wgsl_supported` |
| `compute_dispatch_alive` |

### Nest

| Check |
|-------|
| `storage_roundtrip_match` |
| `dag_alive` |
| `ledger_alive` |
| `attribution_alive` |

### NUCLEUS

| Check |
|-------|
| `cross_tower_hash` |
| `cross_nest_roundtrip` |

---

## What Downstream Springs Can Now Do

- **Run full NUCLEUS locally** — **12/12 ALIVE** via `nucleus_launcher.sh` with Phase 5
  registry seeding covering the nine core NUCLEUS primals.
- **Use `primalspring::composition`** for `validate_parity` flows that touch
  `stats.mean`, `storage.store` / `storage.retrieve`, and `crypto.hash`.
- **Use `ipc.resolve`** to discover any primal by capability, with Songbird exposing
  `native_endpoint` and `virtual_endpoint` metadata.
- **Rely on uniform liveness** — all primals expose **`health.liveness`** on UDS for
  operational probes and harness alignment.

---

## Remaining Debt

Phase 40 completes the NUCLEUS milestone and clears **LD-01 — LD-10**; remaining work is
ordinary product and engineering hygiene rather than blocking gap closure:

- Continue monitoring **cross-spring** upgrades so TOML graphs and plasmid checksums stay
  in sync with released primals.
- Preserve **exp094** and launcher scripts as first-class gates when bumping primal
  versions or transport defaults.
- Track any **new** layer-debt IDs outside LD-01–LD-10 through the standard gap registry
  process (this handoff does not supersede future audits).

---

## Next Steps

- Tag and publish artifacts for **primalSpring v0.9.13** and dependent primals per
  release policy.
- Broadcast this handoff to **downstream springs** so composition and IPC callers adopt
  `validate_parity`, `ipc.resolve`, and UDS `health.liveness` assumptions consistently.
- Keep **nucleus_launcher.sh** Phase 5 validation in CI or release checklists so registry
  seeding for the nine core NUCLEUS primals cannot regress silently.
- Schedule the **next phase** of roadmap work (post–NUCLEUS Complete) once product owners
  set priorities; no LD-series items remain open from this milestone.

---

## License

Copyright © contributors.

This document is part of the ecoPrimals / primalSpring ecosystem documentation.

Licensed under the **GNU Affero General Public License v3.0 or later** (AGPL-3.0-or-later).
See <https://www.gnu.org/licenses/agpl-3.0.html>.
