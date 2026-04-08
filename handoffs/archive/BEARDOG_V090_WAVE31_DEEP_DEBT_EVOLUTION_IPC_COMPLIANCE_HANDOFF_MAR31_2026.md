# BearDog v0.9.0 — Wave 31 Deep Debt Evolution + IPC Compliance Handoff

**Date:** March 31, 2026
**Author:** AI pair (Claude) + eastgate
**Scope:** Waves 30–31 combined — wateringHole compliance, deep debt resolution, smart refactoring, rand 0.9 migration, doc reconciliation

---

## Summary

Two-wave sprint resolving all remaining IPC compliance gaps identified in
`IPC_COMPLIANCE_MATRIX.md` v1.3, completing the rand 0.8 → 0.9 migration,
decomposing 8 large files into domain-driven modules, evolving production
mocks to capability-based errors, centralising hardcoded values, and
reconciling all root documentation to a single source of truth.

---

## Gate Status (March 31, 2026)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace --all-features -D warnings` | Pass (0 warnings) |
| `cargo build --workspace` | Pass |
| `cargo test --workspace` | **14,610 passed, 0 failed** |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo doc --workspace --no-deps` | Pass |

---

## IPC Compliance Matrix — BearDog Now Conformant

All beardog-specific items in `IPC_COMPLIANCE_MATRIX.md` resolved:

| Dimension | Before | After | How |
|-----------|--------|-------|-----|
| `--port` | **X** | **C** | `--port PORT` binds `0.0.0.0:PORT` (alias for `--listen`) |
| Standalone startup | **X** | **C** | `PrimalIdentity::from_env()` defaults to `standalone`/`default` |
| `health.check` | missing | **C** | Full canonical health suite: `liveness`, `readiness`, `check` |
| Domain symlink | **P** (missing) | **C** | `crypto.sock` → `beardog.sock`, cleaned on shutdown |
| Abstract logging | **P** (buggy) | **C** | Logs `"bound to abstract namespace (kernel-only, not on disk)"` |
| Audit dir | **P** | **C** | `--audit-dir` / `BEARDOG_AUDIT_DIR`, falls back to `$TMPDIR/beardog` |
| Beacon RPC | missing | **C** | `birdsong.generate_encrypted_beacon` wired in `SecurityHandler` |
| **Summary scorecard** | **Close** | **Conformant** | |

6 priority items in the matrix marked **RESOLVED**.

---

## Smart Domain-Driven Refactoring (8 files decomposed)

| Original file | Before LOC | After | Domain split |
|---------------|-----------|-------|-------------|
| `pkcs11_discoverer.rs` | 899 | 6 files, max 414 | types, discovery, library, tokens, capabilities, classification |
| `crypto_service/implementation.rs` | 896 | 7 files, max 312 | lifecycle, keys, encrypt/decrypt, sign/verify, trait impl |
| `canonical/crypto.rs` | 891 | 7 files, max 274 | algorithms, keys, signature, key_management, config |
| `birdsong/genesis_types.rs` | 890 | 6 files, max 418 | core, witness, lineage, physical_proof |
| `ecosystem_discovery_adapter.rs` | 885 | 7 files, max 385 | adapter, listener, endpoint, discovery, rpc |
| `software_hsm/core.rs` | 884 | 6 files, max 323 | key_storage, hsm_provider, lifecycle |
| `key_revoke.rs` | 883 | 555 + tests | tests extracted |
| `fido2/ctap2.rs` | 882 | 5 files, max 274 | types, transport, parse |

**Result:** Largest production file is now 875 LOC. Zero files over 900 LOC.

---

## rand 0.9 Migration (Complete)

- `thread_rng()` → `rng()` across entire workspace
- `gen_range()` → `random_range()`
- `gen()` → `random()`
- `distributions::Alphanumeric` → `distr::Alphanumeric`
- Fixed `OsRng`/`CryptoRngCore` compatibility in test code (password-hash uses rand_core 0.6)

---

## Production Mock Evolution

- 3× `phase2_not_implemented` → `BearDogError::requires_capability("android-keystore", ...)`
- 2× `phase2_not_implemented` → `BearDogError::unsupported_platform("non-android", ...)`
- 1× `not_implemented` → `BearDogError::requires_capability("primal-discovery", ...)`
- **Zero `phase2_not_implemented` calls remain in production code.**

---

## Hardcoding → Constants/Configuration

| What | Before | After |
|------|--------|-------|
| Consul port | `8500` literal | `DEFAULT_CONSUL_HTTP_PORT` |
| Jaeger port | `14268` literal | `DEFAULT_JAEGER_COLLECTOR_PORT` |
| UID fallback | `1000` | Reads `$UID`/`$EUID` env vars, falls back to 1000 |
| Capability `"crypto"` | String literal (3 files) | `BEARDOG_CAPABILITY_DOMAIN` constant |

---

## Workspace Dependency Consolidation

- 5 crates migrated from inline version pins to `{ workspace = true }`
- 10 deps centralised in root `[workspace.dependencies]`
- `scrypt` aligned to stable 0.11 (was 0.12-rc, causing duplicate crypto crate tree)
- `thiserror` aligned to 2.0 workspace-wide

---

## Documentation Reconciliation

All root docs updated to single source of truth:

| Metric | Value |
|--------|-------|
| Workspace crates | 29 |
| Tests | 14,610+ |
| Coverage | 90.16% line (llvm-cov) |
| Crypto methods | 93 |
| .rs files | 1,892 |
| Largest production file | 875 LOC |
| Files over 900 LOC | 0 |

Stale references cleaned:
- `WHATS_NEXT.md` broken links → wateringHole handoff pointers
- `./scripts/` phantom paths → actual `cargo` commands
- `specs/README.md` index → aligned with per-file status headers
- Excluded crate READMEs → noted overstep ownership

---

## Codebase Health Summary

| Metric | Value |
|--------|-------|
| Production `unwrap()` | 0 (all test-only) |
| Production `Box<dyn>` dynamic dispatch | 0 (all test-only) |
| Production `phase2_not_implemented` | 0 |
| Production hardcoded primal names | 0 |
| `TODO` / `FIXME` / `HACK` in .rs | 0 |
| Duplicate dep crate names | 16 (all external/transitive) |

---

## Remaining Future Evolution

| Item | Status | Notes |
|------|--------|-------|
| Files 850–875 LOC | 4 files | Under limit; next-wave candidates |
| `serde_yaml` → `yaml-serde` | Tracked | 3 call sites, ecoBin compliant |
| BM-04 capability visibility | Ecosystem | Requires biomeOS rescan/lazy discovery |
| Composition guidance doc | Future | Per PRIMALSPRING_COMPOSITION_GUIDANCE |
| Property-based test expansion | Future | proptest boundaries for crypto |
| Duplicate deps (16 external) | Waiting | Upstream crate updates needed |
| Coverage → 92%+ | Ongoing | beardog-production, beardog-cli are drag areas |

---

## Files Changed (Summary)

**beardog repo:**
- 50+ `.rs` files (refactoring, rand migration, mock evolution, hardcode fixes)
- 8 `.md` files (README, ARCHITECTURE, CONTEXT, STATUS, ROADMAP, CHANGELOG, SECURITY, docs/)
- 6+ `Cargo.toml` files (dependency consolidation)

**wateringHole:**
- `IPC_COMPLIANCE_MATRIX.md` — beardog rows updated, priority items resolved
