# petalTongue — Doc Refresh, Cross-Arch Fix, Dependency Cleanup

**Date**: April 19, 2026
**Sprint**: petalTongue v1.6.6 (continued)

---

## Cross-Arch macOS Build Fix

**Root cause**: `AudioCanvas` had duplicate `discover()` / `is_available()` methods —
one unconditional (Linux `/dev/snd`) and one in `#[cfg(target_os = "macos")]`. On macOS,
both compiled simultaneously → E0592 (conflicting implementations), cascading to E0034
at every call site.

**Fix**: Moved platform methods to mutually exclusive `#[cfg(target_os)]` blocks.
Added `cfg_attr` dead-code suppression for Linux-only `proc_stats` internals.
Gated unreachable fallback in `external.rs` display detection.

**Verified**: `cargo check` on x86_64-apple-darwin and aarch64-apple-darwin — 0 errors,
0 warnings.

## Dependency Cleanup

| Change | Impact |
|--------|--------|
| `petal-tongue-ui-core`: removed dead `petal-tongue-graph` dep | Was never imported — only in doc comments |
| `petal-tongue-headless`: `default-features = false` on graph | Headless no longer pulls egui/eframe/glow |
| tarpc: `full` → specific features | Dropped unused `serde-transport-json` |
| `petal-tongue-wasm`: removed dup `serde_json` dev-dep | Minor cleanup |

**Result**: `cargo tree -p petal-tongue-headless -i egui` → "did not match any packages"

## Deep Debt Audit

Full sweep of all 18 workspace crates — findings:

| Dimension | Status |
|-----------|--------|
| Files >800 LOC | None (largest production: 597) |
| Unsafe code | Zero (all crates `forbid(unsafe_code)`) |
| Hardcoded values | All env-overridable defaults |
| Production mocks | None (all `#[cfg(test)]` gated) |
| `dyn` usage | Idiomatic only (`Box<dyn Fn>`, `&dyn Error`) |
| TODO/FIXME/HACK | Zero |
| `async-trait` | Zero first-party (transitive only via tarpc) |
| `reqwest` / `ring` | Absent from manifests and lockfile |

## Root Doc Refresh

| File | Changes |
|------|---------|
| CONTEXT.md | Fixed truncated `#[allow]` text, updated IPC domain list, added macOS fix + dep cleanup entries, removed resolved backlog items |
| README.md | Fixed `#[allow]` claim for `cfg_attr` gates, corrected wateringHole paths to `infra/wateringHole/`, removed refs to non-existent docs |
| START_HERE.md | Updated date, added `--port` to server subcommand |
| CHANGELOG.md | Synced UUI boundary test count to 6,144 |
| ENV_VARS.md | Updated date |
| src/main.rs + gather.rs | Updated ecoBin claim to "Pure Rust" (headless now zero GUI deps) |

## Verification

- `cargo clippy --workspace --all-targets` — 0 warnings
- `cargo test --workspace --all-features` — 6,144 tests, 0 failures
- macOS cross-check (x86_64 + aarch64) — 0 errors, 0 warnings

## Commits

- `9a6e2a6` fix: cross-arch macOS build
- `ae1fee7` evolve: dependency cleanup
- `34c114e` docs: root doc refresh
