# biomeOS v3.11 — Deep Debt: Self-Knowledge & Capability-Based Evolution

**Date**: 2026-04-12
**Author**: biomeOS team
**Scope**: Deep debt audit + self-knowledge evolution + dependency analysis
**Commits**: `8515f246` (TCP-only fix), `020c3294` (self-knowledge evolution)

## Audit Summary

Comprehensive 4-axis audit of the biomeOS codebase covering:
- File sizes and refactoring candidates
- Unsafe code and external dependencies
- Hardcoded values and mock code in production
- TODO/FIXME markers and incomplete implementations

### Audit Results (clean)

| Category | Finding |
|----------|---------|
| **Files >800 lines** | **0** production files over 800L — 2 files at exactly 800L |
| **Unsafe code** | **0** — `#![forbid(unsafe_code)]` enforced across all crates |
| **FFI / extern "C"** | **0** — no `#[link]`, no `extern "C"` blocks |
| **todo!() / unimplemented!()** | **0** in production code |
| **TODO / FIXME / HACK / XXX** | **0** in .rs files |
| **#[allow(dead_code)]** | **0** — uses `#[expect]` with documented reasons |
| **Mocks in production** | **0** — `test_support.rs` already gated behind `cfg(any(test, feature))` |
| **unwrap/expect in production** | Confined to tests; workspace denies via clippy |

## Dependency Evolution

### Verified Pure Rust

| Dependency | Status |
|-----------|--------|
| **blake3** | Pinned `features = ["pure"]` — no C assembly, no `cc` needed |
| **serde_yaml_ng** | Uses `unsafe-libyaml` which is c2rust output (Rust, not C linking); tracked for migration to `serde-saphyr` when it reaches 1.0 |
| **rtnetlink** | Pulls `netlink-sys`/`nix`/`libc` — system-level, acceptable for Linux socket ops |
| **First-party code** | Zero `build.rs` C compilation, zero `-sys` crate direct usage |

### tools/ Workspace (separate)
- `reqwest` → `ring` (C/asm) — isolated to tools, not in main workspace

## Code Evolutions Applied

### 1. Bootstrap log messages — resolved provider names
- `bootstrap.rs`: Security health check warn uses `security_provider` variable instead of hardcoded "BearDog"
- Agnostic to which primal provides the security capability

### 2. Forwarding BTSP messages — capability-based
- `forwarding.rs`: BTSP warn/debug messages say "security provider" instead of "BearDog"
- Works correctly regardless of `BIOMEOS_SECURITY_PROVIDER` value

### 3. Capability domain constant
- `capability_domains.rs`: Composition domain uses `primal_names::BIOMEOS` constant instead of string literal `"biomeos"`

### 4. Discovery error — capability-based
- `discovery_bootstrap.rs`: Error message says "No discovery provider found" instead of "ensure Songbird is running"
- Still shows the actual primal name in the quick-fix steps (from variable, not hardcoded)

### 5. TCP self-registration — configurable host
- `bootstrap.rs`: Reads `BIOMEOS_BIND_ADDRESS` env var for TCP endpoint host
- Falls back to `127.0.0.1` only when unset
- Consistent with existing `bind_address()` pattern in `biomeos-types`

## Files Changed

| File | Change |
|------|--------|
| `bootstrap.rs` | Resolved provider name in logs, configurable TCP host |
| `capability_domains.rs` | `BIOMEOS` constant, expanded import |
| `forwarding.rs` | "security provider" instead of "BearDog" in BTSP messages |
| `discovery_bootstrap.rs` | Capability-based error message + test assertion update |

## Remaining Tracked Items

| Item | Status | Notes |
|------|--------|-------|
| `serde_yaml_ng` → `serde-saphyr` | **TRACKED** | Waiting for serde-saphyr 1.0 (currently 0.0.x, not API-compatible drop-in) |
| `unsafe-libyaml` transitive | **ASSESSED** | c2rust output (Rust, not C linking); acceptable until pure Rust YAML is stable |
| `tools/reqwest` → `ring` | **SEPARATE** | Isolated tools workspace; not in main binary |

## Validation
- `cargo fmt --all -- --check`: PASS
- `cargo clippy --workspace --all-targets`: PASS (0 warnings)
- `cargo test --workspace`: **7,000+ passed, 0 failed**
