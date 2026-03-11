# biomeOS V2.30 — Deep Debt Evolution + Hardware Learning Wiring

**Date**: March 11, 2026
**From**: biomeOS v2.30
**To**: All springs, toadStool, coralReef teams
**Tests**: 3,148 passing sequential (0 failures, 24 ignored)
**Clippy**: 0 warnings | **Format**: PASS | **C deps**: 0

---

## Summary

Two major deliverables:

1. **8-Phase Deep Debt Evolution Plan** — comprehensive architecture modernization
2. **Hardware Learning Capability Wiring** — 5 `compute.hardware.*` capabilities registered for toadStool hw-learn crate

---

## Part 1: Deep Debt Evolution (8 Phases)

### Phase 1: Capability-Based Routing
- `primal_spawner.rs` hardcoded `match` block → data-driven `config/primal_launch_profiles.toml`
- `bootstrap.rs` uses `env_config::security_provider()` + `CapabilityTaxonomy::resolve_to_primal("security")`
- `ai_advisor.rs` resolves AI provider dynamically via `CapabilityTaxonomy::resolve_to_primal("ai")`

### Phase 2: Hardcoded Path Elimination
7 files migrated from hardcoded `/tmp`, personal paths, and manual env var lookups to `SystemPaths` XDG:
- `subfederation.rs`, `live_discovery.rs`, `genome_dist.rs`, `types.rs`, `federation.rs` CLI, `genome.rs` CLI
- Removed `/path/to/ecoPrimals/wateringHole/genomeBin` fallback from genome distribution

### Phase 3: Missing Deploy Graphs
- `nucleus_simple.toml` — lightweight NUCLEUS for dev/constrained environments
- `ui_atomic.toml` — Squirrel + petalTongue on top of Tower Atomic
- `livespore_create.toml` — portable LiveSpore creation workflow
- Niche template `graph_id` naming standardized (underscores, not hyphens)

### Phase 4: Large File Refactoring
6 files >1000 LOC split into domain modules:

| Original | Lines | Modules Created |
|----------|-------|----------------|
| `biomeos-system/src/lib.rs` | 1428 | `cpu.rs`, `memory.rs`, `disk.rs`, `network.rs`, `uptime.rs` |
| `biomeos-types/config/security.rs` | 1376 | `security/tls.rs`, `security/crypto.rs`, `security/authorization.rs` |
| `capability_handlers.rs` | 1342 | `capability_handlers/discovery.rs`, `primal_start.rs`, `health.rs` |
| `genome_dist.rs` | 1328 | `genome_dist/discovery.rs`, `manifest.rs`, `distribution.rs`, `error.rs` |
| `protocol_escalation.rs` | 1289 | `protocol_escalation/config.rs`, `metrics.rs`, `engine.rs` |
| `nucleus.rs` | 1282 | `nucleus/discovery.rs`, `verification.rs`, `trust.rs` |

### Phase 5: Dead Code + Placeholder Resolution
- `usb.rs`: Fixed `metadata.len()` misuse for disk space → `(0, 0)` + `tracing::warn!`
- `nucleus/verification.rs`: `UNVERIFIED_SIGNATURE` constant replaces magic string
- `config_builder.rs`: `with_dns_discovery_domain()` replaces hardcoded empty string

### Phase 6: Env Var Centralization
New `biomeos-types/src/env_config.rs`:
- Constants: `FAMILY_ID`, `SECURITY_PROVIDER`, `SOCKET_DIR`, `XDG_RUNTIME_DIR`, etc.
- Typed accessors: `family_id() -> Option<String>`, `socket_dir() -> Option<PathBuf>`, etc.

### Phase 7: Rust Modernization
- Neural API routing: large `match` → `const ROUTE_TABLE: &[(&str, Route)]` (78 entries)
- `unwrap_or_default()` on serde_json → `unwrap_or_else` + `tracing::warn!`
- `#![warn(missing_docs)]` added to `biomeos-atomic-deploy`, `biomeos-test-utils`, `src/lib.rs`, `tools/src/lib.rs`

### Phase 8: Cargo.toml Audit
- `libc` removed from workspace `Cargo.toml` and 3 crate `Cargo.toml` files
- `cargo tree` confirms 0 `-sys` crates except `linux-raw-sys` (pure Rust syscall interface used by `rustix`)

---

## Part 2: Hardware Learning Capability Wiring

5 new capabilities in `config/capability_registry.toml` under `[translations.compute]`:

```toml
"compute.hardware.observe" = { provider = "toadstool", method = "hw_learn.observe" }
"compute.hardware.distill" = { provider = "toadstool", method = "hw_learn.distill" }
"compute.hardware.apply"   = { provider = "toadstool", method = "hw_learn.apply" }
"compute.hardware.share"   = { provider = "toadstool", method = "hw_learn.share_recipe" }
"compute.hardware.status"  = { provider = "toadstool", method = "hw_learn.status" }
```

`hardware_learning` keyword added to compute domain in `capability_domains.rs` with test coverage.

Prefix-based fallback resolution: `compute.hardware.observe` → matches `compute` prefix → resolves to `toadstool`.

---

## Part 3: Bug Fix

Pre-existing flaky test in `capability_handlers/primal_start.rs`: CWD restoration after temp dir could panic. Fixed to gracefully fall back to `std::env::temp_dir()` (3 occurrences).

---

## Action Items

### toadStool Team (P1)
- Wire `hw_learn.observe/distill/apply/share/status` methods into toadStool server for biomeOS capability calls
- The 5 capabilities are registered and will route correctly once toadStool exposes them

### coralReef Team (P2)
- hw-learn's `applicator/nouveau_drm.rs` provides framework for DRM ioctl-based recipe application
- When DRM dispatch works, hw-learn can trace and learn init patterns automatically

### All Springs
- `env_config.rs` is the canonical source for BIOMEOS_* env var names — use `biomeos_types::env_config::vars::*` constants instead of string literals

---

## Files Changed (Key)

| File | Change |
|------|--------|
| `config/primal_launch_profiles.toml` | **New** — data-driven primal launch config |
| `config/capability_registry.toml` | 5 `compute.hardware.*` translations added |
| `crates/biomeos-types/src/env_config.rs` | **New** — centralized env var accessors |
| `crates/biomeos-types/src/config/security/` | **New** — split from monolithic `security.rs` |
| `crates/biomeos-system/src/{cpu,memory,disk,network,uptime}.rs` | **New** — split from monolithic `lib.rs` |
| `crates/biomeos-atomic-deploy/src/capability_handlers/` | **New** — split from monolithic file |
| `crates/biomeos-api/src/handlers/genome_dist/` | **New** — split from monolithic file |
| `crates/biomeos-atomic-deploy/src/protocol_escalation/` | **New** — split from monolithic file |
| `crates/biomeos-federation/src/nucleus/` | **New** — split from monolithic file |
| `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs` | Table-driven ROUTE_TABLE |
| `crates/biomeos-atomic-deploy/src/executor/primal_spawner.rs` | Profile-based launch config |
| `graphs/{nucleus_simple,ui_atomic,livespore_create}.toml` | **New** deploy graphs |
| `Cargo.toml` + 3 crate Cargo.toml | `libc` removed |

---

*biomeOS v2.30 — 170+ capability translations, 24 deploy graphs, 0 C deps, 0 hardcoded paths.*
