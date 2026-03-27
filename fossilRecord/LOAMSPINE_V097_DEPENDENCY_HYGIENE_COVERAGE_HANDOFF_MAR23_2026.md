# LoamSpine v0.9.7 — Dependency Hygiene & Coverage Evolution Handoff

**Date:** March 23, 2026  
**Version:** 0.9.7  
**Previous:** v0.9.6 (Standards compliance, lint evolution)

---

## Summary

v0.9.7 achieves a clean `cargo deny check` (all four categories pass), trims
tarpc features to eliminate a bincode v1 transitive path, corrects stale
advisory attribution in `deny.toml`, and pushes line coverage above 92%.

---

## Changes

### Dependency Hygiene
- **tarpc feature trimming**: `features = ["full"]` → explicit list dropping
  `serde-transport-bincode`. Eliminates bincode v1 via tokio-serde transitive
  path (RUSTSEC-2025-0141 now only from direct storage dep).
- **`deny.toml` accuracy**: Advisory comments corrected —
  `fxhash`/`instant` traced to sled (not tarpc); `bincode` v1 to direct dep;
  `opentelemetry_sdk` to tarpc 0.37 hard dep (not feature-gated).
- **mdns advisories**: Three new ignores documented (async-std RUSTSEC-2025-0052,
  net2 RUSTSEC-2020-0016, proc-macro-error RUSTSEC-2024-0370) — all from
  optional `mdns` feature.
- **`publish = false`**: All workspace crates marked private; `allow-wildcard-paths`
  satisfies cargo-deny wildcard ban.
- **`libsqlite3-sys` wrapper**: `wrappers = ["rusqlite"]` allows the C dep only
  through the optional sqlite feature.
- **Result**: `cargo deny check` → advisories ok, bans ok, licenses ok, sources ok.

### Coverage Evolution
- **7 new sync streaming tests**: `push_entries_streaming` and
  `pull_entries_streaming` — success via mock server, failure fallback,
  requires-peers, empty state.
- **Sync module**: 69.00% → 90.57% line coverage.
- **Overall**: 91.67% → **92.23% line** / 89.87% → **90.46% region**.

### Hardcoding / Unsafe / Lint
- Port 443 → `HTTPS_DEFAULT_PORT` constant.
- Capability strings → `external::*` constants in infant discovery DNS SRV mapping.
- All `infant_discovery` test `unsafe` env mutations → `temp_env::with_vars` + phased `block_on`.
- `#[allow(deprecated)]` → `#[expect(deprecated, reason)]` in two remaining test files.

### Smart Refactors
- `redb_tests.rs` (955 → 574 + 395 `redb_tests_cert_errors.rs`) — split by domain.
- `jsonrpc/tests.rs` (903 → 588 + 379 `tests_permanence_cert.rs`) — split by domain.

### Cleanup
- Empty `examples/` directory removed.
- `verify.sh` updated to check all four `cargo deny` categories.
- Root docs (README, CONTEXT, KNOWN_ISSUES, CONTRIBUTING, STATUS, CHANGELOG) updated.

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 1,232 |
| Line coverage | 92.23% |
| Region coverage | 90.46% |
| Function coverage | 86.52% |
| Clippy | 0 (pedantic + nursery) |
| Unsafe | 0 (production + tests) |
| `cargo deny` | all pass |
| Max file | 865 lines |
| Source files | 124 `.rs` |

---

## Ecosystem Impact

- **No API changes** — Wire format and JSON-RPC methods unchanged.
- **No storage format changes** — bincode v1 remains for redb/sled/backup.
- **Dependency graph smaller** — tokio-serde no longer pulls bincode feature.
- **Partner primals**: No action required. tarpc binary protocol unchanged.

---

## Next (v0.9.8 Targets)

- Signing capability middleware (signature verification on RPC layer)
- mdns crate evolution (async-std → tokio-based alternative)
- Showcase demo expansion
- Collision layer validation (neuralSpring experiments)

---

*Part of ecoPrimals — see [wateringHole](https://github.com/ecoPrimals/wateringHole) for ecosystem standards.*
