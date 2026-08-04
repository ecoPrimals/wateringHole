# tideGlass Remaining Issues AAR — westGate Live Validation

**Date**: Aug 4, 2026
**Gate**: westGate
**Wave**: 156d
**Primal**: tideGlass
**Repo**: `protoKarya/tideGlass`
**Status**: 177 tests, 0 clippy warnings, live NUCLEUS validated, all quality gates GREEN

---

## Resolved This Session

| Issue | Resolution |
|-------|------------|
| DIV-7: Socket paths use `membrane/` with family-ID naming | Discovery rewritten to prefix-glob scan of `membrane/` then `biomeos/`. `find_socket_by_prefix()` public API. |
| DIV-8: Neural API doesn't proxy `content.*` methods | Automatic fallback from Neural API to direct nestGate. Server detects empty response and retries on direct socket. |
| CAS client hangs on `content.list` (30 MB / 333K objects) | Switched from `read_line` to `read_to_end`. Startup probe changed from `content.list` to `health.check`. |
| Stale docs (test counts, socket paths, coverage refs) | All root docs, specs, validation/README reconciled to 177 tests and live layout. |
| Cell graph uses old deploy command | Updated to `biomeos nucleus attach --cell` (v4.57 API). |

---

## Remaining Issues — Upstream Blockers (Not tideGlass Code)

### 1. GPS Data Format (DIV-4) — westGate Data Team

**Problem**: GPS platform data (8 files, 1.4 GB) is in CAS as NumPy/pickle format.
tideGlass cannot deserialize Python-serialized data from Rust.

**Required**: Python one-shot converter: read CAS → parse NumPy → write JSON → CAS re-ingest
with `parent_hash` derivation lineage.

**Impact**: Without this, tideGlass science modules run on caller-supplied params only.
No CAS-backed batch processing. The Chen 2017 benchmark (r >= 0.52) is blocked.

**Owner**: westGate data team.

### 2. biomeOS v4.57 Not Deployed on westGate — Ops

**Problem**: westGate has biomeOS v4.56.0. The `nucleus attach` CLI shipped in v4.57.
tideGlass cell graph is ready but can't be deployed until v4.57 binary is on westGate.

**Required**: Update `/home/westgate/Development/ecoPrimals/infra/plasmidBin/primals/biomeos`
to v4.57 build.

**Impact**: tideGlass can't boot as a formal cell composition. Server works fine standalone
via `tideglass run --socket <path>`.

**Owner**: sporeGate CI / membrane ops.

### 3. Neural API `content.*` Routing (DIV-8) — biomeOS Team

**Problem**: Neural API socket (`neural-api-westgate-tower-155f.sock`) responds to
`health.check` but returns empty responses for all CAS data methods (`content.get`,
`content.exists`, `content.list`, `content.put`).

**Required**: biomeOS Neural API needs to route `content.*` methods to nestGate via
capability discovery.

**Impact**: G56 Neural API routing pattern is not functional for data access. All primals
must fall back to direct nestGate connections. This defeats the purpose of capability-based
routing.

**Owner**: biomeOS team.

### 4. No Query-by-Tag API (DIV-2) — nestGate Team

**Problem**: CAS has 333,695 objects but no way to query by metadata (source, pipeline,
content_type). Only retrieval is by exact BLAKE3 hash.

**Required**: `content.query` method with metadata filters, or a published
`data_manifest.toml` per dataset with known hashes.

**Impact**: tideGlass can't discover its datasets at runtime. Must pre-configure
hashes or receive them from callers.

**Owner**: nestGate team (Session 135 AAR mentions `content.query` as next work).

### 5. Stale CAS Clients in Other Primals (DIV-5)

**Problem**: groundSpring, airSpring, and others have stale CAS client code using
wrong method names (`content.store` instead of `content.put`, legacy `key`/`value`
params instead of CAS contract).

**Required**: Canonical Rust CAS client crate (`nestgate-client`) for ecosystem, or
audit of all primal CAS clients.

**Owner**: nestGate team / overwatch.

### 6. Large Object Streaming (DIV-6)

**Problem**: Several GPS files exceed the 64 MiB `content.get` inline limit. The
`content.retrieve_stream` protocol requires multi-call session management not yet
implemented in tideGlass.

**Required**: Streaming client implementation for large CAS objects, or pre-chunked
data in CAS.

**Impact**: Some GPS datasets can't be loaded until streaming or chunking is implemented.

**Owner**: tideGlass (code) + nestGate (protocol documentation).

---

## tideGlass Code — Complete and Deployment-Ready

| Aspect | Status |
|--------|--------|
| Rust workspace | 9 crates, 7 science modules, 2.0 MB release binary |
| Tests | 177, all green |
| Clippy | pedantic + nursery, zero warnings |
| Unsafe code | `#![forbid(unsafe_code)]` on all crates |
| Dependencies | 6 direct, 21 transitive, all pure Rust |
| CAS connectivity | Live on westGate, graceful degradation |
| Socket discovery | Handles `membrane/` layout with family-ID naming |
| Neural API fallback | Automatic when `content.*` not proxied |
| Cell graph | Ready for `biomeos nucleus attach` v4.57 |
| Health triad | Reports CAS routing, convergence, per-module readiness |
| IPC methods | 11 implemented, all responding on live NUCLEUS |
| Divergences | 8 documented (DIV-1 through DIV-8) |

---

## Recommended Overwatch Actions

1. **Priority**: Deploy biomeOS v4.57 to westGate plasmidBin (unblocks cell boot)
2. **Priority**: GPS NumPy/pickle → JSON converter + CAS re-ingest (unblocks real science)
3. **Review**: biomeOS Neural API `content.*` routing gap (DIV-8) — affects all CAS consumers
4. **Review**: Socket path documentation — `membrane/` vs `biomeos/` convention (DIV-7)
5. **Audit**: Other primals' CAS clients for stale method names (DIV-5)
6. **Track**: nestGate `content.query` progress (DIV-2, Session 135 scope)
