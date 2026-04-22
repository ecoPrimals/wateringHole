# rhizoCrypt v0.14.0-dev — Session 43 Handoff

## Comprehensive Audit + Deep Debt Evolution + Crypto Model

**Date**: 2026-04-15
**Branch**: main
**Tests**: 1,527 passing (0 failures)
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
cargo test               ✅ 1,507 passed
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
1,508 tests passing, clippy clean.

### S43.2 Addendum: Dependency Hygiene + Doc Sweep (April 16)

- **`cargo update`** — all deps to latest compatible semver; **RUSTSEC-2026-0007** (`opentelemetry_sdk` via tarpc) resolved
- **`deny.toml`** — removed stale advisory ignore; only RUSTSEC-2025-0141 (bincode v1 via tarpc) remains
- **`#[allow]` → `#[expect]`** in `metrics.rs` (lint policy alignment)
- **`cargo fmt`** — corrected formatting drift in 6 files from S43 compact style
- **Showcase binary names** — `songbird-cli`/`songbird-rendezvous` → `songbird` (canonical UniBin), `toadstool-cli` → `toadstool`
- **`showcase/README.md`** — `../bins/` path → `primalBins` (matches `showcase-env.sh`)
- **Doc metrics refresh** — `DEPLOYMENT_CHECKLIST.md` (76→65 demos, 9→10 specs), `RHIZOCRYPT_SPECIFICATION.md` (27→28 methods, coverage checkbox resolved), `00_SPECIFICATIONS_INDEX.md` date
- **Metrics**: 1,508 tests, 170 `.rs` files, ~48,800 lines, 724 max file

### S43.3 Addendum: async-trait Removal + DID Semantic Closure (April 16)

- **`async-trait` dependency removed** — 6 direct usages → manual `BoxFuture` desugaring; `ProtocolAdapter` + `ProtocolAdapterExt` + 4 impls (HTTP, UDS, tarpc, mock) converted; `async-trait` remains only as transitive dep via axum
- **DID → `public_key` gap RESOLVED** — `did:key:` strings are the canonical wire format; BearDog resolves `did:key:` → raw Ed25519 internally; formally closed in `CRYPTO_MODEL.md` §DID as Public Key Identifier

### S43.4 Addendum: Final Debt Sweep (April 16)

- **tarpc one-way observability** — fire-and-forget `let _ = client.call(…)` in `TarpcAdapter::call_oneway_json` evolved to structured `tracing::debug!` on failure; production error paths no longer silently discard
- **`deny.toml` wildcard policy** — `wildcards = "warn"` → `"allow"` for path deps (monorepo false-positive); advisory/ban/license/source checks all passing
- **Full audit clean**: 0 `#[allow(` in production code, 0 TODO/FIXME, 0 production unwrap/expect, 0 panic!, 0 unsafe, mocks behind `#[cfg(test)]` or `test-utils` feature only, no hardcoded primal names outside adapter/test code

### S43.5 Addendum: Transport Diagnostics — ludoSpring GAP-06 Response (April 20)

**Context**: ludoSpring V46 audit reports rhizoCrypt as "TCP-only, no UDS" (GAP-06), blocking 4+ composition experiments. This finding is **stale** — UDS has been unconditional on Unix since S23 (March 31) and formalized as "UDS unconditional, TCP opt-in" in S37 (April 12). The `LD-06` item was resolved in the S37 handoff and IPC compliance matrix.

**Root cause of confusion**: The `rhizocrypt doctor` command had **no transport diagnostics**. It reported DAG, storage, config (port/host), and discovery — but nothing about UDS. Springs teams running `doctor` saw TCP port info and no UDS mention, leading to the "TCP-only" conclusion.

**Fix**: Added `check_transport()` to `doctor.rs` — now reports:
- **Transport: UDS** — unconditional status, full socket path (`$XDG_RUNTIME_DIR/biomeos/rhizocrypt[-{family_id}].sock`)
- **Transport: TCP** — opt-in status (enabled/disabled, how to enable)
- **Transport: BTSP** — enforcement mode (required / dev bypass / not required)

Example `rhizocrypt doctor` output now includes:
```
[✓] Transport: UDS (unconditional, path=/run/user/1000/biomeos/rhizocrypt.sock)
[✓] Transport: TCP (disabled — opt-in: pass --port or set RHIZOCRYPT_PORT)
[✓] Transport: BTSP (not required — no FAMILY_ID set, raw JSON-RPC)
```

**For ludoSpring / springs teams**: Please re-validate with the current binary. `rhizocrypt server` binds UDS unconditionally without any flags. If BTSP handshake enforcement is the issue (FAMILY_ID set), ensure springs clients implement the BTSP Phase 2 handshake or use `BIOMEOS_INSECURE=1` for development validation.

### S43.6 Addendum: Doc Reconciliation + Final Sweep (April 20)

- **Doctor TCP alignment** — transport message lists all 3 opt-in env vars (`RHIZOCRYPT_PORT`, `RHIZOCRYPT_RPC_PORT`, `RHIZOCRYPT_JSONRPC_PORT`)
- **Showcase binary names** — remaining `songbird-rendezvous` → `songbird`, `../../../bins/` → `${PRIMAL_BINS:-../../../primalBins}`
- **Full deep-debt audit clean**: 0 files >800L, 0 `#[allow(` in production, 0 TODO/FIXME, 0 unsafe, 0 production mocks, no hardcoded primals outside adapters/tests, no mandatory splits among 600L+ files
- **Metrics**: 1,508 tests, 170 `.rs` files, ~48,800 lines, 724 max file

### S43.7 Addendum: Manifest-Based Discovery — PG-32 Resolution (April 20)

**PG-32 root cause**: UDS listener was binding correctly (since S23), but **no manifest file was published**. Springs calling `discover_by_capability("dag")` scanned `$XDG_RUNTIME_DIR/biomeos/*.json` and found no `rhizocrypt.json`. The UDS socket existed but was invisible to capability-based discovery.

**Fix**: Server startup now publishes `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.json`:
```json
{
  "primal": "rhizocrypt",
  "version": "0.14.0-dev",
  "socket": "/run/user/1000/biomeos/rhizocrypt.sock",
  "capabilities": ["dag.session.create", "dag.event.append", "health.check", ...]
}
```
- Published after UDS listener binds, before TCP decision
- Includes optional `address` field when TCP is active
- All 28 capabilities from `METHOD_CATALOG` listed
- `unpublish_manifest()` called on every shutdown path (clean exit)

**For ludoSpring / springs teams**: `discover_by_capability("dag")` will now return rhizoCrypt's manifest with the UDS socket path. Re-run composition experiments exp094–096, exp098.

### S43.8 Addendum: TCP Dedup + Doctor Manifest + Integration Test (April 20)

- **`resolve_bind_addr` dedup** — TCP address resolved once, passed to both manifest publication and `serve_with_tcp()`; eliminates `.ok()` vs `?` inconsistency
- **Doctor manifest presence** — `check_transport()` now reports `Discovery: manifest` pass/warn based on `rhizocrypt.json` existence
- **Manifest lifecycle integration test** — validates publish → discover → unpublish round-trip
- **Metrics**: 1,508 tests (was 1,507), all passing, 0 clippy warnings, 0 fmt diffs

### S43.8b Addendum: Doc Reconciliation + Spec Modernization (April 20)

- **Test count alignment** — README, CONTEXT, CHANGELOG metrics all updated to 1,508
- **Spec count** — CONTEXT now correctly reports 12 specification documents (was 11)
- **`async-trait` removal from specs** — `STORAGE_BACKENDS.md`, `DATA_MODEL.md`, `INTEGRATION_SPECIFICATION_V2.md` updated to native async syntax (RPITIT), matching S43.3 codebase removal
- **Spec dates** — three specs updated from Dec 2025 / March 2026 to April 2026
- **Discovery language** — integration spec now references manifest-based discovery alongside Songbird
- **Debris audit** — zero TODOs/FIXMEs in crates/, no temp files, no stale binaries, no .env, no orphan scripts; `specs/archive/` retained as fossil record

### S45.1: BTSP Liveness Passthrough — First-Byte Auto-Detect (April 20)

**Resolves primalSpring Phase 45 audit item #3**: plain `health.check` probes on BTSP-enforced UDS sockets no longer fail with EPIPE/ECONNRESET.

**Root cause**: UDS handler always entered BTSP length-prefix framing. Plain JSON-RPC `{...}` first byte was interpreted as a u32 frame length (~1.5 billion), exceeding MAX_FRAME_SIZE, causing immediate connection drop.

**Fix**: First-byte auto-detect in `handle_uds_connection`:
- `{` or `[` → liveness-only JSON-RPC (health.check, capability.list, identity.get, etc.)
- Anything else → BTSP handshake, then full JSON-RPC
- Data methods (`dag.*`, etc.) return `-32000 FORBIDDEN` with a hint to use BTSP
- `UNAUTHENTICATED_METHODS` allowlist: single source of truth for bypass-eligible methods

**For springs teams**: `health.check` over raw UDS now works on BTSP-enforced sockets. Remove any `check_skip()` workarounds for rhizoCrypt health probes.

**Metrics**: 1,512 tests (was 1,508), 0 clippy warnings, 0 fmt diffs

### S45.1b Addendum: Doc Reconciliation (April 20)

- **Test count alignment** — all docs updated to 1,512: CHANGELOG (3 stale refs), showcase/README (2 refs), docs/DEPLOYMENT_CHECKLIST (2 refs), specs/RHIZOCRYPT_SPECIFICATION (1 ref)
- **Line count** — CONTEXT, CHANGELOG updated from ~48,800 to ~48,600 (measured 48,604)
- **Debris audit** — zero artifacts, temp files, empty dirs, .env, stale paths; `specs/archive/` retained as fossil record; `showcase/04-sessions/Cargo.lock` is intentional (nested demo crate)

### S45.2: BTSP Wire-Format Alignment — JSON-Line Interop (April 21)

**Resolves primalSpring Phase 45b BTSP escalation**: `{"protocol":"btsp","version":1,...}\n` from primalSpring was misclassified as invalid JSON-RPC by the S45.1 first-byte auto-detect.

**Root cause**: Three wire-format mismatches between rhizoCrypt (length-prefixed binary, `[u8; 32]` arrays) and primalSpring (newline-delimited JSON, base64 strings, `protocol` discriminator field).

**Fix**: Three-way auto-detect in `handle_uds_connection`:
- First byte `{` + `"protocol":"btsp"` → JSON-line BTSP handshake (`accept_handshake_jsonline`), then full JSON-RPC
- First byte `{` + `"jsonrpc"` → liveness-only JSON-RPC (S45.1 path)
- Non-`{` first byte → length-prefixed BTSP handshake (internal path)

**New code**:
- `btsp/framing.rs`: `read_json_line` / `write_json_line` — byte-by-byte newline framing
- `btsp/types.rs`: `ClientHelloWire`, `ServerHelloWire`, `ChallengeResponseWire`, `HandshakeCompleteWire`, `HandshakeErrorWire` — base64 string fields for primalSpring interop
- `btsp/server.rs`: `accept_handshake_jsonline` — same X25519 + HMAC-SHA256 crypto, JSON-line framing
- `jsonrpc/uds.rs`: updated routing to read first line and detect `"protocol":"btsp"` vs `"jsonrpc"`

**For springs teams**: primalSpring BTSP ClientHello (`{"protocol":"btsp","version":1,"client_ephemeral_pub":"<base64>"}\n`) is now correctly routed to the BTSP handshake path. Remove any `check_skip()` workarounds for BTSP probes against rhizoCrypt.

**Metrics**: 1,527 tests (was 1,512), 0 clippy warnings, 0 fmt diffs

### S45.2b Addendum: Doc Reconciliation + Debris Audit (April 21)

- **Test count alignment** — 6 stale references to 1,512 updated to 1,527: `docs/DEPLOYMENT_CHECKLIST.md` (2), `specs/RHIZOCRYPT_SPECIFICATION.md` (1), `showcase/README.md` (2), `stop-songbird.sh` comment (1 "Rendezvous" → removed)
- **Source metrics** — `.rs` file count corrected from 170 to 166; total lines updated from ~48,600 to ~49,200 (measured 49,237)
- **Spec date** — `RHIZOCRYPT_SPECIFICATION.md` updated from March 2026 to April 2026
- **Debris audit** — zero build artifacts, temp files, .env, empty dirs; `specs/archive/` retained as fossil record; `showcase/04-sessions/Cargo.lock` is intentional nested demo crate
- **Zero TODOs/FIXMEs** in any markdown doc

### S46: BTSP Handshake Robustness — Error Reporting + UDS Integration Tests (April 22)

**Resolves primalSpring Phase 46 audit item**: "BTSP enforced but relay incomplete — connections get `Connection reset by peer`".

**Root cause analysis**: The audit's "relay to BearDog via `BTSP_PROVIDER_SOCKET`" is a **loamSpine/sweetGrass pattern** (provider delegation). rhizoCrypt is self-sovereign — its BTSP is entirely local (HKDF/X25519/HMAC-SHA256, no BearDog delegation). primalSpring's own `PRIMAL_GAPS.md` confirms: "rhizoCrypt: BTSP Phase 2 COMPLETE — Local crypto (self-sovereign)". The "relay incomplete" diagnosis was incorrect for this primal.

**Actual bug found**: On handshake failure (invalid key length, version mismatch, etc.), the error path was:
1. Sending a generic error `{"error":"handshake_failed","reason":"family_verification"}` regardless of actual cause
2. Dropping the writer immediately without explicit `shutdown()`, causing OS-level RST before the error response reached the client
3. Client saw `ECONNRESET` instead of the error JSON line

**Fix** (3 changes):
- `btsp/server.rs`: `send_handshake_error_jsonline` now accepts a `reason: &str` parameter — the actual `HandshakeError` message flows to the client
- `jsonrpc/uds.rs` (JSON-line error path): passes `e.to_string()` as reason, explicit `writer.shutdown().await` after sending error
- `jsonrpc/uds.rs` (length-prefixed error path): matching `writer.shutdown()` for consistency

**New tests** (2):
- `test_btsp_jsonline_handshake_over_uds` — full 4-step handshake over real `UnixStream::pair()`: ClientHello → ServerHello → ChallengeResponse → HandshakeComplete → post-handshake JSON-RPC `health.check` round-trip
- `test_btsp_jsonline_invalid_key_returns_error` — sends the audit's socat test (`dGVzdA==` = 4-byte key), verifies client receives structured error JSON (not ECONNRESET) with key-length diagnostic

**For springs teams**: rhizoCrypt does NOT relay BTSP to BearDog. The `BTSP_PROVIDER_SOCKET` / `create_session` relay pattern applies to loamSpine and sweetGrass only. rhizoCrypt's BTSP handshake is end-to-end verified over real Unix sockets.

**Metrics**: 1,529 tests (was 1,527), 0 clippy warnings, 0 fmt diffs

### S46b Addendum: Clippy Pedantic Clean + Deep Debt Audit (April 22)

Full deep-debt audit across all requested dimensions:

| Dimension | Result |
|---|---|
| Files >800 lines | **None** — max 724L |
| Unsafe code | `forbid(unsafe_code)` on all crates, zero blocks |
| External/C deps | Pure Rust, `deny.toml` bans openssl/ring/aws-lc |
| TODO/FIXME/unimplemented! | **Zero** in code and non-changelog docs |
| Mocks in production | All `Mock*` behind `#[cfg(any(test, feature = "test-utils"))]` |
| Hardcoded primal names | **Fixed**: "BearDog/Squirrel" → ecosystem-generic in `newline.rs` |
| Clippy pedantic+nursery | **Zero warnings** — sole `similar_names` fixed (`peek`→`probe`) |
| Clone discipline | All justified (DashMap guards, Arc, HashMap keys, retry) |

- **Debris audit** — zero temp files, empty dirs, stale artifacts, .env, orphan scripts
- **Line count** — CONTEXT.md updated from ~49,200 to ~49,400 (measured 49,410)
- **CHANGELOG** — S46 + S46b entries added, S45.2 test count corrected (1,527, not 1,529)
- `showcase/04-sessions/Cargo.lock` confirmed intentional (standalone nested demo crate)
- `specs/archive/INTEGRATION_SPECIFICATION.md` retained as fossil record

### Remaining (Not Blocking)

- `Arc<str>` hot-path evolution — intentional roadmap item
- **BTSP Phase 3** — per-frame AEAD using derived session keys
