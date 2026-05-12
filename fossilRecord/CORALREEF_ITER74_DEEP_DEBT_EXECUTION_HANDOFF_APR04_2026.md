<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# coralReef — Iteration 74: Deep Debt Execution Handoff

**Date**: April 4, 2026
**Primal**: coralReef
**Iteration**: 74
**Phase**: 11 — Deep Debt Execution (audit follow-through)
**To**: primalSpring, toadStool, barraCuda, hotSpring

---

## Summary

Iteration 74 executes on the comprehensive audit findings from Iteration 73. Focus: lint evolution, coverage expansion, smart refactoring, unsafe code evolution, hardcoding elimination, and licensing formalization.

## Changes

### Build Optimization

- `.cargo/config.toml` added: `LTO=thin`, `codegen-units=1`, `strip=symbols` (release)
- coral-gpu inherits workspace pedantic+nursery lints (33 findings resolved)

### Code Quality

- Unsafe surface reduced: `DmaBufferBytes` abstracts raw DMA pointers; Send/Sync documented on 6 types
- All `unsafe` blocks verified with `// SAFETY:` comments
- `#[allow]` evolved to `#[expect]` where lint expectations are guaranteed

### Refactoring

- `pci_discovery.rs` → 7 submodules; `uvm_compute.rs` → 5 submodules (all under 1000 LOC)

### Coverage

- 4318 → 4407 tests (+89), 0 failures
- Key coverage gains: coral-ember `handlers_journal` (0%→77%), coral-glowplug `error.rs` expanded

### Hardcoding Evolution

- TCP bind addresses now env-overridable: `CORALREEF_EMBER_TCP_HOST`, `CORALREEF_NEWLINE_TCP_HOST`
- All IPC endpoints configurable for capability-based discovery

### Licensing

- ORC license component formalized (`LICENSE-ORC`) for scyBorg Provenance Trio compliance

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 4318 | 4407 |
| Failures | 0 | 0 |
| Clippy warnings | 0 | 0 |
| Files > 1000 LOC | 2 | 0 |
| unsafe blocks (coral-driver) | ~24 | ~24 (documented + `DmaBufferBytes` abstraction) |

## Impact on Other Primals

- **toadStool**: New env vars for TCP binding affect toadStool → coralReef IPC when not using UDS
- **barraCuda**: Zero-copy at compile output confirmed; `Bytes::from(Vec<u8>)` at call sites is the correct handoff
- **hotSpring**: Hardware validation unaffected; all existing APIs preserved

## Open Items (Phase 11)

- coral-driver: ~1980 pedantic/nursery findings when workspace lints inherited (separate iteration)
- Coverage: ~65% line coverage; 90% target requires hardware-gated test mocking expansion
- SSARef arena/interning for clone elimination (architectural change)
- Intel backend placeholder

---

**Previous handoff**: [Iter 73 — Logic/IO Untangling + Test Consolidation](CORALREEF_ITER73_LOGIC_IO_UNTANGLING_HANDOFF_APR04_2026.md)
