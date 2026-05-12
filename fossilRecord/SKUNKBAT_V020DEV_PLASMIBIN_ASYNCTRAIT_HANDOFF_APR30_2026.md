<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# skunkBat v0.2.0-dev — plasmidBin Publishing + async-trait Elimination

**From**: skunkBat team
**Date**: April 30, 2026
**Triggered by**: primalSpring v0.9.24 plasmidBin CI/CD audit

---

## Summary

Resolves the final blocker preventing skunkBat from being included in the
standard `fetch_primals.sh` download. Also completes the ecosystem-wide
`async-trait` elimination (14→0) that was tracked in PRIMAL_GAPS.md.

## Changes

### 1. plasmidBin Publishing Pipeline

**Problem**: skunkBat was the only primal (13th of 13) not published to
plasmidBin GitHub Releases. `fetch_primals.sh` failed for skunkBat.
`manifest.toml` and `checksums.toml` incorrectly described skunkBat as
"library-only crate, no binary target produced".

**Resolution**:

| Component | Change |
|-----------|--------|
| `manifest.toml` | Updated: added `binary`, `build_package`, `needs_sibling`, `arch` fields; removed "library-only" comment; updated capabilities and description |
| `checksums.toml` | Updated: replaced "library-only" comment with "populated by harvest.sh" |
| `sources.toml` | Already correct (`needs_sibling = "ecoPrimals/sourDough"`, `private = true`) |
| `build-primal.sh` | Already supports `needs_sibling` — clones sourDough as sibling at `$BUILD_ROOT/sourDough` |

**Verified locally**:
- `cargo build --release --target x86_64-unknown-linux-musl -p skunk-bat-server` produces
  a 2.4 MB static-pie ELF binary (`skunkbat`)
- Binary runs correctly from plasmidBin primals dir (`--version`, `health`, `server`)
- Relative path `../sourDough/crates/sourdough-core` resolves correctly in CI sibling layout

### 2. CI Release Workflow

**Problem**: `.github/workflows/ci.yml` did not clone sourDough sibling,
and had no release job for tag pushes.

**Resolution**:
- Added `actions/checkout@v4` for sourDough sibling in `check`, `coverage`,
  and new `release` jobs (uses `SOURDOUGH_PAT` secret for private repo access)
- Added `release` job: triggered on `v*` tags, runs after check/deny/coverage,
  builds musl-static binaries for x86_64 + aarch64, uploads to GitHub Release
- Added `tags: ['v*']` to push trigger

### 3. async-trait Elimination (14→0)

**Problem**: skunkBat had 14 `#[async_trait]` usages across trait definitions
and implementations, requiring the `async-trait` proc macro crate and
`Box<dyn Trait>` dispatch.

**Resolution**:
- All 14 usages replaced with native RPITIT (`impl Future<...> + Send`)
- `Box<dyn PrimalDiscovery>` → generic `D: PrimalDiscovery` (monomorphized)
- `Box<dyn LineageVerifier>` → generic `L: LineageVerifier`
- `Box<dyn BaselineProfiler>` → generic `B: BaselineProfiler`
- `async-trait` crate removed from all Cargo.toml files
- `async-trait` banned in `deny.toml` (wrapped for transitive via opentelemetry_sdk)

**Impact**: Zero-cost trait dispatch, reduced compile surface (`syn v1`
dependency path shortened), matches ecosystem stadial gate (13/13 primals
at zero).

### 4. deny.toml Cleanup

- Banned `async-trait` (wrapped: `opentelemetry_sdk` transitive only)
- Removed stale `iana-time-zone-haiku` wrapper from `cc` ban

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| async-trait usages | 14 | **0** |
| Tests | 171 | 171 |
| Line coverage | 89.5% | **89.5%** |
| Largest file | 867 L | 867 L |
| Binary size (x86_64-musl) | N/A | **2.4 MB** (static-pie, stripped) |
| plasmidBin status | NOT PUBLISHED | **READY** (awaiting first `v0.2.0` tag) |

## Remaining (LOW priority)

1. **First release tag**: Push `v0.2.0` tag to trigger CI release pipeline
   and plasmidBin harvest
2. **`PeekedStream`/`PrefixedStream` convergence**: Consolidate with BearDog's
   impl into shared `sourdough-core` utility
3. **Thymic selection implementation**: Blocked on BearDog `lineage.list` IPC
4. **Composable primitives IPC registration**: Blocked on biomeOS Neural API

## Files Changed

### skunkBat repo
- `Cargo.toml` — removed `async-trait` workspace dep
- `crates/skunk-bat-core/Cargo.toml` — removed `async-trait` dep
- `crates/skunk-bat-integrations/Cargo.toml` — removed `async-trait` dep
- `crates/skunk-bat-core/src/reconnaissance/{traits,mod,discovery}.rs` — RPITIT + generics
- `crates/skunk-bat-core/src/threats/{traits,mod,genetic,behavioral}.rs` — RPITIT + generics
- `crates/skunk-bat-core/src/universal_adapter.rs` — RPITIT
- `crates/skunk-bat-integrations/src/{songbird,toadstool}.rs` — removed `#[async_trait]`
- `.github/workflows/ci.yml` — sourDough sibling checkout + release job
- `deny.toml` — `async-trait` banned, `cc` wrapper cleanup
- `CONTEXT.md` — updated dependency description
- `showcase/99-gaps-analysis/README.md` — added plasmidBin section, async-trait status

### plasmidBin repo
- `manifest.toml` — skunkBat entry updated (binary, arch, capabilities)
- `checksums.toml` — skunkBat placeholder updated

---

*Next handoff: after first `v0.2.0` tag + successful plasmidBin harvest.*
