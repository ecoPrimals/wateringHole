# NestGate v4.7.0-dev Session 51 Handoff

**Date**: May 2, 2026
**Session**: 51
**Trigger**: primalSpring audit (BTSP Phase 3 wiring gaps) + deep debt sweep continuation

---

## Summary

Two commits resolving the last BTSP Phase 3 wiring gaps and executing a deep
debt sweep across the codebase.

---

## What Changed

### BTSP Phase 3 Wiring (3 gaps closed)

primalSpring audit identified three plumbing gaps preventing the existing
`btsp_phase3/` modules (505+509 LOC, 28 tests) from compiling into the module tree.

1. **Module declaration**: `pub mod btsp_phase3;` added to `rpc/mod.rs`
2. **Workspace deps**: `hkdf = "0.12"`, `zeroize = { version = "1", features = ["derive"] }` added to workspace and `nestgate-rpc` Cargo.toml
3. **Accept path wiring**: `post_handshake_phase3_or_plaintext()` intercepts the first post-handshake message in both `unix_socket_server` and `isomorphic_ipc/server` — if `btsp.negotiate`, derives session keys and enters encrypted frame loop; otherwise dispatches normally and falls through to plaintext

Also: `resolve_family_seed()` promoted from private to `pub(crate)` for cross-module access.

### Deep Debt Sweep

- **Commented-out code removed**: `pool.rs` (46-line `/* */` HTTP block), `operations.rs` (S3 SDK stub), `production_capability_bridge.rs` (K8s/Consul future backends)
- **Hardcoded primal name**: `auth_mode == "beardog"` replaced with agnostic `"external"` alias in CLI
- **Stale features removed**: `btsp = []` (nestgate-rpc, never `#[cfg]`-gated), `cli = []` (nestgate-installer, never gated)
- **Visibility narrowed**: `pub mod protocol` → `pub(crate) mod protocol` (only used internally)
- **Lint scoping**: nestgate-bin 6 → 4 crate-level lints (`cast_precision_loss` scoped to display expressions with reasons, `items_after_statements` fixed by hoisting import)
- **Installer Cargo.toml**: BearDog reference in dep comment evolved to "security capability provider"

### Audit Outcomes (no action needed)

- **nestgate-performance** (11 lints): All legitimate — 378 `module_name_repetitions` would require mass API rename
- **nestgate-config** (4 lints): All well-justified with reasons — structural for config DTOs
- **Hardcoded ports** (8080/8081): Already env-driven via `env_var_or_default("NESTGATE_API_PORT", "8080")` — sensible fallback defaults, not hardcoding
- **No files >800L**, no unsafe code, no TODO/FIXME/HACK, no C/C++ deps, no `#[allow]` in production

---

## Verification

```
cargo fmt --all --check          PASS
cargo clippy --workspace         PASS (zero own-code warnings)
  --all-targets -- -D warnings
cargo test --workspace --lib     8,869 passing / 0 failures / 60 ignored
```

---

## Downstream Impact

- **BTSP Phase 3**: Now fully wired — springs can negotiate encrypted channels via `btsp.negotiate` against NestGate
- **Auth mode**: `NESTGATE_AUTH_MODE=beardog` no longer recognized; use `delegated` or `external`
