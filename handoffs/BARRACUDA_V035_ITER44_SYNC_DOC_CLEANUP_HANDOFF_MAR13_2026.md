# barraCuda v0.3.5 — Iter 44 Sync & Doc Cleanup

**Date**: March 13, 2026
**Type**: Maintenance handoff
**Scope**: Cross-primal pin sync, count alignment, debris audit

---

## Summary

barraCuda docs synced to coralReef Iteration 44 (USERD_TARGET + INST_TARGET
runlist fix). Full debris audit confirms zero stale TODOs, zero archive
candidates, zero files over 1,000 lines. All quality gates green.

---

## Pin Updates

| Primal | Previous | Current | Key change |
|--------|----------|---------|------------|
| coralReef | Phase 10 Iter 43 | Phase 10 Iter 44 | USERD_TARGET + INST_TARGET fix in runlist DW0/DW2 |
| toadStool | S153 | S153 | No change |
| hotSpring | v0.6.31 | v0.6.31 | No change |

## VFIO Dispatch Status

coralReef Iter 44 applied the root cause fix for the GP_PUT last-mile issue:
- Runlist DW0: `USERD_TARGET[3:2]` set to SYS_MEM_COHERENT (was VRAM)
- Runlist DW2: `INST_TARGET[5:4]` set to SYS_MEM_NCOH (was VRAM)
- Hardware revalidation on Titan V pending — 7/7 expected

## Count Alignment

| Metric | Value | Status |
|--------|-------|--------|
| Tests | 4,011 (3,941 lib + 70 core) | Aligned |
| Rust files | 1,088 | Aligned |
| WGSL shaders | 806 | Aligned |
| Integration test files | 43 | Fixed (was 42 in 2 files) |

## Debris Audit

| Category | Finding |
|----------|---------|
| TODO/FIXME in .rs | Zero |
| Stale scripts | None |
| Archive candidates | None |
| Files > 1000 lines | None |
| Hardcoded ports/primals | None in production |

## Quality Gates

- `cargo fmt --all -- --check` ✅
- `cargo clippy --workspace --all-targets -- -D warnings` ✅
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` ✅
