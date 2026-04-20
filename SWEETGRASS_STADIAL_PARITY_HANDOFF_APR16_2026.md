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

### `libsqlite3-sys` — **ELIMINATED** (April 16, 2026)

`sqlx` dependency updated to `default-features = false` with explicit feature
list `["runtime-tokio", "postgres", "chrono", "uuid", "json", "migrate"]`.
This removes `sqlx-sqlite`, `sqlx-mysql`, and `libsqlite3-sys` from the
resolved build graph entirely. Verified:

```
cargo tree -i libsqlite3-sys → "warning: nothing to print"
cargo tree -i libsqlite3-sys --target all → "warning: nothing to print"
```

Lockfile metadata entries may persist (Cargo v4 artifact) but are never
compiled or linked.

### `sled` — **ELIMINATED** (April 16, 2026)

`sweet-grass-store-sled` removed from workspace members, archived to
`archive/sweet-grass-store-sled/`. `sled` (0.34.7) and all its transitive deps
(`parking_lot 0.11`, `fxhash`, `crc32fast`, `fs2`, old `hashbrown`) purged from
`Cargo.lock`. `BraidBackend::Sled` variant, factory codepath, CLI arg, and
`DEFAULT_SLED_PATH` constant all removed. 79 sled tests archived (not deleted).
Lockfile now has **zero** `sled` entries.

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
cargo test --all-features       → 1,436 pass, 0 fail
cargo clippy --all-features --tests -- -D warnings → 0 warnings
cargo fmt --check               → 0 issues
cargo deny check                → advisories ok, bans ok, licenses ok, sources ok
RUSTDOCFLAGS="-D warnings" cargo doc --all-features --no-deps → 0 warnings
```

---

## BTSP First-Byte Auto-Detection — April 20, 2026

Resolved primalSpring Phase 45 audit item: plain `health.check` probes
were rejected with EPIPE/ECONNRESET when BTSP was required. The server
now peeks the first byte on every connection when BTSP mode is active:

- `{` (0x7B) → raw newline-delimited JSON-RPC (health probes, biomeOS, springs)
- anything else → BTSP 4-byte length-prefixed handshake

Implementation:
- `PeekedStream<S>` wrapper (`peek.rs`) — zero-copy first-byte re-presentation
- UDS: reads 1 byte, wraps in `PeekedStream`, routes to handler
- TCP: uses `TcpStream::peek()` (non-consuming), routes directly
- Handlers now generic: `impl AsyncRead + AsyncWrite + Unpin + Send`
- 6 new tests (PeekedStream unit, UDS auto-detect roundtrip/sequential/concurrent)

Matches `BearDog` (PG-35) and `Squirrel` (PG-30) ecosystem pattern per
`PRIMALSPRING_V0917_PHASE45_PRIMAL_EVOLUTION_HANDOFF_APR2026.md`.

---

## For primalSpring Gap Registry

sweetGrass row in `STADIAL_PARITY_GATE_APR16_2026.md` updated to **COMPLETE**
(confirmed in primalSpring's gate doc: `| sweetGrass | **No** | 0 | BraidBackend enum, RPITIT | **COMPLETE** |`).

Lockfile ghosts (`ring`, `libsqlite3-sys`) are dev-dep / phantom only.
`sled` is **eliminated** (crate archived, zero lockfile entries).

Post-gate evolution (April 2026):
- BTSP first-byte auto-detect (`PeekedStream`, PG-35/PG-30 pattern)
- Shared ecosystem path constants (`primal_names::paths`, `primal_names::env_vars`)
- All `#[expect]` carry `reason` strings
- 185 .rs files, 50,053 LOC, 1,436 tests, 91.7% coverage

---

**License**: AGPL-3.0-or-later
