<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt v0.13.0-dev — Deep Debt & Standards Evolution Handoff

**Date**: March 12, 2026
**Primal**: rhizoCrypt
**Version**: 0.13.0-dev
**Type**: Deep debt evolution + wateringHole standards compliance

---

## Summary

Full codebase audit against wateringHole standards (UniBin, ecoBin, semantic
naming, Universal IPC, sovereignty, zero-copy, license compliance, code quality).
Multi-wave remediation completed across two sessions. All quality gates green.
491 tests pass, 0 fail. Clippy pedantic+nursery with `-D warnings` clean.

---

## Changes

### wateringHole Standards Compliance

1. **AGPL-3.0-only license**: SPDX identifier updated from `AGPL-3.0` to
   `AGPL-3.0-only` in workspace Cargo.toml. SPDX license headers added to all
   71 `.rs` source files. LICENSE file verified present.

2. **UniBin architecture**: Binary renamed from `rhizocrypt-service` to
   `rhizocrypt`. `clap` integrated for subcommand dispatch (`server`, `status`,
   `version`). All integration tests updated. Compliant with
   `UNIBIN_ARCHITECTURE_STANDARD.md`.

3. **ecoBin compliance (partial)**: `reqwest` switched from default
   `native-tls` to `rustls-tls` feature (Pure Rust TLS, no OpenSSL). `sled`
   backend identified as non-compliant (uses `zstd-sys` C library) — it is
   feature-gated and documented; migration to `redb` (Pure Rust) is planned.

4. **Semantic method naming**: All JSON-RPC method names evolved from
   `"loamspine.healthCheck"` (primal-named) to `"permanent-storage.healthCheck"`
   (capability-named). Method names defined as `&'static str` constants in a
   `methods` module. Compliant with `SEMANTIC_METHOD_NAMING_STANDARD.md`.

5. **Capability-based discovery**: Removed hardcoded development fallback ports
   (`DEVELOPMENT_FALLBACK_PORT: 8091`, `localhost:8080`). Removed deprecated
   primal-specific discovery methods (`discover_beardog`, `discover_loamspine`,
   `discover_nestgate`). Replaced with capability-only methods
   (`discover_signing_provider`, `discover_permanent_storage_provider`,
   `discover_payload_storage_provider`). Primal code only has self-knowledge.

6. **Vendor env var elimination**: Removed deprecated `TOADSTOOL_ADDRESS`,
   `TOADSTOOL_TIMEOUT_MS`, `SWEETGRASS_PUSH_ADDRESS`, `SWEETGRASS_TIMEOUT_MS`
   fallbacks from `safe_env.rs`, `compute.rs`, and `provenance.rs`. Only
   capability-based env vars remain (`COMPUTE_ENDPOINT`, `PROVENANCE_ENDPOINT`).

### Code Quality Evolution

7. **`unused_async` elimination**: Converted `create_session`, `checkout_slice`,
   `resolve_slice`, `get_dehydration_status` from `async fn` to `fn`. These
   methods use lock-free DashMap operations and never `.await`. Removed
   workspace-level `unused_async = "allow"`. Updated 40+ call sites.

8. **`Vertex` error propagation**: Converted `to_canonical_bytes`, `compute_id`,
   `id` from direct return values to `Result` types. Eliminates `expect()` in
   production code. All 30+ callers updated (production uses `?`, test uses
   `.unwrap()`).

9. **`cast_possible_truncation` fixes**: Replaced unsafe `as u64` casts with
   `u64::try_from().unwrap_or(u64::MAX)` and `saturating_add` in
   `Timestamp::now()` and `SliceBuilder::expires_in()`.

10. **Atomic ordering**: Changed `Ordering::SeqCst` to `Ordering::Relaxed` for
    monotonic request ID counters (sufficient for non-synchronized counters).

11. **Clippy lint cleanup**: Removed bulk `#[allow(clippy::*)]` from crate roots.
    Fixed all exposed violations: `uninlined_format_args`, `redundant_clone`,
    `match_same_arms`, `explicit_auto_deref`, `redundant_closure_for_method_calls`.
    Added `[lints] workspace = true` to `rhizocrypt-service` for consistent
    enforcement.

12. **Dehydration implementation**: Completed stubbed logic in
    `dehydration_impl.rs` — calculates actual payload sizes, extracts payload
    values into `serde_json::Value`, counts events per agent with role assignment.

### Infrastructure

13. **Fuzz testing**: Created 3 `cargo-fuzz` targets using `libfuzzer-sys` +
    `arbitrary`: `fuzz_vertex_cbor` (CBOR deserialization), `fuzz_merkle_compute`
    (tree construction), `fuzz_session_builder` (config edge cases).

14. **Test stability**: Fixed `test_service_handles_invalid_port` hang by
    replacing blocking `Command::output()` with `spawn()` + `tokio::time::timeout`.

15. **Legacy cleanup**: Deleted `legacy_aliases.rs` and all deprecated mock type
    aliases (`MockBearDogClient`, etc.). Removed deprecated vendor-specific methods
    from `ClientProvider` trait (125 lines). Reduced `discovery.rs` from 1001 to
    854 lines.

16. **Root documentation cleanup**: Moved 22 session artifacts, verification
    scripts, and status reports to `phase2/archive/rhizoCrypt-mar-12-2026/`.
    README.md rewritten to reflect current codebase state.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check --all` | Pass |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Pass |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Pass |
| `cargo test --workspace` | 491 passed, 0 failed |
| `#![forbid(unsafe_code)]` | Enforced workspace-wide |
| File size limit (1000 lines) | All files compliant (max: 981) |
| SPDX headers | All 71 source files |

---

## Known Gaps

1. **sled C dependency**: `zstd-sys` transitively compiled via sled 0.34.
   Feature-gated behind `sled` feature flag. Migration to Pure Rust `redb`
   planned once storage API stabilizes.

2. **Test coverage**: Target is 90% (`llvm-cov`). Current coverage has not been
   re-measured after this wave of changes. Running `cargo llvm-cov` is recommended.

3. **tarpc binary transport**: The tarpc path for LoamSpine and Songbird is
   defined but not fully exercised in integration tests.

4. **Inter-primal showcase**: `showcase/01-inter-primal-live/` demos reference
   primal names in scripts (expected — they orchestrate external processes).
   Scripts are not production code.

---

## For Other Primals

### LoamSpine Team
- rhizoCrypt now uses `permanent-storage.*` method names (not `loamspine.*`).
  LoamSpine's JSON-RPC server should accept either during migration, then
  deprecate primal-named methods.

### Songbird Team
- Discovery methods are now capability-only. `populate_registry` iterates
  capability mappings instead of hardcoding primal names.

### All Primals
- The deprecated vendor env var pattern (`TOADSTOOL_ADDRESS`,
  `SWEETGRASS_PUSH_ADDRESS`, `SONGBIRD_ADDRESS`) is fully removed from
  rhizoCrypt. Other primals consuming rhizoCrypt should use capability-based
  env vars.

---

## File Inventory

```
rhizoCrypt/
├── Cargo.toml, Cargo.lock     # Workspace manifest
├── README.md, CHANGELOG.md    # Documentation
├── LICENSE                     # AGPL-3.0-only
├── Dockerfile                  # Multi-stage build
├── .github/workflows/ci.yml   # CI pipeline
├── k8s/deployment.yaml         # Kubernetes manifest
├── .llvm-cov.toml              # Coverage config (90% target)
├── rustfmt.toml                # Formatting config
├── docs/                       # ENV_VARS, DEPLOYMENT_CHECKLIST, VERIFICATION_CHECKLIST
├── specs/                      # Formal specifications (10 documents)
├── showcase/                   # 35+ progressive demos
└── crates/
    ├── rhizo-crypt-core/       # Core library (55 source files)
    │   └── fuzz/               # 3 fuzz targets
    ├── rhizo-crypt-rpc/        # RPC layer (9 source files)
    └── rhizocrypt-service/     # UniBin service (3 source files)
```
