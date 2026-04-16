# rhizoCrypt v0.14.0-dev — Session 43 Handoff

## Comprehensive Audit + Deep Debt Evolution + Crypto Model

**Date**: 2026-04-15
**Branch**: main
**Tests**: 1,506 passing (0 failures)
**Coverage**: 93.88% lines (CI gate: 90%)

---

### What Changed

#### 1. Canonical Crypto Model (`specs/CRYPTO_MODEL.md`)

rhizoCrypt delegates all asymmetric cryptography to BearDog via IPC.
Internal Blake3 content-addressing for data integrity remains in-process.
This resolves primalSpring audit item #3 (post-Phase 43).

**Key decisions:**
- rhizoCrypt never stores or manages signing keys
- All Ed25519 signing, verification, and DID operations flow through a
  capability-discovered `crypto.*` provider (canonically BearDog)
- Wire format alignment with BearDog's actual JSON-RPC methods documented
  as a known evolution gap

#### 2. Shared `DiscoveryRegistry`

`RhizoCrypt` struct now holds a single `Arc<DiscoveryRegistry>` initialized
at construction, shared across:
- Dehydration attestation collection (`collect_attestations`)
- Permanent storage commit (`commit_to_permanent_storage`)
- `ProvenanceNotifier` (via `with_discovery()`)

Previously, each call site created an orphan empty `DiscoveryRegistry`,
which could never discover any endpoints. This is now fixed.

#### 3. `niche.rs` `METHOD_CATALOG` — Single Source of Truth

Replaced 4× redundant capability metadata:
- `CAPABILITIES` (flat list)
- `SEMANTIC_MAPPINGS` (HashMap)
- `COST_ESTIMATES` (HashMap)
- `CAPABILITY_DOMAINS` (structured tree with `CapabilityDomain`/`CapabilityMethod`)

All replaced by a single `const METHOD_CATALOG: &[MethodSpec]` array.
`CAPABILITIES` and `SEMANTIC_MAPPINGS` are now derived via `LazyLock`.
File reduced from 654 → 404 lines.

#### 4. Smart Test File Refactoring (>800 line limit)

| File | Before | After | Strategy |
|------|--------|-------|----------|
| `service_integration.rs` | 960 | 231 + 173 + 310 + 268 | Directory module (doctor, config, UDS) |
| `store_redb_tests_advanced.rs` | 861 | 594 + 272 | Coverage tests extracted |
| `loamspine_http_tests.rs` | 858 | 303 + 512 | Wiremock tests extracted |
| `rhizocrypt_tests.rs` | 805 | 463 + 355 | Extended coverage extracted |
| `niche.rs` | 654 | 404 | Structural deduplication (not split) |

#### 5. Additional Debt Cleanup

- `prometheus.rs`: `infallible_write` helper → idiomatic `let _ = writeln!()` pattern
- `service/lib.rs`: shutdown `let _ =` → `if .is_err() { debug!(...) }` logging
- `capability_registry.toml`: domain mismatch fixed (`capability` → `capabilities`)
- showcase `Cargo.toml`: `tokio = "full"` → explicit feature set
- test harnesses: module-level `#![allow(dead_code)]` → targeted per-struct

---

### Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,506 passing |
| Coverage | 93.88% lines |
| `.rs` files | 170 |
| Lines | ~48,350 |
| Max file | 724 lines (limit 1,000) |
| Clippy | 0 warnings (pedantic + nursery) |
| Unsafe | 0 blocks (`unsafe_code = "deny"`) |
| Production unwrap/expect | 0 |
| `cargo deny` | Clean (advisories, bans, licenses, sources) |

---

### Verification

```
cargo fmt --check        ✅
cargo clippy -D warnings ✅ (0 warnings)
cargo test               ✅ 1,506 passed
cargo deny check         ✅
cargo llvm-cov           ✅ 93.88% (gate: 90%)
```

---

### For Trio Partners (loamSpine, sweetGrass)

- **`CRYPTO_MODEL.md`** is now the canonical reference for how rhizoCrypt
  handles cryptographic operations. All signing flows through BearDog IPC.
- **`METHOD_CATALOG`** is the single source of truth for rhizoCrypt's
  28 capabilities. Integrators should reference this for method names,
  domains, and cost estimates.
- **`DiscoveryRegistry`** is now properly shared — endpoint registration
  at service startup propagates to all internal consumers.

### S43 Addendum: `SigningClient` Wire Alignment (April 16)

**RESOLVED** — `SigningClient` adapter now uses BearDog-aligned wire DTOs:

| Method | Wire name | Fields |
|--------|-----------|--------|
| `sign` | `crypto.sign_ed25519` | `message` (base64), `key_id` (DID) |
| `verify` | `crypto.verify_ed25519` | `message`, `signature` (base64), `public_key` (DID) |
| `request_attestation` | `crypto.sign_contract` | `signer`, `terms` (JSON), response → `Attestation` |
| `verify_did` | (stub — no BearDog equivalent) | Unchanged |

`base64` promoted to non-optional dep (pure Rust, needed for wire encoding).
All binary data on the wire is now standard base64, matching BD-01.
1,507 tests passing, clippy clean.

### Remaining (Not Blocking)

- **DID → public key resolution** for `crypto.verify_ed25519` (`public_key`
  field receives DID string; needs BearDog DID resolution or explicit key)
- `specs/RHIZOCRYPT_SPECIFICATION.md` Phase 7 items: 90%+ CI-gated
  coverage and `Arc<str>` hot-path evolution — intentional roadmap
