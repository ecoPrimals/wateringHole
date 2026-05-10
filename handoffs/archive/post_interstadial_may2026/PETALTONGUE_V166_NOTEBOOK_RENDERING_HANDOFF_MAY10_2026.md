# petalTongue v1.6.6 — Notebook Rendering + PT-3 Completion

**Date:** May 10, 2026
**Scope:** Jupyter `.ipynb` → HTML rendering, `WebServeConfig` completion, `Cache-Control` wiring
**Status:** RESOLVED

---

## Problems

1. **No notebook rendering**: `.ipynb` files served from docroot or NestGate were
   delivered as raw JSON, not rendered HTML. projectNUCLEUS sovereignty Step 3a
   required notebook pages with human-readable titles.

2. **`metadata.title` not used**: Jupyter notebooks include a `metadata.title`
   field that should populate page headers. No rendering pipeline existed.

3. **No `strip_sources` config**: Presentation/documentation use cases need to
   hide code input cells and show only outputs.

4. **PT-3 incomplete**: `WebServeConfig.cache_ttl_secs` and `index_file` fields
   existed in schema but were not wired to runtime behavior.

5. **PT-5 stale comment**: `WebConfig.workers` doc said "currently logged only"
   despite being wired to the tokio runtime in `main.rs`.

## Fixes

### New: `src/notebook_render.rs` (553 LOC)

- Parses nbformat v4 JSON via `serde_json`
- Renders markdown cells via `pulldown-cmark` (CommonMark + tables, strikethrough,
  task lists, footnotes)
- Code cells as `<pre><code class="language-{lang}">` with kernel language detection
- Rich outputs: HTML passthrough (priority), SVG, base64 PNG/JPEG, plain text
- Error outputs with distinct styling
- `metadata.title` → `<title>` + `<h1>` header; fallback "Notebook"
- Responsive CSS with dark-mode (`prefers-color-scheme`) support
- XSS protection: all user content HTML-escaped
- 14 unit tests

### New: `--strip-sources` / `PETALTONGUE_STRIP_SOURCES`

- CLI flag + env var + `WebServeConfig.strip_sources` TOML field
- When enabled, `render_code_source()` is skipped; only outputs rendered

### New: `--cache-ttl` / `PETALTONGUE_CACHE_TTL`

- CLI flag + env var + `WebServeConfig.cache_ttl_secs` TOML field
- Sets `Cache-Control: public, max-age={n}` on all served static content
- 0 = no header (default for development)

### Changed: `web_mode.rs`

- `docroot_fallback()` replaces raw `ServeDir` fallback:
  - `.ipynb` requests: read file → render → serve as `text/html`
  - All other requests: delegate to `ServeDir` + inject `Cache-Control`
- `nestgate_fallback()` now renders `.ipynb` content from NestGate as HTML
- `web_mode::run()` takes `WebConfig` struct (was 8 positional params)
- `is_ipynb()` helper for case-insensitive extension check
- 4 new integration tests (docroot notebook, cache-control, is_ipynb, path resolve)

### Changed: Config system

- `WebServeConfig.strip_sources: bool` field (default `false`)
- `PETALTONGUE_CACHE_TTL` and `PETALTONGUE_STRIP_SOURCES` env overrides in loader

### Dependency

- `pulldown-cmark 0.13` (pure Rust, `html` feature only) — workspace dep

## Verification

```
cargo fmt --check     ✅ clean
cargo clippy -D warn  ✅ 0 warnings
cargo test --all      ✅ 213+ tests pass (14 new notebook + 4 new web integration)
```

## Files Changed

| File | Change |
|------|--------|
| `src/notebook_render.rs` | NEW — notebook renderer (553 LOC) |
| `src/web_mode.rs` | `docroot_fallback`, notebook integration, `WebConfig` struct |
| `src/main.rs` | `--strip-sources`, `--cache-ttl` CLI flags, `WebConfig` usage |
| `crates/petal-tongue-core/src/config_system/types.rs` | `strip_sources` field |
| `crates/petal-tongue-core/src/config_system/loader.rs` | Env overrides |
| `Cargo.toml` | `pulldown-cmark` dependency |
| `CHANGELOG.md` | Entry |
| `CONTEXT.md` | Updated |
| `START_HERE.md` | New CLI examples + env vars |
