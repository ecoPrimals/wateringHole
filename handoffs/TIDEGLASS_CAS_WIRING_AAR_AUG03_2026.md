# tideGlass CAS Wiring AAR — First Primal Live Data Integration

**Date**: Aug 3, 2026
**Gate**: westGate
**Wave**: 156b
**Primal**: tideGlass
**Context**: First primal to wire live nestGate CAS data. Divergences documented for upstream teams.

---

## Summary

Wired tideGlass UniBin to discover and connect to nestGate CAS on startup.
Dispatch handlers now fall through from CAS-loaded data to caller-supplied params
gracefully. Health triad reports CAS connection status and loaded dataset counts.

**161 tests passing. Clippy pedantic+nursery clean. All quality gates green.**

---

## Divergences Found

### DIV-1: DATA_ACCESS.md uses wrong hash format

**tideGlass spec** (`specs/DATA_ACCESS.md`):
```json
{"hash": "blake3:abc123...", "format": "gctx"}
```

**Actual nestGate NG-1 contract**:
```json
{"hash": "a1b2c3d4e5f6..."}  // 64-char lowercase hex, no prefix, no format param
```

**Impact**: Any primal implementing from DATA_ACCESS.md would construct invalid requests.
**Fix**: Updated tideGlass CAS client to use plain 64-char hex. DATA_ACCESS.md update needed.
**Upstream**: All DATA_ACCESS.md templates across primals likely have this issue.

### DIV-2: No query-by-tag API in nestGate

**Problem**: GPS platform data (8 files, 1.4 GB) is CAS-indexed with provenance
metadata (source, pipeline), but there's no `content.query_by_tag` or
`content.search` method. The only retrieval mechanism is by exact BLAKE3 hash.

**Impact**: tideGlass can't discover its data at runtime without pre-configured hashes.
`content.list` returns 67,680+ objects — iterating and filtering by metadata would
require fetching each object's `.meta.json` sidecar, which is O(n) network calls.

**Options** (for upstream nestGate team):
1. Add `content.query` method accepting `{source: "...", pipeline: "..."}` filters
2. Add `content.list` metadata filtering: `{family_id: "...", source: "tideglass"}`
3. Publish a `data_manifest.toml` per dataset with known CAS hashes after ingest

**Recommended**: Option 3 is cheapest (no nestGate changes). Option 1 is best long-term.
tideGlass currently uses `resolve_dataset_hash()` which returns `None` — dispatch
falls through to caller-supplied params until hashes are configured.

### DIV-3: DATA_ACCESS.md references nonexistent streaming method

**tideGlass spec**:
```
nestGate.storage.retrieve(key) → stream chunks → process
```

**Actual nestGate**:
- Inline: `content.get` (up to 64 MiB)
- Streaming: `content.retrieve_stream` / `content.retrieve_stream_chunk`
- Method `nestGate.storage.retrieve` does not exist

**Impact**: Any primal implementing streaming from DATA_ACCESS.md would get method-not-found.
**Fix**: tideGlass CAS client handles streaming redirect (`use_streaming: true` response).
Error returned until streaming client is implemented.

### DIV-4: GPS platform data format is NumPy/pickle

**Problem**: The 8 GPS platform CAS objects contain Python-serialized data (NumPy arrays,
pickle files inside zip archives: `RCL.zip`, `GPS4Drugs.zip`, `MolSearch.zip`, etc.).
There is no pure Rust parser for NumPy `.npy` or Python pickle format.

**Impact**: tideGlass cannot directly deserialize GPS platform data from CAS. A conversion
step is needed: Python script reads the CAS objects, converts to JSON/CSV, and re-ingests
into CAS in a Rust-parseable format.

**Options**:
1. Python one-shot converter: read CAS → parse NumPy → write JSON → re-ingest to CAS
2. Add `npy` crate (pure Rust NumPy reader) — handles `.npy` but not pickle
3. Store pre-converted JSON alongside original CAS objects with derivation lineage

**Recommended**: Option 3. The converter can stamp `parent_hash` and `derivation_depth`
to maintain provenance from the original Zenodo archives to the JSON representation.

### DIV-5: Other primals have stale CAS client code

Found during contract research:
- `groundSpring/.../nestgate.rs` uses legacy `key`/`value` params (not the CAS contract)
- `airSpring/.../nestgate_data.rs` calls `content.store` (method is `content.put`)
- `content_pipeline_smoke.toml` comment says `content.list` returns `{items: [...]}` —
  actual field is `hashes`

**Impact**: These primals will fail when they attempt CAS integration.
**Upstream**: nestGate team should publish a canonical Rust client crate (`nestgate-client`)
that all primals can depend on, rather than each primal reimplementing the contract.

### DIV-6: `content.get` inline limit is 64 MiB but GPS files are larger

Several GPS platform files exceed 64 MiB (MolSearch.zip is ~518 MB). `content.get`
returns a streaming redirect for these. tideGlass's CAS client detects this and
returns an error — streaming not yet implemented.

**Impact**: Large CAS objects cannot be loaded at startup until streaming is wired.
**Fix**: Implement `content.retrieve_stream` + `content.retrieve_stream_chunk` protocol.
This is non-trivial (requires maintaining a streaming session across multiple RPC calls).

---

## Architecture Decisions

### CAS types in tideglass-core, async client in tideglass-bin

CAS request/response types (`CasGetResponse`, `CasPutResponse`, etc.) live in
`tideglass-core/src/cas.rs` as sync, serializable structs. The async UDS client
lives in `tideglass-bin/src/cas_client.rs`. This keeps tideglass-core free of
tokio dependency while allowing other crates to use the types.

### Graceful degradation, not hard dependency

The server starts with or without CAS:
1. Discovers nestGate socket via env var / XDG / membrane paths
2. If found: connects, calls `content.list`, attempts data loading
3. If not found: starts with empty `ModuleData`, all modules accept caller params
4. Dispatch handlers check CAS-loaded data first, fall through to caller params

This means tideGlass works in development (no nestGate) and production (with nestGate)
without configuration changes.

### Health triad reports CAS status

`health.check` now includes a `cas` section:
```json
{
  "cas": {
    "connected": true,
    "datasets_loaded": 3,
    "load_errors": 0
  }
}
```

biomeOS orchestration can use this to verify CAS readiness before routing science work.

---

## Files Changed

- `crates/tideglass-core/src/cas.rs` — CAS types, socket discovery (new)
- `crates/tideglass-core/src/lib.rs` — export cas module
- `crates/tideglass-bin/src/cas_client.rs` — async CAS client (new)
- `crates/tideglass-bin/src/data.rs` — CAS data loading, ModuleData (new)
- `crates/tideglass-bin/src/dispatch.rs` — handlers accept ModuleData, CAS fallthrough
- `crates/tideglass-bin/src/server.rs` — thread Arc<ModuleData> to connections
- `crates/tideglass-bin/src/health.rs` — CAS-aware health triad
- `crates/tideglass-bin/src/main.rs` — CAS init on startup
- `crates/tideglass-bin/Cargo.toml` — add base64 dep
- `Cargo.toml` — add base64 workspace dep

## Upstream Review Requests

1. **nestGate team**: Publish canonical CAS client crate or review tideGlass's implementation
2. **nestGate team**: Consider `content.query` method for metadata-based lookups (DIV-2)
3. **westGate data team**: Publish GPS platform CAS hash manifest for tideGlass
4. **westGate data team**: Convert GPS NumPy/pickle to JSON and re-ingest with lineage (DIV-4)
5. **overwatch**: Audit DATA_ACCESS.md templates across all primals for DIV-1/DIV-3
6. **overwatch**: Flag stale CAS clients in groundSpring, airSpring (DIV-5)
