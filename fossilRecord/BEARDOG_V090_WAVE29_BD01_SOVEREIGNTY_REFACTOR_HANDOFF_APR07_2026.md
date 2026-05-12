<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 29: BD-01 Encoding Hint, Sovereignty Sweep, Smart Refactoring & Debt Cleanup

**From:** BearDog
**To:** primalSpring, ecosystem
**Date:** April 7, 2026
**Priority:** RESOLVED — primalSpring audit gap BD-01 closed; sovereignty and debt sweep complete

---

## Context

primalSpring's downstream audit reported a LOW priority gap:
`crypto.verify_ed25519` did not accept encoding hints from `WireWitnessRef`.
Callers with `encoding: "hex"` had to manually decode hex → raw bytes → base64
before calling BearDog verify. This wave resolved BD-01 and then executed a
comprehensive sovereignty sweep, smart refactoring, and debt cleanup pass.

---

## BD-01: Encoding Hint Resolution

### Root Cause

`handle_verify_ed25519` assumed all inputs were base64-encoded. The trio's
`WireWitnessRef` now carries `encoding`, `algorithm`, and `tier` fields, but
BearDog ignored the `encoding` field entirely.

### Changes

| File | Change |
|------|--------|
| `beardog-tunnel/.../crypto/asymmetric.rs` | New `decode_with_encoding()` helper supporting base64, base64url, hex, utf8, none |
| `beardog-tunnel/.../crypto/asymmetric.rs` | `handle_verify_ed25519` now reads optional `encoding` param (default: base64) |
| `beardog-tunnel/.../crypto/asymmetric.rs` | 7 new tests: default base64, explicit hex, hex with 0x prefix, base64url, unsupported encoding error, invalid hex error, backwards-compat (no encoding field) |

### Wire Protocol

```json
{
  "jsonrpc": "2.0",
  "method": "crypto.verify_ed25519",
  "params": {
    "message": "<encoded>",
    "signature": "<encoded>",
    "public_key": "<encoded>",
    "encoding": "hex"
  }
}
```

`encoding` is optional. Omitting it or passing `"base64"` preserves existing behavior.
Supported values: `base64`, `base64url`, `hex`, `utf8`, `none`.

---

## Sovereignty Sweep

Removed 50+ hardcoded primal names from production doc comments, test fixtures, and e2e tests:

| Scope | Count | Examples |
|-------|-------|---------|
| Production doc comments | ~20 files | "Songbird's relay" → "Relay coordinator"; "NestGate storage" → "storage.store capability" |
| Test fixtures/data | ~15 files | `"primal": "ToadStool"` → `"compute-peer"`; `"songbird-family"` → `"peer-family-alpha"` |
| E2E/integration tests | ~10 files | Socket paths, JSON fixtures, variable names genericized |

All replacements use capability-based language or generic peer names (`peer-alpha`, `compute-peer`, `storage-peer`) per the Primal Responsibility Matrix.

---

## Smart Refactoring — 3 Large Files Decomposed

| Original File | Size | Result |
|---------------|------|--------|
| `beardog-threat/src/threat/types/mod.rs` | 862L | 33L hub + 9 domain submodules (taxonomy, source_target, mitigation, intel, ml_model, security_telemetry, incident_response, detection_rules, threat_event) |
| `beardog-core/src/capability_router.rs` | 861L | `capability_routing/` directory with 5 modules (mod, strategy, scoring, filters, types) |
| `beardog-cli/src/handlers/key.rs` | 875L | `key/` directory with 3 modules (generate, list, storage) |

All public API paths preserved via `pub use` re-exports.

---

## Additional Cleanup

| Area | Change |
|------|--------|
| Dead code | Deleted `zero_copy/optimized.rs` (830L, never compiled — orphan duplicate) |
| Dependencies | Removed unused `serde_yaml` from beardog-core and beardog-adapters |
| Production stubs | FIDO2 phase wording aligned; discovery `announce_via_service_registry` upgraded to `warn!` |
| Root docs | CONTEXT.md, START_HERE.md, CHANGELOG.md, STATUS.md updated with current metrics |
| specs/README.md | Removed phantom `otherTeams/` and `experiments/` directory references |
| Showcase index | Cleaned stale timelines, removed broken doc links, genericized ecosystem integration section |
| Stale references | `specs/IMPLEMENTATION_GAPS_NOV_2025.md` pointer → `ROADMAP.md` |
| Zero-copy IPC | `JsonRpcRequest.jsonrpc` field evolved from `String` to `Cow<'static, str>` |

---

## Quality Gates — All Green

| Gate | Result |
|------|--------|
| `cargo fmt --all -- --check` | Pass |
| `cargo clippy --workspace --all-features -- -D warnings` | Pass (0 warnings) |
| `cargo doc --workspace --no-deps` | Pass |
| `cargo test --workspace` | 14,372 pass, 0 fail, 132 ignored |

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 14,372 |
| Coverage | 90%+ line (llvm-cov) |
| Files > 1000 LOC | 0 (production) |
| Production `unsafe` | 0 (`forbid(unsafe_code)`) |
| Hardcoded primal names | 0 in production code and docs |
| TODO/FIXME/HACK | 0 |

---

## For primalSpring

The reported "LOW" gap (BD-01: `crypto.verify_ed25519` encoding hint) is **RESOLVED**.
BearDog now internally decodes evidence based on the `encoding` field from
`WireWitnessRef`, eliminating the caller-side hex→base64 workaround.

The sovereignty sweep ensures BearDog has zero hardcoded knowledge of peer primals
in production code, doc comments, and test data — consistent with the Primal
Responsibility Matrix and self-knowledge principle.

No action required from primalSpring. This handoff is informational.
