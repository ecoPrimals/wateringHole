# ToadStool S203 — Composition Elevation Sprint + Deep Debt Execution

**Date**: April 12, 2026
**Session**: S203
**Primal**: toadStool
**Author**: toadStool team
**Prior**: S202 (deep debt capability evolution)
**Context**: primalSpring downstream audit — Composition Elevation Sprint (dispatch result standardization)

---

## Summary

Resolved the MEDIUM-priority composition blocker identified by primalSpring:
`compute.dispatch` result shape now consistent across all 8 dispatch handlers.
Standardized envelope enables primalSpring's `extract_rpc_result<T>` /
`extract_rpc_dispatch<T>` typed extractors to validate composition parity in
the Node Atomic chain (coralReef → toadStool → barraCuda).

Additionally executed deep debt across 7 categories: smart file refactoring,
primal name evolution, unsafe code evolution, port centralization, clippy
suppression resolution, and RUSTSEC advisory cleanup.

## Changes

### Composition Elevation (Blocking)

- **Dispatch wire contract standardized** — All `compute.dispatch.*` and
  `shader.dispatch` responses now share: `{domain, operation, job_id, status,
  output, error, metadata}`. Previously `shader.dispatch` used different domain,
  pipeline used nested domain, status embedded error text.
- **Wire-stable status tags** — `DispatchStatus::as_str()` / `PipelineStatus::as_str()`
  return clean enum values; `Display` preserved for debug/logging.
- **Wire contract documented** — `specs/DISPATCH_WIRE_CONTRACT.md` covers all 8
  operations with typed extraction examples.

### Deep Debt Execution

- **Smart refactoring** — 4 production files >550 LOC refactored via test extraction:
  background (608→72), federation (594→109), encryption (568→257), runtime (576→249+stats)
- **Primal name evolution** — `get_primal_default_port` deprecated; callers migrated
  to `resolve_capability_port` with capability identifiers
- **Unsafe evolution** — GPU buffer access evolved to `NonNull::slice_from_raw_parts`
  pattern (safe metadata construction + scoped aliasing-only unsafe)
- **Port centralization** — Discovery fallback ports unified in
  `common/constants/discovery_ports.rs`
- **Clippy suppressions resolved** — `unused_self`, `cast_sign_loss`,
  `cast_possible_wrap` fixed rather than allowed
- **deny.toml cleaned** — 6 stale RUSTSEC advisories removed

## Code Health (S203 State)

| Metric | Value |
|--------|-------|
| Tests | 21,600+ passing (0 failures) |
| Coverage | ~83.6% lines (target: 90%) |
| Clippy | 0 warnings (workspace-wide `--all-targets`) |
| Doc warnings | 0 |
| Unsafe blocks | ~66 (all in hw-safe/GPU/VFIO/display containment) |
| Production TODOs | 0 |
| Max production file | <500 lines |

## For primalSpring Gap Registry

- **DISPATCH-RESPONSE-SHAPE**: RESOLVED — All dispatch responses use consistent
  `{domain, operation, job_id, status, output, error, metadata}` envelope.
  Wire contract at `specs/DISPATCH_WIRE_CONTRACT.md`.
- **D-COVERAGE-GAP**: Active — 83.6% → 90% target. Gap in hardware/container/WASM paths.

## For Node Atomic Partners (coralReef, barraCuda)

- toadStool dispatch responses now match the documented wire contract.
  Consumers should deserialize `compute.dispatch` responses using the
  `DispatchEnvelope` struct pattern shown in the wire contract doc.
- `shader.dispatch` wire method name unchanged; response `domain` is now
  `"compute.dispatch"` with `"operation": "shader"`.

## Remaining Debt (not blocking composition)

- Coverage 83.6% → 90% (D-COVERAGE-GAP)
- ~55 async-dyn markers blocked on Rust language evolution
- RUSTSEC-2024-0436 (paste via statrs chain — INFO unmaintained)
- tarpc Phase 3b binary framing (mesh protocol switching)
