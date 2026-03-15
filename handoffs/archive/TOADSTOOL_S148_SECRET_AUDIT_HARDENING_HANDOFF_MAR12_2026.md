# ToadStool S148 — Secret Audit & Credential Hardening

**Date**: March 12, 2026
**Session**: S148
**Tests**: 20,015+ passed (0 failures)
**Clippy**: Pedantic clean (0 warnings)

---

## Trigger

GitHub secret scanning auto-revoked a HuggingFace API token (`hf_ULwg...`)
found in git history. Full codebase + git history audit conducted.

## Findings

### Confirmed Leak (Remediated)

| Secret | Location | Status |
|--------|----------|--------|
| HuggingFace token `hf_ULwg...` | `showcase/gpu-universal/llm-local/test_mistral_7b.py` (deleted S139, in git history) | **Auto-revoked** by GitHub. File deleted from working tree. Token in history only. |

### Clean

- No active secrets in working tree
- AWS `AKIAIOSFODNN7EXAMPLE` is official AWS documentation example (not real)
- All test tokens are clearly synthetic (`"test-token"`, `"secret"`, etc.)
- No private keys, certificates, or SSH keys anywhere
- `@example.com` emails are RFC 2606 compliant

## Changes

### 1. `SecretString` Type (`toadstool_common::secret_string`)

New zero-leakage credential wrapper:

- **Zeroize-on-drop** via `zeroize` crate
- **Debug/Display** emit `[REDACTED]`
- **Serialize** emits `"[REDACTED]"` (prevents config-file round-trip leaks)
- **Deserialize** accepts raw values (for loading from config at startup)
- **`resolve_credential(name)`** — async resolution chain:
  1. Environment variable (`std::env::var`)
  2. OS keyring (placeholder — `D-KEYRING` debt item)
  3. BearDog delegation (placeholder — `D-BD-SECRET` debt item)
- 11 unit tests

**Files**: `crates/core/common/src/secret_string.rs` (new), `crates/core/common/src/lib.rs`, `crates/core/common/Cargo.toml`

### 2. Cloud Credential Hardening

Secret fields in cloud credential structs migrated from `String` to `SecretString`:

| Struct | Field | Before | After |
|--------|-------|--------|-------|
| `AWSCredentials` | `secret_access_key` | `String` | `SecretString` |
| `AWSCredentials` | `session_token` | `Option<String>` | `Option<SecretString>` |
| `AzureCredentials` | `client_secret` | `String` | `SecretString` |
| `GCPCredentials` | `service_account_key` | `String` | `SecretString` |
| `AuthMethod::Token` | `token` | `String` | `SecretString` |
| `AuthMethod::BearDogAuth` | `credentials` | `String` | `SecretString` |

Non-secret identifiers (`access_key_id`, `tenant_id`, `client_id`, etc.) remain `String`.

**Files**: `crates/distributed/src/cloud/credentials.rs`, `crates/distributed/tests/cloud_test.rs`, `crates/distributed/tests/cloud_deployment_tests.rs`

### 3. CI Secret Scanning

New `secret-scan` job in `.github/workflows/ci.yml`:

- Scans all tracked files for: `sk-*`, `hf_*`, `ghp_*`, `gho_*`, `glpat-*`, `AKIA*` (non-example), `xox*-*`, private key headers
- Runs on push/PR to master/main
- Fails CI if any pattern matches

### 4. `.gitignore` Hardening

Added blocks for: `*.env`, `.env.*`, `*-secrets/`, `api-keys*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `credentials.json`

### 5. Doc PII Cleanup

| File | Change |
|------|--------|
| `docs/reference/PRODUCTION_DEPLOYMENT_GUIDE.md` | `/path/to/home/...` → `$TOADSTOOL_SRC` |
| `docs/guides/PRIMAL_INTEGRATION_GUIDE.md` | `postgresql://user:pass@...` → `postgresql://$DB_USER:$DB_PASS@...` |
| `examples/biome-production.yaml` | Hardcoded `DATABASE_URL` → `${LEGACY_DATABASE_URL}` |

### 6. Housekeeping

- **Duplicate workspace member**: `crates/core/hw-learn` listed twice in root `Cargo.toml` — deduplicated.
- **Pre-existing clippy lint**: `toadstool-sysmon` collapsible_if resolved.
- **`.cursorignore` cleanup**: Removed 25+ entries for directories archived in S139.

## New Debt Items

| ID | Description | Priority |
|----|-------------|----------|
| D-KEYRING | Wire `LocalKeyringProvider` into `resolve_credential()` for OS keyring lookup | Low |
| D-BD-SECRET | Wire BearDog `secret.resolve` JSON-RPC into `resolve_credential()` chain | Low |

## Inter-Primal Impact

### For All Primals

`SecretString` is available at `toadstool_common::SecretString`. Any primal using
cloud credentials or external API tokens should adopt this type for secret fields.
The `resolve_credential()` chain provides a standard pattern for loading secrets
at runtime without hardcoding.

### For BearDog

Future work: expose a `secret.resolve` JSON-RPC method that ToadStool (and other
primals) can call to retrieve secrets from BearDog's vault. This completes the
credential resolution chain.

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo check` | PASS |
| `cargo clippy --workspace -D warnings -W clippy::pedantic` | PASS |
| `cargo fmt --check` | PASS (changed files) |
| `cargo doc -D warnings` | PASS |
| `cargo test` (affected crates) | PASS (57 tests) |
| Secret scan (working tree) | PASS (0 matches) |
