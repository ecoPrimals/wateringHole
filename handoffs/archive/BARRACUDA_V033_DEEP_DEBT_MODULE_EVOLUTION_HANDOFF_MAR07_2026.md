# barraCuda v0.3.3 — Deep Debt + Module Evolution Handoff

**Date**: March 7, 2026
**From**: barraCuda
**To**: toadStool, coralReef, hotSpring, wetSpring, neuralSpring, airSpring, groundSpring

---

## Summary

barraCuda completed a deep debt resolution pass, module decomposition of the
two largest files, coralReef Phase 10 IPC alignment, and comprehensive lint
hardening. All quality gates green: `cargo fmt`, `cargo clippy -D warnings`,
`RUSTDOCFLAGS="-D warnings" cargo doc`, `cargo deny`, `cargo check` for
three feature configurations.

---

## What Changed

### Smart Module Decomposition

Two monolithic files were decomposed into semantically cohesive modules:

| Before | After | Submodules |
|--------|-------|------------|
| `device/coral_compiler.rs` (735 lines) | `device/coral_compiler/` | `mod.rs` (client), `types.rs` (wire types), `discovery.rs` (capability scan), `cache.rs` (native binary cache), `jsonrpc.rs` (transport) |
| `shaders/provenance.rs` (767 lines) | `shaders/provenance/` | `mod.rs` (re-exports), `types.rs` (ShaderRecord, SpringDomain), `registry.rs` (static registry + queries), `report.rs` (evolution_report) |

Public API unchanged — all re-exports preserved in `mod.rs`.

### coralReef Phase 10 IPC Alignment

| Old Method | New Method (Phase 10) | Purpose |
|------------|----------------------|---------|
| `compiler.health` | `shader.compile.status` | Health probe |
| `compiler.compile` | `shader.compile.spirv` | SPIR-V → native |
| `compiler.compile_wgsl` | `shader.compile.wgsl` | WGSL → native |
| — | `shader.compile.capabilities` | Architecture enumeration |

- Backward-compat fallback for pre-Phase 10 coralReef in `probe_jsonrpc()`
- Discovery capability scan: `shader.compile` (Phase 10) → `shader_compiler` (legacy) → well-known filename
- AMD RDNA2 (`gfx1030`), RDNA3 (`gfx1100`), CDNA2 (`gfx90a`) architecture mappings added

### Lint Hardening

- **40+ `#[allow(dead_code)]` documented** — all CPU reference implementations carry
  `reason = "CPU reference implementation for GPU parity validation"` parameter
- **`#[expect]` vs `#[allow]` strategy** — `#[expect]` for clippy lints that definitely fire;
  `#[allow]` for `dead_code` on CPU references (avoids `unfulfilled_lint_expectations`
  when `--all-targets` compiles test code) and non-firing clippy lints
- **Zero undocumented suppressions** across the entire codebase

### Hardcoding Evolution

| Before | After | Location |
|--------|-------|----------|
| Magic number `1024` | `DENSE_CPU_THRESHOLD` named constant | `workload.rs`, `npu_bridge.rs` |
| Hardcoded `"coralreef-core.json"` | `LEGACY_DISCOVERY_FILENAME` const | `coral_compiler/discovery.rs` |
| `unreachable!()` bare | `unreachable!("descriptive message")` | `fhe_chaos_expanded.rs` |

### Test Strengthening

- 5 `coral_compiler` tests evolved from `let _ = result` to conditional assertions
  for graceful degradation and valid response types
- New `test_connection_state_transitions` test
- `#[ignore]` test without reason now has documented reason
- IPC capability versions bumped to `0.3.3`

### Documentation

- `CHANGELOG.md` — full session entries under "Changed — coralReef Phase 10 IPC Alignment"
- `STATUS.md` — updated module references and debt items
- `WHATS_NEXT.md` — stale `coral_compiler.rs` → module references fixed
- `README.md` — sibling repos updated to include coralReef and toadStool
- `test-tiered.sh` — test count updated

---

## Quality

- Zero `unsafe` blocks
- Zero clippy warnings (pedantic + `unwrap_used`)
- Zero rustdoc warnings
- Zero `cargo deny` findings
- All `#[allow]` and `#[expect]` carry `reason` parameters
- Zero TODOs, FIXMEs, HACKs, or `unimplemented!()`

---

## For Other Primals

### toadStool
- barraCuda IPC capability versions now at `0.3.3` — toadStool version checks should
  accept `>=0.3.3` for `gpu.compute`, `tensor.ops`, `gpu.dispatch`
- `coral_compiler/` module structure stable for toadStool integration

### coralReef
- barraCuda now uses `shader.compile.*` methods exclusively (with backward-compat fallback)
- `capabilities()` method prefers `shader.compile.capabilities` over health-response arch parsing
- AMD architecture strings (`gfx1030`, `gfx1100`, `gfx90a`) ready for multi-vendor testing

### Springs
- No API changes — all provenance and workload APIs remain stable
- Module decomposition is internal; public re-exports unchanged

---

*Deep debt resolved. Modules clean. IPC aligned. All gates green.*
