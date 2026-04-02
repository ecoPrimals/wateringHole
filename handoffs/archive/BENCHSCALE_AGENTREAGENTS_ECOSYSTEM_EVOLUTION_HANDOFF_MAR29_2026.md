# benchScale + agentReagents — Ecosystem-Wide Evolution Handoff

**Date**: March 29, 2026
**From**: hotSpring (GPU sovereign compute / infra evolution)
**To**: All primal teams + infra maintainers
**Scope**: Final evolution of benchScale and agentReagents to ecoPrimals standards — JSON-RPC servers, gate templates, plasmidBin integration, cross-arch support, IPC compliance validation.

---

## Summary

Both projects were originally built under syntheticChemistry for ionChannel A/B testing. This evolution round upgraded them to full ecoPrimals standards with JSON-RPC 2.0 server modes, gate provisioning templates, cross-architecture binary resolution, and IPC compliance validation tooling. Both now compile clean under Rust 2024 edition with pedantic + nursery clippy lints and zero warnings.

## Changes Completed

### Both Projects

- **Rust 2024 edition** with `deny(clippy::unwrap_used)`, `clippy::pedantic`, `clippy::nursery`
- **Zero TODO/FIXME/HACK** in active source
- **Missing docs filled** across all public items
- **JSON-RPC 2.0 server mode** per UniBin standard: `<binary> server --port PORT`
- All `health.liveness`, `health.readiness`, `health.check` methods implemented
- Git remotes remain at `syntheticChemistry` org pending GitHub transfer

### benchScale Specific (232 tests)

| New Module | Purpose |
|------------|---------|
| `src/server/` | JSON-RPC 2.0 TCP server with lab management methods |
| `src/deploy/arch.rs` | Cross-architecture binary resolution (x86_64, aarch64) |
| `src/deploy/plasmid.rs` | plasmidBin binary deployment to lab nodes |
| `src/validation/ipc_compliance.rs` | JSON-RPC compliance testing against any endpoint |

New CLI subcommands:
- `benchscale server --port PORT [--listen ADDR] [--standalone]`
- `benchscale validate ipc ENDPOINT`

Network simulation presets wired from wateringHole standards:
- `basement_lan`, `campus`, `broadband`, `cellular`, `satellite`

Docker backend: auto-install of `iproute2` (`tc`) when network simulation is needed.

### agentReagents Specific (39 tests)

| New Module | Purpose |
|------------|---------|
| `src/server/mod.rs` | JSON-RPC 2.0 TCP server with template/registry methods |

New CLI subcommands:
- `agent-reagents server --port PORT [--listen ADDR] [--standalone]`

New gate provisioning templates:
- `templates/gates/gate-ubuntu24-biomeos.yaml` — Standard biomeOS gate
- `templates/gates/gate-ubuntu24-gpu-sovereign.yaml` — VFIO GPU passthrough
- `templates/gates/gate-aarch64-pixelgate.yaml` — ARM64 mobile gate

ImageBuilder now supports `with_plasmid_bin(path)` for baking primal binaries into VM images.

## What This Enables

1. **Programmatic lab control**: Any primal can spin up test labs via JSON-RPC without CLI wrappers
2. **IPC compliance validation**: `benchscale validate ipc` tests any primal's JSON-RPC surface
3. **Gate provisioning**: agentReagents can build VM images for Eastgate, biomeGate, pixelGate deployment targets
4. **Cross-arch deployment**: plasmidBin binaries resolve correctly for x86_64 and aarch64
5. **Network simulation**: Labs can simulate real network conditions for chaos testing

## Known Remaining Debt

| Item | Impact | Owner |
|------|--------|-------|
| syntheticChemistry-era shell scripts in benchScale root | Cosmetic, archived | infra team |
| legacy scripts in agentReagents `scripts/legacy/` | Cosmetic, archived | infra team |
| committed `.deb` packages in agentReagents | Repo bloat, needs BFG before public | infra team |
| libvirt backend tests require real libvirt | CI needs Docker-only mode | infra team |
| ionChannel-era templates still present | Fossil record, archived | infra team |

## Integration Points for Teams

| Team | How to Use |
|------|------------|
| **primalSpring** | Use `benchscale validate ipc` in `validate_local_lab.sh` pipeline |
| **biomeOS** | `gate-ubuntu24-biomeos.yaml` template for standardized gate images |
| **hotSpring** | `gate-ubuntu24-gpu-sovereign.yaml` for VFIO isolation testing |
| **Pixel team** | `gate-aarch64-pixelgate.yaml` for ARM64 validation |
| **All primals** | `benchscale server --port 9200` for programmatic lab access |

## Git Locations

- `ecoPrimals/infra/benchScale/` — origin: `git@github.com:syntheticChemistry/benchScale.git`
- `ecoPrimals/infra/agentReagents/` — origin: `git@github.com:syntheticChemistry/agentReagents.git`
