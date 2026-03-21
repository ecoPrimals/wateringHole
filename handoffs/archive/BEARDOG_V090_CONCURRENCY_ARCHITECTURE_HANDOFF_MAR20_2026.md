# BearDog v0.9.0 — Concurrency Architecture & Dependency Modernization Handoff

**Date**: March 20, 2026
**Primal**: BearDog (cryptographic service provider)
**Session Focus**: Deep debt resolution — evolving to fully concurrent, modern idiomatic Rust

---

## What Changed

### Dependency Injection Architecture (the big one)

BearDog's entire codebase was refactored from a pattern of reading environment
variables deep inside business logic to a proper dependency injection architecture:

- **`Default` impls are now pure** — no I/O, no env reads, no file access
- **`from_env()`** reads `std::env::var` (thread-safe, read-only) at startup boundaries
- **`from_env_provider(get: impl Fn(&str) -> Option<String>)`** enables injectable testing
- Config structs flow through the call chain as parameters

This eliminated 330 `#[serial_test::serial]` annotations down to 15 (chaos/fault only).
All 13,400+ tests now run fully concurrent at `--test-threads=8` with zero races.

### Dependency Modernization

| Old | New | Reason |
|-----|-----|--------|
| `trust-dns-resolver` 0.23 | `hickory-resolver` 0.25 | trust-dns unmaintained |
| `bincode` 1.3 | `postcard` 1.0 | bincode unmaintained |
| `validator` 0.18 | `validator` 0.20 | drops unmaintained `proc-macro-error` |

### cargo deny

All 4 checks pass: advisories, bans, licenses, sources.
RSA Marvin Attack (RUSTSEC-2023-0071) documented as accepted risk — no upstream fix exists.

### Hanging Tests Fixed

`beardog-deploy` introduced `CommandRunner` trait with `MockAdbCommandRunner` for tests.
`show_logs` follow mode has bounded timeout. No more zombie `adb logcat` processes.

---

## Current Metrics

| Metric | Value |
|--------|-------|
| Crates | 29 |
| Tests | 13,400+ |
| Coverage | 84% line (llvm-cov) |
| Clippy | 0 warnings (pedantic + nursery) |
| Serial tests | 15 (chaos/fault only) |
| cargo deny | All 4 pass |
| Unsafe code | 0 production blocks |
| Files > 1000 LOC | 0 |

---

## Impact on Other Primals

### For all primals using BearDog's IPC

No wire protocol changes. JSON-RPC interface is unchanged. The `postcard` migration
affects internal serialization only (HSM backup format, constraint hashing) — not IPC.

### For primals referencing BearDog config patterns

The DI pattern (`Default` pure, `from_env()` at boundaries, `from_env_provider()` for
testing) is now the standard. Other primals should adopt this pattern to enable
concurrent testing without `#[serial_test::serial]`.

### hickory-dns

If other primals depend on `trust-dns-resolver`, they should migrate to `hickory-resolver`
to avoid duplicate dependency trees.

---

## Remaining Work

- **Coverage**: 84% → 90% target (need ~6,900 more lines)
- **Large file refactoring**: Some files approach 1000 LOC
- **`#[allow(dead_code)]` cleanup**: ~80 files have planned/future dead code markers
