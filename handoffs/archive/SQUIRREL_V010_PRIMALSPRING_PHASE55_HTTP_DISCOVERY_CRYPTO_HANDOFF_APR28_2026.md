# Squirrel v0.1.0 — primalSpring Phase 55 Audit Resolution

**Date**: April 28, 2026 (session AN)
**Primal**: Squirrel (AI coordination)
**Source**: primalSpring v0.9.20 (Phase 55) — April 28, 2026

## Three Asks Resolved

### Ask 1: Native HTTP Provider Support (Ollama)

**Problem**: `inference.register_provider` only accepted `socket` (UDS path). Ollama is HTTP, causing registration to fail at availability checks (`Path::exists` on an HTTP URL returns false). Workaround was Songbird's `http.post` bridge.

**Solution**: Extended the registration wire format and `RemoteInferenceAdapter` to support both UDS and HTTP transports:

- **Wire format**: New optional `endpoint` param (`http://localhost:11434`). Either `socket` or `endpoint` must be provided.
- **Transport**: When `endpoint` is HTTP, adapter routes through Ollama REST API (`/api/generate` for text, `/api/embeddings` for embeddings).
- **Health check**: `is_available` uses TCP connect probe for HTTP endpoints instead of `Path::exists`.
- **HTTP client**: Lightweight raw TCP + HTTP/1.1 using tokio (no new dependencies, no reqwest, Tower Atomic pattern preserved for external HTTP).
- **Backward compatible**: Existing UDS providers continue to work unchanged.

**Files**: `remote_inference.rs`, `handlers_inference.rs`, `router_tests.rs`

### Ask 2: Inference Payload Encryption Foundation

**Problem**: Inference prompts and responses are plaintext on the wire. NUCLEUS two-tier crypto model requires encryption using purpose keys.

**Solution**: Extended `SecurityProviderClient` with the RPC surface for purpose-key crypto:

- `retrieve_purpose_key(purpose)` → `secrets.retrieve` JSON-RPC
- `encrypt_with_purpose(data, purpose)` → `crypto.encrypt` JSON-RPC (returns `{ v, ct, n, alg }` envelope)
- `decrypt_with_purpose(envelope, purpose)` → `crypto.decrypt` JSON-RPC

**Status**: Foundation only. Full wiring into inference handlers requires BearDog server-side support for `secrets.retrieve` and `crypto.encrypt/decrypt` with ChaCha20-Poly1305. When BearDog ships these methods, Squirrel can gate encryption on `FAMILY_ID` presence and wire it into `handle_inference_complete` / `RemoteInferenceAdapter`.

**File**: `security_provider_client.rs`

### Ask 3: DISCOVERY_SOCKET for Capability Resolution

**Problem**: `DISCOVERY_SOCKET` env var was only used for discovery service registration/heartbeat, not for resolving arbitrary capabilities. Hardcoded filesystem paths (`/run/user/`, `/tmp/biomeos/`) were the fallback.

**Solution**: Added discovery service query as Method 2 in `discover_capability()`:

1. Explicit env var (`{CAPABILITY}_PROVIDER_SOCKET`) — unchanged
2. **NEW**: Query discovery service via `DISCOVERY_SOCKET` (`discovery.find_provider` JSON-RPC)
3. Capability registry query — unchanged
4. Socket directory scan — unchanged (slow fallback)

Graceful degradation: if discovery service is unavailable, falls through silently to methods 3–4.

**Also fixed**: Discovery service docs incorrectly listed `SONGBIRD_SOCKET` as fallback step 2, but the implementation never read it. Docs now match code.

**Files**: `discovery.rs`, `discovery_service.rs`

## Quality Gates

- `cargo fmt` ✓
- `cargo clippy --workspace --all-targets -- -D warnings -W clippy::pedantic -W clippy::nursery` ✓ (0 warnings)
- `cargo test --workspace` ✓ (7,182 passed, 0 failures)
- `cargo deny check` ✓

## Remaining Evolution (for future sessions)

- Wire `encrypt_with_purpose` / `decrypt_with_purpose` into inference handlers when BearDog ships purpose-key RPC
- HTTPS support in HTTP provider transport (currently HTTP only — Ollama is typically local)
- Streaming support for HTTP providers (`/api/generate` with `"stream": true`)
