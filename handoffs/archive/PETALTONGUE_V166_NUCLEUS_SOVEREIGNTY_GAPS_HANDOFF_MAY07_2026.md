# petalTongue v1.6.6 — projectNUCLEUS Sovereignty Gaps Handoff

**Date**: May 7, 2026
**Scope**: PT-1 through PT-5 from projectNUCLEUS sovereignty testing
**Status**: PT-1, PT-3, PT-4, PT-5 RESOLVED. PT-2 documented as future roadmap.

## Context

projectNUCLEUS attempted to use petalTongue `web` mode as a sovereign static
site server (sporePrint, GitHub Pages replacement). 6 hardcoded routes worked;
arbitrary paths 404'd. Five gaps were identified.

## Resolved Gaps

### PT-1 (High): `--docroot` Static File Catch-All

**Problem**: Web router had 6 fixed routes and no fallback for arbitrary paths.

**Fix**: Added `--docroot <path>` CLI flag (+ `PETALTONGUE_DOCROOT` env var).
When set, `tower_http::ServeDir` is wired as `.fallback_service()` on the
axum router with `append_index_html_on_directories(true)`. API routes
(`/health`, `/api/*`, `/static`) take precedence over docroot files.

**Files**: `src/main.rs` (CLI), `src/web_mode.rs` (router fallback)

**Unblocks**: `zola build` → copy to docroot → petalTongue serves static site.

### PT-3 (Medium): Web Config Schema

**Problem**: `run()` only accepted `bind`/`scenario`/`workers`.

**Fix**: New `WebServeConfig` struct in `petal_tongue_core::config_system`:
- `docroot: Option<PathBuf>` — config file fallback for `--docroot`
- `backend: String` — `"filesystem"` (default) or `"nestgate"` (future PT-2)
- `index_file: String` — default `"index.html"`
- `cache_ttl_secs: u64` — default 3600

Config file `[web]` section, `PETALTONGUE_DOCROOT` env override, CLI
`--docroot` takes highest precedence.

**Files**: `crates/petal-tongue-core/src/config_system/types.rs`,
`crates/petal-tongue-core/src/config_system/loader.rs`,
`crates/petal-tongue-core/src/config_system/mod.rs`

### PT-4 (Medium): Deploy Mode Alignment (Dual-Port)

**Problem**: NUCLEUS needs both HTTP (web) and IPC (JSON-RPC UDS) in one process.

**Fix**: Added `--ipc` flag to `Commands::Web`. When set, `server_mode::run()`
is spawned as a background tokio task alongside the HTTP server. Optional
`--ipc-port` for TCP JSON-RPC alongside UDS.

**Usage**:
```bash
petaltongue web --docroot ./public --ipc                    # HTTP + UDS IPC
petaltongue web --docroot ./public --ipc --ipc-port 9900    # HTTP + UDS + TCP IPC
```

**File**: `src/main.rs` (dispatch_async)

### PT-5 (Low): `--workers` Wired to Tokio Runtime

**Problem**: `--workers` flag was parsed and logged but not applied.

**Fix**: `main()` extracts `workers` from `Commands::Web` / `Commands::Headless`
before building the tokio runtime, passes it to
`tokio::runtime::Builder::new_multi_thread().worker_threads(n)`.

**File**: `src/main.rs` (runtime builder)

## Future Roadmap

### PT-2 (High): NestGate Content Backend

Filesystem `--docroot` (PT-1) is the immediate path. Future evolution:
`web` mode queries NestGate `storage.retrieve_blob` for content-addressed
resolution when `backend = "nestgate"` is configured. The `WebServeConfig`
schema already has the `backend` field for this graduation.

## Tests

- `test_run_invalid_docroot_rejects` — non-existent docroot path rejected
- `test_docroot_fallback_serves_static_files` — tempdir files served via fallback
- `test_api_routes_take_precedence_over_docroot` — API routes shadow docroot
- `test_cli_parse_web_with_docroot` — `--docroot /path` parsed
- `test_cli_parse_web_docroot_default_none` — default is None
- All 201 tests pass (193 unit + 8 e2e).

## Verification

```bash
cargo check --all-features                          # clean
cargo clippy --all-features --workspace -D warnings  # 0 warnings
cargo fmt --check                                    # pass
cargo test --all-features                            # 201 pass
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps       # clean
```
