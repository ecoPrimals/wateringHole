<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# skunkBat v0.2.0-dev — Deep Debt + plasmidBin Publishing

**From**: skunkBat team
**Date**: April 30, 2026
**Triggered by**: primalSpring v0.9.24 plasmidBin CI/CD audit + deep debt pass

---

## Summary

Two passes on skunkBat this session:

1. **plasmidBin publishing**: Resolved the sole remaining blocker preventing
   skunkBat from being included in `fetch_primals.sh` (13th of 13 primals).
   Updated infra metadata, added CI release pipeline, verified musl-static build.

2. **Deep debt + evolution**: Comprehensive refactoring, hardcoding cleanup,
   idiomatic Rust evolution, coverage expansion, and dependency hygiene.

## plasmidBin Publishing

**Problem**: skunkBat not yet in plasmidBin GitHub Releases. `manifest.toml`
and `checksums.toml` incorrectly listed skunkBat as "library-only".

**Resolution**:
- Updated `manifest.toml`: binary, build_package, needs_sibling, arch fields
- Updated `checksums.toml`: placeholder for harvest pipeline
- Added CI release job (`.github/workflows/ci.yml`): musl-static x86_64 + aarch64 on tag push
- Verified: 2.4 MB static-pie ELF binary builds and runs from plasmidBin dir
- `sources.toml` + `build-primal.sh` already correct

**Status**: READY — awaiting first `v0.2.0` tag to trigger pipeline.

## async-trait Elimination (14 → 0)

- All `#[async_trait]` replaced with native RPITIT + monomorphized generics
- `async-trait` crate removed from workspace, banned in `deny.toml`
- Matches ecosystem stadial gate (13/13 primals at zero)

## Deep Debt Refactoring

### Smart file refactoring (btsp.rs 867 → 623 lines)
- Extracted `config.rs` (194L): BTSP Phase 1/2 environment configuration
- Extracted `sys.rs` (47L): platform UID helpers without libc
- Protocol logic (framing, provider client, handshake) stays cohesive in `btsp.rs`
- No files over 623 lines (limit: 1000)

### Hardcoding → agnostic
- `health_check()` wired through `config.common.name` instead of literal
- `LocalDiscovery` uses `PRIMAL_NAME`/`CAPABILITIES` named constants
- `JSONRPC_VERSION` const eliminates per-response allocation
- `dispatch.rs` replaces `format!` with `to_string()` on hot paths

### Bug fix
- `rpc.rs`: now strips both `http://` and `https://` prefixes from TCP endpoints

### Dependency cleanup
- Removed duplicate `tokio` dev-dependency from workspace `Cargo.toml`
- `cargo deny` fully clean (advisories, bans, licenses, sources)

### Doc cleanup
- Fixed broken `ECOSYSTEM_ARCHITECTURE.md` reference in threat detection spec
- Fixed stale `whitePaper/` paths in `RECONNAISSANCE_NOT_SURVEILLANCE.md`
- Updated BTSP Phase 1→1/2 wording in showcase START_HERE
- Aligned largest-file metric across README, CONTEXT, gaps analysis

## Metrics

| Metric | Before Session | After |
|--------|---------------|-------|
| Tests | 171 | **178** |
| Line coverage | 89.5% | **90.0%** |
| Largest file | 867 L | **623 L** |
| Source files | 28 | **30** |
| Total lines | 7,288 | **6,749** |
| async-trait usages | 14 | **0** (banned) |
| Binary (x86_64-musl) | N/A | **2.4 MB** static-pie |
| plasmidBin | NOT PUBLISHED | **READY** |

## CI Status

- `cargo fmt --check` — CLEAN
- `cargo clippy --all-targets -- -D warnings` — CLEAN
- `cargo test --workspace` — 178 passed, 15 ignored
- `cargo deny check` — all ok
- `cargo doc --no-deps` — CLEAN
- `cargo llvm-cov --fail-under-lines 85` — 90.0% (passes 85% gate)

## Remaining (LOW priority, design-phase)

1. **First release tag**: Push `v0.2.0` tag to trigger CI release + plasmidBin harvest
2. **`PeekedStream`/`PrefixedStream` convergence**: Consolidate with BearDog impl into `sourdough-core`
3. **Thymic selection implementation**: Design spec complete; implementation awaits BearDog capability discovery via `rpc.methods` + `capabilities.list`
4. **Composable primitives IPC registration**: Blocked on biomeOS Neural API

---

*Next handoff: after `v0.2.0` tag + plasmidBin harvest, or next evolution cycle.*
