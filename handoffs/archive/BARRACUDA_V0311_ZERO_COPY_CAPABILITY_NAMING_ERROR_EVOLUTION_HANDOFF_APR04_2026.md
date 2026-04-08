# barraCuda v0.3.11 — Sprint 28: Zero-Copy ESN, Capability Naming & Error Evolution

**Date**: 2026-04-04
**Primal**: barraCuda
**Version**: 0.3.11
**Session**: Sprint 28

---

## Summary

Targeted deep debt evolution session focused on three patterns discovered by comprehensive
codebase sweep: unnecessary Tensor clones in ESN model, hardcoded sibling primal name in
runtime logs, and flattened io::Error source chain in tarpc transport. All changes verified
against full quality gate suite.

---

## Changes

### 1. Zero-Copy ESN matmul Evolution

**File**: `crates/barracuda/src/esn_v2/model.rs`

5 instances of `Tensor::clone().matmul(other)` evolved to `matmul_ref(other)`:
- `self.w_in.clone().matmul(input)` → `self.w_in.matmul_ref(input)` (forward pass)
- `self.w_res.clone().matmul(&self.state)` → `self.w_res.matmul_ref(&self.state)` (forward pass)
- `states_tensor.clone().matmul(&w_out)` → `states_tensor.matmul_ref(&w_out)` (ridge regression)
- `states.clone().matmul(&w_out)` → `states.matmul_ref(&w_out)` (SGD loop)
- `states_t.clone().matmul(&diff)` → `states_t.matmul_ref(&diff)` (SGD gradient)

**Rationale**: `matmul(self, other)` consumes ownership but delegates to `matmul_ref(&self, other)`.
The clones were allocating and copying entire tensors only to immediately borrow them. Zero semantic
change, pure waste elimination.

### 2. Capability-Based Sovereign Naming

**File**: `crates/barracuda/src/device/wgpu_device/compilation.rs`

4 runtime/doc references to "coralReef" neutralized to capability-based language:
- `tracing::warn!` message: "requesting coralReef sovereign compilation" → "requesting sovereign shader compilation"
- Code comments: "coralReef: adapter-aware" → "Sovereign shader compiler: adapter-aware"
- Doc comments: "source to coralReef for sovereign compilation" → "source to the sovereign shader compiler"

**Principle**: Primal code only has self-knowledge. Discovery of sibling primals happens at runtime
via capability scanning. Module-level doc comments (architectural fossil record) preserved.

### 3. Error Source Chain Preservation

**File**: `crates/barracuda-core/src/ipc/transport.rs`

tarpc TCP listener bind error evolved from:
```rust
.map_err(|e: std::io::Error| BarracudaError::Internal(e.to_string()))
```
to bare `?` — leverages existing `BarracudaCoreError::Io(#[from] std::io::Error)` to preserve
full error source chain. The `to_string()` was destroying the `io::ErrorKind`, source error,
and backtrace that `#[from]` preserves automatically.

---

## Quality Gate Results

| Gate | Status |
|------|--------|
| `cargo clippy --workspace` (pedantic + nursery) | CLEAN |
| `cargo fmt --check` | CLEAN |
| `cargo test --workspace` | 4,446 passing, 0 failures |
| `#[allow(]` suppressions | ZERO (all `#[expect(` with reason) |
| `todo!()` / `unimplemented!()` | ZERO |
| Production `.unwrap()` | ZERO |
| Files > 1000 lines | ZERO |
| `println!` in library code | ZERO |
| Mock implementations in production | ZERO |
| Hardcoded sibling primal names (runtime) | ZERO |
| Temp/backup/archive debris | ZERO |

---

## Metrics (unchanged)

- **Rust source files**: 1,113
- **WGSL shaders**: 824
- **Total tests**: 4,600+ (4,446 passing on llvmpipe + ~204 GPU-gated ignored)
- **Line coverage**: 80.54% (llvmpipe)

---

## Debris Audit

Comprehensive sweep confirmed:
- No `archive/` directory exists
- No `.tmp`, `.bak`, `.swp`, `.orig` files
- No stale scripts (only `scripts/test-tiered.sh` — valid, well-structured test dispatch)
- No TODO/FIXME/HACK markers in Rust code (single hex-value false positive: `0x03xxxx`)
- Doc-level "TODO/FIXME" references are all self-describing audit language ("zero TODO/FIXME")

---

## Open Gaps

None introduced. All existing gaps remain as documented in STATUS.md:
- P0: VFIO dispatch hardware revalidation on Titan V
- P1: DF64 end-to-end NVK hardware verification
- P1: coralReef sovereign compiler evolution
- P2: Coverage 80.54% → 90% (requires discrete GPU hardware)

---

## Cross-Primal Impact

No cross-primal impact. Changes are internal to barraCuda's ESN model, compilation pipeline
log messages, and core transport error handling.
