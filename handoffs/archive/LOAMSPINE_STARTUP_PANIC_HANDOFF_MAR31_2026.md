# loamSpine — Startup Panic (Runtime Nesting)

**Date**: March 31, 2026
**Priority**: P1 — CRITICAL → **RESOLVED** (v0.9.15)
**Reporter**: ludoSpring V37.1 live validation
**Cross-reference**: primalSpring `docs/PRIMAL_GAPS.md` LS-03
**Resolution**: `LOAMSPINE_V0915_DEEP_DEBT_EVOLUTION_LS03_FIX_HANDOFF_MAR31_2026.md`

---

## Problem

`loamspine server` panics at `crates/loam-spine-core/src/service/infant_discovery.rs:233`
with "Cannot start a runtime from within a runtime".

This is a Tokio anti-pattern: `block_on()` is called inside an already-running async
runtime context.

## Impact

- **1 experiment fully blocked**: exp095 (content ownership — requires all 4 primals:
  beardog + loamspine + rhizocrypt + sweetgrass)
- **+6 checks** will pass when both this AND rhizoCrypt UDS are fixed
- **Provenance trio broken** — loamSpine is the ledger component

## Required Fix

In `crates/loam-spine-core/src/service/infant_discovery.rs` around line 233:

Replace:
```rust
tokio::runtime::Runtime::new()?.block_on(async { ... })
```

With one of:
```rust
// Option A: spawn a task (preferred if in async context)
tokio::spawn(async { ... })

// Option B: spawn_blocking if sync context needs async result
tokio::task::spawn_blocking(|| { ... })
```

The async context already exists when `block_on` is invoked. The fix is to use the
existing runtime instead of trying to create a nested one.

## Validation

After fix:
```bash
loamspine server  # should not panic
echo '{"jsonrpc":"2.0","method":"health.liveness","id":1}' | socat - UNIX-CONNECT:/run/user/1000/biomeos/loamspine.sock
```
