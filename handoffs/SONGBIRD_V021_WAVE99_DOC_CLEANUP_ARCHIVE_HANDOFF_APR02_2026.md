# Songbird v0.2.1 Wave 99: Doc Cleanup, Archive, Capability Naming Alignment

**Date**: April 2, 2026  
**Primal**: Songbird  
**Version**: v0.2.1  
**Session**: Wave 99  
**Scope**: Root doc updates, stale spec archival, capability-based naming in docs/specs, CHANGELOG entries

---

## Summary

Cleaned and updated all root documentation, archived stale specs and milestone docs to `specs/archive/`, aligned remaining spec examples with capability-based discovery (`SECURITY_PROVIDER_SOCKET` instead of `BEARDOG_SOCKET`), and added CHANGELOG entries for waves 97–98.

## Root Doc Updates

| File | Change |
|------|--------|
| `README.md` | Updated description from "BearDog via JSON-RPC IPC" to "security provider capability"; env vars now show `SECURITY_PROVIDER_SOCKET` first; architecture diagram uses "Security Provider"; crypto-provider crate description updated; test metrics reconciled with CONTEXT.md; `serial_test` status corrected to "1 E2E suite" |
| `CONTEXT.md` | Test count updated from 12,124 to 12,154; ignored from 269 to ~159; hardcoded primal names description updated to reference `security.sock` symlink |
| `REMAINING_WORK.md` | Test count updated to 12,154/~159 ignored; `serial_test` status corrected to reflect 1 suite in orchestrator_comprehensive_tests.rs |
| `CHANGELOG.md` | Added entries for wave 97 (capability-based discovery compliance) and wave 98 (deep debt evolution) |

## Archived to `specs/archive/`

| Original | Reason |
|----------|--------|
| `IMPLEMENTATION_CHECKLIST.md` | Stale — references "21 remaining unwrap()" (now 0), outdated quality bars |
| `PROTOCOL_NEGOTIATION_STATUS_V3_12_1.md` | Historical snapshot from v3.12.1 (Jan 2026); protocol landscape has evolved |
| `SONGBIRD_TLS_13_COMPLETE.md` | Milestone doc marked "100% COMPLETE" — preserved as historical record |
| `SONGBIRD_EVOLUTION_EXECUTION.md` | References v5.20.0 from pre-renumbering era |
| `SONGBIRD_NEURALAPI_ALIGNMENT_V3_12_1.md` | Historical alignment doc from v3.12.1 |
| `SONGBIRD_FUTURE_WORK.md` | Superseded by `REMAINING_WORK.md` as canonical roadmap |
| `UNIVERSAL_STANDARDS_IMPLEMENTATION_PROGRESS.md` | "MISSION ACCOMPLISHED" from Jan 2025 |
| `PRIMAL_RESPONSIBILITY_SEPARATION_SPEC.md` | Code examples use stale `discover_beardog()` naming |

## Archived to `fossilRecord/`

| Original | Reason |
|----------|--------|
| `docs/architecture/PURE_RUST_TLS_VIA_BEARDOG.md` | Milestone narrative superseded by CHANGELOG wave entries |

## Capability Naming Alignment in Specs

| File | Change |
|------|--------|
| `SOVEREIGN_MULTIPATH_PROTOCOL.md` | 3 `BEARDOG_SOCKET` examples → `SECURITY_PROVIDER_SOCKET`; removed `SONGBIRD_SECURITY_PROVIDER` redundant var |
| `docs/architecture/BEARDOG_CRYPTO_API_SPEC.md` | Renamed to `SECURITY_PROVIDER_CRYPTO_API_SPEC.md` |
| `specs/00_SPECIFICATIONS_INDEX.md` | Updated links to archived files; header date updated |

## Code Hygiene

| File | Change |
|------|--------|
| `songbird-quic/src/endpoint/udp.rs` | Bare `#[allow(dead_code)]` → `#[allow(dead_code, reason = "...")]` (2 locations) |

## Verification

- `cargo clippy --workspace --all-targets --all-features`: 0 warnings
- All 30 crates compile clean
