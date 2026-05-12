# petalTongue v1.6.6 — SPA Catch-All + CORS (Composition Readiness)

**Date:** May 11, 2026
**Scope:** SPA client-side routing, CORS production config, composition readiness
**Status:** RESOLVED (petalTongue-owned items). NestGate transport parity remains blocked.

---

## Context

primalSpring stadial gate audit (May 11) identified two petalTongue-owned items
that can ship independently of NestGate's `content.*` transport parity:

1. SPA catch-all route for client-side routing
2. Production `WebServeConfig` with CORS (`allowed_origins`)

## Fixes

### `--spa` / `PETALTONGUE_SPA` — SPA Catch-All

When enabled, missing paths in the docroot fallback serve `{docroot}/index.html`
instead of 404. Standard SPA behavior for React/Vue/Svelte/etc. client-side
routing where the JS app handles URL dispatch.

- CLI: `petaltongue web --docroot ./dist --spa`
- Env: `PETALTONGUE_SPA=true`
- Config: `[web] spa = true`
- Implementation: `serve_spa_index()` reads `index.html` on 404 from `ServeDir`

### `--allowed-origins` / `PETALTONGUE_ALLOWED_ORIGINS` — CORS

Production CORS configuration via `tower_http::cors::CorsLayer`.

- CLI: `--allowed-origins https://primals.eco,http://localhost:3000`
- Env: `PETALTONGUE_ALLOWED_ORIGINS=https://primals.eco,http://localhost:3000`
- Wildcard: `--allowed-origins '*'`
- Config: `[web] allowed_origins = ["https://primals.eco"]`
- Methods: GET, POST, OPTIONS
- Headers: Content-Type, Authorization

### Config + Schema

- `WebServeConfig.spa: bool` (default `false`)
- `WebServeConfig.allowed_origins: Vec<String>` (default empty = same-origin)
- TOML merge, env override, CLI precedence all wired

## Blocked: NestGate Transport Parity

`backend=nestgate` calls `content.resolve` over UDS. This works when NestGate's
primary `unix_socket_server` dispatch path is directly reachable. However,
NestGate's `content.*` methods are **not routed** through `SemanticRouter`,
isomorphic IPC, or HTTP API paths. Callers hitting those transport paths get
"Method not found."

petalTongue's NestGate integration is structurally complete — it will work the
moment NestGate ships transport parity. No petalTongue changes needed.

## Verification

```
cargo fmt --check     ✅ clean
cargo clippy -D warn  ✅ 0 warnings
cargo test --all      ✅ 222 tests pass (5 new: SPA, non-SPA 404, CORS tests)
```

## Files Changed

| File | Change |
|------|--------|
| `src/web_mode.rs` | SPA fallback, CORS layer, `serve_spa_index`, `build_cors_layer` |
| `src/main.rs` | `--spa`, `--allowed-origins` CLI flags |
| `crates/petal-tongue-core/src/config_system/types.rs` | `spa`, `allowed_origins` fields |
| `crates/petal-tongue-core/src/config_system/loader.rs` | Env overrides |
| `Cargo.toml` | `tower-http` `"cors"` feature |
| `CHANGELOG.md`, `CONTEXT.md`, `START_HERE.md` | Updated |
