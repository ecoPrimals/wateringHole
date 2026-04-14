# biomeOS v3.12 — Composition Forwarding Architecture + graph.list Fix

**Date**: 2026-04-14
**Source**: primalSpring benchScale validation (74-experiment sweep, April 14, 2026)
**Experiments affected**: exp095 (2 FAIL), exp060 (1 FAIL), exp001/004 composition checks, exp080 (1 FAIL)

---

## Gap 1: Forwarding Architecture (3 sub-problems → 4 fixes)

### Root cause

biomeOS resolved capability → primal socket and forwarded directly. This hit three problems:

1. **BTSP rejection**: beardog, rhizoCrypt, sweetGrass require BTSP handshake; biomeOS sent raw JSON-RPC → silent failure
2. **Socket path mismatch**: biomeOS scanned `/tmp/biomeos-default/` but deploy creates sockets in `/tmp/biomeos/`
3. **Method prefix**: biomeOS forwarded `{domain}.{operation}` but primals expect just `{operation}`

### Fixes applied

| Fix | File | Change |
|-----|------|--------|
| **Tower Atomic relay preference** | `handlers/capability.rs` | `capability.call` now tries Tower Atomic (Songbird relay + BearDog secure transport) first. Songbird handles BTSP, correct socket paths, and method translation. Falls back to direct routing only when Tower Atomic unavailable. |
| **Socket path scan** | `handlers/topology.rs` | Added `/tmp/biomeos` (FALLBACK_RUNTIME_BASE) as a regular scan directory (Priority 7). Previously only added as last-resort when no other dirs existed — now always scanned when present. |
| **Method prefix stripping** | `handlers/capability.rs` | Direct routing fallback now forwards just `{operation}` (not `{domain}.{operation}`). Target primal knows its own domain; primals needing specific method names register translations. |
| **BTSP failure visibility** | `neural_router/forwarding.rs` | BTSP handshake failure upgraded from `debug!` to `warn!` with socket path — silent failures now visible in production logs. |

### Architecture impact

```
BEFORE: capability.call → discover_capability → direct socket → (BTSP fail → raw JSON-RPC → rejected)
AFTER:  capability.call → Tower Atomic → Songbird relay (BTSP + correct paths + method translation)
                        ↘ fallback: discover_capability → direct socket → {operation} only
```

---

## Gap 2: graph.list returns [] (76 TOML files invisible)

### Root cause

`graph.list` used `std::fs::read_dir` (flat scan of immediate children only). Graphs organized in subdirectories were invisible.

### Fix applied

| Fix | File | Change |
|-----|------|--------|
| **Recursive directory scan** | `handlers/graph/mod.rs` | Added `collect_toml_files_recursive()` helper. `graph.list` now walks the full directory tree under both `graphs_dir` and `runtime_graphs_dir`. Added info-level logging showing directory paths and file counts for diagnostics. |

---

## Validation

- `cargo build` — clean
- `cargo clippy --workspace` — 0 warnings
- `cargo test --workspace` — 45 test suites, 0 failures
- `cargo fmt --all` — clean

## Expected downstream impact

Once primalSpring rebuilds on this commit:
- exp095, exp060, exp001/004 composition experiments should pass (forwarding via Tower Atomic relay)
- exp080 should pass (graph.list returns all 76 graphs from recursive scan)
- All BTSP handshake failures become visible via warn-level logs
