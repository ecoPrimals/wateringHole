<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0 — MethodGate JH-0 Implementation Handoff

**Date**: May 11, 2026
**Session**: BB
**Audit Source**: primalSpring stadial audit (May 11, 2026)
**Finding**: SQUIRREL — MethodGate (JH-0) Missing (only real gap blocking 13/13)

## Resolution

Implemented the ecosystem-standard pre-dispatch capability gate, bringing Squirrel
to full primalSpring gate compliance (13/13 primals through).

### What Was Implemented

1. **`crates/main/src/rpc/method_gate.rs`** (~230 lines + 25 tests)
   - `MethodVisibility` enum: `Public` / `Protected`
   - `GateMode` enum: `Permissive` / `Enforcing`
   - `classify_method()` — ecosystem-standard classification:
     - Public: `health.*`, `system.*`, `identity.get`, `capabilities.*`,
       `capability.*`, `lifecycle.status`, `discovery.*`, `auth.*`, `provenance.*`
     - Protected: `ai.*`, `inference.*`, `tool.*`, `context.*`, `graph.*`,
       `lifecycle.register`, `provider.*`, `btsp.*`
   - `MethodGate::check_with_context()` — full JH-0/JH-2 pre-dispatch check
   - `CallerContext` — identity + optional ResourceEnvelope (JH-2 prep)
   - `ResourceEnvelope` — mem_mb, cpu_cores, max_timeout_ms, method_allowlist (JH-2 prep)
   - Error codes: `UNAUTHORIZED` (-32000), `PERMISSION_DENIED` (-32001)

2. **Dispatch wiring** (`crates/main/src/rpc/jsonrpc_request_processing.rs`)
   - Gate inserted in `handle_single_request_object` before `dispatch_jsonrpc_method`
   - Applies to both notification and request paths
   - Uses `normalize_method()` so `squirrel.*` and `mcp.*` prefixed methods resolve correctly

3. **Shipped in `GateMode::Permissive`** — no behavioral change (JH-0 ecosystem default)

### Reference Implementations Consulted

- toadStool: `primals/toadStool/crates/server/src/pure_jsonrpc/handler/method_gate.rs`
- primalSpring: `springs/primalSpring/ecoPrimal/src/ipc/method_gate.rs`
- Standard: `springs/primalSpring/wateringHole/METHOD_GATE_STANDARD.md`

### Test Coverage

25 new unit tests covering:
- `classify_method` for all public groups (health, system, identity, capabilities,
  lifecycle, discovery, auth prefix, provenance prefix)
- Protected methods (ai, inference, tool, context, graph, provider, btsp)
- Permissive mode allows all (public + protected + prefixed)
- Enforcing mode: public passes, protected rejects with UNAUTHORIZED
- Enforcing mode: protected with identity passes
- ResourceEnvelope allowlist enforcement in both modes
- CallerContext anonymous construction
- GateMode reporting

### Quality Gate Results

| Metric | Result |
|--------|--------|
| `cargo fmt --all` | PASS |
| `cargo clippy -p squirrel` | ZERO warnings |
| `cargo test --workspace` | 7,203 pass / 0 fail |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

### Future Work (JH-2)

- Wire `CallerContext` from `_bearer_token` JSON-RPC params field
- Implement `BearDogVerifier` integration for `EnforcementMode::Enforcing`
- Thread `ResourceEnvelope` into dispatch handlers for numeric limit enforcement
- Switch `GateMode` to `Enforcing` when ecosystem declares JH-2 ready

### Ecosystem Impact

This resolves the **only remaining gap** identified in the primalSpring stadial audit.
All 13 primals now have method_gate.rs implementing the JH-0 standard.
