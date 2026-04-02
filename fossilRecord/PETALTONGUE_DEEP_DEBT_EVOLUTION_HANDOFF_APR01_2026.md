# petalTongue Deep Debt Evolution Handoff

**Date**: April 1, 2026  
**Phase**: Deep debt elimination and modern Rust evolution  
**Previous**: `PETALTONGUE_CAPABILITIES_DOCS_CLEANUP_HANDOFF_MAR31_2026.md`

---

## Summary

Systematic deep-debt evolution pass across the petalTongue codebase. All
primalSpring audit items (PT-04 through PT-07) were completed in the prior
session; this session focuses on structural debt, idiomatic Rust evolution,
and hardcoding elimination.

---

## Changes

### Zero-Copy IPC Evolution (7 paths)

Evolved all JSON-RPC serialization hot paths from `serde_json::to_string` +
`as_bytes()` (String allocation → byte slice) to `serde_json::to_vec`
(direct byte buffer). Eliminates intermediate `String` allocation on every
IPC frame.

Files: `unix_socket_connection.rs`, `json_rpc_client.rs` (×2), `client.rs`,
`server.rs`, `primal_registration.rs`, `provenance_trio.rs`, `songbird_client.rs`.

### Cryptographic Hash Evolution

Replaced `std::collections::hash_map::DefaultHasher` placeholder in
`provenance_trio.rs` with real **blake3** (pure Rust, `default-features = false`,
zero C/asm deps). Passes `cargo deny check` (advisories, bans, licenses, sources).

### Timeout Centralization

Added `constants::discovery_timeouts` module (12 named constants) covering HTTP
client, cache TTL, and Songbird UDS timeouts. Wired into `http_provider.rs`,
`cache.rs`, `songbird_client.rs`, `provider_trait.rs`, `server_mode.rs`. Scattered
`Duration::from_secs/millis` literals replaced with centralized, env-overridable
constants.

### Hardcoded Primal Names → Constants

7 files evolved from string literals (`"biomeos"`, `"petaltongue"`) to
`primal_names::BIOMEOS`, `primal_names::PETALTONGUE`, `constants::APP_DIR_NAME`,
`socket_roles::NEURAL_API`. Wire/path contexts only — UI branding text remains
as display copy.

### Production Placeholder Evolution

- `provenance_trio.rs` hash → real blake3
- `external.rs` present() → traced with frame metadata (architectural boundary)
- `tui/devices.rs` → renders real discovered `PrimalInfo` from discovery provider
  instead of placeholder "Device N" entries

### Large File Smart Refactoring

- `songbird_client.rs`: extracted `parse_primal_array()` (eliminated 20+ lines duplication)
- `paint.rs`: extracted `world_to_screen()` + `world_points_to_screen()` (deduped 13 inline patterns)
- `graph.rs`: extracted `adjacency_list()` (deduped 3 construction sites)

### Documentation Consistency

12 docs/specs reconciled from "JSON-RPC primary" to "tarpc PRIMARY, JSON-RPC
universal fallback" — aligns with ecosystem standard. Files: `lib.rs` (ipc, api,
ui crates), `README.md`, `START_HERE.md`, `ENV_VARS.md`, 6 spec files.

### Build Infrastructure

- `rust-toolchain.toml` added (pins `stable` + `rustfmt`, `clippy`, `llvm-tools-preview`)
- `Cargo.lock` refreshed (9 deps updated)
- `blake3` added as workspace dep (pure Rust, `default-features = false`)

### Root Documentation

- `README.md`: test counts (5,845+), Rust version (pinned via toolchain), blake3 noted
- `START_HERE.md`: date updated, test counts aligned
- `ENV_VARS.md`: added `PETALTONGUE_WEB_PORT`, `PETALTONGUE_HEADLESS_PORT`,
  `PETALTONGUE_BIND_ADDR`; fixed duplicate separator; moved `PETALTONGUE_TELEMETRY_DIR`
  into main body

---

## Quality Gates

| Check | Status |
|-------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | Zero warnings |
| `cargo doc --workspace --no-deps` | Clean |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |
| `cargo test --workspace` | 5,845+ tests, 0 failures |

---

## Ecosystem Impact

- **Songbird clients** benefit from centralized timeouts (configurable via env)
- **biomeOS integration** uses `primal_names::BIOMEOS` everywhere (no drift)
- **IPC throughput** improved by eliminating String intermediary on every frame
- **Provenance integrity** now uses real BLAKE3 instead of non-cryptographic hash

---

## Deferred

- Full `Cow<'_, str>` evolution for IPC handler request params (requires type changes)
- Pin specific Rust version in `rust-toolchain.toml` (currently `stable` channel)
- Test-module extraction to reduce largest-file line counts below 700
- `with_mock_mode` config flag audit (intentional but worth documenting boundaries)

---

## Not Changed (intentional)

- **println!/eprintln!**: All 98 instances are intentional CLI user output — no tracing evolution needed
- **UI branding strings**: "petalTongue Dashboard", "biomeOS (Neural API):" etc. — display copy stays as literals
- **deny.toml license allowances**: Defensive forward-looking policy, not debt
- **archive/**: Fossil record — not cleaned (ecosystem policy)
