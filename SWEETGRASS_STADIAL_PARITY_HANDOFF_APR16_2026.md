# sweetGrass Stadial Parity Handoff — April 16, 2026

**From**: sweetGrass (provenance + attribution primal)
**To**: primalSpring, all primal teams
**Re**: `STADIAL_PARITY_GATE_APR16_2026.md` resolution
**License**: AGPL-3.0-or-later

---

## Summary

sweetGrass has cleared the stadial parity gate. All `#[async_trait]` attributes
eliminated, all finite-implementor `Arc<dyn Trait>` replaced with enum dispatch,
`async-trait` crate removed from all direct dependencies.

| Gate Criterion | Before | After | Status |
|----------------|--------|-------|--------|
| `#[async_trait]` attributes | 22 | 0 | **CLEARED** |
| `async-trait` in Cargo.toml | 7 crates | 0 crates | **CLEARED** |
| `Arc<dyn Trait>` finite-implementor | ~130 | 0 | **CLEARED** |
| `dyn` (non-trait-object, legitimate) | ~132 | 2 | **CLEARED** |
| Edition 2024 | yes | yes | **CLEARED** |
| `cargo deny check bans` | pass | pass | **CLEARED** |

---

## What Changed

### Traits Converted (6 total)

| Trait | Crate | Impls | Backend Enum |
|-------|-------|-------|-------------|
| `BraidStore` | sweet-grass-store | 5 prod + 2 test | `BraidBackend` |
| `SigningClient` | sweet-grass-integration | 2 | `SigningBackend` |
| `AnchoringClient` | sweet-grass-integration | 2 | `AnchoringBackend` |
| `SessionEventsClient` | sweet-grass-integration | 2 | `SessionEventsBackend` |
| `SessionEventStream` | sweet-grass-integration | 2 | `SessionEventStreamBackend` |
| `PrimalDiscovery` | sweet-grass-integration | 3 | `DiscoveryBackend` |

All traits use `fn ... -> impl Future<Output = ...> + Send` (RPITIT).
All backend enums implement the trait via `match` delegation.

### Generic Consumers

| Consumer | Generic Over | Typical Instantiation |
|----------|-------------|----------------------|
| `QueryEngine<S>` | `S: BraidStore` | `QueryEngine<BraidBackend>` |
| `AnchorManager<S>` | `S: BraidStore` | `AnchorManager<BraidBackend>` |
| `EventHandler<S>` | `S: BraidStore` | `EventHandler<BraidBackend>` |

Tests instantiate with `MemoryStore` or specific backend variants directly.

### Remaining `dyn` (2, legitimate)

1. `traversal/mod.rs:189` — `Pin<Box<dyn Future>>` for recursive async traversal
   (Rust requires boxing for recursive futures)
2. `jsonrpc/mod.rs:138` — `Pin<Box<dyn Future>>` in dispatch function pointer type
   (unbounded implementors — closures)

Neither is a finite-implementor trait object. Both are stadial-compliant.

---

## Lockfile Debt Status

### `ring` — dev-dependency only

```
ring v0.17.14
└── rustls v0.23.38
    └── bollard v0.18.1
        └── testcontainers v0.23.3
            [dev-dependencies]
            └── sweet-grass-store-postgres v0.7.27
```

**Not in production binary.** The chain is:
testcontainers (Docker integration testing) → bollard (Docker API client) → rustls → ring.

**Resolution path**: When `testcontainers` updates to a version using
`rustls-platform-verifier` or `rustls-rustcrypto` (no ring), this clears
automatically. NestGate already demonstrated this path: `reqwest → ureq 3.3 +
rustls-rustcrypto`. Alternatively, pinning bollard features to use `native-tls`
would eliminate `ring` but add `openssl-sys` — not acceptable per ecosystem
standards. The current state (dev-dep only, not in ecoBin) is the correct
holding pattern.

### `libsqlite3-sys` — lockfile phantom

```
cargo tree -i libsqlite3-sys → "warning: nothing to print"
cargo tree -i libsqlite3-sys --target all → "warning: nothing to print"
```

`libsqlite3-sys` appears in `Cargo.lock` because the `sqlx` crate declares
`sqlx-sqlite` as an optional dependency. Cargo's lockfile pins all optional deps
regardless of feature selection. Our `sqlx` features are `["runtime-tokio",
"postgres", "chrono", "uuid", "json"]` — no `sqlite`. The crate is **never
compiled, never linked, not in the dependency tree**.

**Resolution**: No action needed. This is standard Cargo lockfile behavior.
If ecosystem policy requires zero lockfile stanzas for banned crates, the only
fix is for upstream `sqlx` to split `sqlx-sqlite` into a separate crate (already
requested: https://github.com/launchbadge/sqlx/issues).

### `sled` — feature-gated, deprecated

```
sled v0.34.7
└── sweet-grass-store-sled v0.7.27
    [feature: sled]
    └── sweet-grass-service v0.7.27
```

`sled` is **not in default features**. It only compiles when
`--features sled` is explicitly passed. `SledStore` is `#[deprecated(since =
"0.7.26")]` with migration docs pointing to redb. The `sweet-grass-store-sled`
crate exists for backward compatibility during migration.

**Resolution path**: Remove `sweet-grass-store-sled` crate entirely once all
deployments have migrated to redb or nestgate backends.

### `async-trait` — transitive dev-dependency only

```
async-trait v0.1.89
└── testcontainers v0.23.3
    [dev-dependencies]
    └── sweet-grass-store-postgres v0.7.27
```

Zero direct usage. Present only because `testcontainers` still depends on it
internally. Clears when testcontainers updates.

---

## Verification

```
cargo test --all-features       → 1,504 pass, 0 fail
cargo clippy --all-features --tests -- -D warnings → 0 warnings
cargo fmt --check               → 0 issues
cargo deny check bans           → pass
```

---

## For primalSpring Gap Registry

sweetGrass row in `STADIAL_PARITY_GATE_APR16_2026.md` should update to:

| sweetGrass | **No** | 0 | 2 | **INTERSTADIAL-READY** |

Lockfile ghosts (`ring`, `libsqlite3-sys`) are dev-dep / phantom only.
`sled` is feature-gated, not in defaults.

---

**License**: AGPL-3.0-or-later
