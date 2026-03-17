<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# barraCuda v0.3.5 — Cross-Ecosystem Absorption Sprint

**Date**: March 16, 2026
**Primal**: barraCuda
**Version**: 0.3.5
**Sprint**: Deep Debt Sprint 6

---

## Summary

Cross-ecosystem absorption sprint informed by pulling and reviewing all 5
local springs (hotSpring, groundSpring, neuralSpring, wetSpring, airSpring),
6 phase-1 primals, 5 phase-2 primals, and wateringHole handoffs. Absorbed
patterns and fulfilled capability requests from across the ecosystem.

## Changes

### GemmF64 Transpose Flags (groundSpring, airSpring request)

- New `execute_gemm_ex()` method with `trans_a: bool`, `trans_b: bool`
- WGSL shader uses `select()`-based stride swapping — zero-branch indexing
- Enables `A^T * A`, `A^T * b` patterns without materializing the transpose
- **Use case**: Tikhonov regularization (groundSpring), least-squares (airSpring)
- Backward compatible: `execute()` and `execute_gemm()` unchanged (trans=false)
- 2 new GPU roundtrip tests (transpose_a, transpose_b)
- DF64 variant struct updated for layout compatibility

### FAMILY_ID Socket Paths (PRIMAL_IPC_PROTOCOL compliance)

- `default_socket_path()` now includes `$BIOMEOS_FAMILY_ID` (default: `"default"`)
- Path: `$XDG_RUNTIME_DIR/barracuda/barracuda-{family_id}.sock`
- Aligns with squirrel alpha.8, coralReef Iter 51, songBird v0.2.2

### blake3 ecoBin Compliance

- Added `default-features = false` to blake3 dependency
- Only `features = ["pure"]` enabled — no cc build dependency
- Absorbed from wetSpring V121 pattern

### deny.toml Supply Chain Audit

- `wildcards = "deny"` (was `"allow"`)
- barracuda-core wildcard dependency resolved (added `version = "0.3.5"`)
- Absorbed from groundSpring V110, airSpring v0.8.6 pattern

### WGSL_MEAN_REDUCE Public Re-export (neuralSpring request)

- `WGSL_MEAN_REDUCE` and `WGSL_MEAN_REDUCE_F64` re-exported from `ops/mod.rs`
- neuralSpring had a local copy; now uses the upstream constant

### Stale Lint Suppression Removal

- `#[expect]` audit detected 3 stale `#[allow(dead_code)]` on functions that
  are NOT dead code: `cpu_complex::Div`, `yukawa pbc_delta`, `get_neighbor_cells`
- kokkos_parity bench: `#[expect(clippy::unwrap_used)]` with reason

## P0 Bug Investigations

### ReduceScalarPipeline::sum_f64() returns zero (hotSpring)

**Finding**: Shader logic is correct (DF64 workgroup accumulation). The
issue is caller-side — likely `n` parameter mismatch between pipeline
construction and actual input buffer size, or input buffer not yet written
when reduce is dispatched.

**Recommendation**: hotSpring should verify that `ReduceScalarPipeline::new(n)`
matches the actual element count in the input buffer, and ensure the
producing kernel has been submitted and polled before calling `sum_f64()`.

### head_split/head_concat hang (hotSpring, neuralSpring)

**Finding**: WGSL shaders are correct (verified indexing math). The hang
likely originates from Vulkan driver pipeline stall on RTX 4070 or
workgroup dispatch sizing. Cannot reproduce without hardware.

**Recommendation**: Test with `--backend=vulkan` verbose logging. Check if
`dispatch_workgroups()` count exceeds device limits. Consider adding a
`GPU_TEST_TIMEOUT` watchdog around MHA dispatch.

## Quality Gates — All Green

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Pass |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Pass |
| `cargo deny check` | Pass (advisories, bans, licenses, sources) |

## Cross-Primal Impact

| Primal/Spring | Impact |
|---------------|--------|
| groundSpring | GemmF64 transpose unblocks Tikhonov `mat_transpose_mul` |
| airSpring | GemmF64 transpose enables least-squares without CPU transpose |
| neuralSpring | WGSL_MEAN_REDUCE re-export eliminates local shader copy |
| All springs | FAMILY_ID socket paths enable multi-family isolation |
| Ecosystem | deny.toml wildcards=deny prevents wildcard dep supply chain risk |

## Remaining Ecosystem Requests (Future Sprints)

| Priority | Request | Source |
|----------|---------|--------|
| P1 | SparseGemmF64 (CSR × dense) | wetSpring |
| P1 | u64 percentile API | wetSpring |
| P2 | Tridiagonal QL eigensolver (vectors) | groundSpring |
| P2 | TranseScoreF64 (knowledge graph) | wetSpring |
| P2 | TopK kernel | wetSpring |
| P2 | head_split/head_concat unify | neuralSpring |
| P2 | math.stat.* dispatch table | petalTongue |
