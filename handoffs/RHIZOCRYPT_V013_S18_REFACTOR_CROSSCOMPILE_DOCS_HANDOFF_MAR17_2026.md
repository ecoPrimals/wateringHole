# rhizoCrypt v0.13.0-dev — Session 18 Handoff (Final)

**Date**: March 17, 2026
**Sessions**: 17–18 (combined handoff)
**Scope**: Sovereignty, smart refactoring (6 file extractions), 14-crate ecoBin deny, cross-compile CI, RUSTSEC fix, docs cleanup

---

## Changes Delivered

### Session 17

1. **`health.liveness` + `health.readiness` JSON-RPC Methods** — K8s/biomeOS probes
2. **4-Format Capability Parsing** (airSpring v0.8.7 / toadStool S155+)
3. **`ValidationSink` Trait** (ludoSpring V22) — pluggable output for `ValidationHarness`
4. **JSON-RPC Proptest Fuzz** — 7 property tests
5. **4-Format Capability Proptest** — 4 property tests
6. **`deny.toml` Yanked Crate Hardening** — `yanked = "deny"`

### Session 18

1. **Primal Sovereignty — `provenance-trio-types` Eliminated**
   - Removed compile-time dependency on shared crate (boundary violation)
   - Created `dehydration_wire.rs` with rhizoCrypt-owned wire types
   - JSON wire format is identical — zero breaking change for receivers
   - See separate handoff: `RHIZOCRYPT_PROVENANCE_TRIO_TYPES_SOVEREIGNTY_RESOLUTION_MAR17_2026.md`

2. **Smart File Refactoring — 6 Extractions**
   - `error.rs`: 863 → 660 lines (→ `validation.rs`, 236 lines)
   - `registry.rs`: 886 → 399 lines (→ `registry_tests.rs`, 452 lines)
   - `nestgate_http.rs`: 729 → 325 lines (→ `nestgate_http_tests_wiremock.rs`, 407 lines)
   - `signing.rs`: 758 → 408 lines (→ `signing_tests.rs`, 353 lines)
   - `niche.rs`: 732 → 514 lines (→ `niche_tests.rs`, 221 lines)
   - All files under 1000-line limit (max: 867)

3. **`deny.toml` Full ecoBin v3.0 Ban List** — 7 → 16 banned C-sys crates
   - Added: `openssl-src`, `cmake`, `cc`, `bindgen`, `bzip2-sys`, `curl-sys`, `libz-sys`, `pkg-config`, `vcpkg`
   - `cc` allowed as wrapper for `ring` and `blake3` (build-time only)

4. **RUSTSEC-2026-0049 Fix** — `rustls-webpki` 0.103.8 → 0.103.10

5. **`RHIZOCRYPT_JSONRPC_PORT` Configuration**
   - `JSONRPC_PORT_OFFSET` constant + `SafeEnv::get_jsonrpc_port()` with env override

6. **Cross-Compile CI (ecoBin v3.0)**
   - musl (x86_64, aarch64), RISC-V matrix job using `cross`

7. **Documentation Cleanup**
   - Fixed stale test counts across showcase, deployment checklist (→ 1330)
   - Fixed stale spec date (December 2025 → March 2026)
   - Fixed stale license identifier in spec (AGPL-3.0 → AGPL-3.0-or-later)
   - Removed dead `02-federation/` dir reference from showcase README
   - Updated ToadStool/workflows status in showcase README
   - Regenerated showcase Cargo.lock (removed stale provenance-trio-types)
   - Updated PRIMAL_REGISTRY.md and genomeBin manifest

---

## Current State

| Metric | Value |
|--------|-------|
| Tests | 1330 passing (`--all-features`) |
| Coverage | 92.32% (`--fail-under-lines 90` CI gate) |
| Clippy | 0 warnings (pedantic + nursery + cargo) |
| Doc | 0 warnings (`-D warnings`) |
| cargo deny | advisories ok, bans ok, licenses ok, sources ok |
| SPDX | 128 `.rs` files |
| Max file | 867 lines (all under 1000) |
| Unsafe | `deny` workspace-wide, zero in tests (temp-env) |
| Cross-compile | musl (x86_64, aarch64), RISC-V |
| Cross-primal deps | Zero (sovereign wire types) |

---

## Audit Summary (Clean)

| Check | Result |
|-------|--------|
| TODO/FIXME/HACK/XXX in `.rs` | None |
| `unsafe` blocks in code | None (only in a doc comment) |
| unwrap/expect in production | None |
| Mocks in production | None (all `#[cfg(test)]` or `test-utils` gated) |
| Hardcoded primal names in prod | None (only module names and tests) |
| `#[allow(` in production | None (only `cfg_attr(test, ...)`) |
| `#[deprecated` annotations | None |
| `#[allow(dead_code)]` in prod | None (only test harness) |

---

## For Other Primals

- `provenance-trio-types` shared crate should be archived — rhizoCrypt has inlined its wire types; loamSpine and sweetGrass should do the same
- 14-crate ecoBin deny list is available for adoption by other primals
- `health.liveness` + `health.readiness` probe pattern available for ecosystem standardization
- 4-format capability parsing handles all known response formats across the ecosystem
- Cross-compile CI pattern (musl + RISC-V) available as template
