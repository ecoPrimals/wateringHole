# benchScale + agentReagents Modernization Handoff

**Date**: March 28, 2026
**Status**: Complete — both tools modernized and ready for Phase B/C work
**Builds on**: `BENCHSCALE_AGENTREAGENTS_LOCAL_VALIDATION_SUBSTRATE_HANDOFF_MAR28_2026.md`

---

## What Changed

### benchScale v3.0.0

Deep Rust modernization — the crate is now idiomatic, maintainable, and primal-agnostic.

| Area | Before | After |
|------|--------|-------|
| YAML | `serde_yaml` 0.9 (deprecated) | `yaml_serde` 0.10 (official maintained fork) |
| Logging | `log` + `env_logger` + `tracing` (3 facades) | `tracing` only (2 deps removed) |
| CLI | Manual `std::env::args()` parsing | clap 4.5 with derive macros |
| Config | Hardcoded paths, IPs, OS defaults | Env-overridable via `BENCHSCALE_*` vars, capability-based |
| Error handling | `anyhow` + `thiserror` inconsistent | `thiserror` public API, `config_legacy` deprecated |
| Production safety | `unwrap()` in `image_builder`, `boot_diagnostics` | Proper error propagation |
| Primal-agnostic | "Songbird" in test fixtures, `primal_substrate` in docs | Generic terms, no ecosystem coupling |
| Module structure | 4 files >700 lines with inline tests | Tests extracted to dedicated files (212 pass) |
| Dead code | Orphan `.rs` files, fake `run-tests.sh`, misnamed `deploy-to-lab.sh` | Archived, replaced with real wrappers |
| Naming | `pub mod tests` (conflicts with `#[cfg(test)]`) | `pub mod scenarios` |

### agentReagents v1.2.0

Shell hardening, golden path selection, and full branding cleanup.

| Area | Before | After |
|------|--------|-------|
| Error handling | `set -e` only (16 scripts) | `set -euo pipefail` (all 9 active scripts) |
| Configuration | Hardcoded `/var/lib/libvirt/images`, `iontest` | `configs/defaults.env` sourced everywhere |
| Script organization | 16 scripts in flat `scripts/` | 9 active + 9 legacy in `scripts/legacy/` |
| Integrity | `verify-setup.sh` checked size only | SHA256 checksum verification from `docs/CHECKSUMS.md` |
| Quality gates | None | `lint.sh` (18/18 pass), `update-checksums.sh` |
| Branding | ionChannel/syntheticChemistry in 7+ scripts, all docs | ecoPrimals throughout active code and docs |
| Cloud-init | Duplicate `iproute2`, no `ports.env` | Clean packages list, default `ports.env` generation |
| Documentation | Stale session notes in root | Archived to `archive/docs/`, legacy guides header-tagged |
| `.gitkeep` | Missing (empty dirs wouldn't survive clone) | Present in all artifact directories |

---

## Specs Written

- `benchScale/specs/BENCHSCALE_EVOLUTION.md` — Full Phase A–D roadmap (state model, clap CLI, deployment matrix, IPC compliance)
- `agentReagents/specs/AGENTREAGENTS_EVOLUTION.md` — Full Phase A–D roadmap (golden path, manifest, quality gates, config centralization)

Phase A executed for both. Phases B–D defined and tractable.

---

## What's Next (Phase B–D)

### benchScale
- **Phase B**: Unify state model (`.state/` canonical, Rust CLI reads it, fix `destroy`)
- **Phase C**: Deployment validation matrix (nucleus-3node live test, cross-arch binaries, enforce tc presets)
- **Phase D**: IPC compliance integration (deploy reads `primal_launch_profiles.toml`, TCP/UDS-first testing)
- **Examples**: Several need `--features libvirt` and have stale `ImageBuilder` APIs — separate cleanup pass

### agentReagents
- **Phase B**: `setup-reagents.sh --minimal` flag, archive documentation for legacy flows
- **Phase C**: shellcheck target, config YAML validation, checksum generation automation
- **Phase D**: Shared `defaults.env` for all paths, consistent headers

### Ecosystem
- Update `IPC_COMPLIANCE_MATRIX.md` with per-primal health probe protocol (TCP JSON-RPC vs HTTP)
- benchScale `deploy-ecoprimals.sh` should read the compliance matrix instead of hardcoding launch commands
- `PLASIDBIN_ECOBIN_COMPLIANCE_ALL_PRIMALS_HANDOFF_MAR28_2026.md` filename has a typo (PLASIDBIN → PLASMIDBIN)

---

## Files Modified (across both repos)

### benchScale (35+ files)
- `Cargo.toml` — v3.0.0, yaml_serde, removed log+env_logger, clap to deps
- `src/bin/main.rs` — full clap rewrite
- `src/lib.rs` — `scenarios` module, deprecated re-export
- `src/error.rs` — unchanged (thiserror already correct)
- `src/image_builder.rs` — tracing, unwrap fix, tests extracted
- `src/backend/libvirt/vm_guard.rs` — tracing
- `src/backend/libvirt/boot_diagnostics.rs` — unwrap fixes
- `src/constants.rs` — env-overridable defaults
- `src/config_legacy.rs` — deprecated, stale paths removed
- `src/backend/docker.rs` — hardened image feature-gated
- `src/backend/serial_console.rs` — primal-agnostic test data
- `src/persistence/lifecycle.rs` — primal-agnostic docs
- `src/cloud_init.rs` — uses new DNS helpers
- `src/lab/mod.rs`, `src/topology/mod.rs`, `src/cloud_init.rs`, `src/image_builder.rs` — tests extracted
- `scripts/run-tests.sh` — real wrapper replacing stub
- `scripts/create-lab.sh` — updated next-steps text
- `examples/*.rs` — env_logger → tracing, paths → env vars
- All root docs (README, CONTEXT, CHANGELOG, wateringHole/README)

### agentReagents (25+ files)
- `configs/defaults.env` — created
- `scripts/*.sh` (9 active) — hardened headers, sourcing, credential variables
- `scripts/lint.sh`, `scripts/update-checksums.sh` — created
- `scripts/legacy/` — 9 scripts moved
- `configs/ecoprimals-node.yaml` — duplicate package, ports.env, SSH key docs
- All root docs (README, CONTEXT, SETUP, CHANGELOG, LICENSE)
- `specs/ARCHITECTURE.md`, `specs/AGENTREAGENTS_EVOLUTION.md` — updated for current state
- `docs/MANIFEST.md`, `docs/CHECKSUMS.md` — populated and restructured
- `wateringHole/README.md` — updated capabilities
- `.gitkeep` files in artifact directories
- `archive/docs/` — 4 stale docs moved
