# barraCuda v0.3.12 — Sprint 52: Phase 58 Audit Response

**Date**: May 4, 2026
**Primal**: barraCuda
**Sprint**: 52
**Trigger**: primalSpring Phase 58 debt handoff

---

## Audit Response Summary

### Item 1: Phase 3 Transport Encryption (HIGH) — ALREADY RESOLVED

The audit states: "server needs to actually switch transport."

**Status**: Resolved in Sprint 51 + 51b (May 2–3).

- `handle_btsp_connection` uses `BtspFrameReader`/`BtspFrameWriter` with
  `[4B len][12B nonce][ciphertext + 16B Poly1305 tag]` wire framing
- Transport switch confirmed with 2 live-validation integration tests
- BufReader data-loss bug fixed (Sprint 51b)
- `client_nonce` incorporated in HKDF salt per spec

### Item 2: ~12 JSON-RPC Surface Gaps (MEDIUM) — MOSTLY RESOLVED

All 4 priority methods are already wired:

| Method | Status | Since |
|--------|--------|-------|
| `linalg.eigh` | Wired (alias → `linalg.eigenvalues`) | Sprint 49 |
| `stats.pearson` | Wired (alias → `stats.correlation`) | Sprint 45 |
| `stats.chi_squared` | Wired | Sprint 45 |
| `stats.shannon` | Wired (aliased with `stats.entropy`) | Sprint 50 |

Also already wired: `linalg.solve` (Sprint 44), `ml.mlp_forward` (Sprint 45),
`graph.belief_propagation` (Sprint 50), `linalg.graph_laplacian` (Sprint 50),
`stats.fit_linear` (Sprint 49).

**Remaining (stateful, require session APIs)**: ESN v2, nautilus — these are
inherently multi-call stateful systems that don't map to single JSON-RPC requests.

### Item 3: Response Format Consistency (LOW) — RESOLVED

Added `result` key to 6 methods that previously returned only domain-specific keys:

| Method | `result` value |
|--------|---------------|
| `stats.chi_squared` | chi² statistic |
| `stats.anova_oneway` | F-statistic |
| `linalg.svd` | singular values (s) |
| `linalg.qr` | Q matrix |
| `stats.empirical_spectral_density` | density array |
| `graph.belief_propagation` | distributions array |

All existing domain keys preserved (backward-compatible). primalSpring's
`call_f64_flex` / `call_array_flex` will now find `result` on first try.

---

## Quality Gates

- `cargo fmt --all --check` ✓
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` ✓
- `cargo test -p barracuda-core --lib` — 292 pass
- 59 registered JSON-RPC methods (unchanged)
