# petalTongue v1.6.6 — Doc Refresh & Debris Clean

**Date**: April 15, 2026
**Commits**: `fb23e49` (clippy zero), `28c51dd` (doc refresh) on `main`
**Author**: westgate

---

## Summary

Root documentation audit and refresh. Stale test counts, misleading CLI
descriptions, and obsolete feature tier strings corrected. Dead web/static
mount fixed. Build artifacts cleaned (49.1 GiB). All claims verified
against current code.

## Doc Fixes

| File | Fix |
|------|-----|
| README.md | Test count 6,140→6,144+; headless desc "Batch rendering"→"API server"; `forbid(unsafe_code)` contributing rule: "unless unavoidable"→"unconditional" |
| CONTEXT.md | Test count 6,140→6,144; IPC method count 41→43; domain list corrected (added `ui.*`, `motor.*`, `audio.*`, `lifecycle.*`; removed stale `sensor.*`); `async-trait` claim refined to "first-party only"; `#[allow]` claim adds `#[expect]` clarification |
| START_HERE.md | Headless CLI corrected (no `--mode`/`-o` on UniBin; CLI export via `petal-tongue-headless` crate); test count updated; `forbid(unsafe_code)` unconditional; display backend desc: tarpc→JSON-RPC primary |
| display_demo.rs | Feature tier strings updated to match actual `DisplayBackendImpl` variants (removed "Compute WASM", "Toadstool WASM"; added "Discovered Display") |
| web/index.html | "ecoBud"→"Universal User Interface"; "ecoBin 80%"→"Pure Rust 100%" |
| web/static/.gitkeep | Added missing directory for `ServeDir` mount |
| sandbox/scenarios/README.md | Date updated to April 15 |

## Code Fixes

| File | Fix |
|------|-----|
| `src/cli_mode/gather.rs` | `#[allow(clippy::unused_async)]`→removed; `async fn`→`fn` (function contains no awaits); zero `#[allow]` in production maintained |
| `src/cli_mode/tests.rs` | `#[tokio::test] async fn`→`#[test] fn` for sync gather test |

## Debris Cleaned

- **49.1 GiB** build artifacts cleaned (`cargo clean`)
- `sandbox/mock-biomeos/target/` verified clean

## Audit Results (No Action Required)

- `sandbox/` docs (README, BENCHTOP_ARCHITECTURE) — aspirational design vision, kept as-is
- `showcase/QUICK_START.sh` — omits some demos listed in README (known gap, not breaking)
- `graphs/petaltongue_deploy.toml` — still wired into deployment metadata
- `.github/workflows/ci.yml` — current with workspace structure
- All 7 `examples/*.rs` — compile against current API (verified)
- `sandbox/mock-biomeos/` — needed for showcase/dev mode

## Test Results

- `cargo test --workspace` — **6,008 tests**, 0 failures (default features)
- `cargo test --workspace --all-features` — **6,144 tests**, 0 failures
- `cargo clippy --workspace --all-targets` — **0 warnings**
