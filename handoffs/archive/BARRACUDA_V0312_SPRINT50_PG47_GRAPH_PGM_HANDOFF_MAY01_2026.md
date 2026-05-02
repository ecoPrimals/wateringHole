# barraCuda v0.3.12 — Sprint 50 Handoff (PG-47 + Graph PGM + BTSP Phase 3 Assessment)

**Date**: May 1, 2026
**Sprint**: 50 (Phase 56 — PG-47 resolution + graph expansion)
**Version**: 0.3.12
**Tests**: 279 barracuda-core pass, 0 failures
**IPC Methods**: 58 registered (was 56)
**Quality Gates**: fmt ✓ clippy (pedantic+nursery) ✓ doc (zero warnings) ✓ deny ✓
**Supersedes**: `BARRACUDA_V0312_SPRINT49_IPC_SURFACE_EXPANSION_P2_HANDOFF_APR30_2026.md`

---

## Context

primalSpring Phase 56 audit identified PG-47 (`stats.entropy` method not found)
as an upstream barraCuda gap blocking downstream callers. Investigation confirmed
this is a naming mismatch — `stats.shannon` (Shannon entropy) was wired in Sprint
49 but primalSpring callers expected `stats.entropy`.

## What Changed

### PG-47 Resolution: `stats.entropy` Alias

`stats.entropy` now dispatches to `stats.shannon` (Shannon entropy). primalSpring
callers using `stats.entropy` no longer receive method-not-found errors.
Both method names remain in `REGISTERED_METHODS` for discovery compliance.

### `graph.belief_propagation` — New JSON-RPC Method

Wires `barracuda::linalg::belief_propagation_chain` (chain PGM forward pass,
HMM-like) to IPC surface.

| Param | Type | Description |
|-------|------|-------------|
| `input` | `[f64]` | Initial probability distribution |
| `transitions` | `[[f64]]` | Array of flat row-major transition matrices |
| `layer_dims` | `[usize]` | Output dimension per layer |

Returns: `{ distributions: [[f64]], n_layers: int }`

### Module Decomposition

`math.rs` (837 lines, over 800L limit) decomposed: `linalg.graph_laplacian` and
`graph.belief_propagation` extracted to new `methods/graph.rs` (87 lines).
`math.rs` back to 760 lines.

### Sprint 50 Coverage Tests (7 new)

- `stats.entropy` alias dispatch, Shannon frequencies path, missing params
- Belief propagation: identity transition, two-layer, missing input, mismatched lengths

### BTSP Phase 3 Assessment

| Phase 3 Item | barraCuda Status |
|--------------|------------------|
| Cipher negotiation | **Implemented** — relay forwards `preferred_cipher` to BearDog, applies returned cipher + session_key |
| Stream wrapping | **Implemented** — `BtspFrameReader`/`BtspFrameWriter` with ChaCha20-Poly1305 AEAD on TCP + UDS |
| X25519 ECDH key exchange | **By design** — delegated to client + BearDog; barraCuda is crypto-agnostic relay |
| AES-256-GCM | **Not yet** — only ChaCha20-Poly1305 in `BtspCipher` enum |
| Client-side BTSP | **Deferred** — will absorb sourDough scaffold pattern when available |

**Summary**: barraCuda is Phase 3 ready as a **server/relay**. Client-side BTSP
(for connecting to other primals over encrypted channels) awaits sourDough scaffold.

## Sprint 50b: 12-Axis Deep Debt Audit + cargo update

- 12-axis audit confirmed clean: zero TODO/FIXME, zero unsafe outside barracuda-spirv,
  zero async-trait, zero Box<dyn Error> in production, zero println in library code,
  zero mocks in production, zero hardcoded sibling names in runtime, all files <800L
- `barracuda-core` tempfile dev-dep normalized to workspace version
- `cargo update` applied: tokio 1.50→1.52, clap 4.6.0→4.6.1, blake3 1.8.3→1.8.5,
  rayon 1.11→1.12, proptest 1.10→1.11, rand 0.9.2→0.9.4
- All quality gates green post-update (fmt, clippy, doc, deny bans+licenses, 1537+ tests)

## Remaining IPC Surface Gaps (GAP-11)

From the original 18 gaps (neuralSpring V133), **14 resolved** (11 prior + belief_propagation + stats.entropy alias).

Remaining 4 items — all architecturally complex, properly deferred:

| Item | Complexity | Reason |
|------|-----------|--------|
| `esn_v2::*` (~5 functions) | Stateful model (create/train/predict) | Needs session-based IPC protocol |
| `nautilus::*` (~5 functions) | Stateful exploration framework | Needs session-based IPC protocol |
| `numerical_hessian` | Takes `&dyn Fn` closure | Closure-over-IPC architecture decision |
| `boltzmann_sampling` | Takes `&dyn Fn` closure | Closure-over-IPC architecture decision |

---

<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
