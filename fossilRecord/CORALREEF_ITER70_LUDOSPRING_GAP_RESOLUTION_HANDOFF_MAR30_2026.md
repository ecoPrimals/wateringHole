# coralReef Iteration 70 — ludoSpring V35 Gap Resolution + Deep Audit

**Date**: March 30, 2026
**Primal**: coralReef (sovereign GPU compiler)
**Phase**: 10 — Iteration 70
**Triggered by**: `LUDOSPRING_V35_PRIMAL_COMPOSITION_GAP_DISCOVERY_HANDOFF_MAR30_2026.md`

---

## ludoSpring V35 Gap Resolution

### P1: UDS HTTP-wrapped framing → RESOLVED (Iter 69)

ludoSpring exp085 discovered coralReef wrapping JSON-RPC in HTTP on UDS.
This was already fixed in Iteration 69 (prior to V35 handoff):

- `unix_jsonrpc.rs` uses `process_newline_reader_writer()` — raw newline-delimited
- UDS socket at `$XDG_RUNTIME_DIR/biomeos/coralreef.sock` speaks raw protocol
- HTTP framing remains on TCP (jsonrpsee) for external consumers
- Newline-delimited TCP also available via `--port` flag

**Status**: Conformant. exp085 would pass on current code.

### P1: capability.register → RESOLVED (Iter 69)

`ecosystem.rs` already implements:
- Startup scan of `$XDG_RUNTIME_DIR/biomeos/*.json` for registries
- `capability.register` call to discovered Neural API socket
- `ipc.heartbeat` every 45s
- `BIOMEOS_ECOSYSTEM_REGISTRY` env override for explicit registry

**Status**: Conformant. Primals can route to coralReef via Neural API.

### P1: capabilities.list → NEW (Iter 70)

Added `capabilities.list` JSON-RPC method to both servers:
- Newline-delimited (UDS + TCP): `dispatch_jsonrpc` routes to `crate::capability::self_description()`
- jsonrpsee HTTP: `CoralReefRpc` trait method added

Returns: `["shader.compile", "shader.compile.multi", "shader.health"]`

biomeOS Neural API can now auto-discover coralReef's capabilities via standard probe.

### P2: Compile→dispatch E2E chain

The compile step (coralReef) is now reachable over raw newline UDS.
The dispatch step requires toadStool to implement `shader.dispatch` accepting
compiled binary over IPC — that's toadStool's gap, documented in V35 Part 4.

---

## Deep Audit Results

### Build Health

| Check | Status |
|-------|--------|
| `cargo fmt --check` | **PASS** |
| `cargo clippy --all-features -D warnings` | **PASS** |
| `cargo doc --all-features --no-deps` | **0 warnings** |
| Files > 1000 LOC (production) | **0** |

### Clippy Fixes (8 errors)

| Lint | File | Fix |
|------|------|-----|
| `branches_sharing_code` | `codegen/ops/mod.rs` | Hoisted `src_to_encoding(src0)` before branch |
| `branches_sharing_code` | `naga_translate/expr.rs` | Unified uniform/storage CBuf load paths |
| `redundant_clone` | `naga_translate/expr.rs` | Removed `.clone()` after `.cloned()` |
| `collapsible_if` | `coral-ember/lib.rs` | Collapsed to let-chain |
| `struct_excessive_bools` | `service/types.rs` | `#[allow]` with reason (1:1 f64 transcendental map) |
| `unused_variables` | `channel/mod.rs` | Prefixed with `_` |
| `dead_code` | `pfifo.rs` | `#[allow]` with reason (public API for experiments) |
| `missing_docs` | `rm_client/mod.rs` | Added doc comment |
| `too_many_arguments` | `rm_client/alloc.rs` | `#[expect]` with reason (RM API boundary) |
| `unfulfilled_lint_expectations` | `registers/falcon.rs` | Removed stale `#[expect(dead_code)]` |

### File Size Refactoring

| File | Before | After | Extracted to |
|------|--------|-------|-------------|
| `coral-ember/src/swap.rs` | 1102 | 708 | `swap_preflight.rs` (362) |
| `coral-driver/src/nv/vfio_compute/mod.rs` | 1018 | 855 | `gr_engine_status.rs` (173) |

### Pre-existing Test Regression (not ours)

2 tests (`corpus_euler_hll_f64_sm70`, `corpus_euler_hll_f64_rdna2`) fail with
SSA value assertion in upstream code. Confirmed pre-existing via `git stash` test.
Likely Rust 1.93 toolchain interaction — tracked for next compiler iteration.

---

## IPC Compliance Status (updated)

Per `IPC_COMPLIANCE_MATRIX.md` v1.2.0, coralReef status should be updated:

| Dimension | Matrix (stale) | Actual |
|-----------|---------------|--------|
| UDS Framing | P (HTTP-wrapped) | **C** (raw newline) |
| TCP Framing | HTTP (jsonrpsee) | **P** (HTTP + newline via `--port`) |
| Socket Path | P | **C** (`biomeos/coralreef.sock` + `shader.sock` symlink) |
| Health Names | ? | **C** (`health.liveness`, `health.readiness`, `health.check`) |
| `--port` | X | **C** (newline-delimited TCP) |
| `capabilities.list` | missing | **C** (added Iter 70) |
| Standalone | C | **C** |

---

## Files Changed

- 15 files modified across 4 crates
- 2 new files (gr_engine_status.rs, capabilities.list test)
- 1 oversize file split (swap.rs → swap.rs + swap_preflight.rs)
- 1 new JSON-RPC method (capabilities.list)

---

*Composition requires trust. Trust requires conformance. Conformance is tested, not claimed.*
