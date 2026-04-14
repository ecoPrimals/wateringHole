# ToadStool S201 — primalSpring Gap Closure & Coverage Push

**Date**: April 11, 2026
**Session**: S201
**Contact**: toadStool team
**Trigger**: primalSpring downstream audit (April 11, 2026) — gap matrix review

---

## primalSpring Audit Resolution

### Confirmed Resolved (S199)

**Pipeline scheduling for ordered dispatch** — The audit listed this as "Open" with
"Multi-stage pipeline ordering is still caller-side composition." This was stale:
`compute.dispatch.pipeline.submit` was implemented in S199 with:
- Full DAG-based topological ordering (Kahn's algorithm)
- `previous_results` forwarding between stages
- Exact tokenize→attention→FFN pattern neuralSpring needs
- 14 integration tests including multi-stage ordered dispatch, cycle rejection, unknown stage rejection
- Wire L3 cost estimates and semantic mappings

The audit's own conclusion confirms: "All springs should use stable
compute.dispatch.pipeline.submit (S199) for multi-stage workloads."

### Confirmed Blocked (External)

| Item | Status | Blocker |
|------|--------|---------|
| `D-RUSTIX-DISPLAY-038` | Blocked | V4L2 ioctl migration requires rustix 1.x `Ioctl` trait pattern; non-trivial, properly documented |
| `D-ASYNC-DYN-MARKERS` | Blocked | ~55 `NOTE(async-dyn)` markers — awaiting Rust `dyn Trait` + native async fn stabilization |

### Coverage Push: +46 Tests

| Module | Tests | Coverage Impact |
|--------|-------|-----------------|
| Wire L3 (`wire_l3.rs`) | 14 | Structural validation of 55+ method cost entries + 20+ dependency DAG edges |
| Dispatch types (`dispatch/types.rs`) | 12 | Display, serde roundtrip, equality, deserialization |
| Rate limiter (`rate_limiter.rs`) | 6 | Threshold enforcement, ban, daily limit, client isolation |
| Intrusion detection (`intrusion.rs`) | 7 | Auto-ban, risk score, ban expiry |
| Input validator (`input_validator.rs`) | 13 | XSS/SQL/command injection, sanitization, edge cases |
| Audit logger (`audit.rs`) | 7 | Event logging/retrieval, ordering, serde roundtrip |

All pure-logic tests — zero hardware requirements.

## For Other Primal Teams

- **All springs**: `compute.dispatch.pipeline.submit` (S199) is stable for multi-stage ordered workloads
- **neuralSpring**: 3-stage ML inference (tokenize→attention→FFN) pattern tested and confirmed working
- **wetSpring**: PG-05 (`compute.dispatch.submit`) stable since S199; pipeline API available for complex workloads
- **primalSpring**: All upstream gaps from cross-spring synthesis confirmed resolved from toadStool's perspective

## Remaining Known Debt

| Item | Status | Notes |
|------|--------|-------|
| `D-RUSTIX-DISPLAY-038` | Blocked | V4L2 ioctl wrapper migration to rustix 1.x |
| `D-ASYNC-DYN-MARKERS` | Blocked | Awaiting Rust language evolution |
| `D-COVERAGE-GAP` | Ongoing | 83.6% → 90% target; hardware-dependent paths remain uncovered |
| `D-EMBEDDED-PROGRAMMER` | Partial | Typed errors; awaiting hardware transport layers |
| `D-FUZZ-TARGETS` | Partial | Infrastructure added; needs CI + extended campaigns |

## Quality Gates

- `cargo check`: PASS
- `cargo clippy -D warnings`: PASS (0 warnings)
- All 46 new tests passing
- Zero regressions in existing test suite
