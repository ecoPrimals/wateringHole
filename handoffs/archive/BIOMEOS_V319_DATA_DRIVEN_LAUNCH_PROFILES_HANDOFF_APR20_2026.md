# biomeOS v3.19 — Data-Driven Launch Profiles, Port Constants, Dependency Pruning

**Date**: April 20, 2026
**From**: biomeOS v3.19
**Status**: COMPLETE — all changes committed, tested, pushed
**Tests**: 7,802 passing (0 failures), clippy 0 warnings

---

## Summary

Comprehensive hardcoding evolution pass: nucleus and spawner `match`/`if` blocks replaced by
TOML-driven launch profiles, magic port numbers centralized as typed constants, and unused
dependencies pruned. Follows directly from v3.18 spring audit fixes.

---

## Changes

### 1. Port Constants (biomeos-types)

Defined in `biomeos-types::constants::ports`:

- `TCP_SPAWN_BASE: u16 = 9900` — base port for child-primal spawn allocation
- `TCP_SPAWN_SCAN_RANGE: u16 = 20` — number of ports to probe during TCP-only discovery

Replaces hardcoded `9900` and `9920` literals in:
- `executor/context.rs` — `AtomicU16::new(9900)` → `AtomicU16::new(TCP_SPAWN_BASE)`
- `discovery_init.rs` — `for port in 9900..9920u16` → `TCP_SPAWN_BASE..(TCP_SPAWN_BASE + TCP_SPAWN_SCAN_RANGE)`

### 2. Translation Loader — Agnostic Port Resolution

`translation_loader.rs::resolve_tcp_port_for_primal()`:
- **Before**: 7-primal hardcoded port table (`BEARDOG→9900, SONGBIRD→9901, …`)
- **After**: Sequential `AtomicU16` counter starting at `TCP_SPAWN_BASE`; primal-agnostic

Removed direct imports of `BARRACUDA`, `BEARDOG`, `CORALREEF`, `NESTGATE`, `SONGBIRD`,
`SQUIRREL`, `TOADSTOOL` primal name constants from the translation loader.

### 3. Spawner Launch Profiles — `tcp_listen_flag`

`primal_spawner.rs::LaunchProfile` extended with:
```rust
tcp_listen_flag: Option<String>
```

`configure_primal_sockets()`:
- **Before**: `if primal_name == SONGBIRD { cmd.arg("--listen")… }`
- **After**: reads `tcp_listen_flag` from `config/primal_launch_profiles.toml`

Updated `primal_launch_profiles.toml`:
```toml
[profiles.songbird]
tcp_listen_flag = "--listen"
```

Removed unused `SONGBIRD` import from `primal_spawner.rs`.

### 4. Nucleus Launch Profiles — Data-Driven Build

Created `config/nucleus_launch_profiles.toml` defining per-primal nucleus-mode configuration:

| Profile | subcommand | pass_socket_flag | pass_family_id_flag | capability_sockets | env_vars | jwt | ai |
|---------|-----------|-----------------|--------------------|--------------------|----------|-----|-----|
| default | server | true | false | — | — | no | no |
| songbird | server | true | false | security(×3) | — | no | no |
| nestgate | daemon | false | true | — | JWT_SECRET_KEY | yes | no |
| toadstool | server | true | false | — | TOADSTOOL_FAMILY_ID | no | no |
| squirrel | server | true | false | discovery | — | no | yes |

`nucleus.rs::build_primal_command_with()`:
- **Before**: 67-line `match config.name { SONGBIRD => …, NESTGATE => …, … }` block
- **After**: loads `NucleusLaunchConfig` from embedded TOML, applies profile fields generically
- Features: `$family_id` substitution in env vars, capability-resolved socket paths, JWT
  auto-generation, AI model/provider passthrough — all configurable without code changes

### 5. Dependency Pruning

Removed unused `walkdir` from 3 crate `Cargo.toml` files:
- `biomeos-deploy`
- `biomeos-boot`
- `biomeos-niche`

---

## Verification

- `cargo check --workspace` — PASS
- `cargo clippy --workspace --all-targets` — 0 warnings
- `cargo test --workspace` — 7,802 tests, 0 failures
- `cargo fmt --all` — clean

---

## Impact for Other Primals

- **New primals** no longer require code changes to biomeOS for nucleus-mode launch — add a
  TOML profile to `nucleus_launch_profiles.toml` and `primal_launch_profiles.toml`
- TCP port allocation is fully agnostic — no primal-name-to-port mapping needed
- Springs validating TCP-only mode should use `TCP_SPAWN_BASE` from `biomeos-types` if
  they need to predict port assignments

---

## Files Changed

| File | Change |
|------|--------|
| `crates/biomeos-types/src/constants/mod.rs` | Added `TCP_SPAWN_BASE`, `TCP_SPAWN_SCAN_RANGE` |
| `crates/biomeos-atomic-deploy/src/executor/context.rs` | Use `TCP_SPAWN_BASE` constant |
| `crates/biomeos-atomic-deploy/src/neural_api_server/discovery_init.rs` | Use port constants |
| `crates/biomeos-atomic-deploy/src/neural_api_server/translation_loader.rs` | Agnostic counter |
| `crates/biomeos-atomic-deploy/src/executor/primal_spawner.rs` | `tcp_listen_flag` field |
| `config/primal_launch_profiles.toml` | Songbird `tcp_listen_flag` |
| `config/nucleus_launch_profiles.toml` | **New** — data-driven nucleus profiles |
| `crates/biomeos/src/modes/nucleus.rs` | TOML-driven `build_primal_command_with` |
| `crates/biomeos-deploy/Cargo.toml` | Removed `walkdir` |
| `crates/biomeos-boot/Cargo.toml` | Removed `walkdir` |
| `crates/biomeos-niche/Cargo.toml` | Removed `walkdir` |
