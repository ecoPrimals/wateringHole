# petalTongue v1.6.6 — Socket Path Centralization + #[expect] Reasons

**Date**: April 30, 2026  
**Scope**: Deep debt — socket search path deduplication, lint attribute hygiene  
**Tests**: 6,054+ passing (98 suites), 0 failures, 0 Clippy warnings

---

## 1. Socket Search Path Centralization

**Problem**: 8+ files across 6 crates duplicated the same socket search path
construction logic (XDG → /run/user/{uid} → /tmp → /var/run/ecoPrimals).
Each copy independently reimplemented the priority chain, risking drift and
inconsistency.

**Fix**: New `constants::socket_search_dirs() -> Vec<PathBuf>` in
`petal-tongue-core/src/constants/network.rs`. Returns the canonical ordered
list with XDG/run deduplication. All consumers now call this single function.

**Files updated** (16 total, -81/+63 lines):

| File | Change |
|------|--------|
| `petal-tongue-core/src/constants/network.rs` | Added `socket_search_dirs()` |
| `petal-tongue-discovery/src/unix_socket_provider.rs` | Replaced 12-line constructor |
| `petal-tongue-discovery/src/neural_api_provider/provider.rs` | Replaced `get_search_paths()` body |
| `petal-tongue-discovery/src/discovery_service_client/mod.rs` | Replaced `get_search_paths()` body |
| `petal-tongue-ui/src/universal_discovery.rs` | Replaced 7-line path block |
| `petal-tongue-ipc/src/socket_path.rs` | `/tmp` → `LEGACY_TMP_PREFIX` |
| `petal-tongue-ipc/src/discovery_helpers.rs` | `/tmp` → `LEGACY_TMP_PREFIX` |
| `petal-tongue-ipc/src/provenance_trio.rs` | `/tmp` → `LEGACY_TMP_PREFIX` |
| `petal-tongue-api/src/biomeos_jsonrpc_client.rs` | `/tmp` → `LEGACY_TMP_PREFIX` |
| `petal-tongue-core/src/gpu_compute_provider.rs` | `/tmp` → `LEGACY_TMP_PREFIX` |
| `petal-tongue-discovery/src/jsonrpc_provider/provider.rs` | Deduplicated `/run/user` formatting |

**Result**: Zero hardcoded `/tmp` literals remain in production code.

---

## 2. Bare #[expect] Reason Strings

**Problem**: 6 `#[expect(...)]` attributes lacked `reason = "..."` strings,
violating the project policy that all lint suppressions must be justified.

**Fixed**:

| File | Lint | Reason added |
|------|------|-------------|
| `petal-tongue-ui/src/app/mod.rs` | `struct_excessive_bools` | UI app state naturally requires many boolean flags |
| `petal-tongue-core/src/sensor/types.rs` | `struct_excessive_bools` | capability flags are naturally boolean |
| `petal-tongue-core/src/modality.rs` (×2) | `struct_excessive_bools` | accessibility/capability flags are naturally boolean |
| `petal-tongue-core/src/instance/lifecycle.rs` | `unnecessary_wraps` | Result return needed for trait consistency |
| `petal-tongue-discovery/src/dns_parser/record.rs` | `upper_case_acronyms` | DNS record types are canonically all-caps |

---

## Comprehensive Audit Metrics

| Metric | Status |
|--------|--------|
| `unsafe` in production | **0** |
| `dyn` in production | **0** |
| `TODO`/`FIXME`/`HACK` | **0** |
| `#[allow(` in production | **0** |
| Bare `#[expect(` without reason | **0** |
| Production `unwrap`/`expect` | **1** (justified: `retry.rs` loop invariant) |
| Files >700 lines | **1** (`visualization/mod.rs` at 712) |
| Hardcoded `/tmp` in production | **0** |
| Tests | 6,054+ (98 suites) |
| Clippy warnings | **0** |

---

## Remaining

- BTSP Phase 3 encryption
- aarch64 musl cross-compile for headless
- Audio backend wire protocols (via ToadStool `audio.play` discovery)
- Overlay mode (toadStool Display Phase 2)
- egui texture resolution (`TextureResolver` with `egui::Shape::image`)
- BearDog crypto.sign delegation for scene signing (currently local BLAKE3)
