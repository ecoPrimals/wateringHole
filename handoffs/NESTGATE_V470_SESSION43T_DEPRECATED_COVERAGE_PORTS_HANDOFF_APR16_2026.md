# NestGate v4.7.0-dev — Session 43t Handoff

**Date**: April 16, 2026
**Session**: 43t (deep debt — deprecated pruning, coverage, hardcoded ports, unwrap triage)

---

## Summary

Continued deep debt execution addressing primalSpring April 16 audit items.
All verification gates green: fmt, clippy (pedantic+nursery), doc, deny, tests (8,627/0),
coverage 83.86%, zero files over 800 lines.

---

## Work Completed

### 1. Deprecated APIs: 133 → 116

| Crate | Items Removed | Details |
|-------|---------------|---------|
| nestgate-core | 15 | `config_registry/network.rs` module (9 structs), `SecurityPrimalProvider`, `ZeroCost*` security, `HealthCheck` alias, `NetworkServiceConfig` struct |
| nestgate-config | 2 | `ApiPathsConfig` vertical (6 items), `ServicesConfig::capability_url_or_local` |

Remaining 116 are active compat shims with live production callers.

### 2. Hardcoded Ports Evolved

5 files in nestgate-config migrated from literal port numbers (8080, 8443, 9090,
3000, 5432) to `runtime_fallback_ports::*` named constants with `#[expect(deprecated)]`
for intermediate migration.

### 3. Coverage: 82.94% → 83.86%

Tests added for 15+ lowest-coverage production files across 8 crates. 8,627 tests
passing, 0 failures.

### 4. Production Quality

- Zero `#[allow]` in non-test production code (last evolved to `#[expect]`)
- Zero `#[deprecated]` dead callers
- Zero unsafe code, zero `-sys` crates, zero `extern "C"`
- `NoopStorage` null-object pattern documented
- `.unwrap()`/`.expect()` triage: ~2700 instances confirmed test-only;
  production uses `?`/`map_err`

---

## Items for primalSpring to Update

1. **ECOSYSTEM_COMPLIANCE_MATRIX**: NestGate deprecated count → 116, tests → 8,627,
   coverage → 83.86%.
2. **PRIMAL_GAPS.md**: Coverage 83.86% → 90% still tracked. Deprecated 116 (active shims).
3. **UPSTREAM_GAP_STATUS**: All prior NestGate gaps remain RESOLVED. Vendored
   rustls-rustcrypto still needed (upstream 0.0.2-alpha unchanged).

---

## Verification

```
Build:    cargo check --workspace                                    PASS
Clippy:   cargo clippy --workspace --lib -- pedantic+nursery         0 warnings
Format:   cargo fmt --check                                          PASS
Docs:     cargo doc --workspace --no-deps                            PASS
Deny:     cargo deny check                                           advisories ok, bans ok, licenses ok, sources ok
Tests:    cargo test --workspace --lib                               8,627 passed, 0 failed, 60 ignored
Coverage: cargo llvm-cov --workspace --lib --summary-only            83.86% line
Files:    find . -name '*.rs' | xargs wc -l | awk '$1>800'          0 files
#[allow]: rg '#[allow(' production                                   0 matches
```

---

## Remaining Evolution Targets

- Coverage 83.86% → 90%
- 116 deprecated markers (active compat shims, migrate one vertical at a time)
- Vendored `rustls-rustcrypto` — track upstream for drop opportunity
