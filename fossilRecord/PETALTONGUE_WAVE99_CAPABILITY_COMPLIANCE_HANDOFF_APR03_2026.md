# petalTongue Wave 99 — Capability-First Compliance Handoff

**Date**: April 3, 2026
**Previous**: `PETALTONGUE_DEEP_DEBT_EVOLUTION_PHASE4_HANDOFF_APR02_2026.md`
**Commit**: `10dda54`
**Audit**: primalSpring downstream audit, wave 99

---

## Summary

Eliminated all 24 primal-specific env-var references and ~20 primal-name violations in
production code paths. Completed PT-04 (HTML export validation) and PT-06 (callback push
server wiring). 23 files changed, 304 insertions, 194 deletions.

---

## Changes

### 1. Legacy Env-Var Removal (24 → 0 primal-specific env references)

| Removed Variable | File | Replacement |
|-----------------|------|-------------|
| `SONGBIRD_SOCKET_FALLBACK` | `primal_registration.rs` | Conventional `/tmp/biomeos/{socket}.sock` path |
| `TOADSTOOL_PORT` | `constants.rs` | `DISPLAY_BACKEND_PORT` only |
| `TOADSTOOL_URL` | `audio_providers/toadstool.rs`, `builders.rs` | `AUDIO_PROVIDER_URL` only |
| `BARRACUDA_SOCKET` | `physics_bridge.rs` | `COMPUTE_SOCKET` only |
| `BEARDOG_ENTROPY_ENDPOINT` | `human_entropy_window/state.rs` | `ENTROPY_SOURCE_ENDPOINT` only |

### 2. UI/Log String Cleanup (~20 primal-name violations → 0)

| Before | After |
|--------|-------|
| `"Toadstool Synthesis"` | `"Discovered Audio Synthesis"` |
| `"Active tier: Toadstool Synthesis"` | `"Active tier: Discovered Synthesis"` |
| `"Tiers: ... → Toadstool"` | `"Tiers: ... → Discovered synthesis"` |
| `"Toadstool not available/configured"` | `"Audio provider not available/configured"` |
| `"Requesting Toadstool synthesis"` | `"Requesting audio synthesis"` |
| All Toadstool-branded error/log strings | Capability-generic equivalents |

### 3. Capability-Based Routing Fix

`provenance_trio.rs::capability_matches_socket_name` now matches capability-domain keywords
(`dag`, `braid`, `spine`) instead of primal names (`rhizocrypt`, `sweetgrass`, `loamspine`).

### 4. PT-04: HTML Export Validation

- `validate_standalone_html_export()` in `petal-tongue-ui-core/trait_def.rs`
- Checks: non-empty, starts with `<!DOCTYPE` or `<html>`, contains `</html>`
- Wired into `wrap_svg_in_html` and `compile_html` paths
- Unit tests added

### 5. PT-06: Callback Push Server Wiring

- `spawn_push_delivery()` creates its own current-thread tokio runtime (works from sync context)
- `UnixSocketServer::new` now wires `callback_tx` at construction
- Push delivery thread stays alive for server lifetime
- Tests verify wiring

### 6. Documentation

- `ENV_VARS.md`: Removed stale primal-specific vars, added `COMPUTE_SOCKET`, `AUDIO_PROVIDER_URL`,
  `DISPLAY_BACKEND_PORT`, `ENTROPY_SOURCE_ENDPOINT`
- Doc comments across 6 crates cleaned of primal-name routing language
- `backend/mod.rs` docs aligned with current `FromStr` valid values

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | Zero warnings |
| `cargo doc --no-deps --all-features` | Clean |
| `cargo test --workspace --all-features` | **6,078 passing**, 0 failures |

---

## Audit Compliance

| Finding | Status |
|---------|--------|
| 24 primal-specific env-var references across 10 files | **RESOLVED** — all removed |
| ~20 non-test source files with primal names in discovery/IPC/UI | **RESOLVED** — all cleaned |
| PT-04 HTML export validation | **RESOLVED** — validation wired |
| PT-06 callback push server wiring | **RESOLVED** — thread spawned and wired |

All primalSpring wave 99 findings are addressed. Zero remaining primal-specific env-var
references in production code. `primal_names` constants remain in `capability_names.rs`
for logging context only — never used in routing or socket resolution.
