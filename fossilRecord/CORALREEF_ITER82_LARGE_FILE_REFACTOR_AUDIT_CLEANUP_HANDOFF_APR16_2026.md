<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 82 Handoff

**Date**: April 16, 2026
**Phase**: 10 — Large File Refactoring, Hardcoding Dedup, Audit Cleanup
**Tests**: 4,506 passing, 0 failed, 153 ignored (hardware-gated). Zero clippy warnings.

---

## Summary

Iteration 82 is a deep audit and refactoring pass. No IPC wire changes, no new features. All work is internal quality evolution.

## Smart File Refactoring (>800L → Cohesive Modules)

| File | Before | After | Method |
|------|--------|-------|--------|
| `nvidia_headers.rs` | 839 | 460 + 381 (tests) | Test extraction to `nvidia_headers_tests.rs` |
| `firmware_parser.rs` | 806 | 318 + 488 (tests) | Test extraction to `firmware_parser_tests.rs` |
| `registers.rs` | 822 | 725 + 97 (tests) | Test extraction to `registers_tests.rs` |

Remaining >800L production files assessed and accepted:
- `runner.rs` (802L) — monolithic diagnostic matrix, barely over threshold
- `sm20/tex.rs` (854L) — dense SM20 texture encoding tables
- `sm75_instr_latencies/gpr.rs` (814L) — GPR allocation latency tables

All well under the 1000L hard limit; splitting would reduce cohesion.

## Hardcoding Deduplication

- Added `ECOSYSTEM_NAMESPACE` constants to `coral-glowplug/src/config.rs` and `coral-ember/src/config.rs`, matching the pattern already established in `coralreef-core/src/config.rs`. Each crate defines its own constant (primals don't cross-import per self-knowledge rule). The inline `"biomeos"` string literal is replaced with a named constant in all three crates.

## Deep Audit — All Areas Clean

| Dimension | Finding |
|-----------|---------|
| `.unwrap()` in library code | Zero instances outside `#[cfg(test)]` |
| `.ok()` in production | All in diagnostic/teardown/best-effort paths — justified |
| `#[allow(dead_code)]` BTSP | Justified: used in tests, `Debug` formatting, future evolution |
| Hardcoded primal names | Only `biomeos` ecosystem namespace (self-knowledge, env-overridable) |
| Mocks in production | None — all `#[cfg(test)]` gated |
| `unsafe` code | All in `coral-driver` with `// SAFETY:` on every block |
| EVOLUTION markers | 10 remaining — all legitimate future codegen/hardware items |
| External deps | Only `cudarc` (optional `cuda`) is non-pure-Rust; transitive `libc` permanent via tokio/mio |

## Transitive libc Coexistence (primalSpring Gap — Documented)

mio#1735 (rustix migration) was DECLINED upstream — transitive `libc` through tokio/mio is permanent. Both coexist: Tokio uses mio (libc), while coral-driver, coral-ember, and coral-glowplug use rustix directly (linux_raw, zero libc). Documented in `Cargo.toml` and `STATUS.md`.

## For Other Teams

- **No IPC wire changes** — `shader.compile.*` response schema unchanged vs Iter 80.
- **No capability registry changes** — discovery pattern stable.
- **No new dependencies** — workspace dep set unchanged.

## Remaining Gaps (unchanged from Iter 81)

- Coverage 62.7% → 90% target (hardware-gated code is primary barrier)
- musl-static verification
- Falcon boot FBP=0 resolution
- tarpc OpenTelemetry dep trimming
- plasmidBin deferred
