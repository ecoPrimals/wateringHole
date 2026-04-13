<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — Deep Debt & Evolution Pass 2 Handoff

**Date**: April 12, 2026
**Version**: 0.9.16
**Tests**: 1,395 (0 failures)
**Source files**: 178 `.rs` (+ 3 fuzz targets)
**Coverage**: 90.92% line / 89.09% branch / 92.92% region

---

## Summary

Second deep debt evolution pass on LoamSpine v0.9.16, driven by primalSpring
downstream audit findings and continued cleanup of hardcoding, stale primal
name coupling, and inline test sprawl.

---

## Changes

### LD-09: TCP Opt-In (Port 8080 Crash Fix)

**Root cause**: `loamspine server` unconditionally bound `0.0.0.0:8080` for
HTTP JSON-RPC on startup. Port 8080 is commonly occupied in NUCLEUS
deployments, causing an immediate fatal crash that also prevented the UDS
socket from reaching readiness.

**Fix**: TCP transports (tarpc + JSON-RPC TCP) are now opt-in. They only start
when explicitly requested via `--port`/`--tarpc-port` CLI flags or
`LOAMSPINE_JSONRPC_PORT`/`LOAMSPINE_TARPC_PORT`/`USE_OS_ASSIGNED_PORTS`
environment variables. UDS socket is always the primary transport and starts
regardless of TCP configuration. Follows ToadStool/barraCuda pattern.

**New function**: `has_explicit_tcp_config()` in `constants::env_resolution`
detects whether any TCP-related env var is set.

**Test**: `has_explicit_tcp_config_default_without_env` verifies default
behavior returns false.

### Connection-Close Bug Fixed (primalSpring Audit Item)

**Root cause**: `handle_http_request` in JSON-RPC TCP server was single-shot —
wrote `Connection: close` after every HTTP response and returned. Clients had
to reconnect for each JSON-RPC call.

**Fix**: Evolved to HTTP/1.1 keep-alive loop. Server reads subsequent HTTP
requests on the same TCP connection until the client sends `Connection: close`
or EOF. NDJSON path was already persistent (unaffected).

**Tests**: `tcp_http_persistent_connection_keepalive` (3 sequential requests on
one socket) and `tcp_http_connection_close_header_respected` (verifies EOF after
client-requested close).

**Resolves**: primalSpring audit item — "loamSpine connection closes after first
response (workaround: call capabilities() before health_check())".

### BTSP Provider Decoupled from Hardcoded Primal Name

`BTSP_PROVIDER_PREFIX` ("beardog") evolved from hardcoded constant to
env-configurable `BTSP_PROVIDER` with "beardog" as default fallback.

- `BtspHandshakeConfig.beardog_socket` → `provider_socket`
- `beardog_socket_name()` → `provider_socket_name(family_id, provider_override)`
- `resolve_beardog_socket_with()` → `resolve_provider_socket_with(family_id, socket_dir, provider_override)`
- Backward-compatible `beardog_socket()` accessor retained
- 2 new tests for custom provider name resolution

### Smart Test Extraction (5 Files)

| File | Before → After | Extracted to |
|------|---------------|-------------|
| `streaming.rs` | 354 → 203 | `streaming_tests.rs` |
| `health.rs` | 482 → 347 | `health_tests.rs` |
| `service/mod.rs` | 438 → 277 | `service/service_mod_tests.rs` |
| `config.rs` | 370 → 285 | `config_tests.rs` |
| `lib.rs` | 532 → 374 | `lib_tests.rs` |

All using `#[path = "..."] mod tests;` pattern — zero churn, production code
cohesion preserved.

### Stale Primal Name Cleanup

All production doc comments referencing deprecated "Songbird" discovery primal
evolved to generic capability-based language across 7 files. Transport docs now
describe "capability-discovered HTTP provider" instead of coupling to a specific
primal.

### Additional Test Extraction

| File | Before → After | Extracted to |
|------|---------------|-------------|
| `traits/mod.rs` | 446 → 279 | `traits/mod_tests.rs` |

### Magic Number Timeouts Named

Bare `Duration::from_secs(N)` literals in production code replaced with named constants:

| File | Constant | Value |
|------|----------|-------|
| `transport/http.rs` | `CONNECT_TIMEOUT` | 5s |
| `transport/http.rs` | `READ_TIMEOUT` | 30s |
| `infant_discovery/mod.rs` | `DNS_SRV_TIMEOUT` | 2s |
| `infant_discovery/backends.rs` | `MDNS_TIMEOUT` | 2s |

### Clone Audit

Full production clone audit confirmed all `.clone()` calls are either `Arc`-based
O(1) reference counting or structurally necessary for owned captures in
`spawn_blocking`/retry closures. No unnecessary heap allocations in hot paths.

### Doc Infrastructure & Cleanup

- Broken `read_ndjson_stream_with` intra-doc link → `read_ndjson_stream_bounded`
- Root docs (README, CONTEXT, CONTRIBUTING) reconciled with STATUS.md metrics (1,383 tests, 176 source files)
- WHATS_NEXT.md updated with deep debt pass 3 entry
- Showcase stale Songbird references cleaned: capability table → "Capability discovery", tarpc description → "Structured RPC (JSON-over-TCP)"
- `QUICK_REFERENCE.md` date bumped to April 12, 2026
- `SHOWCASE_PRINCIPLES.md` date bumped, "Songbird service discovery" → "Capability-based service discovery"
- `00_START_HERE.md` conceptual Songbird refs → capability-based language (binary name refs preserved)
- Full debris sweep: zero empty files, zero build artifacts, zero stale TODOs, `.gitignore` covers all artifact patterns

---

## Gates

| Check | Status |
|-------|--------|
| `cargo fmt --all -- --check` | PASS |
| `cargo clippy --all-targets --all-features -- -D warnings` | PASS (0 warnings) |
| `cargo doc --no-deps` | PASS (0 warnings) |
| `cargo test --workspace` | PASS (1,383 tests, 0 failures) |
| `cargo deny check` | PASS (advisories, bans, licenses, sources ok) |

### Capability-Domain Symlink (Ecosystem Validation Pass)

**Gap identified**: `ECOSYSTEM_COMPLIANCE_MATRIX.md` flagged loamSpine as "No domain
symlink". Other primals (BearDog `crypto.sock`, Songbird `network.sock`,
coralReef `shader.sock`/`device.sock`) already have capability-domain symlinks
for biomeOS routing.

**Fix**: New `ledger.sock → permanence.sock` symlink created on bind, cleaned
up on graceful shutdown. Follows `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` Phase 2
pattern. Socket naming now three-tier:
- **Primary**: `permanence.sock` (domain-based)
- **Capability**: `ledger.sock` (biomeOS `by_capability = "ledger"` routing)
- **Legacy**: `loamspine.sock` (backward compat)

New code:
- `primal_names.rs`: `CAPABILITY_DOMAIN = "ledger"` constant
- `socket.rs`: `capability_domain_socket_name()`, `resolve_capability_symlink_path()`
- `main.rs`: Symlink creation/cleanup wired alongside legacy symlink
- 5 new tests (3 socket naming + 2 primal_names constants)

### Wire Standard Promotion

`CAPABILITY_WIRE_STANDARD.md` loamSpine row updated from "Partial / Partial —
Needs top-level `methods`, `identity.get`" to "✓ / ✓ — Full L3" with complete
attribute list. This was **stale** — loamSpine shipped `methods`, `identity.get`,
`provided_capabilities`, `consumed_capabilities`, `cost_estimates`, and
`operation_dependencies` in the v0.9.16 neural_api evolution.

### plasmidBin Metadata Reconciled

`plasmidBin/loamspine/metadata.toml`:
- Version: 0.9.13 → **0.9.16**
- Domain: `lineage` → **`permanence`**
- Capabilities: 6 stale entries → **22 live methods** matching `niche.rs`
- TCP opt-in documented, socket naming section added
- `manifest.lock` updated (version, domain, default_port 0, tcp_opt_in)

### Compliance Matrix Updated

`ECOSYSTEM_COMPLIANCE_MATRIX.md` loamSpine entries corrected:
- Transport: Added domain symlink PASS, TCP opt-in, UDS unconditional
- Discovery: Wire L2+L3 complete, domain symlink `ledger.sock`
- Transport line: Updated to reflect full transport suite

---

## Ecosystem Impact

- **Trio IPC**: Connection-close fix directly benefits any partner (wetSpring,
  ludoSpring, healthSpring) that uses HTTP-mode JSON-RPC over TCP. Partners
  no longer need to reconnect between calls.
- **BTSP**: Provider socket naming is now runtime-configurable. Deployments
  with non-BearDog handshake providers can set `BTSP_PROVIDER=custodian` (or
  similar) without code changes.
- **Compliance Matrix**: Tier 10 re-validation now possible — the LS-03
  connection stability issue that blocked composition checks is resolved.
- **NUCLEUS Deployments**: LD-09 resolved — `loamspine server` no longer crashes
  on port 8080 contention. UDS-only mode is the default; TCP is explicitly
  opted into when needed. All NUCLEUS deployments can run without TCP binding.

### Pass 4: Port Decoupling & Debris Cleanup

**Hardcoded port constants decoupled from production callers.**

`DiscoveryConfig::default()` was building fallback endpoints as
`http://0.0.0.0:{DEFAULT_TARPC_PORT}` and `http://0.0.0.0:{DEFAULT_JSONRPC_PORT}`
using raw constants. Now routes through `env_resolution` module (reads
`LOAMSPINE_*_PORT` > `*_PORT` > default). `discovery_client::advertise_self()`
port fallback similarly evolved. Constants remain only in doc examples and the
cfg-gated `debug_assertions` dev fallback.

**Full 11-dimension debt audit — all clean:**
- Zero unsafe code (`#![forbid(unsafe_code)]` all 3 crate roots)
- Zero `.unwrap()` / `.expect()` in production (denied by clippy)
- Zero `TODO` / `FIXME` / `HACK` markers in all source files
- Zero production mocks (all `#[cfg(test)]` gated)
- Zero hardcoded primal names (BTSP default env-configurable)
- Zero files over 1000 lines (max Rust: 956 lines)
- Zero archive directories, IDE debris, stale scripts, build artifacts
- 4 production `#[allow(]` — all justified with reason strings
- Dependencies: all advisories tracked in `deny.toml`, evolution paths in
  `specs/DEPENDENCY_EVOLUTION.md`

**Showcase consolidation:** Redundant `SHOWCASE_QUICK_REFERENCE_CARD.md` (126
lines) removed. `QUICK_REFERENCE.md` (306 lines) is canonical. Index and
entry point references updated.

**`.gitignore` hardened:** Added `.vscode/`, `.idea/`, `coverage/`, `htmlcov/`,
`*.lcov`, `*.rs.bk`.

### Pass 5: primalSpring Audit — `health.check` Empty Params Fix

**Issue (primalSpring Phase 39-41 audit):** `health.check` required
`{"include_details": true}` or it errored. Calling with `{}` or null params
broke deserialization. primalSpring auto-injected the param as a workaround,
but any other consumer calling `health.check` with empty params would fail.

**Fix (two-part):**
1. `HealthCheckRequest.include_details` → `#[serde(default)]`. Defaults to
   `false` when absent, so `{}` deserializes cleanly.
2. JSON-RPC `deser()` function now normalizes `null` params to `{}` per
   JSON-RPC 2.0 §4.2 ("omitted or null params means no arguments"). This
   handles the case where `params` is `null` or completely absent.

**Tests:** 2 new tests — `health_check_empty_params_defaults_include_details_false`
and `health_check_null_params_defaults_include_details_false`.

**Impact:** primalSpring can remove its `include_details` auto-injection
workaround. All consumers can call `health.check` with `{}`, `null`, or
omitted params.

### Pass 6: Deep Debt — Constants, Test Refactoring, Arc<str>, Modernization

**Discovery string literal → named constants:**
- `discovered_via` field values (`"environment"`, `"dns-srv"`, `"mdns"`) moved to
  `constants::discovery_method` module. DNS SRV metadata keys (`"priority"`,
  `"weight"`, `"target"`, `"port"`) moved to `constants::srv_metadata`.
- Eliminates scattered string literals across `infant_discovery/mod.rs` and
  `backends.rs`, enabling compile-time typo detection.
- 3 new tests: lowercase-ascii validation, distinctness, and SRV key validation.

**Witness default constants:**
- `DEFAULT_WITNESS_KIND` ("signature") and `DEFAULT_WITNESS_ENCODING` ("hex")
  extracted as public constants in `trio_types`. Serde default functions now
  reference the constants, ensuring the canonical values are documented.
- 2 new tests verify deserialized defaults match constants.

**Test file smart-refactoring (>800 lines):**
- `tests_protocol.rs` (956L) → `tests_protocol_transport.rs` (~430L) +
  `tests_protocol_wire.rs` (~500L). Split by cohesive concern: transport
  lifecycle vs wire-format conformance.
- `discovery/tests.rs` (899L) → `tests_registry.rs` (~330L) +
  `tests_attestation.rs` (~570L). Split by domain: capability registry vs
  attestation providers + TCP integration.
- 4 remaining test files (806-885L) are borderline and test-only — left as-is.

**Arc<str> for async retry closures:**
- `ResilientDiscoveryClient::discover_capability` and `advertise_self` evolved
  from `String` cloning (`capability.to_string()` + `.clone()` per retry) to
  `Arc<str>` — O(1) clone per retry iteration.

**`.into()` modernization:**
- Error constructors across `resilience.rs`, `sync/mod.rs`, `error.rs`, and
  `jsonrpc/mod.rs` updated from `"literal".to_string()` to `"literal".into()`.

**All gates green:** 1,395 tests, 0 failures, 0 clippy warnings, 0 doc warnings.

---

## Remaining Debt (LOW)

- `sweetGrass` coverage 87→90% (not LoamSpine scope)
- Witness chain validation under NUCLEUS mesh (composition-level, low urgency)
- `bincode v1 → v2` migration (tracked in `specs/DEPENDENCY_EVOLUTION.md`)
- `mdns` crate evolution (`async-std` advisories; feature-gated, optional)
- `tarpc 0.37` opentelemetry advisory (waiting on upstream)

---

## Files Changed

- `crates/loam-spine-api/src/jsonrpc/server.rs` — HTTP/1.1 keep-alive loop
- `crates/loam-spine-api/src/jsonrpc/tests_protocol_transport.rs` — UDS/TCP/HTTP transport tests (split from tests_protocol.rs)
- `crates/loam-spine-api/src/jsonrpc/tests_protocol_wire.rs` — Wire-format/dispatch tests (split from tests_protocol.rs)
- `crates/loam-spine-core/src/btsp/config.rs` — Provider-agnostic naming
- `crates/loam-spine-core/src/btsp/mod.rs` — Re-export updates
- `crates/loam-spine-core/src/btsp_tests.rs` — Updated for new APIs
- `crates/loam-spine-api/src/jsonrpc/uds.rs` — `provider_socket` field
- `bin/loamspine-service/main.rs` — TCP opt-in refactor (LD-09), provider log
- `crates/loam-spine-core/src/constants/env_resolution.rs` — `has_explicit_tcp_config()`
- `crates/loam-spine-core/src/constants/network.rs` — Re-export
- `crates/loam-spine-core/src/traits/mod.rs` — Test extraction
- `crates/loam-spine-core/src/traits/mod_tests.rs` — New extracted test file
- `crates/loam-spine-core/src/transport/http.rs` — Named timeout constants
- `crates/loam-spine-core/src/infant_discovery/mod.rs` — Named DNS SRV timeout
- `crates/loam-spine-core/src/infant_discovery/backends.rs` — Named mDNS timeout
- 5 earlier test files (streaming, health, service_mod, config, lib)
- 7 production files with Songbird doc cleanup
- 5 root markdown docs reconciled
- `STATUS.md` — Updated metrics and changelog
- `crates/loam-spine-core/src/primal_names.rs` — `CAPABILITY_DOMAIN` constant + 2 tests
- `crates/loam-spine-core/src/neural_api/socket.rs` — Capability-domain symlink functions
- `crates/loam-spine-core/src/neural_api/mod.rs` — Re-export new socket functions
- `crates/loam-spine-core/src/neural_api/tests.rs` — 3 capability-domain socket tests
- `bin/loamspine-service/main.rs` — Capability symlink creation + shutdown cleanup
- `CAPABILITY_WIRE_STANDARD.md` — loamSpine row L2 ✓ L3 ✓
- `ECOSYSTEM_COMPLIANCE_MATRIX.md` — loamSpine transport/discovery/transport-line entries
- `plasmidBin/loamspine/metadata.toml` — Version, domain, capabilities, sockets
- `plasmidBin/manifest.lock` — Version, domain, tcp_opt_in
- 5 root markdown docs (README, STATUS, CONTEXT, CONTRIBUTING, WHATS_NEXT) — Metrics to 1,395
- `crates/loam-spine-core/src/config.rs` — DiscoveryConfig::default() uses env_resolution
- `crates/loam-spine-core/src/discovery_client/mod.rs` — Port fallbacks use env_resolution, Arc<str> for retry closures
- `showcase/SHOWCASE_QUICK_REFERENCE_CARD.md` — Deleted (duplicate of QUICK_REFERENCE.md)
- `showcase/00_START_HERE.md` — References updated
- `showcase/00_SHOWCASE_INDEX.md` — References updated
- `.gitignore` — Hardened with IDE/coverage patterns
- `crates/loam-spine-api/src/types/mod.rs` — `#[serde(default)]` on `HealthCheckRequest.include_details`
- `crates/loam-spine-api/src/jsonrpc/mod.rs` — `deser()` null→{} normalization, `.into()` for wire error
- `crates/loam-spine-api/src/jsonrpc/tests_validation.rs` — 2 new health.check param tests
- `crates/loam-spine-core/src/constants.rs` — `discovery_method::*` and `srv_metadata::*` constant modules + 3 tests
- `crates/loam-spine-core/src/infant_discovery/mod.rs` — Uses discovery_method/srv_metadata constants
- `crates/loam-spine-core/src/infant_discovery/backends.rs` — Uses discovery_method::MDNS constant
- `crates/loam-spine-core/src/trio_types.rs` — `DEFAULT_WITNESS_KIND`/`DEFAULT_WITNESS_ENCODING` constants
- `crates/loam-spine-core/src/trio_types_tests.rs` — 2 new witness constant tests
- `crates/loam-spine-api/src/jsonrpc/tests_protocol.rs` — Deleted, replaced by two split files
- `crates/loam-spine-api/src/jsonrpc/tests_protocol_transport.rs` — New: UDS/TCP/HTTP/concurrent load tests
- `crates/loam-spine-api/src/jsonrpc/tests_protocol_wire.rs` — New: Wire-format/dispatch/notification/batch tests
- `crates/loam-spine-core/src/discovery/tests.rs` — Deleted, replaced by two split files
- `crates/loam-spine-core/src/discovery/tests_registry.rs` — New: Capability registry tests
- `crates/loam-spine-core/src/discovery/tests_attestation.rs` — New: Attestation provider + TCP integration tests
- `crates/loam-spine-core/src/resilience.rs` — `.into()` for error string literals
- `crates/loam-spine-core/src/sync/mod.rs` — `.into()` for error string literals
- `crates/loam-spine-api/src/error.rs` — `.into()` for error string literals

### Pass 7: Doc Reconciliation & Debris Cleanup

- **Root doc metrics aligned** across README, STATUS, CONTEXT, CONTRIBUTING, CHANGELOG
  - Source files: 176 → **178** (all docs)
  - Test badge: 1,383 → **1,395** (README)
  - JSON-RPC method count reconciled to **32** (STATUS, CONTRIBUTING matched to `niche.rs` METHODS)
  - Showcase file count: 55 → **54** (README)
  - CHANGELOG 0.9.16 metrics corrected from stale intermediate snapshot
- **Stale `phase1/` cross-repo links fixed** — 8 references across 5 files:
  - `specs/00_SPECIFICATIONS_INDEX.md` — BearDog, Songbird, NestGate links + Architecture link
  - `specs/LOAMSPINE_SPECIFICATION.md` — BearDog link
  - `specs/INTEGRATION_SPECIFICATION.md` — BearDog, Songbird links
  - `specs/PURE_RUST_RPC.md` — Songbird tarpc spec link (both inline and reference)
  - `showcase/00_SHOWCASE_INDEX.md` — 5 primal showcase links (also fixed casing: songbird→songBird, toadstool→toadStool, etc.)
- **Build artifacts cleaned**: `cargo clean` removed 9,847 files / 6.4 GiB
- **No stale scripts, tracked artifacts, TODO/FIXME markers, or secrets found**
- **Handoff header updated**: test count 1,390→1,395, source files 176→178
