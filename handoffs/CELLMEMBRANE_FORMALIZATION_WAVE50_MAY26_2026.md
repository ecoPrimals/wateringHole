# cellMembrane — Formalization as Deployable Infrastructure

**From**: cellMembrane team (ironGate)
**To**: primalSpring (upstream audit), all primal teams
**Date**: May 26, 2026
**Wave**: 50
**Priority**: Medium — formalizes membrane architecture for open-source deployability
**Status**: Complete — requesting upstream review

---

## Summary

cellMembrane has been formalized from 8 files (docs + bash scripts) into a typed
Rust system with 4 spec documents, a `cellmembrane-types` crate (46 tests), and a
reference `membrane.toml` configuration. The membrane architecture is now encoded
in types that can be validated programmatically, and the config file is the
open-source interface for third-party membrane operators.

## What Changed

### New: `specs/` (4 documents)

| Spec | Purpose |
|------|---------|
| `CELLMEMBRANE_ARCHITECTURE.md` | Canonical 3-channel model (Signal/Relay/Surface), crypto layers, process isolation, firewall policy |
| `MEMBRANE_COMPOSITION_MODEL.md` | Composition ladder: relay → rustdesk → tower → nest, with per-tier requirements |
| `FIELDMOUSE_CONTRACT.md` | What a fieldMouse deployment must satisfy — hardening, credentials, lifecycle |
| `MULTI_MEMBRANE_DEPLOYMENT.md` | `membrane.toml` schema, provider abstraction, multi-region topology |

### New: `crates/cellmembrane-types/` (Rust)

Pure types crate — `#![forbid(unsafe_code)]`, zero async, serde + toml only.

| Module | Types | Source |
|--------|-------|--------|
| `channels.rs` | `MembraneChannel`, `ChannelConfig`, `TrustLevel`, `CryptoLayer` | MEMBRANE_CHANNEL_ARCHITECTURE.md |
| `composition.rs` | `MembraneComposition`, `CompositionSpec` | `deploy_membrane.sh` case statements + `ports.env` |
| `config.rs` | `MembraneConfig`, `HardeningConfig`, `TelemetryConfig` | New — `membrane.toml` parser |
| `credentials.rs` | `CredentialModel`, `CredentialFile`, `credential_files_for()` | `share_credentials.sh` + MEM-08/MEM-12 |
| `firewall.rs` | `FirewallRuleset`, `FirewallRule` | UFW logic in `deploy_membrane.sh` |
| `identity.rs` | `MembraneIdentity` | `VPS_STATE.md` + `tower.env` |
| `provider.rs` | `ProviderConfig`, `SubstrateProfile` | Hardcoded DO config in `deploy_membrane.sh` |
| `service.rs` | `MembraneService`, `BinaryIntegrity`, `binary_integrity_for()` | `membrane/*.service` units + MEM-09 |
| `validation.rs` | `Report`, `ReportEntry`, `Severity` | `plasmidbin-types` pattern |

### New: `membrane.toml`

Reference configuration for the live `membrane-relay` VPS (Tower composition,
DigitalOcean nyc1). This is the file a third party writes to deploy their own
membrane.

### Gap Closure: Dark Forest Audit Alignment

Compared `cellmembrane-types` against `darkforest_membrane.sh` (MEM-01..17),
`s_membrane_composition.rs` (4 pillars), and `ports.env`. Closed 5 gaps:

| Gap | MEM Check | Resolution |
|-----|-----------|------------|
| Journald persistence | MEM-07 | `HardeningConfig.journald_persistent` |
| Credential file permissions | MEM-08, MEM-12 | `credential_files_for()` returns paths + expected mode/owner |
| Binary integrity | MEM-09 | `binary_integrity_for()` with BLAKE3/SHA-256 per binary |
| RustDesk key path | MEM-12 | Included in credential file inventory |
| Telemetry/shadow config | Pillar 4 | `TelemetryConfig` with `shadow_mode`, `cutover_gate_days`, `skunkbat_correlation` |

## Port Registry Note

`cellmembrane-types` models membrane-deployed ports (e.g. rhizoCrypt :9601,
sweetGrass :9850) which differ from `ports.env` gate-standard ports (rhizoCrypt
:9700, sweetGrass :9720). This is intentional — membrane and gate deployments
use different port ranges. The discrepancy is now documented in the types.

## What Did NOT Change

- `deploy_membrane.sh` — stays operational, Rust types describe the same domain
- Existing operational docs — VPS_STATE.md, RUNBOOKS.md untouched (except tracker update)
- biomeOS integration — no compile-time dep on `biomeos-graph` yet
- No CLI binary — types only, CLI follows in a later cycle

## Upstream Review Requested

### For primalSpring
- [ ] Audit `specs/` against existing wateringHole standards for consistency
- [ ] Verify `CompositionSpec` primal lists match `ports.env` compositions
- [ ] Validate `TelemetryConfig` fields against `s_membrane_composition.rs` Pillar 4
- [ ] Review `membrane.toml` schema for open-source consumer readiness

### For primal teams
- [ ] Confirm service port/protocol/bind in `MembraneService::for_binary()` matches your primal
- [ ] Confirm health check method name (`health.liveness`, `tcp_connect`, `https_probe`)
- [ ] Flag any missing credential files in `credential_files_for()`

### For projectNUCLEUS
- [ ] Review `HardeningConfig.prohibited_services()` against `darkforest_membrane.sh` MEM-06
- [ ] Validate `BinaryIntegrity` expectations against `checksums.toml`

## Next Cycle

- `cellmembrane` CLI binary (parse + validate + generate UFW script)
- Replace `deploy_membrane.sh` composition logic with Rust
- biomeOS `biomeos-graph` integration (typed `CompositionModel::Membrane`)
- Gate-local membrane layer (inner membrane leading outer)
