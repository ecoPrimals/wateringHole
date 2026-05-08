# skunkBat v0.2.0-dev — Deep Debt: Observability Wiring + Genetic Detection + Transport Split

**Date**: May 5, 2026
**From**: skunkBat team
**To**: primalSpring, BearDog, biomeOS, Songbird, ecosystem
**Triggered by**: primalSpring Phase 58+ — "no new debt" confirmation + ongoing deep debt directive

---

## Summary

Deep debt evolution pass: production observability metrics are now wired to live operations,
genetic threat detection calls the real lineage verifier, `RuntimeVerifier` enum dispatch
enables automatic provider upgrade, and `btsp.negotiate` is cleanly separated from
application dispatch. Six items resolved, 338 tests passing.

---

## What Was Evolved

### 1. SecurityObserver Metrics Wired to Live Pipeline

Previously, `record_*` methods on `SecurityObserver` were never called from production code.
Now:

| Operation | Counter Incremented |
|-----------|-------------------|
| `detect_threats()` | `record_threat_detected` (per threat found) |
| `respond_to_threat()` | `record_threat_mitigated` + `record_quarantine` + `record_alert` (granular by action type) |
| `scan_network()` | `record_scan_performed` |

`DefenseEngine::respond` now returns `ActionType` so the caller can instrument appropriately.

### 2. Genetic Threat Detection — No-Op → Real Verifier Call

`detect_genetic_threats` was previously a stub that always returned an empty list.
Now:
- Checks `lineage_id` configuration
- Calls `lineage_verifier.is_family(my_lineage)` on the injected verifier
- On verification failure → produces `UnknownLineage` threat (Critical severity, 0.95 confidence)
- On verifier unavailability → gracefully skips (debug log)

### 3. RuntimeVerifier Enum Dispatch (`integrations::verifier`)

New module `skunk-bat-integrations/src/verifier.rs`:
- `RuntimeVerifier::from_env()` probes:
  - `LINEAGE_ENDPOINT` env var (TCP)
  - `{BIOMEOS_SOCKET_DIR}/lineage-verification.sock` (UDS)
- If either exists → `RuntimeVerifier::Remote(RemoteLineageVerifier::from_env())`
- Otherwise → `RuntimeVerifier::Local(LocalLineageVerifier)` (conservative deny)

Zero-cost enum dispatch, no trait objects, no `dyn`.

### 4. Transport Method Split

`btsp.negotiate` separated from application `METHODS` into `TRANSPORT_METHODS`:
- `capabilities.list` and `lifecycle.capabilities` advertise both arrays combined
- `dispatch()` correctly rejects `btsp.negotiate` as unknown (it's handled at the connection layer)
- Two new tests enforce this invariant

### 5. SKUNKBAT_LISTEN_ADDR Environment Variable

Bind address now driven by `SKUNKBAT_LISTEN_ADDR` env var (defaults to `0.0.0.0`),
giving parity with `SKUNKBAT_PORT`.

### 6. Threat ID Format Evolution

From: `format!("anomaly-{:?}", SystemTime::now())` (Debug-formatted, ugly)
To: `format!("anomaly-{}", microsecond_epoch)` (clean, monotonic-ish)

---

## Build Health

| Metric | Value |
|--------|-------|
| Tests | 338 passing / 0 failures / 15 ignored |
| Clippy | CLEAN (pedantic + nursery, `-D warnings`) |
| Format | CLEAN |
| Docs | CLEAN |
| Deny | CLEAN |
| Source files | 43 |
| Max file | 790 lines (`negotiate.rs`) |
| Version | 0.2.0-dev |

---

## Remaining Gaps

| Gap | Priority | Status |
|-----|----------|--------|
| BearDog live `lineage.verify` endpoint | CRITICAL (blocks real genetic detection) | `RemoteLineageVerifier` ready, needs BearDog to serve |
| Network defense execution | CRITICAL | Actions logged, need OS/firewall abstraction |
| ToadStool / Songbird live discovery | HIGH | Clients written, `#[ignore]`-gated |
| Thymic selection model | LOW | Blocked on BearDog `lineage.list` |

---

## For Ecosystem Primals

### BearDog
- skunkBat now actively calls `lineage.verify` and `lineage.list` via `RuntimeVerifier`
- When BearDog exposes these endpoints, genetic detection lights up automatically
- No skunkBat code changes needed — env var `LINEAGE_ENDPOINT` or socket presence is sufficient

### Songbird
- skunkBat registers via `ipc.register` on startup (prior handoff)
- Federation broadcast alerts will use `record_alert` counter for visibility

### biomeOS
- skunkBat supports Discovery Escalation Hierarchy tiers 1, 3, and 5
- `SKUNKBAT_LISTEN_ADDR` + `SKUNKBAT_PORT` enable flexible deployment

---

## Doc Cleanup (same session)

- Source file count: 39/40 → **43** across README.md, CONTEXT.md
- Max file size: 780 → **790** aligned to actual
- `COMPOSABLE_PRIMITIVES_SPEC.md` consumed capabilities updated to match implementation method names
- `RUN_ALL_LOCAL.sh` next-steps relative paths fixed
