# BearDog v0.9.0 — Wave 27 primalSpring License Audit Handoff

**Date:** April 2, 2026
**Author:** AI pair (Claude) + eastgate
**Scope:** primalSpring license audit remediation: AGPL-3.0-or-later migration, `#[expect(reason)]` lint migration, legacy method deprecation, extra binary documentation

---

## Summary

Addressed all four items from the primalSpring downstream audit: license
alignment with ecosystem standard, lint attribute modernisation, flat method
alias deprecation, and binary target documentation.

---

## Gate Status (April 2, 2026)

| Gate | Result |
|------|--------|
| `cargo fmt --check` | Pass |
| `cargo clippy --workspace -D warnings` | Pass (0 warnings) |
| `cargo build --workspace` | Pass |
| `cargo test --workspace` | **14,366 passed, 0 failed** |
| `cargo deny check` | advisories ok, bans ok, licenses ok, sources ok |

---

## Audit Items — All Resolved

### 1. License: AGPL-3.0-only → AGPL-3.0-or-later

Per `STANDARDS_AND_EXPECTATIONS.md`: "Pinning to `-only` means not trusting
the nonprofit stewards who fight the legal battles."

| Artifact | Count | Change |
|----------|-------|--------|
| `Cargo.toml` (workspace + crates + showcase + benchmarks) | 58 | `license = "AGPL-3.0-or-later"` |
| `deny.toml` allowed licenses | 1 | `"AGPL-3.0-or-later"` |
| SPDX headers (`// SPDX-License-Identifier:`) | 2,075 | `AGPL-3.0-or-later` |
| Markdown docs | 21+ | All references updated |
| `LICENSE-DOCS.md` | 1 | Provenance Trio table + rationale updated |

### 2. `#[allow()]` → `#[expect(reason)]` in Non-Test Code

| Crate area | Migrated | Notes |
|------------|----------|-------|
| `beardog-cli` | 35 → `#[expect]` or removed | Some items were revealed as non-dead-code by `#[expect]` (unfulfilled expectation) — confirmed used and attribute removed |
| `beardog-core` | 5 → `#[expect(reason)]` | `deprecated`, `missing_docs` |
| `beardog-tunnel` | 9 → `#[expect(reason)]` or removed | Cast/precision attrs, deprecated, dead_code |

**Documented limitation:** `dead_code` on pub items in lib+bin dual-target
crates (e.g. `beardog-cli` with both `lib.rs` and `main.rs`) requires
`#[allow]` — the `dead_code` lint fires only in the bin context, but
`#[expect]` is evaluated in the lib context where pub items are never dead.
Each such `#[allow]` carries a `reason` explaining this.

### 3. Legacy Flat Method Aliases — Documented Deprecated

| Handler | Canonical (use these) | Deprecated (v1.0 removal) |
|---------|----------------------|--------------------------|
| `CapabilitiesHandler` | `capabilities.list`, `capability.list`, `primal.capabilities` | `capabilities`, `get_capabilities` |
| `CapabilitiesHandler` | (future `identity.*`) | `identity`, `whoami`, `get_identity` |
| `HealthHandler` | `health.liveness`, `health.readiness`, `health.check` | `ping`, `health`, `status`, `check` |

Doc comments updated with `## Canonical Methods` and `## Deprecated Flat
Aliases` sections. Inline comments in `match` arms mark deprecated branches.

### 4. Extra Binaries — Documented as Tooling Exceptions

Added `Binary Targets` section to `ARCHITECTURE.md`:

| Binary | Status |
|--------|--------|
| `beardog` | Primary UniBin (all user-facing functionality) |
| `beardog-installer` | Tooling exception: host-side deployment tool |
| `deploy-pixel8` | Tooling exception: Android adb deployment |
| 22+ showcase demos | Non-workspace standalone examples |

---

## Files Changed (2,158 total)

Bulk: 2,075 `.rs` SPDX headers, 58 `Cargo.toml` license fields, 21+ `.md` docs

Key targeted files:
- `deny.toml` — license allow list
- `LICENSE-DOCS.md` — provenance trio rationale
- `ARCHITECTURE.md` — binary targets section
- `STATUS.md` / `CHANGELOG.md` — Wave 27 entry
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` — deprecation docs
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/health.rs` — deprecation docs
- `crates/beardog-tunnel/src/universal_hsm/entropy/collector.rs` — lint cleanup
- `crates/beardog-core/src/zero_knowledge_bootstrap/mod.rs` — `#[expect(deprecated)]`
- 11 files in `crates/beardog-cli/src/handlers/` — `#[allow]`/`#[expect]` migration
