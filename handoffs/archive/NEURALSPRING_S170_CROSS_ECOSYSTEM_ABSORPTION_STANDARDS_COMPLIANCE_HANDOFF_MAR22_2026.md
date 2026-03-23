# neuralSpring S170 — Cross-Ecosystem Absorption & Standards Compliance Handoff

**Date:** March 22, 2026
**From:** neuralSpring S169–S170 (deep debt + cross-spring absorption)
**To:** barraCuda, toadStool, biomeOS, All Springs
**License:** AGPL-3.0-or-later
**Covers:** S169 deep debt (zero clippy, full public surface) + S170 cross-ecosystem absorption (standards compliance, barraCuda v0.3.7 compat, 5-tier discovery)

---

## Executive Summary

- **S169**: Eliminated all 626 `missing_docs` warnings → 0, documented every public item across 40+ files. Created `CONTEXT.md`, full AGPL-3.0 LICENSE (661-line canonical), GitHub description + 14 topics + "Part of ecoPrimals" README footer. Named constants, graceful shutdown, TCP fallback, zero-copy streaming, provenance/discover/offload handlers, UniBin binary rename.
- **S170**: Cross-ecosystem absorption sprint — barraCuda v0.3.7 compatibility (Precision::F16, wgpu_device removal, GpuDriverProfile deprecation), Semantic Method Naming v2.1 compliance (`capabilities.list` canonical + aliases), biomeOS 5-tier discovery with `socket-registry.json`, `publish = false` on all workspace crates, 4-format capability response parsing.
- All gates green: 0 clippy (pedantic+nursery, `-D warnings`), 0 fmt diff, 0 doc warnings, 1,183 lib + 9 forge + 13 doc tests passing.

---

## Part 1: What Changed (S169)

### 1a. Public Surface (GitHub + repo)

| Item | Before | After |
|------|--------|-------|
| GitHub description | Empty | "Pure Rust spectral analysis, ML validation & protein folding spring — 1,205 tests, GPU via barraCuda. AGPL-3.0" |
| GitHub topics | None | 14 topics: `agpl-3-0`, `anderson-localization`, `ecoprimals`, `gpu-computing`, `json-rpc`, `machine-learning`, `paper-reproduction`, `protein-folding`, `pure-rust`, `rust`, `scientific-computing`, `sovereign-computing`, `spectral-analysis`, `wgsl` |
| LICENSE | 17-line notice (not detected) | Full 661-line AGPL-3.0 (detected as `agpl-3.0` by GitHub) |
| README footer | Missing | "Part of ecoPrimals" block matching wetSpring/healthSpring |
| `CONTEXT.md` | Missing | Created per `PUBLIC_SURFACE_STANDARD.md` |

### 1b. Code Quality — Zero Warnings

| Metric | Before | After |
|--------|--------|-------|
| `missing_docs` | 626 | 0 |
| `doc_markdown` | 3 | 0 |
| clippy (pedantic+nursery) | 0 | 0 |
| Unnecessary `.clone()` | 2 (spectral.rs) | 0 (move instead) |

### 1c. Architecture Evolution (S169)

- **Graceful shutdown**: `tokio::sync::watch` channel replaces `std::process::exit(0)` in signal handlers
- **TCP fallback**: `PRIMAL_TCP_PORT` / `NEURALSPRING_TCP_PORT` env-driven, loopback-only, for ecoBin v2.0
- **Named constants**: `DEFAULT_IPC_TIMEOUT_SECS`, `DEFAULT_HEARTBEAT_SECS`, `DEFAULT_MAX_CONCURRENT`
- **HuggingFace URLs**: Configurable via `HF_API_BASE` / `HF_DOWNLOAD_BASE` env vars
- **Provenance handlers**: `provenance.begin/record/complete/status` + `primal.discover` + `compute.offload` wired
- **Zero-copy streaming**: In-place trimming, `std::mem::take` for buffer reuse in FASTA/FASTQ/VCF
- **Binary rename**: `neuralspring_primal` → `neuralspring` (UniBin compliance)

---

## Part 2: What Changed (S170)

### 2a. barraCuda v0.3.7 Compatibility

| Change | Fix |
|--------|-----|
| `Precision::F16` added | Handled in `compile_shader_universal` — routes to f32 path (pending native f16 shader support) |
| `MultiHeadEsn::wgpu_device()` removed | Stored `Arc<WgpuDevice>` separately in `MultiHeadWdmClassifier` |
| `GpuDriverProfile` deprecated | `#[expect(deprecated)]` on `gpu_dispatch` module + 3 validation binaries, pending `DeviceCapabilities` migration |

### 2b. Semantic Method Naming Standard v2.1

| Method | Before | After |
|--------|--------|-------|
| `capabilities.list` (canonical) | Not handled | Dispatched to `handle_capability_list` |
| `capability.list` (legacy) | Dispatched | Still dispatched (alias) |
| `primal.capabilities` (ecosystem) | Not handled | Dispatched to `handle_capability_list` |
| `health.liveness` response | `{"alive": true}` | `{"status": "alive"}` per standard |

### 2c. biomeOS 5-Tier Discovery

| Tier | Implementation |
|------|---------------|
| 1. `BIOMEOS_SOCKET_DIR` env | Existing |
| 2. `$XDG_RUNTIME_DIR/biomeos/` | Existing |
| 3. `/run/user/{uid}/biomeos/` | Existing |
| 4. `temp_dir()/biomeos/` | Existing |
| 5. `socket-registry.json` | **New**: `lookup_socket_registry()` reads JSON map in socket dir |

Capability probing now tries `capabilities.list` first (canonical), falls back to `capability.list` (legacy), and parses 4 response formats (flat array, object array, wrapped, direct).

### 2d. Ecosystem Compliance

| Item | Status |
|------|--------|
| `publish = false` | Added to all 3 workspace `Cargo.toml` files |
| `deny.toml` | Already present |
| `provenance-trio-types` | Not referenced (clean) |
| `barracuda.*` IPC prefixes | Not present (clean — already using bare `domain.operation`) |
| Production mocks | None (only test mocks + intentional `coralreef_bridge` feature stub) |
| Files > 1000 lines | None (largest: 942 lines) |
| `todo!()`/`unimplemented!()` | None in production code |

---

## Part 3: Metrics

| Metric | Value |
|--------|-------|
| Lib tests | 1,183 |
| Forge tests | 9 |
| Doc tests | 13 |
| Total passing | 1,205 |
| Clippy warnings | 0 (pedantic + nursery, `-D warnings`) |
| Fmt diff | 0 |
| Doc warnings | 0 |
| Files modified (S169+S170) | 79 |
| Lines added | ~2,200 |

---

## Part 4: Ecosystem Recommendations

### For barraCuda
- `GpuDriverProfile` deprecation forces downstream `#[expect(deprecated)]` — consider maintaining the type until `DeviceCapabilities` has full parity for `fp64_strategy()`, `precision_routing()`, `needs_pow_f64_workaround()`
- `MultiHeadEsn` lost its `wgpu_device()` accessor — consumers must store the device separately

### For biomeOS
- neuralSpring now supports 5-tier discovery including `socket-registry.json`
- `health.liveness` response format aligned to `{"status": "alive"}`

### For All Springs
- `capabilities.list` (plural) should be the canonical method name per Semantic Method Naming v2.1
- `capability.list` and `primal.capabilities` should be kept as aliases
- 4-format capability response parsing is available as a reference in `discovery.rs`

---

## Part 5: Known Debt

| Item | Priority | Notes |
|------|----------|-------|
| `GpuDriverProfile` → `DeviceCapabilities` migration | P2 | Blocked on barraCuda documenting migration path |
| Coverage push to 90% | P2 | Currently ~92% per prior measurement; verify with fresh `llvm-cov` |
| Proptests for scientific invariants | P3 | groundSpring pattern; spectral/ESN/Anderson candidates identified |

---

*neuralSpring S170 — syntheticChemistry/neuralSpring @ main*
