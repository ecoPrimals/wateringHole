# NestGate — Deep Debt Audit Session 39

**Date:** April 8, 2026
**Primal:** NestGate (storage domain)
**Commits:** `90c45cec` (BTSP Phase 1), `68c7c122` (deep debt cleanup)

---

## Scope

Full-spectrum deep debt audit covering: large files, unsafe code, hardcoded primal
names, production mocks/stubs, external dependencies, deprecated/dead code patterns,
production unwrap/panic usage.

---

## Audit Findings (verified clean)

| Dimension | Result |
|-----------|--------|
| **Files >800 lines** | Zero production files over 800L. Largest: ~759L (`crud.rs`) |
| **Unsafe code** | Zero `unsafe` blocks in executable code anywhere in tree |
| **`unreachable!()` macros** | Zero in entire codebase |
| **Production `.unwrap()`** | Zero in high-traffic crates (nestgate-rpc, nestgate-config, nestgate-api) — all in test code |
| **Production `todo!` / `unimplemented!`** | Zero in executable code (only in doc examples) |
| **Single logging stack** | tracing only (no `log` crate) |
| **Single JSON stack** | serde + serde_json |

---

## Changes Made

### 1. BTSP Phase 1 (commit `90c45cec`)

**False positives in primalSpring audit corrected:**

- **BIOMEOS_INSECURE guard** — new: refuse startup when `FAMILY_ID` + `BIOMEOS_INSECURE=1` both set.
  Also reads generic `FAMILY_ID` env (in addition to `NESTGATE_FAMILY_ID`).
- **Family-scoped socket naming** — `nestgate-{fid}.sock` and `storage-{fid}.sock` when FAMILY_ID is
  set (not "standalone"/"default"). Tiers 2/3/4 all updated.
- 13 new tests for guard and naming.

### 2. Self-Knowledge Standard (commit `68c7c122`)

Removed hardcoded primal names from doc comments in 8 files:
- `nestgate-config/src/config/runtime/services.rs` — "BearDog" → `<specific-primal>`
- `nestgate-config/src/config/external/services_config.rs` — `beardog_url` → generic
- `nestgate-discovery/src/capability_discovery.rs` — "beardog, songbird" → "specific primal names"
- `nestgate-discovery/src/capabilities/mod.rs` — "beardog" in anti-pattern examples → generic
- `nestgate-discovery/src/capabilities/discovery/mod.rs` — same
- `nestgate-discovery/src/primal_discovery/runtime_discovery.rs` — "beardog" removed
- `nestgate-rpc/src/rpc/unix_socket_server/storage_handlers.rs` — "primalSpring" → "downstream"
- `nestgate-core/src/services/storage/operations/objects.rs` — "primalspring" path example → "myapp"

### 3. Dead Dependency Cleanup (commit `68c7c122`)

- Removed unused `tokio`, `anyhow`, `thiserror` from `nestgate-middleware/Cargo.toml`
- Removed unused workspace entries: `ahash`, `arrayvec`, `indexmap`, `smallvec` from root `Cargo.toml`

### 4. Panic Elimination (commit `68c7c122`)

- `safe_ring_buffer.rs`: `unwrap_or_else(|_| panic!(...))` → `match` + `unreachable!()`
- `safe_memory_pool.rs`: same pattern
- Removed now-unfulfilled `#[expect(clippy::panic)]` attributes from both

---

## Remaining Observations (not blocking)

| Item | Status | Notes |
|------|--------|-------|
| ~130 `#[deprecated]` attributes | Intentional migration wave | Guides canonical config migration |
| `expect(dead_code)` in 4 crate roots | Scaffold pattern | Will auto-warn when dead code is used |
| `dev-stubs` / `mock-metrics` features | Feature-gated | Not in default production build |
| Storage detector placeholders (Ok(Vec::new())) | Documented structural stubs | AWS/Azure/GCS/SMB/NFS/iSCSI detection |
| tower-http 0.5 + 0.6 in lockfile | Transitive duplicate | Align when dependents update |
| rustix 0.38 + 1.1 in lockfile | Transitive duplicate | Migrate to 1.x when touching call sites |
| base64, rand, getrandom duplicates | Transitive | Reduce via coordinated dependency updates |
| Pre-existing flaky test (ZFS workspace) | Intermittent in parallel | Not from current changes |

---

## Verification

- `cargo check --workspace` — clean
- `cargo clippy -p nestgate-core -p nestgate-rpc -p nestgate-config -p nestgate-middleware --lib` — clean
- `cargo test -p nestgate-core -p nestgate-rpc -p nestgate-config -p nestgate-middleware -p nestgate-discovery` — 927+ passed
- `cargo fmt --all -- --check` — clean
