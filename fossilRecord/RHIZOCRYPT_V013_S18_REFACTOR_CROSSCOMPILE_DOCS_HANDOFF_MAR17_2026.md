# rhizoCrypt v0.13.0-dev — Session 18 Handoff

**Date**: March 17, 2026
**Sessions**: 17–18 (combined handoff)
**Scope**: Smart refactoring, cross-compile CI, JSON-RPC port config, documentation refresh

---

## Changes Delivered

### Session 17 (Earlier Today)

1. **`health.liveness` + `health.readiness` JSON-RPC Methods**
   - Zero-cost liveness probe, readiness probe with version + primal ID
   - Registered in all capability registries, wired into JSON-RPC handler

2. **4-Format Capability Parsing** (absorbed from airSpring v0.8.7 / toadStool S155+)
   - Handles flat strings, nested objects, wrapper objects, double-nested
   - Also handles `{"methods": [...]}` (coralReef variant)

3. **`ValidationSink` Trait** (absorbed from ludoSpring V22)
   - Pluggable output for `ValidationHarness` — `StderrSink`, `StringSink`
   - `finish_to(sink)` and `checks()` accessor

4. **JSON-RPC Proptest Fuzz** — 7 new property tests
5. **4-Format Capability Proptest** — 4 new property tests
6. **`deny.toml` Yanked Crate Hardening** — `yanked = "deny"`

### Session 18 (This Session)

1. **Smart File Refactoring — `validation.rs` Extraction**
   - `error.rs`: 863 → 660 lines
   - New `validation.rs`: 236 lines (canonical home for `ValidationHarness`)
   - Re-exported from both `error` and root for backward compat

2. **Smart File Refactoring — `registry_tests.rs` Extraction**
   - `discovery/registry.rs`: 886 → 399 lines
   - New `registry_tests.rs`: 452 lines (via `#[path]` attribute)

3. **`RHIZOCRYPT_JSONRPC_PORT` Configuration**
   - `JSONRPC_PORT_OFFSET` constant (default: +1 from tarpc port)
   - `SafeEnv::get_jsonrpc_port()` with env override support
   - `rhizocrypt-service` uses it instead of hardcoded offset

4. **Cross-Compile CI (ecoBin v3.0)**
   - New `cross-compile` matrix job: musl x86_64/aarch64, RISC-V
   - Uses `cross` for builds, validates default-features-only

5. **Dependency Evolution Documentation**
   - `ring` → `rustls-rustcrypto` path documented in `deny.toml`
   - `sled` deprecation status documented in Cargo.toml
   - tarpc transitive debt tracked

6. **Documentation Refresh**
   - README: 1327 tests, 124 SPDX files, ecoBin v3.0, cross-compile, `RHIZOCRYPT_JSONRPC_PORT`
   - CHANGELOG: sessions 17 + 18
   - `docs/ENV_VARS.md`: `RHIZOCRYPT_JSONRPC_PORT` added
   - `showcase/00_START_HERE.md`: fixed stale stats, removed dead `02-complete-workflows/` refs
   - Cleaned all stale date footers

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1327 passing (`--all-features`) |
| Coverage | 92.32% (`--fail-under-lines 90` CI gate) |
| Clippy | 0 warnings (pedantic + nursery + cargo) |
| Doc | 0 warnings (`-D warnings`) |
| SPDX | 124 `.rs` files |
| Max file | All under 1000 lines |
| Unsafe | `deny` workspace-wide, zero in tests (temp-env) |
| Cross-compile | musl (x86_64, aarch64), RISC-V |

---

## Dependency Evolution Status

| Current | Target | Status |
|---------|--------|--------|
| `ring` (via reqwest/rustls, opt-in) | `rustls-rustcrypto` | Waiting for stable release |
| `sled` (optional) | `redb` (default) | redb is default; sled retained for compat |
| tarpc transitives (fxhash, instant, bincode v1) | upstream fixes | tracked, non-blocking |

---

## Open Items for Future Sessions

1. **`GAPS_DISCOVERED.md`** — referenced in inter-primal showcase as a testing protocol artifact; created during live test runs, not stale
2. **`showcase/QUICK_START.sh`** — fallback `cargo run --example quick_demo` path is dead; works via binary path
3. **Coverage push** — 92.32% is healthy; remaining gap is DB error paths and binary entry point
4. **`songbird-config` ConfigMap** — k8s deployment references it; must be provided externally or documented

---

## For Other Primals

- rhizoCrypt now exposes `health.liveness` and `health.readiness` JSON-RPC methods for K8s/biomeOS probes
- Capability parsing handles 4+ response formats — no need to standardize across primals immediately
- `ValidationHarness` pattern is reusable — consider absorbing into shared crate
- Cross-compile CI validates ecoBin v3.0 compliance (musl, RISC-V targets)
- `RHIZOCRYPT_JSONRPC_PORT` env var allows explicit JSON-RPC port binding (default: tarpc + 1)
