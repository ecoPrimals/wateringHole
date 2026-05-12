# Songbird v0.2.1 — Wave 122: Doc Cleanup, Debris Removal, Legacy Name Scrub

**Date**: April 7, 2026
**Primal**: songBird
**Previous**: Wave 121 (archived)

---

## Summary

Wave 122 focused on documentation accuracy, debris removal, and scrubbing legacy primal names from non-Rust assets (deployment graphs, example configs, scripts). All root docs updated to reflect current metrics and dates. Stale binary artifact (`vis_test`) removed from git. Legacy `beardog`/`toadstool`/`squirrel`/`nestgate` references in deployment configs and example files evolved to capability-based naming.

## Root Docs Updated

- **README.md**: Date references updated to Apr 7; total Rust lines updated to ~427,000 / 1,578 files
- **CONTRIBUTING.md**: File limit corrected from 1000→800 lines; coverage updated to 72.29%
- **CONTEXT.md**: Last Updated date to April 7
- **REMAINING_WORK.md**: Date to April 7; Last Deep Debt Audit expanded to cover Waves 119-121; stale coverage note replaced; `tower_atomic.rs` coverage entry updated to reflect module split; all `Apr 6` references updated

## Debris Removed

- **`vis_test`**: 6MB compiled ELF binary at repo root, tracked in git, zero references — deleted via `git rm`
- **Doc claims verified**: Zero `TODO`/`FIXME`/`HACK` in Rust source confirmed; zero production `.unwrap()`/`panic!()` confirmed (all in `#[cfg(test)]`)

## Legacy Name Scrub (Non-Rust Assets)

### Scripts
- `scripts/test-with-security-provider.sh`: Binary discovery now tries `security-provider` first, falls back to `beardog` with warning
- `scripts/health-monitor.sh`: "BTSP provider(s)" → "security provider(s)"
- `deployment/usb-live-spore/launch-songbird.sh`: Auto-discover `security-provider` binary first, `beardog` as warned fallback

### Deployment Graphs
- `deployment/graphs/tower_genome.toml`: All human-readable descriptions and comments evolved to "security provider" language (actual binary/genome references preserved since they reference real artifacts)

### Example Configs
- `examples/config/songbird-ecosystem.toml`: `well_known` section keys changed from primal names to capability identifiers (`compute-provider`, `storage-provider`, `ai-provider`, `security-provider`); routing preferences updated; integration sections renamed
- `examples/config/songbird-universal-primal-discovery.toml`: Environment variable examples updated from `BEARDOG_ENDPOINT` to `SECURITY_PROVIDER_SOCKET`
- `examples/custom_primal_integration.yaml`: Primal keys changed from `beardog`→`security-provider`, `squirrel`→`ai-provider`, `nestgate`→`storage-provider`, `toadstool`→`compute-provider`, `forked-toadstool`→`forked-compute-provider`
- `examples/universal-config-example.yml`: "replaces BearDog" → "crypto.delegate capability"
- `examples/README.md`: "BearDog delegation" → "security provider delegation"
- `examples/clients/README.md`: "on Toadstool" → "on compute provider"
- `examples/provider-configs/README.md`: "ToadStool local GPU provider" → "Local GPU compute provider"

## What Remains Unchanged (By Design)

- `deployment/graphs/tower_genome.toml` still references `beardog.genome`, `primal = "beardog"` in graph nodes — these are actual binary/genome artifact names that can't change until the binary is renamed upstream
- `scripts/test-with-security-provider.sh` still exports `BEARDOG_BIN`/`BEARDOG_SOCKET` for backward compatibility

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 12,811 passed, 0 failed, 252 ignored |
| Line coverage | 72.29% |
| Files >800L | 0 (largest 519L) |
| Total Rust | ~427,000 lines / 1,578 files / 30 crates |
| Legacy primal names in scripts/configs | All evolved to capability-first with deprecated fallbacks |
| Stale artifacts removed | 1 (vis_test, 6MB binary) |

## Verification

- `cargo check --workspace` — clean (zero errors, zero warnings)
- `cargo test --workspace` — 12,811 passed, 0 failed
- All doc claims verified accurate (zero TODO/FIXME/HACK, zero production unwrap/panic)
