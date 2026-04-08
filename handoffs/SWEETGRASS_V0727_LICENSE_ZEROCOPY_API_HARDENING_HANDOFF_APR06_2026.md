<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# SweetGrass v0.7.27 — License Evolution, Zero-Copy, API Hardening, Dep Hygiene

**Date**: April 6, 2026
**From**: SweetGrass
**To**: All Springs, All Primals, biomeOS
**Status**: Complete — 1,190+ tests, 90.90% region coverage, GAP-MATRIX-05 RESOLVED, all checks green

**Supersedes**: `SWEETGRASS_V0727_DEEP_DEBT_EVOLUTION_HANDOFF_MAR31_2026.md` (archived)

---

## Summary

Six-phase deep evolution session addressing primalSpring downstream audit
findings and remaining deep debt. License evolved to AGPL-3.0-or-later per
wateringHole/LICENSING_AND_COPYLEFT.md scyBorg standard. Zero-copy
improvements on hot paths. API hardened with `#[non_exhaustive]` on all
public enums. `deny.toml` tightened against protobuf codegen crates.
17 unused dependencies removed. Attribution API now derivation-aware
(Phase 4 radiating attribution prep). musl-static builds verified.
Braid proof block evolved from LD-Proof `BraidSignature` to
`WireWitnessRef`-aligned `Witness` type, unifying trio output format.

---

## Phase 1 — primalSpring Audit Resolution

| Finding | Resolution |
|---------|-----------|
| `cargo deny` fails (time 0.3.44) | Updated to 0.3.47 |
| Clippy unused imports in `tcp_jsonrpc.rs` | Test rewritten, imports removed |
| `.cargo/config.toml` hardcoded `target-dir` | Removed; env-var override pattern |
| `#[allow(cast_precision_loss)]` in `object_memory.rs` | Removed (lint not triggered) |

## Phase 2 — License Evolution

All artifacts evolved from `AGPL-3.0-only` to `AGPL-3.0-or-later` per
wateringHole LICENSING_AND_COPYLEFT.md ("-or-later delegates future version
trust to the FSF"):

| Artifact | Count |
|----------|-------|
| `.rs` SPDX headers | 154 |
| `Cargo.toml` files (workspace + 10 crates + fuzz) | 12 |
| `LICENSE` preamble + section header | 1 |
| `deny.toml` allow-list | 1 |
| `scyborg.rs` `LicenseId` enum variant | renamed `Agpl3Only` → `Agpl3OrLater` |
| Root docs, specs, config, `.cursor/rules` | all updated |

`unsafe_code` promoted from `deny` to `forbid` at workspace level.

## Phase 3 — Zero-Copy & API Hardening

### Zero-Copy Improvements

| Change | Impact |
|--------|--------|
| `traversal.rs` cycle detection: `HashSet<String>` → `HashSet<ContentHash>` | O(1) Arc clone vs heap alloc per node |
| `QueryError::NotFound`: `String` → `ContentHash` | O(1) clone at 3 call sites |
| `ActivityType` derives `Hash`; analyzer keyed by type not string | Eliminates per-vertex `.to_string()` in compression |

### Static Error Variants

| New Variant | Replaces |
|-------------|----------|
| `IntegrationError::MissingTarpcAddress` | 3 × `"Primal has no tarpc address".to_string()` |
| `CompressionError::NoCommittedVertices` | 1 × `"No committed vertices".to_string()` |

### API Hardening

- `#[non_exhaustive]` added to **35+ public enums** across all 10 crates
- Cross-crate match statements updated with forward-compatible wildcard arms
- `deny.toml`: added `tonic-build`, `prost-build`, `quick-protobuf`, `pbjson` to ban list

## Phase 4 — Dependency Hygiene & Attribution Evolution

### Dependency Cleanup

17 unused dependencies removed across 10 crates:

| Crate | Removed |
|-------|---------|
| sweet-grass-core | `chrono`, `tokio` (prod), `serial_test` |
| sweet-grass-factory | `chrono`, `tracing`, `uuid` |
| sweet-grass-compression | `chrono`, `tokio`, `tracing`, `uuid` |
| sweet-grass-query | `tracing`, `uuid` |
| sweet-grass-store | `chrono`, `tracing`, `uuid` |
| sweet-grass-store-postgres | `serde`, `chrono`, `uuid` |
| sweet-grass-store-sled | `serde` |
| sweet-grass-store-redb | `serde` |
| sweet-grass-integration | `futures`, `sweet-grass-query` (dev) |
| sweet-grass-service | `tower` |

### Attribution API Derivation-Aware

- `attribution_chain()` now delegates to `full_attribution_chain()` — all
  JSON-RPC/REST/tarpc callers get decay-weighted derivation traversal
  instead of single-braid-only attribution
- Parent creators receive inherited credit through `was_derived_from` chain
- Prep for Phase 4 radiating attribution (blocked on ionic bonding protocol,
  primalSpring Track 4)

### Hardcoding Elimination

- `create_app_state_from_env()` gated to `#[cfg(test)]` — hardcoded
  `did:primal:test` no longer in production builds; reads
  `SWEETGRASS_AGENT_DID` env var with test fallback

---

## Current State

```
cargo clippy --all-features --all-targets -- -D warnings   ✓ 0 warnings
cargo fmt --all -- --check                                  ✓ clean
cargo deny check                                            ✓ advisories ok, bans ok, licenses ok, sources ok
cargo doc --all-features --no-deps                          ✓ clean
cargo test --all-features --workspace                       ✓ 1,190 passed, 0 failed
```

| Metric | Value |
|--------|-------|
| Version | v0.7.27 |
| Tests | 1,190 |
| Coverage | 90.90% region (llvm-cov) |
| .rs files | 151 (42,161 LOC) |
| Max file | 766 lines (limit: 1000) |
| Unsafe blocks | 0 (`#![forbid(unsafe_code)]` workspace-level) |
| License | AGPL-3.0-or-later (scyBorg standard) |
| SPDX headers | 151/151 |

---

## Phase 5 — musl-static Deployment (ecoBin / plasmidBin)

Trio glibc debt resolved for sweetGrass. Binary now builds musl-static.

| Artifact | Value |
|----------|-------|
| Target | `x86_64-unknown-linux-musl` |
| Profile | `release-static` (LTO fat, strip, codegen-units 1, opt-level z) |
| Binary size | 4.5 MB |
| `file` | `static-pie linked, stripped` |
| `ldd` | `statically linked` |
| Smoke test | `sweetgrass capabilities` — 27 methods |

- `.cargo/config.toml`: musl target profiles, aarch64 cross-linker, cargo aliases
- `deploy.sh`: defaults to musl-static; `SWEETGRASS_TARGET` env var override
- CI: `musl-static` job (build, verify linkage, smoke test)
- `DEVELOPMENT.md`: musl build instructions

---

## Phase 6 — `BraidSignature` → `Witness` (WireWitnessRef alignment)

Braid top-level proof field evolved from W3C LD-Proof `BraidSignature`
(`sig_type` / `proof_value` / `proof_purpose`) to the ecosystem
`WireWitnessRef`-aligned `Witness` type (`kind` / `evidence` / `encoding`
/ `algorithm` / `tier`).

| Before (LD-Proof) | After (WireWitnessRef) |
|--------------------|------------------------|
| `Braid.signature: BraidSignature` | `Braid.witness: Witness` |
| `sig_type: "Ed25519Signature2020"` | `kind: "signature"`, `algorithm: Some("ed25519")` |
| `proof_value` (base64) | `evidence` (base64), `encoding: "base64"` |
| `proof_purpose: "assertionMethod"` | (implicit — not in WireWitnessRef) |
| `verification_method: "did:key:...#keys-1"` | `agent: Did` |
| `created` (ns timestamp) | `witnessed_at` (ns timestamp) |
| N/A | `tier: Some("local")` for crypto, `Some("open")` for unsigned |

**Files changed**: 16 Rust source files + 3 spec files

- `Witness::unsigned()` and `Witness::from_ed25519()` constructors added
- `BraidSignature` deprecated (`#[deprecated(since = "0.7.28")]`), retained for one release cycle
- `#[serde(alias = "signature")]` on `Braid.witness` for backward compat
- Postgres JSONB: fallback deserializer converts old rows losslessly
- `SigningClient::sign()` returns `Witness` instead of `BraidSignature`
- Mock signing client updated to produce `Witness` instances

---

## Phase 7 — Constant Unification, Proptest Expansion, Test Coverage (April 7)

Deep debt sweep: centralized shared constants, expanded property-based testing,
strengthened error path coverage, cleaned zero-allocation witness vocabulary.

| Category | Changes |
|----------|---------|
| **Constant unification** | `DEFAULT_MAX_PROVENANCE_DEPTH` single source in `sweet-grass-core::config`; replaced 3 independent `10` constants in query engine, attribution calculator, traversal builder |
| **Graph metadata** | `ProvenanceGraph.has_cycles` field — cycle detection recorded at traversal time instead of silently skipping |
| **Witness vocabulary** | 8 named `&'static str` constants (`WITNESS_KIND_SIGNATURE`, `WITNESS_ENCODING_BASE64`, `WITNESS_ALGORITHM_ED25519`, `WITNESS_TIER_LOCAL`, etc.) replace magic strings in constructors and Postgres legacy deserializer |
| **Contribution defaults** | `DEFAULT_CONTRIBUTION_MIME` constant for serde default mime type |
| **Proptest expansion** | Added to `sweet-grass-query` (graph entity count, serialization roundtrip) and `sweet-grass-compression` (vertex count, roots, tips, max depth) — 6 new property tests |
| **Error path tests** | `MissingTarpcAddress` coverage for signer, anchor, listener `from_primal()` |
| **Dep hygiene** | `serial_test` removed from service (unused) |

**Metrics**: 1,190 tests (was 1,181), 151 .rs files (42,161 LOC), proptest in 5 crates

---

## Phase 8 — GAP-MATRIX-05 Live Validation (April 7, 2026)

sweetGrass live-tested through UDS JSON-RPC per primalSpring v0.9.3 gap matrix.

### Validation Results

| Probe | Socket | Result |
|-------|--------|--------|
| `identity.get` | `sweetgrass.sock` | `{"name":"sweetgrass","version":"0.7.27"}` |
| `health.liveness` | `sweetgrass.sock` | `{"alive":true}` |
| `health.readiness` | `sweetgrass.sock` | `{"ready":true}` |
| `health.check` | `sweetgrass.sock` | `{"status":"healthy","store_status":"ok","braid_count":0,"version":"0.7.27"}` |
| `capabilities.list` | `sweetgrass.sock` | 28 methods, 12 domains |
| `capability.list` | `sweetgrass.sock` | 28 methods (alias confirmed) |
| `identity.get` | `provenance.sock` | Same (capability symlink validated) |

### Changes

- **Added `identity.get`** — new JSON-RPC method returning primal name + version for biomeOS Neural API observability. biomeOS probes this alongside `capabilities.list` for routing table construction.
- **28 methods** in dispatch table (was 27): added `identity.get` to METHODS table, niche CAPABILITIES, operation_dependencies, cost_estimates, and semantic_mappings.
- **Wire format**: `capabilities.list` result contains `methods` and `capabilities` as flat string arrays (Format A data in structured envelope), plus `domains` (grouped map). biomeOS's 5-format parser extracts from `result.methods` / `result.capabilities`.
- **No CLI flags needed**: UDS listener starts automatically with `sweetgrass server`. Socket path controlled by `SWEETGRASS_SOCKET` env var (or falls back to `BIOMEOS_SOCKET_DIR`, `XDG_RUNTIME_DIR`, `TMPDIR`).
- **Capability symlink**: `provenance.sock -> sweetgrass.sock` created automatically per `CAPABILITY_BASED_DISCOVERY_STANDARD v1.1`.

### GAP-MATRIX-05 Status: RESOLVED for sweetGrass

---

## Phase 9 — Wire Standard L3 Compliance (April 8, 2026)

sweetGrass now passes the full `CAPABILITY_WIRE_STANDARD.md` v1.0 L3 (Composable) audit checklist.

### Wire Standard L3 Checklist

| Requirement | Status |
|-------------|--------|
| L1: `capabilities.list` parseable | ✓ |
| L1: `health.liveness` responds | ✓ `{"alive":true}` |
| L2: `{primal, version, methods}` envelope | ✓ |
| L2: `identity.get` with `{primal, version, domain, license}` | ✓ |
| L2: All 28 `methods` callable (no method-not-found) | ✓ |
| L3: `provided_capabilities` grouping | ✓ 12 groups with type, methods, version, description |
| L3: `consumed_capabilities` declared | ✓ 8 cross-primal dependencies |
| L3: `cost_estimates` per-method `{cpu, latency_ms}` | ✓ all 28 methods |
| L3: `operation_dependencies` flat map | ✓ 13 prerequisite chains |

### Changes

- **`provided_capabilities`**: 12 domain groups (braid, anchoring, provenance, attribution, compression, contribution, pipeline, health, identity, capabilities, capability, tools) with `type`, `methods[]`, `version`, and `description`. biomeOS registers both group type and qualified `type.method` names.
- **`cost_estimates`**: Per-method `{cpu: "low"|"medium"|"high", latency_ms: N}` for all 28 methods. High-cost methods: `anchoring.anchor` (50ms), `attribution.chain` (50ms), `attribution.calculate_rewards` (60ms), `compression.compress_session` (40ms), `provenance.export_graph_provo` (30ms).
- **`operation_dependencies`**: Flat `{method: [prerequisites]}` map for 13 methods with dependencies. Enables AI-assisted execution planning (Squirrel).
- **`identity.get` upgraded**: Now returns `{primal, version, domain, license}` per Wire Standard §4. `domain: "attribution"`, `license: "AGPL-3.0-or-later"`.
- **Backward-compatible**: Legacy `capabilities`, `domains`, and `operations` fields retained in the response for pre-Wire Standard consumers.

### sweetGrass Wire Standard Status: Level 3 (Composable) — FULL COMPLIANCE

---

## Phase 10 — Comprehensive Coverage Expansion (April 8, 2026)

### Metrics
- **1,213 tests passing** (up from 1,190)
- 0 clippy warnings, 0 unsafe, `cargo deny` clean
- 151 .rs files, 42,543 LOC

### Changes
- **`identity.get` dispatch test**: Added to completeness list + Wire Standard L2 response validation (primal, version, domain, license)
- **Wire Standard L3 tests**: `provided_capabilities` grouping, per-method `cost_estimates`, `operation_dependencies` flat map — all asserted structurally
- **`RegistryError` variant coverage**: Display for `NotFound`, `RegistrationFailed`, `Internal` + serialization roundtrip
- **`IntegrationError` full sweep**: All 17+ variant Display tests + `From<Store>`, `From<Core>`, `From<Compression>` conversions
- **Compression/Factory/Query error gaps filled**: `NoCommittedVertices`, `Factory`, `Core`, `Store` variants all tested
- **`ServiceError` IntoResponse expansion**: `Query`, `Factory`, `Compression`, `Core` HTTP status mapping tests
- **Router test expansion**: 2 → 4 tests (construction + parity)

### Audit Summary (Clean)
- Zero unsafe code (forbidden workspace-level + all 11 crate roots)
- Zero production unwraps/expects (denied)
- Zero mocks in production (all `cfg(test)` / `feature = "test"` gated)
- Zero hardcoded primal names in code logic (comments/docs only)
- Zero banned dependencies (`cargo deny` clean)
- All files under 1000 lines (max: 766)
- All `#[allow(clippy::*)]` migrated to `#[expect(...)]` (except deprecated items)
- Deprecated items properly annotated: `BraidSignature` (0.7.28), `SledStore` (0.7.26)

---

## Remaining Debt (None Blocking)

- **Radiating attribution across ionic bonds** — Phase 4 / LOW; derivation chain attribution is live, but cross-NUCLEUS traversal requires ionic bonding protocol (primalSpring Track 4)
- **aarch64 musl**: Target profile configured but not CI-verified (needs cross-linker in CI runner)
- **Coverage gap**: Postgres store tests require Docker runtime; excluded from llvm-cov
- **`sled` backend**: Optional, unmaintained upstream; `skip-tree` in `deny.toml`; redb is primary
- **`testcontainers` dev chain**: Pulls `bollard` → `rustls` → `ring` (C/ASM); dev-only, wrappered in `deny.toml`
- **Remove `BraidSignature` (v0.7.29)**: Currently deprecated; remove after one release cycle once no Postgres rows use the old format

---

## Cross-Ecosystem Signals

- **License alignment**: sweetGrass now matches wateringHole AGPL-3.0-or-later standard
- **API stability**: `#[non_exhaustive]` on all public enums means downstream crates need wildcard match arms
- **`LicenseId::Agpl3OrLater`**: Any code referencing `LicenseId::Agpl3Only` needs updating
- **`QueryError::NotFound(ContentHash)`**: Downstream match on `NotFound(String)` needs updating to `NotFound(ContentHash)`
- **Attribution now walks derivations**: `attribution.chain` JSON-RPC results now include inherited contributors from parent braids; consumers expecting single-braid-only results should account for additional contributors
- **17 deps removed**: Crates depending on sweetGrass transitives may see resolved version changes in lockfile
- **`Attestation` → `Witness`**: Dehydration type renamed; `WireAttestationRef` is now `WireWitnessRef` with `witnessed_at` field. Trio partners must update wire type references.
- **`Braid.signature` → `Braid.witness`**: Top-level proof block now uses `WireWitnessRef` vocabulary. Wire consumers expecting `"signature": {"type": ..., "proofValue": ...}` should update to `"witness": {"kind": ..., "evidence": ...}`. `#[serde(alias = "signature")]` provides read-path backward compatibility.
- **musl-static ready**: sweetGrass binary is now `statically linked` (4.5 MB); trio glibc deployment debt resolved for sweetGrass. rhizoCrypt musl-static also shipped (April 2026). loamSpine musl-static also shipped (April 2026).
