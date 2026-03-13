<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — Deep Debt, Coverage Push, ecoBin Verification Handoff

**Date**: March 13, 2026 (session 2)
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Deep debt resolution + coverage expansion + infrastructure hardening

---

## Summary

Comprehensive audit and execution pass covering deep technical debt, modern
idiomatic Rust evolution, coverage expansion, dependency audit, and
infrastructure hardening.

1. **862 tests passing** (was 600) — +262 new tests across all HTTP clients,
   storage backends, JSON-RPC handlers, discovery registry, and service library.

2. **87.78% line coverage** (llvm-cov) — remaining 2.2% gap is in DB error
   paths requiring corruption injection and the binary entry point.

3. **ecoBin verified** — zero application C dependencies in default build.
   `blake3 pure`, `rustls-tls`, no project `build.rs` invoking C compilers.

4. **cargo-deny enforced** — `deny.toml` configured for advisories, licenses
   (AGPL-3.0-only + permissive transitive), bans, and sources.

5. **Service library extracted** — `rhizocrypt-service` now has both `lib.rs`
   and `main.rs`; server logic is testable without subprocess.

6. **All files under 1000 lines** — extracted test modules from `handler.rs`
   (1008 → 481) and `loamspine_http.rs` (1007 → 703).

7. **Mock isolation confirmed** — all mock types gated behind
   `#[cfg(any(test, feature = "test-utils"))]`. Zero mock code in production.

8. **Documentation cleaned** — removed stale VERIFICATION_CHECKLIST.md,
   stale SHOWCASE_INDEX.md, broken doc links, outdated test/coverage counts.

---

## Changes

### Coverage Expansion (600 → 862 tests)

| Module | New Tests | Focus |
|--------|-----------|-------|
| `store_sled.rs` | +20 | exists, export, batch, concurrent, frontier, genesis |
| `clients/loamspine_http.rs` | +15 | JSON-RPC response, serde, method negotiation |
| `clients/toadstool_http.rs` | +12 | deployment parsing, event conversion, serde |
| `clients/nestgate_http.rs` | +10 | blob storage serde, error display, source chain |
| `clients/beardog_http.rs` | +10 | signing serde, DID document, error chain |
| `jsonrpc/mod.rs` | +7 | invalid UTF-8, empty batch, wrong version |
| `jsonrpc/handler.rs` | existing | extracted to `handler_tests.rs` |
| `discovery/registry.rs` | +6 | capability parsing, unhealthy filtering |
| `rhizocrypt-service/lib.rs` | +6 | bind addr, error display, discovery |

### Infrastructure

| Item | Detail |
|------|--------|
| `deny.toml` | cargo-deny 0.19 config: advisories, licenses, bans, sources |
| Allowed licenses | AGPL-3.0-only, MIT, Apache-2.0, BSD-2/3, ISC, Unicode-3.0, BSL-1.0, CDLA-Permissive-2.0 |
| Ignored advisories | 5 transitive unmaintained (tarpc → bincode, fxhash, instant, opentelemetry) |
| Wildcards | Allowed for internal workspace path deps |
| SPDX headers | All `.rs` files verified |

### File Size Compliance

| File | Before | After | Method |
|------|--------|-------|--------|
| `handler.rs` | 1008 | 481 | Extracted tests to `handler_tests.rs` |
| `loamspine_http.rs` | 1007 | 703 | Extracted tests to `loamspine_http_tests.rs` |

### Service Library

- `rhizocrypt-service` now has `[lib]` in Cargo.toml
- `lib.rs` exports: `run_server`, `resolve_bind_addr`, `register_with_discovery`,
  `print_version`, `print_status`, `ServiceError`
- `main.rs` is a thin CLI wrapper (80 lines)

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-features --all-targets -- -D warnings` | Clean |
| `cargo doc --workspace --all-features --no-deps` | Clean |
| `cargo test --workspace --all-features` | 862 pass, 0 fail |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `#![forbid(unsafe_code)]` | Workspace-wide |
| SPDX headers | All `.rs` files |
| Max file size | All under 1000 lines |
| Line coverage (llvm-cov) | 87.78% |

---

## For Other Primals

- **LoamSpine**: rhizoCrypt's `LoamSpineHttpClient` uses method negotiation
  (native `commit.session` → compat `permanent-storage.commitSession`).
  LoamSpine should support both method name sets.

- **Songbird**: rhizoCrypt queries `discovery.resolve` via JSON-RPC over
  HTTP/1.1. Songbird should return endpoints with capability names matching
  `Capability` enum variants.

- **All primals**: rhizoCrypt uses capability-based env vars
  (`PERMANENT_STORAGE_ENDPOINT`, `SIGNING_ENDPOINT`, etc.) and discovers
  via `RHIZOCRYPT_DISCOVERY_ADAPTER`. No primal-specific env vars remain.

---

## Known Constraints

- Coverage ceiling at ~88% without HTTP mock server infrastructure (e.g.
  `wiremock`) for client network methods, DB corruption injection for
  `store_redb` error paths, and subprocess testing for `main.rs`.

- `tarpc` pulls 5 unmaintained transitive dependencies (tracked in
  `deny.toml`). These are not under rhizoCrypt's control.

---

## Next Steps

- Wire redb backend into service binary `start()` for persistent mode
- Add `wiremock` for HTTP client integration tests (push past 90%)
- Expand property-based testing (proptest) for DAG operations
- Integrate sweetGrass provenance trait for RootPulse coordination
- Evolve tarpc transport to reduce unmaintained transitive deps
