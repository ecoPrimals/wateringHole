# petalTongue v1.6.7 — Deep Debt Audit: Zero Warnings, Zero Debt

**Date**: April 21, 2026
**From**: petalTongue team

## Audit Scope

Comprehensive deep debt pass across entire workspace (818+ .rs files, 19 crates):

| Dimension | Finding |
|-----------|---------|
| **Files >800 lines** | None (largest ~600L after prior refactoring) |
| **Unsafe code** | Zero blocks — every crate uses `#![forbid(unsafe_code)]` |
| **TODO/FIXME** | None in production code |
| **Hardcoded primal names** | None in production (1 debug log mention, acceptable) |
| **Mocks in production** | All behind `#[cfg(test)]` or `#[cfg(feature = "test-fixtures")]` |
| **ring/openssl/reqwest/native-tls** | None in dependency tree |
| **Clippy warnings** | 0 (was 3, all fixed) |
| **dyn trait objects** | 4 remaining — all idiomatic (callbacks + error trait) |

## Changes Made

### 1. Clippy Zero-Warnings

- **`socket.rs`**: Removed `needless_return` in socket audio backend
- **`factory.rs`**: Boxed `DoomPanelWrapper` enum variant (432 → 8 bytes on stack) to resolve `large_enum_variant`. Switched all 19 match arm methods from UFCS (`PanelInstance::method(p, ...)`) to method syntax (`p.method(...)`) for clean auto-deref through `Box`.
- **`chaos_tests.rs`**: Changed `async fn one_demo_provider()` (no awaits) to `fn → impl Future` to resolve `unused_async`

### 2. Dependency Trimming: futures → futures-util

Replaced full `futures` crate with lighter `futures-util` in `petal-tongue-discovery`:
- Source uses only `join_all` and `select_all` from `futures::future`
- `futures-util` provides these same re-exports at lower compile cost
- Updated 3 source files + 2 test files

### 3. dyn Assessment (No Changes Needed)

| Usage | Location | Verdict |
|-------|----------|---------|
| `Box<dyn Fn(EcosystemEvent) + Send + Sync>` | `sse.rs` | Idiomatic — open-ended event callback |
| `Box<dyn Fn(BiomeOSEvent) + Send + Sync>` | `events.rs` | Idiomatic — open-ended event callback |
| `&dyn std::error::Error` | `types.rs`, `factory.rs` | Standard Rust error trait interface |

### 4. Dependency Audit (No Action Needed)

- `symphonia` with `mp3` feature: actively used for embedded startup audio
- Duplicate `png` versions (0.17 / 0.18): caused by eframe/image upstream, not controllable
- `petal-tongue-adapters` egui dep: actively used across 6 source files

## Verification

- `cargo clippy --workspace --all-targets --all-features` — **0 warnings**
- `cargo test --workspace --all-features` — **all passing**
- `cargo check --target x86_64-apple-darwin` — **macOS clean**
